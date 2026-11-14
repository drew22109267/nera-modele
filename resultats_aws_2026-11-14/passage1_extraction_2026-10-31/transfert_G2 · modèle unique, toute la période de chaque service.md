# Transfert de la méthode — source MEDF vers PED

**Test final sur le coffre** (septembre–octobre 2026). Niveau du modèle : 4. « (retenu) » = stratégie P (modèle propre, réglages choisis sur le service), référence du test de Diebold-Mariano.


## Horizon J+1 · service PED (18 lits, 59 jours évalués)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Persistance de la cible | 0.708 | 1.455 | 0.102 | 0.3234 |  | 0.0 | 0.0 | 0.0 | meilleur |
| P · modèle propre (cible seule, réglages choisis sur la cible) (retenu) | 3.365 | 3.945 | 2.875 | 1.0343 | 42.4 |  |  |  | — choix retenu |
| A · local (cible seule, réglages de la source gelés) | 4.338 | 5.259 | 3.77 | 1.2189 | 42.4 | 0.0 | 0.0 | 0.0 | moins bon |
| B · transfert direct (source seule, en taux) | 1.774 | 2.271 | 1.541 | 1.1884 | 33.9 | 0.0096 | 0.0096 | 0.0 | moins bon |
| C · groupé (source + cible ×1, en taux) | 2.788 | 3.226 | 2.621 | 1.75 | 86.4 | 0.0 | 0.0 | 0.1126 | moins bon |
| G1 · modèle unique, période commune (dès le 15/07/2025) | 2.144 | 2.571 | 1.906 | 0.9199 | 86.4 | 0.0004 | 0.0008 | 0.0001 | meilleur |
| G2 · modèle unique, toute la période de chaque service | 3.606 | 4.012 | 3.506 | 1.7334 | 93.2 | 0.0 | 0.0 | 0.4998 | moins bon |


Plus petite MAE : **Persistance de la cible** (0.708). ⚠ Significativement meilleur que le choix retenu : Persistance de la cible, G1 · modèle unique, période commune (dès le 15/07/2025) — le choix est à revoir.



Réglages choisis par le modèle propre, sur 1 origine(s) : C ×3 / portée ×0,5 : 1. Un même choix à presque toutes les origines = réglage stable ; des choix qui changent sans cesse = trop peu de jours pour régler, préférer la stratégie A.


## Horizon J+1 · total de l'hôpital (MEDF + PED)

| stratégie (services cibles) | jours | MAE total (lits) | biais total |
|---|---|---|---|
| Persistance de la cible | 59.0 | 2.838 | -0.156 |
| P · modèle propre (cible seule, réglages choisis sur la cible) | 59.0 | 4.596 | 2.617 |
| A · local (cible seule, réglages de la source gelés) | 59.0 | 5.658 | 3.512 |
| B · transfert direct (source seule, en taux) | 59.0 | 2.937 | 1.283 |
| C · groupé (source + cible ×1, en taux) | 59.0 | 3.334 | 2.363 |
| G1 · modèle unique, période commune (dès le 15/07/2025) | 59.0 | 3.148 | 1.648 |
| G2 · modèle unique, toute la période de chaque service | 59.0 | 3.902 | 3.248 |

Somme des prévisions centrales (médianes) ; la source est prévue par son modèle local.


## Horizon J+7 · service PED (18 lits, 53 jours évalués)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Persistance de la cible | 1.561 | 2.809 | 0.999 | 0.4806 |  | 0.0155 | 0.0155 | 0.0277 | meilleur |
| P · modèle propre (cible seule, réglages choisis sur la cible) (retenu) | 5.635 | 6.257 | 5.477 | 1.6899 | 34.0 |  |  |  | — choix retenu |
| A · local (cible seule, réglages de la source gelés) | 5.923 | 6.486 | 5.825 | 1.8267 | 35.8 | 0.0 | 0.0 | 0.0 | moins bon |
| B · transfert direct (source seule, en taux) | 7.808 | 8.193 | 7.808 | 2.1722 | 22.6 | 0.0 | 0.0 | 0.0 | moins bon |
| C · groupé (source + cible ×1, en taux) | 6.842 | 7.288 | 6.806 | 2.1416 | 37.7 | 0.0 | 0.0 | 0.0 | moins bon |
| G1 · modèle unique, période commune (dès le 15/07/2025) | 5.855 | 6.369 | 5.77 | 2.0248 | 35.8 | 0.0 | 0.0 | 0.2224 | moins bon |
| G2 · modèle unique, toute la période de chaque service | 7.04 | 7.536 | 7.002 | 2.1416 | 37.7 | 0.0 | 0.0 | 0.0 | moins bon |


Plus petite MAE : **Persistance de la cible** (1.561). ⚠ Significativement meilleur que le choix retenu : Persistance de la cible — le choix est à revoir.



Réglages choisis par le modèle propre, sur 1 origine(s) : C ×3 / portée ×2 : 1. Un même choix à presque toutes les origines = réglage stable ; des choix qui changent sans cesse = trop peu de jours pour régler, préférer la stratégie A.


## Horizon J+7 · total de l'hôpital (MEDF + PED)

| stratégie (services cibles) | jours | MAE total (lits) | biais total |
|---|---|---|---|
| Persistance de la cible | 53.0 | 5.003 | 0.651 |
| P · modèle propre (cible seule, réglages choisis sur la cible) | 53.0 | 6.986 | 5.129 |
| A · local (cible seule, réglages de la source gelés) | 53.0 | 7.023 | 5.477 |
| B · transfert direct (source seule, en taux) | 53.0 | 7.919 | 7.46 |
| C · groupé (source + cible ×1, en taux) | 53.0 | 7.373 | 6.458 |
| G1 · modèle unique, période commune (dès le 15/07/2025) | 53.0 | 6.884 | 5.422 |
| G2 · modèle unique, toute la période de chaque service | 53.0 | 7.613 | 6.654 |

Somme des prévisions centrales (médianes) ; la source est prévue par son modèle local.
