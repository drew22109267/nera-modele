"""Transfert (banc T9) : caractéristiques de Fourier, SVM a priori, toutes les variantes, sur des données fictives."""
import math

import pandas as pd
import torch

import triage  # noqa: F401
from triage.transfert import VARIANTES, ConfigTransfert, FourierAleatoire, Pretraine, SVMAPriori, evaluer_transfert
from triage.validation import decoupages_mensuels
from triage.variables import OptionsVariables, construire
from svr.modeles import TYPE, Entrainement

PLAINTES = ["fievre", "toux", "vomissements", "diarrhee", "convulsions", "douleur_abdominale", "cephalees", "dyspnee",
            "paleur", "conscience", "traumatisme", "brulure", "saignement", "douleur_thoracique", "oedemes", "ictere",
            "refus_alimentation", "deshydratation"]


def passages(n, debut, graine, decalage=0.0):
    """Enfants fictifs : grave si fièvre élevée et pouls rapide (plus un décalage propre au « pays »)."""
    g = torch.Generator().manual_seed(graine)
    t = 37 + 1.5 * torch.randn(n, generator=g)
    p = 110 + 25 * torch.randn(n, generator=g)
    score = (t - 38) + (p - 120) / 20 + decalage + 0.5 * torch.randn(n, generator=g)
    df = pd.DataFrame({"date_passage": pd.date_range(debut, periods=n, freq="6h"), "age": 4.0, "nourrisson": 0,
                       "sexe": "F", "temperature": t.numpy(), "pouls": p.numpy(), "fr": 30.0, "ta_sys": float("nan"),
                       "ta_dia": float("nan"), "spo2": 97.0, "glycemie": float("nan"), "poids": 15.0,
                       "moment": "jour", "groupe": "enfant", "nombre_plaintes": 1,
                       "classe": ["grave" if s > 0.8 else "non_grave" for s in score.tolist()]})
    for f in PLAINTES:
        df[f"plainte_{f}"] = 0
    df["plainte_fievre"] = (t > 38).to(torch.int64).numpy()
    return df


def test_fourier_approche_le_noyau_rbf():
    X = torch.randn(30, 5, dtype=TYPE)
    phi = FourierAleatoire(5, D=20000, gamma=0.2, graine=1)
    K = torch.exp(-0.2 * torch.cdist(X, X) ** 2)
    assert (phi(X) @ phi(X).T - K).abs().max() < 0.05


def test_regularisation_biaisee_reste_pres_du_modele_source():
    X = torch.randn(200, 4, dtype=TYPE); y = torch.where(X[:, 0] > 0, 1.0, -1.0).to(TYPE)
    w0 = torch.tensor([5.0, 5.0, 5.0, 5.0], dtype=TYPE)
    m = SVMAPriori(1e-4, 1e-4, Entrainement(iterations=300), w0=w0).entrainer(X, y)
    assert torch.allclose(m.parametres["w"], w0, atol=0.05)        # C minuscule : w reste w₀


def test_toutes_les_variantes_tournent():
    opts = OptionsVariables()
    source = passages(1500, "2020-01-01", 0)
    cible = passages(500, "2025-09-01", 1, decalage=0.3)
    tab_s, tab_c = construire(source, opts), construire(cible, opts)
    cfg = ConfigTransfert(D=100, grille_C=(1.0,), entrainement=Entrainement(iterations=150))
    pre = Pretraine(tab_s, tab_c, cfg)
    assert "glycemie" not in " ".join(pre.noms) and pre.auc_source > 0.7
    res = evaluer_transfert(tab_c, decoupages_mensuels(tab_c.dates, pd.Timestamp("2026-09-01"), 1), pre, cfg)
    assert set(res) == set(VARIANTES)
    n = {len(r["y"]) for r in res.values()}
    assert len(n) == 1                                              # mêmes passages pour toutes les variantes
    for r in res.values():
        assert torch.all((r["p"] >= 0) & (r["p"] <= 1)) and not math.isnan(float(r["p"].sum()))
