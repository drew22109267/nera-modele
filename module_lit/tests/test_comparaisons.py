"""Tests de comparaison des modèles : Diebold-Mariano sur la perte pinball, correction de Holm, reprise."""
import math

import torch

from svr import metriques as M
from svr.reprise import Reprise

T = torch.float64


def test_holm_cas_a_la_main():
    # p croissantes 0,01 ; 0,02 ; 0,04 avec m = 3 : 3·0,01 = 0,03 ; max(0,03 ; 2·0,02) = 0,04 ; max(0,04 ; 1·0,04) = 0,04
    assert M.holm([0.04, 0.01, 0.02]) == [0.04, 0.03, 0.04]
    # valeurs absentes gardées, bornée à 1
    r = M.holm([None, 0.6, float("nan"), 0.7])
    assert r[0] is None and math.isnan(r[2]) and r[1] == 1.0 and r[3] == 1.0


def test_dm_pinball_voit_le_quantile_et_pas_la_mediane():
    # A et B ont la même erreur absolue chaque jour, mais A sous-estime et B surestime.
    # Perte absolue : aucune différence. Pinball à τ = 0,8 : sous-estimer coûte 0,8, surestimer 0,2 → B gagne.
    g = torch.Generator().manual_seed(0)
    y = torch.randint(5, 15, (200,), generator=g).to(T)          # entiers : erreurs absolues exactement égales
    e = torch.randint(1, 4, (200,), generator=g).to(T)
    a, b = y - e, y + e
    assert M.diebold_mariano(y, a, b)["plus_precis"] == "indéterminé"
    t = M.diebold_mariano(y, a, b, perte="pinball", tau=0.8)
    assert t["plus_precis"] == "B" and t["significatif_5pc"]


def test_dm_pinball_demande_tau():
    y = torch.arange(20, dtype=T)
    try:
        M.diebold_mariano(y, y + 1, y - 1, perte="pinball")
    except ValueError:
        return
    raise AssertionError("tau manquant non signalé")


def test_reprise_adopter_garde_si_memes_donnees(tmp_path):
    r = Reprise(tmp_path, "code1", signature_donnees="donnees1")
    r.calculer("a", lambda: 1)
    # code changé, mêmes données, adopter : gardé
    r2 = Reprise(tmp_path, "code2", adopter=True, signature_donnees="donnees1")
    assert r2.existe("a")
    # code changé, autres données : effacé même avec adopter
    r3 = Reprise(tmp_path, "code3", adopter=True, signature_donnees="donnees2")
    assert not r3.existe("a")
    # code changé sans adopter : effacé
    r3.calculer("b", lambda: 2)
    r4 = Reprise(tmp_path, "code4", signature_donnees="donnees2")
    assert not r4.existe("b")


def test_reprise_ancienne_marque(tmp_path):
    (tmp_path / "signature.txt").write_text("ancienne", encoding="utf-8")
    torch.save({"cle": "x", "valeur": 3}, Reprise(tmp_path, "ancienne")._chemin("x"))
    r = Reprise(tmp_path, "nouvelle", adopter=True, signature_donnees="d")
    assert r.existe("x") and r.lire("x") == 3
