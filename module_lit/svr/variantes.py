r"""
Variantes du SVR (SVM de régression) comparées au modèle retenu, et catalogue de TOUS les modèles du module lit
utilisé par les bancs croisés (P1 × modèles), le banc D13 et la sélection finale (selection.py).

Noyaux supplémentaires
----------------------
  Laplacien     K(x, z) = exp(−γ ‖x − z‖₁)          (distance « en blocs » : moins sensible à une variable
                                                       très écartée que le RBF, qui l'élève au carré)
  Polynomial    K(x, z) = (γ xᵀz + 1)^d, d = 2       (interactions d'ordre 2 entre variables : occupation × flux…)
Les deux sont des noyaux de Mercer (matrice K semi-définie positive) : le même SVR quantile s'applique.

SVR à moindres carrés (LS-SVR, Suykens et Vandewalle, 1999)
-----------------------------------------------------------
On remplace la perte ε-insensible par le carré des erreurs et les inégalités par des égalités :
    min ½‖w‖² + (C/2) Σ e_i²   sous   y_i = wᵀφ(x_i) + b + e_i.
Les conditions d'optimalité (Lagrangien, α_i = C e_i) donnent un SYSTÈME LINÉAIRE, sans itérations :
    [ 0      1ᵀ       ] [ b ]   [ 0 ]
    [ 1   K + I/C     ] [ α ] = [ y ],          f(x) = Σ α_i K(x_i, x) + b.
Erreurs « laisser-un-de-côté » exactes, sans réentraîner (Cawley et Talbot, 2004) : avec H la matrice du
système, r_i^{LOO} = α_i / (H⁻¹)_{ii}. Les quantiles τ de ces erreurs donnent l'intervalle et le quantile
décisionnel : q_τ(x) = f(x) + quantile_τ(r^{LOO}) (le LS-SVR n'a pas de perte pinball).
"""
from __future__ import annotations

from dataclasses import dataclass

import torch

from .concurrents import CONCURRENTS, HyperConcurrents, fabrique_concurrent
from .modeles import TYPE, IntervalleQuantile, Perte, SVRNoyau
from .niveaux import Hyperparametres, fabrique
from .noyaux import NoyauRBF


@dataclass
class NoyauLaplacien:
    gamma: float

    def __call__(self, X: torch.Tensor, Z: torch.Tensor) -> torch.Tensor:
        return torch.exp(-self.gamma * torch.cdist(X, Z, p=1))


@dataclass
class NoyauPolynomial:
    gamma: float
    degre: int = 2

    def __call__(self, X: torch.Tensor, Z: torch.Tensor) -> torch.Tensor:
        return (self.gamma * X @ Z.T + 1.0) ** self.degre


class LSSVR:
    """SVR à moindres carrés : un système linéaire ; quantiles par les erreurs LOO exactes."""

    def __init__(self, noyau, C: float = 1.0, taus: tuple = (0.05, 0.5, 0.95)):
        self.noyau, self.C, self.taus = noyau, C, taus

    def entrainer(self, X, y) -> "LSSVR":
        X, y = torch.as_tensor(X, dtype=TYPE), torch.as_tensor(y, dtype=TYPE)
        n = len(y)
        H = torch.zeros(n + 1, n + 1, dtype=TYPE)
        H[0, 1:] = 1.0
        H[1:, 0] = 1.0
        H[1:, 1:] = self.noyau(X, X) + torch.eye(n, dtype=TYPE) / self.C
        sol = torch.linalg.solve(H, torch.cat([torch.zeros(1, dtype=TYPE), y]))
        self.b, self.alpha, self.X = sol[0], sol[1:], X
        Hinv_diag = torch.diagonal(torch.linalg.inv(H))[1:]
        self.residus_loo = self.alpha / Hinv_diag                    # r_i = y_i − f_{−i}(x_i)
        return self

    def predire(self, X) -> dict[float, torch.Tensor]:
        f = self.noyau(torch.as_tensor(X, dtype=TYPE), self.X) @ self.alpha + self.b
        return {t: f + torch.quantile(self.residus_loo, t) for t in self.taus}


def _quantile(noyau, hp: Hyperparametres):
    e = hp.entrainement
    modele = lambda tau: SVRNoyau(noyau, C=hp.C, perte=Perte("pinball_epsilon", epsilon=hp.epsilon_quantile, tau=tau), entrainement=e)
    return lambda: IntervalleQuantile(modele, tuple(sorted({*hp.taus_intervalle, hp.tau})))


# Catalogue : clé → (nom affiché, famille, fabrique(hp_par_niveau, blocs, hpc)). « svm » = famille SVM (sélection).
CATALOGUE = {
    "svr_lineaire": ("SVR linéaire (niveau 1)", "svm", lambda hp, b, c: fabrique(1, hp[1], b)),
    "svr_rbf": ("SVR RBF (niveau 2)", "svm", lambda hp, b, c: fabrique(2, hp[2], b)),
    "svr_q_rbf": ("SVR quantile RBF (niveau 3)", "svm", lambda hp, b, c: fabrique(3, hp[3], b)),
    "svr_q_composite": ("SVR quantile composite (niveau 4, retenu)", "svm", lambda hp, b, c: fabrique(4, hp[4], b)),
    "svr_q_laplacien": ("SVR quantile, noyau laplacien", "svm", lambda hp, b, c: _quantile(NoyauLaplacien(hp[3].gamma), hp[3])),
    "svr_q_polynomial": ("SVR quantile, noyau polynomial (degré 2)", "svm",
                         lambda hp, b, c: _quantile(NoyauPolynomial(1.0 / max(1, sum(len(v) for v in b.values()))), hp[3])),
    "lssvr_rbf": ("LS-SVR (moindres carrés), noyau RBF, quantiles LOO", "svm",
                  lambda hp, b, c: lambda: LSSVR(NoyauRBF(hp[2].gamma), hp[2].C, tuple(sorted({*hp[3].taus_intervalle, hp[3].tau})))),
    **{k: (v, "concurrent", (lambda k: lambda hp, b, c: fabrique_concurrent(k, c, retards=7))(k)) for k, v in CONCURRENTS.items()},
}
RETENU = "svr_q_composite"


def fabrique_catalogue(cle: str, hp: dict[int, Hyperparametres], blocs: dict, hpc: HyperConcurrents | None = None):
    if cle not in CATALOGUE:
        raise ValueError(f"Modèle inconnu : {cle}. Choix : {', '.join(CATALOGUE)}.")
    return CATALOGUE[cle][2](hp, blocs, hpc or HyperConcurrents(tau=hp[4].tau))
