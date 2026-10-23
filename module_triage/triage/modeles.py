r"""
Modèles de classification du triage, écrits à la main sur le socle du module lit (svr.modeles.ModeleSVR :
boucle d'Adam, meilleur point, arrêt anticipé, moyenne de Polyak).

Chaque modèle donne un SCORE f(x) : plus il est grand, plus le passage est jugé grave. Le score est ensuite
transformé en probabilité par la calibration de Platt (validation.py), la même pour tous les modèles : ils sont
ainsi comparés à armes égales.

1. SVM à noyau, coûts par exemple (svm_rbf, svm_composite)
-----------------------------------------------------------
Comme le SVR à noyau du module lit (théorème du représentant) : f(x) = Σ_j α_j K(x_j, x) + b, f = Kα + b
sur l'entraînement, et
    J(α, b) = ½ αᵀ K α + Σ_i C_i max(0, 1 − y_i f_i)          C_i = C₊ (grave) ou C₋ (non grave)
Avec g_i = ∂L_i/∂f_i = −C_i y_i 1(y_i f_i < 1) (sous-gradient de la hinge pondérée) :
    ∂J/∂α = Kα + K g = K(α + g)          ∂J/∂b = Σ_i g_i
Direction préconditionnée α + g (s'annule là où K(α + g) s'annule si K est inversible : même solution,
atteinte plus vite), exactement comme svr.modeles.SVRNoyau.
Noyau composite : K = ½ K₁ + ½ K₂, K₁ RBF sur l'âge et les constantes, K₂ RBF sur les plaintes et le
contexte (poids fixé à ½ : avec quelques centaines de passages, apprendre β en plus serait fragile).

2. Régression logistique pondérée (logistique)
-----------------------------------------------
    J(w, b) = ½ ‖w‖² + Σ_i C_i ln(1 + exp(−y_i f_i)),      f = Xw + b
    ∂ ln(1 + e^{−m})/∂m = −1/(1 + e^{m}) = −σ(−m)   ⇒   g_i = −C_i y_i σ(−y_i f_i)
    ∂J/∂w = w + Xᵀ g          ∂J/∂b = Σ g_i
La logistique est la version « lisse » du SVM linéaire : même forme de modèle, perte log au lieu de hinge.

3. Arbre et forêt (arbre, foret)
---------------------------------
L'arbre CART de svr.concurrents, appris sur la cible 0/1 : la somme des carrés des écarts dans une feuille
de n₁ graves sur n passages vaut n p(1 − p), avec p = n₁/n : c'est n fois l'impureté de Gini (à un facteur
2 près). La valeur d'une feuille est p, la part de graves. La forêt fait la moyenne de B arbres appris sur
des échantillons bootstrap, avec √d variables tirées à chaque coupure.

4. Règle de référence (regle)
------------------------------
Score = nombre de signes d'alerte (constantes hors de leur plage normale selon l'âge, normes.py). Rien
n'est appris : c'est ce que ferait un soignant qui applique une grille de seuils.
"""
from __future__ import annotations

import math

import torch

from svr.classification import SVMLineaireClassifieur
from svr.concurrents import Arbre
from svr.modeles import TYPE, Entrainement, ModeleSVR
from svr.empilement import softplus
from svr.noyaux import NoyauComposite, NoyauRBF, sigmoide


def couts_exemples(y: torch.Tensor, C_positif: float, C_negatif: float) -> torch.Tensor:
    return torch.where(y > 0, C_positif, C_negatif).to(TYPE)


class SVMNoyauClassifieur(ModeleSVR):
    """SVM à noyau, perte hinge, coût C₊ pour les graves et C₋ pour les non graves."""

    def __init__(self, noyau, C_positif: float = 1.0, C_negatif: float = 1.0, entrainement: Entrainement | None = None):
        super().__init__(C=1.0, entrainement=entrainement)
        if C_positif <= 0 or C_negatif <= 0:
            raise ValueError("C+ et C− doivent être strictement positifs.")
        self.noyau, self.C_positif, self.C_negatif = noyau, C_positif, C_negatif

    def entrainer(self, X, y) -> "SVMNoyauClassifieur":
        y = torch.where(torch.as_tensor(y, dtype=TYPE) > 0, 1.0, -1.0).to(TYPE)
        self.C_exemple = couts_exemples(y, self.C_positif, self.C_negatif)
        return super().entrainer(X, y)

    def _initialiser(self, X, y):
        self.X = X
        self.K = self.noyau(X, X)                                   # calculée une seule fois
        self.parametres = {"alpha": torch.zeros(X.shape[0], dtype=TYPE), "b": torch.zeros(1, dtype=TYPE)}

    def _f_entrainement(self):
        return self.K @ self.parametres["alpha"] + self.parametres["b"]

    def objectif_et_gradients(self, y):
        a, f = self.parametres["alpha"], self._f_entrainement()
        marge = y * f
        g = -self.C_exemple * y * (marge < 1).to(TYPE)              # g_i = −C_i y_i 1(y_i f_i < 1)
        J = 0.5 * float(a @ (self.K @ a)) + float((self.C_exemple * (1 - marge).clamp(min=0)).sum())
        direction = a + g
        grad_alpha = direction if self.entrainement.preconditionne else self.K @ direction
        return J, {"alpha": grad_alpha, "b": g.sum().reshape(1)}, f

    def gradient_exact(self, y) -> dict[str, torch.Tensor]:
        """Le vrai gradient K(α + g), même en mode préconditionné (pour les tests)."""
        f = self._f_entrainement()
        g = -self.C_exemple * y * ((y * f) < 1).to(TYPE)
        return {"alpha": self.K @ (self.parametres["alpha"] + g), "b": g.sum().reshape(1)}

    def predire(self, X):
        return self.noyau(torch.as_tensor(X, dtype=TYPE), self.X) @ self.parametres["alpha"] + self.parametres["b"]


class NoyauMelange:
    """K = ½ RBF(γ₁) sur le bloc 1 + ½ RBF(γ₂) sur le bloc 2 (poids fixe)."""

    def __init__(self, bloc1: list[int], bloc2: list[int], gamma1: float, gamma2: float):
        self.composite = NoyauComposite(bloc1, bloc2, gamma1, gamma2)

    def __call__(self, X, Z):
        K1, K2 = self.composite.partiels(X, Z)
        return NoyauComposite.melanger(K1, K2, torch.zeros(1, dtype=TYPE))      # σ(0) = ½


class RegressionLogistique(ModeleSVR):
    """Logistique pondérée, pénalité ½‖w‖² (voir l'en-tête)."""

    def __init__(self, C_positif: float = 1.0, C_negatif: float = 1.0, entrainement: Entrainement | None = None):
        super().__init__(C=1.0, entrainement=entrainement)
        self.C_positif, self.C_negatif = C_positif, C_negatif

    def entrainer(self, X, y) -> "RegressionLogistique":
        y = torch.where(torch.as_tensor(y, dtype=TYPE) > 0, 1.0, -1.0).to(TYPE)
        self.C_exemple = couts_exemples(y, self.C_positif, self.C_negatif)
        return super().entrainer(X, y)

    def _initialiser(self, X, y):
        self.X = X
        self.parametres = {"w": torch.zeros(X.shape[1], dtype=TYPE), "b": torch.zeros(1, dtype=TYPE)}

    def objectif_et_gradients(self, y):
        w = self.parametres["w"]
        f = self.X @ w + self.parametres["b"]
        m = y * f
        perte = softplus(-m)                                       # ln(1 + e^{−m}), forme stable
        J = 0.5 * float(w @ w) + float((self.C_exemple * perte).sum())
        g = -self.C_exemple * y * sigmoide(-m)                    # g_i = −C_i y_i σ(−m_i)
        return J, {"w": w + self.X.T @ g, "b": g.sum().reshape(1)}, f

    def predire(self, X):
        return torch.as_tensor(X, dtype=TYPE) @ self.parametres["w"] + self.parametres["b"]


class ArbreClassification:
    """Un arbre CART sur la cible 0/1 ; score = part de graves dans la feuille."""

    def __init__(self, profondeur_max: int = 4, min_feuille: int = 10):
        self.profondeur_max, self.min_feuille = profondeur_max, min_feuille

    def entrainer(self, X, y) -> "ArbreClassification":
        y01 = (torch.as_tensor(y, dtype=TYPE) > 0).to(TYPE)
        self.arbre = Arbre(self.profondeur_max, self.min_feuille).construire(torch.as_tensor(X, dtype=TYPE), y01)
        return self

    def predire(self, X):
        return self.arbre.predire(torch.as_tensor(X, dtype=TYPE))


class ForetClassification:
    """Moyenne de B arbres sur échantillons bootstrap, √d variables par coupure."""

    def __init__(self, arbres: int = 200, profondeur_max: int = 8, min_feuille: int = 5, graine: int = 0):
        self.B, self.prof, self.min_feuille, self.graine = arbres, profondeur_max, min_feuille, graine

    def entrainer(self, X, y) -> "ForetClassification":
        X = torch.as_tensor(X, dtype=TYPE)
        y01 = (torch.as_tensor(y, dtype=TYPE) > 0).to(TYPE)
        gen = torch.Generator().manual_seed(self.graine)
        n, d = X.shape
        m = max(1, int(math.sqrt(d)))
        self.arbres = []
        for _ in range(self.B):
            boot = torch.randint(0, n, (n,), generator=gen)
            self.arbres.append(Arbre(self.prof, self.min_feuille, m, gen).construire(X[boot], y01[boot]))
        return self

    def predire(self, X):
        X = torch.as_tensor(X, dtype=TYPE)
        return torch.stack([a.predire(X) for a in self.arbres]).mean(dim=0)


MODELES = ("regle", "logistique", "arbre", "foret", "svm_lineaire", "svm_rbf", "svm_composite")


def fabrique(nom: str, C: float, portee: float, C_positif: float, C_negatif: float, blocs: dict[str, list[int]],
             entrainement: Entrainement | None = None):
    """Fonction sans argument qui crée un modèle neuf (None pour la règle, qui n'apprend rien).
    C multiplie les coûts de classe : C_i = C · C₊ ou C · C₋. La portée du noyau RBF est donnée relativement
    au nombre de variables : γ = portée / d (variables standardisées : ‖x − z‖² grandit comme d)."""
    e = entrainement or Entrainement()
    cp, cn = C * C_positif, C * C_negatif
    if nom == "regle":
        return None
    if nom == "logistique":
        return lambda: RegressionLogistique(cp, cn, e)
    if nom == "arbre":
        return lambda: ArbreClassification()
    if nom == "foret":
        return lambda: ForetClassification()
    if nom == "svm_lineaire":
        return lambda: SVMLineaireClassifieur(cp, cn, e)
    if nom == "svm_rbf":
        d = len(blocs["constantes"]) + len(blocs["autres"])
        return lambda: SVMNoyauClassifieur(NoyauRBF(portee / d), cp, cn, e)
    if nom == "svm_composite":
        b1, b2 = blocs["constantes"], blocs["autres"]
        if not b2:
            raise ValueError("Noyau composite : le bloc « plaintes et contexte » est vide.")
        return lambda: SVMNoyauClassifieur(NoyauMelange(b1, b2, portee / len(b1), portee / len(b2)), cp, cn, e)
    raise ValueError(f"Modèle inconnu : {nom}. Choix : {', '.join(MODELES)}.")
