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
    2. calibration    les derniers passages de l'entraînement (part_calibration, 25 % par défaut) :
                        a. choix des réglages (C, portée du noyau) : celui de meilleure AUC ;
                        b. calibration de Platt du score du modèle choisi : P(grave | f) = 1/(1 + e^{A f + B}) ;
    3. évaluation     le mois M, jamais vu : probabilité calibrée, alerte si P ≥ s*.
Platt doit être appris sur des passages NON utilisés pour apprendre le modèle : sur l'apprentissage lui-même,
les scores sont trop confiants (le modèle les a appris par cœur), et les probabilités le seraient aussi.

Coûts de classe C₊/C₋ (banc T3)
--------------------------------
    egaux       C₊ = C₋ = 1
    equilibre   C₊/C₋ = n₋/n₊ sur l'apprentissage : chaque classe pèse autant au total
    service     C₊/C₋ = c₊/c₋, le rapport des coûts fixé avec le service (le même que pour le seuil s*)
"""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd
import torch

from svr.classification import CalibrationPlatt, auc
from svr.modeles import TYPE, Entrainement

from .modeles import fabrique
from .variables import Preparateur, TableauTriage

COUTS = ("egaux", "equilibre", "service")


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


def evaluer(tab: TableauTriage, decoupages: list[Decoupage], config: ConfigTriage) -> dict:
    """Probabilités calibrées, hors échantillon, pour tous les passages évalués (voir l'en-tête)."""
    ys, ps, scores, idx_eval, choix = [], [], [], [], []
    for dec in decoupages:
        ordre = dec.entrainement[torch.argsort(torch.tensor(tab.dates[dec.entrainement.numpy()].asi8))]
        n_cal = max(1, int(round(config.part_calibration * len(ordre))))
        app, cal = ordre[:-n_cal], ordre[-n_cal:]
        y_app, y_cal = tab.y[app], tab.y[cal]
        if len(torch.unique(y_app)) < 2 or len(torch.unique(y_cal)) < 2:
            choix.append({"mois": f"{dec.mois:%Y-%m}", "ignore": "une seule classe à l'apprentissage ou à la calibration"})
            continue
        prep = Preparateur(tab.continues).ajuster(tab.X[app])
        Xa, Xc, Xe = (prep.transformer(tab.X[i]) for i in (app, cal, dec.evaluation))
        cp, cn = rapport_classes(y_app, config.couts, config.rapport_couts)
        grille = [(None, None)] if config.modele in ("regle", "arbre", "foret") else \
            [(C, g) for C in config.grille_C for g in (config.grille_portee if config.modele.startswith("svm_") and
                                                         config.modele != "svm_lineaire" else (1.0,))]
        meilleur = None
        for C, g in grille:
            fab = fabrique(config.modele, C or 1.0, g or 1.0, cp, cn, tab.blocs, config.entrainement)
            s_cal, s_ev = _scores(config.modele, fab, Xa, y_app, [Xc, Xe], [tab.alertes[cal], tab.alertes[dec.evaluation]])
            a = auc(s_cal, y_cal)
            if meilleur is None or a > meilleur[0] + 1e-12:
                meilleur = (a, C, g, s_cal, s_ev)
        a, C, g, s_cal, s_ev = meilleur
        platt = CalibrationPlatt().ajuster(s_cal, y_cal)
        ps.append(platt.probabilite(s_ev))
        scores.append(s_ev.to(TYPE))
        ys.append(tab.y[dec.evaluation])
        idx_eval.append(dec.evaluation)
        choix.append({"mois": f"{dec.mois:%Y-%m}", "apprentissage": len(app), "calibration": len(cal),
                      "evaluation": len(dec.evaluation), "C": C, "portee": g, "C_plus_sur_C_moins": round(cp / cn, 3),
                      "auc_calibration": round(a, 4), "platt_A": round(platt.A, 4), "platt_B": round(platt.B, 4)})
    if not ys:
        raise ValueError("Aucun mois évaluable (classes absentes de l'apprentissage ou de la calibration).")
    idx = torch.cat(idx_eval)
    return {"y": torch.cat(ys), "p": torch.cat(ps), "score": torch.cat(scores), "indices": idx,
            "dates": tab.dates[idx.numpy()], "meo": tab.meo[idx], "choix": choix}
