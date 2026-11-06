"""Concurrents du SVR (svr/concurrents.py) : gradients par différences finies, cas exacts, interface."""
import math

import torch

from svr import concurrents as C

T = torch.float64


def _donnees(n=120, p=4, graine=0):
    g = torch.Generator().manual_seed(graine)                  # données de test, graine fixe
    X = torch.randn(n, p, generator=g, dtype=T)
    y = 2 * X[:, 0] - X[:, 1] + 0.3 * torch.randn(n, generator=g, dtype=T)
    return X, y


def _verifier_gradients(modele, X, y, eps=1e-6, tol=1e-5):
    gen = torch.Generator().manual_seed(3)
    P = modele._initialiser(X.shape[1], gen)
    for nom in P:                                               # petite perturbation : évite les points anguleux
        P[nom] = P[nom] + 0.01 * torch.randn(P[nom].shape, generator=gen, dtype=T)
    _, grads = modele.objectif_et_gradients(X, y, P)
    for nom, v in P.items():
        plat = v.reshape(-1)
        for k in range(0, plat.numel(), max(1, plat.numel() // 7)):
            orig = float(plat[k])
            plat[k] = orig + eps; jp, _ = modele.objectif_et_gradients(X, y, P)
            plat[k] = orig - eps; jm, _ = modele.objectif_et_gradients(X, y, P)
            plat[k] = orig
            num = (jp - jm) / (2 * eps)
            assert abs(num - float(grads[nom].reshape(-1)[k])) < tol * (1 + abs(num)), (nom, k, num)


def test_gradients_mlp_par_differences_finies():
    X, y = _donnees(40, 3)
    _verifier_gradients(C.PerceptronQuantile(couches=(5, 4), lambda_=1e-2), X, y)


def test_gradients_lstm_par_differences_finies():
    X, y = _donnees(30, 5)                                      # 3 retards + 2 variables exogènes
    _verifier_gradients(C.LSTMQuantile(retards=3, cache=4, lambda_=1e-2), X, y)


def test_arbre_retrouve_une_marche():
    X = torch.linspace(0, 1, 100, dtype=T)[:, None]
    y = torch.where(X[:, 0] <= 0.5, torch.tensor(1.0, dtype=T), torch.tensor(5.0, dtype=T))
    a = C.Arbre(profondeur_max=3, min_feuille=5).construire(X, y)
    p = a.predire(torch.tensor([[0.2], [0.8]], dtype=T))
    assert torch.allclose(p, torch.tensor([1.0, 5.0], dtype=T))


def test_foret_quantiles_ordonnes_et_plausibles():
    X, y = _donnees(150, 3)
    f = C.ForetAleatoireQuantile(taus=(0.05, 0.5, 0.95), arbres=40).entrainer(X, y)
    q = f.predire(X[:20])
    assert bool((q[0.05] <= q[0.5]).all()) and bool((q[0.5] <= q[0.95]).all())
    couverture = float(((y[:20] >= q[0.05]) & (y[:20] <= q[0.95])).to(T).mean())
    assert couverture >= 0.8                                      # sur l'entraînement, l'intervalle couvre


def test_boosting_fait_baisser_la_perte():
    X, y = _donnees(150, 3)
    m0 = C.GradientBoostingQuantile(tau=0.5, etapes=1, taux=0.1).entrainer(X, y)
    m1 = C.GradientBoostingQuantile(tau=0.5, etapes=150, taux=0.1).entrainer(X, y)
    t = torch.tensor([0.5], dtype=T)
    p0, _ = C.pinball_et_gradient(y, m0.predire(X)[:, None], t)
    p1, _ = C.pinball_et_gradient(y, m1.predire(X)[:, None], t)
    assert p1 < 0.5 * p0


def test_interface_commune_et_tri():
    X, y = _donnees(80, 9)
    hp = C.HyperConcurrents(arbres=10, etapes=20, epoques=60, patience=20, graines=1)
    for nom in C.CONCURRENTS:
        m = C.fabrique_concurrent(nom, hp, retards=7)().entrainer(X, y)
        q = m.predire(X[:10])
        assert set(q) == set(hp.quantiles()), nom
        cles = sorted(q)
        for a, b in zip(cles, cles[1:]):
            assert bool((q[a] <= q[b]).all()), nom              # pas de croisement des quantiles
        assert all(bool(torch.isfinite(v).all()) for v in q.values()), nom


def test_arbre_valeurs_presque_egales():
    """sin 0 = 0 et sin π ≈ 1e−16 : aucune feuille vide, aucune coupure entre ces deux valeurs."""
    import math as m
    from svr.concurrents import Arbre, GradientBoostingQuantile
    x = torch.tensor([0.0, m.sin(m.pi)] * 20 + [1.0] * 10, dtype=torch.float64)[:, None]
    y = torch.tensor([0.0, 5.0] * 20 + [9.0] * 10, dtype=torch.float64)
    a = Arbre(3, 5).construire(x, y)
    assert int((a.var >= 0).sum()) == 1                      # une seule coupure : entre ≈0 et 1
    GradientBoostingQuantile(tau=0.8, etapes=5, min_feuille=5).entrainer(x, y)


def test_xgboost_second_ordre():
    """Perte carrée : suit une fonction en escalier ; pinball : le quantile 0,8 est au-dessus du quantile 0,2."""
    from svr.concurrents import XGBoost
    g = torch.Generator().manual_seed(0)
    X = torch.rand(400, 3, generator=g, dtype=torch.float64)
    y = torch.where(X[:, 0] > 0.5, 5.0, 1.0).to(torch.float64) + 0.3 * torch.randn(400, generator=g, dtype=torch.float64)
    m = XGBoost("carree", etapes=60, taux=0.3, profondeur=2).entrainer(X, y)
    assert float((m.predire(X) - y).abs().mean()) < 0.5
    haut = XGBoost("pinball", 0.8, etapes=80, taux=0.3).entrainer(X, y).predire(X)
    bas = XGBoost("pinball", 0.2, etapes=80, taux=0.3).entrainer(X, y).predire(X)
    assert float((haut > bas).double().mean()) > 0.9
