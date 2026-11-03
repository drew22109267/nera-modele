"""Plaintes bilingues, sac de mots sans fuite, groupe déduit de la profession, comparaison sur les mêmes passages."""
import pandas as pd
import torch

import triage  # noqa: F401
from traitement.urgences import PLAINTES, _groupe_sans_age, lire_passages, mots, plaintes
from triage.nhamcs import PLAINTES_RFV
from triage.variables import OptionsVariables, construire, vocabulaire


def test_plaintes_en_anglais_et_nouvelles_familles():
    p = plaintes("Fever, cough, chest pain, LOC, RTA")
    for f in ("fievre", "toux", "douleur_thoracique", "conscience", "traumatisme"):
        assert p[f"plainte_{f}"] == 1, f
    p = plaintes("Asthénie, vertiges, frissons, hémiplégie, polyurie, lombalgie, rhinorrhée, prurit")
    for f in ("asthenie", "vertiges", "frissons", "deficit_neurologique", "metabolique", "douleur_osteo_articulaire",
              "orl", "cutane"):
        assert p[f"plainte_{f}"] == 1, f
    assert sum(plaintes("Céphalées").values()) == 1


def test_nhamcs_a_les_memes_familles():
    assert set(PLAINTES_RFV) | {"traumatisme"} == set(PLAINTES)


def test_groupe_deduit_de_la_profession():
    assert _groupe_sans_age("Enfant", "?") == "enfant"
    assert _groupe_sans_age("", "? mois") == "enfant"
    assert _groupe_sans_age("Ménagère", "?") == "adulte"
    assert _groupe_sans_age("Élève", "?") is None                   # 10 à 20 ans : pas sûr
    assert _groupe_sans_age("", "?") is None


def test_lecture_garde_le_groupe_deduit(tmp_path):
    entete = "Date de passage;Sexe;Âge;Profession;Plaintes;Décision"
    lignes = [entete, "25/01/26;F;?;Commerçante;Fever, headache;Hosp", "26/01/26;M;4 ans;;Toux;Ext",
              "27/01/26;M;?;Élève;Toux;Ext"]
    f = tmp_path / "urg.csv"
    f.write_text("\n".join(lignes), encoding="utf-8")
    df, _ = lire_passages(f, aujourdhui=pd.Timestamp("2026-10-23"))
    assert list(df["groupe"][:2]) == ["adulte", "enfant"] and pd.isna(df.loc[2, "groupe"])
    assert list(df["groupe_deduit"]) == [1, 0, 0]
    assert df.loc[0, "plainte_fievre"] == 1 and df.loc[0, "plaintes_texte"] == "fever, headache"


def test_vocabulaire_avant_le_verrou_seulement():
    d = pd.DataFrame({"date_passage": pd.to_datetime(["2026-01-01"] * 5 + ["2026-10-01"] * 9),
                      "plaintes_texte": ["fievre, toux"] * 5 + ["paludisme"] * 9})
    v = vocabulaire(d, pd.Timestamp("2026-09-01"))
    assert v == ("fievre", "toux")                                  # « paludisme » n'est écrit qu'après le verrou
    assert mots("Douleur de la tête et fièvre") == {"douleur", "tete", "fievre"}


def test_colonnes_de_mots():
    d = pd.DataFrame({"date_passage": pd.to_datetime(["2026-01-01", "2026-02-01"]), "classe": ["grave", "non_grave"],
                      "age": [3.0, 5.0], "sexe": ["F", "M"], "plaintes_texte": ["fievre, convulsions", "toux"],
                      "plainte_fievre": [1, 0], "nombre_plaintes": [2, 1], "groupe": ["enfant", "enfant"]})
    o = OptionsVariables(plaintes=False, contexte=False, manquants=False, mots=("convulsions", "toux"))
    tab = construire(d, o)
    j = [tab.noms.index("mot_convulsions"), tab.noms.index("mot_toux")]
    assert torch.equal(tab.X[:, j], torch.tensor([[1.0, 0.0], [0.0, 1.0]], dtype=tab.X.dtype))
    assert "plainte_fievre" not in tab.noms
    sans_texte = construire(d.drop(columns="plaintes_texte"), o)        # la source NHAMCS : mots non observés
    assert torch.isnan(sans_texte.X[:, j]).all()


def test_specificite_a_sensibilite_fixee():
    from triage.mesures import resume, specificite_a_sensibilite
    y = torch.tensor([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1], dtype=torch.float64)
    p = torch.tensor([.9, .9, .8, .8, .7, .7, .6, .6, .5, .1, .55, .3, .2, .05], dtype=torch.float64)
    # 90 % des graves (9 sur 10) : seuil 0,5 ; non-graves sous 0,5 : 3 sur 4
    assert specificite_a_sensibilite(y, p, 0.90) == 0.75
    # 100 % : seuil 0,1 ; seul 0,05 est dessous
    assert specificite_a_sensibilite(y, p, 1.0) == 0.25
    r = resume(y, p, seuil=0.2, rapport_couts=4.0)
    assert r["taux_alerte"] == 12 / 14


def test_restreindre_aligne_les_passages():
    from lancer_triage import restreindre
    res = {"y": torch.tensor([1.0, -1.0, 1.0]), "p": torch.tensor([0.9, 0.2, 0.6], dtype=torch.float64), "meo": torch.zeros(3),
           "ids": [10, 11, 12], "indices": torch.tensor([0, 1, 2]), "choix": {}}
    r = restreindre(res, [12, 10])
    assert r["p"].tolist() == [0.6, 0.9] and r["indices"].tolist() == [12, 10]
