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
    mots        sac de mots (banc T11) : une indicatrice par MOT des plaintes, pour chaque mot du vocabulaire.
                Le vocabulaire = les mots écrits dans au moins 5 passages AVANT le verrou (vocabulaire()) : il est
                tiré du texte seul, jamais de la décision, et ne regarde pas la période de test. Il reconnaît ce
                que les familles ratent (mots rares, fautes, anglais) ; le SVM pèse chaque mot (régularisation).
    contexte    garde de nuit, permanence (week-end, férié), samedi ou dimanche, mois (sinus, cosinus)
    manquants   une indicatrice « constante non prise » par constante : ne pas prendre une constante est
                aussi une information (un patient très bien portant… ou une urgence vitale)
Le diagnostic n'est JAMAIS une variable : il est écrit après l'examen (fuite de l'avenir).

Valeurs manquantes et standardisation : `Preparateur`, appris sur l'entraînement SEULEMENT
-----------------------------------------------------------------------------------------
    1. chaque valeur manquante est complétée selon le traitement choisi (médiane par défaut ; les neuf
       traitements comparés par le banc T8 sont dans triage/imputation.py) ;
    2. les colonnes continues sont mises à l'échelle, par défaut z = (x − μ)/σ, μ et σ de l'entraînement
       (le banc T14 compare z-score, robuste (médiane, Q3 − Q1), min-max et aucune mise à l'échelle).
Les deux étapes sont apprises sur les passages d'entraînement et appliquées telles quelles aux passages à
prévoir : aucune information des passages à prévoir n'entre dans la préparation.
"""
from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass

import pandas as pd
import torch

from svr.caracteristiques import Standardiseur
from svr.modeles import TYPE
from traitement.urgences import mots as mots_de

from .imputation import Imputeur
from .normes import CONSTANTES_NORMEES, AGE_NOURRISSON, alertes, ecarts, plage

CONSTANTES = ["pouls", "fr", "ta_sys", "ta_dia", "temperature", "spo2", "glycemie", "poids"]
FORMES = ("brutes", "ecart", "seuils")
MEO = ("grave", "non_grave", "exclue")


@dataclass
class OptionsVariables:
    constantes: str = "ecart"        # 'brutes', 'ecart' ou 'seuils' (banc T5)
    plaintes: bool = True            # banc T4
    mots: tuple[str, ...] = ()       # vocabulaire du sac de mots (banc T11) ; vide = pas de mots
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
    ids: list = None                 # identifiant du passage (colonne id_passage), pour raccorder enfants et adultes


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
    if o.mots:
        noms += [f"mot_{m}" for m in o.mots]
    if o.contexte:
        noms += ["garde_nuit", "permanence", "week_end", "mois_sin", "mois_cos"]
        continues += [len(noms) - 2, len(noms) - 1]

    lignes, ys, dates, nb_alertes, meo, groupes, ids = [], [], [], [], [], [], []
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
        if o.mots:
            if "plaintes_texte" in passages:
                texte = p.get("plaintes_texte")
                ecrits = mots_de(texte if isinstance(texte, str) else "")
                v += [float(m in ecrits) for m in o.mots]
            else:                                         # source sans texte (NHAMCS) : mots non observés
                v += [math.nan] * len(o.mots)
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
        ids.append(p.get("id_passage"))
    if not lignes:
        raise ValueError("Aucun passage avec une décision lisible.")
    return TableauTriage(X=torch.tensor(lignes, dtype=TYPE), y=torch.tensor(ys, dtype=TYPE),
                         dates=pd.DatetimeIndex(dates), noms=noms, continues=continues,
                         blocs={"constantes": list(range(fin_constantes)),
                                "autres": list(range(fin_constantes, len(noms)))},
                         alertes=torch.tensor(nb_alertes, dtype=TYPE), meo=torch.tensor(meo, dtype=TYPE),
                         groupe=groupes, ids=ids)


def vocabulaire(passages: pd.DataFrame, avant: pd.Timestamp, min_passages: int = 5) -> tuple[str, ...]:
    """Mots des plaintes écrits dans au moins `min_passages` passages datés avant `avant` (texte seul)."""
    if "plaintes_texte" not in passages:
        return ()
    textes = passages.loc[passages["date_passage"] < avant, "plaintes_texte"].dropna()
    compte = Counter(m for t in textes for m in mots_de(t))
    return tuple(sorted(m for m, n in compte.items() if n >= min_passages))


def _val(v) -> float:
    try:
        f = float(v)
    except (TypeError, ValueError):
        return math.nan
    return f


ECHELLES = ("zscore", "robuste", "minmax", "aucune")     # banc T14

class Preparateur:
    """Imputation (banc T8, médiane par défaut) puis standardisation, apprises sur l'entraînement seulement."""

    def __init__(self, continues: list[int], imputation: str = "mediane", echelle: str = "zscore"):
        if echelle not in ECHELLES:
            raise ValueError(f"Mise à l'échelle inconnue : {echelle}. Choix : {', '.join(ECHELLES)}.")
        self.continues, self.echelle = continues, echelle
        self.imputeur = Imputeur(imputation, continues)

    def ajuster(self, X: torch.Tensor) -> "Preparateur":
        self.imputeur.ajuster(X)
        Z = self._imputer(X)[:, self.continues]
        if self.echelle == "aucune":
            self.moyenne, self.ecart = torch.zeros(Z.shape[1], dtype=Z.dtype), torch.ones(Z.shape[1], dtype=Z.dtype)
        else:                                            # même calcul que le module lit (constante : écart 1)
            s = Standardiseur(list(range(Z.shape[1])), self.echelle).ajuster(Z)
            self.moyenne, self.ecart = s.moyenne, s.ecart
        return self

    def _imputer(self, X: torch.Tensor) -> torch.Tensor:
        return self.imputeur.transformer(X)

    def transformer(self, X: torch.Tensor) -> torch.Tensor:
        Z = self._imputer(X)
        Z[:, self.continues] = (Z[:, self.continues] - self.moyenne) / self.ecart
        Z[:, self.imputeur.retirees] = 0.0          # suppression_colonnes : colonne constante = colonne retirée
        return Z
