"""Variantes de SVM du triage : chaque modèle s'entraîne, la hinge carrée a le bon gradient, le LS-SVM sépare."""
import torch

import triage  # noqa: F401
from svr.modeles import TYPE, Entrainement
from svr.noyaux import NoyauRBF
from triage.modeles import A_PORTEE, MODELES, LSSVMClassifieur, SVMHingeCarree, fabrique


def donnees(n=120, graine=0):
    g = torch.Generator().manual_seed(graine)
    X = torch.randn(n, 6, generator=g, dtype=TYPE)
    y = torch.where(X[:, 0] + 0.5 * X[:, 1] > 0.3, 1.0, -1.0).to(TYPE)
    return X, y


def auc(s, y):
    pos, neg = s[y > 0], s[y <= 0]
    return float((pos[:, None] > neg[None, :]).to(TYPE).mean())


def test_chaque_modele_apprend():
    X, y = donnees()
    blocs = {"constantes": [0, 1, 2], "autres": [3, 4, 5]}
    for m in MODELES:
        fab = fabrique(m, 1.0, 1.0, 1.0, 1.0, blocs, Entrainement(iterations=200))
        if fab is None:
            continue
        modele = fab().entrainer(X[:90], y[:90])
        assert auc(modele.predire(X[90:]), y[90:]) > 0.75, m


def test_gradient_hinge_carree_par_differences_finies():
    X, y = donnees(30)
    m = SVMHingeCarree(NoyauRBF(0.3), 1.0, 2.0, Entrainement(iterations=1, preconditionne=False))
    m.entrainer(X, y)
    m.parametres["alpha"] = 0.05 * torch.randn(30, dtype=TYPE)
    J, grad, _ = m.objectif_et_gradients(m.y if hasattr(m, "y") else y)
    h = 1e-6
    for i in (0, 5, 17):
        m.parametres["alpha"][i] += h
        J2, _, _ = m.objectif_et_gradients(y)
        m.parametres["alpha"][i] -= h
        assert abs((J2 - J) / h - float(grad["alpha"][i])) < 1e-3


def test_lssvm_et_grille():
    X, y = donnees()
    assert auc(LSSVMClassifieur(NoyauRBF(0.2), 1.0, 1.0).entrainer(X[:90], y[:90]).predire(X[90:]), y[90:]) > 0.8
    assert "svm_lineaire" not in A_PORTEE and "lssvm" in A_PORTEE
