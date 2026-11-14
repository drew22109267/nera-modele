# Banc de comparaison du prétraitement — service MEDF

Une décision change à la fois ; « (retenu) » = choix retenu. MAE « propre » : contre la série de la variante ; MAE « retenue » : contre la série du choix retenu, mêmes jours pour toutes les variantes. Diebold-Mariano (perte pinball au quantile τ=0.8, correction HLN) contre la série retenue, puis correction de Holm sur les variantes d'une même dimension ; la p-valeur sur la MAE reste affichée.


## Horizon J+1


### P1 · Durées inconnues

183 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Exclure les séjours sans durée | 15/07/2025 | 0 | 8.74 | 51.4 | -0.4 | 2.148 | 0.7766 | -17.0 | 2.205 | 3.5 | 0.8218 | 0.0029 | 0.0261 | 0.0094 | moins bon |
| Médiane du service | 15/07/2025 | 0 | 9.73 | 57.3 | -3.5 | 2.035 | 0.7504 | -11.5 | 2.031 | 3.7 | 0.743 | 0.0096 | 0.0576 | 0.735 | équivalent |
| Moyenne du service | 15/07/2025 | 0 | 10.06 | 59.2 | -0.2 | 2.015 | 0.754 | -11.1 | 2.016 | 4.1 | 0.7488 | 0.006 | 0.048 | 0.4793 | moins bon |
| Médiane de la tranche d'âge | 15/07/2025 | 0 | 9.73 | 57.3 | -3.5 | 2.035 | 0.7504 | -11.5 | 2.031 | 6.8 | 0.743 | 0.0096 | 0.0576 | 0.735 | équivalent |
| Estimée : prix, puis issue, puis médiane (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.037 | 0.7217 | -13.5 | 2.037 | 5.3 | 0.7217 |  |  |  | — choix retenu |
| k plus proches voisins (prix, âge, sexe, issue, mois) | 15/07/2025 | 0 | 9.75 | 57.3 | -3.4 | 2.047 | 0.7406 | -13.3 | 2.015 | 3.4 | 0.7244 | 0.6626 | 1.0 | 0.0185 | équivalent |
| Régressions enchaînées (ridge, principe de MICE) | 15/07/2025 | 0 | 9.75 | 57.3 | -3.4 | 2.042 | 0.7391 | -13.8 | 2.042 | 4.1 | 0.7391 | 0.0003 | 0.0033 | 0.1505 | moins bon |
| Loi normale multivariée par EM | 15/07/2025 | 0 | 9.74 | 57.3 | -3.4 | 2.046 | 0.7375 | -14.0 | 2.046 | 6.3 | 0.7375 | 0.0006 | 0.006 | 0.0646 | moins bon |
| ACP itérative (rang faible) | 15/07/2025 | 0 | 9.62 | 56.6 | -4.3 | 2.037 | 0.7454 | -11.6 | 1.963 | 14.2 | 0.7158 | 0.5691 | 1.0 | 0.005 | équivalent |
| SoftImpute (norme nucléaire) | 15/07/2025 | 0 | 9.75 | 57.3 | -3.4 | 2.016 | 0.7512 | -11.9 | 2.024 | 9.0 | 0.7445 | 0.0061 | 0.048 | 0.451 | moins bon |
| XGBoost (avec le diagnostic) | 15/07/2025 | 0 | 9.7 | 57.0 | -3.8 | 2.058 | 0.7208 | -16.2 | 2.056 | 24.8 | 0.7125 | 0.1144 | 0.3432 | 0.1371 | équivalent |
| Hybride : prix, sinon XGBoost | 15/07/2025 | 0 | 9.7 | 57.0 | -3.8 | 2.044 | 0.7188 | -15.4 | 2.047 | 24.6 | 0.7134 | 0.0385 | 0.154 | 0.3997 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Estimée : prix, puis issue, puis médiane (retenu)).



### P2 · Fenêtre de censure (encore hospitalisé)

183 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 14 jours | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.037 | 0.7217 | -13.5 | 2.037 | 6.2 | 0.7217 |  |  |  | identique |
| 30 jours | 15/07/2025 | 0 | 9.79 | 57.6 | -3.6 | 2.04 | 0.7292 | -13.3 | 2.042 | 5.8 | 0.7183 | 0.4538 | 0.9076 | 0.6867 | équivalent |
| p95 des durées connues (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.037 | 0.7217 | -13.5 | 2.037 | 6.3 | 0.7217 |  |  |  | — choix retenu |
| 60 jours | 15/07/2025 | 0 | 9.94 | 58.5 | -3.5 | 2.063 | 0.7377 | -15.3 | 2.084 | 7.3 | 0.7285 | 0.6359 | 0.9076 | 0.2354 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (p95 des durées connues (retenu)).



### P3 · Convention du nombre de jours

183 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Attendue (nuit incertaine = 1 − p) (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.037 | 0.7217 | -13.5 | 2.037 | 5.2 | 0.7217 |  |  |  | — choix retenu |
| Tout inclusif (borne basse) | 15/07/2025 | 0 | 9.07 | 53.4 | -6.5 | 2.087 | 0.7582 | -18.6 | 2.146 | 5.6 | 0.7851 | 0.0127 | 0.0254 | 0.053 | moins bon |
| Tout en nuits (borne haute) | 15/07/2025 | 0 | 10.36 | 60.9 | 2.1 | 2.006 | 0.6795 | -8.6 | 2.014 | 7.6 | 0.6788 | 0.0321 | 0.0321 | 0.6097 | meilleur |


Significativement meilleur que le choix retenu : Tout en nuits (borne haute) — à revoir.



### P4 · Patients « Ancien » reportés

183 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Garder toutes les lignes (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.037 | 0.7217 | -13.5 | 2.037 | 6.7 | 0.7217 |  |  |  | — choix retenu |
| Fusionner les reports confirmés | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.037 | 0.7217 | -13.5 | 2.037 | 6.1 | 0.7217 |  |  |  | identique |


Aucune variante ne fait significativement mieux que le choix retenu (Garder toutes les lignes (retenu)).



### P5 · Période exploitable

183 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Durées connues ≥ 80 % | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.037 | 0.7217 | -13.5 | 2.037 | 5.6 | 0.7217 |  |  |  | identique |
| Durées connues ≥ 90 % (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.037 | 0.7217 | -13.5 | 2.037 | 6.2 | 0.7217 |  |  |  | — choix retenu |
| Durées connues ≥ 95 % | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.037 | 0.7217 | -13.5 | 2.037 | 5.7 | 0.7217 |  |  |  | identique |
| ≥ 90 %, sans rodage au début (premier mois = début réel du registre) | 01/07/2025 | 0 | 9.43 | 55.5 | -4.1 | 2.087 | 0.7535 | -16.3 | 2.087 | 6.1 | 0.7535 | 0.0005 | 0.0005 | 0.0394 | moins bon |


Aucune variante ne fait significativement mieux que le choix retenu (Durées connues ≥ 90 % (retenu)).



### P6 · Fin de série (délai d'inscription)

176 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Aucune coupe | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.046 | 0.725 | -14.2 | 2.046 | 4.8 | 0.725 |  |  |  | identique |
| 7 derniers jours retirés | 15/07/2025 | 7 | 9.71 | 57.1 | -3.7 | 2.046 | 0.725 | -14.2 | 2.046 | 5.8 | 0.725 |  |  |  | identique |
| p95 du délai d'inscription (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.046 | 0.725 | -14.2 | 2.046 | 6.0 | 0.725 |  |  |  | — choix retenu |


Aucune variante ne fait significativement mieux que le choix retenu (p95 du délai d'inscription (retenu)).



### P7 · Trous de saisie (≥ 4 jours sans admission)

183 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Gardés tels quels (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.037 | 0.7217 | -13.5 | 2.037 | 5.5 | 0.7217 |  |  |  | — choix retenu |
| Lignes d'apprentissage qui les touchent exclues | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.04 | 0.709 | -13.6 | 2.04 | 6.7 | 0.709 | 0.0098 | 0.0098 | 0.851 | meilleur |


Significativement meilleur que le choix retenu : Lignes d'apprentissage qui les touchent exclues — à revoir.



### P8 · Méthode de comptage des présents

183 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Recensement de minuit (nuits passées) (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.037 | 0.7217 | -13.5 | 2.037 | 5.9 | 0.7217 |  |  |  | — choix retenu |
| Présence dans la journée (jour de sortie compris) | 15/07/2025 | 0 | 12.27 | 72.2 | -2.8 | 2.28 | 0.865 | -7.2 | 2.535 | 4.8 | 0.8111 | 0.1017 | 0.1017 | 0.0022 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Recensement de minuit (nuits passées) (retenu)).



### P1 × modèles (J+1) : chaque méthode des durées inconnues avec chaque modèle

183 jours évalués ; tri par perte pinball τ=0.8 contre la série retenue.

| variante | imputation | modèle | famille | cle_imputation | cle_modele | pinball τ=0.8 retenue | MAE retenue | MAE propre | pinball τ=0.8 propre | temps (s) | DM p vs paire retenue | DM p vs imputation retenue, même modèle | p Holm vs paire retenue | vs paire retenue | p Holm vs imputation retenue, même modèle | vs imputation retenue, même modèle |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Loi normale multivariée par EM | A · forêt aléatoire quantile | concurrent | em | foret | 0.6015 | 1.869 | 1.869 | 0.6015 | 12.2 | 0.001 | 0.0191 | 0.114 | équivalent | 1.0 | équivalent |
| 1 | ACP itérative (rang faible) | A · forêt aléatoire quantile | concurrent | acp_iterative | foret | 0.6069 | 1.816 | 1.897 | 0.6089 | 11.5 | 0.0019 | 0.3838 | 0.1976 | équivalent | 1.0 | équivalent |
| 2 | Hybride : prix, sinon XGBoost | A · forêt aléatoire quantile | concurrent | hybride | foret | 0.6109 | 1.854 | 1.854 | 0.6196 | 13.3 | 0.0021 | 0.2125 | 0.2121 | équivalent | 1.0 | équivalent |
| 3 | Régressions enchaînées (ridge, principe de MICE) | A · forêt aléatoire quantile | concurrent | regression | foret | 0.6109 | 1.849 | 1.849 | 0.6109 | 11.1 | 0.0021 | 0.223 | 0.2121 | équivalent | 1.0 | équivalent |
| 4 | Hybride : prix, sinon XGBoost | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | hybride | lssvr_rbf | 0.6117 | 1.919 | 1.906 | 0.6205 | 0.4 | 0.0004 | 0.001 | 0.0468 | meilleur | 0.118 | équivalent |
| 5 | XGBoost (avec le diagnostic) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | xgboost | lssvr_rbf | 0.6117 | 1.918 | 1.91 | 0.6232 | 0.2 | 0.0005 | 0.0108 | 0.058 | équivalent | 1.0 | équivalent |
| 6 | XGBoost (avec le diagnostic) | A · forêt aléatoire quantile | concurrent | xgboost | foret | 0.6171 | 1.851 | 1.857 | 0.6248 | 9.9 | 0.0044 | 0.5811 | 0.4004 | équivalent | 1.0 | équivalent |
| 7 | Estimée : prix, puis issue, puis médiane | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | estimee | lssvr_rbf | 0.6224 | 1.907 | 1.907 | 0.6224 | 0.4 | 0.0013 |  | 0.1443 | équivalent |  | — référence |
| 8 | Estimée : prix, puis issue, puis médiane | A · forêt aléatoire quantile | concurrent | estimee | foret | 0.6229 | 1.9 | 1.9 | 0.6229 | 16.2 | 0.0048 |  | 0.4224 | équivalent |  | — référence |
| 9 | k plus proches voisins (prix, âge, sexe, issue, mois) | A · forêt aléatoire quantile | concurrent | knn | foret | 0.6237 | 1.841 | 1.878 | 0.6308 | 15.1 | 0.0043 | 0.9518 | 0.3956 | équivalent | 1.0 | équivalent |
| 10 | Moyenne du service | A · forêt aléatoire quantile | concurrent | moyenne | foret | 0.6238 | 1.851 | 1.844 | 0.6048 | 16.5 | 0.0084 | 0.9631 | 0.6552 | équivalent | 1.0 | équivalent |
| 11 | Loi normale multivariée par EM | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | em | lssvr_rbf | 0.6247 | 1.899 | 1.899 | 0.6247 | 0.4 | 0.0014 | 0.283 | 0.154 | équivalent | 1.0 | équivalent |
| 12 | Exclure les séjours sans durée | A · forêt aléatoire quantile | concurrent | exclure | foret | 0.6251 | 2.02 | 1.962 | 0.6012 | 6.7 | 0.0419 | 0.9544 | 1.0 | équivalent | 1.0 | équivalent |
| 13 | Régressions enchaînées (ridge, principe de MICE) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | regression | lssvr_rbf | 0.6252 | 1.901 | 1.901 | 0.6252 | 0.4 | 0.0015 | 0.2059 | 0.1635 | équivalent | 1.0 | équivalent |
| 14 | ACP itérative (rang faible) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | acp_iterative | lssvr_rbf | 0.6254 | 1.912 | 1.979 | 0.626 | 0.5 | 0.0025 | 0.6997 | 0.245 | équivalent | 1.0 | équivalent |
| 15 | k plus proches voisins (prix, âge, sexe, issue, mois) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | knn | lssvr_rbf | 0.6265 | 1.88 | 1.908 | 0.6344 | 0.4 | 0.0015 | 0.3211 | 0.1635 | équivalent | 1.0 | équivalent |
| 16 | SoftImpute (norme nucléaire) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | softimpute | lssvr_rbf | 0.6303 | 1.903 | 1.889 | 0.6283 | 0.1 | 0.0023 | 0.1476 | 0.2277 | équivalent | 1.0 | équivalent |
| 17 | Médiane de la tranche d'âge | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | mediane_age | lssvr_rbf | 0.6321 | 1.912 | 1.905 | 0.6315 | 0.3 | 0.003 | 0.102 | 0.288 | équivalent | 1.0 | équivalent |
| 18 | Médiane du service | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | mediane | lssvr_rbf | 0.6321 | 1.912 | 1.905 | 0.6315 | 0.5 | 0.003 | 0.102 | 0.288 | équivalent | 1.0 | équivalent |
| 19 | SoftImpute (norme nucléaire) | A · forêt aléatoire quantile | concurrent | softimpute | foret | 0.633 | 1.871 | 1.869 | 0.6297 | 8.4 | 0.0124 | 0.5399 | 0.8432 | équivalent | 1.0 | équivalent |
| 20 | Médiane de la tranche d'âge | A · forêt aléatoire quantile | concurrent | mediane_age | foret | 0.6332 | 1.854 | 1.866 | 0.6321 | 14.1 | 0.0096 | 0.5012 | 0.7296 | équivalent | 1.0 | équivalent |
| 21 | Médiane du service | A · forêt aléatoire quantile | concurrent | mediane | foret | 0.6332 | 1.854 | 1.866 | 0.6321 | 8.7 | 0.0096 | 0.5012 | 0.7296 | équivalent | 1.0 | équivalent |
| 22 | Moyenne du service | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | moyenne | lssvr_rbf | 0.64 | 1.899 | 1.923 | 0.6325 | 0.4 | 0.0091 | 0.0738 | 0.7007 | équivalent | 1.0 | équivalent |
| 23 | XGBoost (avec le diagnostic) | SVR quantile, noyau polynomial (degré 2) | svm | xgboost | svr_q_polynomial | 0.6485 | 1.814 | 1.821 | 0.6616 | 4.1 | 0.002 | 0.1673 | 0.206 | équivalent | 1.0 | équivalent |
| 24 | Hybride : prix, sinon XGBoost | SVR quantile, noyau polynomial (degré 2) | svm | hybride | svr_q_polynomial | 0.6503 | 1.805 | 1.808 | 0.6587 | 6.3 | 0.002 | 0.2506 | 0.206 | équivalent | 1.0 | équivalent |
| 25 | Estimée : prix, puis issue, puis médiane | SVR quantile, noyau polynomial (degré 2) | svm | estimee | svr_q_polynomial | 0.6569 | 1.795 | 1.795 | 0.6569 | 6.8 | 0.0046 |  | 0.4094 | équivalent |  | — référence |
| 26 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile, noyau polynomial (degré 2) | svm | regression | svr_q_polynomial | 0.662 | 1.804 | 1.804 | 0.662 | 6.8 | 0.0068 | 0.2357 | 0.5644 | équivalent | 1.0 | équivalent |
| 27 | ACP itérative (rang faible) | SVR quantile, noyau polynomial (degré 2) | svm | acp_iterative | svr_q_polynomial | 0.6637 | 1.773 | 1.825 | 0.6829 | 6.3 | 0.0082 | 0.5242 | 0.6478 | équivalent | 1.0 | équivalent |
| 28 | Médiane du service | SVR quantile, noyau polynomial (degré 2) | svm | mediane | svr_q_polynomial | 0.6642 | 1.8 | 1.81 | 0.664 | 6.7 | 0.0104 | 0.406 | 0.7296 | équivalent | 1.0 | équivalent |
| 29 | Médiane de la tranche d'âge | SVR quantile, noyau polynomial (degré 2) | svm | mediane_age | svr_q_polynomial | 0.6642 | 1.8 | 1.81 | 0.664 | 6.0 | 0.0104 | 0.406 | 0.7296 | équivalent | 1.0 | équivalent |
| 30 | Loi normale multivariée par EM | SVR quantile, noyau polynomial (degré 2) | svm | em | svr_q_polynomial | 0.6651 | 1.802 | 1.802 | 0.6651 | 5.7 | 0.0163 | 0.0598 | 1.0 | équivalent | 1.0 | équivalent |
| 31 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile, noyau polynomial (degré 2) | svm | knn | svr_q_polynomial | 0.6654 | 1.764 | 1.801 | 0.6764 | 6.4 | 0.0245 | 0.3024 | 1.0 | équivalent | 1.0 | équivalent |
| 32 | SoftImpute (norme nucléaire) | SVR quantile, noyau polynomial (degré 2) | svm | softimpute | svr_q_polynomial | 0.666 | 1.792 | 1.789 | 0.6638 | 3.1 | 0.0098 | 0.2968 | 0.7296 | équivalent | 1.0 | équivalent |
| 33 | Moyenne du service | SVR quantile, noyau polynomial (degré 2) | svm | moyenne | svr_q_polynomial | 0.6711 | 1.801 | 1.81 | 0.6685 | 7.7 | 0.0359 | 0.4644 | 1.0 | équivalent | 1.0 | équivalent |
| 34 | k plus proches voisins (prix, âge, sexe, issue, mois) | C · perceptron multicouche quantile | concurrent | knn | mlp | 0.6845 | 1.948 | 1.99 | 0.7009 | 1.6 | 0.3552 | 0.0548 | 1.0 | équivalent | 1.0 | équivalent |
| 35 | ACP itérative (rang faible) | C · perceptron multicouche quantile | concurrent | acp_iterative | mlp | 0.6847 | 1.977 | 2.048 | 0.7117 | 1.3 | 0.3894 | 0.1522 | 1.0 | équivalent | 1.0 | équivalent |
| 36 | Régressions enchaînées (ridge, principe de MICE) | C · perceptron multicouche quantile | concurrent | regression | mlp | 0.7007 | 2.005 | 2.005 | 0.7007 | 1.4 | 0.6166 | 0.2693 | 1.0 | équivalent | 1.0 | équivalent |
| 37 | SoftImpute (norme nucléaire) | C · perceptron multicouche quantile | concurrent | softimpute | mlp | 0.703 | 1.975 | 1.978 | 0.7057 | 1.3 | 0.6446 | 0.3259 | 1.0 | équivalent | 1.0 | équivalent |
| 38 | XGBoost (avec le diagnostic) | D · LSTM quantile | concurrent | xgboost | lstm | 0.7039 | 2.032 | 2.016 | 0.7148 | 12.3 | 0.6148 | 0.5697 | 1.0 | équivalent | 1.0 | équivalent |
| 39 | Moyenne du service | B · gradient boosting quantile | concurrent | moyenne | boosting | 0.7077 | 1.852 | 1.834 | 0.7168 | 11.2 | 0.7115 | 0.2321 | 1.0 | équivalent | 1.0 | équivalent |
| 40 | Exclure les séjours sans durée | SVR quantile, noyau polynomial (degré 2) | svm | exclure | svr_q_polynomial | 0.7091 | 1.85 | 1.832 | 0.6648 | 3.8 | 0.7488 | 0.0956 | 1.0 | équivalent | 1.0 | équivalent |
| 41 | Médiane de la tranche d'âge | C · perceptron multicouche quantile | concurrent | mediane_age | mlp | 0.7091 | 2.009 | 2.011 | 0.7138 | 1.5 | 0.7575 | 0.5161 | 1.0 | équivalent | 1.0 | équivalent |
| 42 | Médiane du service | C · perceptron multicouche quantile | concurrent | mediane | mlp | 0.7091 | 2.009 | 2.011 | 0.7138 | 1.4 | 0.7575 | 0.5161 | 1.0 | équivalent | 1.0 | équivalent |
| 43 | Moyenne du service | C · perceptron multicouche quantile | concurrent | moyenne | mlp | 0.7091 | 2.029 | 2.065 | 0.7406 | 1.5 | 0.7307 | 0.6097 | 1.0 | équivalent | 1.0 | équivalent |
| 44 | k plus proches voisins (prix, âge, sexe, issue, mois) | D · LSTM quantile | concurrent | knn | lstm | 0.7108 | 1.972 | 2.0 | 0.7249 | 13.1 | 0.7523 | 0.8129 | 1.0 | équivalent | 1.0 | équivalent |
| 45 | XGBoost (avec le diagnostic) | SVR quantile composite (niveau 4, retenu) | svm | xgboost | svr_q_composite | 0.7125 | 2.056 | 2.058 | 0.7208 | 4.8 | 0.1144 | 0.1144 | 1.0 | équivalent | 1.0 | équivalent |
| 46 | Hybride : prix, sinon XGBoost | SVR quantile composite (niveau 4, retenu) | svm | hybride | svr_q_composite | 0.7134 | 2.047 | 2.044 | 0.7188 | 4.5 | 0.0385 | 0.0385 | 1.0 | équivalent | 1.0 | équivalent |
| 47 | Estimée : prix, puis issue, puis médiane | D · LSTM quantile | concurrent | estimee | lstm | 0.714 | 1.987 | 1.987 | 0.714 | 12.5 | 0.8268 |  | 1.0 | équivalent |  | — référence |
| 48 | ACP itérative (rang faible) | SVR quantile composite (niveau 4, retenu) | svm | acp_iterative | svr_q_composite | 0.7158 | 1.963 | 2.037 | 0.7454 | 5.1 | 0.5691 | 0.5691 | 1.0 | équivalent | 1.0 | équivalent |
| 49 | Moyenne du service | SVR quantile RBF (niveau 3) | svm | moyenne | svr_q_rbf | 0.7162 | 2.0 | 2.004 | 0.7171 | 3.7 | 0.6527 | 0.413 | 1.0 | équivalent | 1.0 | équivalent |
| 50 | Régressions enchaînées (ridge, principe de MICE) | D · LSTM quantile | concurrent | regression | lstm | 0.7173 | 2.021 | 2.021 | 0.7173 | 11.1 | 0.8948 | 0.5925 | 1.0 | équivalent | 1.0 | équivalent |
| 51 | Hybride : prix, sinon XGBoost | D · LSTM quantile | concurrent | hybride | lstm | 0.7195 | 2.033 | 2.011 | 0.7261 | 14.3 | 0.9496 | 0.7555 | 1.0 | équivalent | 1.0 | équivalent |
| 52 | Estimée : prix, puis issue, puis médiane | C · perceptron multicouche quantile | concurrent | estimee | mlp | 0.7201 | 1.962 | 1.962 | 0.7201 | 2.0 | 0.9675 |  | 1.0 | équivalent |  | — référence |
| 53 | Estimée : prix, puis issue, puis médiane | SVR quantile composite (niveau 4, retenu) | svm | estimee | svr_q_composite | 0.7217 | 2.037 | 2.037 | 0.7217 | 9.8 |  |  |  | — référence |  | — référence |
| 54 | ACP itérative (rang faible) | B · gradient boosting quantile | concurrent | acp_iterative | boosting | 0.722 | 1.844 | 1.889 | 0.7438 | 7.3 | 0.9933 | 0.4235 | 1.0 | équivalent | 1.0 | équivalent |
| 55 | XGBoost (avec le diagnostic) | C · perceptron multicouche quantile | concurrent | xgboost | mlp | 0.7234 | 1.943 | 1.952 | 0.7292 | 1.3 | 0.9696 | 0.8534 | 1.0 | équivalent | 1.0 | équivalent |
| 56 | ACP itérative (rang faible) | SVR quantile RBF (niveau 3) | svm | acp_iterative | svr_q_rbf | 0.7243 | 1.997 | 2.069 | 0.7503 | 3.9 | 0.7633 | 0.8165 | 1.0 | équivalent | 1.0 | équivalent |
| 57 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile composite (niveau 4, retenu) | svm | knn | svr_q_composite | 0.7244 | 2.015 | 2.047 | 0.7406 | 7.2 | 0.6626 | 0.6626 | 1.0 | équivalent | 1.0 | équivalent |
| 58 | Estimée : prix, puis issue, puis médiane | SVR quantile RBF (niveau 3) | svm | estimee | svr_q_rbf | 0.7262 | 2.016 | 2.016 | 0.7262 | 6.3 | 0.4542 |  | 1.0 | équivalent |  | — référence |
| 59 | Médiane du service | E · XGBoost quantile (second ordre) | concurrent | mediane | xgboost | 0.7265 | 1.854 | 1.851 | 0.7302 | 12.7 | 0.8789 | 0.4057 | 1.0 | équivalent | 1.0 | équivalent |
| 60 | Médiane de la tranche d'âge | E · XGBoost quantile (second ordre) | concurrent | mediane_age | xgboost | 0.7265 | 1.854 | 1.851 | 0.7302 | 12.1 | 0.8789 | 0.4057 | 1.0 | équivalent | 1.0 | équivalent |
| 61 | ACP itérative (rang faible) | E · XGBoost quantile (second ordre) | concurrent | acp_iterative | xgboost | 0.7267 | 1.84 | 1.902 | 0.7619 | 7.6 | 0.9022 | 0.533 | 1.0 | équivalent | 1.0 | équivalent |
| 62 | ACP itérative (rang faible) | D · LSTM quantile | concurrent | acp_iterative | lstm | 0.7269 | 1.967 | 2.018 | 0.7524 | 13.0 | 0.8838 | 0.503 | 1.0 | équivalent | 1.0 | équivalent |
| 63 | Hybride : prix, sinon XGBoost | SVR quantile RBF (niveau 3) | svm | hybride | svr_q_rbf | 0.7286 | 2.039 | 2.03 | 0.7347 | 3.3 | 0.2668 | 0.5056 | 1.0 | équivalent | 1.0 | équivalent |
| 64 | Loi normale multivariée par EM | SVR quantile RBF (niveau 3) | svm | em | svr_q_rbf | 0.7298 | 2.019 | 2.019 | 0.7298 | 3.9 | 0.1458 | 0.1103 | 1.0 | équivalent | 1.0 | équivalent |
| 65 | k plus proches voisins (prix, âge, sexe, issue, mois) | B · gradient boosting quantile | concurrent | knn | boosting | 0.7298 | 1.801 | 1.842 | 0.7462 | 10.2 | 0.8332 | 0.451 | 1.0 | équivalent | 1.0 | équivalent |
| 66 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile RBF (niveau 3) | svm | regression | svr_q_rbf | 0.73 | 2.018 | 2.018 | 0.73 | 4.2 | 0.1337 | 0.1047 | 1.0 | équivalent | 1.0 | équivalent |
| 67 | XGBoost (avec le diagnostic) | SVR quantile RBF (niveau 3) | svm | xgboost | svr_q_rbf | 0.731 | 2.044 | 2.041 | 0.7408 | 2.6 | 0.0796 | 0.2958 | 1.0 | équivalent | 1.0 | équivalent |
| 68 | Loi normale multivariée par EM | B · gradient boosting quantile | concurrent | em | boosting | 0.7318 | 1.856 | 1.856 | 0.7318 | 11.4 | 0.7914 | 0.3533 | 1.0 | équivalent | 1.0 | équivalent |
| 69 | Loi normale multivariée par EM | C · perceptron multicouche quantile | concurrent | em | mlp | 0.7329 | 2.017 | 2.017 | 0.7329 | 1.6 | 0.788 | 0.3516 | 1.0 | équivalent | 1.0 | équivalent |
| 70 | Médiane de la tranche d'âge | B · gradient boosting quantile | concurrent | mediane_age | boosting | 0.7352 | 1.875 | 1.87 | 0.7356 | 12.1 | 0.7182 | 0.6105 | 1.0 | équivalent | 1.0 | équivalent |
| 71 | Médiane du service | B · gradient boosting quantile | concurrent | mediane | boosting | 0.7352 | 1.875 | 1.87 | 0.7356 | 10.9 | 0.7182 | 0.6105 | 1.0 | équivalent | 1.0 | équivalent |
| 72 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile RBF (niveau 3) | svm | knn | svr_q_rbf | 0.7354 | 2.018 | 2.047 | 0.7499 | 5.0 | 0.0297 | 0.0792 | 1.0 | équivalent | 1.0 | équivalent |
| 73 | SoftImpute (norme nucléaire) | E · XGBoost quantile (second ordre) | concurrent | softimpute | xgboost | 0.7358 | 1.872 | 1.858 | 0.7358 | 6.7 | 0.6881 | 0.7117 | 1.0 | équivalent | 1.0 | équivalent |
| 74 | Loi normale multivariée par EM | SVR quantile composite (niveau 4, retenu) | svm | em | svr_q_composite | 0.7375 | 2.046 | 2.046 | 0.7375 | 5.9 | 0.0006 | 0.0006 | 0.069 | équivalent | 0.072 | équivalent |
| 75 | Moyenne du service | SVR quantile, noyau laplacien | svm | moyenne | svr_q_laplacien | 0.738 | 2.089 | 2.074 | 0.7499 | 3.9 | 0.2808 | 0.0646 | 1.0 | équivalent | 1.0 | équivalent |
| 76 | Hybride : prix, sinon XGBoost | B · gradient boosting quantile | concurrent | hybride | boosting | 0.7383 | 1.874 | 1.867 | 0.7416 | 11.6 | 0.6552 | 0.7156 | 1.0 | équivalent | 1.0 | équivalent |
| 77 | Loi normale multivariée par EM | D · LSTM quantile | concurrent | em | lstm | 0.7391 | 2.014 | 2.014 | 0.7391 | 11.2 | 0.6299 | 0.0271 | 1.0 | équivalent | 1.0 | équivalent |
| 78 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile composite (niveau 4, retenu) | svm | regression | svr_q_composite | 0.7391 | 2.042 | 2.042 | 0.7391 | 5.0 | 0.0003 | 0.0003 | 0.0357 | moins bon | 0.0366 | moins bon |
| 79 | SoftImpute (norme nucléaire) | B · gradient boosting quantile | concurrent | softimpute | boosting | 0.7415 | 1.858 | 1.855 | 0.7409 | 9.6 | 0.612 | 0.8798 | 1.0 | équivalent | 1.0 | équivalent |
| 80 | Régressions enchaînées (ridge, principe de MICE) | B · gradient boosting quantile | concurrent | regression | boosting | 0.7416 | 1.838 | 1.838 | 0.7416 | 11.2 | 0.5989 | 0.844 | 1.0 | équivalent | 1.0 | équivalent |
| 81 | Médiane du service | SVR quantile RBF (niveau 3) | svm | mediane | svr_q_rbf | 0.743 | 2.039 | 2.039 | 0.7443 | 4.2 | 0.0034 | 0.0099 | 0.3196 | équivalent | 1.0 | équivalent |
| 82 | Médiane du service | SVR quantile composite (niveau 4, retenu) | svm | mediane | svr_q_composite | 0.743 | 2.031 | 2.035 | 0.7504 | 7.6 | 0.0096 | 0.0096 | 0.7296 | équivalent | 1.0 | équivalent |
| 83 | Médiane de la tranche d'âge | SVR quantile RBF (niveau 3) | svm | mediane_age | svr_q_rbf | 0.743 | 2.039 | 2.039 | 0.7443 | 3.5 | 0.0034 | 0.0099 | 0.3196 | équivalent | 1.0 | équivalent |
| 84 | Médiane de la tranche d'âge | SVR quantile composite (niveau 4, retenu) | svm | mediane_age | svr_q_composite | 0.743 | 2.031 | 2.035 | 0.7504 | 6.0 | 0.0096 | 0.0096 | 0.7296 | équivalent | 1.0 | équivalent |
| 85 | SoftImpute (norme nucléaire) | SVR quantile RBF (niveau 3) | svm | softimpute | svr_q_rbf | 0.7431 | 2.034 | 2.023 | 0.7439 | 2.0 | 0.0045 | 0.0166 | 0.405 | équivalent | 1.0 | équivalent |
| 86 | Estimée : prix, puis issue, puis médiane | E · XGBoost quantile (second ordre) | concurrent | estimee | xgboost | 0.744 | 1.896 | 1.896 | 0.744 | 12.0 | 0.5474 |  | 1.0 | équivalent |  | — référence |
| 87 | Estimée : prix, puis issue, puis médiane | B · gradient boosting quantile | concurrent | estimee | boosting | 0.7442 | 1.904 | 1.904 | 0.7442 | 12.1 | 0.5481 |  | 1.0 | équivalent |  | — référence |
| 88 | SoftImpute (norme nucléaire) | SVR quantile composite (niveau 4, retenu) | svm | softimpute | svr_q_composite | 0.7445 | 2.024 | 2.016 | 0.7512 | 2.7 | 0.0061 | 0.0061 | 0.5185 | équivalent | 0.6527 | équivalent |
| 89 | Loi normale multivariée par EM | E · XGBoost quantile (second ordre) | concurrent | em | xgboost | 0.7457 | 1.906 | 1.906 | 0.7457 | 10.9 | 0.5196 | 0.906 | 1.0 | équivalent | 1.0 | équivalent |
| 90 | XGBoost (avec le diagnostic) | B · gradient boosting quantile | concurrent | xgboost | boosting | 0.7468 | 1.842 | 1.839 | 0.7535 | 8.8 | 0.5202 | 0.8919 | 1.0 | équivalent | 1.0 | équivalent |
| 91 | Exclure les séjours sans durée | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | exclure | lssvr_rbf | 0.7483 | 2.12 | 2.053 | 0.6907 | 0.1 | 0.4723 | 0.0024 | 1.0 | équivalent | 0.2784 | équivalent |
| 92 | Moyenne du service | SVR quantile composite (niveau 4, retenu) | svm | moyenne | svr_q_composite | 0.7488 | 2.016 | 2.015 | 0.754 | 7.0 | 0.006 | 0.006 | 0.516 | équivalent | 0.648 | équivalent |
| 93 | XGBoost (avec le diagnostic) | SVR quantile, noyau laplacien | svm | xgboost | svr_q_laplacien | 0.7535 | 2.111 | 2.122 | 0.7564 | 2.2 | 0.0171 | 0.2577 | 1.0 | équivalent | 1.0 | équivalent |
| 94 | Moyenne du service | E · XGBoost quantile (second ordre) | concurrent | moyenne | xgboost | 0.7543 | 1.921 | 1.913 | 0.7641 | 10.4 | 0.3402 | 0.758 | 1.0 | équivalent | 1.0 | équivalent |
| 95 | Régressions enchaînées (ridge, principe de MICE) | E · XGBoost quantile (second ordre) | concurrent | regression | xgboost | 0.7544 | 1.862 | 1.862 | 0.7544 | 12.3 | 0.3612 | 0.4934 | 1.0 | équivalent | 1.0 | équivalent |
| 96 | Loi normale multivariée par EM | SVR quantile, noyau laplacien | svm | em | svr_q_laplacien | 0.7545 | 2.084 | 2.084 | 0.7545 | 5.5 | 0.0079 | 0.1847 | 0.632 | équivalent | 1.0 | équivalent |
| 97 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile, noyau laplacien | svm | regression | svr_q_laplacien | 0.7549 | 2.084 | 2.084 | 0.7549 | 3.5 | 0.0077 | 0.2533 | 0.6237 | équivalent | 1.0 | équivalent |
| 98 | SoftImpute (norme nucléaire) | D · LSTM quantile | concurrent | softimpute | lstm | 0.7554 | 2.017 | 2.011 | 0.7614 | 8.6 | 0.3711 | 0.0051 | 1.0 | équivalent | 0.5661 | équivalent |
| 99 | Hybride : prix, sinon XGBoost | SVR quantile, noyau laplacien | svm | hybride | svr_q_laplacien | 0.7564 | 2.105 | 2.11 | 0.7569 | 3.3 | 0.0098 | 0.6846 | 0.7296 | équivalent | 1.0 | équivalent |
| 100 | Estimée : prix, puis issue, puis médiane | SVR quantile, noyau laplacien | svm | estimee | svr_q_laplacien | 0.7576 | 2.087 | 2.087 | 0.7576 | 4.6 | 0.0056 |  | 0.4872 | équivalent |  | — référence |
| 101 | k plus proches voisins (prix, âge, sexe, issue, mois) | E · XGBoost quantile (second ordre) | concurrent | knn | xgboost | 0.7577 | 1.839 | 1.876 | 0.7731 | 11.1 | 0.303 | 0.4816 | 1.0 | équivalent | 1.0 | équivalent |
| 102 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile, noyau laplacien | svm | knn | svr_q_laplacien | 0.7587 | 2.084 | 2.11 | 0.7751 | 5.6 | 0.0067 | 0.7514 | 0.5628 | équivalent | 1.0 | équivalent |
| 103 | ACP itérative (rang faible) | SVR quantile, noyau laplacien | svm | acp_iterative | svr_q_laplacien | 0.7601 | 2.071 | 2.15 | 0.7903 | 3.8 | 0.0071 | 0.7396 | 0.5822 | équivalent | 1.0 | équivalent |
| 104 | Hybride : prix, sinon XGBoost | E · XGBoost quantile (second ordre) | concurrent | hybride | xgboost | 0.7636 | 1.92 | 1.918 | 0.766 | 12.3 | 0.2845 | 0.2976 | 1.0 | équivalent | 1.0 | équivalent |
| 105 | Médiane de la tranche d'âge | D · LSTM quantile | concurrent | mediane_age | lstm | 0.7664 | 2.029 | 2.035 | 0.7702 | 13.9 | 0.2126 | 0.0001 | 1.0 | équivalent | 0.0129 | moins bon |
| 106 | Médiane du service | D · LSTM quantile | concurrent | mediane | lstm | 0.7664 | 2.029 | 2.035 | 0.7702 | 14.0 | 0.2126 | 0.0001 | 1.0 | équivalent | 0.0129 | moins bon |
| 107 | Moyenne du service | D · LSTM quantile | concurrent | moyenne | lstm | 0.7685 | 2.046 | 2.072 | 0.7856 | 12.6 | 0.2232 | 0.0162 | 1.0 | équivalent | 1.0 | équivalent |
| 108 | Hybride : prix, sinon XGBoost | C · perceptron multicouche quantile | concurrent | hybride | mlp | 0.7686 | 2.038 | 2.039 | 0.765 | 1.4 | 0.2891 | 0.0038 | 1.0 | équivalent | 0.4256 | équivalent |
| 109 | Exclure les séjours sans durée | C · perceptron multicouche quantile | concurrent | exclure | mlp | 0.7687 | 2.1 | 2.063 | 0.7034 | 0.6 | 0.384 | 0.1611 | 1.0 | équivalent | 1.0 | équivalent |
| 110 | Médiane du service | SVR quantile, noyau laplacien | svm | mediane | svr_q_laplacien | 0.7692 | 2.114 | 2.119 | 0.7739 | 4.1 | 0.0016 | 0.0229 | 0.1712 | équivalent | 1.0 | équivalent |
| 111 | Médiane de la tranche d'âge | SVR quantile, noyau laplacien | svm | mediane_age | svr_q_laplacien | 0.7692 | 2.114 | 2.119 | 0.7739 | 3.8 | 0.0016 | 0.0229 | 0.1712 | équivalent | 1.0 | équivalent |
| 112 | SoftImpute (norme nucléaire) | SVR quantile, noyau laplacien | svm | softimpute | svr_q_laplacien | 0.7713 | 2.102 | 2.098 | 0.7743 | 1.7 | 0.0011 | 0.0051 | 0.1243 | équivalent | 0.5661 | équivalent |
| 113 | XGBoost (avec le diagnostic) | E · XGBoost quantile (second ordre) | concurrent | xgboost | xgboost | 0.7739 | 1.91 | 1.909 | 0.7808 | 11.8 | 0.179 | 0.0798 | 1.0 | équivalent | 1.0 | équivalent |
| 114 | Exclure les séjours sans durée | D · LSTM quantile | concurrent | exclure | lstm | 0.7847 | 2.096 | 1.99 | 0.7251 | 5.9 | 0.1875 | 0.0873 | 1.0 | équivalent | 1.0 | équivalent |
| 115 | Exclure les séjours sans durée | SVR quantile composite (niveau 4, retenu) | svm | exclure | svr_q_composite | 0.8218 | 2.205 | 2.148 | 0.7766 | 3.1 | 0.0029 | 0.0029 | 0.2813 | équivalent | 0.3335 | équivalent |
| 116 | Exclure les séjours sans durée | B · gradient boosting quantile | concurrent | exclure | boosting | 0.8274 | 1.963 | 1.868 | 0.7333 | 5.0 | 0.0649 | 0.0657 | 1.0 | équivalent | 1.0 | équivalent |
| 117 | Exclure les séjours sans durée | SVR quantile RBF (niveau 3) | svm | exclure | svr_q_rbf | 0.8621 | 2.239 | 2.186 | 0.8175 | 3.0 | 0.0001 | 0.0002 | 0.0121 | moins bon | 0.0246 | moins bon |
| 118 | Exclure les séjours sans durée | SVR quantile, noyau laplacien | svm | exclure | svr_q_laplacien | 0.896 | 2.342 | 2.295 | 0.8586 | 2.0 | 0.0 | 0.0 | 0.0 | moins bon | 0.0 | moins bon |
| 119 | Exclure les séjours sans durée | E · XGBoost quantile (second ordre) | concurrent | exclure | xgboost | 0.9118 | 2.083 | 1.987 | 0.8138 | 6.6 | 0.0012 | 0.0008 | 0.1344 | équivalent | 0.0952 | équivalent |
| 120 | Moyenne du service | SVR linéaire (niveau 1) | svm | moyenne | svr_lineaire | 0.9139 | 1.77 | 1.768 | 0.9505 | 2.1 | 0.0016 | 0.0082 | 0.1712 | équivalent | 0.8692 | équivalent |
| 121 | ACP itérative (rang faible) | SVR linéaire (niveau 1) | svm | acp_iterative | svr_lineaire | 0.9343 | 1.765 | 1.786 | 0.9712 | 1.3 | 0.0003 | 0.0368 | 0.0357 | moins bon | 1.0 | équivalent |
| 122 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR linéaire (niveau 1) | svm | knn | svr_lineaire | 0.9715 | 1.759 | 1.795 | 0.998 | 1.6 | 0.0001 | 0.707 | 0.0121 | moins bon | 1.0 | équivalent |
| 123 | Estimée : prix, puis issue, puis médiane | SVR linéaire (niveau 1) | svm | estimee | svr_lineaire | 0.9769 | 1.761 | 1.761 | 0.9769 | 1.6 | 0.0 |  | 0.0 | moins bon |  | — référence |
| 124 | Loi normale multivariée par EM | SVR linéaire (niveau 1) | svm | em | svr_lineaire | 0.9843 | 1.783 | 1.783 | 0.9843 | 1.5 | 0.0 | 0.4687 | 0.0 | moins bon | 1.0 | équivalent |
| 125 | Régressions enchaînées (ridge, principe de MICE) | SVR linéaire (niveau 1) | svm | regression | svr_lineaire | 0.9855 | 1.776 | 1.776 | 0.9855 | 1.7 | 0.0 | 0.4026 | 0.0 | moins bon | 1.0 | équivalent |
| 126 | XGBoost (avec le diagnostic) | SVR linéaire (niveau 1) | svm | xgboost | svr_lineaire | 0.9866 | 1.768 | 1.768 | 0.9748 | 0.9 | 0.0 | 0.4879 | 0.0 | moins bon | 1.0 | équivalent |
| 127 | Hybride : prix, sinon XGBoost | SVR linéaire (niveau 1) | svm | hybride | svr_lineaire | 0.9883 | 1.773 | 1.767 | 0.9719 | 1.3 | 0.0 | 0.3797 | 0.0 | moins bon | 1.0 | équivalent |
| 128 | Médiane de la tranche d'âge | SVR linéaire (niveau 1) | svm | mediane_age | svr_lineaire | 1.0189 | 1.812 | 1.821 | 1.0169 | 1.5 | 0.0 | 0.0032 | 0.0 | moins bon | 0.3648 | équivalent |
| 129 | Médiane du service | SVR linéaire (niveau 1) | svm | mediane | svr_lineaire | 1.0189 | 1.812 | 1.821 | 1.0169 | 0.9 | 0.0 | 0.0032 | 0.0 | moins bon | 0.3648 | équivalent |
| 130 | SoftImpute (norme nucléaire) | SVR linéaire (niveau 1) | svm | softimpute | svr_lineaire | 1.0237 | 1.798 | 1.795 | 1.0189 | 1.3 | 0.0 | 0.0005 | 0.0 | moins bon | 0.0605 | équivalent |
| 131 | Moyenne du service | SVR RBF (niveau 2) | svm | moyenne | svr_rbf | 1.0416 | 1.933 | 1.928 | 1.0772 | 2.2 | 0.0 | 0.0001 | 0.0 | moins bon | 0.0129 | meilleur |
| 132 | Estimée : prix, puis issue, puis médiane | SVR RBF (niveau 2) | svm | estimee | svr_rbf | 1.1042 | 1.934 | 1.934 | 1.1042 | 2.0 | 0.0 |  | 0.0 | moins bon |  | — référence |
| 133 | Régressions enchaînées (ridge, principe de MICE) | SVR RBF (niveau 2) | svm | regression | svr_rbf | 1.1097 | 1.947 | 1.947 | 1.1097 | 1.1 | 0.0 | 0.0185 | 0.0 | moins bon | 1.0 | équivalent |
| 134 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR RBF (niveau 2) | svm | knn | svr_rbf | 1.1105 | 1.941 | 1.958 | 1.1273 | 2.0 | 0.0 | 0.2914 | 0.0 | moins bon | 1.0 | équivalent |
| 135 | Loi normale multivariée par EM | SVR RBF (niveau 2) | svm | em | svr_rbf | 1.1117 | 1.941 | 1.941 | 1.1117 | 2.0 | 0.0 | 0.0019 | 0.0 | moins bon | 0.2223 | équivalent |
| 136 | XGBoost (avec le diagnostic) | SVR RBF (niveau 2) | svm | xgboost | svr_rbf | 1.1223 | 1.934 | 1.93 | 1.1087 | 1.1 | 0.0 | 0.0058 | 0.0 | moins bon | 0.6322 | équivalent |
| 137 | SoftImpute (norme nucléaire) | SVR RBF (niveau 2) | svm | softimpute | svr_rbf | 1.1225 | 1.946 | 1.928 | 1.1104 | 1.5 | 0.0 | 0.0243 | 0.0 | moins bon | 1.0 | équivalent |
| 138 | ACP itérative (rang faible) | SVR RBF (niveau 2) | svm | acp_iterative | svr_rbf | 1.1265 | 1.958 | 2.026 | 1.1867 | 2.0 | 0.0 | 0.0476 | 0.0 | moins bon | 1.0 | équivalent |
| 139 | Hybride : prix, sinon XGBoost | SVR RBF (niveau 2) | svm | hybride | svr_rbf | 1.1301 | 1.943 | 1.934 | 1.1125 | 1.2 | 0.0 | 0.0 | 0.0 | moins bon | 0.0 | moins bon |
| 140 | Médiane de la tranche d'âge | SVR RBF (niveau 2) | svm | mediane_age | svr_rbf | 1.1412 | 1.962 | 1.954 | 1.1305 | 2.0 | 0.0 | 0.0001 | 0.0 | moins bon | 0.0129 | moins bon |
| 141 | Médiane du service | SVR RBF (niveau 2) | svm | mediane | svr_rbf | 1.1412 | 1.962 | 1.954 | 1.1305 | 1.2 | 0.0 | 0.0001 | 0.0 | moins bon | 0.0129 | moins bon |
| 142 | Exclure les séjours sans durée | SVR linéaire (niveau 1) | svm | exclure | svr_lineaire | 1.1507 | 1.832 | 1.766 | 0.9769 | 0.8 | 0.0 | 0.0001 | 0.0 | moins bon | 0.0129 | moins bon |
| 143 | Exclure les séjours sans durée | SVR RBF (niveau 2) | svm | exclure | svr_rbf | 1.4387 | 2.162 | 2.11 | 1.2713 | 0.8 | 0.0 | 0.0 | 0.0 | moins bon | 0.0 | moins bon |


Meilleure paire : **Loi normale multivariée par EM × A · forêt aléatoire quantile**.


## Horizon J+7


### P1 · Durées inconnues

177 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Exclure les séjours sans durée | 15/07/2025 | 0 | 8.74 | 51.4 | -0.4 | 3.044 | 1.1384 | 3.7 | 3.096 | 7.5 | 1.1831 | 0.0187 | 0.187 | 0.0652 | équivalent |
| Médiane du service | 15/07/2025 | 0 | 9.73 | 57.3 | -3.5 | 2.709 | 0.9524 | 10.4 | 2.705 | 9.1 | 0.9507 | 0.0967 | 0.612 | 0.2869 | équivalent |
| Moyenne du service | 15/07/2025 | 0 | 10.06 | 59.2 | -0.2 | 2.651 | 0.9489 | 12.7 | 2.668 | 5.6 | 0.9276 | 0.402 | 0.804 | 0.3033 | équivalent |
| Médiane de la tranche d'âge | 15/07/2025 | 0 | 9.73 | 57.3 | -3.5 | 2.709 | 0.9524 | 10.4 | 2.705 | 7.6 | 0.9507 | 0.0967 | 0.612 | 0.2869 | équivalent |
| Estimée : prix, puis issue, puis médiane (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.719 | 0.9447 | 7.3 | 2.719 | 6.4 | 0.9447 |  |  |  | — choix retenu |
| k plus proches voisins (prix, âge, sexe, issue, mois) | 15/07/2025 | 0 | 9.75 | 57.3 | -3.4 | 2.717 | 0.957 | 9.5 | 2.697 | 10.1 | 0.9414 | 0.0621 | 0.5589 | 0.1359 | équivalent |
| Régressions enchaînées (ridge, principe de MICE) | 15/07/2025 | 0 | 9.75 | 57.3 | -3.4 | 2.72 | 0.9396 | 7.3 | 2.72 | 8.8 | 0.9396 | 0.0812 | 0.612 | 0.9379 | équivalent |
| Loi normale multivariée par EM | 15/07/2025 | 0 | 9.74 | 57.3 | -3.4 | 2.718 | 0.9397 | 7.3 | 2.718 | 7.2 | 0.9397 | 0.0765 | 0.612 | 0.7766 | équivalent |
| ACP itérative (rang faible) | 15/07/2025 | 0 | 9.62 | 56.6 | -4.3 | 2.811 | 0.9962 | 5.5 | 2.725 | 11.8 | 0.9667 | 0.1283 | 0.612 | 0.8602 | équivalent |
| SoftImpute (norme nucléaire) | 15/07/2025 | 0 | 9.75 | 57.3 | -3.4 | 2.698 | 0.9498 | 10.4 | 2.696 | 9.4 | 0.9504 | 0.0944 | 0.612 | 0.0887 | équivalent |
| XGBoost (avec le diagnostic) | 15/07/2025 | 0 | 9.7 | 57.0 | -3.8 | 2.766 | 0.9299 | 6.0 | 2.757 | 33.4 | 0.9343 | 0.0068 | 0.0748 | 0.0673 | équivalent |
| Hybride : prix, sinon XGBoost | 15/07/2025 | 0 | 9.7 | 57.0 | -3.8 | 2.761 | 0.9377 | 6.2 | 2.758 | 29.4 | 0.9422 | 0.4466 | 0.804 | 0.0641 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Estimée : prix, puis issue, puis médiane (retenu)).



### P2 · Fenêtre de censure (encore hospitalisé)

177 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 14 jours | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.719 | 0.9447 | 7.3 | 2.719 | 9.0 | 0.9447 |  |  |  | identique |
| 30 jours | 15/07/2025 | 0 | 9.79 | 57.6 | -3.6 | 2.702 | 0.9297 | 7.3 | 2.719 | 7.0 | 0.9458 | 0.3009 | 0.5784 | 0.3064 | équivalent |
| p95 des durées connues (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.719 | 0.9447 | 7.3 | 2.719 | 6.5 | 0.9447 |  |  |  | — choix retenu |
| 60 jours | 15/07/2025 | 0 | 9.94 | 58.5 | -3.5 | 2.718 | 0.9469 | 7.7 | 2.721 | 7.7 | 0.9472 | 0.2892 | 0.5784 | 0.5311 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (p95 des durées connues (retenu)).



### P3 · Convention du nombre de jours

177 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Attendue (nuit incertaine = 1 − p) (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.719 | 0.9447 | 7.3 | 2.719 | 8.0 | 0.9447 |  |  |  | — choix retenu |
| Tout inclusif (borne basse) | 15/07/2025 | 0 | 9.07 | 53.4 | -6.5 | 2.86 | 1.0588 | 8.0 | 2.952 | 9.6 | 1.0902 | 0.0429 | 0.0858 | 0.1577 | équivalent |
| Tout en nuits (borne haute) | 15/07/2025 | 0 | 10.36 | 60.9 | 2.1 | 2.7 | 0.8887 | 9.7 | 2.716 | 8.0 | 0.8716 | 0.2393 | 0.2393 | 0.979 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Attendue (nuit incertaine = 1 − p) (retenu)).



### P4 · Patients « Ancien » reportés

177 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Garder toutes les lignes (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.719 | 0.9447 | 7.3 | 2.719 | 6.9 | 0.9447 |  |  |  | — choix retenu |
| Fusionner les reports confirmés | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.719 | 0.9447 | 7.3 | 2.719 | 6.1 | 0.9447 |  |  |  | identique |


Aucune variante ne fait significativement mieux que le choix retenu (Garder toutes les lignes (retenu)).



### P5 · Période exploitable

177 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Durées connues ≥ 80 % | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.719 | 0.9447 | 7.3 | 2.719 | 9.2 | 0.9447 |  |  |  | identique |
| Durées connues ≥ 90 % (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.719 | 0.9447 | 7.3 | 2.719 | 7.5 | 0.9447 |  |  |  | — choix retenu |
| Durées connues ≥ 95 % | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.719 | 0.9447 | 7.3 | 2.719 | 5.7 | 0.9447 |  |  |  | identique |
| ≥ 90 %, sans rodage au début (premier mois = début réel du registre) | 01/07/2025 | 0 | 9.43 | 55.5 | -4.1 | 2.744 | 0.9455 | 6.4 | 2.744 | 6.1 | 0.9455 | 0.912 | 0.912 | 0.7184 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Durées connues ≥ 90 % (retenu)).



### P6 · Fin de série (délai d'inscription)

170 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Aucune coupe | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.771 | 0.9631 | 4.5 | 2.771 | 6.6 | 0.9631 |  |  |  | identique |
| 7 derniers jours retirés | 15/07/2025 | 7 | 9.71 | 57.1 | -3.7 | 2.771 | 0.9631 | 4.5 | 2.771 | 6.2 | 0.9631 |  |  |  | identique |
| p95 du délai d'inscription (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.771 | 0.9631 | 4.5 | 2.771 | 7.4 | 0.9631 |  |  |  | — choix retenu |


Aucune variante ne fait significativement mieux que le choix retenu (p95 du délai d'inscription (retenu)).



### P7 · Trous de saisie (≥ 4 jours sans admission)

177 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Gardés tels quels (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.719 | 0.9447 | 7.3 | 2.719 | 7.3 | 0.9447 |  |  |  | — choix retenu |
| Lignes d'apprentissage qui les touchent exclues | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.726 | 0.9445 | 7.1 | 2.726 | 6.4 | 0.9445 | 0.9177 | 0.9177 | 0.682 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Gardés tels quels (retenu)).



### P8 · Méthode de comptage des présents

177 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Recensement de minuit (nuits passées) (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.719 | 0.9447 | 7.3 | 2.719 | 5.3 | 0.9447 |  |  |  | — choix retenu |
| Présence dans la journée (jour de sortie compris) | 15/07/2025 | 0 | 12.27 | 72.2 | -2.8 | 3.129 | 1.0459 | -1.7 | 2.849 | 4.7 | 0.954 | 0.9495 | 0.9495 | 0.7331 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Recensement de minuit (nuits passées) (retenu)).



### P1 × modèles (J+7) : chaque méthode des durées inconnues avec chaque modèle

177 jours évalués ; tri par perte pinball τ=0.8 contre la série retenue.

| variante | imputation | modèle | famille | cle_imputation | cle_modele | pinball τ=0.8 retenue | MAE retenue | MAE propre | pinball τ=0.8 propre | temps (s) | DM p vs paire retenue | DM p vs imputation retenue, même modèle | p Holm vs paire retenue | vs paire retenue | p Holm vs imputation retenue, même modèle | vs imputation retenue, même modèle |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Moyenne du service | SVR quantile, noyau laplacien | svm | moyenne | svr_q_laplacien | 0.8956 | 2.673 | 2.652 | 0.9235 | 2.2 | 0.3035 | 0.4724 | 1.0 | équivalent | 1.0 | équivalent |
| 1 | Moyenne du service | SVR quantile RBF (niveau 3) | svm | moyenne | svr_q_rbf | 0.902 | 2.662 | 2.642 | 0.9264 | 2.9 | 0.2594 | 0.2883 | 1.0 | équivalent | 1.0 | équivalent |
| 2 | Hybride : prix, sinon XGBoost | SVR quantile, noyau laplacien | svm | hybride | svr_q_laplacien | 0.9242 | 2.745 | 2.747 | 0.9197 | 2.2 | 0.1422 | 0.0883 | 1.0 | équivalent | 1.0 | équivalent |
| 3 | XGBoost (avec le diagnostic) | SVR quantile, noyau laplacien | svm | xgboost | svr_q_laplacien | 0.9268 | 2.744 | 2.752 | 0.9212 | 2.2 | 0.263 | 0.8987 | 1.0 | équivalent | 1.0 | équivalent |
| 4 | Estimée : prix, puis issue, puis médiane | SVR quantile, noyau laplacien | svm | estimee | svr_q_laplacien | 0.9274 | 2.707 | 2.707 | 0.9274 | 2.1 | 0.189 |  | 1.0 | équivalent |  | — référence |
| 5 | Moyenne du service | SVR quantile composite (niveau 4, retenu) | svm | moyenne | svr_q_composite | 0.9276 | 2.668 | 2.651 | 0.9489 | 5.9 | 0.402 | 0.402 | 1.0 | équivalent | 1.0 | équivalent |
| 6 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile, noyau laplacien | svm | knn | svr_q_laplacien | 0.9278 | 2.69 | 2.709 | 0.9447 | 3.3 | 0.1943 | 0.7848 | 1.0 | équivalent | 1.0 | équivalent |
| 7 | Régressions enchaînées (ridge, principe de MICE) | A · forêt aléatoire quantile | concurrent | regression | foret | 0.9281 | 2.682 | 2.682 | 0.9281 | 8.3 | 0.6892 | 0.0587 | 1.0 | équivalent | 1.0 | équivalent |
| 8 | k plus proches voisins (prix, âge, sexe, issue, mois) | A · forêt aléatoire quantile | concurrent | knn | foret | 0.9282 | 2.636 | 2.661 | 0.9451 | 10.3 | 0.6949 | 0.015 | 1.0 | équivalent | 1.0 | équivalent |
| 9 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile, noyau laplacien | svm | regression | svr_q_laplacien | 0.9292 | 2.696 | 2.696 | 0.9292 | 3.7 | 0.3147 | 0.6897 | 1.0 | équivalent | 1.0 | équivalent |
| 10 | Loi normale multivariée par EM | SVR quantile, noyau laplacien | svm | em | svr_q_laplacien | 0.9293 | 2.698 | 2.698 | 0.9293 | 1.6 | 0.3162 | 0.6705 | 1.0 | équivalent | 1.0 | équivalent |
| 11 | Médiane de la tranche d'âge | SVR quantile, noyau laplacien | svm | mediane_age | svr_q_laplacien | 0.9293 | 2.703 | 2.707 | 0.9327 | 2.8 | 0.242 | 0.4173 | 1.0 | équivalent | 1.0 | équivalent |
| 12 | Médiane du service | SVR quantile, noyau laplacien | svm | mediane | svr_q_laplacien | 0.9293 | 2.703 | 2.707 | 0.9327 | 3.9 | 0.242 | 0.4173 | 1.0 | équivalent | 1.0 | équivalent |
| 13 | SoftImpute (norme nucléaire) | SVR quantile, noyau laplacien | svm | softimpute | svr_q_laplacien | 0.9295 | 2.697 | 2.696 | 0.9305 | 3.5 | 0.2426 | 0.3381 | 1.0 | équivalent | 1.0 | équivalent |
| 14 | XGBoost (avec le diagnostic) | SVR quantile RBF (niveau 3) | svm | xgboost | svr_q_rbf | 0.9305 | 2.772 | 2.782 | 0.9248 | 1.5 | 0.1367 | 0.0139 | 1.0 | équivalent | 1.0 | équivalent |
| 15 | ACP itérative (rang faible) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | acp_iterative | lssvr_rbf | 0.9328 | 2.662 | 2.757 | 0.9549 | 0.2 | 0.7426 | 0.9444 | 1.0 | équivalent | 1.0 | équivalent |
| 16 | Hybride : prix, sinon XGBoost | SVR quantile RBF (niveau 3) | svm | hybride | svr_q_rbf | 0.9336 | 2.772 | 2.776 | 0.9291 | 2.0 | 0.1047 | 0.055 | 1.0 | équivalent | 1.0 | équivalent |
| 17 | Loi normale multivariée par EM | SVR quantile RBF (niveau 3) | svm | em | svr_q_rbf | 0.9337 | 2.724 | 2.724 | 0.9337 | 2.8 | 0.3149 | 0.2517 | 1.0 | équivalent | 1.0 | équivalent |
| 18 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile RBF (niveau 3) | svm | regression | svr_q_rbf | 0.9339 | 2.722 | 2.722 | 0.9339 | 2.0 | 0.3196 | 0.2535 | 1.0 | équivalent | 1.0 | équivalent |
| 19 | XGBoost (avec le diagnostic) | SVR quantile composite (niveau 4, retenu) | svm | xgboost | svr_q_composite | 0.9343 | 2.757 | 2.766 | 0.9299 | 4.1 | 0.0068 | 0.0068 | 0.7102 | équivalent | 0.8364 | équivalent |
| 20 | SoftImpute (norme nucléaire) | A · forêt aléatoire quantile | concurrent | softimpute | foret | 0.9344 | 2.712 | 2.706 | 0.9355 | 10.5 | 0.8066 | 0.2162 | 1.0 | équivalent | 1.0 | équivalent |
| 21 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile RBF (niveau 3) | svm | knn | svr_q_rbf | 0.9346 | 2.715 | 2.735 | 0.9508 | 1.7 | 0.1051 | 0.0191 | 1.0 | équivalent | 1.0 | équivalent |
| 22 | Estimée : prix, puis issue, puis médiane | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | estimee | lssvr_rbf | 0.935 | 2.659 | 2.659 | 0.935 | 0.2 | 0.7618 |  | 1.0 | équivalent |  | — référence |
| 23 | Loi normale multivariée par EM | A · forêt aléatoire quantile | concurrent | em | foret | 0.9357 | 2.714 | 2.714 | 0.9357 | 10.2 | 0.833 | 0.1685 | 1.0 | équivalent | 1.0 | équivalent |
| 24 | XGBoost (avec le diagnostic) | A · forêt aléatoire quantile | concurrent | xgboost | foret | 0.938 | 2.743 | 2.745 | 0.9324 | 8.4 | 0.8722 | 0.1101 | 1.0 | équivalent | 1.0 | équivalent |
| 25 | Régressions enchaînées (ridge, principe de MICE) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | regression | lssvr_rbf | 0.9385 | 2.664 | 2.664 | 0.9385 | 0.4 | 0.8327 | 0.5788 | 1.0 | équivalent | 1.0 | équivalent |
| 26 | SoftImpute (norme nucléaire) | SVR quantile RBF (niveau 3) | svm | softimpute | svr_q_rbf | 0.9388 | 2.722 | 2.724 | 0.939 | 1.8 | 0.3643 | 0.5732 | 1.0 | équivalent | 1.0 | équivalent |
| 27 | Médiane du service | SVR quantile RBF (niveau 3) | svm | mediane | svr_q_rbf | 0.9395 | 2.725 | 2.731 | 0.9419 | 1.7 | 0.429 | 0.7865 | 1.0 | équivalent | 1.0 | équivalent |
| 28 | Médiane de la tranche d'âge | SVR quantile RBF (niveau 3) | svm | mediane_age | svr_q_rbf | 0.9395 | 2.725 | 2.731 | 0.9419 | 2.2 | 0.429 | 0.7865 | 1.0 | équivalent | 1.0 | équivalent |
| 29 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile composite (niveau 4, retenu) | svm | regression | svr_q_composite | 0.9396 | 2.72 | 2.72 | 0.9396 | 4.7 | 0.0812 | 0.0812 | 1.0 | équivalent | 1.0 | équivalent |
| 30 | Loi normale multivariée par EM | SVR quantile composite (niveau 4, retenu) | svm | em | svr_q_composite | 0.9397 | 2.718 | 2.718 | 0.9397 | 4.2 | 0.0765 | 0.0765 | 1.0 | équivalent | 1.0 | équivalent |
| 31 | Estimée : prix, puis issue, puis médiane | SVR quantile RBF (niveau 3) | svm | estimee | svr_q_rbf | 0.9401 | 2.744 | 2.744 | 0.9401 | 2.6 | 0.538 |  | 1.0 | équivalent |  | — référence |
| 32 | Loi normale multivariée par EM | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | em | lssvr_rbf | 0.9411 | 2.677 | 2.677 | 0.9411 | 0.3 | 0.9048 | 0.2856 | 1.0 | équivalent | 1.0 | équivalent |
| 33 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile composite (niveau 4, retenu) | svm | knn | svr_q_composite | 0.9414 | 2.697 | 2.717 | 0.957 | 5.6 | 0.0621 | 0.0621 | 1.0 | équivalent | 1.0 | équivalent |
| 34 | Hybride : prix, sinon XGBoost | SVR quantile composite (niveau 4, retenu) | svm | hybride | svr_q_composite | 0.9422 | 2.758 | 2.761 | 0.9377 | 3.4 | 0.4466 | 0.4466 | 1.0 | équivalent | 1.0 | équivalent |
| 35 | ACP itérative (rang faible) | A · forêt aléatoire quantile | concurrent | acp_iterative | foret | 0.9426 | 2.657 | 2.754 | 0.9878 | 8.2 | 0.9713 | 0.5842 | 1.0 | équivalent | 1.0 | équivalent |
| 36 | Médiane de la tranche d'âge | A · forêt aléatoire quantile | concurrent | mediane_age | foret | 0.9444 | 2.712 | 2.715 | 0.9478 | 10.1 | 0.9936 | 0.4667 | 1.0 | équivalent | 1.0 | équivalent |
| 37 | Médiane du service | A · forêt aléatoire quantile | concurrent | mediane | foret | 0.9444 | 2.712 | 2.715 | 0.9478 | 8.4 | 0.9936 | 0.4667 | 1.0 | équivalent | 1.0 | équivalent |
| 38 | Hybride : prix, sinon XGBoost | A · forêt aléatoire quantile | concurrent | hybride | foret | 0.9445 | 2.729 | 2.725 | 0.9399 | 7.8 | 0.9951 | 0.1611 | 1.0 | équivalent | 1.0 | équivalent |
| 39 | Estimée : prix, puis issue, puis médiane | SVR quantile composite (niveau 4, retenu) | svm | estimee | svr_q_composite | 0.9447 | 2.719 | 2.719 | 0.9447 | 4.0 |  |  |  | — référence |  | — référence |
| 40 | Moyenne du service | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | moyenne | lssvr_rbf | 0.9478 | 2.67 | 2.702 | 0.9668 | 0.2 | 0.9224 | 0.4582 | 1.0 | équivalent | 1.0 | équivalent |
| 41 | XGBoost (avec le diagnostic) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | xgboost | lssvr_rbf | 0.9484 | 2.683 | 2.67 | 0.9485 | 0.2 | 0.9163 | 0.1704 | 1.0 | équivalent | 1.0 | équivalent |
| 42 | XGBoost (avec le diagnostic) | SVR quantile, noyau polynomial (degré 2) | svm | xgboost | svr_q_polynomial | 0.9487 | 2.825 | 2.829 | 0.943 | 2.9 | 0.8176 | 0.1339 | 1.0 | équivalent | 1.0 | équivalent |
| 43 | k plus proches voisins (prix, âge, sexe, issue, mois) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | knn | lssvr_rbf | 0.9499 | 2.664 | 2.685 | 0.9612 | 0.4 | 0.8852 | 0.1809 | 1.0 | équivalent | 1.0 | équivalent |
| 44 | SoftImpute (norme nucléaire) | SVR quantile composite (niveau 4, retenu) | svm | softimpute | svr_q_composite | 0.9504 | 2.696 | 2.698 | 0.9498 | 4.6 | 0.0944 | 0.0944 | 1.0 | équivalent | 1.0 | équivalent |
| 45 | Médiane du service | SVR quantile composite (niveau 4, retenu) | svm | mediane | svr_q_composite | 0.9507 | 2.705 | 2.709 | 0.9524 | 4.4 | 0.0967 | 0.0967 | 1.0 | équivalent | 1.0 | équivalent |
| 46 | Médiane de la tranche d'âge | SVR quantile composite (niveau 4, retenu) | svm | mediane_age | svr_q_composite | 0.9507 | 2.705 | 2.709 | 0.9524 | 5.1 | 0.0967 | 0.0967 | 1.0 | équivalent | 1.0 | équivalent |
| 47 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile, noyau polynomial (degré 2) | svm | regression | svr_q_polynomial | 0.951 | 2.797 | 2.797 | 0.951 | 2.9 | 0.7244 | 0.0976 | 1.0 | équivalent | 1.0 | équivalent |
| 48 | Hybride : prix, sinon XGBoost | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | hybride | lssvr_rbf | 0.9512 | 2.688 | 2.67 | 0.9469 | 0.2 | 0.8589 | 0.1127 | 1.0 | équivalent | 1.0 | équivalent |
| 49 | Loi normale multivariée par EM | SVR quantile, noyau polynomial (degré 2) | svm | em | svr_q_polynomial | 0.9512 | 2.784 | 2.784 | 0.9512 | 3.7 | 0.7256 | 0.1753 | 1.0 | équivalent | 1.0 | équivalent |
| 50 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile, noyau polynomial (degré 2) | svm | knn | svr_q_polynomial | 0.9513 | 2.757 | 2.78 | 0.9664 | 5.9 | 0.7712 | 0.6773 | 1.0 | équivalent | 1.0 | équivalent |
| 51 | Estimée : prix, puis issue, puis médiane | SVR quantile, noyau polynomial (degré 2) | svm | estimee | svr_q_polynomial | 0.954 | 2.789 | 2.789 | 0.954 | 3.8 | 0.6129 |  | 1.0 | équivalent |  | — référence |
| 52 | Hybride : prix, sinon XGBoost | SVR quantile, noyau polynomial (degré 2) | svm | hybride | svr_q_polynomial | 0.9556 | 2.825 | 2.825 | 0.9511 | 2.6 | 0.5824 | 0.8057 | 1.0 | équivalent | 1.0 | équivalent |
| 53 | SoftImpute (norme nucléaire) | SVR quantile, noyau polynomial (degré 2) | svm | softimpute | svr_q_polynomial | 0.9584 | 2.769 | 2.772 | 0.9583 | 3.7 | 0.5626 | 0.6072 | 1.0 | équivalent | 1.0 | équivalent |
| 54 | Estimée : prix, puis issue, puis médiane | A · forêt aléatoire quantile | concurrent | estimee | foret | 0.9587 | 2.691 | 2.691 | 0.9587 | 11.2 | 0.7914 |  | 1.0 | équivalent |  | — référence |
| 55 | Médiane du service | SVR quantile, noyau polynomial (degré 2) | svm | mediane | svr_q_polynomial | 0.9607 | 2.773 | 2.778 | 0.9627 | 3.6 | 0.5179 | 0.4765 | 1.0 | équivalent | 1.0 | équivalent |
| 56 | Médiane de la tranche d'âge | SVR quantile, noyau polynomial (degré 2) | svm | mediane_age | svr_q_polynomial | 0.9607 | 2.773 | 2.778 | 0.9627 | 4.7 | 0.5179 | 0.4765 | 1.0 | équivalent | 1.0 | équivalent |
| 57 | Moyenne du service | A · forêt aléatoire quantile | concurrent | moyenne | foret | 0.962 | 2.686 | 2.68 | 0.9844 | 8.1 | 0.6783 | 0.9189 | 1.0 | équivalent | 1.0 | équivalent |
| 58 | ACP itérative (rang faible) | SVR quantile, noyau laplacien | svm | acp_iterative | svr_q_laplacien | 0.9638 | 2.766 | 2.863 | 0.995 | 2.7 | 0.343 | 0.0517 | 1.0 | équivalent | 1.0 | équivalent |
| 59 | Moyenne du service | SVR quantile, noyau polynomial (degré 2) | svm | moyenne | svr_q_polynomial | 0.9646 | 2.703 | 2.689 | 0.9879 | 5.4 | 0.3905 | 0.5052 | 1.0 | équivalent | 1.0 | équivalent |
| 60 | ACP itérative (rang faible) | SVR quantile composite (niveau 4, retenu) | svm | acp_iterative | svr_q_composite | 0.9667 | 2.725 | 2.811 | 0.9962 | 4.0 | 0.1283 | 0.1283 | 1.0 | équivalent | 1.0 | équivalent |
| 61 | ACP itérative (rang faible) | SVR quantile RBF (niveau 3) | svm | acp_iterative | svr_q_rbf | 0.967 | 2.732 | 2.827 | 0.998 | 3.6 | 0.1935 | 0.1542 | 1.0 | équivalent | 1.0 | équivalent |
| 62 | Médiane du service | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | mediane | lssvr_rbf | 0.9703 | 2.714 | 2.695 | 0.9664 | 0.5 | 0.512 | 0.0048 | 1.0 | équivalent | 0.6096 | équivalent |
| 63 | Médiane de la tranche d'âge | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | mediane_age | lssvr_rbf | 0.9703 | 2.714 | 2.695 | 0.9664 | 0.5 | 0.512 | 0.0048 | 1.0 | équivalent | 0.6096 | équivalent |
| 64 | SoftImpute (norme nucléaire) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | softimpute | lssvr_rbf | 0.9763 | 2.709 | 2.692 | 0.9732 | 0.3 | 0.4527 | 0.0057 | 1.0 | équivalent | 0.7125 | équivalent |
| 65 | ACP itérative (rang faible) | SVR quantile, noyau polynomial (degré 2) | svm | acp_iterative | svr_q_polynomial | 0.9798 | 2.801 | 2.885 | 1.0134 | 3.1 | 0.3214 | 0.3259 | 1.0 | équivalent | 1.0 | équivalent |
| 66 | SoftImpute (norme nucléaire) | C · perceptron multicouche quantile | concurrent | softimpute | mlp | 1.015 | 3.048 | 3.028 | 1.0105 | 0.9 | 0.3863 | 0.2931 | 1.0 | équivalent | 1.0 | équivalent |
| 67 | Moyenne du service | C · perceptron multicouche quantile | concurrent | moyenne | mlp | 1.0152 | 3.1 | 3.087 | 1.032 | 1.2 | 0.1638 | 0.3511 | 1.0 | équivalent | 1.0 | équivalent |
| 68 | Loi normale multivariée par EM | C · perceptron multicouche quantile | concurrent | em | mlp | 1.021 | 2.996 | 2.996 | 1.021 | 1.0 | 0.1754 | 0.0978 | 1.0 | équivalent | 1.0 | équivalent |
| 69 | Médiane du service | C · perceptron multicouche quantile | concurrent | mediane | mlp | 1.0284 | 3.019 | 3.009 | 1.0241 | 1.0 | 0.1418 | 0.2037 | 1.0 | équivalent | 1.0 | équivalent |
| 70 | Médiane de la tranche d'âge | C · perceptron multicouche quantile | concurrent | mediane_age | mlp | 1.0284 | 3.019 | 3.009 | 1.0241 | 1.4 | 0.1418 | 0.2037 | 1.0 | équivalent | 1.0 | équivalent |
| 71 | Régressions enchaînées (ridge, principe de MICE) | C · perceptron multicouche quantile | concurrent | regression | mlp | 1.0317 | 3.021 | 3.021 | 1.0317 | 0.7 | 0.0927 | 0.332 | 1.0 | équivalent | 1.0 | équivalent |
| 72 | Hybride : prix, sinon XGBoost | C · perceptron multicouche quantile | concurrent | hybride | mlp | 1.033 | 3.085 | 3.079 | 1.0285 | 0.9 | 0.267 | 0.4643 | 1.0 | équivalent | 1.0 | équivalent |
| 73 | k plus proches voisins (prix, âge, sexe, issue, mois) | C · perceptron multicouche quantile | concurrent | knn | mlp | 1.0452 | 3.006 | 3.022 | 1.0571 | 0.8 | 0.1008 | 0.6235 | 1.0 | équivalent | 1.0 | équivalent |
| 74 | Estimée : prix, puis issue, puis médiane | C · perceptron multicouche quantile | concurrent | estimee | mlp | 1.0586 | 3.087 | 3.087 | 1.0586 | 0.7 | 0.0696 |  | 1.0 | équivalent |  | — référence |
| 75 | XGBoost (avec le diagnostic) | C · perceptron multicouche quantile | concurrent | xgboost | mlp | 1.0718 | 3.019 | 3.017 | 1.0718 | 1.4 | 0.0975 | 0.637 | 1.0 | équivalent | 1.0 | équivalent |
| 76 | ACP itérative (rang faible) | C · perceptron multicouche quantile | concurrent | acp_iterative | mlp | 1.0794 | 3.143 | 3.222 | 1.1245 | 0.8 | 0.0158 | 0.6649 | 1.0 | équivalent | 1.0 | équivalent |
| 77 | ACP itérative (rang faible) | B · gradient boosting quantile | concurrent | acp_iterative | boosting | 1.1078 | 2.885 | 2.991 | 1.1669 | 5.8 | 0.0867 | 0.0173 | 1.0 | équivalent | 1.0 | équivalent |
| 78 | Moyenne du service | D · LSTM quantile | concurrent | moyenne | lstm | 1.1241 | 3.127 | 3.109 | 1.1404 | 5.7 | 0.0003 | 0.2509 | 0.036 | moins bon | 1.0 | équivalent |
| 79 | Exclure les séjours sans durée | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | exclure | lssvr_rbf | 1.1353 | 3.234 | 3.133 | 1.0909 | 0.3 | 0.0708 | 0.0233 | 1.0 | équivalent | 1.0 | équivalent |
| 80 | Moyenne du service | B · gradient boosting quantile | concurrent | moyenne | boosting | 1.1546 | 2.816 | 2.818 | 1.1787 | 7.8 | 0.0813 | 0.2277 | 1.0 | équivalent | 1.0 | équivalent |
| 81 | Exclure les séjours sans durée | SVR quantile, noyau polynomial (degré 2) | svm | exclure | svr_q_polynomial | 1.156 | 3.271 | 3.165 | 1.1087 | 3.2 | 0.0405 | 0.0263 | 1.0 | équivalent | 1.0 | équivalent |
| 82 | k plus proches voisins (prix, âge, sexe, issue, mois) | E · XGBoost quantile (second ordre) | concurrent | knn | xgboost | 1.1562 | 2.804 | 2.824 | 1.1736 | 7.8 | 0.0531 | 0.3987 | 1.0 | équivalent | 1.0 | équivalent |
| 83 | SoftImpute (norme nucléaire) | E · XGBoost quantile (second ordre) | concurrent | softimpute | xgboost | 1.1701 | 2.83 | 2.827 | 1.1713 | 7.7 | 0.0556 | 0.7191 | 1.0 | équivalent | 1.0 | équivalent |
| 84 | ACP itérative (rang faible) | D · LSTM quantile | concurrent | acp_iterative | lstm | 1.1707 | 3.242 | 3.317 | 1.2027 | 5.3 | 0.0041 | 0.3946 | 0.451 | équivalent | 1.0 | équivalent |
| 85 | Médiane du service | B · gradient boosting quantile | concurrent | mediane | boosting | 1.1739 | 2.821 | 2.822 | 1.1823 | 6.8 | 0.0544 | 0.3132 | 1.0 | équivalent | 1.0 | équivalent |
| 86 | Médiane de la tranche d'âge | B · gradient boosting quantile | concurrent | mediane_age | boosting | 1.1739 | 2.821 | 2.822 | 1.1823 | 7.5 | 0.0544 | 0.3132 | 1.0 | équivalent | 1.0 | équivalent |
| 87 | Régressions enchaînées (ridge, principe de MICE) | E · XGBoost quantile (second ordre) | concurrent | regression | xgboost | 1.1749 | 2.829 | 2.829 | 1.1749 | 7.1 | 0.0424 | 0.7983 | 1.0 | équivalent | 1.0 | équivalent |
| 88 | Exclure les séjours sans durée | A · forêt aléatoire quantile | concurrent | exclure | foret | 1.1774 | 3.319 | 3.177 | 1.1363 | 9.6 | 0.0316 | 0.0067 | 1.0 | équivalent | 0.8308 | équivalent |
| 89 | Régressions enchaînées (ridge, principe de MICE) | D · LSTM quantile | concurrent | regression | lstm | 1.1784 | 3.314 | 3.314 | 1.1784 | 4.8 | 0.0041 | 0.439 | 0.451 | équivalent | 1.0 | équivalent |
| 90 | Moyenne du service | E · XGBoost quantile (second ordre) | concurrent | moyenne | xgboost | 1.1787 | 2.89 | 2.877 | 1.2017 | 8.9 | 0.0276 | 0.9774 | 1.0 | équivalent | 1.0 | équivalent |
| 91 | Médiane du service | D · LSTM quantile | concurrent | mediane | lstm | 1.1788 | 3.39 | 3.381 | 1.177 | 6.7 | 0.0067 | 0.4824 | 0.7102 | équivalent | 1.0 | équivalent |
| 92 | Médiane de la tranche d'âge | D · LSTM quantile | concurrent | mediane_age | lstm | 1.1788 | 3.39 | 3.381 | 1.177 | 7.4 | 0.0067 | 0.4824 | 0.7102 | équivalent | 1.0 | équivalent |
| 93 | Loi normale multivariée par EM | D · LSTM quantile | concurrent | em | lstm | 1.1794 | 3.312 | 3.312 | 1.1794 | 7.5 | 0.0037 | 0.4703 | 0.4144 | équivalent | 1.0 | équivalent |
| 94 | Estimée : prix, puis issue, puis médiane | E · XGBoost quantile (second ordre) | concurrent | estimee | xgboost | 1.1802 | 2.844 | 2.844 | 1.1802 | 7.8 | 0.0548 |  | 1.0 | équivalent |  | — référence |
| 95 | Exclure les séjours sans durée | SVR quantile composite (niveau 4, retenu) | svm | exclure | svr_q_composite | 1.1831 | 3.096 | 3.044 | 1.1384 | 5.2 | 0.0187 | 0.0187 | 1.0 | équivalent | 1.0 | équivalent |
| 96 | XGBoost (avec le diagnostic) | D · LSTM quantile | concurrent | xgboost | lstm | 1.1844 | 3.336 | 3.32 | 1.1839 | 8.8 | 0.0039 | 0.7322 | 0.4329 | équivalent | 1.0 | équivalent |
| 97 | Loi normale multivariée par EM | E · XGBoost quantile (second ordre) | concurrent | em | xgboost | 1.185 | 2.729 | 2.729 | 1.185 | 8.8 | 0.0408 | 0.8355 | 1.0 | équivalent | 1.0 | équivalent |
| 98 | ACP itérative (rang faible) | E · XGBoost quantile (second ordre) | concurrent | acp_iterative | xgboost | 1.1853 | 2.777 | 2.87 | 1.2332 | 6.9 | 0.0448 | 0.8857 | 1.0 | équivalent | 1.0 | équivalent |
| 99 | XGBoost (avec le diagnostic) | E · XGBoost quantile (second ordre) | concurrent | xgboost | xgboost | 1.1854 | 2.862 | 2.856 | 1.1862 | 8.5 | 0.0295 | 0.843 | 1.0 | équivalent | 1.0 | équivalent |
| 100 | Loi normale multivariée par EM | B · gradient boosting quantile | concurrent | em | boosting | 1.1861 | 2.834 | 2.834 | 1.1861 | 5.9 | 0.0486 | 0.2709 | 1.0 | équivalent | 1.0 | équivalent |
| 101 | Médiane de la tranche d'âge | E · XGBoost quantile (second ordre) | concurrent | mediane_age | xgboost | 1.1863 | 2.832 | 2.832 | 1.1896 | 9.4 | 0.0492 | 0.854 | 1.0 | équivalent | 1.0 | équivalent |
| 102 | Médiane du service | E · XGBoost quantile (second ordre) | concurrent | mediane | xgboost | 1.1863 | 2.832 | 2.832 | 1.1896 | 8.0 | 0.0492 | 0.854 | 1.0 | équivalent | 1.0 | équivalent |
| 103 | Hybride : prix, sinon XGBoost | B · gradient boosting quantile | concurrent | hybride | boosting | 1.1865 | 2.855 | 2.844 | 1.1854 | 7.7 | 0.0623 | 0.5157 | 1.0 | équivalent | 1.0 | équivalent |
| 104 | k plus proches voisins (prix, âge, sexe, issue, mois) | B · gradient boosting quantile | concurrent | knn | boosting | 1.1923 | 2.809 | 2.832 | 1.2058 | 7.2 | 0.0332 | 0.6019 | 1.0 | équivalent | 1.0 | équivalent |
| 105 | Hybride : prix, sinon XGBoost | D · LSTM quantile | concurrent | hybride | lstm | 1.1956 | 3.325 | 3.304 | 1.1906 | 5.9 | 0.0061 | 0.992 | 0.6527 | équivalent | 1.0 | équivalent |
| 106 | Régressions enchaînées (ridge, principe de MICE) | B · gradient boosting quantile | concurrent | regression | boosting | 1.1958 | 2.827 | 2.827 | 1.1958 | 5.9 | 0.032 | 0.5521 | 1.0 | équivalent | 1.0 | équivalent |
| 107 | Estimée : prix, puis issue, puis médiane | D · LSTM quantile | concurrent | estimee | lstm | 1.196 | 3.291 | 3.291 | 1.196 | 5.4 | 0.0031 |  | 0.3503 | équivalent |  | — référence |
| 108 | XGBoost (avec le diagnostic) | B · gradient boosting quantile | concurrent | xgboost | boosting | 1.1972 | 2.86 | 2.855 | 1.1955 | 7.1 | 0.0562 | 0.7674 | 1.0 | équivalent | 1.0 | équivalent |
| 109 | k plus proches voisins (prix, âge, sexe, issue, mois) | D · LSTM quantile | concurrent | knn | lstm | 1.2014 | 3.276 | 3.306 | 1.2127 | 5.7 | 0.001 | 0.8469 | 0.118 | équivalent | 1.0 | équivalent |
| 110 | Hybride : prix, sinon XGBoost | E · XGBoost quantile (second ordre) | concurrent | hybride | xgboost | 1.2032 | 2.905 | 2.893 | 1.1986 | 7.6 | 0.0441 | 0.4296 | 1.0 | équivalent | 1.0 | équivalent |
| 111 | SoftImpute (norme nucléaire) | B · gradient boosting quantile | concurrent | softimpute | boosting | 1.2033 | 2.82 | 2.817 | 1.2053 | 8.0 | 0.0619 | 0.9159 | 1.0 | équivalent | 1.0 | équivalent |
| 112 | SoftImpute (norme nucléaire) | D · LSTM quantile | concurrent | softimpute | lstm | 1.2036 | 3.404 | 3.393 | 1.2003 | 6.4 | 0.0047 | 0.8061 | 0.5076 | équivalent | 1.0 | équivalent |
| 113 | Exclure les séjours sans durée | SVR quantile RBF (niveau 3) | svm | exclure | svr_q_rbf | 1.2053 | 3.225 | 3.168 | 1.161 | 1.7 | 0.0163 | 0.0166 | 1.0 | équivalent | 1.0 | équivalent |
| 114 | Estimée : prix, puis issue, puis médiane | B · gradient boosting quantile | concurrent | estimee | boosting | 1.2069 | 2.817 | 2.817 | 1.2069 | 5.7 | 0.0291 |  | 1.0 | équivalent |  | — référence |
| 115 | Exclure les séjours sans durée | SVR quantile, noyau laplacien | svm | exclure | svr_q_laplacien | 1.2232 | 3.257 | 3.198 | 1.1811 | 2.2 | 0.0112 | 0.0073 | 1.0 | équivalent | 0.8906 | équivalent |
| 116 | Exclure les séjours sans durée | C · perceptron multicouche quantile | concurrent | exclure | mlp | 1.3565 | 4.106 | 3.986 | 1.2995 | 1.1 | 0.0021 | 0.0076 | 0.2394 | équivalent | 0.9196 | équivalent |
| 117 | Exclure les séjours sans durée | E · XGBoost quantile (second ordre) | concurrent | exclure | xgboost | 1.5757 | 3.472 | 3.335 | 1.4781 | 7.5 | 0.0012 | 0.0004 | 0.1404 | équivalent | 0.052 | équivalent |
| 118 | Exclure les séjours sans durée | D · LSTM quantile | concurrent | exclure | lstm | 1.5883 | 3.756 | 3.66 | 1.5415 | 7.0 | 0.0012 | 0.0025 | 0.1404 | équivalent | 0.3225 | équivalent |
| 119 | ACP itérative (rang faible) | SVR RBF (niveau 2) | svm | acp_iterative | svr_rbf | 1.6229 | 2.59 | 2.687 | 1.697 | 1.2 | 0.0002 | 0.3933 | 0.0252 | moins bon | 1.0 | équivalent |
| 120 | Moyenne du service | SVR RBF (niveau 2) | svm | moyenne | svr_rbf | 1.6536 | 2.738 | 2.738 | 1.6908 | 1.0 | 0.0003 | 0.974 | 0.036 | moins bon | 1.0 | équivalent |
| 121 | Estimée : prix, puis issue, puis médiane | SVR RBF (niveau 2) | svm | estimee | svr_rbf | 1.6544 | 2.682 | 2.682 | 1.6544 | 1.4 | 0.0001 |  | 0.0141 | moins bon |  | — référence |
| 122 | Régressions enchaînées (ridge, principe de MICE) | SVR RBF (niveau 2) | svm | regression | svr_rbf | 1.6605 | 2.678 | 2.678 | 1.6605 | 1.3 | 0.0001 | 0.4027 | 0.0141 | moins bon | 1.0 | équivalent |
| 123 | Exclure les séjours sans durée | B · gradient boosting quantile | concurrent | exclure | boosting | 1.6617 | 3.367 | 3.223 | 1.5152 | 7.9 | 0.0013 | 0.0031 | 0.1495 | équivalent | 0.3968 | équivalent |
| 124 | Loi normale multivariée par EM | SVR RBF (niveau 2) | svm | em | svr_rbf | 1.6654 | 2.673 | 2.673 | 1.6654 | 1.7 | 0.0002 | 0.2646 | 0.0252 | moins bon | 1.0 | équivalent |
| 125 | XGBoost (avec le diagnostic) | SVR RBF (niveau 2) | svm | xgboost | svr_rbf | 1.68 | 2.677 | 2.674 | 1.6701 | 1.7 | 0.0001 | 0.2281 | 0.0141 | moins bon | 1.0 | équivalent |
| 126 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR RBF (niveau 2) | svm | knn | svr_rbf | 1.68 | 2.693 | 2.714 | 1.6991 | 1.4 | 0.0002 | 0.1751 | 0.0252 | moins bon | 1.0 | équivalent |
| 127 | Hybride : prix, sinon XGBoost | SVR RBF (niveau 2) | svm | hybride | svr_rbf | 1.6905 | 2.699 | 2.69 | 1.6756 | 1.5 | 0.0001 | 0.0668 | 0.0141 | moins bon | 1.0 | équivalent |
| 128 | SoftImpute (norme nucléaire) | SVR RBF (niveau 2) | svm | softimpute | svr_rbf | 1.706 | 2.731 | 2.721 | 1.6997 | 0.8 | 0.0002 | 0.0739 | 0.0252 | moins bon | 1.0 | équivalent |
| 129 | Médiane du service | SVR RBF (niveau 2) | svm | mediane | svr_rbf | 1.7096 | 2.715 | 2.706 | 1.6998 | 1.6 | 0.0002 | 0.0501 | 0.0252 | moins bon | 1.0 | équivalent |
| 130 | Médiane de la tranche d'âge | SVR RBF (niveau 2) | svm | mediane_age | svr_rbf | 1.7096 | 2.715 | 2.706 | 1.6998 | 1.7 | 0.0002 | 0.0501 | 0.0252 | moins bon | 1.0 | équivalent |
| 131 | Moyenne du service | SVR linéaire (niveau 1) | svm | moyenne | svr_lineaire | 1.8054 | 2.999 | 3.027 | 1.8564 | 1.5 | 0.0001 | 0.61 | 0.0141 | moins bon | 1.0 | équivalent |
| 132 | ACP itérative (rang faible) | SVR linéaire (niveau 1) | svm | acp_iterative | svr_lineaire | 1.8147 | 2.898 | 3.002 | 1.8921 | 1.2 | 0.0001 | 0.9544 | 0.0141 | moins bon | 1.0 | équivalent |
| 133 | Estimée : prix, puis issue, puis médiane | SVR linéaire (niveau 1) | svm | estimee | svr_lineaire | 1.8176 | 2.938 | 2.938 | 1.8176 | 1.6 | 0.0001 |  | 0.0141 | moins bon |  | — référence |
| 134 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR linéaire (niveau 1) | svm | knn | svr_lineaire | 1.8298 | 2.936 | 2.964 | 1.8526 | 1.3 | 0.0001 | 0.5229 | 0.0141 | moins bon | 1.0 | équivalent |
| 135 | Régressions enchaînées (ridge, principe de MICE) | SVR linéaire (niveau 1) | svm | regression | svr_lineaire | 1.8322 | 2.938 | 2.938 | 1.8322 | 1.3 | 0.0001 | 0.2869 | 0.0141 | moins bon | 1.0 | équivalent |
| 136 | SoftImpute (norme nucléaire) | SVR linéaire (niveau 1) | svm | softimpute | svr_lineaire | 1.8342 | 2.945 | 2.957 | 1.8387 | 0.8 | 0.0001 | 0.5522 | 0.0141 | moins bon | 1.0 | équivalent |
| 137 | Loi normale multivariée par EM | SVR linéaire (niveau 1) | svm | em | svr_lineaire | 1.8399 | 2.944 | 2.944 | 1.8399 | 0.7 | 0.0001 | 0.1709 | 0.0141 | moins bon | 1.0 | équivalent |
| 138 | XGBoost (avec le diagnostic) | SVR linéaire (niveau 1) | svm | xgboost | svr_lineaire | 1.8434 | 2.962 | 2.967 | 1.8377 | 0.9 | 0.0001 | 0.06 | 0.0141 | moins bon | 1.0 | équivalent |
| 139 | Hybride : prix, sinon XGBoost | SVR linéaire (niveau 1) | svm | hybride | svr_lineaire | 1.8474 | 2.975 | 2.975 | 1.8371 | 0.9 | 0.0001 | 0.0804 | 0.0141 | moins bon | 1.0 | équivalent |
| 140 | Médiane de la tranche d'âge | SVR linéaire (niveau 1) | svm | mediane_age | svr_lineaire | 1.8518 | 2.981 | 2.995 | 1.8536 | 1.6 | 0.0001 | 0.4021 | 0.0141 | moins bon | 1.0 | équivalent |
| 141 | Médiane du service | SVR linéaire (niveau 1) | svm | mediane | svr_lineaire | 1.8518 | 2.981 | 2.995 | 1.8536 | 1.6 | 0.0001 | 0.4021 | 0.0141 | moins bon | 1.0 | équivalent |
| 142 | Exclure les séjours sans durée | SVR linéaire (niveau 1) | svm | exclure | svr_lineaire | 2.106 | 3.132 | 3.091 | 1.9619 | 1.6 | 0.0 | 0.0001 | 0.0 | moins bon | 0.0131 | moins bon |
| 143 | Exclure les séjours sans durée | SVR RBF (niveau 2) | svm | exclure | svr_rbf | 2.168 | 3.118 | 3.028 | 1.9992 | 1.4 | 0.0 | 0.0 | 0.0 | moins bon | 0.0 | moins bon |


Meilleure paire : **Moyenne du service × SVR quantile, noyau laplacien**.
