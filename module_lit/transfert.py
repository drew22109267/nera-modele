r"""
TRANSFERT de la méthode du service source (pédiatrie, 27 mois de données) vers d'autres services,
comparé à un MODÈLE PROPRE de chaque service, et prévision du total de l'hôpital comme somme des
services.

Le problème
-----------
Un modèle appris sur 3 mois ne voit ni une saison complète ni beaucoup de situations rares.
Le banc de comparaison (D7) montre ce que coûte un historique court. On compare ici trois
façons de s'en sortir, sur les MÊMES jours du service cible :

  A · local          le modèle n'apprend que sur la fenêtre courte du service cible, avec les
                     hyperparamètres de la source gelés (pas de nouveau réglage sur 3 mois,
                     qui surapprendrait) ;
  B · transfert direct  le modèle n'apprend QUE sur la source ; il est appliqué tel quel au
                     service cible ;
  C · groupé         le modèle apprend sur la source ET sur la fenêtre de la cible réunies
                     (les jours de la cible peuvent compter plusieurs fois : --poids-cible).
  P · modèle propre  le modèle n'apprend que sur la cible ET choisit ses propres réglages sur la
                     cible (voir plus bas). C'est la stratégie RETENUE dès qu'un service a environ
                     un an d'historique (médecine femme : août 2025 → octobre 2026) ; A, B et C
                     servent alors à vérifier, par le test de Diebold-Mariano, que le transfert
                     n'apporte plus rien.
  G · modèle unique  UN SEUL modèle pour tous les services (source et cibles), appris en taux sur les
                     jours de tous les services réunis, avec une variable indicatrice du service (une
                     colonne 0/1 par service, dans le bloc « flux et saison » du noyau composite) pour
                     que chaque service garde son niveau. Les registres se chevauchent dans le temps :
                     tous les services sont évalués sur les MÊMES origines (une seule validation). Deux
                     options :
                       G1 · période commune : seulement les jours où tous les services ont des données
                            (pour la médecine femme, août 2025 → août 2026) ; la pédiatrie perd ses
                            premiers mois ;
                       G2 · toute la période : tous les jours de chaque service ; aucune donnée perdue,
                            mais le service le plus ancien (pédiatrie) pèse davantage.
  + la persistance de la cible (référence sans apprentissage).

Modèle propre : des réglages choisis sur la cible, sans rien du futur
---------------------------------------------------------------------
À chaque origine O, les réglages sont cherchés sur les seuls jours connus au soir de O, par une
validation IMBRIQUÉE : apprentissage sur les jours dont la cible est ≤ O − v, évaluation sur les
origines de ]O − v, O] (v = --validation-interne, 56 jours par défaut), puis réentraînement sur
tout ce qui est connu avec les réglages gagnants. La grille part des réglages de la source :
C × {0,3 ; 1 ; 3} et portées du noyau (γ, γ₁, γ₂) × {0,5 ; 1 ; 2}, soit 9 modèles ; le critère
est la perte pinball au quantile τ (MAE pour un modèle ponctuel). À égalité, les réglages de la
source sont gardés. Si la fenêtre interne est trop courte (moins de --minimum-entrainement jours
d'apprentissage), ce sont aussi les réglages de la source. Les réglages retenus à chaque origine
sont comptés dans le rapport : s'ils changent beaucoup d'une origine à l'autre, le choix est
instable (trop peu de jours pour régler) et la stratégie A est plus sûre.

Limite à écrire : un an d'historique ne montre chaque saison qu'une fois ; le modèle propre ne
peut pas séparer un effet de saison d'un hasard de cette année-là.

Rendre les services comparables : les taux
------------------------------------------
« 20 patients » ne veut pas dire la même chose dans un service de 20 lits et de 40 lits. Pour
B et C, toutes les grandeurs (présents, admissions, sorties) sont divisées par le nombre de lits
du service : on modélise des TAUX. La prévision est remultipliée par les lits de la cible.

Les hyperparamètres ont été choisis en NOMBRE de patients ; il faut les convertir pour qu'en
taux le modèle soit le même. Si Y = N·y (N lits) et que le modèle en nombre a pour objectif
    J_N = ½ αᵀKα + C Σ L_ε(Y − f),
en posant f = N f_r, α = N α_r et en remarquant que L_ε(N r) = N L_{ε/N}(r) (pour la perte
ε-insensible comme pour la pinball, qui sont positivement homogènes) :
    J_N = N² · [ ½ α_rᵀKα_r + (C/N) Σ L_{ε/N}(y − f_r) ].
Minimiser J_N revient donc à minimiser le même objectif en taux avec
    C_taux = C / N        et        ε_taux = ε / N
(γ ne change pas : les variables sont standardisées). N = lits de la source.

Rien du futur
-------------
En validation glissante, à chaque origine O, A n'utilise que les jours de la cible de cible ≤ O,
B et C que les jours de la source de cible ≤ O (et les jours de la cible ≤ O pour C) : au soir
du jour O, on ne connaît rien d'autre. La période de test final (le coffre) n'est lue qu'avec la
phrase de confirmation, comme dans validation_finale.py.

Total de l'hôpital
------------------
Le total des lits est la somme des services. Chaque stratégie donne une prévision par service ;
on additionne les MÉDIANES (prévisions centrales) jour par jour, la source étant prévue par son
propre modèle local. Attention : la somme des quantiles 80 % n'est pas le quantile 80 % de la
somme (les erreurs des services se compensent en partie) ; on ne note donc le total que sur
sa prévision centrale (MAE, biais), pas sur un quantile.

Exemples
--------
Développement (données verrouillées) :
    ~/memoire-env/bin/python transfert.py donnees/<export>.csv --source PED --cibles MEDF --horizons 1 7
(lits connus par défaut : PED=18, MEDF=17 ; un autre service s'ajoute avec --lits MEDH=<N>)
Test final, UNE fois à la fin :
    ~/memoire-env/bin/python transfert.py donnees/<export>.csv --source PED --cibles MEDF --extraction 2026-10-31 \
        --confirmation "J'ouvre le coffre pour la validation finale"

Sorties dans resultats/ : transfert_<CIBLE>_h<h>.csv, transfert_total_h<h>.csv, transfert.md
(tableaux et conclusions pour le mémoire), transfert_environnement.json.
"""
import argparse
import dataclasses
from pathlib import Path

import pandas as pd
import torch

from benchmark_choix import Dimension, en_markdown
from traitement.chargement import lire_export, periode_exploitable, preparer_sejours
from traitement.occupation import reconstituer_occupation
from traitement.verrou import DATE_VERROU
from svr import metriques as M
from svr import references as R
from svr.caracteristiques import Standardiseur, construire
from svr.niveaux import Hyperparametres, fabrique
from svr.reproductibilite import ecrire_environnement
from svr.validation import Decoupage, decoupage_final, origines_glissantes
from validation_finale import hyperparametres

TYPE = torch.float64
# Lits connus de chaque service (codes de l'outil de saisie, registres.js) ; --lits les remplace ou complète.
LITS_CONNUS = {"PED": 18, "MEDF": 17}   # PED : 20 installés, 18 opérationnels en pratique
GRANDEURS = ("presents", "admissions")       # + toutes les colonnes sorties_*, divisées par les lits


def occupation_du_service(df: pd.DataFrame, code: str, extraction) -> pd.DataFrame:
    """
    Occupation attendue d'un service, sur sa période exploitable, avec les réglages RETENUS pour toute la
    chaîne (lancer_tout.sh) : durées inconnues estimées (prix, issue), censure au p95 des durées, rodage
    compté depuis le premier jour d'enregistrement. Avec les réglages d'origine (durées inconnues exclues),
    un seul mois à moins de 90 % de durées connues repousserait le début de toute la série.
    """
    sejours, _ = preparer_sejours(df, code, extraction, "p95", "estimee")
    if sejours.empty:
        raise ValueError(f"Aucun séjour pour le service {code}.")
    periode = periode_exploitable(sejours, rodage_au_debut=True)
    return reconstituer_occupation(sejours, extraction, debut=periode["debut"], scenario="attendue")


def en_taux(occ: pd.DataFrame, lits: int) -> pd.DataFrame:
    """Présents, admissions et sorties divisés par le nombre de lits : des taux comparables entre services."""
    t = occ.copy()
    for c in [*GRANDEURS, *[c for c in occ.columns if c.startswith("sorties_")]]:
        t[c] = occ[c] / lits
    return t


def hp_en_taux(hp: Hyperparametres, lits: int) -> Hyperparametres:
    """C/N et ε/N : le même modèle, exprimé en taux (démonstration dans l'en-tête)."""
    return dataclasses.replace(hp, C=hp.C / lits, epsilon=hp.epsilon / lits, epsilon_quantile=hp.epsilon_quantile / lits)


def multiplier(prevision, facteur: float):
    """Remet une prévision en nombre de patients (tenseur, ou dict {τ: tenseur})."""
    if isinstance(prevision, dict):
        return {t: v * facteur for t, v in prevision.items()}
    return prevision * facteur


def entrainer_predire(fab, X_entr, y_entr, X_pred, continues):
    """Standardisation apprise sur l'entraînement seul, puis entraînement et prévision."""
    std = Standardiseur(continues).ajuster(X_entr)
    return fab().entrainer(std.transformer(X_entr), y_entr).predire(std.transformer(X_pred))


GRILLE_PROPRE = {"C": (0.3, 1.0, 3.0), "portee": (0.5, 1.0, 2.0)}   # multiplicateurs des réglages de la source


def score(y, prevision, tau: float) -> float:
    """Critère de choix des réglages : pinball au quantile τ (prévision quantile), sinon MAE."""
    if isinstance(prevision, dict):
        return M.pinball_moyenne(y, prevision[tau], tau)
    return M.mae(y, prevision)


def regler_sur_la_cible(niveau: int, hp: Hyperparametres, tab, entrainement: torch.Tensor, origine: pd.Timestamp,
                        validation_interne: int, minimum: int) -> tuple[Hyperparametres, str]:
    """
    Recherche par grille des réglages du modèle propre, avec les seules lignes d'`entrainement`
    (connues au soir de `origine`) : apprentissage interne sur les cibles ≤ origine − v, évaluation
    sur les origines de ]origine − v, origine]. Renvoie les réglages gagnants et leur étiquette
    (« ×1 / ×1 » = réglages de la source).
    """
    o_int = origine - pd.Timedelta(days=validation_interne)
    idx = entrainement.numpy()
    cibles, origines = tab.dates_cible[idx], tab.dates_origine[idx]
    i_app = entrainement[torch.tensor(cibles <= o_int)]
    i_val = entrainement[torch.tensor(origines > o_int)]
    if len(i_app) < minimum or len(i_val) == 0:
        return hp, "source (fenêtre interne trop courte)"
    meilleur, etiquette, s_min = hp, "×1 / ×1", None
    for mc in GRILLE_PROPRE["C"]:
        for mg in GRILLE_PROPRE["portee"]:
            essai = dataclasses.replace(hp, C=hp.C * mc, gamma=hp.gamma * mg, gamma1=hp.gamma1 * mg, gamma2=hp.gamma2 * mg)
            prev = entrainer_predire(fabrique(niveau, essai, tab.blocs), tab.X[i_app], tab.y[i_app], tab.X[i_val], tab.continues)
            sc = score(tab.y[i_val], prev, hp.tau)
            source = mc == 1.0 and mg == 1.0
            # strictement meilleur, ou réglages de la source à égalité
            if s_min is None or sc < s_min - 1e-12 or (source and abs(sc - s_min) <= 1e-12):
                meilleur, s_min = essai, sc
                etiquette = f"C ×{mc:g} / portée ×{mg:g}".replace(".", ",")
    return meilleur, etiquette


def avec_service(tab, services: list[str], code: str):
    """
    Ajoute au tableau d'un service ses variables indicatrices (une colonne 0/1 par service, 1 pour `code`),
    pour le modèle unique G. Elles ne sont pas standardisées et entrent dans le bloc « flux et saison » du
    noyau composite : deux jours de services différents se ressemblent moins que deux jours du même service.
    """
    ind = torch.zeros(len(tab.y), len(services), dtype=tab.X.dtype)
    ind[:, services.index(code)] = 1.0
    d = tab.X.shape[1]
    blocs = {**tab.blocs, "flux_saison": [*tab.blocs.get("flux_saison", []), *range(d, d + len(services))]}
    return dataclasses.replace(tab, X=torch.cat([tab.X, ind], dim=1), noms=[*tab.noms, *(f"service_{c}" for c in services)],
                               blocs=blocs)


def lignes_connues(tab, origine: pd.Timestamp, final: bool, debut: pd.Timestamp | None = None) -> torch.Tensor:
    """Lignes d'un tableau connues au soir de `origine` (cible ≤ origine ; < verrou au test final), à partir de `debut`."""
    connus = (tab.dates_cible < origine) if final else (tab.dates_cible <= origine)
    if debut is not None:
        connus = connus & (tab.dates_origine >= debut)
    return torch.nonzero(torch.tensor(connus)).flatten()


def concatener(morceaux):
    """Recolle les prévisions des origines successives (tenseurs ou dict {τ: tenseur})."""
    if isinstance(morceaux[0], dict):
        return {t: torch.cat([m[t] for m in morceaux]) for t in morceaux[0]}
    return torch.cat(morceaux)


def main() -> None:
    p = argparse.ArgumentParser(description="Transfert de la méthode vers des services à historique court.")
    p.add_argument("export")
    p.add_argument("--source", default="PED", help="service source, à long historique (PED)")
    p.add_argument("--cibles", nargs="+", required=True, help="services cibles, à fenêtre courte")
    p.add_argument("--lits", nargs="+", default=[], help="lits de chaque service : PED=20 MEDH=… (connus par défaut : "
                   + ", ".join(f"{k}={v}" for k, v in LITS_CONNUS.items()) + ")")
    p.add_argument("--horizons", type=int, nargs="+", default=[1, 7])
    p.add_argument("--tau", type=float, default=0.8)
    p.add_argument("--niveau", type=int, default=4, choices=[1, 2, 3, 4], help="niveau de modèle transféré (4)")
    p.add_argument("--pas", type=int, default=14)
    p.add_argument("--minimum-entrainement", type=int, default=28,
                   help="jours d'entraînement de la cible au minimum avant la première origine (28)")
    p.add_argument("--poids-cible", type=int, default=1, help="stratégie C : nombre de fois où chaque jour de la cible compte (1)")
    p.add_argument("--validation-interne", type=int, default=56,
                   help="modèle propre : jours de la validation interne qui choisit ses réglages (56)")
    p.add_argument("--extraction", help="test final : date du relevé du registre (aaaa-mm-jj)")
    p.add_argument("--confirmation", help="test final : phrase d'ouverture du coffre")
    a = p.parse_args()

    lits = LITS_CONNUS | {k: int(v) for k, v in (x.split("=") for x in a.lits)}
    manquants = [s for s in [a.source, *a.cibles] if s not in lits]
    if manquants:
        raise SystemExit(f"Nombre de lits manquant pour : {', '.join(manquants)} (option --lits).")
    final = a.confirmation is not None
    if final and not a.extraction:
        raise SystemExit("Le test final demande --extraction (date du relevé).")
    resultats = Path("resultats"); resultats.mkdir(exist_ok=True)
    ecrire_environnement(resultats / "transfert_environnement.json", **{k: v for k, v in vars(a).items() if k != "confirmation"})

    df = lire_export(a.export, confirmation_coffre=a.confirmation) if final else lire_export(a.export)
    extraction = pd.Timestamp(a.extraction) if final else DATE_VERROU
    occs = {a.source: occupation_du_service(df, a.source, extraction)}
    for c in a.cibles:
        occs[c] = occupation_du_service(df, c, extraction)
        print(f"{c} : occupation exploitable du {occs[c].index.min():%d/%m/%Y} au {occs[c].index.max():%d/%m/%Y}")
    N_s = lits[a.source]
    rapport = [f"# Transfert de la méthode — source {a.source} vers {', '.join(a.cibles)}\n",
               ("**Test final sur le coffre** (septembre–octobre 2026)." if final else
                "Validation glissante sur la fenêtre de chaque service cible (données verrouillées).")
               + f" Niveau du modèle : {a.niveau}. « (retenu) » = stratégie P (modèle propre, réglages choisis sur le service),"
               " référence du test de Diebold-Mariano.\n"]

    for h in a.horizons:
        print(f"\n══════ Horizon J+{h}")
        chemin = resultats / f"hyperparametres_{a.source}_h{h}.json"
        if chemin.exists():
            hp = hyperparametres(chemin)[a.niveau]
        else:
            print(f"  ({chemin.name} absent : hyperparamètres par défaut — lancez d'abord lancer_niveaux.py sur {a.source})")
            hp = Hyperparametres(tau=a.tau)
        hp_taux = hp_en_taux(hp, N_s)
        tab_s = construire(en_taux(occs[a.source], N_s), h)
        # Modèle unique G : tableaux en taux de TOUS les services, avec l'indicatrice du service.
        services = [a.source, *a.cibles]
        tabs_g = {c: avec_service(construire(en_taux(occs[c], lits[c]), h), services, c) for c in services}
        debut_commun = max(occs[c].index.min() for c in services)          # premier jour où tous les services ont des données
        totaux = {}                                              # stratégie → {service → Series par date}
        # Mêmes origines pour tous les services (indispensable pour additionner les prévisions au total) :
        # la première origine laisse `minimum_entrainement` jours à la cible qui démarre le plus tard.
        debut_val = max(occs[c].index.min() for c in a.cibles) + pd.Timedelta(days=a.minimum_entrainement + h + 7)

        for cible in a.cibles:
            N_c = lits[cible]
            tab_c = construire(occs[cible], h)                  # en nombre (stratégie A, persistance)
            tab_ct = construire(en_taux(occs[cible], N_c), h)   # en taux (stratégies B et C)
            if final:
                decs = [decoupage_final(tab_c, DATE_VERROU)]
            else:
                decs = origines_glissantes(tab_c, debut_val, DATE_VERROU, pas=a.pas, minimum_entrainement=a.minimum_entrainement)

            y = torch.cat([tab_c.y[d.evaluation] for d in decs])
            orig = torch.cat([tab_c.origines[d.evaluation] for d in decs])
            dates = pd.DatetimeIndex([dt for d in decs for dt in tab_c.dates_cible[d.evaluation.numpy()]])
            previsions = {"Persistance de la cible": R.persistance(tab_c.serie, orig, h)}
            nom_p = "P · modèle propre (cible seule, réglages choisis sur la cible)"
            nom_g1 = f"G1 · modèle unique, période commune (dès le {debut_commun:%d/%m/%Y})"
            nom_g2 = "G2 · modèle unique, toute la période de chaque service"
            morceaux = {nom_p: [], "A · local (cible seule, réglages de la source gelés)": [],
                        "B · transfert direct (source seule, en taux)": [],
                        f"C · groupé (source + cible ×{a.poids_cible}, en taux)": [], nom_g1: [], nom_g2: []}
            noms = list(morceaux)[1:4]
            choix_propre = []
            for d in decs:
                # Jours de la source connus au soir de l'origine (cible ≤ O ; < verrou au test final).
                connus = tab_s.dates_cible < d.origine if final else tab_s.dates_cible <= d.origine
                i_s = torch.nonzero(torch.tensor(connus)).flatten()
                Xs, ys = tab_s.X[i_s], tab_s.y[i_s]
                Xc, yc = tab_ct.X[d.entrainement].repeat(a.poids_cible, 1), tab_ct.y[d.entrainement].repeat(a.poids_cible)
                hp_p, etiq = regler_sur_la_cible(a.niveau, hp, tab_c, d.entrainement, d.origine, a.validation_interne,
                                                 a.minimum_entrainement)
                choix_propre.append(etiq)
                morceaux[nom_p].append(entrainer_predire(fabrique(a.niveau, hp_p, tab_c.blocs), tab_c.X[d.entrainement],
                                                         tab_c.y[d.entrainement], tab_c.X[d.evaluation], tab_c.continues))
                morceaux[noms[0]].append(entrainer_predire(fabrique(a.niveau, hp, tab_c.blocs), tab_c.X[d.entrainement],
                                                           tab_c.y[d.entrainement], tab_c.X[d.evaluation], tab_c.continues))
                morceaux[noms[1]].append(multiplier(entrainer_predire(fabrique(a.niveau, hp_taux, tab_s.blocs), Xs, ys,
                                                                      tab_ct.X[d.evaluation], tab_s.continues), N_c))
                morceaux[noms[2]].append(multiplier(entrainer_predire(fabrique(a.niveau, hp_taux, tab_s.blocs),
                                                                      torch.cat([Xs, Xc]), torch.cat([ys, yc]),
                                                                      tab_ct.X[d.evaluation], tab_s.continues), N_c))
                # Modèle unique : tous les services, jours connus au soir de l'origine (G1 : période commune seulement).
                tg = tabs_g[cible]
                for nom_g, debut in ((nom_g1, debut_commun), (nom_g2, None)):
                    idx = {c: lignes_connues(tabs_g[c], d.origine, final, debut) for c in services}
                    idx[cible] = d.entrainement if debut is None else d.entrainement[torch.tensor(tg.dates_origine[d.entrainement.numpy()] >= debut)]
                    Xg = torch.cat([tabs_g[c].X[idx[c]] for c in services])
                    yg = torch.cat([tabs_g[c].y[idx[c]] for c in services])
                    morceaux[nom_g].append(multiplier(entrainer_predire(fabrique(a.niveau, hp_taux, tg.blocs), Xg, yg,
                                                                        tg.X[d.evaluation], tg.continues), N_c))
            for nom, m in morceaux.items():
                previsions[nom] = concatener(m)

            dim = Dimension(cible, f"Service {cible} ({N_c} lits)", "Quelle stratégie prévoit le mieux un service à historique court ?", h, a.tau)
            for nom, prev in previsions.items():
                dim.ajouter(nom, y, prev, 0.0, retenu=nom.startswith("P ·"))
                totaux.setdefault(nom, {})[cible] = pd.Series(point_de(prev).numpy(), index=dates)
            totaux.setdefault("_vrai", {})[cible] = pd.Series(y.numpy(), index=dates)
            t = dim.tableau().drop(columns=["temps (s)"])
            print(f"\n── {cible} · {len(y)} jours évalués, {len(decs)} origine(s)\n{t.to_string()}")
            t.to_csv(resultats / f"transfert_{cible}_h{h}.csv", sep=";", encoding="utf-8-sig")
            frequences = pd.Series(choix_propre).value_counts()
            stab = ", ".join(f"{k} : {v}" for k, v in frequences.items())
            print(f"   réglages du modèle propre (nombre d'origines) : {stab}")
            rapport.extend([f"\n## Horizon J+{h} · service {cible} ({N_c} lits, {len(y)} jours évalués)\n",
                            en_markdown(t), "\n", dim.conclusion(t), "\n",
                            f"\nRéglages choisis par le modèle propre, sur {len(decs)} origine(s) : {stab}. "
                            "Un même choix à presque toutes les origines = réglage stable ; des choix qui changent sans cesse = "
                            "trop peu de jours pour régler, préférer la stratégie A.\n"])

        # ── Total de l'hôpital : somme des prévisions centrales des services, sur les jours communs ─
        if a.source not in totaux.get("_vrai", {}):
            tab_src = construire(occs[a.source], h)
            jours_cibles = sorted(set.intersection(*(set(s.index) for s in totaux["_vrai"].values())))
            if jours_cibles:
                # La source est prévue par son propre modèle local, réentraîné aux MÊMES origines que
                # les cibles (un entraînement par origine, pas un par jour).
                decs_src = ([decoupage_final(tab_src, DATE_VERROU)] if final
                            else origines_glissantes(tab_src, debut_val, DATE_VERROU, pas=a.pas))
                prev_src = torch.cat([point_de(entrainer_predire(fabrique(a.niveau, hp, tab_src.blocs), tab_src.X[d.entrainement],
                                                                 tab_src.y[d.entrainement], tab_src.X[d.evaluation], tab_src.continues))
                                      for d in decs_src]).tolist()
                vrai_src = torch.cat([tab_src.y[d.evaluation] for d in decs_src]).tolist()
                jours_src = [dt for d in decs_src for dt in tab_src.dates_cible[d.evaluation.numpy()]]
                lignes = []
                vrai = sum(totaux["_vrai"][c].reindex(jours_cibles) for c in a.cibles) + pd.Series(vrai_src, index=jours_src).reindex(jours_cibles)
                for nom in [n for n in totaux if n != "_vrai"]:
                    prev = sum(totaux[nom][c].reindex(jours_cibles) for c in a.cibles) + pd.Series(prev_src, index=jours_src).reindex(jours_cibles)
                    ok = vrai.notna() & prev.notna()
                    yv, pv = torch.tensor(vrai[ok].to_numpy(), dtype=TYPE), torch.tensor(prev[ok].to_numpy(), dtype=TYPE)
                    lignes.append({"stratégie (services cibles)": nom, "jours": int(ok.sum()),
                                   "MAE total (lits)": round(M.mae(yv, pv), 3), "biais total": round(M.biais(yv, pv), 3)})
                tt = pd.DataFrame(lignes).set_index("stratégie (services cibles)")
                print(f"\n── Total de l'hôpital ({a.source} + {' + '.join(a.cibles)}) : {sum(lits[s] for s in [a.source, *a.cibles])} lits\n{tt.to_string()}")
                tt.to_csv(resultats / f"transfert_total_h{h}.csv", sep=";", encoding="utf-8-sig")
                rapport.extend([f"\n## Horizon J+{h} · total de l'hôpital ({a.source} + {' + '.join(a.cibles)})\n", en_markdown(tt),
                                "\nSomme des prévisions centrales (médianes) ; la source est prévue par son modèle local.\n"])

    (resultats / "transfert.md").write_text("\n".join(rapport), encoding="utf-8")
    print(f"\nTableaux écrits dans {resultats.resolve()} (transfert.md pour le mémoire)")


def point_de(prevision):
    """Prévision centrale : la médiane d'une prévision quantile, sinon la prévision elle-même."""
    return prevision[0.5] if isinstance(prevision, dict) else prevision


if __name__ == "__main__":
    main()
