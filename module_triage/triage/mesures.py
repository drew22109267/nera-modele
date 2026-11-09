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
    taux d'alerte = (VP + FP) / n          part des passages mis en alerte (1 = tout le monde : plus de tri)

Spécificité à sensibilité fixée (point de la courbe ROC, sans seuil choisi à l'avance)
--------------------------------------------------------------------------------------
    spec@90 = la plus grande spécificité parmi les seuils t qui détectent au moins 90 % des graves.
Comme l'AUC, c'est une lecture de la courbe ROC (pas une règle de décision) : « en gardant 90 % des graves,
quelle part des non-graves le modèle écarte-t-il ? ». Elle compare les modèles là où le triage travaille
(sensibilité élevée), même quand le seuil s* met presque tout le monde en alerte.

Test de McNemar : deux modèles A et B jugés sur les MÊMES passages
-------------------------------------------------------------------
Seuls comptent les passages où ils ne sont pas d'accord :
    b = A juste et B faux,      c = A faux et B juste.
Si A et B se valent, chaque désaccord est « pile ou face » : b suit une loi binomiale(b + c, ½).
    b + c ≥ 25 :  χ² = (|b − c| − 1)² / (b + c)   (correction de continuité de Yates), 1 degré de liberté ;
                  p = P(χ²₁ ≥ χ²) = 2 (1 − Φ(√χ²))   car un χ²₁ est le carré d'une loi normale centrée réduite ;
    b + c < 25 :  test exact,  p = min(1, 2 Σ_{k ≤ min(b, c)} C(b + c, k) / 2^{b+c}).
Limite : McNemar compte un grave manqué et une fausse alerte comme UNE erreur chacun, alors que la décision
suppose qu'un grave manqué coûte c₊/c₋ = 4 fausses alertes. Deux tests complètent donc McNemar :

Test apparié sur le coût (comparer_couts)
-----------------------------------------
Pour chaque passage i, coût de A : c₊·1(grave, pas d'alerte) + c₋·1(non grave, alerte) ; idem pour B ;
d_i = coût_A(i) − coût_B(i), moyenne d̄ = différence des coûts moyens. Sous H₀ (A et B interchangeables sur
chaque passage), le signe de chaque d_i est « pile ou face » : test de permutation par changement de signes
(R tirages), p = (1 + #{|d̄*| ≥ |d̄|}) / (1 + R). Intervalle à 95 % de d̄ par bootstrap des passages.

Spécificité au seuil s₉₀ (mcnemar_specificite)
----------------------------------------------
Chaque modèle alerte au-dessus de SON seuil s₉₀ (fixé sur la calibration pour garder 90 % des graves). Sur les
seuls NON-GRAVES : b = écarté par A et pas par B, c = l'inverse ; McNemar sur (b, c). C'est le test du critère
de sélection du triage (spécificité à sensibilité ~90 %).
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
            "taux_alerte": _part(m["VP"] + m["FP"], n),
            "spec_sens90": specificite_a_sensibilite(y, p, 0.90), "spec_sens95": specificite_a_sensibilite(y, p, 0.95),
            "auc": auc(p, y01), "brier": brier(p, y01), "log_loss": log_loss(p, y01)}


def specificite_a_sensibilite(y, p, cible: float) -> float:
    """Plus grande spécificité parmi les seuils dont la sensibilité atteint `cible` (voir l'en-tête)."""
    grave = torch.as_tensor(y, dtype=TYPE) > 0
    p = torch.as_tensor(p, dtype=TYPE)
    if grave.all() or not grave.any():
        return float("nan")
    for t in torch.unique(p).flip(0):                  # seuils décroissants : la sensibilité ne fait que monter
        if float((p[grave] >= t).to(TYPE).mean()) >= cible:
            return float((p[~grave] < t).to(TYPE).mean())
    return 0.0


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


def comparer_couts(y, alerte_a, alerte_b, rapport_couts: float, tirages: int = 5000, graine: int = 0) -> dict:
    """Différence de coût moyen A − B, test de permutation apparié et IC à 95 % par bootstrap (voir l'en-tête)."""
    grave = torch.as_tensor(y, dtype=TYPE) > 0
    a, b = torch.as_tensor(alerte_a).bool(), torch.as_tensor(alerte_b).bool()
    cout = lambda al: rapport_couts * (grave & ~al).to(TYPE) + (~grave & al).to(TYPE)
    d = cout(a) - cout(b)
    n = len(d)
    if n == 0 or bool((d == 0).all()):
        return {"difference_cout": 0.0, "ic95_bas": 0.0, "ic95_haut": 0.0, "p_valeur": 1.0}
    g = torch.Generator().manual_seed(graine)
    d_barre = float(d.mean())
    signes = torch.randint(0, 2, (tirages, n), generator=g, dtype=torch.int64).to(TYPE) * 2 - 1
    extremes = int(((signes * d).mean(dim=1).abs() >= abs(d_barre) - 1e-12).sum())
    boot = d[torch.randint(0, n, (tirages, n), generator=g)].mean(dim=1)
    bas, haut = torch.quantile(boot, torch.tensor([0.025, 0.975], dtype=TYPE)).tolist()
    return {"difference_cout": d_barre, "ic95_bas": bas, "ic95_haut": haut, "p_valeur": (1 + extremes) / (1 + tirages)}


def mcnemar_specificite(y, alerte_a, alerte_b) -> dict:
    """McNemar sur les non-graves seulement : A écarte-t-il plus de non-graves que B ? (voir l'en-tête)."""
    non_grave = ~(torch.as_tensor(y, dtype=TYPE) > 0)
    a, b = torch.as_tensor(alerte_a).bool()[non_grave], torch.as_tensor(alerte_b).bool()[non_grave]
    # « juste » pour un non-grave = pas d'alerte : on réutilise mcnemar avec une cible toute « non grave ».
    return mcnemar(-torch.ones(int(non_grave.sum()), dtype=TYPE), a, b)


def holm(p_valeurs) -> list:
    """p-valeurs ajustées de Holm (None et NaN gardés, exclus du nombre de tests)."""
    idx = [i for i, p in enumerate(p_valeurs) if p is not None and p == p]
    m, ajustees, courant = len(idx), list(p_valeurs), 0.0
    for rang, i in enumerate(sorted(idx, key=lambda i: p_valeurs[i])):
        courant = max(courant, min(1.0, (m - rang) * p_valeurs[i]))
        ajustees[i] = courant
    return ajustees
