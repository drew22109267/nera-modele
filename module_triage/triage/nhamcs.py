r"""
Source externe du transfert : NHAMCS-ED (National Hospital Ambulatory Medical Care Survey, urgences ;
CDC/NCHS, États-Unis, données publiques), une ligne par passage, environ 19 500 passages par an.

Fichiers : ftp.cdc.gov/pub/Health_Statistics/NCHS/dataset_documentation/NHAMCS/stata/ED<année>-stata.zip
(téléchargés dans MEMOIRE/donnees_externes/nhamcs, jamais sur GitHub). Lus par pandas.read_stata.

Mise en correspondance avec le registre des urgences (traitement/urgences.py, même tableau de passages)
-------------------------------------------------------------------------------------------------------
  âge            AGE (années) ; avant 1 an, AGEDAYS/365,25 quand il est donné
  sexe           SEX : 1 = F, 2 = M
  température    TEMPF, en dixièmes de degré Fahrenheit → °C = (TEMPF/10 − 32) × 5/9
  pouls          PULSE (998 = « Doppler » : pas de valeur)
  FR, TA, SpO2   RESPR, BPSYS/BPDIAS, POPCT
  glycémie, poids  absents de NHAMCS : toujours manquants (le transfert travaille sur les variables COMMUNES)
  plaintes       RFV1 à RFV5 (classification des motifs de consultation du NCHS), libellé anglais → les
                 28 familles du registre (PLAINTES_RFV ci-dessous, liste fixée à l'avance) ; le traumatisme
                 regroupe le module « blessures » (codes 50000 à 59999) hors brûlures et conscience
  moment         ARRTIME (heure d'arrivée) : garde de 18 h à 8 h ; permanence le samedi et le dimanche de jour ;
                 sinon jour — comme le registre (jour, garde de nuit, permanence)
  date           l'année, le mois (VMONTH) et le jour de la semaine (VDAYR) sont connus, pas le jour exact :
                 premier jour du mois qui tombe ce jour de la semaine (suffit pour le mois et le week-end)
  cible          la même règle que la colonne « Décision » du registre :
                   hospitalisé (ADMITHOS), hospitalisé après observation (OBSHOS), transféré vers un autre
                   hôpital (TRANOTH, TRANPSYC : le « référé »), décédé (DIEDED, DOA),
                   parti contre avis médical (LEFTAMA : la SCAM)                → grave
                   observation puis retour à domicile (OBSDIS : la MEO)         → intermédiaire (banc T1)
                   rentré à domicile                                             → non grave
                   parti sans être vu (LWBS, LBTC), devenir inconnu (NODISP)     → sans cible
Les valeurs codées « vide » ou « inconnu » (−9, −8, −7) deviennent manquantes ; les constantes hors des
plages plausibles du registre (traitement.urgences.PLAUSIBLE) aussi.
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

from traitement.urgences import AGE_ADULTE, PLAINTES, PLAUSIBLE

PLAINTES_RFV = {
    "fievre": r"^fever$",
    "toux": r"^cough",
    "vomissements": r"vomit",
    "diarrhee": r"diarrh",
    "convulsions": r"convuls|seizure",
    "douleur_abdominale": r"abdominal pain|stomach and abdominal pain",
    "cephalees": r"headache",
    "dyspnee": r"shortness of breath|dyspnea|wheez|breathing",
    "paleur": r"pallor|anemia",
    "conscience": r"syncope|consciousness|unconscious|letharg|confus|disorient",
    "brulure": r"^burn",
    "saignement": r"bleed|hemorr|hematemesis|epistaxis|blood in",
    "douleur_thoracique": r"chest pain",
    "oedemes": r"edema|swelling",
    "ictere": r"jaundice",
    "refus_alimentation": r"feeding problem|decreased appetite",
    "deshydratation": r"dehydrat|thirst",
    "asthenie": r"weakness|tired|fatigue|malaise",
    "vertiges": r"vertigo|dizz",
    "frissons": r"chills",
    "deficit_neurologique": r"paralysis|numbness|tingling|stroke|speech",
    "metabolique": r"diabet|blood sugar|glucose|frequent urination",
    "douleur_pelvienne": r"pelvic",
    "douleur_osteo_articulaire": r"\bback\b|joint|knee|neck pain|muscle|\bhip|shoulder|leg pain|arm pain|body ache",
    "orl": r"nasal|\bnose|throat|\bear\b|earache|sinus|head cold",
    "palpitations": r"palpitation|heart pounding|racing",
    "cutane": r"rash|itch|\bskin",
}
GRAVE = ("ADMITHOS", "OBSHOS", "TRANOTH", "TRANPSYC", "DIEDED", "DOA", "LEFTAMA")
SANS_CIBLE = ("LWBS", "LBTC", "NODISP")
COLONNES = ["AGE", "AGEDAYS", "SEX", "TEMPF", "PULSE", "RESPR", "BPSYS", "BPDIAS", "POPCT", "RFV1", "RFV2", "RFV3",
            "RFV4", "RFV5", "ARRTIME", "VMONTH", "VDAYR", "OBSDIS", *GRAVE, *SANS_CIBLE]


def familles_rfv(libelles: dict) -> dict[int, set[str]]:
    """Code RFV → familles de plaintes, d'après le libellé anglais du code (table du fichier Stata)."""
    assert set(PLAINTES_RFV) | {"traumatisme"} == set(PLAINTES), "les familles doivent être celles du registre"
    table = {}
    for code, texte in libelles.items():
        t, c, fam = str(texte).strip().lower(), int(code), set()
        for f, motif in PLAINTES_RFV.items():
            if re.search(motif, t):
                fam.add(f)
        if 50000 <= c < 60000 and not fam & {"brulure", "conscience"}:
            fam.add("traumatisme")
        if fam:
            table[c] = fam
    return table


def _num(s: pd.Series) -> pd.Series:
    v = pd.to_numeric(s, errors="coerce").astype(float)
    return v.where(v >= 0)                                 # −9 vide, −8 inconnu, −7 sans objet


def _plausible(v: pd.Series, nom: str) -> pd.Series:
    bas, haut = PLAUSIBLE[nom]
    return v.where((v >= bas) & (v <= haut))


def lire_annee(fichier: Path) -> pd.DataFrame:
    lecteur = pd.read_stata(fichier, iterator=True)
    etiquettes = lecteur.value_labels()
    colonnes = {c.upper(): c for c in lecteur.variable_labels()}
    nom_rfv = next((n for n in etiquettes if n.upper().startswith("RFV") and len(etiquettes[n]) > 300), None)
    if nom_rfv is None:
        raise ValueError(f"{fichier.name} : table des motifs de consultation (RFV) introuvable.")
    familles = familles_rfv(etiquettes[nom_rfv])
    r = pd.read_stata(fichier, columns=[colonnes[c] for c in COLONNES if c in colonnes], convert_categoricals=False)
    r.columns = [c.upper() for c in r.columns]
    annee = int(re.search(r"(20\d\d)", fichier.name).group(1))

    p = pd.DataFrame(index=r.index)
    age = _num(r["AGE"])
    if "AGEDAYS" in r:
        jours = _num(r["AGEDAYS"])
        age = age.where(~((age == 0) & jours.notna()), jours / 365.25)
    p["age"] = age
    p["nourrisson"] = (age < 1).astype(int)
    p["sexe"] = r["SEX"].map({1: "F", 2: "M"})
    tf = _num(r["TEMPF"])
    p["temperature"] = _plausible(((tf / 10) - 32) * 5 / 9, "temperature")
    p["pouls"] = _plausible(_num(r["PULSE"]).where(r["PULSE"] != 998), "pouls")
    p["fr"] = _plausible(_num(r["RESPR"]), "fr")
    sys_, dia = _plausible(_num(r["BPSYS"]), "ta_sys"), _plausible(_num(r["BPDIAS"]), "ta_dia")
    ok = sys_.notna() & dia.notna() & (sys_ > dia)
    p["ta_sys"], p["ta_dia"] = sys_.where(ok), dia.where(ok)
    p["spo2"] = _plausible(_num(r["POPCT"]), "spo2")
    p["glycemie"] = np.nan
    p["poids"] = np.nan

    codes = r[[c for c in ("RFV1", "RFV2", "RFV3", "RFV4", "RFV5") if c in r]].apply(pd.to_numeric, errors="coerce")
    for f in PLAINTES:
        de_la_famille = [c for c, fam in familles.items() if f in fam]
        p[f"plainte_{f}"] = codes.isin(de_la_famille).any(axis=1).astype(int)
    p["nombre_plaintes"] = (codes > 0).sum(axis=1)

    heure = pd.to_numeric(r["ARRTIME"], errors="coerce") // 100
    week_end = r["VDAYR"].isin([1, 7])                    # 1 = dimanche, 7 = samedi
    nuit = (heure >= 18) | (heure < 8)
    p["moment"] = np.where(nuit, "garde", np.where(week_end, "permanence", "jour"))
    p.loc[heure.isna(), "moment"] = None
    premier = pd.to_datetime(dict(year=annee, month=r["VMONTH"].clip(1, 12), day=1))
    decalage = ((r["VDAYR"] - 1) - ((premier.dt.dayofweek + 1) % 7)) % 7     # VDAYR : 1 = dimanche
    p["date_passage"] = premier + pd.to_timedelta(decalage, unit="D")

    def drapeau(c):
        return (pd.to_numeric(r[c], errors="coerce") == 1) if c in r else pd.Series(False, index=r.index)
    grave = pd.concat([drapeau(c) for c in GRAVE], axis=1).any(axis=1)
    sans = pd.concat([drapeau(c) for c in SANS_CIBLE], axis=1).any(axis=1)
    p["classe"] = np.where(grave, "grave", np.where(drapeau("OBSDIS"), "intermediaire", "non_grave"))
    p.loc[sans & ~grave, "classe"] = None
    p["decision"] = p["classe"]
    p["groupe"] = np.where(p["nourrisson"] == 1, "enfant", np.where(age < AGE_ADULTE, "enfant", np.where(age.notna(), "adulte", None)))
    p["annee"] = annee
    p["source"] = "NHAMCS"
    return p


def lire_nhamcs(dossier: str | Path) -> pd.DataFrame:
    """Tous les fichiers ED<année>-stata.dta du dossier, réunis (un passage par ligne)."""
    fichiers = sorted(Path(dossier).glob("*.dta"))
    if not fichiers:
        raise FileNotFoundError(f"Aucun fichier .dta dans {dossier}.")
    return pd.concat([lire_annee(f) for f in fichiers], ignore_index=True)
