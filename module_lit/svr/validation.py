"""
Découpages temporels et validation glissante (protocole, étape 3.5).

Règle d'or : on n'entraîne jamais sur une information que l'on n'aurait pas eue le jour de la
prévision. Une ligne (origine t, cible t + h) n'est utilisable pour entraîner un modèle à
l'origine O que si sa cible est déjà connue :  t + h ≤ O.

1. Test final (une seule fois, à la toute fin)
   Entraînement : lignes dont la cible est antérieure au début du test.
   Test        : lignes dont l'origine est dans la période de test.
   Les lignes à cheval (origine avant le test, cible dedans) sont écartées.

2. Validation glissante « rolling origin » (pour choisir modèles et hyperparamètres)
   Sur la période d'entraînement, on avance l'origine O par pas de `pas` jours :
      à chaque O : entraînement sur toutes les lignes de cible ≤ O (fenêtre qui s'agrandit),
                   validation sur les lignes d'origine dans [O, O + pas[.
   On simule ainsi ce que le modèle aurait fait, semaine après semaine, en conditions réelles.
   La standardisation est réapprise à chaque pas, sur l'entraînement du pas.
"""
from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from multiprocessing import get_all_start_methods, get_context

import pandas as pd
import torch

from .caracteristiques import Standardiseur, Tableau


@dataclass
class Decoupage:
    entrainement: torch.Tensor      # indices des lignes du tableau
    evaluation: torch.Tensor
    origine: pd.Timestamp


def decoupage_final(tab: Tableau, debut_test: str | pd.Timestamp) -> Decoupage:
    d = pd.Timestamp(debut_test)
    entr = torch.nonzero(torch.tensor(tab.dates_cible < d)).flatten()
    test = torch.nonzero(torch.tensor(tab.dates_origine >= d)).flatten()
    if len(entr) == 0 or len(test) == 0:
        raise ValueError("Découpage vide : vérifiez la date de début du test.")
    return Decoupage(entr, test, d)


def decoupages_test_mensuels(tab: Tableau, debut_test: str | pd.Timestamp) -> list[Decoupage]:
    """
    Test final découpé en blocs d'un mois, avec réentraînement au début de chaque mois.

    Bloc m (origines du mois m) : entraînement sur toutes les lignes dont la cible précède le 1er du
    mois m, donc y compris les mois de test déjà écoulés ; c'est ce qui se passerait en service avec
    un réentraînement mensuel. Le premier bloc est identique à decoupage_final (rien du test n'est
    connu) ; les suivants montrent si réentraîner chaque mois améliore la prévision.
    """
    d = pd.Timestamp(debut_test).normalize().replace(day=1)
    fin = pd.Timestamp(tab.dates_origine.max())
    decoupages = []
    while d <= fin:
        suivant = d + pd.DateOffset(months=1)
        entr = torch.nonzero(torch.tensor(tab.dates_cible < d)).flatten()
        ev = torch.nonzero(torch.tensor((tab.dates_origine >= d) & (tab.dates_origine < suivant))).flatten()
        if len(entr) and len(ev):
            decoupages.append(Decoupage(entr, ev, d))
        d = suivant
    if not decoupages:
        raise ValueError("Découpage vide : vérifiez la date de début du test.")
    return decoupages


def origines_glissantes(tab: Tableau, debut: str | pd.Timestamp, fin: str | pd.Timestamp,
                        pas: int = 14, minimum_entrainement: int = 60) -> list[Decoupage]:
    """Découpages successifs entre `debut` et `fin` (fin exclue : typiquement le début du test)."""
    decoupages, O, fin = [], pd.Timestamp(debut), pd.Timestamp(fin)
    while O < fin:
        fin_pas = min(O + pd.Timedelta(days=pas), fin)
        entr = torch.nonzero(torch.tensor(tab.dates_cible <= O)).flatten()
        ev = torch.nonzero(torch.tensor((tab.dates_origine >= O) & (tab.dates_origine < fin_pas))).flatten()
        if len(entr) >= minimum_entrainement and len(ev):
            decoupages.append(Decoupage(entr, ev, O))
        O = fin_pas
    if not decoupages:
        raise ValueError("Aucun découpage glissant possible : période trop courte.")
    return decoupages


_TACHE = None                     # (tableau, découpages, fabrique) hérités par les processus « fork » de evaluer


def _un_pli(tab: Tableau, dec: Decoupage, fabrique):
    std = Standardiseur(tab.continues, tab.echelle).ajuster(tab.X[dec.entrainement])
    modele = fabrique().entrainer(std.transformer(tab.X[dec.entrainement]), tab.y[dec.entrainement])
    return modele.predire(std.transformer(tab.X[dec.evaluation]))


def _pli_herite(i: int):
    tab, decoupages, fabrique = _TACHE
    os.environ["NERA_PROCESSUS"] = "1"             # pas de nouveaux processus à l'intérieur d'un pli
    return _un_pli(tab, decoupages[i], fabrique)


def _processus_plis(n_plis: int, processus: int | None) -> int:
    """
    Processus pour les plis : NERA_PROCESSUS (sinon tous les cœurs), seulement si « fork » existe (Linux, WSL) et
    si torch calcule sur un seul fil (OMP_NUM_THREADS=1) : un fork après des fils OpenMP peut se bloquer. Les
    plis ne partagent rien (chaque modèle a ses propres graines) : même résultat qu'en série.
    """
    if processus is None:
        processus = int(os.environ.get("NERA_PROCESSUS", os.cpu_count() or 1))
    if processus <= 1 or n_plis <= 1 or "fork" not in get_all_start_methods() or torch.get_num_threads() != 1:
        return 1
    return min(processus, n_plis)


def evaluer(tab: Tableau, decoupages: list[Decoupage], fabrique, processus: int | None = None) -> dict:
    """
    Pour chaque découpage : standardise, entraîne `fabrique()` sur l'entraînement, prédit l'évaluation.
    Le modèle renvoie soit un tenseur (prévision ponctuelle), soit un dict {τ: tenseur} (quantiles).
    Renvoie les prévisions concaténées, alignées sur les vraies valeurs et les dates.
    Les plis sont indépendants : ils sont entraînés en parallèle quand c'est possible (voir _processus_plis),
    et rangés dans l'ordre des découpages.
    """
    global _TACHE
    n = _processus_plis(len(decoupages), processus)
    if n > 1:
        _TACHE = (tab, decoupages, fabrique)
        try:
            # Les plis au plus grand apprentissage, les plus longs, partent les premiers ; ordre rétabli ensuite.
            ordre = sorted(range(len(decoupages)), key=lambda k: -len(decoupages[k].entrainement))
            with ProcessPoolExecutor(n, mp_context=get_context("fork")) as ex:
                futurs = {k: ex.submit(_pli_herite, k) for k in ordre}
                prev = [futurs[k].result() for k in range(len(decoupages))]
        finally:
            _TACHE = None
    else:
        prev = [_un_pli(tab, dec, fabrique) for dec in decoupages]
    y_vrai = [tab.y[dec.evaluation] for dec in decoupages]
    dates = [d for dec in decoupages for d in tab.dates_cible[dec.evaluation.numpy()]]
    origines = [tab.origines[dec.evaluation] for dec in decoupages]
    if isinstance(prev[0], dict):
        prev = {tau: torch.cat([p[tau] for p in prev]) for tau in prev[0]}
    else:
        prev = torch.cat(prev)
    return {"y": torch.cat(y_vrai), "prevision": prev, "dates": pd.DatetimeIndex(dates),
            "origines": torch.cat(origines)}
