r"""
Module triage : lecture du registre des urgences, modèle principal, bancs d'essai T1 à T8 et raccordement
des modèles enfants et adultes.

Usage (WSL, depuis nera-modele/module_triage) :
    ~/memoire-env/bin/python lancer_triage.py <CSV du registre URG exporté par l'outil>
    ~/memoire-env/bin/python lancer_triage.py urg.csv --bancs T2 T3 --groupes enfant
    ~/memoire-env/bin/python lancer_triage.py urg.csv --rapide              (essai rapide de la chaîne)
    ~/memoire-env/bin/python lancer_triage.py urg.csv --extraction 2026-10-31 --confirmation "…"   (test final)

Enfants (< 15 ans) et adultes sont TOUJOURS modélisés séparément (protocole) ; le banc T6 vérifie ce choix.
Sorties (jamais sur GitHub) : resultats/triage/ — description des passages, mesures de chaque banc (CSV),
réglages choisis chaque mois (JSON) et un rapport lisible (triage_rapport.md).
Pour le lien avec le module lit (module_lit/lien_triage_lits.py) :
    probabilites_<groupe>.csv   P(grave) du modèle principal pour chaque passage : p_chronologique (validation
                                mensuelle, vide les premiers mois) et p_croisee (chaque mois prédit sans lui)
    passages_<groupe>.csv       nombre de passages par jour (avec ou sans décision lisible)

Modèle principal : SVM à noyau RBF, constantes en écart à la norme de l'âge, plaintes, contexte et
indicatrices de valeurs manquantes, MEO comptée grave, coûts de classe équilibrés, probabilité de Platt,
alerte si P(grave) ≥ s* = 1/(1 + c₊/c₋).

| Banc | Question                                   | Variantes                                               |
|------|--------------------------------------------|---------------------------------------------------------|
| T1   | place de la mise en observation            | grave, non grave, exclue                                |
| T2   | modèle                                     | règle de seuils, logistique, arbre, forêt, SVM linéaire, RBF, composite |
| T3   | coûts de classe C₊/C₋                      | égaux, équilibrés (n₋/n₊), rapport du service           |
| T4   | variables                                  | constantes ; + plaintes ; + contexte ; + manquants      |
| T5   | forme des constantes                       | brutes, écart à la norme de l'âge, seuils d'alerte      |
| T6   | enfants et adultes séparés ou ensemble     | modèle du groupe, modèle commun                         |
| T7   | représentation des variables               | originales, ACP, AFDM, k-means, originales + k-means    |
| T8   | valeurs manquantes                         | cas complets, colonnes retirées, médiane, moyenne,      |
|      |                                            | médiane par âge, k-NN, régressions enchaînées, EM, ACP  |
| T9   | transfert d'un SVM pré-entraîné sur NHAMCS | Cameroun seul (Fourier), source seule, source recalibrée,|
|      | (urgences des États-Unis, > 100 000)       | réunies, augmentation (Daumé), régularisation biaisée,  |
|      |                                            | A-SVM, score de la source comme variable                |
T9 demande la source préparée une fois par preparer_nhamcs.py (option --source-externe) ; sans elle, T9 est ignoré.
Raccordement (après les groupes) : les prévisions des modèles enfants et adultes sont réunies et comparées,
sur TOUS les passages des urgences, au modèle commun appris sur tout le monde (McNemar, mêmes passages).
Chaque variante est comparée à la référence du banc par le test de McNemar sur les mêmes passages.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
from pathlib import Path

import pandas as pd
import torch

import triage  # noqa: F401  (rend le dossier module_lit importable)
from svr.modeles import Entrainement
from traitement import verrou
from traitement.urgences import decrire, lire_passages
from triage.mesures import mcnemar, resume, seuil_optimal
from triage.modeles import MODELES
from triage.validation import COUTS, ConfigTriage, decoupage_final, decoupages_croises, decoupages_mensuels, evaluer
from triage.imputation import IMPUTATIONS
from triage.transfert import SOURCES, ConfigTransfert, Pretraine, evaluer_transfert, lire_source
from triage.representations import REPRESENTATIONS
from triage.variables import FORMES, MEO, OptionsVariables, construire

BANCS = ("T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9")
SOURCE_EXTERNE = "/mnt/c/Users/User/Desktop/MEMOIRE/donnees_externes/nhamcs/passages_nhamcs.csv.gz"


def en_markdown(t: pd.DataFrame) -> str:
    """Tableau markdown écrit à la main (pas de dépendance supplémentaire)."""
    lignes = ["| " + " | ".join(t.columns) + " |", "|" + "---|" * len(t.columns)]
    for _, rangee in t.iterrows():
        lignes.append("| " + " | ".join("" if pd.isna(v) else str(v) for v in rangee) + " |")
    return "\n".join(lignes)


class Banc:
    """Évalue des variantes sur un groupe et compare chacune à la référence du banc (McNemar)."""

    def __init__(self, passages: pd.DataFrame, decouper, seuil: float, rapport_couts: float):
        self.passages, self.decouper, self.seuil, self.rapport = passages, decouper, seuil, rapport_couts
        self.choix = {}
        self.reference = None            # résultats du modèle principal (exportés pour le module lit)
        self.source = None               # passages NHAMCS du groupe (banc T9)
        self.cfg_transfert = ConfigTransfert()
        self.pretraine, self.transferts = None, {}

    def lancer(self, options: OptionsVariables, config: ConfigTriage, passages: pd.DataFrame | None = None):
        tab = construire(self.passages if passages is None else passages, options)
        res = evaluer(tab, self.decouper(tab.dates), config)
        res["groupe"] = [tab.groupe[i] for i in res["indices"].tolist()]
        return res

    def ligne(self, banc: str, variante: str, res: dict, reference: dict | None, masque=None) -> dict:
        y, p = res["y"], res["p"]
        if masque is not None:
            y, p = y[masque], p[masque]
        ligne = {"banc": banc, "variante": variante, **resume(y, p, self.seuil, self.rapport)}
        if reference is not None and reference is not res and torch.equal(reference["indices"], res["indices"]):
            t = mcnemar(res["y"], res["p"] >= self.seuil, reference["p"] >= self.seuil)
            ligne.update({"mcnemar_b": t["b"], "mcnemar_c": t["c"], "mcnemar_p": t["p_valeur"]})
        self.choix[f"{banc} {variante}"] = res["choix"]
        return ligne


def bancs_du_groupe(b: Banc, bancs: list[str], opts: OptionsVariables, cfg: ConfigTriage,
                    tous: pd.DataFrame, groupe: str) -> list[dict]:
    lignes = []
    ref = b.lancer(opts, cfg)
    b.reference = ref
    lignes.append(b.ligne("principal", "modèle principal", ref, None))
    print(f"  modèle principal : sensibilité {lignes[-1]['sensibilite']:.3f}, AUC {lignes[-1]['auc']:.3f}")
    if "T1" in bancs:
        for meo in MEO:
            r = ref if meo == opts.meo else b.lancer(dataclasses.replace(opts, meo=meo), cfg)
            lignes.append(b.ligne("T1", f"MEO {meo}", r, None))
            lignes.append(b.ligne("T1", f"MEO {meo} (passages hors MEO)", r, None, masque=r["meo"] == 0))
    if "T2" in bancs:
        regle = b.lancer(opts, dataclasses.replace(cfg, modele="regle"))
        for m in MODELES:
            r = regle if m == "regle" else ref if m == cfg.modele else b.lancer(opts, dataclasses.replace(cfg, modele=m))
            lignes.append(b.ligne("T2", m, r, regle))
            print(f"  T2 {m:<14} sensibilité {lignes[-1]['sensibilite']:.3f}, AUC {lignes[-1]['auc']:.3f}")
    if "T3" in bancs:
        for c in COUTS:
            r = ref if c == cfg.couts else b.lancer(opts, dataclasses.replace(cfg, couts=c))
            lignes.append(b.ligne("T3", f"coûts {c}", r, ref))
    if "T4" in bancs:
        etapes = [("constantes seules", dict(plaintes=False, contexte=False, manquants=False)),
                  ("+ plaintes", dict(plaintes=True, contexte=False, manquants=False)),
                  ("+ contexte", dict(plaintes=True, contexte=True, manquants=False)),
                  ("+ manquants", dict(plaintes=True, contexte=True, manquants=True))]
        for nom, o in etapes:
            o2 = dataclasses.replace(opts, **o)
            r = ref if o2 == opts else b.lancer(o2, cfg)
            lignes.append(b.ligne("T4", nom, r, ref))
    if "T5" in bancs:
        for f in FORMES:
            r = ref if f == opts.constantes else b.lancer(dataclasses.replace(opts, constantes=f), cfg)
            lignes.append(b.ligne("T5", f"constantes {f}", r, ref))
    if "T7" in bancs:
        for rp in REPRESENTATIONS:
            r = ref if rp == cfg.representation else b.lancer(opts, dataclasses.replace(cfg, representation=rp))
            lignes.append(b.ligne("T7", rp, r, ref))
            print(f"  T7 {rp:<15} sensibilité {lignes[-1]['sensibilite']:.3f}, AUC {lignes[-1]['auc']:.3f}")
    if "T8" in bancs:
        for imp in IMPUTATIONS:
            try:
                r = ref if imp == cfg.imputation else b.lancer(opts, dataclasses.replace(cfg, imputation=imp))
            except ValueError as e:
                print(f"  T8 {imp:<20} impossible : {e}")
                continue
            if imp == "suppression_lignes":
                # Moins de passages : on compare aussi la référence sur ces seuls passages complets.
                lignes.append(b.ligne("T8", "cas complets", r, None))
                gardes = set(r["indices"].tolist())
                masque = torch.tensor([i in gardes for i in ref["indices"].tolist()])
                lignes.append(b.ligne("T8", f"{cfg.imputation} (mêmes passages complets)", ref, None, masque=masque))
            else:
                lignes.append(b.ligne("T8", imp, r, ref))
            print(f"  T8 {imp:<20} passages {lignes[-1]['passages']}, sensibilité {lignes[-1]['sensibilite']:.3f}, "
                  f"AUC {lignes[-1]['auc']:.3f}")
    if "T9" in bancs and b.source is not None and len(b.source):
        print(f"  T9 pré-entraînement sur {len(b.source)} passages NHAMCS ({groupe})…")
        tab = construire(b.passages, opts)
        b.pretraine = Pretraine(construire(b.source, opts), tab, b.cfg_transfert)
        print(f"     {b.pretraine.description()}")
        b.choix["T9 pré-entraînement"] = b.pretraine.description()
        b.transferts = evaluer_transfert(tab, b.decouper(tab.dates), b.pretraine, b.cfg_transfert)
        temoin = b.transferts.get("cible_fourier")
        for v, r in b.transferts.items():
            r["groupe"] = [tab.groupe[i] for i in r["indices"].tolist()]
            lignes.append(b.ligne("T9", v, r, ref))
            lignes[-1]["donnees"] = SOURCES[v]
            # Deuxième comparaison : contre le Cameroun seul dans la MÊME représentation (le transfert aide-t-il ?).
            if temoin is not None and r is not temoin and torch.equal(r["indices"], temoin["indices"]):
                t = mcnemar(r["y"], r["p"] >= b.seuil, temoin["p"] >= b.seuil)
                lignes[-1]["mcnemar_p_vs_cameroun_seul"] = t["p_valeur"]
            print(f"  T9 {v:<24} sensibilité {lignes[-1]['sensibilite']:.3f}, AUC {lignes[-1]['auc']:.3f}")
    elif "T9" in bancs:
        print("  T9 ignoré : source externe absente (lancez preparer_nhamcs.py, puis --source-externe).")
    if "T6" in bancs:
        ensemble = b.lancer(opts, cfg, passages=tous)
        masque = torch.tensor([g == groupe for g in ensemble["groupe"]])
        lignes.append(b.ligne("T6", "modèle du groupe", ref, None))
        lignes.append(b.ligne("T6", "modèle commun enfants + adultes", ensemble, None, masque=masque))
    return lignes


def raccorder(references: dict, tous: pd.DataFrame, opts: OptionsVariables, cfg: ConfigTriage, decouper,
              seuil: float, rapport_couts: float) -> list[dict]:
    """
    Les deux modèles séparés (enfants, adultes) forment UN système de triage pour toutes les urgences : chaque
    passage reçoit la probabilité du modèle de son groupe. On le compare au modèle commun (appris sur tous les
    passages), sur exactement les mêmes passages (ceux évalués par les deux), avec le même seuil s*.
    """
    print("\n══════ Raccordement enfants + adultes")
    sep = pd.concat([pd.DataFrame({"id": r["ids"], "y": r["y"].numpy(), "p": r["p"].numpy(), "groupe": g})
                     for g, r in references.items()]).set_index("id")
    commun = Banc(tous, decouper, seuil, rapport_couts).lancer(opts, cfg)
    com = pd.DataFrame({"id": commun["ids"], "y": commun["y"].numpy(), "p": commun["p"].numpy()}).set_index("id")
    communs = sep.index.intersection(com.index)
    if len(communs) < 20:
        raise ValueError("trop peu de passages évalués à la fois par les modèles séparés et le modèle commun.")
    s, c = sep.loc[communs], com.loc[communs]
    y = torch.tensor(s["y"].to_numpy(), dtype=torch.float64)
    p_sep = torch.tensor(s["p"].to_numpy(), dtype=torch.float64)
    p_com = torch.tensor(c["p"].to_numpy(), dtype=torch.float64)
    lignes = [{"banc": "raccordement", "variante": "modèles séparés réunis (référence)", **resume(y, p_sep, seuil, rapport_couts)}]
    t = mcnemar(y, p_com >= seuil, p_sep >= seuil)
    lignes.append({"banc": "raccordement", "variante": "modèle commun enfants + adultes", **resume(y, p_com, seuil, rapport_couts),
                   "mcnemar_b": t["b"], "mcnemar_c": t["c"], "mcnemar_p": t["p_valeur"]})
    for g in references:                                   # le détail par groupe, sur les mêmes passages
        m = torch.tensor((s["groupe"] == g).to_numpy())
        if m.sum() and len(torch.unique(y[m])) == 2:
            lignes.append({"banc": "raccordement", "variante": f"dont {g} : modèle séparé", **resume(y[m], p_sep[m], seuil, rapport_couts)})
            lignes.append({"banc": "raccordement", "variante": f"dont {g} : modèle commun", **resume(y[m], p_com[m], seuil, rapport_couts)})
    for l in lignes:
        l["groupe"] = "tous"
        print(f"  {l['variante']:<40} passages {l['passages']}, sensibilité {l['sensibilite']:.3f}, AUC {l['auc']:.3f}")
    return lignes


def exporter_probabilites(b: Banc, part: pd.DataFrame, opts: OptionsVariables, cfg: ConfigTriage, groupe: str,
                          sortie: Path, fin: pd.Timestamp | None) -> None:
    """
    P(grave) du modèle principal pour chaque passage, pour le lien avec le module lit : la validation mensuelle
    (p_chronologique) et, hors test final, la validation croisée par mois (p_croisee), qui couvre tous les mois.
    Si le banc T9 a tourné : les mêmes colonnes pour chaque modèle transféré (p_chronologique_<variante>, …).
    Les deux tableaux sont construits sur les mêmes passages et dans le même ordre : les indices se correspondent.
    """
    ref = b.reference
    lignes = pd.DataFrame({"date": ref["dates"].normalize(), "grave": (ref["y"] > 0).to(torch.int64).numpy(), "meo": ref["meo"].numpy(),
                           "p_chronologique": ref["p"].numpy()}, index=ref["indices"].numpy())
    if fin is not None:
        try:
            croise = Banc(part, lambda dates: decoupages_croises(dates, fin), b.seuil, b.rapport).lancer(opts, cfg)
            c = pd.DataFrame({"date": croise["dates"].normalize(), "grave": (croise["y"] > 0).to(torch.int64).numpy(), "meo": croise["meo"].numpy(),
                              "p_croisee": croise["p"].numpy()}, index=croise["indices"].numpy())
            lignes = c.join(lignes[["p_chronologique"]], how="left")
        except ValueError as e:
            print(f"  probabilités croisées impossibles : {e}")
    if b.pretraine is not None:
        # Modèles transférés (banc T9) : mêmes passages, mêmes indices du tableau ; colonnes p_<validation>_<variante>.
        for v, r in b.transferts.items():
            lignes[f"p_chronologique_{v}"] = pd.Series(r["p"].numpy(), index=r["indices"].numpy())
        if fin is not None:
            tab = construire(part, opts)
            try:
                for v, r in evaluer_transfert(tab, decoupages_croises(tab.dates, fin), b.pretraine, b.cfg_transfert).items():
                    lignes[f"p_croisee_{v}"] = pd.Series(r["p"].numpy(), index=r["indices"].numpy())
            except ValueError as e:
                print(f"  probabilités croisées des modèles transférés impossibles : {e}")
    lignes.sort_values("date").to_csv(sortie / f"probabilites_{groupe}.csv", index=False, encoding="utf-8")
    jours = pd.to_datetime(part["date_passage"]).dt.normalize().value_counts().sort_index()
    jours.rename_axis("date").rename("passages").reset_index().to_csv(sortie / f"passages_{groupe}.csv", index=False, encoding="utf-8")
    print(f"  probabilités par passage écrites : probabilites_{groupe}.csv ({len(lignes)} passages)")


def main() -> None:
    p = argparse.ArgumentParser(description="Module triage NERA : modèle principal et bancs d'essai.")
    p.add_argument("export", help="CSV du registre URG exporté par l'outil de saisie")
    p.add_argument("--groupes", nargs="+", default=["enfant", "adulte"], choices=["enfant", "adulte"])
    p.add_argument("--bancs", nargs="+", default=list(BANCS), choices=BANCS)
    p.add_argument("--rapport-couts", type=float, default=4.0, help="c₊/c₋ : coût d'un grave manqué / d'une fausse alerte (4)")
    p.add_argument("--mois-min", type=int, default=2, help="mois de données avant le premier mois évalué (2)")
    p.add_argument("--rapide", action="store_true", help="essai de la chaîne : peu d'itérations, pas de grille")
    p.add_argument("--source-externe", default=SOURCE_EXTERNE, help="passages NHAMCS préparés (banc T9)")
    p.add_argument("--fourier", type=int, default=500, help="T9 : nombre de caractéristiques de Fourier aléatoires (500)")
    p.add_argument("--extraction", help="test final : date du relevé du registre (aaaa-mm-jj)")
    p.add_argument("--confirmation", help="test final : phrase d'ouverture du coffre")
    a = p.parse_args()

    final = a.confirmation is not None
    if final:
        if not a.extraction:
            raise SystemExit("Le test final demande --extraction (date du relevé).")
        verrou.ouvrir_coffre(a.confirmation)
    sortie = Path("resultats") / "triage"
    sortie.mkdir(parents=True, exist_ok=True)

    passages, lecture = lire_passages(a.export)
    if len(passages) == 0:
        raise SystemExit("Aucun passage lisible dans ce fichier.")
    fin = pd.Timestamp(a.extraction) + pd.Timedelta(days=1) if final else verrou.DATE_VERROU
    passages = passages[passages["date_passage"] < fin].reset_index(drop=True)
    print(f"{lecture['passages']} passages lus ; {len(passages)} avant le {fin:%d/%m/%Y} "
          f"(date illisible : {lecture['date_illisible']}, valeurs écrites mais illisibles : {lecture['valeurs_ecrites_mais_illisibles']})")
    description = decrire(passages)
    description.to_csv(sortie / "description.csv", index=False, encoding="utf-8")
    print(description.to_string(index=False))

    seuil = seuil_optimal(a.rapport_couts)
    opts = OptionsVariables()
    cfg = ConfigTriage(rapport_couts=a.rapport_couts)
    if a.rapide:
        cfg = dataclasses.replace(cfg, grille_C=(1.0,), grille_portee=(1.0,), entrainement=Entrainement(iterations=300))
    if final:
        decouper = lambda dates: [decoupage_final(dates, verrou.DATE_VERROU)]
        bancs = []                                   # au test final : le modèle retenu seulement, rien n'est choisi
    else:
        decouper = lambda dates: decoupages_mensuels(dates, verrou.DATE_VERROU, a.mois_min)
        bancs = a.bancs
    passages["id_passage"] = range(len(passages))           # pour raccorder les modèles enfants et adultes
    tous = passages[passages["groupe"].notna()].reset_index(drop=True)

    rapport = [f"# Triage — {'test final' if final else 'validation mensuelle'}\n",
               f"Seuil d'alerte s* = 1/(1 + {a.rapport_couts:g}) = {seuil:.3f}. Mesures sur les passages jamais vus.\n"]
    tout, references = [], {}
    for g in a.groupes:
        part = passages[passages["groupe"] == g].reset_index(drop=True)
        print(f"\n══════ {g} : {len(part)} passages")
        if len(part) < 50:
            print("  trop peu de passages pour apprendre (moins de 50) : groupe ignoré")
            continue
        b = Banc(part, decouper, seuil, a.rapport_couts)
        b.cfg_transfert = ConfigTransfert(D=a.fourier, entrainement=cfg.entrainement)
        if "T9" in bancs and Path(a.source_externe).exists():
            b.source = lire_source(a.source_externe, g)
        try:
            lignes = bancs_du_groupe(b, bancs, opts, cfg, tous, g)
        except ValueError as e:
            print(f"  impossible : {e}")
            continue
        for l in lignes:
            l["groupe"] = g
        tout += lignes
        exporter_probabilites(b, part, opts, cfg, g, sortie, None if final else fin)
        references[g] = b.reference
        (sortie / f"choix_{g}.json").write_text(json.dumps(b.choix, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
        df = pd.DataFrame(lignes)
        rapport.append(f"\n## {g.capitalize()}\n")
        colonnes = ["banc", "variante"] + [c for c in ("donnees",) if c in df] + ["passages", "graves", "sensibilite",
                    "specificite", "sous_triage", "sur_triage", "vpp", "cout_moyen", "auc", "brier"] + \
                   [c for c in ("mcnemar_p", "mcnemar_p_vs_cameroun_seul") if c in df]
        rapport.append(en_markdown(df[colonnes].round(3)))
    if len(references) == 2:
        try:
            lignes = raccorder(references, tous, opts, cfg, decouper, seuil, a.rapport_couts)
            tout += lignes
            df = pd.DataFrame(lignes)
            rapport.append("\n## Raccordement : enfants et adultes réunis, tous les passages des urgences\n")
            rapport.append("Modèles séparés (chacun sur son groupe) réunis, comparés au modèle commun sur les mêmes passages.\n")
            rapport.append(en_markdown(df[["banc", "variante", "passages", "graves", "sensibilite", "specificite", "sous_triage",
                                           "sur_triage", "vpp", "cout_moyen", "auc", "brier"]
                                          + [c for c in ("mcnemar_p",) if c in df]].round(3)))
        except ValueError as e:
            print(f"\nRaccordement impossible : {e}")
    if tout:
        pd.DataFrame(tout).to_csv(sortie / "bancs.csv", index=False, encoding="utf-8")
    (sortie / "triage_rapport.md").write_text("\n".join(rapport) + "\n", encoding="utf-8")
    print(f"\nRésultats : {sortie}/")


if __name__ == "__main__":
    main()
