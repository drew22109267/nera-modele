r"""
Représentations des variables du triage (banc T7) : faut-il résumer les variables avant de classer ?

Le modèle principal reçoit les variables d'origine (âge, constantes en écart à la norme, plaintes, contexte,
indicatrices de valeurs manquantes), déjà imputées et standardisées par `Preparateur`. Ce banc demande si une
méthode d'analyse multivariée, appliquée AVANT le classement, l'aide : en retirant le bruit, en regroupant des
variables redondantes (pouls et fréquence respiratoire montent souvent ensemble), ou en donnant au modèle le
« profil » du patient. Chaque méthode est apprise sur les passages d'APPRENTISSAGE seulement, puis appliquée
telle quelle aux passages de calibration et d'évaluation : aucune information des passages à prévoir ne fuit.

    originales   les variables telles quelles (référence du banc)
    acp          analyse en composantes principales : on garde les k premiers axes qui expliquent au moins
                 80 % de la variance. Les axes sont les vecteurs propres de la matrice de covariance des
                 variables standardisées, triés par valeur propre décroissante ; un passage est remplacé par
                 ses coordonnées sur ces axes. Les variables binaires (plaintes, indicatrices) sont traitées
                 comme des nombres 0/1 : c'est ce que corrige l'AFDM.
    afdm         analyse factorielle de données mixtes (Pagès, 2004) : une ACP où chaque indicatrice 0/1 de
                 fréquence p est recodée (x − p)/√p, comme dans une analyse des correspondances multiples,
                 et chaque variable continue est centrée-réduite. Une indicatrice rare (convulsions) pèse
                 alors autant dans les axes qu'une constante, au lieu d'être écrasée par les variables
                 continues. Mêmes règles : k axes pour 80 % de la variance.
    kmeans       classification des passages en g groupes (k-means, g = 4, 10 départs, initialisation
                 k-means++ à graine fixe) ; chaque passage est remplacé par son groupe (g indicatrices). Le
                 modèle ne voit plus que le « profil » du patient.
    origine+kmeans   les variables d'origine, plus les g indicatrices du groupe : le profil s'ajoute aux
                 variables au lieu de les remplacer.

Pourquoi ces méthodes et pas d'autres : ACP et AFDM sont linéaires, déterministes et interprétables (chaque
axe est une combinaison connue des variables) ; k-means est la classification la plus simple et la plus
utilisée. t-SNE et UMAP sont écartés : leurs coordonnées n'ont pas de sens hors de l'échantillon où elles
ont été calculées (on ne peut pas y placer un nouveau patient), ce qui les rend inutilisables pour prévoir.
"""
from __future__ import annotations

import torch

from svr.modeles import TYPE

REPRESENTATIONS = ("originales", "acp", "afdm", "kmeans", "origine+kmeans")


def _axes(Z: torch.Tensor, part: float) -> tuple[torch.Tensor, torch.Tensor, int]:
    """Vecteurs propres de la covariance de Z (centrée), triés ; nombre d'axes pour `part` de la variance."""
    n = Z.shape[0]
    cov = Z.T @ Z / max(n - 1, 1)
    valeurs, vecteurs = torch.linalg.eigh(cov)                 # ordre croissant
    ordre = torch.argsort(valeurs, descending=True)
    valeurs, vecteurs = valeurs[ordre].clamp(min=0), vecteurs[:, ordre]
    cumul = torch.cumsum(valeurs, 0) / valeurs.sum().clamp(min=1e-12)
    k = int(torch.searchsorted(cumul, torch.tensor(part, dtype=cumul.dtype)).item()) + 1
    return valeurs, vecteurs, min(k, Z.shape[1])


def kmeans(X: torch.Tensor, g: int, departs: int = 10, iterations: int = 100, graine: int = 0) -> torch.Tensor:
    """Centres de g groupes par k-means (Lloyd), initialisation k-means++, meilleur de `departs` essais
    (plus petite inertie : somme des carrés des distances de chaque point à son centre)."""
    gen = torch.Generator().manual_seed(graine)
    n = X.shape[0]
    g = min(g, n)
    meilleur = None
    for _ in range(departs):
        centres = X[torch.randint(n, (1,), generator=gen)]
        for _ in range(1, g):                                  # k-means++ : loin des centres déjà choisis
            d2 = torch.cdist(X, centres).min(dim=1).values ** 2
            p = d2 / d2.sum() if d2.sum() > 0 else torch.full_like(d2, 1 / n)
            centres = torch.cat([centres, X[torch.multinomial(p, 1, generator=gen)]])
        for _ in range(iterations):
            groupe = torch.cdist(X, centres).argmin(dim=1)
            nouveaux = torch.stack([X[groupe == j].mean(0) if (groupe == j).any() else centres[j] for j in range(g)])
            if torch.allclose(nouveaux, centres):
                break
            centres = nouveaux
        inertie = float((torch.cdist(X, centres).min(dim=1).values ** 2).sum())
        if meilleur is None or inertie < meilleur[0]:
            meilleur = (inertie, centres)
    return meilleur[1]


class Representation:
    """Apprise sur l'apprentissage (`ajuster`), appliquée telle quelle ensuite (`transformer`)."""

    def __init__(self, nom: str, continues: list[int], part_variance: float = 0.80, groupes: int = 4):
        if nom not in REPRESENTATIONS:
            raise ValueError(f"Représentation inconnue : {nom}. Choix : {', '.join(REPRESENTATIONS)}.")
        self.nom, self.continues, self.part, self.g = nom, set(continues), part_variance, groupes

    def ajuster(self, X: torch.Tensor) -> "Representation":
        X = X.to(TYPE)
        if self.nom in ("acp", "afdm"):
            Z = self._recoder(X, apprendre=True)
            self.valeurs, vecteurs, self.k = _axes(Z, self.part)
            self.vecteurs = vecteurs[:, :self.k]
            self.variance_expliquee = float(self.valeurs[:self.k].sum() / self.valeurs.sum().clamp(min=1e-12))
        if self.nom in ("kmeans", "origine+kmeans"):
            self.centres = kmeans(X, self.g)
        return self

    def _recoder(self, X: torch.Tensor, apprendre: bool = False) -> torch.Tensor:
        """ACP : centrage. AFDM : centrage-réduction des continues, (x − p)/√p des indicatrices."""
        if apprendre:
            self.moyenne = X.mean(0)
            binaires = [j for j in range(X.shape[1]) if j not in self.continues]
            self.echelle = torch.ones(X.shape[1], dtype=TYPE)
            if self.nom == "afdm":
                p = self.moyenne[binaires].clamp(1e-6, 1 - 1e-6)
                self.echelle[binaires] = torch.sqrt(p)
                cont = [j for j in self.continues if j < X.shape[1]]
                sd = X[:, cont].std(0, unbiased=False)
                self.echelle[cont] = torch.where(sd < 1e-12, torch.ones_like(sd), sd)
        return (X - self.moyenne) / self.echelle

    def _groupes(self, X: torch.Tensor) -> torch.Tensor:
        groupe = torch.cdist(X, self.centres).argmin(dim=1)
        return torch.nn.functional.one_hot(groupe, self.centres.shape[0]).to(TYPE)

    def transformer(self, X: torch.Tensor) -> torch.Tensor:
        X = X.to(TYPE)
        if self.nom == "originales":
            return X
        if self.nom in ("acp", "afdm"):
            return self._recoder(X) @ self.vecteurs
        if self.nom == "kmeans":
            return self._groupes(X)
        return torch.cat([X, self._groupes(X)], dim=1)

    def description(self) -> dict:
        if self.nom in ("acp", "afdm"):
            return {"axes": self.k, "variance_expliquee": round(self.variance_expliquee, 3)}
        if self.nom in ("kmeans", "origine+kmeans"):
            return {"groupes": int(self.centres.shape[0])}
        return {}
