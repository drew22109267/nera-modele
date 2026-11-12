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
    probabilites_<groupe>.csv   pour chaque passage : niveau vrai (0 non grave, 1 moyen, 2 grave), P(grave ou moyen)
                                (p_chronologique : validation mensuelle, vide les premiers mois ; p_croisee : chaque
                                mois prédit sans lui), P(grave), P(moyen) et la priorité donnée (0, 1, 2)
    passages_<groupe>.csv       nombre de passages par jour (avec ou sans décision lisible)

TROIS NIVEAUX DE PRIORITÉ (triage/ordinal.py) : grave (rouge, priorité 1), moyen = mise en observation (jaune,
priorité 2), non grave (vert, priorité 3). Classification ordinale de Frank et Hall : deux SVM binaires,
« grave » contre le reste et « grave ou moyen » contre non grave, chacun calibré par Platt ; P(moyen) est leur
différence. Priorité donnée = celle de plus petit coût attendu, avec la matrice des coûts c(i, j) = r (i − j) en
sous-triage, (j − i) en sur-triage, r = c₊/c₋. Chaque variante d'un banc est donc apprise deux fois.

Modèle principal : SVM à noyau RBF, constantes en écart à la norme de l'âge, plaintes, contexte et
indicatrices de valeurs manquantes, coûts de classe équilibrés, probabilités de Platt.

| Banc | Question                                   | Variantes                                               |
|------|--------------------------------------------|---------------------------------------------------------|
| T1   | trois niveaux ou deux                      | 3 niveaux ; 2 niveaux MEO comptée grave ; MEO non grave |
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
| T10  | valeurs manquantes × modèles (croisé)      | chaque traitement de T8 avec chaque modèle de T2        |
| T11  | plaintes × modèles (croisé)                | familles fixées à l'avance, sac de mots, familles + mots,|
|      |                                            | sans plaintes ; chacune avec chaque modèle de T2        |
| T12  | passages d'âge illisible, groupe déduit    | avec, sans (comparés sur les passages d'âge écrit)      |
|      | de la profession                           |                                                         |
| T13  | rapport des coûts r = c₊/c₋                | 1, 2, 3, 4, 6 : mêmes probabilités, matrice des coûts r |
| T14  | mise à l'échelle des constantes            | z-score, robuste (médiane, Q3 − Q1), min-max, aucune    |
| T15  | sélection des variables par le lasso       | toutes, lasso (λ par validation croisée), lasso 1 écart-type |
MEO : niveau MOYEN, entre grave et non grave (choix clinique fixé à l'avance, pas d'après le score). T1 lit, sur
les mêmes passages et les mêmes probabilités, ce qu'aurait donné l'ancien triage à deux niveaux (rouge ou vert)
selon que la MEO est comptée grave ou non grave ; McNemar sur « priorité juste ».
Chaque ligne donne les mesures à trois niveaux (graves en rouge, sous-triage, sur-triage, kappa pondéré, coût
moyen, AUC des deux questions) et la spécificité à 90 % de sensibilité pour détecter les graves.
Sélection : le SVM (modèle, valeurs manquantes, plaintes, mise à l'échelle, lasso, transfert) de plus petit coût moyen, écrit dans
resultats/triage/choix_retenu_<groupe>.json ; --utiliser-selection le prend comme modèle principal (test final).
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
from svr.metriques import holm
from svr.modeles import Entrainement
from svr.reprise import Reprise, empreinte
from traitement import verrou
from traitement.urgences import decrire, lire_passages
from triage.mesures import mcnemar_justes, resume, seuil_optimal, specificite_a_sensibilite
from triage.ordinal import bootstrap_cout, combiner, decider, decision_binaire, justes, resume3
from triage.modeles import FAMILLE_SVM, MODELES
from triage.validation import COUTS, SELECTIONS, ConfigTriage, decoupage_final, decoupages_croises, decoupages_mensuels, evaluer
from triage.imputation import IMPUTATIONS
from triage.transfert import SOURCES, ConfigTransfert, Pretraine, evaluer_transfert, lire_source
from triage.representations import REPRESENTATIONS
from triage.variables import ECHELLES, FORMES, OptionsVariables, construire, vocabulaire

BANCS = ("T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12", "T13", "T14", "T15")
RAPPORTS_COUTS = (1.0, 2.0, 3.0, 4.0, 6.0)
PLAINTES_VARIANTES = ("familles", "mots", "familles + mots", "sans plaintes")
SOURCE_EXTERNE = "/mnt/c/Users/User/Desktop/MEMOIRE/donnees_externes/nhamcs/passages_nhamcs.csv.gz"
# Reprise après coupure (svr/reprise.py) : chaque modèle évalué est enregistré dès qu'il est fini ; relancé, le
# programme relit ce qui est fait. Réglée dans main() ; None = pas de reprise (tests, import).
REPRISE: Reprise | None = None


def calculer(cle, fonction):
    """Résultat enregistré s'il existe (même données, mêmes options, même code), sinon calculé puis enregistré."""
    return REPRISE.calculer(cle, fonction) if REPRISE is not None else fonction()


def en_markdown(t: pd.DataFrame) -> str:
    """Tableau markdown écrit à la main (pas de dépendance supplémentaire)."""
    lignes = ["| " + " | ".join(t.columns) + " |", "|" + "---|" * len(t.columns)]
    for _, rangee in t.iterrows():
        lignes.append("| " + " | ".join("" if pd.isna(v) else str(v) for v in rangee) + " |")
    return "\n".join(lignes)


def mesurer(y, P, r: float, pred=None) -> dict:
    """
    Mesures à trois niveaux (triage/ordinal.py), avec quatre noms courts pour les affichages : sensibilite = part
    des graves mis en rouge, specificite = part des non graves laissés en vert, taux_alerte = part mise en rouge,
    auc = AUC de la question « grave ? ».
    """
    d = resume3(y, P, r, pred)
    d.update(sensibilite=d["graves_en_rouge"], specificite=d["non_graves_en_vert"], taux_alerte=d["rouges"], auc=d["auc_haut"])
    grave = torch.where(torch.as_tensor(y) == 2, 1.0, -1.0)
    d["spec_sens90"] = specificite_a_sensibilite(grave, torch.as_tensor(P)[:, 2], 0.90)
    d["spec_sens95"] = specificite_a_sensibilite(grave, torch.as_tensor(P)[:, 2], 0.95)
    return d


class Banc:
    """Évalue des variantes sur un groupe et compare chacune à la référence du banc (McNemar)."""

    def __init__(self, passages: pd.DataFrame, decouper, seuil: float, rapport_couts: float, nom_decoupage: str = ""):
        self.passages, self.decouper, self.seuil, self.rapport = passages, decouper, seuil, rapport_couts
        self.nom_decoupage = nom_decoupage           # décrit `decouper` dans la clé de reprise
        self.empreinte = empreinte(passages)
        self.choix = {}
        self.reference = None            # résultats du modèle principal (exportés pour le module lit)
        self.source = None               # passages NHAMCS du groupe (banc T9)
        self.cfg_transfert = ConfigTransfert()
        self.pretraine, self.transferts = {}, {}   # T9 : modèles pré-entraînés « haut » et « bas »
        self.vocab = ()                  # vocabulaire du sac de mots (banc T11)

    def lancer(self, options: OptionsVariables, config: ConfigTriage, passages: pd.DataFrame | None = None):
        """Trois niveaux : le modèle « grave » (MEO avec les non graves) et « grave ou moyen » (MEO avec les graves)."""
        haut = self.binaire(dataclasses.replace(options, meo="non_grave"), config, passages)
        bas = self.binaire(dataclasses.replace(options, meo="grave"), config, passages)
        return combiner(haut, bas)

    def binaire(self, options: OptionsVariables, config: ConfigTriage, passages: pd.DataFrame | None = None):
        part = self.passages if passages is None else passages
        cle = ("lancer", self.nom_decoupage, self.empreinte if passages is None else empreinte(passages),
               repr(options), repr(config))

        def calcul():
            tab = construire(part, options)
            res = evaluer(tab, self.decouper(tab.dates), config)
            res["groupe"] = [tab.groupe[i] for i in res["indices"].tolist()]
            return res
        return calculer(cle, calcul)

    def ligne(self, banc: str, variante: str, res: dict, reference: dict | None, masque=None) -> dict:
        y, P = res["y"], res["p"]
        if masque is not None:
            y, P = y[masque], P[masque]
        ligne = {"banc": banc, "variante": variante, **mesurer(y, P, self.rapport), "ordre_corrige": res.get("ordre_corrige")}
        if "seuil90" in res:                     # détection des graves au seuil s₉₀ fixé sur la calibration
            t = res["seuil90"] if masque is None else res["seuil90"][masque]
            grave = torch.where(y == 2, 1.0, -1.0)
            m = resume(grave, (P[:, 2] >= t).to(P.dtype), 0.5, self.rapport)
            ligne.update({"sens_s90": m["sensibilite"], "spec_s90": m["specificite"], "alertes_s90": m["taux_alerte"]})
        if reference is not None and reference is not res and torch.equal(reference["indices"], res["indices"]):
            pa, pb = decider(res["p"], self.rapport), decider(reference["p"], self.rapport)
            t = mcnemar_justes(*justes(res["y"], pa, pb))
            ligne.update({"mcnemar_b": t["b"], "mcnemar_c": t["c"], "mcnemar_p": t["p_valeur"]})
            bc = bootstrap_cout(res["y"], pa, pb, self.rapport, res["dates"])    # coût moyen, par jours
            ligne.update({"diff_cout": bc["diff_cout"], "diff_cout_ic95": f"[{bc['ic_bas']} ; {bc['ic_haut']}]",
                          "bootstrap_cout_p": bc["p_valeur"]})
            if "seuil90" in res and "seuil90" in reference:
                # Test du critère de sélection : chaque modèle met en rouge au-dessus de SON seuil s₉₀ ; sur les seuls
                # passages NON graves, « juste » = pas en rouge. McNemar dit si A écarte significativement plus (ou
                # moins) de non-graves que B, à détection des graves fixée (~90 %).
                ng = res["y"] != 2
                t90 = mcnemar_justes((res["p"][:, 2] < res["seuil90"])[ng], (reference["p"][:, 2] < reference["seuil90"])[ng])
                ligne.update({"spec_s90_b": t90["b"], "spec_s90_c": t90["c"], "spec_s90_p": t90["p_valeur"]})
        self.choix[f"{banc} {variante}"] = res["choix"]
        return ligne


def options_plaintes(nom: str, vocab: tuple[str, ...]) -> dict:
    """Options de variables d'une variante du banc T11."""
    return {"familles": dict(plaintes=True, mots=()), "mots": dict(plaintes=False, mots=vocab),
            "familles + mots": dict(plaintes=True, mots=vocab), "sans plaintes": dict(plaintes=False, mots=())}[nom]


def restreindre(res: dict, ids: list) -> dict:
    """Les résultats d'un modèle sur une liste de passages (identifiants), dans cet ordre."""
    position = {i: k for k, i in enumerate(res["ids"])}
    k = torch.tensor([position[i] for i in ids], dtype=torch.long)
    return {**res, "y": res["y"][k], "p": res["p"][k], "meo": res["meo"][k], "ids": list(ids),
            **({"seuil90": res["seuil90"][k]} if "seuil90" in res else {}),
            "indices": torch.tensor(list(ids), dtype=torch.long)}


def selectionner(lignes: list[dict]) -> dict:
    """
    Le meilleur SVM d'après les bancs (règle fixée à l'avance) : parmi les lignes de la famille SVM des bancs
    T2, T8, T10, T11, T14, T15 et T9 (les variantes « cas complets » sont exclues : elles ne portent pas sur tous les passages),
    la plus grande SPÉCIFICITÉ AU SEUIL s₉₀ de la question « grave ? » (seuil fixé sur la calibration pour mettre
    en rouge 90 % des graves, appliqué aux mois évalués) ; à égalité, la plus grande AUC de cette question, puis
    le plus petit coût moyen à trois niveaux. La détection des graves reste le premier critère : c'est le
    sous-triage d'un grave qui coûte le plus.
    Significativité : un candidat ne remplace le modèle principal que si sa spécificité au seuil s₉₀ est plus
    grande ET que l'écart est significatif (McNemar sur les non-graves, colonne spec_s90_p, p ajustée de Holm
    < 0,05 sur tous les candidats comparés au principal). Sinon le modèle principal, fixé avant les bancs, est
    gardé : parmi des dizaines de variantes jugées sur les mêmes mois, la plus grande spécificité est en partie
    due au hasard (biais du gagnant), comme pour la sélection du module lit.
    Tout vient de la validation mensuelle avant le verrou.
    """
    candidats = [l for l in lignes if l.get("svm") and l.get("imputation") != "suppression_lignes"
                 and l.get("cout_moyen") == l.get("cout_moyen")]
    if not candidats:
        return {}
    def spec(l):
        v = l.get("spec_s90")
        return v if v == v and v is not None else -1.0
    principal = next((l for l in lignes if l.get("banc") == "principal"), None)
    testes = [l for l in candidats if l is not principal and l.get("spec_s90_p") is not None]
    for l, ph in zip(testes, holm([l["spec_s90_p"] for l in testes])):
        l["spec_s90_p_holm"] = ph
    if principal is not None:
        gagnants = [l for l in testes if spec(l) > spec(principal) and l["spec_s90_p_holm"] < 0.05]
        candidats = gagnants or [principal]
    meilleur = min(candidats, key=lambda l: (-spec(l), -(l.get("auc") or 0), l["cout_moyen"]))
    return {k: meilleur.get(k) for k in ("banc", "variante", "modele", "imputation", "plaintes", "echelle", "selection", "transfert", "cout_moyen", "auc",
                                         "auc_bas", "kappa_pondere", "graves_en_rouge", "graves_sous_tries", "sous_triage", "sur_triage",
                                         "sensibilite", "specificite", "sens_s90", "spec_s90", "alertes_s90", "mcnemar_p",
                                         "spec_s90_p", "spec_s90_p_holm", "diff_cout", "bootstrap_cout_p")}


def bancs_du_groupe(b: Banc, bancs: list[str], opts: OptionsVariables, cfg: ConfigTriage,
                    tous: pd.DataFrame, groupe: str) -> list[dict]:
    lignes = []
    ref = b.lancer(opts, cfg)
    b.reference = ref
    lignes.append(b.ligne("principal", "modèle principal", ref, None))
    lignes[-1].update(modele=cfg.modele, imputation=cfg.imputation, svm=cfg.modele in FAMILLE_SVM)
    l0 = lignes[-1]
    print(f"  modèle principal : graves en rouge {l0['graves_en_rouge']:.3f}, sous-triage {l0['sous_triage']:.3f}, "
          f"sur-triage {l0['sur_triage']:.3f}, rouges {l0['rouges']:.1%} / jaunes {l0['jaunes']:.1%} / verts {l0['verts']:.1%}, "
          f"kappa pondéré {l0['kappa_pondere']:.3f}, AUC grave {l0['auc_haut']:.3f}, AUC grave ou moyen {l0['auc_bas']:.3f}, "
          f"spécificité à 90 % de sensibilité {l0['spec_sens90']:.3f}")
    if "T1" in bancs:
        # Trois niveaux contre deux : mêmes passages, mêmes probabilités ; l'ancien triage à deux niveaux met en rouge
        # si P(question) ≥ s* = 1/(1 + r), sinon en vert. McNemar sur « priorité juste » contre les trois niveaux.
        p3 = decider(ref["p"], b.rapport)
        lignes.append({"banc": "T1", "variante": "3 niveaux : grave, moyen (MEO), non grave", **mesurer(ref["y"], ref["p"], b.rapport, p3)})
        for question, nom in (("grave_ou_moyen", "2 niveaux, MEO comptée grave"), ("grave", "2 niveaux, MEO comptée non grave")):
            p2 = decision_binaire(ref["p"], b.seuil, question)
            mc = mcnemar_justes(*justes(ref["y"], p2, p3))
            lignes.append({"banc": "T1", "variante": nom, **mesurer(ref["y"], ref["p"], b.rapport, p2),
                           "mcnemar_b": mc["b"], "mcnemar_c": mc["c"], "mcnemar_p": mc["p_valeur"]})
            print(f"  T1 {nom:<34} exactitude {lignes[-1]['exactitude']:.3f}, sous-triage {lignes[-1]['sous_triage']:.3f}, "
                  f"coût {lignes[-1]['cout_moyen']:.3f} (3 niveaux : {lignes[-3 if question == 'grave' else -2]['cout_moyen']:.3f})")
    if "T2" in bancs:
        regle = b.lancer(opts, dataclasses.replace(cfg, modele="regle"))
        for m in MODELES:
            r = regle if m == "regle" else ref if m == cfg.modele else b.lancer(opts, dataclasses.replace(cfg, modele=m))
            lignes.append(b.ligne("T2", m, r, regle))
            lignes[-1].update(modele=m, imputation=cfg.imputation, svm=m in FAMILLE_SVM)
            print(f"  T2 {m:<24} sensibilité {lignes[-1]['sensibilite']:.3f}, alertes {lignes[-1]['taux_alerte']:.1%}, "
                  f"AUC {lignes[-1]['auc']:.3f}, spec@90 {lignes[-1]['spec_sens90']:.3f}")
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
                lignes[-1].update(modele=cfg.modele, imputation=imp, svm=cfg.modele in FAMILLE_SVM)
            print(f"  T8 {imp:<20} passages {lignes[-1]['passages']}, sensibilité {lignes[-1]['sensibilite']:.3f}, "
                  f"AUC {lignes[-1]['auc']:.3f}")
    if "T10" in bancs:
        # Croisé : chaque traitement des valeurs manquantes avec chaque modèle (la règle n'utilise pas les variables).
        for m in MODELES:
            if m == "regle":
                continue
            for imp in IMPUTATIONS:
                try:
                    r = ref if (m, imp) == (cfg.modele, cfg.imputation) else \
                        b.lancer(opts, dataclasses.replace(cfg, modele=m, imputation=imp))
                except ValueError as e:
                    print(f"  T10 {imp} × {m} impossible : {e}")
                    continue
                lignes.append(b.ligne("T10", f"{imp} × {m}", r, ref if imp != "suppression_lignes" else None))
                lignes[-1].update(modele=m, imputation=imp, svm=m in FAMILLE_SVM)
                print(f"  T10 {imp:<20} × {m:<24} coût {lignes[-1]['cout_moyen']:.3f}, AUC {lignes[-1]['auc']:.3f}")
    if "T11" in bancs:
        # Plaintes : familles fixées à l'avance, sac de mots, les deux, ou rien — croisé avec chaque modèle.
        for m in MODELES:
            if m == "regle":
                continue
            for nom in PLAINTES_VARIANTES:
                o2 = dataclasses.replace(opts, **options_plaintes(nom, b.vocab))
                c2 = dataclasses.replace(cfg, modele=m)
                r = ref if (o2, c2) == (opts, cfg) else b.lancer(o2, c2)
                lignes.append(b.ligne("T11", f"{nom} × {m}", r, ref))
                lignes[-1].update(modele=m, imputation=cfg.imputation, plaintes=nom, svm=m in FAMILLE_SVM)
                print(f"  T11 {nom:<16} × {m:<24} coût {lignes[-1]['cout_moyen']:.3f}, AUC {lignes[-1]['auc']:.3f}")
    if "T12" in bancs and "groupe_deduit" in b.passages and b.passages["groupe_deduit"].sum() > 0:
        # Passages d'âge illisible rattachés au groupe par la profession : aident-ils ? Comparaison sur les
        # passages d'âge ÉCRIT seulement (les mêmes pour les deux modèles), McNemar.
        sans = b.lancer(opts, cfg, passages=b.passages[b.passages["groupe_deduit"] == 0].reset_index(drop=True))
        dans_ref = set(ref["ids"])
        communs = [i for i in sans["ids"] if i in dans_ref]
        ref_c = restreindre(ref, communs)
        lignes.append(b.ligne("T12", "avec les groupes déduits (passages d'âge écrit)", ref_c, None))
        lignes.append(b.ligne("T12", "sans les groupes déduits", restreindre(sans, communs), ref_c))
        print(f"  T12 avec groupes déduits AUC {lignes[-2]['auc']:.3f} ; sans : AUC {lignes[-1]['auc']:.3f} "
              f"({int(b.passages['groupe_deduit'].sum())} passages déduits)")
    if "T13" in bancs:
        # Le rapport des coûts ne change pas l'apprentissage (coûts de classe équilibrés), seulement la décision :
        # mêmes probabilités, matrice des coûts de rapport r. Le coût moyen dépend de r : comparer les lignes par
        # les graves en rouge, le sous-triage, le sur-triage et la part de rouges, pas par le coût.
        for rc in RAPPORTS_COUTS:
            lignes.append({"banc": "T13", "variante": f"r = c₊/c₋ = {rc:g}", **mesurer(ref["y"], ref["p"], rc)})
            print(f"  T13 r = {rc:<3g} : graves en rouge {lignes[-1]['graves_en_rouge']:.3f}, sous-triage {lignes[-1]['sous_triage']:.3f}, "
                  f"sur-triage {lignes[-1]['sur_triage']:.3f}, rouges {lignes[-1]['rouges']:.1%}, jaunes {lignes[-1]['jaunes']:.1%}")
    if "T14" in bancs:
        # Mise à l'échelle des colonnes continues, apprise sur l'apprentissage seul ; même modèle, mêmes passages.
        for ech in ECHELLES:
            r = ref if ech == cfg.echelle else b.lancer(opts, dataclasses.replace(cfg, echelle=ech))
            lignes.append(b.ligne("T14", ech, r, ref))
            lignes[-1].update(modele=cfg.modele, imputation=cfg.imputation, echelle=ech, svm=cfg.modele in FAMILLE_SVM)
            print(f"  T14 {ech:<8} coût {lignes[-1]['cout_moyen']:.3f}, AUC {lignes[-1]['auc']:.3f}")
    if "T15" in bancs:
        # Lasso logistique appris chaque mois sur l'apprentissage seul ; le SVM n'apprend que sur les variables gardées.
        # On écrit aussi la part des mois où chaque variable est gardée (stabilité de la sélection).
        for sel in SELECTIONS:
            r = ref if sel == cfg.selection else b.lancer(opts, dataclasses.replace(cfg, selection=sel))
            lignes.append(b.ligne("T15", "toutes les variables" if sel == "aucune" else sel, r, ref))
            lignes[-1].update(modele=cfg.modele, imputation=cfg.imputation, echelle=cfg.echelle, selection=sel,
                              svm=cfg.modele in FAMILLE_SVM)
            mois = [c["lasso"] for c in r["choix"] if "lasso" in c]
            if mois:
                lignes[-1]["variables_gardees"] = round(sum(m["variables_gardees"] for m in mois) / len(mois), 1)
                compte = {}
                for m in mois:
                    for v in m["variables"]:
                        compte[v] = compte.get(v, 0) + 1
                freq = pd.DataFrame({"variable": list(compte), "part_des_mois": [n / len(mois) for n in compte.values()]})
                freq.sort_values("part_des_mois", ascending=False).to_csv(
                    Path("resultats") / "triage" / f"selection_{sel}_{groupe}.csv", index=False, encoding="utf-8")
            print(f"  T15 {sel:<10} coût {lignes[-1]['cout_moyen']:.3f}, AUC {lignes[-1]['auc']:.3f}"
                  + (f", variables gardées {lignes[-1]['variables_gardees']}" if mois else ""))
    if "T9" in bancs and b.source is not None and len(b.source):
        print(f"  T9 pré-entraînement sur {len(b.source)} passages NHAMCS ({groupe})…")
        b.transferts = transferer(b, b.passages, opts, b.decouper, b.nom_decoupage, groupe)
        print(f"     {b.pretraine['haut'].description()}")
        b.choix["T9 pré-entraînement"] = {c: m.description() for c, m in b.pretraine.items()}
        temoin = b.transferts.get("cible_fourier")
        for v, r in b.transferts.items():              # r["groupe"] est déjà rempli par transferer()
            lignes.append(b.ligne("T9", v, r, ref))
            lignes[-1].update(modele="transfert", transfert=v, svm=True)
            lignes[-1]["donnees"] = SOURCES[v]
            # Deuxième comparaison : contre le Cameroun seul dans la MÊME représentation (le transfert aide-t-il ?).
            if temoin is not None and r is not temoin and torch.equal(r["indices"], temoin["indices"]):
                t = mcnemar_justes(*justes(r["y"], decider(r["p"], b.rapport), decider(temoin["p"], b.rapport)))
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


def transferer(b: Banc, part: pd.DataFrame, opts: OptionsVariables, decouper, nom_decoupage: str, groupe: str,
               variantes: tuple | None = None) -> dict:
    """
    Banc T9 à trois niveaux : chaque variante de transfert est apprise pour la question « grave » (haut) et
    « grave ou moyen » (bas), avec un pré-entraînement NHAMCS pour chacune (NHAMCS distingue aussi la mise en
    observation), puis les deux sont réunies comme le modèle principal (triage/ordinal.py).
    """
    par, groupes = {}, None
    for cote, meo in (("haut", "non_grave"), ("bas", "grave")):
        o = dataclasses.replace(opts, meo=meo)
        tab = construire(part, o)
        groupes = tab.groupe
        cle = (groupe, nom_decoupage, empreinte(part), empreinte(b.source), repr(o), repr(b.cfg_transfert))
        if cote not in b.pretraine:
            b.pretraine[cote] = calculer(("pretraine", *cle), lambda: Pretraine(construire(b.source, o), tab, b.cfg_transfert))
        extra = (variantes,) if variantes else ()
        par[cote] = calculer(("transferts", *cle, repr(variantes)),
                             lambda: evaluer_transfert(tab, decouper(tab.dates), b.pretraine[cote], b.cfg_transfert, *extra))
    out = {}
    for v, haut in par["haut"].items():
        if v in par["bas"]:
            r = combiner(haut, par["bas"][v])
            r["groupe"] = [groupes[i] for i in r["indices"].tolist()]
            out[v] = r
    return out


def raccorder(references: dict, tous: pd.DataFrame, opts: OptionsVariables, cfg: ConfigTriage, decouper,
              seuil: float, rapport_couts: float, nom_decoupage: str = "") -> list[dict]:
    """
    Les deux modèles séparés (enfants, adultes) forment UN système de triage pour toutes les urgences : chaque
    passage reçoit la probabilité du modèle de son groupe. On le compare au modèle commun (appris sur tous les
    passages), sur exactement les mêmes passages (ceux évalués par les deux), avec le même seuil s*.
    """
    print("\n══════ Raccordement enfants + adultes")
    def cadre(r: dict, **extra) -> pd.DataFrame:
        P = r["p"].numpy()
        return pd.DataFrame({"id": r["ids"], "y": r["y"].numpy(), "p0": P[:, 0], "p1": P[:, 1], "p2": P[:, 2], **extra})
    sep = pd.concat([cadre(r, groupe=g) for g, r in references.items()]).set_index("id")
    commun = Banc(tous, decouper, seuil, rapport_couts, nom_decoupage).lancer(opts, cfg)
    com = cadre(commun).set_index("id")
    communs = sep.index.intersection(com.index)
    if len(communs) < 20:
        raise ValueError("trop peu de passages évalués à la fois par les modèles séparés et le modèle commun.")
    s, c = sep.loc[communs], com.loc[communs]
    y = torch.tensor(s["y"].to_numpy(), dtype=torch.float64)
    P_sep = torch.tensor(s[["p0", "p1", "p2"]].to_numpy(), dtype=torch.float64)
    P_com = torch.tensor(c[["p0", "p1", "p2"]].to_numpy(), dtype=torch.float64)
    lignes = [{"banc": "raccordement", "variante": "modèles séparés réunis (référence)", **mesurer(y, P_sep, rapport_couts)}]
    t = mcnemar_justes(*justes(y, decider(P_com, rapport_couts), decider(P_sep, rapport_couts)))
    lignes.append({"banc": "raccordement", "variante": "modèle commun enfants + adultes", **mesurer(y, P_com, rapport_couts),
                   "mcnemar_b": t["b"], "mcnemar_c": t["c"], "mcnemar_p": t["p_valeur"]})
    for g in references:                                   # le détail par groupe, sur les mêmes passages
        m = torch.tensor((s["groupe"] == g).to_numpy())
        if m.sum() and len(torch.unique(y[m])) >= 2:
            lignes.append({"banc": "raccordement", "variante": f"dont {g} : modèle séparé", **mesurer(y[m], P_sep[m], rapport_couts)})
            lignes.append({"banc": "raccordement", "variante": f"dont {g} : modèle commun", **mesurer(y[m], P_com[m], rapport_couts)})
    for l in lignes:
        l["groupe"] = "tous"
        print(f"  {l['variante']:<40} passages {l['passages']}, graves en rouge {l['graves_en_rouge']:.3f}, "
              f"sous-triage {l['sous_triage']:.3f}, kappa {l['kappa_pondere']:.3f}")
    return lignes


def exporter_probabilites(b: Banc, part: pd.DataFrame, opts: OptionsVariables, cfg: ConfigTriage, groupe: str,
                          sortie: Path, fin: pd.Timestamp | None) -> None:
    """
    P(grave) du modèle principal pour chaque passage, pour le lien avec le module lit : la validation mensuelle
    (p_chronologique) et, hors test final, la validation croisée par mois (p_croisee), qui couvre tous les mois.
    Si le banc T9 a tourné : les mêmes colonnes pour chaque modèle transféré (p_chronologique_<variante>, …).
    Les deux tableaux sont construits sur les mêmes passages et dans le même ordre : les indices se correspondent.
    """
    def colonnes(r: dict, suffixe: str) -> pd.DataFrame:
        P = r["p"]
        return pd.DataFrame({f"p_{suffixe}": (P[:, 1] + P[:, 2]).numpy(), f"p_grave_{suffixe}": P[:, 2].numpy(),
                             f"p_moyen_{suffixe}": P[:, 1].numpy(), f"priorite_{suffixe}": decider(P, b.rapport).numpy()},
                            index=r["indices"].numpy())

    def base(r: dict) -> pd.DataFrame:
        # « grave » = grave ou moyen (comme avant : le lien avec les lits compte la MEO, hors MEO à part) ; niveau 0/1/2.
        return pd.DataFrame({"date": r["dates"].normalize(), "niveau": r["y"].to(torch.int64).numpy(),
                             "grave": (r["y"] >= 1).to(torch.int64).numpy(), "meo": r["meo"].numpy()},
                            index=r["indices"].numpy())

    ref = b.reference
    lignes = base(ref).join(colonnes(ref, "chronologique"))
    if fin is not None:
        try:
            croise = Banc(part, lambda dates: decoupages_croises(dates, fin), b.seuil, b.rapport, f"croise {fin}").lancer(opts, cfg)
            lignes = base(croise).join(colonnes(croise, "croisee")).join(lignes.drop(columns=["date", "niveau", "grave", "meo"]), how="left")
        except ValueError as e:
            print(f"  probabilités croisées impossibles : {e}")
    if b.pretraine:
        # Modèles transférés (banc T9) : mêmes passages, mêmes indices du tableau ; colonnes p_<validation>_<variante>.
        for v, r in b.transferts.items():
            lignes[f"p_chronologique_{v}"] = pd.Series((r["p"][:, 1] + r["p"][:, 2]).numpy(), index=r["indices"].numpy())
        if fin is not None:
            try:
                croises = transferer(b, part, opts, lambda dates: decoupages_croises(dates, fin), f"croise {fin}", groupe)
                for v, r in croises.items():
                    lignes[f"p_croisee_{v}"] = pd.Series((r["p"][:, 1] + r["p"][:, 2]).numpy(), index=r["indices"].numpy())
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
    p.add_argument("--utiliser-selection", action="store_true",
                   help="modèle principal = choix_retenu_<groupe>.json (écrit par les bancs) ; à utiliser pour le test final")
    p.add_argument("--extraction", help="test final : date du relevé du registre (aaaa-mm-jj)")
    p.add_argument("--confirmation", help="test final : phrase d'ouverture du coffre")
    p.add_argument("--recommencer", action="store_true", help="ignore les résultats déjà enregistrés (svr/reprise.py)")
    p.add_argument("--fin-developpement", default="2026-01-01",
                   help="fin de la période de développement du triage (aaaa-mm-jj) : les bancs ne voient rien à partir "
                   "de cette date, qui devient le coffre du triage. Par défaut 2026-01-01 : le registre des urgences "
                   "s'arrêtant le 25/01/2026, janvier 2026 est mis de côté pour le test final.")
    a = p.parse_args()

    fin_dev = pd.Timestamp(a.fin_developpement)
    if fin_dev > verrou.DATE_VERROU:
        raise SystemExit("La fin du développement ne peut pas dépasser le verrou commun.")
    final = a.confirmation is not None
    sortie = Path("resultats") / "triage"
    sortie.mkdir(parents=True, exist_ok=True)
    if final:
        if not a.extraction:
            raise SystemExit("Le test final demande --extraction (date du relevé).")
        if pd.Timestamp(a.extraction) >= verrou.DATE_VERROU:
            verrou.ouvrir_coffre(a.confirmation)              # données après le verrou commun : coffre général
        else:                                                 # coffre propre au triage (avant le verrou commun)
            if a.confirmation != verrou.PHRASE:
                raise PermissionError(f"Coffre du triage fermé. Pour le test final uniquement, confirmez avec : « {verrou.PHRASE} ».")
            journal = sortie / "test_final_ouvertures.log"
            if journal.exists():
                print("ATTENTION : le coffre du triage a déjà été ouvert :\n" + journal.read_text(encoding="utf-8"))
            with journal.open("a", encoding="utf-8") as f:
                f.write(f"{pd.Timestamp.now():%Y-%m-%d %H:%M:%S} — test final du triage sur les passages du "
                        f"{fin_dev:%d/%m/%Y} au {pd.Timestamp(a.extraction):%d/%m/%Y}\n")

    passages, lecture = lire_passages(a.export)
    if len(passages) == 0:
        raise SystemExit("Aucun passage lisible dans ce fichier.")
    fin = pd.Timestamp(a.extraction) + pd.Timedelta(days=1) if final else fin_dev
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
        decouper = lambda dates: [decoupage_final(dates, fin_dev)]
        nom_dec = f"final {fin_dev}"
        bancs = []                                   # au test final : le modèle retenu seulement, rien n'est choisi
    else:
        decouper = lambda dates: decoupages_mensuels(dates, fin_dev, a.mois_min)
        nom_dec = f"mensuel {fin_dev} {a.mois_min}"
        bancs = a.bancs
    # Reprise après coupure (jamais au test final : il ne se fait qu'une fois, en entier).
    global REPRISE
    if not final:
        ici, lit = Path(__file__).resolve().parent, Path(__file__).resolve().parents[1] / "module_lit"
        options = {k: v for k, v in sorted(vars(a).items()) if k not in ("recommencer", "bancs", "groupes")}
        source = [Path(a.source_externe)] if Path(a.source_externe).exists() else []
        REPRISE = Reprise(Path("resultats") / "reprise" / "triage",
                          empreinte(passages, options, *source, Path(__file__), ici / "triage", lit / "svr"), a.recommencer)
    passages["id_passage"] = range(len(passages))           # pour raccorder les modèles enfants et adultes
    tous = passages[passages["groupe"].notna()].reset_index(drop=True)
    vocab = vocabulaire(passages, fin_dev)                   # texte seul, passages d'avant la fin du développement
    print(f"Sac de mots : {len(vocab)} mots écrits dans au moins 5 passages avant le {fin_dev:%d/%m/%Y}")

    rapport = [f"# Triage — {'test final' if final else 'validation mensuelle'}\n",
               f"Trois niveaux de priorité : grave (rouge), moyen = MEO (jaune), non grave (vert). Priorité donnée = plus petit "
               f"coût attendu, matrice c(i, j) = {a.rapport_couts:g} × (i − j) en sous-triage, (j − i) en sur-triage. "
               "Mesures sur les passages jamais vus.\n"]
    tout, references = [], {}
    for g in a.groupes:
        part = passages[passages["groupe"] == g].reset_index(drop=True)
        print(f"\n══════ {g} : {len(part)} passages")
        if len(part) < 50:
            print("  trop peu de passages pour apprendre (moins de 50) : groupe ignoré")
            continue
        b = Banc(part, decouper, seuil, a.rapport_couts, nom_dec)
        b.cfg_transfert = ConfigTransfert(D=a.fourier, entrainement=cfg.entrainement)
        b.vocab = vocab
        cfg_g, opts_g, sel = cfg, opts, {}
        chemin_sel = sortie / f"choix_retenu_{g}.json"
        if a.utiliser_selection and chemin_sel.exists():
            sel = json.loads(chemin_sel.read_text(encoding="utf-8"))
            if sel.get("modele") in MODELES:
                cfg_g = dataclasses.replace(cfg, modele=sel["modele"], imputation=sel.get("imputation") or cfg.imputation,
                                            echelle=sel.get("echelle") or cfg.echelle,
                                            selection=sel.get("selection") or cfg.selection)
            if sel.get("plaintes") in PLAINTES_VARIANTES:
                opts_g = dataclasses.replace(opts, **options_plaintes(sel["plaintes"], vocab))
            print(f"  modèle principal = sélection des bancs : {sel.get('variante')} ({sel.get('banc')})")
        if "T9" in bancs and Path(a.source_externe).exists():
            b.source = lire_source(a.source_externe, g)
        try:
            lignes = bancs_du_groupe(b, bancs, opts_g, cfg_g, tous, g)
            if sel.get("transfert") and Path(a.source_externe).exists():
                # La sélection est un modèle transféré : on l'évalue aussi (au test final, sur le coffre).
                b.source = lire_source(a.source_externe, g)
                r = transferer(b, part, opts_g, decouper, nom_dec, g, (sel["transfert"],))[sel["transfert"]]
                lignes.append(b.ligne("sélection", f"transfert {sel['transfert']}", r, b.reference))
        except ValueError as e:
            print(f"  impossible : {e}")
            continue
        for l in lignes:
            l["groupe"] = g
        tout += lignes
        exporter_probabilites(b, part, opts_g, cfg_g, g, sortie, None if final else fin)
        references[g] = b.reference
        (sortie / f"choix_{g}.json").write_text(json.dumps(b.choix, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
        if not final and bancs:
            choix = selectionner(lignes)
            if choix:
                chemin_sel.write_text(json.dumps(choix, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
                print(f"  ► SVM sélectionné ({g}) : {choix['variante']} [{choix['banc']}], spécificité au seuil s₉₀ "
                      f"{choix.get('spec_s90')}, AUC grave {choix['auc']:.3f}, kappa pondéré {choix.get('kappa_pondere')}, "
                      f"coût moyen {choix['cout_moyen']:.3f}")
                rapport.append(f"\n**SVM sélectionné ({g}) : {choix['variante']}** (banc {choix['banc']}) — détection des graves au "
                               f"seuil s₉₀ : sensibilité {choix.get('sens_s90')}, spécificité {choix.get('spec_s90')}, alertes "
                               f"{choix.get('alertes_s90')} ; trois niveaux : graves en rouge {choix.get('graves_en_rouge')}, sous-triage "
                               f"{choix.get('sous_triage')}, sur-triage {choix.get('sur_triage')}, kappa pondéré {choix.get('kappa_pondere')}, "
                               f"coût moyen {choix['cout_moyen']:.3f} ; AUC grave {choix['auc']:.3f}. "
                               "Règle : plus grande spécificité au seuil s₉₀ parmi les SVM des bancs T2, T8, T10, T11, T14, T15 et T9.\n")
        df = pd.DataFrame(lignes)
        rapport.append(f"\n## {g.capitalize()}\n")
        colonnes = ["banc", "variante"] + [c for c in ("donnees",) if c in df] + ["passages", "graves", "moyens", "non_graves",
                    "graves_en_rouge", "graves_sous_tries", "moyens_en_jaune", "non_graves_en_vert", "sous_triage",
                    "sur_triage", "rouges", "jaunes", "exactitude", "kappa_pondere", "cout_moyen", "auc_haut", "auc_bas",
                    "spec_sens90", "brier3"] + \
                   [c for c in ("sens_s90", "spec_s90", "alertes_s90") if c in df] + \
                   [c for c in ("mcnemar_p", "diff_cout", "bootstrap_cout_p", "spec_s90_p", "spec_s90_p_holm", "mcnemar_p_vs_cameroun_seul") if c in df]
        rapport.append(en_markdown(df[colonnes].round(3)))
    if len(references) == 2:
        try:
            lignes = raccorder(references, tous, opts, cfg, decouper, seuil, a.rapport_couts, nom_dec)
            tout += lignes
            df = pd.DataFrame(lignes)
            rapport.append("\n## Raccordement : enfants et adultes réunis, tous les passages des urgences\n")
            rapport.append("Modèles séparés (chacun sur son groupe) réunis, comparés au modèle commun sur les mêmes passages.\n")
            rapport.append(en_markdown(df[["banc", "variante"] + ["passages", "graves", "moyens", "non_graves",
                    "graves_en_rouge", "graves_sous_tries", "moyens_en_jaune", "non_graves_en_vert", "sous_triage",
                    "sur_triage", "rouges", "jaunes", "exactitude", "kappa_pondere", "cout_moyen", "auc_haut", "auc_bas",
                    "spec_sens90", "brier3"]
                                          + [c for c in ("mcnemar_p",) if c in df]].round(3)))
        except ValueError as e:
            print(f"\nRaccordement impossible : {e}")
    if tout:
        pd.DataFrame(tout).to_csv(sortie / "bancs.csv", index=False, encoding="utf-8")
    (sortie / "triage_rapport.md").write_text("\n".join(rapport) + "\n", encoding="utf-8")
    print(f"\nRésultats : {sortie}/")
    if REPRISE is not None:
        print(REPRISE.bilan())


if __name__ == "__main__":
    main()
