r"""
Résultats des bancs d'essai → un seul fichier JSON, à importer dans l'outil de saisie (Indicateurs → « Résultats du modèle »).

Rassemble les tableaux écrits dans resultats/ par la chaîne (lancer_tout.sh) :

  pretraitement_<S>_<P>_h<h>.csv   banc du prétraitement P1 à P8
  benchmark_<S>_<D>_h<h>.csv       banc des choix de conception D1 à D11
  ablation_<S>_h<h>.csv            niveaux 0 à 5 (ce que chaque bloc de variables apporte)
  parametres_<S>_synthese.csv      sensibilité de chaque hyperparamètre
  sensibilite_<S>_synthese.csv     sensibilité à la convention des jours
  survie_<S>.csv                   modèle de survie J0 / J1 / J2

et, pour chaque tableau, la phrase de conclusion écrite par le banc dans son rapport markdown (« Aucune variante ne
fait significativement mieux que le choix retenu… » ou « … à revoir »). L'outil s'en sert pour dire, sous chaque
analyse, si le banc a CONFIRMÉ le choix ou s'il est À REVOIR.

Les bancs qui dépendent de la série (niveaux, choix, sensibilité) existent pour chaque méthode de comptage
(minuit, journee, pondere, pic : fichiers <SERVICE>, <SERVICE>_journee…) ; chaque tableau garde sa méthode.

Aucune donnée de patient n'est copiée : seulement des erreurs de prévision, des tests et des réglages.

Exemple :
    ~/memoire-env/bin/python exporter_resultats.py --service PED
Sortie : resultats/resultats_nera_<SERVICE>.json
"""
from __future__ import annotations

import argparse
import json
import math
import re
from datetime import datetime
from pathlib import Path

import pandas as pd

from traitement.comptage import COMPTAGES, etiquette

# (motif du fichier, groupe, titre du groupe) ; {s} = service. Le code (P1, D4…) et l'horizon sont lus dans le nom.
FICHIERS = [
    (r"pretraitement_{s}_(P\d+)_h(\d+)\.csv", "pretraitement", "Banc du prétraitement"),
    (r"benchmark_{s}_(D\d+)_h(\d+)\.csv", "choix", "Banc des choix de conception"),
    (r"ablation_{s}_h(\d+)\.csv", "niveaux", "Niveaux 0 à 5 (ablation)"),
    (r"ablation_{s}_tests\.csv", "niveaux_tests", "Niveaux : tests entre niveaux"),
    (r"parametres_{s}_synthese\.csv", "parametres", "Sensibilité des hyperparamètres"),
    (r"sensibilite_{s}_synthese\.csv", "sensibilite", "Sensibilité à la convention des jours"),
    (r"survie_{s}\.csv", "survie", "Modèle de survie (J0, J1, J2)"),
]
RAPPORTS = {"pretraitement": "pretraitement_{s}.md", "choix": "benchmark_{s}.md"}


def valeur(v):
    """Cellule → valeur JSON (NaN → null, nombres numpy → float/int)."""
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return None
    if hasattr(v, "item"):
        v = v.item()
        if isinstance(v, float) and math.isnan(v):
            return None
    return v


def conclusions_markdown(chemin: Path) -> dict[tuple[str, int], dict]:
    """(code, horizon) → {titre, conclusion} : la phrase écrite après chaque tableau du rapport du banc."""
    if not chemin.exists():
        return {}
    res, h, code, titre, texte = {}, None, None, None, []

    def fermer():
        if code is not None and h is not None:
            phrase = " ".join(l.strip() for l in texte if l.strip() and not l.lstrip().startswith("|")
                              and not l.strip().startswith("*") and "jours évalués" not in l)
            res[(code, h)] = {"titre": titre, "conclusion": phrase.replace("**", "").replace("⚠ ", "")}

    for ligne in chemin.read_text(encoding="utf-8").splitlines():
        m_h = re.match(r"^## Horizon J\+(\d+)", ligne)
        m_d = re.match(r"^### (\w+) · (.+)$", ligne)
        if m_h or m_d:
            fermer(); texte = []
            if m_h:
                h, code, titre = int(m_h.group(1)), None, None
            else:
                code, titre = m_d.group(1), m_d.group(2).strip()
        else:
            texte.append(ligne)
    fermer()
    return res


def verdict(colonnes: list[str], lignes: list[list], conclusion: str | None) -> str | None:
    """« confirme » si aucune variante ne bat le choix retenu, « a_revoir » sinon ; None si le tableau n'en dit rien."""
    if "vs choix retenu" in colonnes:
        j = colonnes.index("vs choix retenu")
        return "a_revoir" if any(l[j] == "meilleur" for l in lignes) else "confirme"
    if conclusion:
        return "a_revoir" if "à revoir" in conclusion else "confirme" if "Aucune variante" in conclusion else None
    return None


def tables_du_comptage(dossier: Path, service: str, comptage: str) -> list[dict]:
    """Tableaux d'une méthode de comptage ; prétraitement et survie : une seule fois, avec la série retenue (minuit)."""
    lab = etiquette(service, comptage)
    phrases = {g: conclusions_markdown(dossier / m.format(s=lab)) for g, m in RAPPORTS.items()}
    tables = []
    for motif, groupe, titre_groupe in FICHIERS:
        unique = groupe in ("pretraitement", "survie")
        if unique and comptage != "minuit":
            continue
        rx = re.compile(motif.format(s=re.escape(lab)) + "$")
        for f in sorted(dossier.glob("*.csv")):
            m = rx.match(f.name)
            if not m:
                continue
            g = m.groups()
            code = g[0] if g and not g[0].isdigit() else None
            horizon = int(g[-1]) if g and g[-1].isdigit() else None
            t = pd.read_csv(f, sep=";", encoding="utf-8-sig")
            colonnes = [str(c) for c in t.columns]
            if colonnes and colonnes[0].startswith("Unnamed"):
                colonnes[0] = "variante"
            lignes = [[valeur(v) for v in r] for r in t.itertuples(index=False)]
            info = phrases.get(groupe, {}).get((code, horizon), {})
            tables.append({"fichier": f.name, "groupe": groupe, "titre_groupe": titre_groupe, "code": code, "horizon": horizon,
                           "comptage": None if unique else comptage,
                           "titre": info.get("titre"), "conclusion": info.get("conclusion"),
                           "verdict": verdict(colonnes, lignes, info.get("conclusion")),
                           "modifie": datetime.fromtimestamp(f.stat().st_mtime).isoformat(timespec="minutes"),
                           "colonnes": colonnes, "lignes": lignes})
    return tables


def main() -> None:
    p = argparse.ArgumentParser(description="Rassemble les résultats des bancs en un JSON pour l'outil de saisie.")
    p.add_argument("--service", required=True)
    p.add_argument("--dossier", default="resultats")
    a = p.parse_args()
    dossier = Path(a.dossier)
    tables = [t for c in COMPTAGES for t in tables_du_comptage(dossier, a.service, c)]
    if not tables:
        raise SystemExit(f"Aucun résultat pour le service {a.service} dans {dossier.resolve()} : lancer d'abord lancer_tout.sh.")
    sortie = dossier / f"resultats_nera_{a.service}.json"
    sortie.write_text(json.dumps({"format": "resultats-nera/1", "service": a.service,
                                  "genere": datetime.now().isoformat(timespec="minutes"), "tables": tables},
                                 ensure_ascii=False, indent=1), encoding="utf-8")
    par = {}
    for t in tables:
        par[t["groupe"]] = par.get(t["groupe"], 0) + 1
    print(f"{len(tables)} tableaux ({', '.join(f'{g} : {n}' for g, n in par.items())}) → {sortie.resolve()}")


if __name__ == "__main__":
    main()
