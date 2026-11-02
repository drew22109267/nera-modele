r"""
Prépare la source externe du transfert : lit les fichiers NHAMCS-ED (Stata) et écrit un seul tableau de
passages au format du registre des urgences (triage/nhamcs.py), avec un rapport de lecture.

Usage (WSL, depuis nera-modele/module_triage), une seule fois :
    ~/memoire-env/bin/python preparer_nhamcs.py /mnt/c/Users/User/Desktop/MEMOIRE/donnees_externes/nhamcs/dta

Écrit dans le dossier parent de dta/ (jamais sur GitHub) :
    passages_nhamcs.csv.gz       un passage par ligne (relu par lancer_triage.py, banc T9)
    lecture_nhamcs.csv           par année et par groupe : passages, constantes renseignées, classes
"""
from __future__ import annotations

import argparse
from pathlib import Path

import triage  # noqa: F401  (rend le dossier module_lit importable)
from triage.nhamcs import lire_nhamcs

CONSTANTES = ["pouls", "fr", "ta_sys", "temperature", "spo2"]


def main() -> None:
    p = argparse.ArgumentParser(description="Lit NHAMCS-ED et écrit les passages au format du registre des urgences.")
    p.add_argument("dossier", help="dossier des fichiers ED<année>-stata.dta")
    a = p.parse_args()
    dossier = Path(a.dossier)
    passages = lire_nhamcs(dossier)
    sortie = dossier.parent / "passages_nhamcs.csv.gz"
    passages.to_csv(sortie, index=False, compression="gzip")
    lignes = []
    for (annee, g), part in passages.groupby(["annee", passages["groupe"].fillna("âge inconnu")]):
        l = {"annee": annee, "groupe": g, "passages": len(part)}
        l.update({f"{c}_%": round(100 * part[c].notna().mean(), 1) for c in CONSTANTES})
        l.update({k: int((part["classe"] == k).sum()) for k in ("grave", "intermediaire", "non_grave")})
        l["sans_cible"] = int(part["classe"].isna().sum())
        lignes.append(l)
    import pandas as pd
    rapport = pd.DataFrame(lignes)
    rapport.to_csv(dossier.parent / "lecture_nhamcs.csv", index=False, encoding="utf-8")
    print(rapport.to_string(index=False))
    print(f"\n{len(passages)} passages écrits dans {sortie}")


if __name__ == "__main__":
    main()
