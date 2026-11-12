r"""
SÉLECTION : le SVM et le traitement des durées inconnues retenus pour un service, d'après les bancs.

Règle (écrite à l'avance, appliquée telle quelle) :
  1. Modèle : parmi les SVM du banc D13 (svr/variantes.py), celui dont la perte pinball au quantile décisionnel
     τ est la plus petite, en moyenne sur les horizons évalués (J+1, J+7). La perte pinball est le critère du
     problème : elle mesure le coût asymétrique d'une pénurie de lits et d'un lit vide. Les concurrents (forêt,
     boosting, réseaux) et les références du banc D1 sont classés à côté pour situer le SVM, mais la sélection
     porte sur la famille SVM, objet du mémoire.
  2. Durées inconnues : pour CE modèle, la méthode dont la perte pinball τ contre la série retenue est la plus petite dans le
     banc croisé P1 × modèles (moyenne sur les horizons) ; à défaut de banc croisé, la méthode retenue (« estimee »).
  3. Avec --regle significatif (défaut), un modèle ou une méthode ne remplace le choix retenu que si le test de
     Diebold-Mariano (perte pinball τ, correction de Holm) le dit « meilleur » sur au moins un horizon et
     « moins bon » sur aucun ; sinon le choix retenu, fixé
     avant les bancs, est gardé. Prendre la plus petite erreur parmi une vingtaine de variantes favoriserait celle
     qui a eu de la chance sur ces jours (biais du gagnant) ; --regle meilleur reste disponible, la
     significativité étant alors seulement indiquée.
Toutes ces mesures viennent de la validation glissante AVANT le verrou : la sélection ne voit jamais le coffre.
validation_finale.py relit selection_<SERVICE>.json et évalue le modèle choisi sur le coffre, une seule fois.

Usage (après lancer_tout.sh) :
    ~/memoire-env/bin/python selection.py --service PED
Sorties : resultats/selection_<SERVICE>.json (relu par validation_finale.py), selection_<SERVICE>.csv (classement,
exporté vers l'outil de saisie), selection_<SERVICE>.md.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd

from benchmark_choix import en_markdown
from svr.variantes import CATALOGUE, RETENU
from traitement.comptage import etiquette, option_comptage

NOM_VERS_CLE = {v[0]: k for k, v in CATALOGUE.items()}


def lire(chemin: Path) -> pd.DataFrame:
    t = pd.read_csv(chemin, sep=";", encoding="utf-8-sig")
    t = t.rename(columns={t.columns[0]: "variante"})
    t["variante"] = t["variante"].astype(str).str.replace(" (retenu)", "", regex=False)
    return t


def colonne_pinball(t: pd.DataFrame) -> str:
    return next(c for c in t.columns if c.startswith("pinball"))


def main() -> None:
    p = argparse.ArgumentParser(description="Choisit le SVM et le traitement des durées inconnues d'après les bancs.")
    p.add_argument("--service", required=True)
    p.add_argument("--regle", choices=["meilleur", "significatif"], default="significatif")
    p.add_argument("--dossier", default="resultats")
    option_comptage(p)
    a = p.parse_args()
    lab = etiquette(a.service, a.comptage)
    d = Path(a.dossier)

    # 1. Modèle : banc D13 (famille SVM), moyenne sur les horizons.
    tables = sorted(d.glob(f"benchmark_{lab}_D13_h*.csv"))
    if not tables:
        raise SystemExit(f"Banc D13 absent pour {lab} : lancez d'abord benchmark_choix.py (étape 3 de lancer_tout.sh).")
    lignes = []
    for f in tables:
        h = int(re.search(r"_h(\d+)\.csv$", f.name).group(1))
        t = lire(f)
        pc = colonne_pinball(t)
        for _, r in t.iterrows():
            lignes.append({"modèle": r["variante"], "horizon": h, "pinball": r[pc], "MAE": r.get("MAE"),
                           "vs retenu": r.get("vs choix retenu"), "famille": "svm"})
    for f in sorted(d.glob(f"benchmark_{lab}_D1_h*.csv")):        # pour situer : concurrents et références
        h = int(re.search(r"_h(\d+)\.csv$", f.name).group(1))
        t = lire(f)
        pc = colonne_pinball(t)
        for _, r in t.iterrows():
            cle = NOM_VERS_CLE.get(r["variante"])
            if cle is None or CATALOGUE[cle][1] != "svm":
                lignes.append({"modèle": r["variante"], "horizon": h, "pinball": r[pc], "MAE": r.get("MAE"),
                               "vs retenu": r.get("vs choix retenu"), "famille": "autre (D1)"})
    tout = pd.DataFrame(lignes)
    classement = (tout.groupby(["famille", "modèle"]).agg(pinball_moyen=("pinball", "mean"), MAE_moyenne=("MAE", "mean"),
                                                          horizons=("horizon", "nunique"),
                                                          significatif=("vs retenu", lambda s: ", ".join(sorted(set(map(str, s))))))
                  .reset_index().sort_values("pinball_moyen"))
    svm = classement[classement["famille"] == "svm"]
    nom_retenu = CATALOGUE[RETENU][0]
    choisi = svm.iloc[0]
    gagne = lambda verdicts: "meilleur" in verdicts and "moins bon" not in verdicts   # sur les horizons réunis
    if a.regle == "significatif" and not gagne(choisi["significatif"]):
        choisi = svm[svm["modèle"] == nom_retenu].iloc[0]
    cle = NOM_VERS_CLE.get(choisi["modèle"], RETENU)

    # 2. Durées inconnues pour ce modèle : banc croisé P1 × modèles (série « minuit », le prétraitement est commun).
    imputation, detail_imp = "estimee", "banc croisé absent : méthode retenue"
    croises = sorted(d.glob(f"pretraitement_{a.service}_P1xM_h*.csv"))
    if croises:
        c = pd.concat([pd.read_csv(f, sep=";", encoding="utf-8-sig") for f in croises])
        c = c[c["cle_modele"] == cle]
        if len(c):
            critere = next((k for k in c.columns if k.startswith("pinball τ=") and k.endswith("retenue")), "MAE retenue")
            moy = c.groupby("cle_imputation").agg(MAE=(critere, "mean"),
                                                   verdict=("vs imputation retenue, même modèle", lambda s: ", ".join(sorted(set(map(str, s))))))
            meilleur = moy["MAE"].idxmin()
            if a.regle == "meilleur" or gagne(moy.loc[meilleur, "verdict"]):
                imputation = meilleur
            detail_imp = f"MAE moyenne {moy.loc[meilleur, 'MAE']:.3f} ; contre « estimee » pour ce modèle : {moy.loc[meilleur, 'verdict']}"

    selection = {"service": a.service, "comptage": a.comptage, "regle": a.regle, "modele": cle, "nom_modele": choisi["modèle"],
                 "pinball_moyen": float(choisi["pinball_moyen"]), "significatif_vs_retenu": choisi["significatif"],
                 "imputation": imputation, "detail_imputation": detail_imp,
                 "meilleur_toutes_familles": classement.iloc[0]["modèle"]}
    (d / f"selection_{lab}.json").write_text(json.dumps(selection, ensure_ascii=False, indent=1), encoding="utf-8")
    classement.to_csv(d / f"selection_{lab}.csv", sep=";", encoding="utf-8-sig", index=False)
    texte = [f"# Sélection — {lab}\n", f"Règle : {a.regle}. Critère : perte pinball au quantile décisionnel, moyenne sur les horizons.\n",
             f"**SVM retenu : {choisi['modèle']}** (pinball moyen {choisi['pinball_moyen']:.4f} ; contre le choix d'origine : {choisi['significatif']}).\n",
             f"**Durées inconnues : {imputation}** ({detail_imp}).\n",
             f"Meilleur modèle toutes familles confondues : {classement.iloc[0]['modèle']}.\n", en_markdown(classement.round(4))]
    (d / f"selection_{lab}.md").write_text("\n".join(texte), encoding="utf-8")
    print("\n".join(texte))


if __name__ == "__main__":
    main()
