"""Triage à trois niveaux (triage/ordinal.py) : cas calculés à la main."""
import math

import torch

import triage  # noqa: F401
from triage.ordinal import combiner, decider, decision_binaire, kappa_pondere, matrice_couts, resume3


def test_matrice_des_couts():
    c = matrice_couts(4.0)
    # vrai grave (2) mis en vert (0) : 2 niveaux de sous-triage × 4 ; vrai vert mis en rouge : 2 niveaux de sur-triage
    assert c[2, 0] == 8 and c[2, 1] == 4 and c[1, 0] == 4
    assert c[0, 2] == 2 and c[0, 1] == 1 and c[1, 2] == 1
    assert c[0, 0] == c[1, 1] == c[2, 2] == 0


def test_combiner_et_ordre_impose():
    haut = {"y": torch.tensor([1.0, -1.0, -1.0]), "p": torch.tensor([0.7, 0.2, 0.3], dtype=torch.float64),
            "indices": torch.tensor([10, 11, 12]), "meo": torch.tensor([0.0, 1.0, 0.0])}
    bas = {"y": torch.tensor([1.0, 1.0, -1.0]), "p": torch.tensor([0.9, 0.6, 0.1], dtype=torch.float64),
           "indices": torch.tensor([10, 11, 12]), "meo": torch.tensor([0.0, 1.0, 0.0])}
    r = combiner(haut, bas)
    assert r["y"].tolist() == [2.0, 1.0, 0.0]                         # grave, moyen (MEO), non grave
    P = r["p"]
    assert torch.allclose(P.sum(1), torch.ones(3, dtype=torch.float64))
    assert math.isclose(float(P[0, 2]), 0.7) and math.isclose(float(P[0, 1]), 0.2)
    # 3e passage : p_bas = 0,1 < p_haut = 0,3 → corrigé à 0,3 ; P(moyen) = 0, jamais négative
    assert math.isclose(float(P[2, 1]), 0.0) and r["ordre_corrige"] == 1


def test_decision_par_cout_attendu():
    # P = (non grave, moyen, grave). Coût attendu de chaque priorité j : Σ_i P_i c(i, j), r = 4.
    P = torch.tensor([[0.9, 0.08, 0.02],      # vert : 0,08×4 + 0,02×8 = 0,48 ; jaune : 0,9 + 0,08 = 0,98 → vert
                      [0.5, 0.3, 0.2],        # vert 2,8 ; jaune 0,5 + 0,8 = 1,3 ; rouge 1 + 0,3 = 1,3 → jaune (premier)
                      [0.2, 0.2, 0.6]], dtype=torch.float64)   # rouge : 0,4 + 0,2 = 0,6 → rouge
    assert decider(P, 4.0).tolist() == [0, 1, 2]


def test_deux_niveaux_retrouve_le_seuil_binaire():
    P = torch.tensor([[0.85, 0.0, 0.15], [0.75, 0.0, 0.25]], dtype=torch.float64)
    # Sans niveau moyen, la règle de coût revient au seuil s* = 1/(1 + r) = 0,2 du triage binaire.
    assert decider(P, 4.0)[0] == 0 and decider(P, 4.0)[1] == 2
    assert decision_binaire(P, 0.2, "grave").tolist() == [0, 2]


def test_kappa_pondere():
    parfait = torch.diag(torch.tensor([5.0, 3.0, 2.0], dtype=torch.float64))
    assert math.isclose(kappa_pondere(parfait), 1.0)
    # Accord au hasard : chaque ligne répartie comme les colonnes → κ = 0.
    hasard = torch.outer(torch.tensor([2.0, 3.0, 5.0]), torch.tensor([2.0, 3.0, 5.0])).to(torch.float64)
    assert abs(kappa_pondere(hasard)) < 1e-12


def test_resume3_sous_et_sur_triage():
    y = torch.tensor([2, 2, 1, 0])
    pred = torch.tensor([2, 0, 2, 0])          # un grave en vert (sous-triage de 2), un moyen en rouge (sur-triage)
    P = torch.tensor([[0, 0, 1], [1, 0, 0], [0, 0, 1], [1, 0, 0]], dtype=torch.float64)
    m = resume3(y, P, 4.0, pred)
    assert m["graves"] == 2 and m["moyens"] == 1 and m["non_graves"] == 1
    assert math.isclose(m["sous_triage"], 0.25) and math.isclose(m["sur_triage"], 0.25)
    assert math.isclose(m["graves_en_rouge"], 0.5) and math.isclose(m["graves_sous_tries"], 0.5)
    assert math.isclose(m["cout_moyen"], (8 + 1) / 4)


def test_bootstrap_cout_par_jours():
    import pandas as pd
    from triage.ordinal import bootstrap_cout
    # 40 jours, 5 passages par jour, tous graves (niveau 2). A les met en rouge (coût 0), B en jaune (coût r = 4).
    jours = pd.date_range("2025-01-01", periods=40).repeat(5)
    y = torch.full((200,), 2)
    r = bootstrap_cout(y, torch.full((200,), 2), torch.full((200,), 1), 4.0, jours, tirages=500)
    assert r["diff_cout"] == -4.0 and r["ic_haut"] == -4.0 and r["p_valeur"] == 0.0
    # mêmes décisions : aucune différence, p = 1
    r = bootstrap_cout(y, torch.full((200,), 1), torch.full((200,), 1), 4.0, jours, tirages=200)
    assert r["diff_cout"] == 0.0 and r["p_valeur"] == 1.0
