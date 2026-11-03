r"""
Transfert d'apprentissage pour le triage (banc T9) : un SVM PRÉ-ENTRAÎNÉ sur une grande source externe
(NHAMCS-ED, triage/nhamcs.py, plus de 100 000 passages) puis adapté aux urgences du Cameroun.

Enfants et adultes restent séparés : la source d'un groupe est le MÊME groupe de NHAMCS (jamais enfant → adulte).

1. Variables communes
---------------------
On garde les colonnes du tableau (triage/variables.py) que la source renseigne vraiment (au moins 1 % de
valeurs et pas constantes) : la glycémie et le poids, absents de NHAMCS, sortent du transfert. Imputation et
standardisation (Preparateur) apprises une fois, sur la SOURCE : le modèle pré-entraîné garde ainsi la même
échelle pour tous les mois du Cameroun.

2. Un SVM à noyau sur 100 000 passages : les caractéristiques de Fourier aléatoires
--------------------------------------------------------------------------------
Le SVM à noyau de validation.py calcule la matrice K (n × n) : 100 000² nombres, 80 Go. Rahimi et Recht (2007) :
le noyau RBF est la transformée de Fourier d'une loi normale (théorème de Bochner),
    k(x, z) = exp(−γ‖x − z‖²) = E_ω[ cos(ωᵀx + b) · cos(ωᵀz + b) ] · 2,  ω ~ N(0, 2γ I),  b ~ U[0, 2π].
On tire D couples (ω_j, b_j) une fois pour toutes et on pose
    φ(x) = √(2/D) · (cos(ω_1ᵀx + b_1), …, cos(ω_Dᵀx + b_D)),   alors   φ(x)ᵀφ(z) ≈ k(x, z)
(erreur de l'ordre de 1/√D). Un SVM LINÉAIRE sur φ(x) est donc (presque) le SVM à noyau RBF, mais il ne
coûte que n × D : f(x) = wᵀφ(x) + b, avec D = 500 et γ = portée / d comme le SVM RBF du triage.

3. Pré-entraînement
-------------------
Sur la source du groupe : 80 % pour apprendre, 20 % pour choisir C ∈ {0,1 ; 1 ; 10} (AUC) et calibrer Platt.
Coûts de classe équilibrés (C₊/C₋ = n₋/n₊), comme le modèle principal. Résultat : (w_s, b_s) et f_s.

4. Huit façons d'utiliser le modèle pré-entraîné (mêmes mois du Cameroun, mêmes passages)
-----------------------------------------------------------------------------------------
Dans chaque mois : apprentissage (75 % le plus ancien de l'entraînement) et calibration (25 % le plus récent)
du Cameroun, comme validation.evaluer ; C choisi sur la calibration (AUC) ; probabilité par Platt.
  cible_fourier      SVM sur φ, Cameroun seul (même représentation que le transfert : le juste témoin)
  source_seule       f_s tel quel, Platt de la source : « le modèle américain appliqué au Cameroun »
  source_recalibree  f_s, Platt refait sur la calibration du Cameroun (seule l'échelle des probabilités change)
  reunies            SVM sur la source ET l'apprentissage du Cameroun ; chaque passage du Cameroun pèse
                     n_source / n_cameroun, pour que les deux pèsent autant au total
  augmentation       Daumé (2007) : φ_aug = (φ, φ, 0) pour la source, (φ, 0, φ) pour le Cameroun ; le modèle
                     apprend une partie commune et une partie propre au Cameroun (mêmes poids que « reunies »)
  regularisation_biaisee  Kuzborskij et Orabona (2013) : sur le Cameroun seul,
                         J(w, b) = ½‖w − w_s‖² + Σ C_i max(0, 1 − y_i (wᵀφ_i + b))
                     le modèle part de w_s et ne s'en éloigne que si les données du Cameroun l'exigent
                     (∂J/∂w = (w − w_s) − Σ C_i y_i 1{marge < 1} φ_i)
  a_svm              Yang et al. (2007), SVM adaptatif : f(x) = f_s(x) + Δ(x), Δ(x) = vᵀx_loc + c,
                         J(v, c) = ½‖v‖² + Σ C_i max(0, 1 − y_i (f_s(x_i) + vᵀx_loc,i + c))
                     on n'apprend que la CORRECTION à apporter au modèle source. La correction est linéaire et
                     porte sur TOUTES les variables du registre (x_loc : glycémie, poids et leurs indicatrices
                     compris, préparées sur l'apprentissage du mois). Pourquoi pas sur φ : avec Δ = vᵀφ + c,
                     f = (w_s + v)ᵀφ + (b_s + c) et ½‖v‖² = ½‖w − w_s‖² : ce serait EXACTEMENT la régularisation
                     biaisée écrite autrement. Ici les deux variantes diffèrent vraiment : l'une réapprend le modèle
                     en restant près de la source, l'autre garde la source intacte et la corrige avec ce que seul
                     le registre du Cameroun connaît.
  score_source       SVM sur (φ(x), f_s(x)) : la probabilité de la source devient une variable du Cameroun
Le modèle principal du triage (validation.evaluer, toutes les variables) est la référence du banc (McNemar).
Le transfert est NÉGATIF si une variante fait moins bien que cible_fourier : c'est un résultat, pas une erreur.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import pandas as pd
import torch

from svr.classification import CalibrationPlatt, SVMLineaireClassifieur, auc
from svr.modeles import TYPE, Entrainement
from traitement.urgences import PLAINTES

from .modeles import FourierAleatoire
from .validation import Decoupage, rapport_classes
from .variables import Preparateur, TableauTriage

# Variantes qui n'utilisent AUCUNE donnée du Cameroun pour apprendre (elles sont seulement évaluées dessus),
# variantes qui n'utilisent QUE le Cameroun, et variantes qui combinent les deux.
SOURCES = {"cible_fourier": "Cameroun seul", "source_seule": "externe seule", "source_recalibree": "externe (calibration Cameroun)",
           "reunies": "Cameroun + externe", "augmentation": "Cameroun + externe", "regularisation_biaisee": "Cameroun + externe",
           "a_svm": "Cameroun + externe", "score_source": "Cameroun + externe"}

VARIANTES = ("cible_fourier", "source_seule", "source_recalibree", "reunies", "augmentation",
             "regularisation_biaisee", "a_svm", "score_source")


class SVMAPriori(SVMLineaireClassifieur):
    """
    SVM linéaire, J = ½‖w − w₀‖² + Σ C_i max(0, 1 − y_i (wᵀx_i + b + o_i)) :
    w₀ = 0 et o = 0 : le SVM ordinaire ; w₀ = w_s : régularisation biaisée ; o_i = f_s(x_i) : A-SVM.
    """

    def __init__(self, C_positif=1.0, C_negatif=1.0, entrainement=None, w0=None):
        super().__init__(C_positif, C_negatif, entrainement)
        self.w0 = w0

    def entrainer(self, X, y, poids=None, decalage=None) -> "SVMAPriori":
        self.decalage = torch.zeros(len(X), dtype=TYPE) if decalage is None else torch.as_tensor(decalage, dtype=TYPE)
        return super().entrainer(X, y, poids)

    def _initialiser(self, X, y):
        super()._initialiser(X, y)
        if self.w0 is not None:
            self.parametres["w"] = self.w0.clone()                 # on part du modèle source

    def _f_entrainement(self):
        return self.X @ self.parametres["w"] + self.parametres["b"] + self.decalage

    def objectif_et_gradients(self, y):
        w, f = self.parametres["w"], self._f_entrainement()
        ecart = w - (self.w0 if self.w0 is not None else 0.0)
        marge = y * f
        coef = self.C_exemple * y * (marge < 1).to(TYPE)
        J = 0.5 * float(ecart @ ecart) + float((self.C_exemple * (1 - marge).clamp(min=0)).sum())
        return J, {"w": ecart - self.X.T @ coef, "b": (-coef.sum()).reshape(1)}, f

    def predire(self, X, decalage=None):
        f = torch.as_tensor(X, dtype=TYPE) @ self.parametres["w"] + self.parametres["b"]
        return f if decalage is None else f + decalage


@dataclass
class ConfigTransfert:
    D: int = 500                                  # nombre de caractéristiques de Fourier
    portee: float = 1.0                           # γ = portée / d
    grille_C: tuple = (0.1, 1.0, 10.0)
    part_validation_source: float = 0.2
    max_source: int = 60000                       # passages de la source au plus (mémoire : n × D nombres)
    entrainement: Entrainement = None
    graine: int = 0

    def __post_init__(self):
        if self.entrainement is None:
            self.entrainement = Entrainement(iterations=2000)


class Pretraine:
    """Le modèle source : préparation, φ, SVM linéaire sur φ, Platt de la source."""

    def __init__(self, source: TableauTriage, cible: TableauTriage, cfg: ConfigTransfert):
        self.cfg = cfg
        if source.noms != cible.noms:
            raise ValueError("La source et le Cameroun n'ont pas les mêmes colonnes (options de variables différentes ?).")
        Xs, ys = source.X, source.y
        if len(Xs) > cfg.max_source:                            # sous-échantillon tiré au hasard, graine fixe
            g = torch.Generator().manual_seed(cfg.graine)
            garde = torch.randperm(len(Xs), generator=g)[:cfg.max_source]
            Xs, ys = Xs[garde], ys[garde]
        observe = (~torch.isnan(Xs)).to(TYPE).mean(dim=0)
        self.communes = [j for j in range(Xs.shape[1]) if observe[j] >= 0.01 and float(torch.nan_to_num(Xs[:, j]).std()) > 1e-9]
        self.noms = [source.noms[j] for j in self.communes]
        continues = [self.communes.index(j) for j in source.continues if j in self.communes]
        Xs = Xs[:, self.communes]
        self.prep = Preparateur(continues).ajuster(Xs)
        Zs = self.prep.transformer(Xs)
        self.phi = FourierAleatoire(Zs.shape[1], cfg.D, cfg.portee / Zs.shape[1], cfg.graine)
        Ps = self.phi(Zs)
        g = torch.Generator().manual_seed(cfg.graine + 1)
        ordre = torch.randperm(len(Ps), generator=g)
        n_val = max(1, int(cfg.part_validation_source * len(Ps)))
        val, app = ordre[:n_val], ordre[n_val:]
        cp, cn = rapport_classes(ys[app], "equilibre", 1.0)
        meilleur = None
        for C in cfg.grille_C:
            m = SVMAPriori(C * cp, C * cn, cfg.entrainement).entrainer(Ps[app], ys[app])
            a = auc(m.predire(Ps[val]), ys[val])
            if meilleur is None or a > meilleur[0]:
                meilleur = (a, C, m)
        self.auc_source, self.C, self.modele = meilleur
        self.platt = CalibrationPlatt().ajuster(self.modele.predire(Ps[val]), ys[val])
        self.Ps, self.ys = Ps, ys                                # pour « reunies » et « augmentation »
        self.n_source = len(Ps)

    def phi_de(self, X: torch.Tensor) -> torch.Tensor:
        return self.phi(self.prep.transformer(X[:, self.communes]))

    def score(self, P: torch.Tensor) -> torch.Tensor:
        return self.modele.predire(P)

    def description(self) -> dict:
        return {"passages_source": self.n_source, "variables_communes": len(self.communes), "D": self.cfg.D,
                "C_source": self.C, "auc_validation_source": round(self.auc_source, 4)}


def _choisir(fabriquer, cal_scores, y_cal, grille):
    """Entraîne une variante pour chaque C, garde la meilleure AUC sur la calibration du Cameroun."""
    meilleur = None
    for C in grille:
        modele, sc = fabriquer(C)
        a = auc(cal_scores(modele, sc), y_cal)
        if meilleur is None or a > meilleur[0]:
            meilleur = (a, C, modele, sc)
    return meilleur


def evaluer_transfert(tab: TableauTriage, decoupages: list[Decoupage], pre: Pretraine, cfg: ConfigTransfert,
                      variantes=VARIANTES) -> dict[str, dict]:
    """Pour chaque variante : probabilités hors échantillon sur les mois évalués (même forme que validation.evaluer)."""
    sortie = {v: {"ys": [], "ps": [], "idx": [], "choix": []} for v in variantes}
    P_tout = pre.phi_de(tab.X)
    f_tout = pre.score(P_tout)
    e = cfg.entrainement
    for dec in decoupages:
        ordre = dec.entrainement[torch.argsort(torch.tensor(tab.dates[dec.entrainement.numpy()].asi8))]
        n_cal = max(1, int(round(0.25 * len(ordre))))
        app, cal, ev = ordre[:-n_cal], ordre[-n_cal:], dec.evaluation
        y_app, y_cal = tab.y[app], tab.y[cal]
        if len(torch.unique(y_app)) < 2 or len(torch.unique(y_cal)) < 2:
            continue
        cp, cn = rapport_classes(y_app, "equilibre", 1.0)
        Pa, Pc, Pe = P_tout[app], P_tout[cal], P_tout[ev]
        fa, fc, fe = f_tout[app], f_tout[cal], f_tout[ev]
        poids_cible = pre.n_source / max(1, len(app))
        prep_loc = Preparateur(tab.continues).ajuster(tab.X[app])           # variables complètes du registre (A-SVM)
        La, Lc, Le = (prep_loc.transformer(tab.X[i]) for i in (app, cal, ev))
        for v in variantes:
            if v == "source_seule":
                s_cal, s_ev, platt, C = fc, fe, pre.platt, None
            elif v == "source_recalibree":
                s_cal, s_ev, platt, C = fc, fe, CalibrationPlatt().ajuster(fc, y_cal), None
            else:
                if v == "cible_fourier":
                    fab = lambda C: (SVMAPriori(C * cp, C * cn, e).entrainer(Pa, y_app), None)
                    sc = lambda m, _, X=Pc: m.predire(X)
                    pred = lambda m, X: m.predire(X)
                elif v == "regularisation_biaisee":
                    w_s = pre.modele.parametres["w"]
                    fab = lambda C: (SVMAPriori(C * cp, C * cn, e, w0=w_s).entrainer(Pa, y_app), None)
                    sc = lambda m, _, X=Pc: m.predire(X)
                    pred = lambda m, X: m.predire(X)
                elif v == "a_svm":
                    fab = lambda C: (SVMAPriori(C * cp, C * cn, e).entrainer(La, y_app, decalage=fa), None)
                    sc = lambda m, _: m.predire(Lc, fc)
                    pred = None
                elif v == "score_source":
                    aug = lambda P, f: torch.cat([P, f.unsqueeze(1)], dim=1)
                    fab = lambda C: (SVMAPriori(C * cp, C * cn, e).entrainer(aug(Pa, fa), y_app), None)
                    sc = lambda m, _: m.predire(aug(Pc, fc))
                    pred = lambda m, X: m.predire(aug(X, fe))
                elif v in ("reunies", "augmentation"):
                    if v == "reunies":
                        Xs_, Xa_, Xc_, Xe_ = pre.Ps, Pa, Pc, Pe
                    else:
                        zs, za = torch.zeros_like(pre.Ps), torch.zeros_like(Pa)
                        Xs_ = torch.cat([pre.Ps, pre.Ps, zs], dim=1)
                        Xa_ = torch.cat([Pa, za, Pa], dim=1)
                        Xc_ = torch.cat([Pc, torch.zeros_like(Pc), Pc], dim=1)
                        Xe_ = torch.cat([Pe, torch.zeros_like(Pe), Pe], dim=1)
                    X_ = torch.cat([Xs_, Xa_]); y_ = torch.cat([pre.ys, y_app])
                    poids = torch.cat([torch.ones(len(Xs_), dtype=TYPE), torch.full((len(Xa_),), poids_cible, dtype=TYPE)])
                    cps, cns = rapport_classes(y_, "equilibre", 1.0)
                    fab = lambda C: (SVMAPriori(C * cps, C * cns, e).entrainer(X_, y_, poids=poids), None)
                    sc = lambda m, _, X=Xc_: m.predire(X)
                    pred = lambda m, X=Xe_: m.predire(X)
                a, C, m, _ = _choisir(fab, sc, y_cal, cfg.grille_C)
                s_cal = sc(m, None)
                if v == "a_svm":
                    s_ev = m.predire(Le, fe)
                elif v in ("reunies", "augmentation"):
                    s_ev = pred(m)
                elif v == "score_source":
                    s_ev = pred(m, Pe)
                else:
                    s_ev = pred(m, Pe)
                platt = CalibrationPlatt().ajuster(s_cal, y_cal)
            o = sortie[v]
            o["ps"].append(platt.probabilite(s_ev)); o["ys"].append(tab.y[ev]); o["idx"].append(ev)
            o["choix"].append({"mois": f"{dec.mois:%Y-%m}", "C": C, "apprentissage": len(app), "calibration": len(cal)})
    resultats = {}
    for v, o in sortie.items():
        if not o["ys"]:
            continue
        idx = torch.cat(o["idx"])
        resultats[v] = {"y": torch.cat(o["ys"]), "p": torch.cat(o["ps"]), "indices": idx, "dates": tab.dates[idx.numpy()],
                        "meo": tab.meo[idx], "ids": [tab.ids[i] for i in idx.tolist()] if tab.ids else None,
                        "choix": o["choix"], "groupe": [tab.groupe[i] for i in idx.tolist()]}
    return resultats


def lire_source(chemin: str, groupe: str) -> pd.DataFrame:
    """Passages NHAMCS du groupe (fichier écrit par preparer_nhamcs.py)."""
    s = pd.read_csv(chemin, parse_dates=["date_passage"], low_memory=False)
    s = s[s["groupe"] == groupe].reset_index(drop=True)
    # Fichier préparé avant l'ajout de familles de plaintes : la famille absente est « non observée » (NaN), donc
    # hors des variables communes, jusqu'à ce que preparer_nhamcs.py soit relancé. Colonnes dans l'ordre du registre.
    for f in PLAINTES:
        if f"plainte_{f}" not in s:
            s[f"plainte_{f}"] = float("nan")
    autres = [c for c in s.columns if not c.startswith("plainte_")]
    return s[autres + [f"plainte_{f}" for f in PLAINTES]]
