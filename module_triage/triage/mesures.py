r"""
Mesures du triage, toutes écrites à la main.

Matrice de confusion (décision : alerte si P(grave) ≥ s)
---------------------------------------------------------
                    alerte        pas d'alerte
    grave           VP            FN  (sous-triage : un grave manqué)
    non grave       FP            VN
                    (sur-triage : fausse alerte)

    sensibilité  = VP / (VP + FN)          part des graves détectés            (PRIORITAIRE)
    sous-triage  = FN / (VP + FN) = 1 − sensibilité
    spécificité  = VN / (VN + FP)
    sur-triage   = FP / (VN + FP) = 1 − spécificité
    VPP          = VP / (VP + FP)          part des alertes justifiées
    coût moyen   = (c₊ FN + c₋ FP) / n     c₊ : coût d'un grave manqué, c₋ : d'une fausse alerte (c₋ = 1)

Test de McNemar : deux modèles A et B jugés sur les MÊMES passages
-------------------------------------------------------------------
Seuls comptent les passages où ils ne sont pas d'accord :
    b = A juste et B faux,      c = A faux et B juste.
Si A et B se valent, chaque désaccord est « pile ou face » : b suit une loi binomiale(b + c, ½).
    b + c ≥ 25 :  χ² = (|b − c| − 1)² / (b + c)   (correction de continuité de Yates), 1 degré de liberté ;
                  p = P(χ²₁ ≥ χ²) = 2 (1 − Φ(√χ²))   car un χ²₁ est le carré d'une loi normale centrée réduite ;
    b + c < 25 :  test exact,  p = min(1, 2 Σ_{k ≤ min(b, c)} C(b + c, k) / 2^{b+c}).
"""
from __future__ import annotations

import math

import torch

from svr.classification import auc, brier, log_loss
from svr.metriques import phi
from svr.modeles import TYPE


def confusion(y, alerte) -> dict[str, int]:
    grave = torch.as_tensor(y, dtype=TYPE) > 0
    a = torch.as_tensor(alerte).bool()
    return {"VP": int((grave & a).sum()), "FN": int((grave & ~a).sum()),
            "FP": int((~grave & a).sum()), "VN": int((~grave & ~a).sum())}


def _part(num: int, den: int) -> float:
    return num / den if den else float("nan")


def resume(y, p, seuil: float, rapport_couts: float) -> dict:
    """Toutes les mesures d'un modèle : y = ±1 (ou 0/1), p = probabilités calibrées, seuil s."""
    y = torch.as_tensor(y, dtype=TYPE)
    p = torch.as_tensor(p, dtype=TYPE)
    y01 = (y > 0).to(TYPE)
    m = confusion(y, p >= seuil)
    n = len(y)
    return {"passages": n, "graves": m["VP"] + m["FN"], **m,
            "sensibilite": _part(m["VP"], m["VP"] + m["FN"]), "specificite": _part(m["VN"], m["VN"] + m["FP"]),
            "sous_triage": _part(m["FN"], m["VP"] + m["FN"]), "sur_triage": _part(m["FP"], m["VN"] + m["FP"]),
            "vpp": _part(m["VP"], m["VP"] + m["FP"]),
            "cout_moyen": (rapport_couts * m["FN"] + m["FP"]) / n if n else float("nan"),
            "auc": auc(p, y01), "brier": brier(p, y01), "log_loss": log_loss(p, y01)}


def mcnemar(y, alerte_a, alerte_b) -> dict:
    """Compare les décisions de A et B sur les mêmes passages (voir l'en-tête)."""
    grave = torch.as_tensor(y, dtype=TYPE) > 0
    juste_a = torch.as_tensor(alerte_a).bool() == grave
    juste_b = torch.as_tensor(alerte_b).bool() == grave
    b, c = int((juste_a & ~juste_b).sum()), int((~juste_a & juste_b).sum())
    if b + c == 0:
        return {"b": 0, "c": 0, "statistique": 0.0, "p_valeur": 1.0, "test": "aucun désaccord"}
    if b + c < 25:
        k, n = min(b, c), b + c
        p = min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)
        return {"b": b, "c": c, "statistique": float("nan"), "p_valeur": p, "test": "exact (binomial)"}
    chi2 = (abs(b - c) - 1) ** 2 / (b + c)
    return {"b": b, "c": c, "statistique": chi2, "p_valeur": 2 * (1 - phi(math.sqrt(chi2))), "test": "χ² de McNemar"}


def seuil_optimal(rapport_couts: float) -> float:
    """s* = c₋ / (c₊ + c₋) avec c₋ = 1 et c₊ = rapport : on alerte si c₊ p ≥ c₋ (1 − p)."""
    if rapport_couts <= 0:
        raise ValueError("Le rapport des coûts doit être strictement positif.")
    return 1.0 / (rapport_couts + 1.0)
