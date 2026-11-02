r"""
Valeurs manquantes du triage : neuf traitements comparés par le banc T8.

Le problème
-----------
Aux urgences, les constantes sont rarement toutes prises (chez l'enfant, le pouls n'est noté qu'une fois sur
sept environ). Le modèle a besoin d'un nombre dans chaque case : il faut décider quoi faire des cases vides.
Chaque traitement est APPRIS SUR L'APPRENTISSAGE SEULEMENT (médianes, moyennes, régressions, loi normale,
axes de l'ACP, voisins) puis appliqué tel quel aux passages de calibration et d'évaluation : rien des passages
à prévoir n'entre dans l'imputation. Les indicatrices « constante non prise » (banc T4) restent dans le
tableau quel que soit le traitement : le fait qu'une valeur manque est lui-même une information.

Notations : X (n × p), M_ij = 1 si x_ij est observé. o = colonnes observées d'une ligne, m = colonnes manquantes.
Les méthodes « à modèle » (k-NN, régressions, EM, ACP) travaillent sur les colonnes S = continues ∪ colonnes
ayant au moins une valeur manquante, centrées-réduites par la moyenne et l'écart-type des valeurs observées :
z = (x − x̄_obs)/s_obs ; elles rendent les valeurs dans l'échelle d'origine.

  suppression_lignes    analyse des cas complets : les passages incomplets sont retirés de l'apprentissage ET de
                        l'évaluation (ils ne peuvent pas être prévus). Traité dans validation.evaluer ; ici, rien.
                        Mesuré sur moins de passages : le banc compare aussi la référence sur ces seuls passages.
  suppression_colonnes  les variables manquantes dans plus de 50 % de l'apprentissage sont retirées (mises à 0
                        après standardisation : une colonne constante ne change ni un produit scalaire ni une
                        distance, c'est exactement la retirer) ; les autres manquants : médiane.
  mediane               x_ij ← médiane de la colonne j (référence ; robuste aux valeurs extrêmes).
  moyenne               x_ij ← moyenne de la colonne j (optimale pour l'erreur quadratique si rien d'autre n'est su).
  mediane_age           médiane de la colonne j dans la tranche d'âge du passage : < 1 an, 1–4, 5–14, 15–39, 40–64,
                        ≥ 65 ans (les normes des constantes dépendent de l'âge) ; tranche vide : médiane globale.
  knn                   k plus proches voisins (k = 10) parmi les passages d'apprentissage, avec la distance
                        euclidienne sur les seules colonnes observées des deux côtés, remise à l'échelle :
                            d²(a, b) = (p / |o_a ∩ o_b|) Σ_{j ∈ o_a ∩ o_b} (z_aj − z_bj)²
                        x_ij ← moyenne de x_kj sur les k voisins qui ont la colonne j.
  regression            équations enchaînées (principe de MICE, version déterministe) : on remplit d'abord par
                        la moyenne, puis, 10 fois de suite, chaque colonne incomplète est prédite par une régression
                        ridge sur toutes les autres :
                            β_j = (AᵀA + λI)⁻¹ Aᵀ z_j   (lignes où j est observé, A = autres colonnes + constante),
                            z_ij ← a_iᵀ β_j             (lignes où j manque), λ = 1.
  em                    loi normale multivariée apprise par l'algorithme EM (Dempster, Laird et Rubin, 1977) :
                            E : z_m ← μ_m + Σ_mo Σ_oo⁻¹ (z_o − μ_o),   C = Σ_mm − Σ_mo Σ_oo⁻¹ Σ_om
                            M : μ ← moyenne des lignes complétées ;
                                Σ ← (1/n) Σ_i [(ẑ_i − μ)(ẑ_i − μ)ᵀ + C_i] + λI   (C_i : incertitude des cases imputées)
                        jusqu'à stabilité de μ et Σ (au plus 100 tours) ; puis chaque case manquante reçoit son
                        espérance conditionnelle E[z_m | z_o]. Le terme C_i empêche de sous-estimer la variance
                        (ce que ferait une simple régression répétée).
  acp_iterative         imputation de rang faible : on remplit par 0 (la moyenne), on garde les k premiers axes
                        de l'ACP (k : 80 % de la variance), on remplace les cases manquantes par la reconstruction
                        Z ≈ U_k S_k V_kᵀ, et on recommence jusqu'à stabilité. Pour un nouveau passage, ses
                        coordonnées s sur les axes viennent des seules colonnes observées :
                            s = (V_oᵀ V_o + αI)⁻¹ V_oᵀ z_o,   z_m ← V_m s.
"""
from __future__ import annotations

import torch

from svr.modeles import TYPE

IMPUTATIONS = ("suppression_lignes", "suppression_colonnes", "mediane", "moyenne", "mediane_age", "knn",
               "regression", "em", "acp_iterative")
TRANCHES_AGE = (0.0, 1.0, 5.0, 15.0, 40.0, 65.0, float("inf"))
SEUIL_COLONNE = 0.5          # suppression_colonnes : part de manquants au-delà de laquelle la variable est retirée


def _nanmediane(X: torch.Tensor) -> torch.Tensor:
    m = torch.nanmedian(X, dim=0).values if len(X) else torch.full((X.shape[1],), float("nan"), dtype=X.dtype)
    return torch.where(torch.isnan(m), torch.zeros_like(m), m)


def _motifs(M: torch.Tensor):
    """Regroupe les lignes par motif de cases observées (même motif = mêmes matrices à inverser)."""
    motifs, inverse = torch.unique(M, dim=0, return_inverse=True)
    for k in range(len(motifs)):
        yield motifs[k], torch.nonzero(inverse == k).flatten()


class Imputeur:
    """Apprend un traitement des valeurs manquantes sur l'apprentissage, puis complète n'importe quel tableau."""

    def __init__(self, methode: str = "mediane", continues: list[int] | None = None, col_age: int = 0, k: int = 10):
        if methode not in IMPUTATIONS:
            raise ValueError(f"Imputation inconnue : {methode}. Choix : {', '.join(IMPUTATIONS)}.")
        self.methode, self.continues, self.col_age, self.k = methode, list(continues or []), col_age, k
        self.retirees: list[int] = []

    # ── apprentissage ──────────────────────────────────────────────────────────────────────────
    def ajuster(self, X: torch.Tensor) -> "Imputeur":
        self.mediane = _nanmediane(X)
        manque = torch.isnan(X)
        if self.methode == "suppression_colonnes":
            part = manque.to(TYPE).mean(dim=0)
            self.retirees = [j for j in range(X.shape[1]) if part[j] > SEUIL_COLONNE]
        if self.methode == "moyenne":
            m = torch.nanmean(X, dim=0)
            self.moyenne_col = torch.where(torch.isnan(m), self.mediane, m)
        if self.methode == "mediane_age":
            age = X[:, self.col_age]
            self.par_tranche = []
            for a, b in zip(TRANCHES_AGE[:-1], TRANCHES_AGE[1:]):
                dans = (age >= a) & (age < b)
                med = torch.nanmedian(X[dans], dim=0).values if dans.any() else torch.full_like(self.mediane, float("nan"))
                self.par_tranche.append(torch.where(torch.isnan(med), self.mediane, med))
        if self.methode in ("knn", "regression", "em", "acp_iterative"):
            self.S = sorted(set(self.continues) | {j for j in range(X.shape[1]) if manque[:, j].any()})
            self.S = [j for j in self.S if (~manque[:, j]).any()]          # une colonne jamais observée : médiane (0)
            XS = X[:, self.S]
            self.centre = torch.nanmean(XS, dim=0)
            ecart = torch.sqrt(torch.nanmean((XS - self.centre) ** 2, dim=0))
            self.echelle = torch.where(ecart > 1e-12, ecart, torch.ones_like(ecart))
            Z = (XS - self.centre) / self.echelle
            getattr(self, f"_ajuster_{self.methode}")(Z)
        return self

    def _ajuster_knn(self, Z):
        self.Z_app = Z

    def _ajuster_regression(self, Z, tours: int = 10, lam: float = 1.0):
        M = ~torch.isnan(Z)
        Zf = torch.where(M, Z, torch.zeros_like(Z))
        self.incompletes = [j for j in range(Z.shape[1]) if (~M[:, j]).any()]
        self.beta = {}
        for _ in range(tours):
            for j in self.incompletes:
                autres = [i for i in range(Z.shape[1]) if i != j]
                A = torch.cat([Zf[:, autres], torch.ones(len(Zf), 1, dtype=TYPE)], dim=1)
                obs = M[:, j]
                Ao = A[obs]
                b = torch.linalg.solve(Ao.T @ Ao + lam * torch.eye(A.shape[1], dtype=TYPE), Ao.T @ Zf[obs, j])
                self.beta[j] = b
                Zf[~obs, j] = A[~obs] @ b
        self.tours = tours

    def _ajuster_em(self, Z, tours: int = 100, lam: float = 1e-3, tol: float = 1e-5):
        n, p = Z.shape
        M = ~torch.isnan(Z)
        mu = torch.zeros(p, dtype=TYPE)
        sigma = torch.eye(p, dtype=TYPE)
        for _ in range(tours):
            Zc, C = self._esperance(Z, M, mu, sigma)
            mu_n = Zc.mean(dim=0)
            D = Zc - mu_n
            sigma_n = (D.T @ D + C) / n + lam * torch.eye(p, dtype=TYPE)
            ecart = max(float((mu_n - mu).abs().max()), float((sigma_n - sigma).abs().max()))
            mu, sigma = mu_n, sigma_n
            if ecart < tol:
                break
        self.mu, self.sigma = mu, sigma

    @staticmethod
    def _esperance(Z, M, mu, sigma):
        """Étape E : complète chaque ligne par E[z_m | z_o] ; renvoie aussi Σ_i C_i (covariance conditionnelle)."""
        Zc = torch.where(M, Z, torch.zeros_like(Z))
        C = torch.zeros_like(sigma)
        for motif, lignes in _motifs(M):
            o, m = motif, ~motif
            if not m.any():
                continue
            if not o.any():
                Zc[lignes] = mu.expand(len(lignes), -1).clone()
                C[m.nonzero().flatten()[:, None], m.nonzero().flatten()] += len(lignes) * sigma[m][:, m]
                continue
            S_oo, S_mo = sigma[o][:, o], sigma[m][:, o]
            K = torch.linalg.solve(S_oo, S_mo.T).T                        # Σ_mo Σ_oo⁻¹
            zo = Zc[lignes][:, o]
            Zm = mu[m] + (zo - mu[o]) @ K.T
            bloc = Zc[lignes]
            bloc[:, m] = Zm
            Zc[lignes] = bloc
            Cm = sigma[m][:, m] - K @ S_mo.T
            im = m.nonzero().flatten()
            C[im[:, None], im] += len(lignes) * Cm
        return Zc, C

    def _ajuster_acp_iterative(self, Z, tours: int = 100, part: float = 0.8, tol: float = 1e-6):
        M = ~torch.isnan(Z)
        Zf = torch.where(M, Z, torch.zeros_like(Z))
        _, s, _ = torch.linalg.svd(Zf, full_matrices=False)
        cumul = torch.cumsum(s ** 2, 0) / (s ** 2).sum()
        self.rang = max(1, int((cumul < part).sum()) + 1)
        for _ in range(tours):
            U, s, Vt = torch.linalg.svd(Zf, full_matrices=False)
            R = U[:, :self.rang] * s[:self.rang] @ Vt[:self.rang]
            avant = Zf[~M].clone()
            Zf[~M] = R[~M]
            if len(avant) == 0 or float((Zf[~M] - avant).abs().max()) < tol:
                break
        self.V = Vt[:self.rang].T                                         # p × k

    # ── application ────────────────────────────────────────────────────────────────────────────
    def transformer(self, X: torch.Tensor) -> torch.Tensor:
        X = X.clone()
        manque = torch.isnan(X)
        if self.methode == "moyenne":
            X = torch.where(manque, self.moyenne_col.expand_as(X), X)
        elif self.methode == "mediane_age":
            age = X[:, self.col_age]
            for (a, b), med in zip(zip(TRANCHES_AGE[:-1], TRANCHES_AGE[1:]), self.par_tranche):
                dans = ((age >= a) & (age < b)).unsqueeze(1) & manque
                X = torch.where(dans, med.expand_as(X), X)
        elif self.methode in ("knn", "regression", "em", "acp_iterative"):
            Z = (X[:, self.S] - self.centre) / self.echelle
            Z = getattr(self, f"_completer_{self.methode}")(Z)
            XS = X[:, self.S]
            X[:, self.S] = torch.where(torch.isnan(XS), Z * self.echelle + self.centre, XS)   # l'observé ne bouge pas
        # Tout ce qui reste vide (mediane, suppression_*, colonnes hors S, âge manquant…) : médiane de l'apprentissage.
        return torch.where(torch.isnan(X), self.mediane.expand_as(X), X)

    def _completer_knn(self, Z):
        Ma, Mb = (~torch.isnan(Z)).to(TYPE), (~torch.isnan(self.Z_app)).to(TYPE)
        za, zb = torch.nan_to_num(Z), torch.nan_to_num(self.Z_app)
        communes = Ma @ Mb.T
        d2 = (Ma * za ** 2) @ Mb.T + Ma @ (Mb * zb ** 2).T - 2 * (Ma * za) @ (Mb * zb).T
        d2 = d2.clamp(min=0) * Z.shape[1] / communes.clamp(min=1)
        d2 = torch.where(communes > 0, d2, torch.full_like(d2, float("inf")))
        sortie = Z.clone()
        for j in range(Z.shape[1]):
            vides = torch.isnan(Z[:, j])
            donneurs = ~torch.isnan(self.Z_app[:, j])
            if not vides.any() or not donneurs.any():
                continue
            dj = d2[vides][:, donneurs]
            k = min(self.k, int(donneurs.sum()))
            proches = torch.topk(dj, k, dim=1, largest=False).indices
            sortie[vides, j] = self.Z_app[donneurs, j][proches].mean(dim=1)
        return torch.where(torch.isnan(sortie), torch.zeros_like(sortie), sortie)

    def _completer_regression(self, Z):
        M = ~torch.isnan(Z)
        Zf = torch.where(M, Z, torch.zeros_like(Z))
        for _ in range(self.tours):
            for j in self.incompletes:
                vides = ~M[:, j]
                if not vides.any():
                    continue
                autres = [i for i in range(Z.shape[1]) if i != j]
                A = torch.cat([Zf[vides][:, autres], torch.ones(int(vides.sum()), 1, dtype=TYPE)], dim=1)
                Zf[vides, j] = A @ self.beta[j]
        return Zf

    def _completer_em(self, Z):
        Zc, _ = self._esperance(Z, ~torch.isnan(Z), self.mu, self.sigma)
        return Zc

    def _completer_acp_iterative(self, Z, alpha: float = 1e-3):
        M = ~torch.isnan(Z)
        Zc = torch.where(M, Z, torch.zeros_like(Z))
        for motif, lignes in _motifs(M):
            o, m = motif, ~motif
            if not m.any() or not o.any():
                continue                                                 # rien à faire, ou rien d'observé : 0 (la moyenne)
            Vo, Vm = self.V[o], self.V[m]
            s = torch.linalg.solve(Vo.T @ Vo + alpha * torch.eye(Vo.shape[1], dtype=TYPE), Vo.T @ Zc[lignes][:, o].T).T
            bloc = Zc[lignes]
            bloc[:, m] = s @ Vm.T
            Zc[lignes] = bloc
        return Zc
