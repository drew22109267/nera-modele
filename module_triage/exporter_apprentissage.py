r"""
Exporte, pour l'outil de saisie (rubrique « Apprentissage : SVM et arbres »), ce que font les modèles du triage
sur les passages réels : comment ils séparent les patients, comment ils apprennent, et où commencent le sous- et
le sur-apprentissage. Tous les calculs sont faits ICI, avec les classes de triage/modeles.py ; l'outil ne fait
qu'afficher le fichier.

Usage (WSL, depuis nera-modele/module_triage) :
    ~/memoire-env/bin/python exporter_apprentissage.py <registre-urgences.csv> [--groupes enfant adulte]

Écrit resultats/triage/apprentissage_<groupe>.json (jamais sur GitHub : il contient des coordonnées de passages,
sans identifiant, sans date, sans texte).

Données. Passages du groupe antérieurs au verrou, avec une décision lisible (cible du modèle principal : MEO =
grave). Séparation chronologique : les 75 % les plus anciens pour apprendre, les 25 % les plus récents pour
évaluer (jamais vus). Préparation (médiane, standardisation) apprise sur l'apprentissage seul (Preparateur).

1. Plan des patients : ACP des variables préparées, apprise sur l'apprentissage ; les deux premiers axes
   résument les passages (inertie et variables les plus liées à chaque axe exportées).
2. Frontières : chaque modèle (SVM linéaire, RBF, laplacien, arbre, forêt, logistique) est appris par sa classe
   Python sur les DEUX coordonnées du plan ; on exporte son score sur une grille du plan, son seuil de décision
   et ses AUC (apprentissage, évaluation). C'est une vue en deux dimensions : le modèle principal, lui, utilise
   toutes les variables (son AUC est exportée à part).
3. Apprentissage du modèle principal (SVM RBF, toutes les variables) : J à chaque pas d'Adam (historique de
   ModeleSVR) et l'AUC du modèle arrêté après t pas, sur l'apprentissage et sur l'évaluation ; frontière du SVM
   RBF du plan après t pas, et un « film » de 24 images (t de 1 à la fin, espacés géométriquement) que l'outil
   rejoue en 2D et en 3D.
4. Courbes de complexité (toutes les variables) : portée du noyau (SVM RBF), C (SVM linéaire), profondeur
   (arbre) ; erreur = 1 − AUC sur l'apprentissage et sur l'évaluation. Courbe d'apprentissage : SVM RBF appris
   sur une part croissante des passages d'apprentissage.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
from pathlib import Path

import pandas as pd
import torch

import triage  # noqa: F401  (rend le dossier module_lit importable)
from svr.classification import auc
from svr.modeles import TYPE, Entrainement
from traitement import verrou
from traitement.urgences import lire_passages
from triage.modeles import ArbreClassification, fabrique
from triage.validation import rapport_classes
from triage.variables import OptionsVariables, Preparateur, construire

MODELES_PLAN = [("svm_rbf", "SVM, noyau RBF"), ("svm_laplacien", "SVM, noyau laplacien"), ("svm_lineaire", "SVM linéaire"),
                ("logistique", "Régression logistique"), ("arbre", "Arbre de décision"), ("foret", "Forêt aléatoire")]
GRILLE = (60, 45)
INSTANTS = (1, 5, 10, 20, 50, 100, 200, 400, 800, 1600)


def arrondir(t, k=4):
    return [round(float(v), k) for v in t]


def proba_affichee(nom: str, s: torch.Tensor) -> torch.Tensor:
    """Score ramené entre 0 et 1 pour la couleur : part de graves (arbre, forêt), σ(2f) sinon."""
    return s.clamp(0, 1) if nom in ("arbre", "foret") else torch.sigmoid(2 * s)


def exporter_groupe(part: pd.DataFrame, groupe: str, sortie: Path, iterations: int) -> None:
    tab = construire(part, OptionsVariables())
    ordre = torch.sort(torch.tensor(tab.dates.asi8), stable=True).indices
    n = len(ordre)
    n_app = int(0.75 * n)
    app, ev = ordre[:n_app], ordre[n_app:]
    y_app, y_ev = tab.y[app], tab.y[ev]
    prep = Preparateur(tab.continues, "mediane").ajuster(tab.X[app])
    Xa, Xe = prep.transformer(tab.X[app]), prep.transformer(tab.X[ev])
    cp, cn = rapport_classes(y_app, "equilibre", 4.0)
    e = Entrainement(iterations=iterations)
    print(f"  {n} passages : {n_app} pour apprendre, {n - n_app} pour évaluer ; {Xa.shape[1]} variables")

    # 1. Plan : ACP apprise sur l'apprentissage (centrage sur sa moyenne).
    centre = Xa.mean(dim=0)
    _, S, Vt = torch.linalg.svd(Xa - centre, full_matrices=False)
    V = Vt[:2].T
    inertie = (S ** 2 / (S ** 2).sum())[:2]
    Ua, Ue = (Xa - centre) @ V, (Xe - centre) @ V
    fortes = [[{"variable": tab.noms[j], "poids": round(float(V[j, k]), 3)} for j in torch.argsort(V[:, k].abs(), descending=True)[:5].tolist()] for k in range(2)]
    U = torch.cat([Ua, Ue])
    marge = 0.05 * (U.max(dim=0).values - U.min(dim=0).values)
    bornes = torch.stack([U.min(dim=0).values - marge, U.max(dim=0).values + marge])
    gx = torch.linspace(float(bornes[0, 0]), float(bornes[1, 0]), GRILLE[0], dtype=TYPE)
    gy = torch.linspace(float(bornes[0, 1]), float(bornes[1, 1]), GRILLE[1], dtype=TYPE)
    G = torch.cartesian_prod(gx, gy)                                    # GRILLE[0] × GRILLE[1] points, x d'abord
    blocs2 = {"constantes": [0, 1], "autres": []}

    def grille(nom, modele):
        return [arrondir(r, 3) for r in proba_affichee(nom, modele.predire(G)).reshape(GRILLE[0], GRILLE[1]).tolist()]

    # 2. Frontières dans le plan, chaque modèle appris par sa classe Python sur les deux coordonnées.
    frontieres = {}
    for nom, libelle in MODELES_PLAN:
        m = fabrique(nom, 1.0, 1.0, cp, cn, blocs2, e)()
        m.entrainer(Ua, y_app)
        s_a, s_e = m.predire(Ua), m.predire(Ue)
        seuil = float((y_app > 0).to(TYPE).mean()) if nom in ("arbre", "foret") else 0.5
        frontieres[nom] = {"libelle": libelle, "grille": grille(nom, m), "seuil": round(seuil, 4),
                           "auc_apprentissage": round(auc(s_a, y_app), 4), "auc_evaluation": round(auc(s_e, y_ev), 4),
                           "points": arrondir(proba_affichee(nom, torch.cat([s_a, s_e])), 3)}
        print(f"  plan · {libelle:24s} AUC apprentissage {frontieres[nom]['auc_apprentissage']:.3f}, évaluation {frontieres[nom]['auc_evaluation']:.3f}")

    # 3. Apprentissage du modèle principal (SVM RBF, toutes les variables) et du SVM RBF du plan.
    principal = fabrique("svm_rbf", 1.0, 1.0, cp, cn, tab.blocs, e)
    m = principal().entrainer(Xa, y_app)
    historique = m.historique
    pas = max(1, len(historique) // 300)
    suivi = []
    for t in INSTANTS:
        if t > len(historique):
            break
        mt = fabrique("svm_rbf", 1.0, 1.0, cp, cn, tab.blocs, Entrainement(iterations=t, moyenne_polyak=0.0))().entrainer(Xa, y_app)
        suivi.append({"t": t, "auc_apprentissage": round(auc(mt.predire(Xa), y_app), 4), "auc_evaluation": round(auc(mt.predire(Xe), y_ev), 4)})
    photos = []
    for t in (1, 10, 50, iterations):
        mt = fabrique("svm_rbf", 1.0, 1.0, cp, cn, blocs2, Entrainement(iterations=t, moyenne_polyak=0.0 if t < iterations else 0.5))().entrainer(Ua, y_app)
        photos.append({"t": t, "grille": grille("svm_rbf", mt)})
    print(f"  modèle principal : {len(historique)} pas ({m.arret}), AUC évaluation {auc(m.predire(Xe), y_ev):.3f}")
    # Film : le SVM RBF du plan arrêté après t pas, pour t de 1 à la fin (même départ α = 0, b = 0 : chaque
    # image est l'état réel de l'optimisation au pas t). Score de la grille, score des passages, J et AUC.
    film = []
    for t in sorted({int(round(v)) for v in torch.logspace(0, math.log10(iterations), 24, dtype=torch.float64).tolist()}):
        mt = fabrique("svm_rbf", 1.0, 1.0, cp, cn, blocs2, Entrainement(iterations=t, moyenne_polyak=0.0))().entrainer(Ua, y_app)
        s_a, s_e = mt.predire(Ua), mt.predire(Ue)
        film.append({"t": t, "J": round(float(mt.historique[-1]), 4), "grille": grille("svm_rbf", mt),
                     "points": arrondir(proba_affichee("svm_rbf", torch.cat([s_a, s_e])), 3),
                     "auc_apprentissage": round(auc(s_a, y_app), 4), "auc_evaluation": round(auc(s_e, y_ev), 4)})
    print(f"  film du SVM RBF du plan : {len(film)} images")

    # 4. Courbes de complexité (toutes les variables) et d'apprentissage.
    def point(fab, I=None):
        I = app if I is None else I
        XI, yI = prep.transformer(tab.X[I]), tab.y[I]
        mm = fab().entrainer(XI, yI)
        return round(1 - auc(mm.predire(XI), yI), 4), round(1 - auc(mm.predire(Xe), y_ev), 4)

    e_c = Entrainement(iterations=min(iterations, 1000))
    complexite = {}
    for nom, reglage, valeurs, fab in (
            ("svm_rbf", "portée du noyau (γ × nombre de variables)", (0.05, 0.1, 0.25, 0.5, 1, 2, 4, 8, 16, 32),
             lambda v: fabrique("svm_rbf", 1.0, v, cp, cn, tab.blocs, e_c)),
            ("svm_lineaire", "C (moins de régularisation à droite)", (0.001, 0.01, 0.1, 1, 10, 100),
             lambda v: fabrique("svm_lineaire", v, 1.0, cp, cn, tab.blocs, e_c)),
            ("arbre", "profondeur de l'arbre", (1, 2, 3, 4, 5, 6, 8, 10, 12),
             lambda v: (lambda: ArbreClassification(profondeur_max=v, min_feuille=5)))):
        pts = []
        for v in valeurs:
            ea, ee = point(fab(v))
            pts.append({"valeur": v, "erreur_apprentissage": ea, "erreur_evaluation": ee})
        complexite[nom] = {"reglage": reglage, "points": pts}
        meilleur = min(pts, key=lambda p: p["erreur_evaluation"])
        print(f"  complexité · {nom:13s} meilleur réglage {meilleur['valeur']} (erreur d'évaluation {meilleur['erreur_evaluation']:.3f})")
    melange = app[torch.randperm(len(app), generator=torch.Generator().manual_seed(20261103))]
    taille = []
    for f in (0.1, 0.2, 0.35, 0.5, 0.75, 1.0):
        I = melange[:max(30, int(f * len(melange)))]
        if len(torch.unique(tab.y[I])) < 2:
            continue
        ea, ee = point(fabrique("svm_rbf", 1.0, 1.0, *rapport_classes(tab.y[I], "equilibre", 4.0), tab.blocs, e_c), I)
        taille.append({"passages": len(I), "erreur_apprentissage": ea, "erreur_evaluation": ee})

    resultat = {
        "format": "apprentissage-nera/1", "genere": dt.datetime.now().isoformat(timespec="seconds"), "groupe": groupe,
        "cible": "grave (hospitalisé, référé, décédé, SCAM, MEO) contre externe",
        "passages": n, "apprentissage": n_app, "evaluation": n - n_app, "variables": Xa.shape[1],
        "plan": {"inertie": arrondir(inertie, 4), "fortes": fortes, "bornes": arrondir(bornes.flatten(), 4), "grille": list(GRILLE),
                 "points": [[round(float(u[0]), 3), round(float(u[1]), 3), int(yy > 0), int(i >= n_app)]
                            for i, (u, yy) in enumerate(zip(U, torch.cat([y_app, y_ev])))]},
        "frontieres": frontieres,
        "apprentissage_principal": {"modele": "SVM RBF, toutes les variables (portée 1, C = 1, coûts équilibrés)",
                                    "J": [round(float(v), 4) for v in historique[::pas]], "pas": pas, "arret": m.arret,
                                    "suivi": suivi, "photos": photos, "film": film},
        "complexite": complexite, "taille": taille,
    }
    chemin = sortie / f"apprentissage_{groupe}.json"
    chemin.write_text(json.dumps(resultat, ensure_ascii=False), encoding="utf-8")
    print(f"  écrit : {chemin}")


def main() -> None:
    p = argparse.ArgumentParser(description="Exporte la séparation des patients et les courbes d'apprentissage pour l'outil.")
    p.add_argument("export", help="CSV du registre des urgences exporté par l'outil de saisie")
    p.add_argument("--groupes", nargs="+", default=["enfant", "adulte"], choices=["enfant", "adulte"])
    p.add_argument("--iterations", type=int, default=2000, help="pas d'Adam du modèle principal (2000)")
    p.add_argument("--fin-developpement", help="même date que lancer_triage.py (2026-01-01 dans le mémoire) : "
                   "les passages du coffre du triage ne sont pas utilisés")
    a = p.parse_args()
    fin_dev = pd.Timestamp(a.fin_developpement) if a.fin_developpement else verrou.DATE_VERROU
    sortie = Path("resultats") / "triage"
    sortie.mkdir(parents=True, exist_ok=True)
    passages, _ = lire_passages(a.export)
    passages = passages[passages["date_passage"] < min(fin_dev, verrou.DATE_VERROU)].reset_index(drop=True)
    for g in a.groupes:
        part = passages[passages["groupe"] == g].reset_index(drop=True)
        print(f"══════ {g} : {len(part)} passages")
        if len(part) < 50:
            print("  trop peu de passages (moins de 50) : groupe ignoré")
            continue
        exporter_groupe(part, g, sortie, a.iterations)


if __name__ == "__main__":
    main()
