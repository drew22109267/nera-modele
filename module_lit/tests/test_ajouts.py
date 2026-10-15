"""Briques ajoutées pour le banc de comparaison : cas vérifiables à la main."""
from datetime import date

import pandas as pd
import pytest
import torch

from svr import analyse as A
from svr.calendrier import feries, paques
from svr.caracteristiques import construire
from svr.classiques import RegressionRidge, holt_winters

T = torch.float64


def test_paques_et_feries_camerounais():
    # Dates de Pâques connues (calendrier grégorien)
    assert paques(2024) == date(2024, 3, 31) and paques(2025) == date(2025, 4, 20) and paques(2026) == date(2026, 4, 5)
    f = feries([2026])
    assert date(2026, 5, 20) in f and date(2026, 2, 11) in f            # fête nationale, fête de la Jeunesse
    assert date(2026, 4, 3) in f and date(2026, 5, 14) in f             # Vendredi saint, Ascension (Pâques + 39)
    assert date(2026, 5, 21) not in f


def test_holt_winters_serie_purement_hebdomadaire():
    # Série = motif hebdomadaire exact, sans tendance : la prévision doit retrouver le motif.
    motif = [10.0, 12, 14, 13, 11, 8, 7]
    serie = torch.tensor(motif * 10, dtype=T)
    origines = torch.arange(30, 60)
    prev = holt_winters(serie, origines, 1, alpha=0.3, beta=0.0, gamma=0.3, phi=0.9)
    assert torch.allclose(prev, serie[origines + 1], atol=1e-9)


def test_ridge_retrouve_une_droite():
    X = torch.linspace(0, 1, 20, dtype=T)[:, None]
    y = 3 * X[:, 0] + 2
    m = RegressionRidge(1e-9).entrainer(X, y)
    assert float(m.w[0]) == pytest.approx(3.0, abs=1e-5) and float(m.b) == pytest.approx(2.0, abs=1e-5)


def test_construire_options():
    jours = pd.date_range("2026-01-01", periods=40, freq="D")
    occ = pd.DataFrame({"presents": range(40), "admissions": 1, "sorties_sortie": 1}, index=jours)
    defaut = construire(occ, 1)
    assert defaut.X.shape[1] == 19 and defaut.noms[0] == "occ_j-0"     # 7 + 3 + 7 + 2 : inchangé
    assert defaut.continues == list(range(10)) + [17, 18]
    court = construire(occ, 1, retards=3, flux=False, calendrier=False, debut_min=13)
    assert court.X.shape[1] == 3 and int(court.origines[0]) == 13
    avec = construire(occ, 1, feries={date(2026, 1, 15)})
    i = list(avec.dates_cible).index(pd.Timestamp("2026-01-15"))
    assert avec.X[i, avec.noms.index("cible_feriee")] == 1 and avec.X[i + 1, avec.noms.index("veille_feriee")] == 1


def test_cout_et_importance():
    y = torch.tensor([10.0, 10.0], dtype=T)
    assert A.cout_decision(y, torch.tensor([8.0, 12.0], dtype=T), 4, 1) == pytest.approx((4 * 2 + 1 * 2) / 2)

    class Lineaire:                                                    # n'utilise que la colonne 0
        def predire(self, X):
            return 2 * X[:, 0]
    X = torch.randn(200, 2, generator=torch.Generator().manual_seed(1), dtype=T)
    imp = A.importance_permutation(Lineaire(), X, 2 * X[:, 0], lambda a, b: float((a - b).abs().mean()),
                                   {"utile": [0], "inutile": [1]})
    assert imp["utile"][0] > 0.5 and imp["inutile"][0] == pytest.approx(0.0)
