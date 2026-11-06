r"""
Sélection des variables par le lasso (Tibshirani, 1996), écrite à la main (bancs D14 des lits, T15 du triage).

Idée
----
Un modèle linéaire dont la pénalité est la somme des VALEURS ABSOLUES des coefficients :

    lits    (régression)      J(b, β) = 1/(2n) Σ_i (y_i − b − z_iᵀβ)²            + λ Σ_j |β_j|
    triage  (classement)      J(b, β) = 1/n Σ_i w_i ln(1 + e^{−s_i (b + z_iᵀβ)}) + λ Σ_j |β_j|     (s_i = ±1)

La valeur absolue a un coin en 0 : au-dessous d'un certain λ, la meilleure valeur d'un coefficient est
EXACTEMENT 0 (et non « petite » comme avec la ridge, pénalité Σ β_j²). Les variables de coefficient nul sont
retirées : c'est une sélection. Plus λ est grand, moins il reste de variables.

Avant le lasso, toutes les colonnes (y compris les indicatrices 0/1) sont centrées-réduites sur l'apprentissage :
la pénalité doit traiter chaque variable de la même façon, quelle que soit son unité.

Calcul
------
Opérateur de seuillage doux :  S(u, λ) = signe(u) · max(|u| − λ, 0).
  régression : descente par coordonnées. Les colonnes ayant moyenne 0 et variance 1, la meilleure valeur
               de β_j, les autres fixées, est  β_j = S( (1/n) Σ_i z_ij r_i + β_j , λ ),  r_i = y_i − b − z_iᵀβ ;
               b = moyenne de y. On parcourt les colonnes jusqu'à ce qu'aucune ne bouge plus de 1e-6.
  logistique : gradient proximal accéléré (FISTA, Beck et Teboulle, 2009). Pas 1/L, L = ‖Z‖₂² max w /(4n)
               (la dérivée seconde de ln(1 + e^{−u}) ne dépasse pas 1/4) :
                   β ← S(β − ∇/L, λ/L),   b ← b − ∂J/∂b / L      (b n'est pas pénalisé).
               Poids w_i : les coûts de classe du triage (équilibrés), pour que la classe rare compte autant.

Choix de λ
----------
Chemin de 20 valeurs de λ_max à λ_max/100 (échelle logarithmique) ; λ_max est la plus petite valeur pour
laquelle tous les coefficients sont nuls : λ_max = max_j |∂J/∂β_j| en β = 0. Chaque λ est mesuré par
validation croisée en 5 blocs CONSÉCUTIFS dans le temps (erreur quadratique ou déviance logistique pondérée
sur le bloc caché), chaque λ partant de la solution du λ précédent (démarrage à chaud). Deux règles :
  lasso       λ_min = l'erreur moyenne la plus petite ;
  lasso_1se   λ_1se = le plus grand λ dont l'erreur ne dépasse pas min + un écart-type de la moyenne
              (Hastie, Tibshirani et Friedman, 2009, §7.10) : moins de variables pour une erreur équivalente.
Si aucune variable ne survit, on garde la première qui entre dans le chemin (celle de plus grand |∂J/∂β_j|).
"""
from __future__ import annotations

import math

import torch

TYPE = torch.float64
REGLES = ("lasso", "lasso_1se")
NOMBRE_LAMBDA, RAPPORT_LAMBDA, PLIS = 20, 0.01, 5


def seuillage(u: torch.Tensor, seuil: float) -> torch.Tensor:
    """S(u, λ) = signe(u) · max(|u| − λ, 0)."""
    return torch.sign(u) * torch.clamp(u.abs() - seuil, min=0.0)


def _reduire(Z: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Centre et réduit chaque colonne ; une colonne constante garde l'écart 1 (elle ne sera jamais choisie)."""
    m = Z.mean(0)
    s = Z.std(0, unbiased=False)
    s = torch.where(s < 1e-12, torch.ones_like(s), s)
    return (Z - m) / s, m, s


# ─────────────────────────────────────────────────────────────────────────────
# Régression (lits) : descente par coordonnées
# ─────────────────────────────────────────────────────────────────────────────
def lasso_lineaire(Z: torch.Tensor, y: torch.Tensor, lam: float, beta: torch.Tensor | None = None,
                   tolerance: float = 1e-6, passages_max: int = 1000) -> tuple[float, torch.Tensor]:
    """(b, β) minimisant 1/(2n)‖y − b − Zβ‖² + λ‖β‖₁ ; Z de colonnes centrées-réduites."""
    n, d = Z.shape
    b = float(y.mean())
    beta = torch.zeros(d, dtype=TYPE) if beta is None else beta.clone()
    norme = (Z * Z).sum(0) / n                       # 1 pour une colonne réduite, 0 pour une colonne constante
    r = y - b - Z @ beta
    for _ in range(passages_max):
        plus_grand = 0.0
        for j in range(d):
            if norme[j] < 1e-12:
                continue
            ancien = float(beta[j])
            rho = float(Z[:, j] @ r) / n + float(norme[j]) * ancien
            nouveau = math.copysign(max(abs(rho) - lam, 0.0), rho) / float(norme[j])
            if nouveau != ancien:
                r -= Z[:, j] * (nouveau - ancien)
                beta[j] = nouveau
                plus_grand = max(plus_grand, abs(nouveau - ancien))
        if plus_grand < tolerance:
            break
    return b, beta


def _lambda_max_lineaire(Z: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    return (Z.T @ (y - y.mean())).abs() / Z.shape[0]


# ─────────────────────────────────────────────────────────────────────────────
# Logistique (triage) : gradient proximal accéléré
# ─────────────────────────────────────────────────────────────────────────────
def _gradient_logistique(Z, s, w, b, beta):
    u = s * (b + Z @ beta)
    g = -s * w * torch.sigmoid(-u) / Z.shape[0]        # dérivée de w ln(1 + e^{−u}) par rapport à (b + zᵀβ), /n
    return Z.T @ g, float(g.sum())


def lasso_logistique(Z: torch.Tensor, s: torch.Tensor, w: torch.Tensor, lam: float,
                     depart: tuple[float, torch.Tensor] | None = None, tolerance: float = 1e-6,
                     iterations: int = 2000) -> tuple[float, torch.Tensor]:
    """(b, β) minimisant 1/n Σ w_i ln(1 + e^{−s_i(b + z_iᵀβ)}) + λ‖β‖₁, s_i = ±1 (FISTA)."""
    n, d = Z.shape
    L = float(torch.linalg.matrix_norm(Z, 2)) ** 2 * float(w.max()) / (4 * n) + 1e-12
    L = max(L, float(w.max()) / 4)                     # l'ordonnée b a aussi sa courbure (colonne de 1)
    if depart is None:
        p = float((w * (s > 0)).sum() / w.sum())
        b, beta = math.log(max(p, 1e-12) / max(1 - p, 1e-12)), torch.zeros(d, dtype=TYPE)
    else:
        b, beta = depart[0], depart[1].clone()
    vb, vbeta, t = b, beta.clone(), 1.0
    for _ in range(iterations):
        gbeta, gb = _gradient_logistique(Z, s, w, vb, vbeta)
        nouveau = seuillage(vbeta - gbeta / L, lam / L)
        nb = vb - gb / L
        t_suiv = (1 + math.sqrt(1 + 4 * t * t)) / 2
        ecart = max(float((nouveau - beta).abs().max()) if d else 0.0, abs(nb - b))
        vbeta = nouveau + (t - 1) / t_suiv * (nouveau - beta)
        vb = nb + (t - 1) / t_suiv * (nb - b)
        beta, b, t = nouveau, nb, t_suiv
        if ecart < tolerance:
            break
    return b, beta


def deviance(Z, s, w, b, beta) -> float:
    """Perte logistique pondérée moyenne, 1/Σw Σ w_i ln(1 + e^{−s_i(b + z_iᵀβ)})."""
    u = s * (b + Z @ beta)
    return float((w * torch.nn.functional.softplus(-u)).sum() / w.sum())


def _lambda_max_logistique(Z, s, w):
    p = float((w * (s > 0)).sum() / w.sum())
    gbeta, _ = _gradient_logistique(Z, s, w, math.log(max(p, 1e-12) / max(1 - p, 1e-12)), torch.zeros(Z.shape[1], dtype=TYPE))
    return gbeta.abs()


# ─────────────────────────────────────────────────────────────────────────────
# Chemin de λ, validation croisée, sélection
# ─────────────────────────────────────────────────────────────────────────────
def chemin(lam_max: float, nombre: int = NOMBRE_LAMBDA, rapport: float = RAPPORT_LAMBDA) -> list[float]:
    """λ_max, …, rapport · λ_max, régulièrement espacés en logarithme."""
    lam_max = max(lam_max, 1e-12)
    return [lam_max * rapport ** (k / (nombre - 1)) for k in range(nombre)]


def blocs_consecutifs(n: int, plis: int = PLIS) -> list[torch.Tensor]:
    """Indices 0 … n−1 coupés en `plis` blocs consécutifs (les lignes sont dans l'ordre du temps)."""
    bornes = [round(k * n / plis) for k in range(plis + 1)]
    return [torch.arange(bornes[k], bornes[k + 1]) for k in range(plis) if bornes[k + 1] > bornes[k]]


class SelectionLasso:
    """
    Apprise sur l'apprentissage (`ajuster`) : garde les colonnes de coefficient non nul au λ choisi.
    `perte` = 'carree' (lits) ou 'logistique' (triage, cible ±1, poids w) ; `regle` = 'lasso' ou 'lasso_1se'.
    """

    def __init__(self, perte: str = "carree", regle: str = "lasso", plis: int = PLIS):
        if perte not in ("carree", "logistique") or regle not in REGLES:
            raise ValueError(f"Lasso : perte ∈ (carree, logistique), règle ∈ {REGLES}.")
        self.perte, self.regle, self.plis = perte, regle, plis

    def _resoudre(self, Z, y, w, lam, depart):
        if self.perte == "carree":
            return lasso_lineaire(Z, y, lam, None if depart is None else depart[1])
        return lasso_logistique(Z, y, w, lam, depart)

    def _erreur(self, Z, y, w, b, beta) -> float:
        if self.perte == "carree":
            return float(((y - b - Z @ beta) ** 2).mean())
        return deviance(Z, y, w, b, beta)

    def ajuster(self, X: torch.Tensor, y: torch.Tensor, poids: torch.Tensor | None = None) -> "SelectionLasso":
        X, y = X.to(TYPE), y.to(TYPE)
        w = torch.ones(len(y), dtype=TYPE) if poids is None else poids.to(TYPE) * len(y) / poids.sum()
        Z, _, _ = _reduire(X)
        gmax = _lambda_max_lineaire(Z, y) if self.perte == "carree" else _lambda_max_logistique(Z, y, w)
        self.lambdas = chemin(float(gmax.max()))
        colonnes = []
        for cache in blocs_consecutifs(len(y), self.plis):
            garde = torch.ones(len(y), dtype=torch.bool)
            garde[cache] = False
            if self.perte == "logistique" and len(torch.unique(y[garde])) < 2:
                continue
            Za, ma, sa = _reduire(X[garde])
            Zc = (X[cache] - ma) / sa
            depart, e = None, []
            for lam in self.lambdas:
                depart = self._resoudre(Za, y[garde], w[garde], lam, depart)
                e.append(self._erreur(Zc, y[cache], w[cache], *depart))
            colonnes.append(torch.tensor(e, dtype=TYPE))
        if not colonnes:
            raise ValueError("Lasso : aucun bloc de validation utilisable.")
        erreurs = torch.stack(colonnes, dim=1)                       # λ × blocs
        self.erreur_moyenne = erreurs.mean(1)
        self.erreur_se = erreurs.std(1, unbiased=True) / math.sqrt(erreurs.shape[1]) if erreurs.shape[1] > 1 \
            else torch.zeros(len(self.lambdas), dtype=TYPE)
        k_min = int(torch.argmin(self.erreur_moyenne))
        if self.regle == "lasso":
            k = k_min
        else:                                                         # le plus grand λ sous min + 1 écart-type
            limite = self.erreur_moyenne[k_min] + self.erreur_se[k_min]
            k = next(i for i in range(len(self.lambdas)) if self.erreur_moyenne[i] <= limite)
        self.lam = self.lambdas[k]
        depart = None                                                 # chemin complet sur tout l'apprentissage
        for lam in self.lambdas[:k + 1]:
            depart = self._resoudre(Z, y, w, lam, depart)
        self.b, self.beta = depart
        self.colonnes = [j for j in range(X.shape[1]) if abs(float(self.beta[j])) > 1e-10]
        if not self.colonnes:
            self.colonnes = [int(torch.argmax(gmax))]
        return self

    def transformer(self, X: torch.Tensor) -> torch.Tensor:
        return X[:, self.colonnes]

    def description(self, noms: list[str] | None = None) -> dict:
        return {"regle": self.regle, "lambda": round(self.lam, 6), "variables_gardees": len(self.colonnes),
                "variables": [noms[j] for j in self.colonnes] if noms else self.colonnes}
