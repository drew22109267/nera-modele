r"""
Valeurs normales des constantes selon l'âge, et signes d'alerte.

Les constantes n'ont pas le même sens à tout âge : un pouls de 140/min est normal chez un nourrisson et
inquiétant chez un adulte. On ramène donc chaque constante à sa plage normale [bas(âge), haut(âge)].

Plages retenues (valeurs de référence courantes, à VALIDER AVEC LE SERVICE avant le test final)
------------------------------------------------------------------------------------------------
  Pouls (/min)      < 1 an 100–160 · 1–2 ans 90–150 · 2–5 ans 80–140 · 5–12 ans 70–120 · 12–15 ans 60–100
                    · adulte 50–100                                          (APLS, pédiatrie avancée)
  FR (/min)         < 2 mois ≤ 60 · 2–12 mois ≤ 50 · 1–5 ans ≤ 40 · 5–12 ans ≤ 30 · 12–15 ans ≤ 24
                    · adulte ≤ 22     (seuils de tachypnée de l'OMS ; adulte : qSOFA)
                    bas : < 1 an 25 · 1–5 ans 20 · 5–12 ans 14 · ≥ 12 ans 10
  TA systolique     bas : < 1 mois 60 · < 1 an 70 · 1–10 ans 70 + 2 × âge · > 10 ans 90 (hypotension, PALS)
                    haut : adulte 180 (poussée hypertensive) ; pas de seuil haut chez l'enfant
  TA diastolique    haut : adulte 110
  Température (°C)  36,0–38,0 (hypothermie, fièvre)
  SpO2 (%)          bas 92
  Glycémie (g/L)    0,6–2,5 (hypoglycémie ≈ 3,3 mmol/L ; hyperglycémie ≈ 14 mmol/L)

Trois façons de donner une constante x au modèle (banc T5)
-----------------------------------------------------------
  brute    x tel quel ;
  écart    deux variables, l'excès au-dessus et le déficit au-dessous de la plage, relatifs :
               e⁺ = max(0, (x − haut)/haut)      e⁻ = max(0, (bas − x)/bas)
           elles valent 0 dans la plage normale ; un modèle LINÉAIRE peut alors voir qu'un pouls trop haut
           ET un pouls trop bas sont graves (une seule variable brute ne le peut pas : le danger est des
           deux côtés, en forme de U) ;
  seuil    deux indicatrices 1(x > haut) et 1(x < bas).
Le nombre de signes d'alerte (somme des indicatrices) est aussi la RÈGLE DE RÉFÉRENCE du banc T2 : « au
moins un signe d'alerte → patient grave », comme un score d'alerte précoce simplifié.
"""
from __future__ import annotations

import math

CONSTANTES_NORMEES = ["pouls", "fr", "ta_sys", "ta_dia", "temperature", "spo2", "glycemie"]
AGE_NOURRISSON = 0.5            # âge utilisé pour les normes d'un nourrisson (« NRS ») sans âge écrit


def _inconnu(v) -> bool:
    return v is None or (isinstance(v, float) and math.isnan(v))


def plage(constante: str, age: float | None, adulte: bool) -> tuple[float | None, float | None] | None:
    """(bas, haut) de la plage normale ; None dans le couple = pas de seuil de ce côté ;
    None tout court = plage inconnue (enfant sans âge, pour une constante qui dépend de l'âge)."""
    if constante == "temperature":
        return 36.0, 38.0
    if constante == "spo2":
        return 92.0, None
    if constante == "glycemie":
        return 0.6, 2.5
    if adulte:
        return {"pouls": (50.0, 100.0), "fr": (10.0, 22.0), "ta_sys": (90.0, 180.0), "ta_dia": (None, 110.0)}[constante]
    if constante == "ta_dia":
        return None, None                                # pas de seuil de TA diastolique chez l'enfant
    if _inconnu(age):
        return None
    if constante == "pouls":
        for limite, bornes in ((1, (100, 160)), (2, (90, 150)), (5, (80, 140)), (12, (70, 120))):
            if age < limite:
                return float(bornes[0]), float(bornes[1])
        return 60.0, 100.0
    if constante == "fr":
        haut = 60 if age < 2 / 12 else 50 if age < 1 else 40 if age < 5 else 30 if age < 12 else 24
        bas = 25 if age < 1 else 20 if age < 5 else 14 if age < 12 else 10
        return float(bas), float(haut)
    if constante == "ta_sys":
        bas = 60 if age < 1 / 12 else 70 if age < 1 else 70 + 2 * age if age <= 10 else 90
        return float(bas), None
    raise ValueError(f"Constante sans norme : {constante}")


def ecarts(x: float | None, bas: float | None, haut: float | None) -> tuple[float, float]:
    """(e⁺, e⁻) ; NaN si la constante manque, 0 du côté où il n'y a pas de seuil."""
    if _inconnu(x):
        return math.nan, math.nan
    e_haut = max(0.0, (x - haut) / haut) if haut is not None else 0.0
    e_bas = max(0.0, (bas - x) / bas) if bas is not None else 0.0
    return e_haut, e_bas


def alertes(x: float | None, bas: float | None, haut: float | None) -> tuple[float, float]:
    """(1(x > haut), 1(x < bas)) ; NaN si la constante manque."""
    if _inconnu(x):
        return math.nan, math.nan
    return float(haut is not None and x > haut), float(bas is not None and x < bas)
