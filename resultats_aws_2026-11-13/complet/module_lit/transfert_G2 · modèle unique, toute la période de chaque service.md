# Transfert de la méthode — source MEDF vers PED

Validation glissante sur la fenêtre de chaque service cible (données verrouillées). Niveau du modèle : 4. « (retenu) » = stratégie P (modèle propre, réglages choisis sur le service), référence du test de Diebold-Mariano.


## Horizon J+1 · service PED (18 lits, 376 jours évalués)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Persistance de la cible | 2.26 | 2.892 | 0.003 | 1.129 |  | 0.0 | 0.0 | 0.0 | moins bon |
| P · modèle propre (cible seule, réglages choisis sur la cible) (retenu) | 1.862 | 2.377 | 0.395 | 0.6982 | 88.3 |  |  |  | — choix retenu |
| A · local (cible seule, réglages de la source gelés) | 1.894 | 2.391 | 0.348 | 0.719 | 88.3 | 0.034 | 0.0394 | 0.1919 | moins bon |
| B · transfert direct (source seule, en taux) | 2.41 | 2.97 | 1.072 | 0.8563 | 83.8 | 0.0 | 0.0 | 0.0 | moins bon |
| C · groupé (source + cible ×1, en taux) | 2.435 | 3.019 | 1.019 | 0.8014 | 87.8 | 0.0 | 0.0 | 0.0 | moins bon |
| G1 · modèle unique, période commune (dès le 15/07/2025) | 2.223 | 2.807 | 0.226 | 0.7514 | 87.8 | 0.0197 | 0.0394 | 0.0 | moins bon |
| G2 · modèle unique, toute la période de chaque service | 2.489 | 3.083 | 1.119 | 0.7847 | 87.8 | 0.0 | 0.0 | 0.0 | moins bon |


Plus petite MAE : **P · modèle propre (cible seule, réglages choisis sur la cible) (retenu)** (1.862). Aucune variante ne bat significativement le choix retenu (P · modèle propre (cible seule, réglages choisis sur la cible) (retenu)).



Réglages choisis par le modèle propre, sur 27 origine(s) : C ×3 / portée ×0,5 : 17, C ×3 / portée ×2 : 4, C ×3 / portée ×1 : 3, C ×1 / portée ×2 : 2, C ×1 / portée ×0,5 : 1. Un même choix à presque toutes les origines = réglage stable ; des choix qui changent sans cesse = trop peu de jours pour régler, préférer la stratégie A.


## Horizon J+1 · total de l'hôpital (MEDF + PED)

| stratégie (services cibles) | jours | MAE total (lits) | biais total |
|---|---|---|---|
| Persistance de la cible | 334.0 | 3.378 | -0.82 |
| P · modèle propre (cible seule, réglages choisis sur la cible) | 334.0 | 2.988 | -0.504 |
| A · local (cible seule, réglages de la source gelés) | 334.0 | 3.009 | -0.525 |
| B · transfert direct (source seule, en taux) | 334.0 | 3.305 | 0.139 |
| C · groupé (source + cible ×1, en taux) | 334.0 | 3.454 | 0.246 |
| G1 · modèle unique, période commune (dès le 15/07/2025) | 334.0 | 3.29 | -0.626 |
| G2 · modèle unique, toute la période de chaque service | 334.0 | 3.413 | 0.358 |

Somme des prévisions centrales (médianes) ; la source est prévue par son modèle local.


## Horizon J+7 · service PED (18 lits, 364 jours évalués)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Persistance de la cible | 3.928 | 4.972 | 0.107 | 1.9318 |  | 0.0003 | 0.0018 | 0.0447 | moins bon |
| P · modèle propre (cible seule, réglages choisis sur la cible) (retenu) | 3.442 | 4.156 | 1.007 | 1.1921 | 84.6 |  |  |  | — choix retenu |
| A · local (cible seule, réglages de la source gelés) | 3.461 | 4.237 | 1.023 | 1.2134 | 86.0 | 0.3377 | 1.0 | 0.7848 | équivalent |
| B · transfert direct (source seule, en taux) | 3.615 | 4.473 | 2.051 | 1.2209 | 88.5 | 0.5494 | 1.0 | 0.4083 | équivalent |
| C · groupé (source + cible ×1, en taux) | 3.494 | 4.278 | 1.526 | 1.2288 | 87.9 | 0.3004 | 1.0 | 0.6883 | équivalent |
| G1 · modèle unique, période commune (dès le 15/07/2025) | 3.404 | 4.159 | 0.49 | 1.1301 | 88.7 | 0.047 | 0.235 | 0.7266 | équivalent |
| G2 · modèle unique, toute la période de chaque service | 3.49 | 4.271 | 1.515 | 1.1994 | 87.9 | 0.7864 | 1.0 | 0.7139 | équivalent |


Plus petite MAE : **G1 · modèle unique, période commune (dès le 15/07/2025)** (3.404). Aucune variante ne bat significativement le choix retenu (P · modèle propre (cible seule, réglages choisis sur la cible) (retenu)).



Réglages choisis par le modèle propre, sur 26 origine(s) : C ×3 / portée ×2 : 10, C ×0,3 / portée ×0,5 : 10, C ×3 / portée ×1 : 3, C ×1 / portée ×2 : 1, C ×0,3 / portée ×1 : 1, C ×0,3 / portée ×2 : 1. Un même choix à presque toutes les origines = réglage stable ; des choix qui changent sans cesse = trop peu de jours pour régler, préférer la stratégie A.


## Horizon J+7 · total de l'hôpital (MEDF + PED)

| stratégie (services cibles) | jours | MAE total (lits) | biais total |
|---|---|---|---|
| Persistance de la cible | 322.0 | 5.248 | -0.818 |
| P · modèle propre (cible seule, réglages choisis sur la cible) | 322.0 | 4.497 | -0.246 |
| A · local (cible seule, réglages de la source gelés) | 322.0 | 4.682 | -0.195 |
| B · transfert direct (source seule, en taux) | 322.0 | 4.81 | 1.083 |
| C · groupé (source + cible ×1, en taux) | 322.0 | 4.669 | 0.354 |
| G1 · modèle unique, période commune (dès le 15/07/2025) | 322.0 | 4.79 | -0.494 |
| G2 · modèle unique, toute la période de chaque service | 322.0 | 4.67 | 0.349 |

Somme des prévisions centrales (médianes) ; la source est prévue par son modèle local.
