"""
Module triage du modèle NERA : priorité des patients aux urgences (classification grave / non grave).

Il réutilise les briques écrites à la main du module lit (dossier ../module_lit/svr : optimiseurs, socle
d'entraînement, SVM à coûts, calibration de Platt, AUC, Brier, arbre CART), et le paquet `traitement` du
dépôt outil-saisi pour lire le registre des urgences (traitement.urgences).
"""
import sys
from pathlib import Path

_LIT = Path(__file__).resolve().parents[2] / "module_lit"
if str(_LIT) not in sys.path:
    sys.path.insert(0, str(_LIT))
