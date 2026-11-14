# Transfert de la méthode — source MEDF vers PED

**Test final sur le coffre** (septembre–octobre 2026). Niveau du modèle : 4. « (retenu) » = stratégie P (modèle propre, réglages choisis sur le service), référence du test de Diebold-Mariano.


## Horizon J+1 · service PED (18 lits, 28 jours évalués)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Persistance de la cible | 1.492 | 2.113 | 0.214 | 0.6815 |  | 0.326 | 0.5014 | 0.8931 | équivalent |
| P · modèle propre (cible seule, réglages choisis sur la cible) (retenu) | 1.515 | 2.072 | 0.482 | 0.5398 | 89.3 |  |  |  | — choix retenu |
| A · local (cible seule, réglages de la source gelés) | 1.47 | 2.058 | 0.273 | 0.5641 | 89.3 | 0.2507 | 0.5014 | 0.4827 | équivalent |
| B · transfert direct (source seule, en taux) | 2.175 | 2.748 | 1.684 | 1.0421 | 67.9 | 0.0 | 0.0 | 0.0026 | moins bon |
| C · groupé (source + cible ×1, en taux) | 3.212 | 3.737 | 2.859 | 1.1184 | 78.6 | 0.0 | 0.0 | 0.0 | moins bon |
| G1 · modèle unique, période commune (dès le 15/07/2025) | 2.333 | 2.906 | 1.83 | 0.5962 | 89.3 | 0.1307 | 0.3921 | 0.0009 | équivalent |
| G2 · modèle unique, toute la période de chaque service | 3.746 | 4.345 | 3.535 | 1.1206 | 92.9 | 0.0 | 0.0 | 0.0 | moins bon |


Plus petite MAE : **A · local (cible seule, réglages de la source gelés)** (1.47). Aucune variante ne bat significativement le choix retenu (P · modèle propre (cible seule, réglages choisis sur la cible) (retenu)).



Réglages choisis par le modèle propre, sur 1 origine(s) : C ×3 / portée ×0,5 : 1. Un même choix à presque toutes les origines = réglage stable ; des choix qui changent sans cesse = trop peu de jours pour régler, préférer la stratégie A.


## Horizon J+1 · total de l'hôpital (MEDF + PED)

| stratégie (services cibles) | jours | MAE total (lits) | biais total |
|---|---|---|---|
| Persistance de la cible | 28.0 | 3.179 | -1.914 |
| P · modèle propre (cible seule, réglages choisis sur la cible) | 28.0 | 2.891 | -1.646 |
| A · local (cible seule, réglages de la source gelés) | 28.0 | 2.998 | -1.855 |
| B · transfert direct (source seule, en taux) | 28.0 | 2.384 | -0.444 |
| C · groupé (source + cible ×1, en taux) | 28.0 | 2.413 | 0.732 |
| G1 · modèle unique, période commune (dès le 15/07/2025) | 28.0 | 2.479 | -0.298 |
| G2 · modèle unique, toute la période de chaque service | 28.0 | 2.612 | 1.408 |

Somme des prévisions centrales (médianes) ; la source est prévue par son modèle local.


## Horizon J+7 · service PED (18 lits, 22 jours évalués)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Persistance de la cible | 2.578 | 3.569 | 1.225 | 0.9215 |  | 0.7024 | 0.7024 | 0.8292 | équivalent |
| P · modèle propre (cible seule, réglages choisis sur la cible) (retenu) | 2.742 | 3.293 | 2.361 | 1.0532 | 81.8 |  |  |  | — choix retenu |
| A · local (cible seule, réglages de la source gelés) | 3.16 | 3.704 | 2.925 | 1.2209 | 86.4 | 0.0 | 0.0 | 0.0 | moins bon |
| B · transfert direct (source seule, en taux) | 5.522 | 5.987 | 5.522 | 1.6829 | 54.5 | 0.0 | 0.0 | 0.0 | moins bon |
| C · groupé (source + cible ×1, en taux) | 4.397 | 4.893 | 4.311 | 1.5786 | 90.9 | 0.0 | 0.0 |  | moins bon |
| G1 · modèle unique, période commune (dès le 15/07/2025) | 3.31 | 3.859 | 3.104 | 1.3241 | 86.4 | 0.0 | 0.0 | 0.0 | moins bon |
| G2 · modèle unique, toute la période de chaque service | 4.278 | 4.761 | 4.187 | 1.5786 | 90.9 | 0.0 | 0.0 |  | moins bon |


Plus petite MAE : **Persistance de la cible** (2.578). Aucune variante ne bat significativement le choix retenu (P · modèle propre (cible seule, réglages choisis sur la cible) (retenu)).



Réglages choisis par le modèle propre, sur 1 origine(s) : C ×3 / portée ×2 : 1. Un même choix à presque toutes les origines = réglage stable ; des choix qui changent sans cesse = trop peu de jours pour régler, préférer la stratégie A.


## Horizon J+7 · total de l'hôpital (MEDF + PED)

| stratégie (services cibles) | jours | MAE total (lits) | biais total |
|---|---|---|---|
| Persistance de la cible | 22.0 | 4.793 | -2.96 |
| P · modèle propre (cible seule, réglages choisis sur la cible) | 22.0 | 3.103 | -1.825 |
| A · local (cible seule, réglages de la source gelés) | 22.0 | 2.918 | -1.261 |
| B · transfert direct (source seule, en taux) | 22.0 | 2.896 | 1.336 |
| C · groupé (source + cible ×1, en taux) | 22.0 | 2.784 | 0.126 |
| G1 · modèle unique, période commune (dès le 15/07/2025) | 22.0 | 2.896 | -1.081 |
| G2 · modèle unique, toute la période de chaque service | 22.0 | 2.767 | 0.002 |

Somme des prévisions centrales (médianes) ; la source est prévue par son modèle local.
