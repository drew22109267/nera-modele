"""Module triage : lecture du registre, normes, variables sans fuite, gradients, mesures, chaîne complète."""
import math

import pandas as pd
import pytest
import torch

import triage  # noqa: F401
from svr.modeles import Entrainement
from svr.noyaux import NoyauRBF
from traitement.urgences import classe_decision, lire_age, lire_glycemie, lire_passages, lire_ta
from triage.mesures import mcnemar, resume, seuil_optimal
from triage.modeles import RegressionLogistique, SVMNoyauClassifieur
from triage.normes import ecarts, plage
from triage.validation import ConfigTriage, decoupages_mensuels, evaluer
from triage.variables import OptionsVariables, Preparateur, construire

T = torch.float64


@pytest.mark.parametrize("texte, attendu", [("4 ans", 4.0), ("9 mois", 0.75), ("1 an 6 mois", 1.5), ("35", 35.0),
                                             ("2 sem", 14 / 365.25), ("10 j", 10 / 365.25), ("18 mois", 1.5)])
def test_age_en_annees(texte, attendu):
    age, _ = lire_age(texte)
    assert age == pytest.approx(attendu)


def test_nourrisson_sans_age():
    assert lire_age("NRS") == (None, True)
    assert lire_age(None, "NRS") == (None, True)


def test_ta_et_glycemie():
    assert lire_ta("120/80") == (120, 80)
    assert lire_ta("12/8") == (120, 80)                         # cmHg
    assert lire_ta("80/120") == (None, None)                    # systolique < diastolique : impossible
    assert lire_glycemie("0,95 g/L") == pytest.approx(0.95)
    assert lire_glycemie("5,551 mmol/L") == pytest.approx(1.0)
    assert lire_glycemie("95 mg/dL") == pytest.approx(0.95)
    assert lire_glycemie("HI") == 6.0 and lire_glycemie("LO") == 0.2
    assert lire_glycemie("1,2") == pytest.approx(1.2)           # sans unité, ≤ 3 : g/L


def test_decision_en_classe():
    assert classe_decision("Hospitalisé (pédiatrie)") == "grave"
    assert classe_decision("Référé") == "grave"
    assert classe_decision("†") == "grave"
    assert classe_decision("SCAM") == "grave"
    assert classe_decision("MEO") == "intermediaire"
    assert classe_decision("Externe") == "non_grave"
    assert classe_decision("") is None


def test_normes_selon_age():
    assert plage("pouls", 3.0, adulte=False) == (80.0, 140.0)
    assert plage("ta_sys", 3.0, adulte=False) == (76.0, None)   # 70 + 2 × 3
    assert plage("pouls", None, adulte=False) is None           # enfant sans âge : plage inconnue
    assert plage("pouls", None, adulte=True) == (50.0, 100.0)
    e_haut, e_bas = ecarts(168.0, 80.0, 140.0)
    assert e_haut == pytest.approx(0.2) and e_bas == 0.0        # (168 − 140)/140


def _passages(n_mois=4, par_jour=2):
    """Passages construits : grave si fièvre élevée ou SpO2 basse (règle connue, pour tester la chaîne)."""
    gen = torch.Generator().manual_seed(1)
    lignes = []
    for d in pd.date_range("2026-01-01", periods=30 * n_mois):
        for _ in range(par_jour):
            temp = 36.5 + 3.5 * float(torch.rand(1, generator=gen))
            spo2 = 85 + 15 * float(torch.rand(1, generator=gen))
            pouls = 90 + 60 * float(torch.rand(1, generator=gen))
            grave = temp > 39.0 or spo2 < 90
            lignes.append({"date_passage": d, "moment": "jour", "sexe": "F", "age": 4.0, "nourrisson": 0,
                           "pouls": pouls, "fr": 30.0, "ta_sys": None, "ta_dia": None, "temperature": temp,
                           "spo2": spo2, "glycemie": None, "poids": 16.0, "plainte_fievre": int(temp > 38),
                           "nombre_plaintes": 1, "classe": "grave" if grave else "non_grave", "groupe": "enfant"})
    return pd.DataFrame(lignes)


def test_preparateur_appris_sur_l_entrainement_seulement():
    tab = construire(_passages(1), OptionsVariables(constantes="brutes", plaintes=False, contexte=False, manquants=False))
    j = tab.noms.index("temperature")
    X = tab.X.clone()
    X[:10, j] = math.nan
    prep = Preparateur(tab.continues).ajuster(X[:30])
    mediane = torch.nanmedian(X[:30, j])
    Z = prep.transformer(X[:10])
    attendu = (mediane - prep.moyenne[tab.continues.index(j)]) / prep.ecart[tab.continues.index(j)]
    assert torch.allclose(Z[:, j], attendu.expand(10))          # manquant → médiane de l'entraînement
    assert not torch.isnan(prep.transformer(X)).any()


def _differences_finies(modele, y, nom, k, h=1e-6):
    p = modele.parametres[nom]
    J0, _, _ = modele.objectif_et_gradients(y)
    p[k] += h
    J1, _, _ = modele.objectif_et_gradients(y)
    p[k] -= h
    return (J1 - J0) / h


def test_gradient_svm_a_noyau():
    torch.manual_seed(0)
    X, y = torch.randn(12, 3, dtype=T), torch.tensor([1., -1.] * 6, dtype=T)
    m = SVMNoyauClassifieur(NoyauRBF(0.5), C_positif=2.0, C_negatif=1.0, entrainement=Entrainement(preconditionne=False))
    m.C_exemple = torch.where(y > 0, 2.0, 1.0).to(T)
    m._initialiser(X, y)
    m.parametres["alpha"] = 0.1 * torch.randn(12, dtype=T)
    m.parametres["b"] = torch.tensor([0.05], dtype=T)
    _, g, _ = m.objectif_et_gradients(y)
    for k in range(12):
        assert g["alpha"][k] == pytest.approx(_differences_finies(m, y, "alpha", k), abs=1e-4)
    assert torch.allclose(g["alpha"], m.gradient_exact(y)["alpha"])


def test_gradient_logistique():
    torch.manual_seed(0)
    X, y = torch.randn(20, 4, dtype=T), torch.tensor([1., -1.] * 10, dtype=T)
    m = RegressionLogistique(3.0, 1.0)
    m.C_exemple = torch.where(y > 0, 3.0, 1.0).to(T)
    m._initialiser(X, y)
    m.parametres["w"] = torch.randn(4, dtype=T)
    _, g, _ = m.objectif_et_gradients(y)
    for k in range(4):
        assert g["w"][k] == pytest.approx(_differences_finies(m, y, "w", k), abs=1e-4)


def test_mesures_et_mcnemar():
    y = torch.tensor([1, 1, 1, -1, -1], dtype=T)
    p = torch.tensor([0.9, 0.3, 0.6, 0.1, 0.7], dtype=T)
    r = resume(y, p, seuil=0.5, rapport_couts=4.0)
    assert (r["VP"], r["FN"], r["FP"], r["VN"]) == (2, 1, 1, 1)
    assert r["sensibilite"] == pytest.approx(2 / 3) and r["cout_moyen"] == pytest.approx((4 * 1 + 1) / 5)
    assert seuil_optimal(4.0) == pytest.approx(0.2)
    # 30 désaccords : A juste 20 fois, B juste 10 fois → χ² = (10 − 1)²/30 = 2,7
    y = torch.ones(30, dtype=T)
    a = torch.tensor([True] * 20 + [False] * 10)
    t = mcnemar(y, a, ~a)
    assert (t["b"], t["c"]) == (20, 10) and t["statistique"] == pytest.approx(2.7)
    assert mcnemar(torch.ones(3, dtype=T), torch.tensor([True, True, True]), torch.tensor([False, False, False]))["p_valeur"] == pytest.approx(0.25)


def test_chaine_complete_retrouve_la_regle():
    tab = construire(_passages(4), OptionsVariables())
    decs = decoupages_mensuels(tab.dates, pd.Timestamp("2026-05-01"), mois_min=2)
    assert [f"{d.mois:%m}" for d in decs] == ["03", "04"]
    assert all(tab.dates[d.entrainement.numpy()].max() < d.mois for d in decs)     # jamais le futur
    res = evaluer(tab, decs, ConfigTriage(modele="svm_rbf", grille_C=(1.0,), grille_portee=(0.25,),
                                          entrainement=Entrainement(iterations=400)))
    r = resume(res["y"], res["p"], seuil=0.2, rapport_couts=4.0)
    assert r["auc"] > 0.85 and r["sensibilite"] > 0.8
    assert ((res["p"] > 0) & (res["p"] < 1)).all()


def test_lecture_du_csv_de_l_outil(tmp_path):
    entete = ("Identifiant ligne;N° d'ordre;Date de passage;Garde;Sexe;Âge;Profession;Résidence;Pouls;TA;Glycémie;"
              "Poids;Température;FR;SpO2;Plaintes;Diagnostic;N° dossier;Décision;Remarque de saisie")
    lignes = [entete,
              "a;1;25/01/26;Garde;F;4 ans;élève;Q1;150;;5,5 mmol/L;15;39,5;45;95;Fièvre, Convulsions;Paludisme;123456;Hosp;",
              "b;2;26/01/26;Jour;M;35 ans;;Q2;80;12/8;;70;37;18;99;Céphalées;;654321;Ext;",
              "c;3;??;Jour;M;3 mois;NRS;;;;;;;;;;;;MEO;"]
    f = tmp_path / "urg.csv"
    f.write_text("﻿" + "\n".join(lignes), encoding="utf-8")
    df, rapport = lire_passages(f, aujourdhui=pd.Timestamp("2026-10-23"))
    assert rapport["date_illisible"] == 1 and len(df) == 2
    assert "n_dossier" not in df and "diagnostic" not in df and "residence" not in df      # jamais gardés
    assert list(df["classe"]) == ["grave", "non_grave"] and list(df["groupe"]) == ["enfant", "adulte"]
    assert df.loc[0, "plainte_convulsions"] == 1 and df.loc[0, "glycemie"] == pytest.approx(5.5 / 5.551)
    assert df.loc[1, "ta_sys"] == 120
