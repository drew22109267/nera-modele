r"""
Triage en TROIS niveaux de priorité, ordonnés :

    niveau 2  grave        rouge   priorité 1 : hospitalisé, référé, décédé, sortie contre avis médical
    niveau 1  moyen        jaune   priorité 2 : mise en observation (MEO)
    niveau 0  non grave    vert    priorité 3 : externe, retour à domicile

Méthode : classification ordinale par deux SVM binaires (Frank et Hall, 2001)
------------------------------------------------------------------------------
Les niveaux sont ORDONNÉS (grave > moyen > non grave) : au lieu d'un SVM à trois classes sans ordre, on apprend
les deux questions « emboîtées » que pose l'ordre, chacune par le SVM binaire déjà écrit et calibré (Platt) :
    modèle « haut »   P(niveau ≥ 2) = P(grave)                    (MEO comptée avec les non graves)
    modèle « bas »    P(niveau ≥ 1) = P(grave ou moyen)            (MEO comptée avec les graves)
Les trois probabilités s'en déduisent :
    P(grave) = p_haut,   P(moyen) = p_bas − p_haut,   P(non grave) = 1 − p_bas.
Les deux modèles sont appris séparément : rien n'oblige p_bas ≥ p_haut. On impose l'ordre en prenant
p_bas ← max(p_bas, p_haut) (sinon P(moyen) serait négative) ; le nombre de passages corrigés est compté.

Décision : la priorité de plus petit coût attendu
-------------------------------------------------
Matrice des coûts c(i, j) = coût de donner la priorité j à un patient de niveau vrai i, avec r = c₊/c₋ (le
rapport des coûts du triage binaire, 4 par défaut) :
    sous-triage (j < i) :  c(i, j) = r (i − j)      un grave mis en vert coûte 2r, un grave mis en jaune r ;
    sur-triage  (j > i) :  c(i, j) = j − i          un non grave mis en rouge coûte 2, mis en jaune 1 ;
    c(i, i) = 0.
Pour un passage de probabilités (P₀, P₁, P₂), le coût attendu de la priorité j est Σ_i P_i c(i, j) ; on donne la
priorité j de plus petit coût attendu. Avec deux niveaux seulement, c'est exactement le seuil s* = 1/(1 + r)
du triage binaire. La matrice est à valider avec le service (comme r).

Mesures (écrites à la main)
---------------------------
    matrice de confusion 3 × 3 O[i, j] (vrai i, prédit j)
    exactitude             Σ_i O[i, i] / n
    sous-triage            part des passages mis à une priorité PLUS BASSE que leur niveau (le danger)
    sur-triage             part mise plus haut (encombrement)
    rappel de chaque niveau  O[i, i] / Σ_j O[i, j] ; « graves en rouge » = rappel du niveau 2
    graves sous-triés      part des graves mis en jaune ou en vert
    coût moyen             Σ O[i, j] c(i, j) / n
    kappa pondéré (quadratique, Cohen 1968) : accord entre priorité donnée et niveau vrai, corrigé du hasard,
        les grands écarts pesant plus : w_ij = 1 − (i − j)²/4,  κ_w = (Σ w O/n − Σ w E/n) / (1 − Σ w E/n),
        E[i, j] = n_i. n_.j / n (accord attendu au hasard). κ_w = 1 : accord parfait ; 0 : le hasard.
    AUC haut, AUC bas      les AUC des deux questions (grave contre le reste ; grave ou moyen contre non grave)
    Brier multiclasse      (1/n) Σ_passages Σ_niveaux (P_i − 1[vrai = i])²
McNemar (deux modèles, mêmes passages) : un passage est « juste » si la priorité donnée est son niveau vrai.
Bootstrap apparié du coût moyen, par jours (bootstrap_cout) : le test qui tient compte des coûts.
"""
from __future__ import annotations

import pandas as pd
import torch

from svr.classification import auc
from svr.modeles import TYPE

NIVEAUX = ("non grave", "moyen", "grave")          # indices 0, 1, 2
COULEURS = ("vert", "jaune", "rouge")


def matrice_couts(r: float) -> torch.Tensor:
    """c(i, j) : r (i − j) en sous-triage, (j − i) en sur-triage (voir l'en-tête)."""
    c = torch.zeros(3, 3, dtype=TYPE)
    for i in range(3):
        for j in range(3):
            c[i, j] = r * (i - j) if i > j else (j - i)
    return c


def sous_resultat(res: dict, k: torch.Tensor) -> dict:
    """Les lignes k d'un résultat (tous les champs indexés par passage)."""
    out = dict(res)
    for cle in ("y", "p", "score", "seuil90", "meo", "complet", "indices"):
        if cle in res and res[cle] is not None:
            out[cle] = res[cle][k]
    if "dates" in res:
        out["dates"] = res["dates"][k.numpy()]
    if res.get("ids") is not None:
        out["ids"] = [res["ids"][i] for i in k.tolist()]
    if res.get("groupe") is not None:
        out["groupe"] = [res["groupe"][i] for i in k.tolist()]
    return out


def combiner(haut: dict, bas: dict) -> dict:
    """
    Réunit le modèle « haut » (y = +1 : grave) et le modèle « bas » (y = +1 : grave ou MEO) en un résultat à
    trois niveaux, sur les passages évalués par les deux (un mois peut manquer à l'un s'il n'avait qu'une classe).
    Champs : y = niveau vrai (0, 1, 2), p = n × 3 probabilités (non grave, moyen, grave), seuil90 = celui du
    modèle haut (détection des graves), choix = les réglages des deux modèles.
    """
    pos_haut = {int(i): k for k, i in enumerate(haut["indices"].tolist())}
    communs = [(pos_haut[int(i)], k) for k, i in enumerate(bas["indices"].tolist()) if int(i) in pos_haut]
    if not communs:
        raise ValueError("Aucun passage évalué à la fois par le modèle « grave » et le modèle « grave ou moyen ».")
    kh = torch.tensor([a for a, _ in communs], dtype=torch.long)
    kb = torch.tensor([b for _, b in communs], dtype=torch.long)
    h, b = sous_resultat(haut, kh), sous_resultat(bas, kb)
    p_haut = torch.as_tensor(h["p"], dtype=TYPE)
    p_bas_brut = torch.as_tensor(b["p"], dtype=TYPE)
    p_bas = torch.maximum(p_bas_brut, p_haut)                       # ordre imposé : P(≥ moyen) ≥ P(grave)
    y = (torch.as_tensor(b["y"]) > 0).to(TYPE) + (torch.as_tensor(h["y"]) > 0).to(TYPE)
    P = torch.stack([1 - p_bas, p_bas - p_haut, p_haut], dim=1)
    out = {**h, "y": y, "p": P, "p_bas_brut": p_bas_brut, "ordre_corrige": int((p_bas_brut < p_haut).sum()),
           "choix": {"grave (haut)": haut.get("choix"), "grave ou moyen (bas)": bas.get("choix")}}
    out.pop("score", None)
    return out


def decider(P: torch.Tensor, r: float) -> torch.Tensor:
    """Priorité de plus petit coût attendu : argmin_j Σ_i P_i c(i, j)."""
    return torch.argmin(torch.as_tensor(P, dtype=TYPE) @ matrice_couts(r), dim=1)


def decision_binaire(P: torch.Tensor, seuil: float, question: str) -> torch.Tensor:
    """Ancien triage à deux niveaux lu sur la même échelle : rouge si P(question) ≥ s, sinon vert (jamais jaune)."""
    P = torch.as_tensor(P, dtype=TYPE)
    p = P[:, 2] if question == "grave" else P[:, 1] + P[:, 2]
    return torch.where(p >= seuil, 2, 0)


def confusion3(y, pred) -> torch.Tensor:
    O = torch.zeros(3, 3, dtype=TYPE)
    for i, j in zip(torch.as_tensor(y).long().tolist(), torch.as_tensor(pred).long().tolist()):
        O[i, j] += 1
    return O


def kappa_pondere(O: torch.Tensor) -> float:
    """Kappa pondéré quadratique de Cohen (voir l'en-tête)."""
    n = float(O.sum())
    if n == 0:
        return float("nan")
    k = O.shape[0]
    i = torch.arange(k, dtype=TYPE)
    w = 1 - (i[:, None] - i[None, :]) ** 2 / (k - 1) ** 2
    E = O.sum(1, keepdim=True) * O.sum(0, keepdim=True) / n
    po, pe = float((w * O).sum()) / n, float((w * E).sum()) / n
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def _part(a: float, b: float) -> float:
    return a / b if b else float("nan")


def resume3(y, P, r: float, pred=None) -> dict:
    """Toutes les mesures du triage à trois niveaux (voir l'en-tête). `pred` : priorités déjà décidées (sinon decider)."""
    y = torch.as_tensor(y).long()
    P = torch.as_tensor(P, dtype=TYPE)
    pred = decider(P, r) if pred is None else torch.as_tensor(pred).long()
    O = confusion3(y, pred)
    n = float(O.sum())
    nv = O.sum(1)
    c = matrice_couts(r)
    sous = float(sum(O[i, j] for i in range(3) for j in range(3) if j < i))
    sur = float(sum(O[i, j] for i in range(3) for j in range(3) if j > i))
    un = torch.nn.functional.one_hot(y, 3).to(TYPE)
    return {"passages": int(n), "graves": int(nv[2]), "moyens": int(nv[1]), "non_graves": int(nv[0]),
            "exactitude": _part(float(O.trace()), n), "sous_triage": _part(sous, n), "sur_triage": _part(sur, n),
            "graves_en_rouge": _part(float(O[2, 2]), float(nv[2])),
            "graves_sous_tries": _part(float(O[2, 0] + O[2, 1]), float(nv[2])),
            "moyens_en_jaune": _part(float(O[1, 1]), float(nv[1])),
            "non_graves_en_vert": _part(float(O[0, 0]), float(nv[0])),
            "rouges": _part(float(O[:, 2].sum()), n), "jaunes": _part(float(O[:, 1].sum()), n),
            "verts": _part(float(O[:, 0].sum()), n),
            "cout_moyen": _part(float((O * c).sum()), n), "kappa_pondere": kappa_pondere(O),
            "auc_haut": auc(P[:, 2], (y == 2).to(TYPE)), "auc_bas": auc(P[:, 1] + P[:, 2], (y >= 1).to(TYPE)),
            "brier3": float(((P - un) ** 2).sum(1).mean()) if len(y) else float("nan"),
            "confusion": O.to(torch.int64).tolist()}


def justes(y, pred_a, pred_b):
    """Juste = priorité donnée égale au niveau vrai ; renvoie (juste_a, juste_b) pour triage.mesures.mcnemar."""
    y = torch.as_tensor(y).long()
    return torch.as_tensor(pred_a).long() == y, torch.as_tensor(pred_b).long() == y


def bootstrap_cout(y, pred_a, pred_b, r: float, jours, tirages: int = 2000, graine: int = 0) -> dict:
    """
    Test apparié sur le COÛT MOYEN (ce que le triage minimise), en complément de McNemar qui ne compte que
    « juste / faux » et ignore qu'un grave mis en vert coûte plus qu'un non grave mis en jaune.
    Pour chaque passage : d_k = c(y_k, a_k) − c(y_k, b_k) ; d̄ < 0 : A coûte moins que B.
    Bootstrap PAR JOURS (les passages d'un même jour ne sont pas indépendants : même équipe, même affluence) :
    on tire avec remise autant de jours qu'il y en a, on recalcule d̄* ; intervalle à 95 % = percentiles 2,5 et
    97,5 ; p bilatérale = 2 · min(P(d̄* ≤ 0), P(d̄* ≥ 0)) (bornée à 1).
    """
    c = matrice_couts(r)
    y = torch.as_tensor(y).long()
    d = c[y, torch.as_tensor(pred_a).long()] - c[y, torch.as_tensor(pred_b).long()]
    codes = torch.as_tensor(pd.Series(pd.DatetimeIndex(jours).normalize()).factorize()[0])
    m = int(codes.max()) + 1 if len(codes) else 0
    if m < 2:
        return {"diff_cout": float(d.mean()) if len(d) else float("nan"), "ic_bas": float("nan"),
                "ic_haut": float("nan"), "p_valeur": float("nan")}
    somme = torch.zeros(m, dtype=TYPE).index_add_(0, codes, d.to(TYPE))
    nombre = torch.zeros(m, dtype=TYPE).index_add_(0, codes, torch.ones_like(d, dtype=TYPE))
    g = torch.Generator().manual_seed(graine)
    tirage = torch.randint(0, m, (tirages, m), generator=g)
    moyennes = somme[tirage].sum(1) / nombre[tirage].sum(1)
    p = min(1.0, 2.0 * min(float((moyennes <= 0).to(TYPE).mean()), float((moyennes >= 0).to(TYPE).mean())))
    if float(d.abs().sum()) == 0.0:
        p = 1.0
    return {"diff_cout": round(float(d.mean()), 4), "ic_bas": round(float(torch.quantile(moyennes, 0.025)), 4),
            "ic_haut": round(float(torch.quantile(moyennes, 0.975)), 4), "p_valeur": round(p, 4)}
