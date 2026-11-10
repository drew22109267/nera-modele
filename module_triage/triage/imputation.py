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
  knn                   k plus proches voisins parmi les passages d'apprentissage, avec la distance
                        euclidienne sur les seules colonnes observées des deux côtés, remise à l'échelle :
                            d²(a, b) = (p / |o_a ∩ o_b|) Σ_{j ∈ o_a ∩ o_b} (z_aj − z_bj)²
                        x_ij ← moyenne de x_kj sur les k voisins qui ont la colonne j.
                        k est choisi par validation croisée en 5 plis sur l'apprentissage (au plus 1 500 passages
                        tirés au hasard) : chaque case OBSERVÉE d'un pli est cachée, prédite par les k voisins des
                        autres plis, pour chaque k de K_GRILLE ;
                            k* = argmin_k (1/N) Σ (ẑ_ij^(k) − z_ij)²   (N cases, échelle standardisée ;
                                                                         ex aequo : le plus petit k).
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
  softimpute            même famille que l'ACP itérative, sans couper à un rang : σ_i ← max(σ_i − λ, 0)
                        (Mazumder, Hastie et Tibshirani, 2010), λ = fraction de σ_1 ; coordonnées d'une ligne
                        rétrécies par (σ_i − λ)/σ_i.
  Réglages (λ de la ridge et de l'EM, rang de l'ACP, λ/σ_1 du SoftImpute) choisis par validation croisée : 5 plis
  de cases OBSERVÉES cachées (au plus 1 500 passages), erreur quadratique moyenne sur ces cases, échelle
  standardisée ; ex aequo : le plus simple.
  acp_iterative         imputation de rang faible : on remplit par 0 (la moyenne), on garde les k premiers axes
                        de l'ACP (k choisi par validation croisée ; 80 % de la variance si trop peu de passages), on remplace les cases manquantes par la reconstruction
                        Z ≈ U_k S_k V_kᵀ, et on recommence jusqu'à stabilité. Pour un nouveau passage, ses
                        coordonnées s sur les axes viennent des seules colonnes observées :
                            s = (V_oᵀ V_o + αI)⁻¹ V_oᵀ z_o,   z_m ← V_m s.
"""
from __future__ import annotations

import math

import torch

from svr.modeles import TYPE

IMPUTATIONS = ("suppression_lignes", "suppression_colonnes", "mediane", "moyenne", "mediane_age", "knn",
               "regression", "em", "acp_iterative", "softimpute")
A_REGLAGE = ("regression", "em", "acp_iterative", "softimpute")
GRILLE_LAMBDA_RIDGE = (0.01, 0.1, 1.0, 10.0, 100.0)
GRILLE_LAMBDA_EM = (1e-4, 1e-3, 1e-2, 1e-1)
GRILLE_SOFTIMPUTE = (0.01, 0.03, 0.1, 0.2, 0.3, 0.5)
TRANCHES_AGE = (0.0, 1.0, 5.0, 15.0, 40.0, 65.0, float("inf"))
SEUIL_COLONNE = 0.5          # suppression_colonnes : part de manquants au-delà de laquelle la variable est retirée
K_GRILLE = (1, 3, 5, 7, 10, 15, 21, 31, 51)      # valeurs de k essayées par la validation croisée du k-NN
PLIS_K, LIGNES_CHOIX_K = 5, 1500


def _nanmediane(X: torch.Tensor) -> torch.Tensor:
    m = torch.nanmedian(X, dim=0).values if len(X) else torch.full((X.shape[1],), float("nan"), dtype=X.dtype)
    return torch.where(torch.isnan(m), torch.zeros_like(m), m)


def _nanborne(Z: torch.Tensor, f) -> torch.Tensor:
    """Minimum ou maximum de chaque colonne sur les cases observées (colonne vide : 0, la moyenne)."""
    M = ~torch.isnan(Z)
    remplace = float("inf") if f is torch.amin else -float("inf")
    b = f(torch.where(M, Z, torch.full_like(Z, remplace)), dim=0)
    return torch.where(M.any(dim=0), b, torch.zeros_like(b))


def _motifs(M: torch.Tensor):
    """Regroupe les lignes par motif de cases observées (même motif = mêmes matrices à inverser)."""
    motifs, inverse = torch.unique(M, dim=0, return_inverse=True)
    for k in range(len(motifs)):
        yield motifs[k], torch.nonzero(inverse == k).flatten()


def _groupes(M: torch.Tensor) -> list[tuple]:
    """Motifs de M avec leurs indices (lignes, colonnes observées, colonnes vides), calculés une fois par masque."""
    return [(lignes, motif.nonzero().flatten(), (~motif).nonzero().flatten(), bool(motif.any()), bool((~motif).any()))
            for motif, lignes in _motifs(M)]


class Imputeur:
    """Apprend un traitement des valeurs manquantes sur l'apprentissage, puis complète n'importe quel tableau."""

    def __init__(self, methode: str = "mediane", continues: list[int] | None = None, col_age: int = 0, k: int | None = None,
                 reglage: float | None = None):
        if methode not in IMPUTATIONS:
            raise ValueError(f"Imputation inconnue : {methode}. Choix : {', '.join(IMPUTATIONS)}.")
        self.methode, self.continues, self.col_age, self.k = methode, list(continues or []), col_age, k
        self.retirees: list[int] = []
        self.erreurs_k = None                      # k = None : choisi par validation croisée (k-NN)
        self.reglage, self.erreurs_reglage = reglage, None   # None : choisi par validation croisée

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
        if self.methode in ("knn", *A_REGLAGE):
            self.S = sorted(set(self.continues) | {j for j in range(X.shape[1]) if manque[:, j].any()})
            self.S = [j for j in self.S if (~manque[:, j]).any()]          # une colonne jamais observée : médiane (0)
            XS = X[:, self.S]
            self.centre = torch.nanmean(XS, dim=0)
            ecart = torch.sqrt(torch.nanmean((XS - self.centre) ** 2, dim=0))
            self.echelle = torch.where(ecart > 1e-12, ecart, torch.ones_like(ecart))
            Z = (XS - self.centre) / self.echelle
            self.z_min, self.z_max = _nanborne(Z, torch.amin), _nanborne(Z, torch.amax)
            if self.methode in A_REGLAGE and self.reglage is None:
                self.reglage, self.erreurs_reglage = self._choisir_reglage(Z)
            getattr(self, f"_ajuster_{self.methode}")(Z)
        return self

    def _ajuster_knn(self, Z):
        self.Z_app = Z
        if self.k is None:
            self.k, self.erreurs_k = self._choisir_k(Z)

    @staticmethod
    def _choisir_k(Z, plis: int = PLIS_K, graine: int = 1):
        """
        Validation croisée en `plis` plis : pour chaque pli et chaque colonne j, les cases observées de j sont
        cachées et prédites par la moyenne de x_j chez les k plus proches des autres plis (distance sur les autres
        colonnes observées des deux côtés). Renvoie le k de plus petite erreur quadratique moyenne (échelle
        standardisée, toutes colonnes confondues ; ex aequo : le plus petit) et l'erreur de chaque k.
        Moins de 2 × plis passages : k = √n.
        """
        gen = torch.Generator().manual_seed(graine)
        if len(Z) > LIGNES_CHOIX_K:
            Z = Z[torch.randperm(len(Z), generator=gen)[:LIGNES_CHOIX_K]]
        n, p = Z.shape
        grille = [k for k in K_GRILLE if k <= n - -(-n // plis)]
        if n < 2 * plis or not grille:
            return max(1, round(math.sqrt(n))), None
        ordre = torch.randperm(n, generator=gen)
        somme, cases = dict.fromkeys(grille, 0.0), 0
        for f in range(plis):
            test, app = ordre[f::plis], torch.cat([ordre[g::plis] for g in range(plis) if g != f])
            Ma, Mb = (~torch.isnan(Z[test])).to(TYPE), (~torch.isnan(Z[app])).to(TYPE)
            za, zb = torch.nan_to_num(Z[test]), torch.nan_to_num(Z[app])
            S = (Ma * za ** 2) @ Mb.T + Ma @ (Mb * zb ** 2).T - 2 * (Ma * za) @ (Mb * zb).T
            C = Ma @ Mb.T
            for j in range(p):
                lignes, donneurs = Ma[:, j] > 0, Mb[:, j] > 0
                if not lignes.any() or not donneurs.any():
                    continue
                # On retire la colonne j de la distance : les deux côtés l'ont, elle comptait pour (z_aj − z_bj)².
                Sj = S[lignes][:, donneurs] - (za[lignes, j:j + 1] - zb[donneurs, j].unsqueeze(0)) ** 2
                Cj = C[lignes][:, donneurs] - 1
                d2 = torch.where(Cj > 0, Sj.clamp(min=0) * p / Cj.clamp(min=1), torch.full_like(Sj, float("inf")))
                valeurs = zb[donneurs, j][torch.argsort(d2, dim=1, stable=True)]
                for k in grille:
                    pred = valeurs[:, :k].mean(dim=1)
                    somme[k] += float(((pred - za[lignes, j]) ** 2).sum())
                cases += int(lignes.sum())
        if not cases:
            return max(1, round(math.sqrt(n))), None
        erreurs = {k: s / cases for k, s in somme.items()}
        return min(erreurs, key=lambda k: (erreurs[k], k)), erreurs

    def _grille(self, p: int) -> tuple:
        return {"regression": GRILLE_LAMBDA_RIDGE, "em": GRILLE_LAMBDA_EM, "softimpute": GRILLE_SOFTIMPUTE,
                "acp_iterative": tuple(range(1, max(p, 2)))}[self.methode]

    def _choisir_reglage(self, Z, plis: int = PLIS_K, graine: int = 1):
        """
        Les cases OBSERVÉES (au plus LIGNES_CHOIX_K passages) sont réparties au hasard en `plis` plis ; chaque pli
        est caché à son tour, le traitement est appris sur le reste avec chaque valeur de la grille et complète les
        cases cachées ; erreur = moyenne de (prédit − vrai)² (échelle standardisée). Ex aequo : le plus simple.
        """
        gen = torch.Generator().manual_seed(graine)
        if len(Z) > LIGNES_CHOIX_K:
            Z = Z[torch.randperm(len(Z), generator=gen)[:LIGNES_CHOIX_K]]
        obs = torch.nonzero(~torch.isnan(Z))
        if len(Z) < 2 * plis or len(obs) < 2 * plis:
            return None, None
        pli = torch.randperm(len(obs), generator=gen) % plis
        grille = self._grille(Z.shape[1])
        somme = dict.fromkeys(grille, 0.0)
        for f in range(plis):
            cache = obs[pli == f]
            Zm = Z.clone()
            Zm[cache[:, 0], cache[:, 1]] = float("nan")
            vrai = Z[cache[:, 0], cache[:, 1]]
            for v in grille:
                essai = Imputeur(self.methode, reglage=v)
                getattr(essai, f"_ajuster_{self.methode}")(Zm)
                pred = getattr(essai, f"_completer_{self.methode}")(Zm)[cache[:, 0], cache[:, 1]]
                somme[v] += float(((pred - vrai) ** 2).sum())
        erreurs = {v: t / len(obs) for v, t in somme.items()}
        simple = (lambda v: v) if self.methode == "acp_iterative" else (lambda v: -v)
        return min(erreurs, key=lambda v: (erreurs[v], simple(v))), erreurs

    def _ajuster_regression(self, Z, tours: int = 10):
        lam = 1.0 if self.reglage is None else self.reglage
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

    def _ajuster_em(self, Z, tours: int = 100, tol: float = 1e-5):
        lam = 1e-3 if self.reglage is None else self.reglage
        n, p = Z.shape
        M = ~torch.isnan(Z)
        mu = torch.zeros(p, dtype=TYPE)
        sigma = torch.eye(p, dtype=TYPE)
        groupes = _groupes(M)                     # une fois : le masque ne change pas pendant l'EM
        for _ in range(tours):
            Zc, C = self._esperance(Z, M, mu, sigma, groupes)
            mu_n = Zc.mean(dim=0)
            D = Zc - mu_n
            sigma_n = (D.T @ D + C) / n + lam * torch.eye(p, dtype=TYPE)
            ecart = max(float((mu_n - mu).abs().max()), float((sigma_n - sigma).abs().max()))
            mu, sigma = mu_n, sigma_n
            if ecart < tol:
                break
        self.mu, self.sigma = mu, sigma

    @staticmethod
    def _esperance(Z, M, mu, sigma, groupes=None):
        """Étape E : complète chaque ligne par E[z_m | z_o] ; renvoie aussi Σ_i C_i (covariance conditionnelle).
        `groupes` : motifs du masque déjà calculés (_groupes), mêmes opérations dans le même ordre."""
        Zc = torch.where(M, Z, torch.zeros_like(Z))
        C = torch.zeros_like(sigma)
        for lignes, io, im, a_obs, a_vide in (groupes if groupes is not None else _groupes(M)):
            if not a_vide:
                continue
            if not a_obs:
                Zc[lignes] = mu.expand(len(lignes), -1).clone()
                C[im[:, None], im] += len(lignes) * sigma[im][:, im]
                continue
            S_oo, S_mo = sigma[io][:, io], sigma[im][:, io]
            K = torch.linalg.solve(S_oo, S_mo.T).T                        # Σ_mo Σ_oo⁻¹
            zo = Zc[lignes][:, io]
            Zc[lignes[:, None], im] = mu[im] + (zo - mu[io]) @ K.T
            Cm = sigma[im][:, im] - K @ S_mo.T
            C[im[:, None], im] += len(lignes) * Cm
        return Zc, C

    def _ajuster_acp_iterative(self, Z, tours: int = 100, part: float = 0.8, tol: float = 1e-6):
        M = ~torch.isnan(Z)
        Zf = torch.where(M, Z, torch.zeros_like(Z))
        if self.reglage is None:
            _, s, _ = torch.linalg.svd(Zf, full_matrices=False)
            cumul = torch.cumsum(s ** 2, 0) / (s ** 2).sum()
            self.rang = max(1, int((cumul < part).sum()) + 1)
        else:
            self.rang = int(min(self.reglage, Z.shape[1]))
        for _ in range(tours):
            U, s, Vt = torch.linalg.svd(Zf, full_matrices=False)
            R = U[:, :self.rang] * s[:self.rang] @ Vt[:self.rang]
            avant = Zf[~M].clone()
            Zf[~M] = R[~M]
            if len(avant) == 0 or float((Zf[~M] - avant).abs().max()) < tol:
                break
        # Le rang ne peut pas dépasser le nombre d'axes de la SVD, min(lignes, colonnes) : un mois d'apprentissage
        # de moins de passages que de variables donnait V à 10 axes et retrecir à 11 (arrêt du banc T8, adultes).
        self.rang = min(self.rang, Vt.shape[0])
        self.V = Vt[:self.rang].T                                         # p × k
        self.retrecir = torch.ones(self.rang, dtype=TYPE)

    def _ajuster_softimpute(self, Z, tours: int = 100, tol: float = 1e-6):
        """R = U diag(max(σ − λ, 0)) Vᵀ, cases vides ← R jusqu'à stabilité ; λ = reglage × σ_1 (Z rempli par 0)."""
        M = ~torch.isnan(Z)
        Zf = torch.where(M, Z, torch.zeros_like(Z))
        lam = (0.1 if self.reglage is None else self.reglage) * float(torch.linalg.svdvals(Zf)[0])
        for _ in range(tours):
            U, s, Vt = torch.linalg.svd(Zf, full_matrices=False)
            d = (s - lam).clamp(min=0)
            avant = Zf[~M].clone()
            Zf[~M] = ((U * d) @ Vt)[~M]
            if len(avant) == 0 or float((Zf[~M] - avant).abs().max()) < tol:
                break
        garde = d > 0
        garde[0] = True
        self.rang = int(garde.sum())
        self.V = Vt[garde].T
        self.retrecir = torch.where(s[garde] > 0, d[garde] / s[garde], torch.zeros_like(d[garde]))

    def _completer_softimpute(self, Z):
        return self._completer_acp_iterative(Z)

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
        elif self.methode in ("knn", *A_REGLAGE):
            Z = (X[:, self.S] - self.centre) / self.echelle
            Z = getattr(self, f"_completer_{self.methode}")(Z)
            Z = torch.minimum(torch.maximum(Z, self.z_min), self.z_max)     # jamais hors des valeurs vues à l'apprentissage
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
            Vo, Vm = self.V[o], self.V[m] * self.retrecir                # SoftImpute : axes rétrécis
            s = torch.linalg.solve(Vo.T @ Vo + alpha * torch.eye(Vo.shape[1], dtype=TYPE), Vo.T @ Zc[lignes][:, o].T).T
            bloc = Zc[lignes]
            bloc[:, m] = s @ Vm.T
            Zc[lignes] = bloc
        return Zc
