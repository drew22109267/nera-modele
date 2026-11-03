"""Variantes du SVR (svr/variantes.py) : noyaux, LS-SVR et ses erreurs LOO exactes, catalogue complet."""
import torch

from svr.modeles import TYPE, Entrainement
from svr.niveaux import Hyperparametres
from svr.concurrents import HyperConcurrents
from svr.noyaux import NoyauRBF
from svr.variantes import CATALOGUE, LSSVR, NoyauLaplacien, NoyauPolynomial, fabrique_catalogue


def test_noyaux_semi_definis_positifs():
    X = torch.randn(40, 5, dtype=TYPE)
    for noyau in (NoyauLaplacien(0.3), NoyauPolynomial(0.2)):
        K = noyau(X, X)
        assert torch.allclose(K, K.T)
        assert float(torch.linalg.eigvalsh(K).min()) > -1e-8


def test_lssvr_erreurs_loo_exactes():
    """r_i = α_i / (H⁻¹)_ii doit égaler l'erreur d'un modèle réappris sans le point i."""
    g = torch.Generator().manual_seed(0)
    X = torch.randn(25, 3, generator=g, dtype=TYPE)
    y = X[:, 0] * 2 + 0.3 * torch.randn(25, generator=g, dtype=TYPE)
    m = LSSVR(NoyauRBF(0.5), C=3.0, taus=(0.5,)).entrainer(X, y)
    for i in (0, 7, 19):
        garde = torch.arange(25) != i
        m_i = LSSVR(NoyauRBF(0.5), C=3.0, taus=(0.5,)).entrainer(X[garde], y[garde])
        f_i = NoyauRBF(0.5)(X[i:i + 1], m_i.X) @ m_i.alpha + m_i.b
        assert abs(float(y[i] - f_i) - float(m.residus_loo[i])) < 1e-8


def test_tout_le_catalogue_s_entraine_et_prevoit():
    g = torch.Generator().manual_seed(1)
    X = torch.randn(60, 6, dtype=TYPE, generator=g)
    y = 10 + X[:, 0] + 0.2 * torch.randn(60, generator=g, dtype=TYPE)
    blocs = {"occupation": [0, 1, 2], "flux_saison": [3, 4, 5]}
    e = Entrainement(iterations=60)
    hp = {n: Hyperparametres(entrainement=e) for n in (1, 2, 3, 4)}
    hpc = HyperConcurrents(arbres=5, etapes=5, epoques=20, graines=1)
    for cle in CATALOGUE:
        if cle == "lstm":
            continue                                    # le LSTM attend des retards en colonnes (testé ailleurs)
        modele = fabrique_catalogue(cle, hp, blocs, hpc)().entrainer(X[:50], y[:50])
        p = modele.predire(X[50:])
        valeurs = p[0.5] if isinstance(p, dict) else p
        assert valeurs.shape == (10,) and not torch.isnan(valeurs).any(), cle
