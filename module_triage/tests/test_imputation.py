"""Tests des neuf traitements des valeurs manquantes (banc T8), sur des données fictives."""
import math

import pytest
import torch

import triage  # noqa: F401
from triage.imputation import IMPUTATIONS, Imputeur
from triage.variables import Preparateur

TYPE = torch.float64


def donnees(n=300, graine=0, part=0.3):
    """Âge, puis trois colonnes liées : x2 = 2·x1 + bruit, x3 = −x1 + bruit ; des cases vides au hasard."""
    g = torch.Generator().manual_seed(graine)
    age = torch.rand(n, generator=g, dtype=TYPE) * 80
    x1 = torch.randn(n, generator=g, dtype=TYPE)
    X = torch.stack([age, x1, 2 * x1 + 0.1 * torch.randn(n, generator=g, dtype=TYPE),
                     -x1 + 0.1 * torch.randn(n, generator=g, dtype=TYPE)], dim=1)
    vrai = X.clone()
    trous = torch.rand(n, 4, generator=g, dtype=TYPE) < part
    trous[:, 0] = False
    X[trous] = float("nan")
    return X, vrai, trous


@pytest.mark.parametrize("methode", IMPUTATIONS)
def test_plus_aucune_case_vide(methode):
    X, _, _ = donnees()
    imp = Imputeur(methode, continues=[0, 1, 2, 3]).ajuster(X[:200])
    Z = imp.transformer(X[200:])
    assert not torch.isnan(Z).any()
    observe = ~torch.isnan(X[200:])
    assert torch.equal(Z[observe], X[200:][observe])          # les valeurs observées ne bougent jamais


@pytest.mark.parametrize("methode", ["knn", "regression", "em", "acp_iterative"])
def test_les_methodes_a_modele_battent_la_mediane(methode):
    """Les colonnes sont liées : une méthode qui s'en sert doit retrouver les cases vides mieux que la médiane."""
    X, vrai, trous = donnees()
    erreur = {}
    for m in ("mediane", methode):
        Z = Imputeur(m, continues=[0, 1, 2, 3]).ajuster(X[:200]).transformer(X[200:])
        t = trous[200:]
        erreur[m] = float(((Z[t] - vrai[200:][t]) ** 2).mean())
    assert erreur[methode] < 0.5 * erreur["mediane"]


def test_em_retrouve_la_moyenne_et_la_covariance():
    X, vrai, _ = donnees(n=2000, part=0.2)
    imp = Imputeur("em", continues=[0, 1, 2]).ajuster(X[:, 1:])
    Zv = (vrai[:, 1:] - imp.centre) / imp.echelle
    assert torch.allclose(imp.mu, Zv.mean(0), atol=0.1)
    assert torch.allclose(imp.sigma, torch.cov(Zv.T, correction=0), atol=0.15)


def test_mediane_age_et_suppression_colonnes():
    X = torch.tensor([[0.5, 100.0], [0.5, float("nan")], [30.0, 70.0], [30.0, float("nan")]], dtype=TYPE)
    Z = Imputeur("mediane_age", continues=[0, 1]).ajuster(X).transformer(X)
    assert Z[1, 1] == 100.0 and Z[3, 1] == 70.0                # la médiane de SA tranche d'âge
    X2 = torch.tensor([[1.0, float("nan")], [2.0, float("nan")], [3.0, 5.0]], dtype=TYPE)
    prep = Preparateur([0, 1], "suppression_colonnes").ajuster(X2)
    assert prep.imputeur.retirees == [1]
    assert torch.all(prep.transformer(X2)[:, 1] == 0)           # colonne retirée = constante
    assert not math.isnan(float(prep.transformer(X2).sum()))


def test_k_du_knn_choisi_par_validation_croisee():
    from triage.imputation import K_GRILLE
    X, _, _ = donnees()
    imp = Imputeur("knn", continues=[0, 1, 2, 3]).ajuster(X[:200])
    assert imp.k in K_GRILLE and imp.erreurs_k[imp.k] == min(imp.erreurs_k.values())
    assert Imputeur("knn", continues=[0, 1, 2, 3], k=7).ajuster(X[:200]).k == 7     # k imposé : pas de choix


@pytest.mark.parametrize("echelle", ["zscore", "robuste", "minmax", "aucune"])
def test_mises_a_l_echelle_du_preparateur(echelle):
    X, _, _ = donnees()
    prep = Preparateur([0, 1, 2, 3], "mediane", echelle).ajuster(X[:200])
    Z = prep.transformer(X[:200])
    assert not torch.isnan(Z).any()
    if echelle == "zscore":
        assert torch.allclose(Z.mean(0), torch.zeros(4, dtype=TYPE), atol=1e-9)
    elif echelle == "minmax":
        assert torch.allclose(Z.min(0).values, torch.zeros(4, dtype=TYPE)) and torch.allclose(Z.max(0).values, torch.ones(4, dtype=TYPE))
    elif echelle == "robuste":
        assert torch.allclose(Z.median(0).values, torch.zeros(4, dtype=TYPE), atol=1e-2)
    else:
        assert torch.equal(Z, prep._imputer(X[:200]))
