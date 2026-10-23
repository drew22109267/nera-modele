r"""
Module triage : lecture du registre des urgences, modèle principal et bancs d'essai T1 à T6.

Usage (WSL, depuis nera-modele/module_triage) :
    ~/memoire-env/bin/python lancer_triage.py <CSV du registre URG exporté par l'outil>
    ~/memoire-env/bin/python lancer_triage.py urg.csv --bancs T2 T3 --groupes enfant
    ~/memoire-env/bin/python lancer_triage.py urg.csv --rapide              (essai rapide de la chaîne)
    ~/memoire-env/bin/python lancer_triage.py urg.csv --extraction 2026-10-31 --confirmation "…"   (test final)

Enfants (< 15 ans) et adultes sont TOUJOURS modélisés séparément (protocole) ; le banc T6 vérifie ce choix.
Sorties (jamais sur GitHub) : resultats/triage/ — description des passages, mesures de chaque banc (CSV),
réglages choisis chaque mois (JSON) et un rapport lisible (triage_rapport.md).

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
from triage.validation import COUTS, ConfigTriage, decoupage_final, decoupages_mensuels, evaluer
from triage.variables import FORMES, MEO, OptionsVariables, construire

BANCS = ("T1", "T2", "T3", "T4", "T5", "T6")


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
    if "T6" in bancs:
        ensemble = b.lancer(opts, cfg, passages=tous)
        masque = torch.tensor([g == groupe for g in ensemble["groupe"]])
        lignes.append(b.ligne("T6", "modèle du groupe", ref, None))
        lignes.append(b.ligne("T6", "modèle commun enfants + adultes", ensemble, None, masque=masque))
    return lignes


def main() -> None:
    p = argparse.ArgumentParser(description="Module triage NERA : modèle principal et bancs d'essai.")
    p.add_argument("export", help="CSV du registre URG exporté par l'outil de saisie")
    p.add_argument("--groupes", nargs="+", default=["enfant", "adulte"], choices=["enfant", "adulte"])
    p.add_argument("--bancs", nargs="+", default=list(BANCS), choices=BANCS)
    p.add_argument("--rapport-couts", type=float, default=4.0, help="c₊/c₋ : coût d'un grave manqué / d'une fausse alerte (4)")
    p.add_argument("--mois-min", type=int, default=2, help="mois de données avant le premier mois évalué (2)")
    p.add_argument("--rapide", action="store_true", help="essai de la chaîne : peu d'itérations, pas de grille")
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
    tous = passages[passages["groupe"].notna()].reset_index(drop=True)

    rapport = [f"# Triage — {'test final' if final else 'validation mensuelle'}\n",
               f"Seuil d'alerte s* = 1/(1 + {a.rapport_couts:g}) = {seuil:.3f}. Mesures sur les passages jamais vus.\n"]
    tout = []
    for g in a.groupes:
        part = passages[passages["groupe"] == g].reset_index(drop=True)
        print(f"\n══════ {g} : {len(part)} passages")
        if len(part) < 50:
            print("  trop peu de passages pour apprendre (moins de 50) : groupe ignoré")
            continue
        b = Banc(part, decouper, seuil, a.rapport_couts)
        try:
            lignes = bancs_du_groupe(b, bancs, opts, cfg, tous, g)
        except ValueError as e:
            print(f"  impossible : {e}")
            continue
        for l in lignes:
            l["groupe"] = g
        tout += lignes
        (sortie / f"choix_{g}.json").write_text(json.dumps(b.choix, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
        df = pd.DataFrame(lignes)
        rapport.append(f"\n## {g.capitalize()}\n")
        colonnes = ["banc", "variante", "passages", "graves", "sensibilite", "specificite", "sous_triage", "sur_triage",
                    "vpp", "cout_moyen", "auc", "brier"] + [c for c in ("mcnemar_p",) if c in df]
        rapport.append(en_markdown(df[colonnes].round(3)))
    if tout:
        pd.DataFrame(tout).to_csv(sortie / "bancs.csv", index=False, encoding="utf-8")
    (sortie / "triage_rapport.md").write_text("\n".join(rapport) + "\n", encoding="utf-8")
    print(f"\nRésultats : {sortie}/")


if __name__ == "__main__":
    main()
