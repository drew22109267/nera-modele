r"""
Recherche des hyperparamètres (protocole, étape 3.5) : grille grossière, puis essaim
particulaire (PSO), écrits à la main.

Les hyperparamètres (C, ε, γ…) ne s'apprennent pas par gradient : on les choisit en
comparant la qualité en validation glissante. `objectif(config) → score` (plus petit = meilleur)
entraîne et évalue un modèle pour une configuration.

1. Grille : on essaie toutes les combinaisons d'une liste de valeurs par paramètre.
   Simple et exhaustif, mais le nombre d'essais explose avec le nombre de paramètres.

2. Essaim particulaire (PSO, Kennedy & Eberhart, 1995)
   N « particules » explorent l'espace. Chaque particule i a une position x_i, une vitesse v_i,
   et retient la meilleure position qu'elle a trouvée (p_i) ; l'essaim retient la meilleure de
   toutes (g). À chaque itération :
       v_i ← ω v_i + c₁ r₁ (p_i − x_i) + c₂ r₂ (g − x_i)
       x_i ← x_i + v_i          (ramenée dans les bornes)
   ω (inertie) : garde la direction ; c₁ (mémoire) : retour vers son propre meilleur ;
   c₂ (social) : attraction vers le meilleur de l'essaim ; r₁, r₂ tirés uniformément dans [0, 1].
   Les paramètres positifs d'échelle très variable (C, γ) sont explorés en logarithme :
   on cherche log₁₀ C, si bien que 0,1 → 1 et 1 → 10 sont des pas de même taille.
   Le générateur aléatoire est fixé (graine) : la recherche est reproductible.
"""
from __future__ import annotations

import itertools
import math
import os
import pickle
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from multiprocessing import get_context

import torch


def nombre_processus() -> int:
    """Processus pour les recherches : NERA_PROCESSUS, sinon tous les cœurs."""
    return max(1, int(os.environ.get("NERA_PROCESSUS", os.cpu_count() or 1)))


def _appeler(args):
    objectif, config = args
    torch.set_num_threads(1)                    # un fil par processus : les essais tournent côte à côte
    os.environ["NERA_PROCESSUS"] = "1"          # pas de nouveaux processus à l'intérieur d'un essai
    return objectif(config)


def _transmissible(objet) -> bool:
    try:
        pickle.dumps(objet)
        return True
    except Exception:                           # fonction locale, lambda… : on reste en série
        return False


def evaluer_configs(objectif, configs: list[dict], processus: int | None = None) -> list[float]:
    """
    Score de chaque configuration, dans l'ordre. Les essais sont indépendants : avec plusieurs processus,
    ils tournent en parallèle (même résultat qu'en série). `objectif` doit alors pouvoir être transmis à un
    autre processus (fonction ou objet défini au niveau d'un module, pas une fonction locale) ; sinon, série.
    """
    processus = nombre_processus() if processus is None else max(1, int(processus))
    if processus > 1 and len(configs) > 1 and _transmissible(objectif):
        with ProcessPoolExecutor(min(processus, len(configs)), mp_context=get_context("spawn")) as ex:
            return list(ex.map(_appeler, [(objectif, c) for c in configs]))
    return [objectif(c) for c in configs]


def recherche_grille(espace: dict[str, list], objectif, processus: int | None = None) -> dict:
    """Essaie chaque combinaison (en parallèle si possible). Renvoie la meilleure et le tableau de tous les essais."""
    noms = list(espace)
    configs = [dict(zip(noms, valeurs)) for valeurs in itertools.product(*(espace[n] for n in noms))]
    essais = [{**c, "score": s} for c, s in zip(configs, evaluer_configs(objectif, configs, processus))]
    meilleur = min(essais, key=lambda e: e["score"])
    return {"meilleur": meilleur, "essais": essais}


@dataclass
class Dimension:
    bas: float
    haut: float
    echelle: str = "lin"      # 'lin' ou 'log' (log₁₀)
    entier: bool = False

    def vers_valeur(self, u: float) -> float:
        """u ∈ [0, 1] → valeur réelle du paramètre."""
        if self.echelle == "log":
            v = 10 ** (math.log10(self.bas) + u * (math.log10(self.haut) - math.log10(self.bas)))
        else:
            v = self.bas + u * (self.haut - self.bas)
        return round(v) if self.entier else v


def essaim_particulaire(espace: dict[str, Dimension], objectif, particules: int = 12, iterations: int = 20,
                        omega: float = 0.7, c1: float = 1.5, c2: float = 1.5, graine: int = 0,
                        processus: int | None = None) -> dict:
    """PSO dans le cube [0, 1]^d, chaque coordonnée étant convertie par sa Dimension."""
    gen = torch.Generator().manual_seed(graine)
    noms, d = list(espace), len(espace)

    def config(x: torch.Tensor) -> dict:
        return {n: espace[n].vers_valeur(float(x[k])) for k, n in enumerate(noms)}

    x = torch.rand(particules, d, generator=gen, dtype=torch.float64)
    v = (torch.rand(particules, d, generator=gen, dtype=torch.float64) - 0.5) * 0.2
    scores = torch.tensor(evaluer_configs(objectif, [config(x[i]) for i in range(particules)], processus),
                          dtype=torch.float64)
    p, p_score = x.clone(), scores.clone()
    g_index = int(torch.argmin(p_score))
    g, g_score = p[g_index].clone(), float(p_score[g_index])
    historique = [g_score]

    for _ in range(iterations):
        r1 = torch.rand(particules, d, generator=gen, dtype=torch.float64)
        r2 = torch.rand(particules, d, generator=gen, dtype=torch.float64)
        v = omega * v + c1 * r1 * (p - x) + c2 * r2 * (g - x)
        x = torch.clamp(x + v, 0.0, 1.0)
        # Les particules d'une itération sont indépendantes (g ne sert qu'à l'itération suivante) : évaluées
        # ensemble, puis mises à jour dans l'ordre, comme en série.
        for i, s in enumerate(evaluer_configs(objectif, [config(x[i]) for i in range(particules)], processus)):
            if s < p_score[i]:
                p[i], p_score[i] = x[i].clone(), s
                if s < g_score:
                    g, g_score = x[i].clone(), s
        historique.append(g_score)
    return {"meilleur": {**config(g), "score": g_score}, "historique": historique}
