r"""
Validation du triage dans le temps, sans fuite.

Découpage mensuel (comme le réentraînement mensuel du module lit)
------------------------------------------------------------------
Pour chaque mois M (à partir du `mois_min`-ième mois de données) :
    entraînement   tous les passages AVANT le 1er du mois M ;
    évaluation     les passages du mois M.
Pendant le développement, rien n'est lu à partir de la date du verrou (traitement.verrou.DATE_VERROU,
01/09/2026) : c'est la période du test final.

Dans chaque entraînement, trois rôles, dans l'ordre du temps
------------------------------------------------------------
    1. apprentissage  les premiers (1 − part_calibration) passages : le modèle y apprend ses paramètres ;
    2. calibration    les derniers passages de l'entraînement (part_calibration, 25 % par défaut), coupés en
                      deux dans l'ordre du temps (separer_reglage, par défaut) :
                        a. première moitié, RÉGLAGE : choix des réglages (C, portée du noyau) de meilleure AUC ;
                        b. seconde moitié, CALIBRATION : Platt du score du modèle choisi,
                           P(grave | f) = 1/(1 + e^{A f + B}), et seuil s₉₀.
                      Choisir les réglages et ajuster Platt sur les mêmes passages rend les probabilités un peu
                      trop confiantes (le meilleur des réglages est en partie le plus chanceux sur ces passages) ;
                      les séparer supprime ce biais. Si une moitié n'a qu'une classe, les deux rôles reprennent
                      toute la calibration (noté « reglage_calibration_communs » dans le journal du mois) ;
    3. évaluation     le mois M, jamais vu : probabilité calibrée, alerte si P ≥ s*.
Seuil à sensibilité fixée (lecture complémentaire) : sur la calibration, s₉₀ = le plus grand seuil qui alerte
au moins 90 % des graves de la calibration ; il est appliqué tel quel au mois M (rien du mois M n'est vu). On lit
alors la sensibilité réelle, la spécificité et le taux d'alerte du mois M à ce seuil : quand s* alerte tout le
monde (taux de graves élevé), c'est cette lecture qui dit combien de non-graves le modèle permet d'écarter.
Platt doit être appris sur des passages NON utilisés pour apprendre le modèle : sur l'apprentissage lui-même,
les scores sont trop confiants (le modèle les a appris par cœur), et les probabilités le seraient aussi.

Représentation des variables (banc T7)
---------------------------------------
Après l'imputation et la standardisation, les variables peuvent être résumées (ACP, AFDM) ou remplacées
par le groupe du passage (k-means) : voir triage/representations.py. Comme Preparateur, la représentation
est apprise sur l'apprentissage seulement.

Sélection des variables par le lasso (banc T15)
-----------------------------------------------
Après la représentation, un lasso logistique (svr/lasso.py), pondéré par les coûts de classe et de λ choisi
par validation croisée en blocs consécutifs de l'apprentissage, garde les variables de coefficient non nul ;
le modèle n'apprend que sur elles. « aucune » = toutes les variables (référence).

Valeurs manquantes (banc T8)
-----------------------------
Le traitement des cases vides est appris avec Preparateur sur l'apprentissage seulement (triage/imputation.py).
« suppression_lignes » (cas complets) retire les passages incomplets de l'apprentissage, de la calibration ET
de l'évaluation : ils ne peuvent pas être prévus. Chaque résultat porte donc « complet » (aucune case vide) pour
que le banc compare aussi la référence sur ces seuls passages.

Coûts de classe C₊/C₋ (banc T3)
--------------------------------
    egaux       C₊ = C₋ = 1
    equilibre   C₊/C₋ = n₋/n₊ sur l'apprentissage : chaque classe pèse autant au total
    service     C₊/C₋ = c₊/c₋, le rapport des coûts fixé avec le service (le même que pour le seuil s*)
"""
from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_all_start_methods, get_context

import math
from dataclasses import dataclass, field

import pandas as pd
import torch

from svr.classification import CalibrationPlatt, auc
from svr.lasso import REGLES, SelectionLasso
from svr.modeles import TYPE, Entrainement

from .modeles import A_PORTEE, GRILLE_XGBOOST, fabrique
from .representations import GRILLE_GROUPES, GRILLE_PART, Representation
from .variables import Preparateur, TableauTriage

COUTS = ("egaux", "equilibre", "service")
SELECTIONS = ("aucune", *REGLES)                     # banc T15


@dataclass
class Decoupage:
    entrainement: torch.Tensor
    evaluation: torch.Tensor
    mois: pd.Timestamp


@dataclass
class ConfigTriage:
    modele: str = "svm_rbf"
    couts: str = "equilibre"
    rapport_couts: float = 4.0                         # c₊/c₋ : un grave manqué coûte 4 fausses alertes
    grille_C: tuple = (0.1, 1.0, 10.0)
    grille_portee: tuple = (0.25, 0.5, 1.0, 2.0)
    part_calibration: float = 0.25
    separer_reglage: bool = True                    # réglages sur la 1re moitié de la calibration, Platt et s₉₀ sur la 2de
    representation: str = "originales"              # banc T7 (triage/representations.py)
    imputation: str = "mediane"                     # banc T8 (triage/imputation.py)
    echelle: str = "zscore"                         # banc T14 (triage/variables.py, ECHELLES)
    selection: str = "aucune"                       # banc T15 : 'aucune', 'lasso' ou 'lasso_1se'
    entrainement: Entrainement = field(default_factory=lambda: Entrainement(iterations=2000))


def decoupages_mensuels(dates: pd.DatetimeIndex, fin: pd.Timestamp, mois_min: int = 2) -> list[Decoupage]:
    """Un découpage par mois, du `mois_min`-ième mois de données jusqu'à `fin` (exclue)."""
    d = pd.Series(dates)
    premier = d.min().normalize().replace(day=1)
    M = premier + pd.DateOffset(months=mois_min)
    decoupages = []
    while M < fin:
        suivant = min(M + pd.DateOffset(months=1), fin)
        entr = torch.nonzero(torch.tensor((d < M).to_numpy())).flatten()
        ev = torch.nonzero(torch.tensor(((d >= M) & (d < suivant)).to_numpy())).flatten()
        if len(entr) and len(ev):
            decoupages.append(Decoupage(entr, ev, M))
        M = suivant
    if not decoupages:
        raise ValueError("Aucun mois évaluable : registre trop court (il faut au moins mois_min + 1 mois).")
    return decoupages


def decoupages_croises(dates: pd.DatetimeIndex, fin: pd.Timestamp) -> list[Decoupage]:
    """
    Validation croisée par mois : chaque mois est prédit par un modèle appris sur TOUS les autres mois (avant
    `fin`), jamais sur lui-même. Sert seulement à donner une probabilité hors échantillon à CHAQUE passage, pour
    le lien avec le module lit (lien_triage_lits.py) : la validation mensuelle laisse sans prévision les premiers
    mois. Les mesures du triage, elles, restent celles de la validation mensuelle (rien du futur).
    """
    d = pd.Series(dates)
    d = d[d < fin]
    mois = sorted(d.dt.to_period("M").unique())
    if len(mois) < 2:
        raise ValueError("Validation croisée par mois : il faut au moins deux mois de passages.")
    periode = pd.Series(dates).dt.to_period("M")
    avant = pd.Series(dates) < fin
    decoupages = []
    for m in mois:
        entr = torch.nonzero(torch.tensor((avant & (periode != m)).to_numpy())).flatten()
        ev = torch.nonzero(torch.tensor((avant & (periode == m)).to_numpy())).flatten()
        if len(entr) and len(ev):
            decoupages.append(Decoupage(entr, ev, m.to_timestamp()))
    return decoupages


def decoupage_final(dates: pd.DatetimeIndex, verrou: pd.Timestamp) -> Decoupage:
    d = pd.Series(dates)
    entr = torch.nonzero(torch.tensor((d < verrou).to_numpy())).flatten()
    test = torch.nonzero(torch.tensor((d >= verrou).to_numpy())).flatten()
    if not len(entr) or not len(test):
        raise ValueError("Découpage final vide : vérifiez la date du verrou.")
    return Decoupage(entr, test, verrou)


def rapport_classes(y: torch.Tensor, couts: str, rapport_couts: float) -> tuple[float, float]:
    """(C₊, C₋) selon le choix du banc T3."""
    if couts == "egaux":
        return 1.0, 1.0
    if couts == "equilibre":
        n_pos, n_neg = int((y > 0).sum()), int((y <= 0).sum())
        return (n_neg / n_pos if n_pos else 1.0), 1.0
    if couts == "service":
        return rapport_couts, 1.0
    raise ValueError(f"Coûts inconnus : {couts}. Choix : {', '.join(COUTS)}.")


def _scores(nom: str, fab, Xa, ya, autres: list[torch.Tensor], alertes: list[torch.Tensor]) -> list[torch.Tensor]:
    """Entraîne (sauf la règle) et renvoie les scores sur chacun des ensembles `autres`."""
    if nom == "regle":
        return alertes
    modele = fab().entrainer(Xa, ya)
    return [modele.predire(X) for X in autres]


def _un_mois(tab: TableauTriage, dec: Decoupage, config: ConfigTriage, complet: torch.Tensor) -> list:
    """Un mois évalué : [y, probabilités, scores, indices, choix, seuils s₉₀], une entrée au plus par liste."""
    ys, ps, scores, idx_eval, choix, seuils90 = res = [[], [], [], [], [], []]
    if config.imputation == "suppression_lignes":         # cas complets seulement, partout
        dec = Decoupage(dec.entrainement[complet[dec.entrainement]], dec.evaluation[complet[dec.evaluation]], dec.mois)
        if not len(dec.entrainement) or not len(dec.evaluation):
            choix.append({"mois": f"{dec.mois:%Y-%m}", "ignore": "aucun passage complet"})
            return res
    ordre = dec.entrainement[torch.argsort(torch.tensor(tab.dates[dec.entrainement.numpy()].asi8))]
    n_cal = max(1, int(round(config.part_calibration * len(ordre))))
    app, cal = ordre[:-n_cal], ordre[-n_cal:]
    y_app, y_cal = tab.y[app], tab.y[cal]
    # Réglage (choix de C, portée…) sur la 1re moitié de la calibration, Platt et s₉₀ sur la 2de (voir l'en-tête).
    n_reg = len(cal) // 2
    separe = (config.separer_reglage and n_reg >= 2 and len(torch.unique(y_cal[:n_reg])) == 2
              and len(torch.unique(y_cal[n_reg:])) == 2)
    reg = slice(0, n_reg) if separe else slice(None)
    cal_platt = slice(n_reg, None) if separe else slice(None)
    if len(torch.unique(y_app)) < 2 or len(torch.unique(y_cal)) < 2:
        choix.append({"mois": f"{dec.mois:%Y-%m}", "ignore": "une seule classe à l'apprentissage ou à la calibration"})
        return res
    prep = Preparateur(tab.continues, config.imputation, config.echelle).ajuster(tab.X[app])
    Xa0, Xc0, Xe0 = (prep.transformer(tab.X[i]) for i in (app, cal, dec.evaluation))
    cp, cn = rapport_classes(y_app, config.couts, config.rapport_couts)
    # Banc T7 : ACP, AFDM ou k-means apprises sur l'apprentissage seulement, puis appliquées aux autres. Leur
    # réglage (part de variance gardée, nombre de groupes) est choisi avec C et la portée, sur la calibration.
    reglages_rep = {"acp": GRILLE_PART, "afdm": GRILLE_PART, "kmeans": GRILLE_GROUPES,
                    "origine+kmeans": GRILLE_GROUPES}.get(config.representation, (None,))
    meilleur = None
    for r_rep in reglages_rep:
        options = {} if r_rep is None else \
            {"groupes": r_rep} if "kmeans" in config.representation else {"part_variance": r_rep}
        rep_r = Representation(config.representation, tab.continues, **options).ajuster(Xa0)
        Xa, Xc, Xe = rep_r.transformer(Xa0), rep_r.transformer(Xc0), rep_r.transformer(Xe0)
        blocs = tab.blocs if config.representation == "originales" else {"constantes": list(range(Xa.shape[1])), "autres": []}
        lasso = {}
        if config.selection != "aucune":
            noms = tab.noms if config.representation == "originales" else [f"axe_{j}" for j in range(Xa.shape[1])]
            sel = SelectionLasso("logistique", config.selection).ajuster(Xa, y_app, torch.where(y_app > 0, cp, cn))
            Xa, Xc, Xe = sel.transformer(Xa), sel.transformer(Xc), sel.transformer(Xe)
            nouveau = {j: k for k, j in enumerate(sel.colonnes)}          # anciens indices → nouveaux
            blocs = {b: [nouveau[j] for j in cols if j in nouveau] for b, cols in blocs.items()}
            lasso = sel.description(noms)
        grille = [(None, None)] if config.modele in ("regle", "arbre", "foret") else GRILLE_XGBOOST \
            if config.modele == "xgboost" else \
            [(C, g) for C in config.grille_C for g in (config.grille_portee if config.modele in A_PORTEE else (1.0,))]
        for C, g in grille:
            fab = fabrique(config.modele, C or 1.0, g or 1.0, cp, cn, blocs, config.entrainement)
            s_cal, s_ev = _scores(config.modele, fab, Xa, y_app, [Xc, Xe], [tab.alertes[cal], tab.alertes[dec.evaluation]])
            a = auc(s_cal[reg], y_cal[reg])
            if meilleur is None or a > meilleur[0] + 1e-12:
                meilleur = (a, C, g, s_cal, s_ev, rep_r, lasso)
    a, C, g, s_cal, s_ev, rep, lasso = meilleur
    s_pl, y_pl = s_cal[cal_platt], y_cal[cal_platt]
    platt = CalibrationPlatt().ajuster(s_pl, y_pl)
    p_graves = torch.sort(platt.probabilite(s_pl)[y_pl > 0]).values
    s90 = float(p_graves[int(math.floor(0.10 * len(p_graves)))])      # ≥ 90 % des graves de la calibration au-dessus
    seuils90.append(torch.full((len(dec.evaluation),), s90, dtype=TYPE))
    ps.append(platt.probabilite(s_ev))
    scores.append(s_ev.to(TYPE))
    ys.append(tab.y[dec.evaluation])
    idx_eval.append(dec.evaluation)
    choix.append({"mois": f"{dec.mois:%Y-%m}", "apprentissage": len(app), "calibration": len(cal),
                  "evaluation": len(dec.evaluation), "C": C, "portee": g, "C_plus_sur_C_moins": round(cp / cn, 3),
                  "reglage": n_reg if separe else len(cal), "platt": len(cal) - n_reg if separe else len(cal),
                  **({} if separe else {"reglage_calibration_communs": True}),
                  "auc_reglage": round(a, 4), "seuil_s90": round(s90, 4), "platt_A": round(platt.A, 4), "platt_B": round(platt.B, 4),
                  "representation": config.representation, "imputation": config.imputation, **rep.description(),
                  **({"lasso": lasso} if lasso else {})})
    return res


_TACHE = None                     # (tableau, découpages, config, complet) hérités par les processus « fork »


def _mois_herite(i: int) -> list:
    tab, decoupages, config, complet = _TACHE
    os.environ["NERA_PROCESSUS"] = "1"             # pas de nouveaux processus à l'intérieur d'un mois
    return _un_mois(tab, decoupages[i], config, complet)


def _processus_mois(n: int) -> int:
    """
    Mois en parallèle : NERA_PROCESSUS (sinon tous les cœurs), seulement si « fork » existe (Linux, WSL) et si
    torch calcule sur un seul fil (OMP_NUM_THREADS=1) : un fork après des fils OpenMP peut se bloquer. Chaque mois
    a ses propres graines : même résultat qu'en série.
    """
    processus = int(os.environ.get("NERA_PROCESSUS", os.cpu_count() or 1))
    if processus <= 1 or n <= 1 or "fork" not in get_all_start_methods() or torch.get_num_threads() != 1:
        return 1
    return min(processus, n)


def evaluer(tab: TableauTriage, decoupages: list[Decoupage], config: ConfigTriage) -> dict:
    """Probabilités calibrées, hors échantillon, pour tous les passages évalués (voir l'en-tête).
    Les mois sont indépendants : évalués en parallèle quand c'est possible (_processus_mois), rangés dans l'ordre."""
    global _TACHE
    complet = ~torch.isnan(tab.X).any(dim=1)                 # passage sans aucune case vide
    n = _processus_mois(len(decoupages))
    if n > 1:
        _TACHE = (tab, decoupages, config, complet)
        try:
            # Les mois au plus grand apprentissage, les plus longs, partent les premiers ; ordre rétabli ensuite.
            ordre = sorted(range(len(decoupages)), key=lambda k: -len(decoupages[k].entrainement))
            with ProcessPoolExecutor(n, mp_context=get_context("fork")) as ex:
                futurs = {k: ex.submit(_mois_herite, k) for k in ordre}
                par_mois = [futurs[k].result() for k in range(len(decoupages))]
        finally:
            _TACHE = None
    else:
        par_mois = [_un_mois(tab, dec, config, complet) for dec in decoupages]
    ys, ps, scores, idx_eval, choix, seuils90 = ([x for m in par_mois for x in m[k]] for k in range(6))
    if not ys:
        raise ValueError("Aucun mois évaluable (classes absentes de l'apprentissage ou de la calibration).")
    idx = torch.cat(idx_eval)
    return {"y": torch.cat(ys), "p": torch.cat(ps), "score": torch.cat(scores), "indices": idx, "seuil90": torch.cat(seuils90),
            "dates": tab.dates[idx.numpy()], "meo": tab.meo[idx], "complet": complet[idx],
            "ids": [tab.ids[i] for i in idx.tolist()] if tab.ids else None, "choix": choix}
