r"""
LIEN ENTRE LE MODULE TRIAGE ET LE MODULE LIT (protocole, Document 11, § 1.4 et étape 3).

L'idée
------
Un enfant jugé grave aux urgences aujourd'hui occupe un lit de pédiatrie ce soir ou demain. Le triage est
donc un SIGNAL D'AVANCE pour les lits. Le protocole prévoyait de relier chaque passage à son séjour par un
identifiant patient commun ; il n'existe pas (le registre des urgences n'a qu'un numéro de dossier, qui n'est
pas lu, et les noms ne sont pas transcrits). Le lien est donc fait JOUR PAR JOUR, ce qui ne demande aucune
donnée de patient :

    x_d = ce que les urgences montrent le jour d          y_{d+k} = ce que la pédiatrie reçoit k jours plus tard

Trois signaux des urgences (groupe enfant, < 15 ans), connus au soir du jour d :
    passages      nombre d'enfants passés aux urgences (avec ou sans décision lisible)
    graves        enfants orientés graves (hospitalisé, référé, décédé, SCAM, MEO) : la DÉCISION observée
    charge        Σ P(grave) : la somme des probabilités données par le MODÈLE de triage, chacune hors
                  échantillon (validation croisée par mois, ou validation mensuelle avec --probabilite)

Partie A · la corrélation
-------------------------
Corrélation de Spearman (sur les rangs : les comptages sont asymétriques) entre x_d et les admissions en
pédiatrie y_{d+k}, pour k = 0, 1, 2, 3 jours. Les jours sans aucun passage transcrit sont des TROUS du registre
(environ 20 passages par jour en moyenne), pas des zéros : ils sont retirés.
  · Intervalle à 95 % par bootstrap en blocs de 7 jours (les jours voisins se ressemblent : tirer les jours un
    par un donnerait un intervalle trop étroit).
  · p-valeur par décalage circulaire : on fait glisser la série des urgences de s jours (s = 7 … n − 7) par
    rapport à celle des admissions, ce qui casse le lien jour à jour mais garde la forme de chaque série
    (tendance, semaine) ; p = (1 + nombre de décalages où |r_s| ≥ |r|) / (1 + nombre de décalages).
  · Part des admissions qui passent par les urgences : enfants graves hors MEO ÷ admissions, mois par mois.

Partie B · le banc D12 : le triage améliore-t-il la prévision des lits ?
------------------------------------------------------------------------
Les signaux des urgences entrent dans le bloc « flux et saison » du noyau composite (le bloc « flux
d'admissions » du protocole), en somme sur le jour de l'origine et sur les 3 derniers jours :

    D12-0  sans les urgences (référence : le modèle habituel, mêmes jours, même fenêtre)
    D12-1  + passages enfants aux urgences
    D12-2  + enfants graves orientés (décision observée)
    D12-3  + charge grave attendue Σ P(grave) (sortie du module triage)
    D12-4  + graves observés + charge
    D12-T  + charge Σ P(grave) d'un modèle de triage PRÉ-ENTRAÎNÉ sur NHAMCS puis transféré (banc T9 du triage) :
           une variante par méthode de transfert présente dans probabilites_<groupe>.csv
    et, pour situer : le modèle habituel appris sur TOUT l'historique de la pédiatrie, et la persistance.
Le test de Diebold-Mariano de D12-T contre D12-3 (même modèle lit, charge du modèle local) se lit sur leurs
erreurs : le pré-entraînement améliore-t-il AUSSI la prévision des lits ?

Toutes les variantes sont apprises et évaluées sur les MÊMES jours : ceux où les urgences sont connues (la
fenêtre du registre des urgences), en validation glissante (rien du futur). Test de Diebold-Mariano de chaque
variante contre la référence D12-0 : « meilleur » = le triage apporte une information que l'historique des
lits n'avait pas.

Limites à écrire dans le mémoire
--------------------------------
  · Fenêtre courte (registre des urgences : environ septembre 2025 → janvier 2026) : peu de jours d'apprentissage
    pour le banc D12, d'où un intervalle large ; c'est une PREUVE DE CONCEPT du couplage.
  · Les probabilités ne portent que sur les passages dont la décision est lisible (le modèle de triage les
    apprend et les évalue sur ceux-là).
  · Une partie des admissions ne passe pas par les urgences (consultation, transferts internes) : la partie A
    le mesure.

Usage (WSL, depuis nera-modele/module_lit, APRÈS lancer_triage.py et l'étape 1 de lancer_tout.sh) :
    ~/memoire-env/bin/python lien_triage_lits.py --service PED --horizons 1 7
    ~/memoire-env/bin/python lien_triage_lits.py --service PED --comptage pic --probabilite chronologique

Sorties dans resultats/ (<lab> = PED, ou PED_<comptage> hors minuit) :
    lien_triage_<lab>_correlations.csv   Spearman, intervalle, p-valeur, pour chaque signal et chaque décalage
    lien_triage_<lab>_mois.csv           part des admissions passées par les urgences, mois par mois
    lien_triage_<lab>_series.csv         les séries jour par jour (urgences et pédiatrie)
    benchmark_<lab>_D12_h<h>.csv         banc D12 (repris par exporter_resultats.py dans l'outil de saisie)
    lien_triage_<lab>.md                 rapport pour le mémoire
    lien_triage_<lab>.png                figure : séries lissées et corrélations par décalage
"""
from __future__ import annotations

import argparse
import dataclasses
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")                     # dessin dans des fichiers, sans fenêtre (WSL n'a pas d'écran)
import matplotlib.pyplot as plt
import pandas as pd
import torch

from benchmark_choix import Dimension, en_markdown
from lancer_niveaux import lire_occupation
from traitement.comptage import etiquette, option_comptage
from traitement.verrou import DATE_VERROU
from svr import metriques as M
from svr import references as R
from svr.caracteristiques import construire
from svr.niveaux import Hyperparametres, fabrique
from svr.validation import origines_glissantes
from transfert import entrainer_predire
from validation_finale import hyperparametres

TYPE = torch.float64
SIGNAUX = {"passages": "passages enfants aux urgences",
           "graves": "enfants graves orientés (décision observée)",
           "charge": "charge grave attendue Σ P(grave) (modèle de triage)"}
VARIANTES = [("D12-1 · + passages enfants aux urgences", ["passages"]),
             ("D12-2 · + enfants graves orientés (décision observée)", ["graves"]),
             ("D12-3 · + charge grave attendue Σ P(grave) (module triage)", ["charge"]),
             ("D12-4 · + graves observés + charge", ["graves", "charge"])]
REFERENCE = "D12-0 · sans les urgences (même fenêtre)"


# ─── Les séries des urgences ────────────────────────────────────────────────────────────────────

def series_urgences(dossier: Path, groupe: str, colonne_p: str) -> pd.DataFrame:
    """Une ligne par jour du registre des urgences : passages, graves (avec et sans MEO), charge Σ P(grave)."""
    chemin_p, chemin_j = dossier / f"probabilites_{groupe}.csv", dossier / f"passages_{groupe}.csv"
    for c in (chemin_p, chemin_j):
        if not c.exists():
            raise SystemExit(f"{c} absent : lancez d'abord module_triage/lancer_triage.py (il écrit ce fichier).")
    prob = pd.read_csv(chemin_p, parse_dates=["date"])
    if colonne_p not in prob:
        raise SystemExit(f"Colonne {colonne_p} absente de {chemin_p.name} (relancez lancer_triage.py).")
    jours = pd.read_csv(chemin_j, parse_dates=["date"]).set_index("date")["passages"]
    jours = jours[jours.index < DATE_VERROU]
    prob = prob[prob["date"] < DATE_VERROU]
    transferts = [c[len(colonne_p) + 1:] for c in prob.columns if c.startswith(colonne_p + "_")]
    agregats = {"graves": ("grave", "sum"), "meo": ("meo", "sum"), "charge": (colonne_p, lambda s: s.sum(min_count=1))}
    agregats |= {f"charge_{v}": (f"{colonne_p}_{v}", lambda s: s.sum(min_count=1)) for v in transferts}
    par_jour = prob.groupby("date").agg(**agregats)
    par_jour["graves_hors_meo"] = prob[(prob["grave"] > 0) & (prob["meo"] == 0)].groupby("date").size()
    # Jours du registre : de son premier à son dernier jour ; un jour sans passage transcrit est un trou (NaN).
    calendrier = pd.date_range(jours.index.min(), jours.index.max(), freq="D")
    u = pd.DataFrame(index=calendrier)
    u["passages"] = jours.reindex(calendrier)
    for c in ("graves", "meo", "charge", "graves_hors_meo", *[f"charge_{v}" for v in transferts]):
        u[c] = par_jour[c].reindex(calendrier)
    connus = u["passages"].notna()
    u.loc[connus, ["graves", "meo", "graves_hors_meo"]] = u.loc[connus, ["graves", "meo", "graves_hors_meo"]].fillna(0)
    return u.rename_axis("jour")


# ─── Partie A : corrélations ────────────────────────────────────────────────────────────────────

def rangs(x: torch.Tensor) -> torch.Tensor:
    """Rangs moyens (ex aequo : moyenne de leurs rangs)."""
    return torch.tensor(pd.Series(x.numpy()).rank(method="average").to_numpy(), dtype=TYPE)


def spearman(x: torch.Tensor, y: torch.Tensor) -> float:
    """Corrélation de Pearson des rangs."""
    rx, ry = rangs(x), rangs(y)
    rx, ry = rx - rx.mean(), ry - ry.mean()
    den = torch.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    return float((rx * ry).sum() / den) if den > 0 else float("nan")


def correlation(x: pd.Series, y: pd.Series, k: int, bootstrap: int, graine: int) -> dict:
    """Spearman entre x_d et y_{d+k}, intervalle par bootstrap en blocs de 7 jours, p-valeur par décalage circulaire."""
    yk = y.shift(-k).reindex(x.index)                     # y_{d+k} aligné sur le jour d
    ok = x.notna() & yk.notna()
    xs, ys = torch.tensor(x[ok].to_numpy(), dtype=TYPE), torch.tensor(yk[ok].to_numpy(), dtype=TYPE)
    n = len(xs)
    if n < 20:
        return {"jours": n, "spearman": float("nan"), "IC95_bas": float("nan"), "IC95_haut": float("nan"), "p_valeur": float("nan")}
    r = spearman(xs, ys)
    # Bootstrap en blocs : on tire des blocs de 7 jours consécutifs (parmi les jours valides) avec remise.
    gen = torch.Generator().manual_seed(graine)
    nb_blocs = (n + 6) // 7
    debuts = torch.randint(0, n - 6, (bootstrap, nb_blocs), generator=gen)
    tirages = []
    for b in range(bootstrap):
        idx = (debuts[b].unsqueeze(1) + torch.arange(7)).flatten()[:n]
        tirages.append(spearman(xs[idx], ys[idx]))
    t = torch.tensor([v for v in tirages if v == v], dtype=TYPE)
    bas, haut = (float(torch.quantile(t, 0.025)), float(torch.quantile(t, 0.975))) if len(t) else (float("nan"),) * 2
    # Décalage circulaire sur la série complète (trous compris), puis mêmes jours valides que ci-dessus.
    xa = torch.tensor(x.to_numpy(dtype=float, na_value=float("nan")), dtype=TYPE)
    ya = torch.tensor(yk.to_numpy(dtype=float, na_value=float("nan")), dtype=TYPE)
    N = len(xa)
    extremes = total = 0
    for s in range(7, N - 6):
        xd = torch.roll(xa, s)                            # rotation : la fin revient au début
        m = ~(torch.isnan(xd) | torch.isnan(ya))
        if int(m.sum()) < 20:
            continue
        rs = spearman(xd[m], ya[m])
        total += 1
        extremes += abs(rs) >= abs(r) - 1e-12
    p = (1 + extremes) / (1 + total) if total else float("nan")
    return {"jours": n, "spearman": round(r, 3), "IC95_bas": round(bas, 3), "IC95_haut": round(haut, 3),
            "p_valeur": round(p, 4)}


# ─── Partie B : banc D12 ────────────────────────────────────────────────────────────────────────

def avec_urgences(tab, u: pd.DataFrame, signaux: list[str]):
    """Ajoute, pour chaque signal, la somme du jour de l'origine et des 3 derniers jours (NaN si un jour manque)."""
    cols, noms = [], list(tab.noms)
    for s in signaux:
        serie = u[s]
        j1 = serie.reindex(tab.dates_origine).to_numpy()
        j3 = serie.rolling(3, min_periods=3).sum().reindex(tab.dates_origine).to_numpy()
        cols += [torch.tensor(j1.astype(float), dtype=TYPE), torch.tensor(j3.astype(float), dtype=TYPE)]
        noms += [f"urg_{s}_1j", f"urg_{s}_3j"]
    if not cols:
        return tab
    X = torch.cat([tab.X, torch.stack(cols, dim=1)], dim=1)
    nouvelles = list(range(tab.X.shape[1], X.shape[1]))
    blocs = {**tab.blocs, "flux_saison": tab.blocs["flux_saison"] + nouvelles}
    return dataclasses.replace(tab, X=X, noms=noms, blocs=blocs, continues=tab.continues + nouvelles)


def garder(tab, masque: torch.Tensor):
    """Sous-tableau des lignes retenues (la série complète reste, pour la persistance)."""
    m = masque.numpy()
    return dataclasses.replace(tab, X=tab.X[masque], y=tab.y[masque], origines=tab.origines[masque],
                               dates_origine=tab.dates_origine[m], dates_cible=tab.dates_cible[m])


def transferes(u: pd.DataFrame) -> list[str]:
    """Signaux « charge » des modèles transférés présents (colonnes charge_<variante>)."""
    return [c for c in u.columns if c.startswith("charge_")]


def banc_d12(occ: pd.DataFrame, u: pd.DataFrame, h: int, hp: Hyperparametres, niveau: int, pas: int,
             minimum: int, tau: float) -> tuple[Dimension, int, int]:
    complet = construire(occ, h)
    variantes = VARIANTES + [(f"D12-T · + charge du modèle transféré ({c[len('charge_'):]})", [c]) for c in transferes(u)]
    tous = avec_urgences(complet, u, ["passages", "graves", "charge", *transferes(u)])
    # Mêmes jours pour toutes les variantes : tous les signaux connus à l'origine.
    masque = ~torch.isnan(tous.X[:, complet.X.shape[1]:]).any(dim=1)
    if int(masque.sum()) < minimum + 14:
        raise ValueError(f"seulement {int(masque.sum())} jours avec les urgences connues : trop peu pour le banc D12.")
    ref = garder(complet, masque)
    debut = ref.dates_origine.min() + pd.Timedelta(days=minimum + h)
    decs = origines_glissantes(ref, debut, DATE_VERROU, pas=pas, minimum_entrainement=minimum)
    y = torch.cat([ref.y[d.evaluation] for d in decs])
    orig = torch.cat([ref.origines[d.evaluation] for d in decs])
    dim = Dimension("D12", f"Apport du triage à la prévision des lits (J+{h})",
                    "Les signaux des urgences améliorent-ils la prévision de l'occupation ?", h, tau)

    def evaluer(tab, nom, retenu=False):
        t0 = time.time()
        prev = [entrainer_predire(fabrique(niveau, hp, tab.blocs), tab.X[d.entrainement], tab.y[d.entrainement],
                                  tab.X[d.evaluation], tab.continues) for d in decs]
        prev = {k: torch.cat([p[k] for p in prev]) for k in prev[0]} if isinstance(prev[0], dict) else torch.cat(prev)
        dim.ajouter(nom, y, prev, time.time() - t0, retenu=retenu)
        print(f"   {nom}")

    evaluer(ref, REFERENCE, retenu=True)
    for nom, signaux in variantes:
        evaluer(garder(avec_urgences(complet, u, signaux), masque), nom)
    # Pour situer : le modèle habituel appris sur tout l'historique (mêmes jours évalués), et la persistance.
    t0 = time.time()
    prev = []
    for d in decs:
        o = d.origine
        entr = torch.nonzero(torch.tensor(complet.dates_cible <= o)).flatten()
        ev = ref.origines[d.evaluation] - complet.origines[0]          # mêmes jours, indices du tableau complet
        prev.append(entrainer_predire(fabrique(niveau, hp, complet.blocs), complet.X[entr], complet.y[entr],
                                      complet.X[ev], complet.continues))
    prev = {k: torch.cat([p[k] for p in prev]) for k in prev[0]} if isinstance(prev[0], dict) else torch.cat(prev)
    dim.ajouter("modèle habituel, tout l'historique de la pédiatrie (sans urgences)", y, prev, time.time() - t0)
    dim.ajouter("persistance", y, R.persistance(ref.serie, orig, h), 0.0)
    return dim, len(y), len(decs)


# ─── Programme ──────────────────────────────────────────────────────────────────────────────────

def main() -> None:
    p = argparse.ArgumentParser(description="Lien entre le module triage et le module lit (corrélation et banc D12).")
    p.add_argument("--service", default="PED")
    p.add_argument("--groupe", default="enfant", choices=["enfant", "adulte"], help="groupe du triage relié au service (enfant)")
    p.add_argument("--triage", default="../module_triage/resultats/triage", help="dossier des résultats du triage")
    p.add_argument("--probabilite", default="croisee", choices=["croisee", "chronologique"],
                   help="P(grave) par validation croisée par mois (tous les mois, défaut) ou mensuelle (premiers mois vides)")
    p.add_argument("--horizons", type=int, nargs="+", default=[1, 7])
    p.add_argument("--tau", type=float, default=0.8)
    p.add_argument("--niveau", type=int, default=4, choices=[1, 2, 3, 4])
    p.add_argument("--pas", type=int, default=7, help="jours entre deux origines de la validation glissante (7)")
    p.add_argument("--minimum-entrainement", type=int, default=28)
    p.add_argument("--decalages", type=int, nargs="+", default=[0, 1, 2, 3])
    p.add_argument("--bootstrap", type=int, default=2000)
    p.add_argument("--graine", type=int, default=0)
    option_comptage(p)
    a = p.parse_args()

    lab = etiquette(a.service, a.comptage)
    resultats = Path("resultats")
    occ = lire_occupation(lab)
    u = series_urgences(Path(a.triage), a.groupe, f"p_{a.probabilite}")
    print(f"Urgences ({a.groupe}) : {u.index.min():%d/%m/%Y} → {u.index.max():%d/%m/%Y}, "
          f"{int(u['passages'].notna().sum())} jours transcrits sur {len(u)}")
    serie = pd.DataFrame({"admissions_service": occ["admissions"], "presents_service": occ["presents"]}).join(u, how="outer")
    serie.to_csv(resultats / f"lien_triage_{lab}_series.csv", sep=";", encoding="utf-8-sig")

    # ── Partie A
    signaux = SIGNAUX | {c: f"charge Σ P(grave), modèle transféré ({c[len('charge_'):]})" for c in transferes(u)}
    lignes = []
    for s, titre in signaux.items():
        for cible in ("admissions_service", "presents_service"):
            for k in a.decalages:
                c = correlation(serie[s], serie[cible], k, a.bootstrap, a.graine)
                lignes.append({"signal des urgences (jour d)": titre, "service (jour d+k)": cible.replace("_service", ""),
                               "k (jours)": k, **c})
    corr = pd.DataFrame(lignes)
    corr.to_csv(resultats / f"lien_triage_{lab}_correlations.csv", sep=";", encoding="utf-8-sig", index=False)
    print(f"\n── Corrélations de Spearman (urgences au jour d, {a.service} au jour d+k)\n{corr.to_string(index=False)}")

    fenetre = serie[serie["passages"].notna()]
    mois = fenetre.groupby(fenetre.index.to_period("M")).agg(
        jours_transcrits=("passages", "size"), passages_enfants=("passages", "sum"),
        graves_hors_meo=("graves_hors_meo", "sum"), meo=("meo", "sum"), admissions_service=("admissions_service", "sum"))
    mois["part_admissions_par_urgences_%"] = (100 * mois["graves_hors_meo"] / mois["admissions_service"]).round(1)
    mois.to_csv(resultats / f"lien_triage_{lab}_mois.csv", sep=";", encoding="utf-8-sig")
    print(f"\n── Part des admissions passées par les urgences (jours transcrits seulement)\n{mois.to_string()}")

    # ── Partie B
    chemin_hp = lambda h: resultats / f"hyperparametres_{lab}_h{h}.json"
    rapport = [f"# Lien entre le triage et les lits — {a.service} (comptage : {a.comptage})\n",
               f"Urgences, groupe {a.groupe} : {u.index.min():%d/%m/%Y} → {u.index.max():%d/%m/%Y}, "
               f"{int(u['passages'].notna().sum())} jours transcrits. Probabilités : validation {a.probabilite}.\n",
               "## A · Corrélation entre les urgences au jour d et le service au jour d + k\n",
               "Spearman ; intervalle à 95 % par bootstrap en blocs de 7 jours ; p-valeur par décalage circulaire.\n",
               en_markdown(corr), "\n\n### Part des admissions passées par les urgences\n", en_markdown(mois.reset_index().astype(str)), "\n",
               "\n## B · Banc D12 : le triage améliore-t-il la prévision des lits ?\n"]
    for h in a.horizons:
        print(f"\n══════ Banc D12, horizon J+{h}")
        hp = hyperparametres(chemin_hp(h))[a.niveau] if chemin_hp(h).exists() else Hyperparametres(tau=a.tau)
        if not chemin_hp(h).exists():
            print(f"   ({chemin_hp(h).name} absent : hyperparamètres par défaut — lancez d'abord lancer_niveaux.py)")
        try:
            dim, jours, nb = banc_d12(occ, u, h, hp, a.niveau, a.pas, a.minimum_entrainement, a.tau)
        except ValueError as e:
            print(f"   impossible : {e}")
            rapport.append(f"\nJ+{h} : impossible ({e}).\n")
            continue
        t = dim.tableau().drop(columns=["temps (s)"])
        # Deuxième comparaison : chaque charge transférée contre la charge du modèle de triage LOCAL (D12-3).
        locale = next((k for k in dim.points if k.startswith("D12-3")), None)
        if locale is not None and len(dim.y) > 10:
            pv, verdict = [], []
            for nom in t.index:
                if not nom.startswith("D12-T"):
                    pv.append(None); verdict.append(""); continue
                dm = M.diebold_mariano(dim.y, dim.quantiles[nom], dim.quantiles[locale], h=h, perte="pinball", tau=dim.tau)
                pv.append(dm["p_valeur"])
                verdict.append(dm["plus_precis"])
            p_holm = M.holm(pv)
            verdict = ["" if s == "" else "identique" if s == "indéterminé" else
                       (("meilleur" if s == "A" else "moins bon") if ph < 0.05 else "équivalent")
                       for s, ph in zip(verdict, p_holm)]
            t[f"DM p (pinball τ={dim.tau}) vs charge locale"], t["p Holm vs charge locale"] = pv, p_holm
            t["vs charge locale (D12-3)"] = verdict
        print(t.to_string())
        t.to_csv(resultats / f"benchmark_{lab}_D12_h{h}.csv", sep=";", encoding="utf-8-sig")
        rapport += [f"\n### Horizon J+{h} ({jours} jours évalués, {nb} origines)\n", en_markdown(t.reset_index()), "\n",
                    dim.conclusion(t).replace("le choix est à revoir", "le triage apporte une information utile"), "\n"]
    (resultats / f"lien_triage_{lab}.md").write_text("\n".join(rapport), encoding="utf-8")

    # ── Figure
    fig, (g1, g2) = plt.subplots(2, 1, figsize=(10, 8))
    lisse = fenetre[["admissions_service", "graves", "charge"]].rolling(7, min_periods=4).mean()
    g1.plot(lisse.index, lisse["admissions_service"], color="#1f3b73", label=f"admissions {a.service}")
    g1.plot(lisse.index, lisse["graves"], color="#000000", label="enfants graves aux urgences")
    g1.plot(lisse.index, lisse["charge"], color="#5b8bd9", linestyle="--", label="charge Σ P(grave)")
    g1.set_title("Moyennes sur 7 jours"); g1.legend(); g1.grid(alpha=0.3)
    adm = corr[corr["service (jour d+k)"] == "admissions"]
    largeur = 0.25
    for i, (s, titre) in enumerate(SIGNAUX.items()):
        d = adm[adm["signal des urgences (jour d)"] == titre]
        x = d["k (jours)"].to_numpy() + (i - 1) * largeur
        g2.bar(x, d["spearman"], largeur, color=["#5b8bd9", "#000000", "#1f3b73"][i], label=s,
               yerr=[(d["spearman"] - d["IC95_bas"]).to_numpy(), (d["IC95_haut"] - d["spearman"]).to_numpy()], capsize=3)
    g2.axhline(0, color="grey", linewidth=0.8)
    g2.set_xlabel("décalage k (jours) : urgences au jour d, admissions au jour d + k"); g2.set_ylabel("Spearman")
    g2.set_title("Corrélation avec les admissions (intervalle à 95 %)"); g2.legend(); g2.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(resultats / f"lien_triage_{lab}.png", dpi=150); plt.close(fig)
    print(f"\nRapport : {resultats / f'lien_triage_{lab}.md'} · figure : lien_triage_{lab}.png")


if __name__ == "__main__":
    main()
