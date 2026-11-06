"""Tests du lasso écrit à la main (svr/lasso.py), sur des données fictives."""
import math

import torch

from svr.lasso import SelectionLasso, chemin, lasso_lineaire, lasso_logistique, seuillage, _reduire

TYPE = torch.float64


def donnees(n=400, d=8, graine=0):
    """Seules les colonnes 0 et 1 comptent : y = 3 x0 − 2 x1 + bruit."""
    g = torch.Generator().manual_seed(graine)
    X = torch.randn(n, d, generator=g, dtype=TYPE)
    y = 3 * X[:, 0] - 2 * X[:, 1] + 0.5 * torch.randn(n, generator=g, dtype=TYPE)
    return X, y


def test_seuillage_doux():
    u = torch.tensor([-3.0, -0.5, 0.0, 0.5, 3.0], dtype=TYPE)
    assert torch.allclose(seuillage(u, 1.0), torch.tensor([-2.0, 0.0, 0.0, 0.0, 2.0], dtype=TYPE))


def test_lambda_nul_donne_les_moindres_carres():
    X, y = donnees()
    Z, _, _ = _reduire(X)
    b, beta = lasso_lineaire(Z, y, 0.0, tolerance=1e-10)
    A = torch.cat([torch.ones(len(y), 1, dtype=TYPE), Z], dim=1)
    mc = torch.linalg.lstsq(A, y.unsqueeze(1)).solution.flatten()
    assert abs(b - float(mc[0])) < 1e-6 and torch.allclose(beta, mc[1:], atol=1e-6)


def test_lambda_max_annule_tout():
    X, y = donnees()
    Z, _, _ = _reduire(X)
    lam_max = float((Z.T @ (y - y.mean())).abs().max()) / len(y)
    _, beta = lasso_lineaire(Z, y, lam_max * 1.0001)
    assert torch.all(beta == 0)
    _, beta = lasso_lineaire(Z, y, lam_max * 0.9)
    assert (beta != 0).sum() == 1


def test_chemin_decroissant():
    c = chemin(2.0)
    assert len(c) == 20 and math.isclose(c[0], 2.0) and math.isclose(c[-1], 0.02)
    assert all(a > b for a, b in zip(c, c[1:]))


def test_selection_garde_les_bonnes_colonnes():
    X, y = donnees()
    s = SelectionLasso("carree", "lasso_1se").ajuster(X, y)
    assert s.colonnes[:2] == [0, 1]
    assert set(s.colonnes) <= set(range(8)) and len(s.colonnes) <= 4
    assert s.transformer(X).shape == (len(y), len(s.colonnes))


def test_logistique_selectionne_et_classe():
    g = torch.Generator().manual_seed(1)
    X = torch.randn(600, 6, generator=g, dtype=TYPE)
    u = 2 * X[:, 2] - 1.5 * X[:, 4] - 1.0
    y = torch.where(torch.rand(600, generator=g, dtype=TYPE) < torch.sigmoid(u), 1.0, -1.0).to(TYPE)
    poids = torch.where(y > 0, float((y < 0).sum() / (y > 0).sum()), 1.0).to(TYPE)
    s = SelectionLasso("logistique", "lasso_1se").ajuster(X, y, poids)
    assert 2 in s.colonnes and 4 in s.colonnes and len(s.colonnes) <= 4
    Z, _, _ = _reduire(X)
    b, beta = lasso_logistique(Z, y, torch.ones(600, dtype=TYPE), 0.0, iterations=5000)
    juste = ((b + Z @ beta > 0) == (y > 0)).double().mean()
    assert juste > 0.7 and beta[2] > 0 and beta[4] < 0
