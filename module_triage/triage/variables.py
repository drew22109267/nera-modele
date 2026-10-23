r"""
Tableau d'apprentissage du triage : une ligne par passage, des variables connues À L'ARRIVÉE, une cible.

Cible (banc T1 pour la mise en observation)
--------------------------------------------
    y = +1  grave       (hospitalisé, référé, décédé, sortie contre avis médical)
    y = −1  non grave   (externe)
    MEO     intermédiaire, selon l'option `meo` : 'grave', 'non_grave' ou 'exclue'.
Les passages sans décision lisible n'ont pas de cible : ils sont retirés.

Groupes de variables (banc T4, options cumulables)
---------------------------------------------------
    base        âge (années), sexe féminin (0/1), constantes (forme choisie par `constantes`, banc T5)
    plaintes    une indicatrice par famille de plaintes (liste fixée à l'avance) + nombre de plaintes
    contexte    garde de nuit, permanence (week-end, férié), samedi ou dimanche, mois (sinus, cosinus)
    manquants   une indicatrice « constante non prise » par constante : ne pas prendre une constante est
                aussi une information (un patient très bien portant… ou une urgence vitale)
Le diagnostic n'est JAMAIS une variable : il est écrit après l'examen (fuite de l'avenir).

Valeurs manquantes et standardisation : `Preparateur`, appris sur l'entraînement SEULEMENT
-----------------------------------------------------------------------------------------
    1. chaque valeur manquante est remplacée par la MÉDIANE de sa colonne sur l'entraînement ;
    2. les colonnes continues sont standardisées : z = (x − μ)/σ, μ et σ de l'entraînement.
Les deux étapes sont apprises sur les passages d'entraînement et appliquées telles quelles aux passages à
prévoir : aucune information des passages à prévoir n'entre dans la préparation.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import pandas as pd
import torch

from svr.modeles import TYPE

from .normes import CONSTANTES_NORMEES, AGE_NOURRISSON, alertes, ecarts, plage

CONSTANTES = ["pouls", "fr", "ta_sys", "ta_dia", "temperature", "spo2", "glycemie", "poids"]
FORMES = ("brutes", "ecart", "seuils")
MEO = ("grave", "non_grave", "exclue")


@dataclass
class OptionsVariables:
    constantes: str = "ecart"        # 'brutes', 'ecart' ou 'seuils' (banc T5)
    plaintes: bool = True            # banc T4
    contexte: bool = True
    manquants: bool = True
    meo: str = "grave"               # banc T1


@dataclass
class TableauTriage:
    X: torch.Tensor                  # n × d, NaN = valeur manquante (remplacée par Preparateur)
    y: torch.Tensor                  # +1 grave, −1 non grave
    dates: pd.DatetimeIndex          # date de passage de chaque ligne
    noms: list[str]
    continues: list[int]             # colonnes à standardiser
    blocs: dict[str, list[int]]      # 'constantes' (âge et constantes) et 'autres' (pour le noyau composite)
    alertes: torch.Tensor            # nombre de signes d'alerte de chaque passage (règle de référence)
    meo: torch.Tensor                # 1 si la décision était une mise en observation
    groupe: list[str]


def cible(classe: str | None, meo: str) -> float | None:
    if classe == "grave":
        return 1.0
    if classe == "non_grave":
        return -1.0
    if classe == "intermediaire":
        return {"grave": 1.0, "non_grave": -1.0, "exclue": None}[meo]
    return None


def construire(passages: pd.DataFrame, options: OptionsVariables | None = None) -> TableauTriage:
    o = options or OptionsVariables()
    if o.constantes not in FORMES or o.meo not in MEO:
        raise ValueError(f"Options invalides : constantes ∈ {FORMES}, meo ∈ {MEO}.")
    noms, continues = ["age", "sexe_f"], [0]
    if o.constantes == "brutes":
        noms += CONSTANTES
        continues += list(range(2, 2 + len(CONSTANTES)))
    else:
        suffixes = ("haut", "bas")
        noms += [f"{c}_{s}" for c in CONSTANTES_NORMEES for s in suffixes]
        if o.constantes == "ecart":
            continues += list(range(2, len(noms)))
        noms.append("poids")                             # le poids n'a pas de plage normale : gardé brut
        continues.append(len(noms) - 1)
    fin_constantes = len(noms)
    if o.manquants:
        noms += [f"manque_{c}" for c in CONSTANTES]
    if o.plaintes:
        colonnes_plaintes = [c for c in passages.columns if c.startswith("plainte_")]
        noms += colonnes_plaintes + ["nombre_plaintes"]
        continues.append(len(noms) - 1)
    if o.contexte:
        noms += ["garde_nuit", "permanence", "week_end", "mois_sin", "mois_cos"]
        continues += [len(noms) - 2, len(noms) - 1]

    lignes, ys, dates, nb_alertes, meo, groupes = [], [], [], [], [], []
    for _, p in passages.iterrows():
        yc = cible(p.get("classe"), o.meo)
        if yc is None:
            continue
        age = _val(p.get("age"))
        adulte = p.get("groupe") == "adulte"
        age_norme = AGE_NOURRISSON if math.isnan(age) and p.get("nourrisson") else age
        v = [age, 1.0 if p.get("sexe") == "F" else 0.0 if p.get("sexe") == "M" else math.nan]
        total_alertes = 0.0
        for c in CONSTANTES_NORMEES:
            x = _val(p.get(c))
            pl = plage(c, None if math.isnan(age_norme) else age_norme, adulte)
            bas, haut = pl if pl is not None else (None, None)
            a = alertes(x, bas, haut) if pl is not None else (math.nan, math.nan)
            total_alertes += sum(0.0 if math.isnan(z) else z for z in a)
            if o.constantes == "ecart":
                v += list(ecarts(x, bas, haut)) if pl is not None else [math.nan, math.nan]
            elif o.constantes == "seuils":
                v += list(a)
        if o.constantes == "brutes":
            v += [_val(p.get(c)) for c in CONSTANTES]
        else:
            v.append(_val(p.get("poids")))
        if o.manquants:
            v += [1.0 if math.isnan(_val(p.get(c))) else 0.0 for c in CONSTANTES]
        if o.plaintes:
            v += [float(p.get(c) or 0) for c in colonnes_plaintes] + [float(p.get("nombre_plaintes") or 0)]
        if o.contexte:
            d = pd.Timestamp(p["date_passage"])
            angle = 2 * math.pi * (d.month - 1) / 12
            v += [float(p.get("moment") == "garde"), float(p.get("moment") == "permanence"),
                  float(d.dayofweek >= 5), math.sin(angle), math.cos(angle)]
        lignes.append(v)
        ys.append(yc)
        dates.append(pd.Timestamp(p["date_passage"]))
        nb_alertes.append(total_alertes)
        meo.append(float(p.get("classe") == "intermediaire"))
        groupes.append(p.get("groupe"))
    if not lignes:
        raise ValueError("Aucun passage avec une décision lisible.")
    return TableauTriage(X=torch.tensor(lignes, dtype=TYPE), y=torch.tensor(ys, dtype=TYPE),
                         dates=pd.DatetimeIndex(dates), noms=noms, continues=continues,
                         blocs={"constantes": list(range(fin_constantes)),
                                "autres": list(range(fin_constantes, len(noms)))},
                         alertes=torch.tensor(nb_alertes, dtype=TYPE), meo=torch.tensor(meo, dtype=TYPE),
                         groupe=groupes)


def _val(v) -> float:
    try:
        f = float(v)
    except (TypeError, ValueError):
        return math.nan
    return f


class Preparateur:
    """Imputation par la médiane puis standardisation, apprises sur l'entraînement seulement."""

    def __init__(self, continues: list[int]):
        self.continues = continues

    def ajuster(self, X: torch.Tensor) -> "Preparateur":
        self.mediane = torch.nanmedian(X, dim=0).values
        self.mediane = torch.where(torch.isnan(self.mediane), torch.zeros_like(self.mediane), self.mediane)
        Z = self._imputer(X)[:, self.continues]
        self.moyenne = Z.mean(dim=0)
        self.ecart = Z.std(dim=0, unbiased=False)
        self.ecart[self.ecart < 1e-12] = 1.0             # colonne constante : on ne divise pas par 0
        return self

    def _imputer(self, X: torch.Tensor) -> torch.Tensor:
        return torch.where(torch.isnan(X), self.mediane.expand_as(X), X)

    def transformer(self, X: torch.Tensor) -> torch.Tensor:
        Z = self._imputer(X)
        Z[:, self.continues] = (Z[:, self.continues] - self.moyenne) / self.ecart
        return Z
