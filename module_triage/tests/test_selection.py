"""Règle de sélection du triage : un candidat ne remplace le modèle principal que si l'écart est significatif."""
import triage  # noqa: F401  (rend le dossier module_lit importable)
from lancer_triage import selectionner


def ligne(banc, variante, spec, p=None, auc=0.7):
    return {"banc": banc, "variante": variante, "svm": True, "imputation": "mediane", "cout_moyen": 0.5,
            "auc": auc, "spec_s90": spec, **({"spec_s90_p": p} if p is not None else {})}


def test_garde_le_principal_sans_ecart_significatif():
    lignes = [ligne("principal", "modèle principal", 0.30),
              ligne("T2", "svm composite", 0.36, p=0.04),      # p brute < 0,05 mais Holm sur 2 tests : 0,08
              ligne("T2", "svm linéaire", 0.31, p=0.50)]
    assert selectionner(lignes)["variante"] == "modèle principal"


def test_prend_le_candidat_significativement_meilleur():
    lignes = [ligne("principal", "modèle principal", 0.30),
              ligne("T2", "svm composite", 0.40, p=0.001),
              ligne("T2", "svm linéaire", 0.31, p=0.50)]
    assert selectionner(lignes)["variante"] == "svm composite"


def test_significatif_mais_moins_bon_ne_gagne_pas():
    lignes = [ligne("principal", "modèle principal", 0.30), ligne("T8", "knn", 0.20, p=0.001)]
    assert selectionner(lignes)["variante"] == "modèle principal"
