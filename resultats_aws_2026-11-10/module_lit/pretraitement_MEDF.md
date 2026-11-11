# Banc de comparaison du prétraitement — service MEDF

Une décision change à la fois ; « (retenu) » = choix retenu. MAE « propre » : contre la série de la variante ; MAE « retenue » : contre la série du choix retenu, mêmes jours pour toutes les variantes. Diebold-Mariano (perte absolue, correction HLN) sur la MAE « retenue ».


## Horizon J+1


### P1 · Durées inconnues

15 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | pinball τ=0.8 retenue | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Exclure les séjours sans durée | 15/05/2026 | 0 | 11.29 | 66.4 | -1.2 | 2.774 | 1.0299 | -49.0 | 2.511 | 0.9499 | 3.5 | 0.3045 | 1.0 | équivalent |
| Médiane du service | 15/07/2025 | 0 | 9.73 | 57.3 | -3.5 | 1.942 | 0.7261 | -6.8 | 1.942 | 0.7623 | 6.8 | 0.9314 | 1.0 | équivalent |
| Moyenne du service | 15/07/2025 | 0 | 10.06 | 59.2 | -0.2 | 1.86 | 0.6975 | -10.3 | 1.926 | 0.7326 | 7.1 | 0.6483 | 1.0 | équivalent |
| Médiane de la tranche d'âge | 15/07/2025 | 0 | 9.73 | 57.3 | -3.5 | 1.942 | 0.7261 | -6.8 | 1.942 | 0.7623 | 6.5 | 0.9314 | 1.0 | équivalent |
| Estimée : prix, puis issue, puis médiane (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 1.947 | 0.7594 | -7.0 | 1.947 | 0.7594 | 6.3 |  |  | — choix retenu |
| k plus proches voisins (prix, âge, sexe, issue, mois) | 15/07/2025 | 0 | 9.75 | 57.3 | -3.4 | 1.898 | 0.7564 | -4.4 | 1.898 | 0.7564 | 6.9 | 0.9104 | 1.0 | équivalent |
| Régressions enchaînées (ridge, principe de MICE) | 15/07/2025 | 0 | 9.75 | 57.3 | -3.4 | 1.979 | 0.7638 | -8.8 | 1.979 | 0.7638 | 7.3 | 0.8099 | 1.0 | équivalent |
| Loi normale multivariée par EM | 15/07/2025 | 0 | 9.74 | 57.3 | -3.4 | 1.991 | 0.7588 | -9.4 | 1.991 | 0.7588 | 7.2 | 0.9707 | 1.0 | équivalent |
| ACP itérative (rang faible) | 15/07/2025 | 0 | 9.62 | 56.6 | -4.3 | 1.935 | 0.8024 | -6.4 | 1.935 | 0.8024 | 10.3 | 0.4249 | 1.0 | équivalent |
| SoftImpute (norme nucléaire) | 15/07/2025 | 0 | 9.75 | 57.3 | -3.4 | 1.828 | 0.7128 | -8.4 | 1.894 | 0.7346 | 7.3 | 0.4526 | 1.0 | équivalent |
| XGBoost (avec le diagnostic) | 15/07/2025 | 0 | 9.7 | 57.0 | -3.8 | 1.949 | 0.7752 | -7.1 | 1.949 | 0.7752 | 26.7 | 0.4131 | 1.0 | équivalent |
| Hybride : prix, sinon XGBoost | 15/07/2025 | 0 | 9.7 | 57.0 | -3.8 | 1.936 | 0.7842 | -6.4 | 1.936 | 0.7842 | 25.7 | 0.241 | 1.0 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Estimée : prix, puis issue, puis médiane (retenu)).



### P2 · Fenêtre de censure (encore hospitalisé)

183 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | pinball τ=0.8 retenue | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 14 jours | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 1.941 | 0.6897 | -8.2 | 1.941 | 0.6897 | 6.0 |  |  | identique |
| 30 jours | 15/07/2025 | 0 | 9.79 | 57.6 | -3.6 | 1.945 | 0.7006 | -8.0 | 1.95 | 0.6864 | 6.2 | 0.5555 | 1.0 | équivalent |
| p95 des durées connues (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 1.941 | 0.6897 | -8.2 | 1.941 | 0.6897 | 6.5 |  |  | — choix retenu |
| 60 jours | 15/07/2025 | 0 | 9.94 | 58.5 | -3.5 | 1.962 | 0.7122 | -9.7 | 2.035 | 0.6941 | 6.4 | 0.7985 | 1.0 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (p95 des durées connues (retenu)).



### P3 · Convention du nombre de jours

183 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | pinball τ=0.8 retenue | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Attendue (nuit incertaine = 1 − p) (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 1.941 | 0.6897 | -8.2 | 1.941 | 0.6897 | 6.3 |  |  | — choix retenu |
| Tout inclusif (borne basse) | 15/07/2025 | 0 | 9.07 | 53.4 | -6.5 | 1.921 | 0.6928 | -9.2 | 2.002 | 0.7187 | 6.6 | 0.3215 | 0.3215 | équivalent |
| Tout en nuits (borne haute) | 15/07/2025 | 0 | 10.36 | 60.9 | 2.1 | 1.939 | 0.6472 | -5.0 | 1.958 | 0.6528 | 5.8 | 0.0949 | 0.1898 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Attendue (nuit incertaine = 1 − p) (retenu)).



### P4 · Patients « Ancien » reportés

183 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | pinball τ=0.8 retenue | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Garder toutes les lignes (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 1.941 | 0.6897 | -8.2 | 1.941 | 0.6897 | 5.9 |  |  | — choix retenu |
| Fusionner les reports confirmés | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 1.941 | 0.6897 | -8.2 | 1.941 | 0.6897 | 5.9 |  |  | identique |


Aucune variante ne fait significativement mieux que le choix retenu (Garder toutes les lignes (retenu)).



### P5 · Période exploitable

183 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | pinball τ=0.8 retenue | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Durées connues ≥ 80 % | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 1.941 | 0.6897 | -8.2 | 1.941 | 0.6897 | 5.9 |  |  | identique |
| Durées connues ≥ 90 % (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 1.941 | 0.6897 | -8.2 | 1.941 | 0.6897 | 6.6 |  |  | — choix retenu |
| Durées connues ≥ 95 % | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 1.941 | 0.6897 | -8.2 | 1.941 | 0.6897 | 6.5 |  |  | identique |
| ≥ 90 %, sans rodage au début (premier mois = début réel du registre) | 01/07/2025 | 0 | 9.43 | 55.5 | -4.1 | 1.925 | 0.6949 | -7.3 | 1.925 | 0.6949 | 8.8 | 0.4406 | 0.4406 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Durées connues ≥ 90 % (retenu)).



### P6 · Fin de série (délai d'inscription)

176 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | pinball τ=0.8 retenue | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Aucune coupe | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 1.94 | 0.6846 | -8.3 | 1.94 | 0.6846 | 6.7 |  |  | identique |
| 7 derniers jours retirés | 15/07/2025 | 7 | 9.71 | 57.1 | -3.7 | 1.94 | 0.6846 | -8.3 | 1.94 | 0.6846 | 7.0 |  |  | identique |
| p95 du délai d'inscription (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 1.94 | 0.6846 | -8.3 | 1.94 | 0.6846 | 6.8 |  |  | — choix retenu |


Aucune variante ne fait significativement mieux que le choix retenu (p95 du délai d'inscription (retenu)).



### P7 · Trous de saisie (≥ 4 jours sans admission)

183 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | pinball τ=0.8 retenue | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Gardés tels quels (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 1.941 | 0.6897 | -8.2 | 1.941 | 0.6897 | 6.8 |  |  | — choix retenu |
| Lignes d'apprentissage qui les touchent exclues | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 1.949 | 0.6892 | -8.6 | 1.949 | 0.6892 | 7.5 | 0.9067 | 0.9067 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Gardés tels quels (retenu)).



### P8 · Méthode de comptage des présents

183 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | pinball τ=0.8 retenue | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Recensement de minuit (nuits passées) (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 1.941 | 0.6897 | -8.2 | 1.941 | 0.6897 | 6.8 |  |  | — choix retenu |
| Présence dans la journée (jour de sortie compris) | 15/07/2025 | 0 | 12.27 | 72.2 | -2.8 | 2.004 | 0.7759 | 5.8 | 2.564 | 0.7736 | 7.3 | 0.1017 | 0.1017 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Recensement de minuit (nuits passées) (retenu)).



### P1 × modèles (J+1) : chaque méthode des durées inconnues avec chaque modèle

15 jours évalués ; tri par MAE contre la série retenue.

| variante | imputation | modèle | famille | cle_imputation | cle_modele | pinball τ=0.8 retenue | MAE retenue | MAE propre | pinball τ=0.8 propre | temps (s) | DM p vs paire retenue | DM p vs imputation retenue, même modèle | p Holm vs paire retenue | vs paire retenue | p Holm vs imputation retenue, même modèle | vs imputation retenue, même modèle |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Exclure les séjours sans durée | C · perceptron multicouche quantile | concurrent | exclure | mlp | 0.5118 | 1.71 | 1.967 | 0.5566 | 0.4 | 0.06 | 0.0533 | 1.0 | équivalent | 1.0 | équivalent |
| 1 | Loi normale multivariée par EM | B · gradient boosting quantile | concurrent | em | boosting | 0.5789 | 1.771 | 1.771 | 0.5789 | 9.3 | 0.0214 | 0.074 | 1.0 | équivalent | 1.0 | équivalent |
| 2 | Exclure les séjours sans durée | E · XGBoost quantile (second ordre) | concurrent | exclure | xgboost | 0.5987 | 2.23 | 2.364 | 0.6526 | 3.1 | 0.1517 | 0.5739 | 1.0 | équivalent | 1.0 | équivalent |
| 3 | k plus proches voisins (prix, âge, sexe, issue, mois) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | knn | lssvr_rbf | 0.6238 | 1.75 | 1.75 | 0.6238 | 0.1 | 0.0534 | 0.6661 | 1.0 | équivalent | 1.0 | équivalent |
| 4 | XGBoost (avec le diagnostic) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | xgboost | lssvr_rbf | 0.6238 | 1.746 | 1.746 | 0.6238 | 0.2 | 0.0521 | 0.6559 | 1.0 | équivalent | 1.0 | équivalent |
| 5 | Hybride : prix, sinon XGBoost | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | hybride | lssvr_rbf | 0.6242 | 1.741 | 1.741 | 0.6242 | 0.2 | 0.0494 | 0.6759 | 1.0 | équivalent | 1.0 | équivalent |
| 6 | Hybride : prix, sinon XGBoost | A · forêt aléatoire quantile | concurrent | hybride | foret | 0.6252 | 1.893 | 1.893 | 0.6252 | 11.1 | 0.0813 | 0.5599 | 1.0 | équivalent | 1.0 | équivalent |
| 7 | XGBoost (avec le diagnostic) | A · forêt aléatoire quantile | concurrent | xgboost | foret | 0.6259 | 1.913 | 1.913 | 0.6259 | 10.8 | 0.1143 | 0.487 | 1.0 | équivalent | 1.0 | équivalent |
| 8 | Régressions enchaînées (ridge, principe de MICE) | A · forêt aléatoire quantile | concurrent | regression | foret | 0.6272 | 1.791 | 1.791 | 0.6272 | 10.7 | 0.1183 | 0.3476 | 1.0 | équivalent | 1.0 | équivalent |
| 9 | Estimée : prix, puis issue, puis médiane | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | estimee | lssvr_rbf | 0.6291 | 1.752 | 1.752 | 0.6291 | 0.2 | 0.0731 |  | 1.0 | équivalent |  | — référence |
| 10 | Loi normale multivariée par EM | A · forêt aléatoire quantile | concurrent | em | foret | 0.6298 | 1.785 | 1.785 | 0.6298 | 10.7 | 0.1298 | 0.4481 | 1.0 | équivalent | 1.0 | équivalent |
| 11 | Loi normale multivariée par EM | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | em | lssvr_rbf | 0.6315 | 1.753 | 1.753 | 0.6315 | 0.1 | 0.0741 | 0.5543 | 1.0 | équivalent | 1.0 | équivalent |
| 12 | Régressions enchaînées (ridge, principe de MICE) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | regression | lssvr_rbf | 0.6327 | 1.757 | 1.757 | 0.6327 | 0.2 | 0.0798 | 0.3246 | 1.0 | équivalent | 1.0 | équivalent |
| 13 | ACP itérative (rang faible) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | acp_iterative | lssvr_rbf | 0.6335 | 1.705 | 1.705 | 0.6335 | 0.1 | 0.0659 | 0.7827 | 1.0 | équivalent | 1.0 | équivalent |
| 14 | k plus proches voisins (prix, âge, sexe, issue, mois) | A · forêt aléatoire quantile | concurrent | knn | foret | 0.6336 | 1.797 | 1.797 | 0.6336 | 10.8 | 0.1374 | 0.6885 | 1.0 | équivalent | 1.0 | équivalent |
| 15 | SoftImpute (norme nucléaire) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | softimpute | lssvr_rbf | 0.6337 | 1.731 | 1.664 | 0.5956 | 0.2 | 0.0705 | 0.6695 | 1.0 | équivalent | 1.0 | équivalent |
| 16 | SoftImpute (norme nucléaire) | A · forêt aléatoire quantile | concurrent | softimpute | foret | 0.6357 | 1.813 | 1.746 | 0.5824 | 10.7 | 0.1395 | 0.7701 | 1.0 | équivalent | 1.0 | équivalent |
| 17 | Médiane de la tranche d'âge | A · forêt aléatoire quantile | concurrent | mediane_age | foret | 0.639 | 1.826 | 1.826 | 0.599 | 11.0 | 0.1691 | 0.9609 | 1.0 | équivalent | 1.0 | équivalent |
| 18 | Médiane du service | A · forêt aléatoire quantile | concurrent | mediane | foret | 0.639 | 1.826 | 1.826 | 0.599 | 10.6 | 0.1691 | 0.9609 | 1.0 | équivalent | 1.0 | équivalent |
| 19 | Estimée : prix, puis issue, puis médiane | A · forêt aléatoire quantile | concurrent | estimee | foret | 0.6403 | 1.758 | 1.758 | 0.6403 | 10.8 | 0.1641 |  | 1.0 | équivalent |  | — référence |
| 20 | Exclure les séjours sans durée | A · forêt aléatoire quantile | concurrent | exclure | foret | 0.6409 | 2.24 | 2.374 | 0.7209 | 1.6 | 0.2602 | 0.9928 | 1.0 | équivalent | 1.0 | équivalent |
| 21 | k plus proches voisins (prix, âge, sexe, issue, mois) | B · gradient boosting quantile | concurrent | knn | boosting | 0.6438 | 1.661 | 1.661 | 0.6438 | 9.6 | 0.115 | 0.2485 | 1.0 | équivalent | 1.0 | équivalent |
| 22 | Moyenne du service | A · forêt aléatoire quantile | concurrent | moyenne | foret | 0.6441 | 1.906 | 1.84 | 0.5908 | 10.8 | 0.142 | 0.829 | 1.0 | équivalent | 1.0 | équivalent |
| 23 | k plus proches voisins (prix, âge, sexe, issue, mois) | D · LSTM quantile | concurrent | knn | lstm | 0.6541 | 1.883 | 1.883 | 0.6541 | 9.5 | 0.272 | 0.7086 | 1.0 | équivalent | 1.0 | équivalent |
| 24 | ACP itérative (rang faible) | A · forêt aléatoire quantile | concurrent | acp_iterative | foret | 0.6548 | 1.82 | 1.82 | 0.6548 | 10.6 | 0.2224 | 0.4964 | 1.0 | équivalent | 1.0 | équivalent |
| 25 | Médiane du service | B · gradient boosting quantile | concurrent | mediane | boosting | 0.6571 | 1.701 | 1.701 | 0.6171 | 9.3 | 0.2695 | 0.6656 | 1.0 | équivalent | 1.0 | équivalent |
| 26 | Médiane de la tranche d'âge | B · gradient boosting quantile | concurrent | mediane_age | boosting | 0.6571 | 1.701 | 1.701 | 0.6171 | 9.7 | 0.2695 | 0.6656 | 1.0 | équivalent | 1.0 | équivalent |
| 27 | Médiane de la tranche d'âge | E · XGBoost quantile (second ordre) | concurrent | mediane_age | xgboost | 0.6586 | 1.892 | 1.892 | 0.6218 | 10.2 | 0.0912 | 0.7725 | 1.0 | équivalent | 1.0 | équivalent |
| 28 | Médiane du service | E · XGBoost quantile (second ordre) | concurrent | mediane | xgboost | 0.6586 | 1.892 | 1.892 | 0.6218 | 10.1 | 0.0912 | 0.7725 | 1.0 | équivalent | 1.0 | équivalent |
| 29 | Régressions enchaînées (ridge, principe de MICE) | B · gradient boosting quantile | concurrent | regression | boosting | 0.661 | 1.766 | 1.766 | 0.661 | 9.5 | 0.188 | 0.6052 | 1.0 | équivalent | 1.0 | équivalent |
| 30 | SoftImpute (norme nucléaire) | B · gradient boosting quantile | concurrent | softimpute | boosting | 0.6611 | 1.771 | 1.705 | 0.6078 | 9.2 | 0.32 | 0.6521 | 1.0 | équivalent | 1.0 | équivalent |
| 31 | Estimée : prix, puis issue, puis médiane | D · LSTM quantile | concurrent | estimee | lstm | 0.6612 | 1.865 | 1.865 | 0.6612 | 8.7 | 0.322 |  | 1.0 | équivalent |  | — référence |
| 32 | Hybride : prix, sinon XGBoost | SVR quantile, noyau polynomial (degré 2) | svm | hybride | svr_q_polynomial | 0.6628 | 1.786 | 1.786 | 0.6628 | 5.7 | 0.0669 | 0.3317 | 1.0 | équivalent | 1.0 | équivalent |
| 33 | Médiane du service | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | mediane | lssvr_rbf | 0.6653 | 1.781 | 1.781 | 0.6253 | 0.1 | 0.2608 | 0.183 | 1.0 | équivalent | 1.0 | équivalent |
| 34 | Médiane de la tranche d'âge | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | mediane_age | lssvr_rbf | 0.6653 | 1.781 | 1.781 | 0.6253 | 0.2 | 0.2608 | 0.183 | 1.0 | équivalent | 1.0 | équivalent |
| 35 | ACP itérative (rang faible) | E · XGBoost quantile (second ordre) | concurrent | acp_iterative | xgboost | 0.6694 | 1.895 | 1.895 | 0.6694 | 10.0 | 0.1833 | 0.9676 | 1.0 | équivalent | 1.0 | équivalent |
| 36 | Moyenne du service | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | moyenne | lssvr_rbf | 0.6715 | 1.788 | 1.721 | 0.6256 | 0.2 | 0.1849 | 0.0972 | 1.0 | équivalent | 1.0 | équivalent |
| 37 | Estimée : prix, puis issue, puis médiane | E · XGBoost quantile (second ordre) | concurrent | estimee | xgboost | 0.6716 | 1.743 | 1.743 | 0.6716 | 10.2 | 0.1613 |  | 1.0 | équivalent |  | — référence |
| 38 | XGBoost (avec le diagnostic) | SVR quantile, noyau polynomial (degré 2) | svm | xgboost | svr_q_polynomial | 0.6724 | 1.763 | 1.763 | 0.6724 | 5.7 | 0.1004 | 0.4358 | 1.0 | équivalent | 1.0 | équivalent |
| 39 | Loi normale multivariée par EM | D · LSTM quantile | concurrent | em | lstm | 0.6752 | 1.901 | 1.901 | 0.6752 | 8.7 | 0.4444 | 0.7127 | 1.0 | équivalent | 1.0 | équivalent |
| 40 | Loi normale multivariée par EM | E · XGBoost quantile (second ordre) | concurrent | em | xgboost | 0.6755 | 1.668 | 1.668 | 0.6755 | 10.0 | 0.3158 | 0.9276 | 1.0 | équivalent | 1.0 | équivalent |
| 41 | SoftImpute (norme nucléaire) | SVR quantile, noyau polynomial (degré 2) | svm | softimpute | svr_q_polynomial | 0.6771 | 1.711 | 1.644 | 0.6238 | 6.0 | 0.1753 | 0.5726 | 1.0 | équivalent | 1.0 | équivalent |
| 42 | Estimée : prix, puis issue, puis médiane | B · gradient boosting quantile | concurrent | estimee | boosting | 0.6801 | 1.66 | 1.66 | 0.6801 | 9.4 | 0.2589 |  | 1.0 | équivalent |  | — référence |
| 43 | Moyenne du service | B · gradient boosting quantile | concurrent | moyenne | boosting | 0.6805 | 1.675 | 1.608 | 0.6272 | 9.8 | 0.4421 | 0.9953 | 1.0 | équivalent | 1.0 | équivalent |
| 44 | Exclure les séjours sans durée | SVR quantile, noyau laplacien | svm | exclure | svr_q_laplacien | 0.6825 | 2.346 | 2.529 | 0.7625 | 1.9 | 0.6434 | 0.6638 | 1.0 | équivalent | 1.0 | équivalent |
| 45 | Régressions enchaînées (ridge, principe de MICE) | D · LSTM quantile | concurrent | regression | lstm | 0.6843 | 1.952 | 1.952 | 0.6843 | 8.8 | 0.3998 | 0.4764 | 1.0 | équivalent | 1.0 | équivalent |
| 46 | Exclure les séjours sans durée | D · LSTM quantile | concurrent | exclure | lstm | 0.6856 | 2.211 | 2.477 | 0.6989 | 1.6 | 0.4631 | 0.8823 | 1.0 | équivalent | 1.0 | équivalent |
| 47 | Moyenne du service | C · perceptron multicouche quantile | concurrent | moyenne | mlp | 0.6873 | 2.059 | 1.993 | 0.6551 | 1.1 | 0.2629 | 0.6108 | 1.0 | équivalent | 1.0 | équivalent |
| 48 | Moyenne du service | SVR quantile, noyau laplacien | svm | moyenne | svr_q_laplacien | 0.6884 | 2.09 | 2.023 | 0.6724 | 4.1 | 0.3694 | 0.3959 | 1.0 | équivalent | 1.0 | équivalent |
| 49 | Loi normale multivariée par EM | SVR quantile, noyau polynomial (degré 2) | svm | em | svr_q_polynomial | 0.6899 | 1.772 | 1.772 | 0.6899 | 6.0 | 0.2026 | 0.9807 | 1.0 | équivalent | 1.0 | équivalent |
| 50 | Estimée : prix, puis issue, puis médiane | SVR quantile, noyau polynomial (degré 2) | svm | estimee | svr_q_polynomial | 0.6902 | 1.767 | 1.767 | 0.6902 | 6.0 | 0.1847 |  | 1.0 | équivalent |  | — référence |
| 51 | Moyenne du service | SVR quantile RBF (niveau 3) | svm | moyenne | svr_q_rbf | 0.6933 | 1.929 | 1.862 | 0.646 | 4.1 | 0.2995 | 0.3409 | 1.0 | équivalent | 1.0 | équivalent |
| 52 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile, noyau polynomial (degré 2) | svm | regression | svr_q_polynomial | 0.6955 | 1.768 | 1.768 | 0.6955 | 6.0 | 0.2745 | 0.706 | 1.0 | équivalent | 1.0 | équivalent |
| 53 | SoftImpute (norme nucléaire) | SVR quantile RBF (niveau 3) | svm | softimpute | svr_q_rbf | 0.6961 | 1.895 | 1.829 | 0.6521 | 5.2 | 0.2102 | 0.2062 | 1.0 | équivalent | 1.0 | équivalent |
| 54 | XGBoost (avec le diagnostic) | B · gradient boosting quantile | concurrent | xgboost | boosting | 0.7019 | 1.783 | 1.783 | 0.7019 | 9.4 | 0.5001 | 0.5507 | 1.0 | équivalent | 1.0 | équivalent |
| 55 | Hybride : prix, sinon XGBoost | D · LSTM quantile | concurrent | hybride | lstm | 0.7027 | 2.022 | 2.022 | 0.7027 | 9.2 | 0.5749 | 0.6587 | 1.0 | équivalent | 1.0 | équivalent |
| 56 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile, noyau polynomial (degré 2) | svm | knn | svr_q_polynomial | 0.7039 | 1.704 | 1.704 | 0.7039 | 5.8 | 0.3172 | 0.4116 | 1.0 | équivalent | 1.0 | équivalent |
| 57 | Hybride : prix, sinon XGBoost | C · perceptron multicouche quantile | concurrent | hybride | mlp | 0.7056 | 1.82 | 1.82 | 0.7056 | 1.2 | 0.5012 | 0.5349 | 1.0 | équivalent | 1.0 | équivalent |
| 58 | XGBoost (avec le diagnostic) | SVR quantile RBF (niveau 3) | svm | xgboost | svr_q_rbf | 0.7058 | 1.916 | 1.916 | 0.7058 | 3.9 | 0.2878 | 0.2992 | 1.0 | équivalent | 1.0 | équivalent |
| 59 | Moyenne du service | SVR quantile, noyau polynomial (degré 2) | svm | moyenne | svr_q_polynomial | 0.706 | 1.841 | 1.774 | 0.6527 | 5.9 | 0.4254 | 0.7965 | 1.0 | équivalent | 1.0 | équivalent |
| 60 | Médiane de la tranche d'âge | SVR quantile, noyau polynomial (degré 2) | svm | mediane_age | svr_q_polynomial | 0.7073 | 1.76 | 1.76 | 0.6673 | 5.9 | 0.5216 | 0.6724 | 1.0 | équivalent | 1.0 | équivalent |
| 61 | Médiane du service | SVR quantile, noyau polynomial (degré 2) | svm | mediane | svr_q_polynomial | 0.7073 | 1.76 | 1.76 | 0.6673 | 5.9 | 0.5216 | 0.6724 | 1.0 | équivalent | 1.0 | équivalent |
| 62 | ACP itérative (rang faible) | B · gradient boosting quantile | concurrent | acp_iterative | boosting | 0.7101 | 1.832 | 1.832 | 0.7101 | 9.3 | 0.5589 | 0.5839 | 1.0 | équivalent | 1.0 | équivalent |
| 63 | ACP itérative (rang faible) | SVR quantile, noyau polynomial (degré 2) | svm | acp_iterative | svr_q_polynomial | 0.7102 | 1.867 | 1.867 | 0.7102 | 5.3 | 0.3409 | 0.5391 | 1.0 | équivalent | 1.0 | équivalent |
| 64 | Régressions enchaînées (ridge, principe de MICE) | C · perceptron multicouche quantile | concurrent | regression | mlp | 0.7103 | 1.822 | 1.822 | 0.7103 | 1.2 | 0.548 | 0.6465 | 1.0 | équivalent | 1.0 | équivalent |
| 65 | Moyenne du service | E · XGBoost quantile (second ordre) | concurrent | moyenne | xgboost | 0.7127 | 1.699 | 1.633 | 0.6594 | 9.9 | 0.6019 | 0.4416 | 1.0 | équivalent | 1.0 | équivalent |
| 66 | SoftImpute (norme nucléaire) | E · XGBoost quantile (second ordre) | concurrent | softimpute | xgboost | 0.7132 | 1.603 | 1.536 | 0.6599 | 10.1 | 0.5818 | 0.4326 | 1.0 | équivalent | 1.0 | équivalent |
| 67 | XGBoost (avec le diagnostic) | C · perceptron multicouche quantile | concurrent | xgboost | mlp | 0.7141 | 1.814 | 1.814 | 0.7141 | 1.1 | 0.5921 | 0.8262 | 1.0 | équivalent | 1.0 | équivalent |
| 68 | Régressions enchaînées (ridge, principe de MICE) | E · XGBoost quantile (second ordre) | concurrent | regression | xgboost | 0.7181 | 1.647 | 1.647 | 0.7181 | 9.9 | 0.6014 | 0.3163 | 1.0 | équivalent | 1.0 | équivalent |
| 69 | Estimée : prix, puis issue, puis médiane | C · perceptron multicouche quantile | concurrent | estimee | mlp | 0.7192 | 1.84 | 1.84 | 0.7192 | 1.1 | 0.6368 |  | 1.0 | équivalent |  | — référence |
| 70 | Médiane du service | C · perceptron multicouche quantile | concurrent | mediane | mlp | 0.7197 | 1.916 | 1.916 | 0.6797 | 1.1 | 0.667 | 0.9886 | 1.0 | équivalent | 1.0 | équivalent |
| 71 | Médiane de la tranche d'âge | C · perceptron multicouche quantile | concurrent | mediane_age | mlp | 0.7197 | 1.916 | 1.916 | 0.6797 | 1.1 | 0.667 | 0.9886 | 1.0 | équivalent | 1.0 | équivalent |
| 72 | Hybride : prix, sinon XGBoost | SVR quantile RBF (niveau 3) | svm | hybride | svr_q_rbf | 0.7208 | 1.903 | 1.903 | 0.7208 | 3.9 | 0.3432 | 0.2174 | 1.0 | équivalent | 1.0 | équivalent |
| 73 | Médiane de la tranche d'âge | SVR quantile RBF (niveau 3) | svm | mediane_age | svr_q_rbf | 0.7211 | 1.942 | 1.942 | 0.6811 | 4.9 | 0.5175 | 0.5778 | 1.0 | équivalent | 1.0 | équivalent |
| 74 | Médiane du service | SVR quantile RBF (niveau 3) | svm | mediane | svr_q_rbf | 0.7211 | 1.942 | 1.942 | 0.6811 | 4.8 | 0.5175 | 0.5778 | 1.0 | équivalent | 1.0 | équivalent |
| 75 | Médiane du service | SVR quantile, noyau laplacien | svm | mediane | svr_q_laplacien | 0.7237 | 2.062 | 2.062 | 0.7197 | 3.8 | 0.4939 | 0.3858 | 1.0 | équivalent | 1.0 | équivalent |
| 76 | Médiane de la tranche d'âge | SVR quantile, noyau laplacien | svm | mediane_age | svr_q_laplacien | 0.7237 | 2.062 | 2.062 | 0.7197 | 3.9 | 0.4939 | 0.3858 | 1.0 | équivalent | 1.0 | équivalent |
| 77 | XGBoost (avec le diagnostic) | D · LSTM quantile | concurrent | xgboost | lstm | 0.7245 | 2.064 | 2.064 | 0.7245 | 9.0 | 0.7216 | 0.3038 | 1.0 | équivalent | 1.0 | équivalent |
| 78 | k plus proches voisins (prix, âge, sexe, issue, mois) | E · XGBoost quantile (second ordre) | concurrent | knn | xgboost | 0.7252 | 1.713 | 1.713 | 0.7252 | 10.4 | 0.6634 | 0.2902 | 1.0 | équivalent | 1.0 | équivalent |
| 79 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile RBF (niveau 3) | svm | knn | svr_q_rbf | 0.7279 | 1.907 | 1.907 | 0.7279 | 5.5 | 0.4952 | 0.6243 | 1.0 | équivalent | 1.0 | équivalent |
| 80 | SoftImpute (norme nucléaire) | SVR quantile, noyau laplacien | svm | softimpute | svr_q_laplacien | 0.7302 | 2.06 | 1.993 | 0.7221 | 4.0 | 0.5571 | 0.4816 | 1.0 | équivalent | 1.0 | équivalent |
| 81 | SoftImpute (norme nucléaire) | D · LSTM quantile | concurrent | softimpute | lstm | 0.7313 | 1.886 | 1.819 | 0.7311 | 8.3 | 0.7768 | 0.4367 | 1.0 | équivalent | 1.0 | équivalent |
| 82 | SoftImpute (norme nucléaire) | C · perceptron multicouche quantile | concurrent | softimpute | mlp | 0.7324 | 1.798 | 1.732 | 0.6833 | 1.1 | 0.7458 | 0.6736 | 1.0 | équivalent | 1.0 | équivalent |
| 83 | ACP itérative (rang faible) | D · LSTM quantile | concurrent | acp_iterative | lstm | 0.7326 | 1.975 | 1.975 | 0.7326 | 8.7 | 0.7932 | 0.3579 | 1.0 | équivalent | 1.0 | équivalent |
| 84 | Moyenne du service | SVR quantile composite (niveau 4, retenu) | svm | moyenne | svr_q_composite | 0.7326 | 1.926 | 1.86 | 0.6975 | 7.2 | 0.6483 | 0.6483 | 1.0 | équivalent | 1.0 | équivalent |
| 85 | SoftImpute (norme nucléaire) | SVR quantile composite (niveau 4, retenu) | svm | softimpute | svr_q_composite | 0.7346 | 1.894 | 1.828 | 0.7128 | 5.7 | 0.4526 | 0.4526 | 1.0 | équivalent | 1.0 | équivalent |
| 86 | Exclure les séjours sans durée | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | exclure | lssvr_rbf | 0.7346 | 2.205 | 2.355 | 0.7713 | 0.0 | 0.8605 | 0.3963 | 1.0 | équivalent | 1.0 | équivalent |
| 87 | Moyenne du service | D · LSTM quantile | concurrent | moyenne | lstm | 0.7352 | 1.758 | 1.691 | 0.6819 | 8.8 | 0.727 | 0.3507 | 1.0 | équivalent | 1.0 | équivalent |
| 88 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile, noyau laplacien | svm | regression | svr_q_laplacien | 0.7361 | 2.117 | 2.117 | 0.7361 | 4.8 | 0.6237 | 0.6895 | 1.0 | équivalent | 1.0 | équivalent |
| 89 | Médiane du service | D · LSTM quantile | concurrent | mediane | lstm | 0.7363 | 1.811 | 1.811 | 0.6963 | 8.0 | 0.8127 | 0.2799 | 1.0 | équivalent | 1.0 | équivalent |
| 90 | Médiane de la tranche d'âge | D · LSTM quantile | concurrent | mediane_age | lstm | 0.7363 | 1.811 | 1.811 | 0.6963 | 8.0 | 0.8127 | 0.2799 | 1.0 | équivalent | 1.0 | équivalent |
| 91 | Loi normale multivariée par EM | SVR quantile RBF (niveau 3) | svm | em | svr_q_rbf | 0.737 | 1.933 | 1.933 | 0.737 | 4.7 | 0.548 | 0.7698 | 1.0 | équivalent | 1.0 | équivalent |
| 92 | Loi normale multivariée par EM | SVR quantile, noyau laplacien | svm | em | svr_q_laplacien | 0.7376 | 2.127 | 2.127 | 0.7376 | 3.9 | 0.6439 | 0.7515 | 1.0 | équivalent | 1.0 | équivalent |
| 93 | Estimée : prix, puis issue, puis médiane | SVR quantile RBF (niveau 3) | svm | estimee | svr_q_rbf | 0.739 | 1.918 | 1.918 | 0.739 | 3.9 | 0.5928 |  | 1.0 | équivalent |  | — référence |
| 94 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile RBF (niveau 3) | svm | regression | svr_q_rbf | 0.7391 | 1.933 | 1.933 | 0.7391 | 4.1 | 0.5957 | 0.9925 | 1.0 | équivalent | 1.0 | équivalent |
| 95 | k plus proches voisins (prix, âge, sexe, issue, mois) | C · perceptron multicouche quantile | concurrent | knn | mlp | 0.7395 | 1.981 | 1.981 | 0.7395 | 1.1 | 0.853 | 0.7049 | 1.0 | équivalent | 1.0 | équivalent |
| 96 | Estimée : prix, puis issue, puis médiane | SVR quantile, noyau laplacien | svm | estimee | svr_q_laplacien | 0.7416 | 2.122 | 2.122 | 0.7416 | 4.3 | 0.6799 |  | 1.0 | équivalent |  | — référence |
| 97 | Hybride : prix, sinon XGBoost | B · gradient boosting quantile | concurrent | hybride | boosting | 0.7441 | 1.76 | 1.76 | 0.7441 | 9.5 | 0.8405 | 0.2044 | 1.0 | équivalent | 1.0 | équivalent |
| 98 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile, noyau laplacien | svm | knn | svr_q_laplacien | 0.7455 | 2.089 | 2.089 | 0.7455 | 4.5 | 0.763 | 0.7561 | 1.0 | équivalent | 1.0 | équivalent |
| 99 | Loi normale multivariée par EM | C · perceptron multicouche quantile | concurrent | em | mlp | 0.746 | 1.87 | 1.87 | 0.746 | 1.2 | 0.8788 | 0.4596 | 1.0 | équivalent | 1.0 | équivalent |
| 100 | XGBoost (avec le diagnostic) | SVR quantile, noyau laplacien | svm | xgboost | svr_q_laplacien | 0.7473 | 2.068 | 2.068 | 0.7473 | 4.5 | 0.8056 | 0.6976 | 1.0 | équivalent | 1.0 | équivalent |
| 101 | ACP itérative (rang faible) | SVR quantile RBF (niveau 3) | svm | acp_iterative | svr_q_rbf | 0.7548 | 1.916 | 1.916 | 0.7548 | 4.9 | 0.9133 | 0.3727 | 1.0 | équivalent | 1.0 | équivalent |
| 102 | Hybride : prix, sinon XGBoost | SVR quantile, noyau laplacien | svm | hybride | svr_q_laplacien | 0.755 | 2.071 | 2.071 | 0.755 | 4.8 | 0.9218 | 0.1432 | 1.0 | équivalent | 1.0 | équivalent |
| 103 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile composite (niveau 4, retenu) | svm | knn | svr_q_composite | 0.7564 | 1.898 | 1.898 | 0.7564 | 6.2 | 0.9104 | 0.9104 | 1.0 | équivalent | 1.0 | équivalent |
| 104 | Loi normale multivariée par EM | SVR quantile composite (niveau 4, retenu) | svm | em | svr_q_composite | 0.7588 | 1.991 | 1.991 | 0.7588 | 6.3 | 0.9707 | 0.9707 | 1.0 | équivalent | 1.0 | équivalent |
| 105 | Estimée : prix, puis issue, puis médiane | SVR quantile composite (niveau 4, retenu) | svm | estimee | svr_q_composite | 0.7594 | 1.947 | 1.947 | 0.7594 | 6.5 |  |  |  | — référence |  | — référence |
| 106 | Médiane du service | SVR quantile composite (niveau 4, retenu) | svm | mediane | svr_q_composite | 0.7623 | 1.942 | 1.942 | 0.7261 | 6.9 | 0.9314 | 0.9314 | 1.0 | équivalent | 1.0 | équivalent |
| 107 | Médiane de la tranche d'âge | SVR quantile composite (niveau 4, retenu) | svm | mediane_age | svr_q_composite | 0.7623 | 1.942 | 1.942 | 0.7261 | 7.0 | 0.9314 | 0.9314 | 1.0 | équivalent | 1.0 | équivalent |
| 108 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile composite (niveau 4, retenu) | svm | regression | svr_q_composite | 0.7638 | 1.979 | 1.979 | 0.7638 | 6.5 | 0.8099 | 0.8099 | 1.0 | équivalent | 1.0 | équivalent |
| 109 | ACP itérative (rang faible) | SVR quantile, noyau laplacien | svm | acp_iterative | svr_q_laplacien | 0.7663 | 2.092 | 2.092 | 0.7663 | 4.1 | 0.8868 | 0.2008 | 1.0 | équivalent | 1.0 | équivalent |
| 110 | XGBoost (avec le diagnostic) | SVR quantile composite (niveau 4, retenu) | svm | xgboost | svr_q_composite | 0.7752 | 1.949 | 1.949 | 0.7752 | 7.4 | 0.4131 | 0.4131 | 1.0 | équivalent | 1.0 | équivalent |
| 111 | Hybride : prix, sinon XGBoost | E · XGBoost quantile (second ordre) | concurrent | hybride | xgboost | 0.7822 | 1.809 | 1.809 | 0.7822 | 9.8 | 0.8064 | 0.1316 | 1.0 | équivalent | 1.0 | équivalent |
| 112 | Hybride : prix, sinon XGBoost | SVR quantile composite (niveau 4, retenu) | svm | hybride | svr_q_composite | 0.7842 | 1.936 | 1.936 | 0.7842 | 6.8 | 0.241 | 0.241 | 1.0 | équivalent | 1.0 | équivalent |
| 113 | XGBoost (avec le diagnostic) | E · XGBoost quantile (second ordre) | concurrent | xgboost | xgboost | 0.7947 | 1.906 | 1.906 | 0.7947 | 10.0 | 0.7017 | 0.109 | 1.0 | équivalent | 1.0 | équivalent |
| 114 | Exclure les séjours sans durée | SVR quantile RBF (niveau 3) | svm | exclure | svr_q_rbf | 0.7948 | 2.146 | 2.298 | 0.8547 | 2.2 | 0.8098 | 0.6972 | 1.0 | équivalent | 1.0 | équivalent |
| 115 | ACP itérative (rang faible) | SVR quantile composite (niveau 4, retenu) | svm | acp_iterative | svr_q_composite | 0.8024 | 1.935 | 1.935 | 0.8024 | 8.0 | 0.4249 | 0.4249 | 1.0 | équivalent | 1.0 | équivalent |
| 116 | ACP itérative (rang faible) | C · perceptron multicouche quantile | concurrent | acp_iterative | mlp | 0.8188 | 1.965 | 1.965 | 0.8188 | 1.2 | 0.6352 | 0.1151 | 1.0 | équivalent | 1.0 | équivalent |
| 117 | Exclure les séjours sans durée | B · gradient boosting quantile | concurrent | exclure | boosting | 0.8306 | 2.166 | 2.371 | 0.8439 | 3.5 | 0.5095 | 0.1149 | 1.0 | équivalent | 1.0 | équivalent |
| 118 | Moyenne du service | SVR RBF (niveau 2) | svm | moyenne | svr_rbf | 0.8707 | 1.887 | 1.82 | 0.8174 | 1.5 | 0.5842 | 0.499 | 1.0 | équivalent | 1.0 | équivalent |
| 119 | Moyenne du service | SVR linéaire (niveau 1) | svm | moyenne | svr_lineaire | 0.8721 | 1.857 | 1.791 | 0.8188 | 1.0 | 0.5326 | 0.5115 | 1.0 | équivalent | 1.0 | équivalent |
| 120 | XGBoost (avec le diagnostic) | SVR RBF (niveau 2) | svm | xgboost | svr_rbf | 0.8849 | 1.714 | 1.714 | 0.8849 | 1.5 | 0.5665 | 0.0077 | 1.0 | équivalent | 1.0 | équivalent |
| 121 | Hybride : prix, sinon XGBoost | SVR RBF (niveau 2) | svm | hybride | svr_rbf | 0.8859 | 1.715 | 1.715 | 0.8859 | 0.9 | 0.567 | 0.0168 | 1.0 | équivalent | 1.0 | équivalent |
| 122 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR RBF (niveau 2) | svm | knn | svr_rbf | 0.8922 | 1.734 | 1.734 | 0.8922 | 1.0 | 0.548 | 0.1024 | 1.0 | équivalent | 1.0 | équivalent |
| 123 | XGBoost (avec le diagnostic) | SVR linéaire (niveau 1) | svm | xgboost | svr_lineaire | 0.8938 | 1.819 | 1.819 | 0.8938 | 0.8 | 0.4884 | 0.6366 | 1.0 | équivalent | 1.0 | équivalent |
| 124 | SoftImpute (norme nucléaire) | SVR RBF (niveau 2) | svm | softimpute | svr_rbf | 0.8962 | 1.731 | 1.665 | 0.8429 | 0.8 | 0.5394 | 0.358 | 1.0 | équivalent | 1.0 | équivalent |
| 125 | Hybride : prix, sinon XGBoost | SVR linéaire (niveau 1) | svm | hybride | svr_lineaire | 0.8971 | 1.804 | 1.804 | 0.8971 | 0.7 | 0.4832 | 0.7217 | 1.0 | équivalent | 1.0 | équivalent |
| 126 | Loi normale multivariée par EM | SVR linéaire (niveau 1) | svm | em | svr_lineaire | 0.9034 | 1.819 | 1.819 | 0.9034 | 0.8 | 0.4508 | 0.7001 | 1.0 | équivalent | 1.0 | équivalent |
| 127 | Régressions enchaînées (ridge, principe de MICE) | SVR linéaire (niveau 1) | svm | regression | svr_lineaire | 0.9044 | 1.818 | 1.818 | 0.9044 | 0.8 | 0.4511 | 0.8087 | 1.0 | équivalent | 1.0 | équivalent |
| 128 | SoftImpute (norme nucléaire) | SVR linéaire (niveau 1) | svm | softimpute | svr_lineaire | 0.9062 | 1.777 | 1.711 | 0.8529 | 0.8 | 0.4615 | 0.9395 | 1.0 | équivalent | 1.0 | équivalent |
| 129 | Loi normale multivariée par EM | SVR RBF (niveau 2) | svm | em | svr_rbf | 0.9069 | 1.772 | 1.772 | 0.9069 | 1.1 | 0.5101 | 0.5535 | 1.0 | équivalent | 1.0 | équivalent |
| 130 | Estimée : prix, puis issue, puis médiane | SVR linéaire (niveau 1) | svm | estimee | svr_lineaire | 0.9076 | 1.819 | 1.819 | 0.9076 | 0.8 | 0.4474 |  | 1.0 | équivalent |  | — référence |
| 131 | Régressions enchaînées (ridge, principe de MICE) | SVR RBF (niveau 2) | svm | regression | svr_rbf | 0.908 | 1.771 | 1.771 | 0.908 | 1.4 | 0.5088 | 0.6616 | 1.0 | équivalent | 1.0 | équivalent |
| 132 | Estimée : prix, puis issue, puis médiane | SVR RBF (niveau 2) | svm | estimee | svr_rbf | 0.9122 | 1.767 | 1.767 | 0.9122 | 1.4 | 0.4948 |  | 1.0 | équivalent |  | — référence |
| 133 | Médiane du service | SVR RBF (niveau 2) | svm | mediane | svr_rbf | 0.9166 | 1.76 | 1.76 | 0.8766 | 1.1 | 0.5074 | 0.8999 | 1.0 | équivalent | 1.0 | équivalent |
| 134 | Médiane de la tranche d'âge | SVR RBF (niveau 2) | svm | mediane_age | svr_rbf | 0.9166 | 1.76 | 1.76 | 0.8766 | 1.1 | 0.5074 | 0.8999 | 1.0 | équivalent | 1.0 | équivalent |
| 135 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR linéaire (niveau 1) | svm | knn | svr_lineaire | 0.9197 | 1.863 | 1.863 | 0.9197 | 0.5 | 0.4042 | 0.5944 | 1.0 | équivalent | 1.0 | équivalent |
| 136 | Médiane du service | SVR linéaire (niveau 1) | svm | mediane | svr_lineaire | 0.9376 | 1.832 | 1.832 | 0.8976 | 0.9 | 0.3986 | 0.4259 | 1.0 | équivalent | 1.0 | équivalent |
| 137 | Médiane de la tranche d'âge | SVR linéaire (niveau 1) | svm | mediane_age | svr_lineaire | 0.9376 | 1.832 | 1.832 | 0.8976 | 1.0 | 0.3986 | 0.4259 | 1.0 | équivalent | 1.0 | équivalent |
| 138 | ACP itérative (rang faible) | SVR linéaire (niveau 1) | svm | acp_iterative | svr_lineaire | 0.9412 | 1.844 | 1.844 | 0.9412 | 0.7 | 0.3982 | 0.4264 | 1.0 | équivalent | 1.0 | équivalent |
| 139 | Exclure les séjours sans durée | SVR quantile composite (niveau 4, retenu) | svm | exclure | svr_q_composite | 0.9499 | 2.511 | 2.774 | 1.0299 | 3.6 | 0.3045 | 0.3045 | 1.0 | équivalent | 1.0 | équivalent |
| 140 | ACP itérative (rang faible) | SVR RBF (niveau 2) | svm | acp_iterative | svr_rbf | 0.9519 | 1.788 | 1.788 | 0.9519 | 1.2 | 0.4217 | 0.1944 | 1.0 | équivalent | 1.0 | équivalent |
| 141 | Exclure les séjours sans durée | SVR linéaire (niveau 1) | svm | exclure | svr_lineaire | 1.105 | 1.824 | 1.922 | 1.0339 | 0.6 | 0.2022 | 0.1273 | 1.0 | équivalent | 1.0 | équivalent |
| 142 | Exclure les séjours sans durée | SVR quantile, noyau polynomial (degré 2) | svm | exclure | svr_q_polynomial | 1.1268 | 2.479 | 2.69 | 1.1402 | 2.3 | 0.1098 | 0.0892 | 1.0 | équivalent | 1.0 | équivalent |
| 143 | Exclure les séjours sans durée | SVR RBF (niveau 2) | svm | exclure | svr_rbf | 1.2028 | 2.22 | 2.354 | 1.1495 | 0.4 | 0.0804 | 0.0254 | 1.0 | équivalent | 1.0 | équivalent |


Meilleure paire : **Exclure les séjours sans durée × C · perceptron multicouche quantile**.


## Horizon J+7


### P1 · Durées inconnues

9 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | pinball τ=0.8 retenue | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Exclure les séjours sans durée | 15/05/2026 | 0 | 11.29 | 66.4 | -1.2 | 2.124 | 0.8529 | 54.9 | 1.902 | 0.764 | 3.4 |  |  | non testé (trop peu de jours) |
| Médiane du service | 15/07/2025 | 0 | 9.73 | 57.3 | -3.5 | 1.929 | 0.7061 | 55.9 | 1.819 | 0.6617 | 5.0 |  |  | non testé (trop peu de jours) |
| Moyenne du service | 15/07/2025 | 0 | 10.06 | 59.2 | -0.2 | 1.919 | 0.7105 | 53.8 | 1.868 | 0.6883 | 5.1 |  |  | non testé (trop peu de jours) |
| Médiane de la tranche d'âge | 15/07/2025 | 0 | 9.73 | 57.3 | -3.5 | 1.929 | 0.7061 | 55.9 | 1.819 | 0.6617 | 5.0 |  |  | non testé (trop peu de jours) |
| Estimée : prix, puis issue, puis médiane (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 1.811 | 0.6511 | 55.2 | 1.811 | 0.6511 | 4.7 |  |  | — choix retenu |
| k plus proches voisins (prix, âge, sexe, issue, mois) | 15/07/2025 | 0 | 9.75 | 57.3 | -3.4 | 1.808 | 0.6626 | 55.2 | 1.808 | 0.6626 | 4.9 |  |  | non testé (trop peu de jours) |
| Régressions enchaînées (ridge, principe de MICE) | 15/07/2025 | 0 | 9.75 | 57.3 | -3.4 | 1.806 | 0.6484 | 55.3 | 1.806 | 0.6484 | 6.4 |  |  | non testé (trop peu de jours) |
| Loi normale multivariée par EM | 15/07/2025 | 0 | 9.74 | 57.3 | -3.4 | 1.809 | 0.6465 | 55.2 | 1.809 | 0.6465 | 5.8 |  |  | non testé (trop peu de jours) |
| ACP itérative (rang faible) | 15/07/2025 | 0 | 9.62 | 56.6 | -4.3 | 1.804 | 0.5606 | 55.3 | 1.804 | 0.5606 | 8.2 |  |  | non testé (trop peu de jours) |
| SoftImpute (norme nucléaire) | 15/07/2025 | 0 | 9.75 | 57.3 | -3.4 | 1.807 | 0.6833 | 56.5 | 1.813 | 0.6611 | 6.1 |  |  | non testé (trop peu de jours) |
| XGBoost (avec le diagnostic) | 15/07/2025 | 0 | 9.7 | 57.0 | -3.8 | 1.805 | 0.5927 | 55.3 | 1.805 | 0.5927 | 23.7 |  |  | non testé (trop peu de jours) |
| Hybride : prix, sinon XGBoost | 15/07/2025 | 0 | 9.7 | 57.0 | -3.8 | 1.805 | 0.5931 | 55.3 | 1.805 | 0.5931 | 24.4 |  |  | non testé (trop peu de jours) |


Aucune variante ne fait significativement mieux que le choix retenu (Estimée : prix, puis issue, puis médiane (retenu)).



### P2 · Fenêtre de censure (encore hospitalisé)

177 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | pinball τ=0.8 retenue | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 14 jours | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.719 | 0.9447 | 7.3 | 2.719 | 0.9447 | 4.7 |  |  | identique |
| 30 jours | 15/07/2025 | 0 | 9.79 | 57.6 | -3.6 | 2.702 | 0.9297 | 7.3 | 2.719 | 0.9458 | 4.8 | 0.3009 | 0.5784 | équivalent |
| p95 des durées connues (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.719 | 0.9447 | 7.3 | 2.719 | 0.9447 | 4.7 |  |  | — choix retenu |
| 60 jours | 15/07/2025 | 0 | 9.94 | 58.5 | -3.5 | 2.718 | 0.9469 | 7.7 | 2.721 | 0.9472 | 4.9 | 0.2892 | 0.5784 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (p95 des durées connues (retenu)).



### P3 · Convention du nombre de jours

177 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | pinball τ=0.8 retenue | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Attendue (nuit incertaine = 1 − p) (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.719 | 0.9447 | 7.3 | 2.719 | 0.9447 | 4.9 |  |  | — choix retenu |
| Tout inclusif (borne basse) | 15/07/2025 | 0 | 9.07 | 53.4 | -6.5 | 2.86 | 1.0588 | 8.0 | 2.952 | 1.0902 | 5.7 | 0.0429 | 0.0858 | équivalent |
| Tout en nuits (borne haute) | 15/07/2025 | 0 | 10.36 | 60.9 | 2.1 | 2.7 | 0.8887 | 9.7 | 2.716 | 0.8716 | 5.3 | 0.2393 | 0.2393 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Attendue (nuit incertaine = 1 − p) (retenu)).



### P4 · Patients « Ancien » reportés

177 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | pinball τ=0.8 retenue | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Garder toutes les lignes (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.719 | 0.9447 | 7.3 | 2.719 | 0.9447 | 4.8 |  |  | — choix retenu |
| Fusionner les reports confirmés | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.719 | 0.9447 | 7.3 | 2.719 | 0.9447 | 4.7 |  |  | identique |


Aucune variante ne fait significativement mieux que le choix retenu (Garder toutes les lignes (retenu)).



### P5 · Période exploitable

177 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | pinball τ=0.8 retenue | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Durées connues ≥ 80 % | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.719 | 0.9447 | 7.3 | 2.719 | 0.9447 | 4.9 |  |  | identique |
| Durées connues ≥ 90 % (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.719 | 0.9447 | 7.3 | 2.719 | 0.9447 | 4.9 |  |  | — choix retenu |
| Durées connues ≥ 95 % | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.719 | 0.9447 | 7.3 | 2.719 | 0.9447 | 4.9 |  |  | identique |
| ≥ 90 %, sans rodage au début (premier mois = début réel du registre) | 01/07/2025 | 0 | 9.43 | 55.5 | -4.1 | 2.744 | 0.9455 | 6.4 | 2.744 | 0.9455 | 5.5 | 0.912 | 0.912 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Durées connues ≥ 90 % (retenu)).



### P6 · Fin de série (délai d'inscription)

170 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | pinball τ=0.8 retenue | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Aucune coupe | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.771 | 0.9631 | 4.5 | 2.771 | 0.9631 | 4.9 |  |  | identique |
| 7 derniers jours retirés | 15/07/2025 | 7 | 9.71 | 57.1 | -3.7 | 2.771 | 0.9631 | 4.5 | 2.771 | 0.9631 | 4.9 |  |  | identique |
| p95 du délai d'inscription (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.771 | 0.9631 | 4.5 | 2.771 | 0.9631 | 4.7 |  |  | — choix retenu |


Aucune variante ne fait significativement mieux que le choix retenu (p95 du délai d'inscription (retenu)).



### P7 · Trous de saisie (≥ 4 jours sans admission)

177 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | pinball τ=0.8 retenue | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Gardés tels quels (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.719 | 0.9447 | 7.3 | 2.719 | 0.9447 | 4.7 |  |  | — choix retenu |
| Lignes d'apprentissage qui les touchent exclues | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.726 | 0.9445 | 7.1 | 2.726 | 0.9445 | 6.0 | 0.9177 | 0.9177 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Gardés tels quels (retenu)).



### P8 · Méthode de comptage des présents

177 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | pinball τ=0.8 retenue | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Recensement de minuit (nuits passées) (retenu) | 15/07/2025 | 0 | 9.73 | 57.2 | -3.6 | 2.719 | 0.9447 | 7.3 | 2.719 | 0.9447 | 4.8 |  |  | — choix retenu |
| Présence dans la journée (jour de sortie compris) | 15/07/2025 | 0 | 12.27 | 72.2 | -2.8 | 3.129 | 1.0459 | -1.7 | 2.849 | 0.954 | 4.6 | 0.9495 | 0.9495 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Recensement de minuit (nuits passées) (retenu)).



### P1 × modèles (J+7) : chaque méthode des durées inconnues avec chaque modèle

9 jours évalués ; tri par MAE contre la série retenue.

| variante | imputation | modèle | famille | cle_imputation | cle_modele | pinball τ=0.8 retenue | MAE retenue | MAE propre | pinball τ=0.8 propre | temps (s) | DM p vs paire retenue | DM p vs imputation retenue, même modèle | p Holm vs paire retenue | vs paire retenue | p Holm vs imputation retenue, même modèle | vs imputation retenue, même modèle |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Médiane de la tranche d'âge | E · XGBoost quantile (second ordre) | concurrent | mediane_age | xgboost | 0.4947 | 1.858 | 1.969 | 0.5392 | 9.9 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 1 | Médiane du service | E · XGBoost quantile (second ordre) | concurrent | mediane | xgboost | 0.4947 | 1.858 | 1.969 | 0.5392 | 9.9 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 2 | SoftImpute (norme nucléaire) | E · XGBoost quantile (second ordre) | concurrent | softimpute | xgboost | 0.501 | 1.719 | 1.656 | 0.5232 | 10.3 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 3 | SoftImpute (norme nucléaire) | B · gradient boosting quantile | concurrent | softimpute | boosting | 0.5091 | 1.633 | 1.593 | 0.518 | 9.1 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 4 | SoftImpute (norme nucléaire) | A · forêt aléatoire quantile | concurrent | softimpute | foret | 0.5128 | 1.456 | 1.345 | 0.535 | 10.3 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 5 | k plus proches voisins (prix, âge, sexe, issue, mois) | E · XGBoost quantile (second ordre) | concurrent | knn | xgboost | 0.516 | 1.714 | 1.714 | 0.516 | 9.7 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 6 | Loi normale multivariée par EM | C · perceptron multicouche quantile | concurrent | em | mlp | 0.5168 | 1.947 | 1.947 | 0.5168 | 1.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 7 | Régressions enchaînées (ridge, principe de MICE) | A · forêt aléatoire quantile | concurrent | regression | foret | 0.5245 | 1.566 | 1.566 | 0.5245 | 10.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 8 | Hybride : prix, sinon XGBoost | E · XGBoost quantile (second ordre) | concurrent | hybride | xgboost | 0.5247 | 2.145 | 2.145 | 0.5247 | 10.6 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 9 | k plus proches voisins (prix, âge, sexe, issue, mois) | C · perceptron multicouche quantile | concurrent | knn | mlp | 0.5266 | 2.012 | 2.012 | 0.5266 | 1.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 10 | Médiane de la tranche d'âge | C · perceptron multicouche quantile | concurrent | mediane_age | mlp | 0.5325 | 2.039 | 2.039 | 0.577 | 0.9 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 11 | Médiane du service | C · perceptron multicouche quantile | concurrent | mediane | mlp | 0.5325 | 2.039 | 2.039 | 0.577 | 0.9 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 12 | Régressions enchaînées (ridge, principe de MICE) | B · gradient boosting quantile | concurrent | regression | boosting | 0.5366 | 1.519 | 1.519 | 0.5366 | 9.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 13 | Hybride : prix, sinon XGBoost | A · forêt aléatoire quantile | concurrent | hybride | foret | 0.5467 | 1.646 | 1.646 | 0.5467 | 10.5 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 14 | k plus proches voisins (prix, âge, sexe, issue, mois) | B · gradient boosting quantile | concurrent | knn | boosting | 0.5471 | 1.611 | 1.611 | 0.5471 | 8.5 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 15 | SoftImpute (norme nucléaire) | C · perceptron multicouche quantile | concurrent | softimpute | mlp | 0.5491 | 1.998 | 1.887 | 0.5713 | 1.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 16 | Loi normale multivariée par EM | A · forêt aléatoire quantile | concurrent | em | foret | 0.5492 | 1.554 | 1.554 | 0.5492 | 10.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 17 | Loi normale multivariée par EM | E · XGBoost quantile (second ordre) | concurrent | em | xgboost | 0.5493 | 1.706 | 1.706 | 0.5493 | 10.1 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 18 | Régressions enchaînées (ridge, principe de MICE) | C · perceptron multicouche quantile | concurrent | regression | mlp | 0.5522 | 1.969 | 1.969 | 0.5522 | 1.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 19 | Médiane du service | B · gradient boosting quantile | concurrent | mediane | boosting | 0.5541 | 1.753 | 1.901 | 0.5986 | 8.5 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 20 | Médiane de la tranche d'âge | B · gradient boosting quantile | concurrent | mediane_age | boosting | 0.5541 | 1.753 | 1.901 | 0.5986 | 8.4 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 21 | XGBoost (avec le diagnostic) | A · forêt aléatoire quantile | concurrent | xgboost | foret | 0.5575 | 1.678 | 1.678 | 0.5575 | 10.5 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 22 | XGBoost (avec le diagnostic) | C · perceptron multicouche quantile | concurrent | xgboost | mlp | 0.5582 | 1.958 | 1.958 | 0.5582 | 1.1 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 23 | Régressions enchaînées (ridge, principe de MICE) | E · XGBoost quantile (second ordre) | concurrent | regression | xgboost | 0.559 | 1.937 | 1.937 | 0.559 | 10.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 24 | Loi normale multivariée par EM | B · gradient boosting quantile | concurrent | em | boosting | 0.5603 | 1.798 | 1.798 | 0.5603 | 8.7 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 25 | Estimée : prix, puis issue, puis médiane | C · perceptron multicouche quantile | concurrent | estimee | mlp | 0.5605 | 1.963 | 1.963 | 0.5605 | 1.0 |  |  |  | non testé (trop peu de jours) |  | — référence |
| 26 | ACP itérative (rang faible) | SVR quantile composite (niveau 4, retenu) | svm | acp_iterative | svr_q_composite | 0.5606 | 1.804 | 1.804 | 0.5606 | 5.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 27 | ACP itérative (rang faible) | SVR quantile, noyau laplacien | svm | acp_iterative | svr_q_laplacien | 0.5627 | 1.77 | 1.77 | 0.5627 | 1.8 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 28 | Moyenne du service | B · gradient boosting quantile | concurrent | moyenne | boosting | 0.5634 | 1.86 | 1.788 | 0.5857 | 8.3 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 29 | XGBoost (avec le diagnostic) | B · gradient boosting quantile | concurrent | xgboost | boosting | 0.5654 | 1.801 | 1.801 | 0.5654 | 9.1 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 30 | Estimée : prix, puis issue, puis médiane | B · gradient boosting quantile | concurrent | estimee | boosting | 0.5696 | 1.708 | 1.708 | 0.5696 | 8.5 |  |  |  | non testé (trop peu de jours) |  | — référence |
| 31 | ACP itérative (rang faible) | SVR quantile RBF (niveau 3) | svm | acp_iterative | svr_q_rbf | 0.5698 | 1.778 | 1.778 | 0.5698 | 1.8 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 32 | Médiane de la tranche d'âge | A · forêt aléatoire quantile | concurrent | mediane_age | foret | 0.5714 | 1.615 | 1.615 | 0.6159 | 9.8 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 33 | Médiane du service | A · forêt aléatoire quantile | concurrent | mediane | foret | 0.5714 | 1.615 | 1.615 | 0.6159 | 9.9 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 34 | k plus proches voisins (prix, âge, sexe, issue, mois) | A · forêt aléatoire quantile | concurrent | knn | foret | 0.5714 | 1.61 | 1.61 | 0.5714 | 9.9 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 35 | Estimée : prix, puis issue, puis médiane | E · XGBoost quantile (second ordre) | concurrent | estimee | xgboost | 0.5739 | 1.68 | 1.68 | 0.5739 | 9.7 |  |  |  | non testé (trop peu de jours) |  | — référence |
| 36 | Exclure les séjours sans durée | E · XGBoost quantile (second ordre) | concurrent | exclure | xgboost | 0.5778 | 2.109 | 2.331 | 0.6666 | 2.7 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 37 | XGBoost (avec le diagnostic) | E · XGBoost quantile (second ordre) | concurrent | xgboost | xgboost | 0.5783 | 1.91 | 1.91 | 0.5783 | 10.6 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 38 | Hybride : prix, sinon XGBoost | C · perceptron multicouche quantile | concurrent | hybride | mlp | 0.5807 | 2.044 | 2.044 | 0.5807 | 1.1 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 39 | Hybride : prix, sinon XGBoost | SVR quantile, noyau laplacien | svm | hybride | svr_q_laplacien | 0.5811 | 1.74 | 1.74 | 0.5811 | 2.3 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 40 | XGBoost (avec le diagnostic) | SVR quantile, noyau laplacien | svm | xgboost | svr_q_laplacien | 0.5835 | 1.742 | 1.742 | 0.5835 | 2.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 41 | Hybride : prix, sinon XGBoost | SVR quantile RBF (niveau 3) | svm | hybride | svr_q_rbf | 0.5859 | 1.767 | 1.767 | 0.5859 | 1.6 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 42 | Estimée : prix, puis issue, puis médiane | SVR quantile, noyau laplacien | svm | estimee | svr_q_laplacien | 0.5883 | 1.725 | 1.725 | 0.5883 | 2.6 |  |  |  | non testé (trop peu de jours) |  | — référence |
| 43 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile, noyau laplacien | svm | regression | svr_q_laplacien | 0.589 | 1.735 | 1.735 | 0.589 | 3.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 44 | Loi normale multivariée par EM | SVR quantile, noyau laplacien | svm | em | svr_q_laplacien | 0.5898 | 1.735 | 1.735 | 0.5898 | 1.9 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 45 | SoftImpute (norme nucléaire) | SVR quantile, noyau laplacien | svm | softimpute | svr_q_laplacien | 0.5905 | 1.741 | 1.67 | 0.6127 | 2.4 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 46 | Médiane du service | SVR quantile, noyau laplacien | svm | mediane | svr_q_laplacien | 0.5907 | 1.739 | 1.776 | 0.6351 | 2.5 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 47 | Médiane de la tranche d'âge | SVR quantile, noyau laplacien | svm | mediane_age | svr_q_laplacien | 0.5907 | 1.739 | 1.776 | 0.6351 | 2.5 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 48 | XGBoost (avec le diagnostic) | SVR quantile composite (niveau 4, retenu) | svm | xgboost | svr_q_composite | 0.5927 | 1.805 | 1.805 | 0.5927 | 4.7 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 49 | Hybride : prix, sinon XGBoost | SVR quantile composite (niveau 4, retenu) | svm | hybride | svr_q_composite | 0.5931 | 1.805 | 1.805 | 0.5931 | 5.6 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 50 | Moyenne du service | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | moyenne | lssvr_rbf | 0.5932 | 1.78 | 1.669 | 0.6154 | 0.1 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 51 | Estimée : prix, puis issue, puis médiane | A · forêt aléatoire quantile | concurrent | estimee | foret | 0.5936 | 1.532 | 1.532 | 0.5936 | 10.1 |  |  |  | non testé (trop peu de jours) |  | — référence |
| 52 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile, noyau laplacien | svm | knn | svr_q_laplacien | 0.5972 | 1.737 | 1.737 | 0.5972 | 2.6 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 53 | XGBoost (avec le diagnostic) | SVR quantile RBF (niveau 3) | svm | xgboost | svr_q_rbf | 0.5998 | 1.767 | 1.767 | 0.5998 | 1.8 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 54 | Moyenne du service | C · perceptron multicouche quantile | concurrent | moyenne | mlp | 0.601 | 1.92 | 1.809 | 0.6232 | 0.9 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 55 | Moyenne du service | E · XGBoost quantile (second ordre) | concurrent | moyenne | xgboost | 0.6026 | 1.659 | 1.665 | 0.6249 | 9.5 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 56 | ACP itérative (rang faible) | A · forêt aléatoire quantile | concurrent | acp_iterative | foret | 0.6043 | 1.769 | 1.769 | 0.6043 | 10.4 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 57 | Hybride : prix, sinon XGBoost | SVR quantile, noyau polynomial (degré 2) | svm | hybride | svr_q_polynomial | 0.607 | 1.797 | 1.797 | 0.607 | 4.6 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 58 | ACP itérative (rang faible) | SVR quantile, noyau polynomial (degré 2) | svm | acp_iterative | svr_q_polynomial | 0.6073 | 1.765 | 1.765 | 0.6073 | 3.4 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 59 | Loi normale multivariée par EM | SVR quantile RBF (niveau 3) | svm | em | svr_q_rbf | 0.6077 | 1.762 | 1.762 | 0.6077 | 2.3 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 60 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile RBF (niveau 3) | svm | regression | svr_q_rbf | 0.6085 | 1.757 | 1.757 | 0.6085 | 2.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 61 | XGBoost (avec le diagnostic) | SVR quantile, noyau polynomial (degré 2) | svm | xgboost | svr_q_polynomial | 0.6108 | 1.793 | 1.793 | 0.6108 | 4.7 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 62 | Estimée : prix, puis issue, puis médiane | SVR quantile RBF (niveau 3) | svm | estimee | svr_q_rbf | 0.6113 | 1.744 | 1.744 | 0.6113 | 2.2 |  |  |  | non testé (trop peu de jours) |  | — référence |
| 63 | Médiane de la tranche d'âge | SVR quantile RBF (niveau 3) | svm | mediane_age | svr_q_rbf | 0.6145 | 1.78 | 1.873 | 0.6589 | 2.1 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 64 | Médiane du service | SVR quantile RBF (niveau 3) | svm | mediane | svr_q_rbf | 0.6145 | 1.78 | 1.873 | 0.6589 | 2.1 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 65 | SoftImpute (norme nucléaire) | SVR quantile, noyau polynomial (degré 2) | svm | softimpute | svr_q_polynomial | 0.6147 | 1.794 | 1.84 | 0.6369 | 3.7 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 66 | SoftImpute (norme nucléaire) | SVR quantile RBF (niveau 3) | svm | softimpute | svr_q_rbf | 0.6155 | 1.782 | 1.766 | 0.6377 | 1.9 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 67 | Hybride : prix, sinon XGBoost | B · gradient boosting quantile | concurrent | hybride | boosting | 0.6157 | 2.116 | 2.116 | 0.6157 | 9.5 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 68 | Médiane du service | SVR quantile, noyau polynomial (degré 2) | svm | mediane | svr_q_polynomial | 0.6158 | 1.787 | 1.938 | 0.6602 | 3.8 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 69 | Médiane de la tranche d'âge | SVR quantile, noyau polynomial (degré 2) | svm | mediane_age | svr_q_polynomial | 0.6158 | 1.787 | 1.938 | 0.6602 | 3.8 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 70 | k plus proches voisins (prix, âge, sexe, issue, mois) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | knn | lssvr_rbf | 0.6207 | 1.677 | 1.677 | 0.6207 | 0.1 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 71 | Exclure les séjours sans durée | A · forêt aléatoire quantile | concurrent | exclure | foret | 0.6222 | 1.726 | 1.948 | 0.7111 | 1.3 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 72 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile, noyau polynomial (degré 2) | svm | knn | svr_q_polynomial | 0.6224 | 1.746 | 1.746 | 0.6224 | 5.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 73 | ACP itérative (rang faible) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | acp_iterative | lssvr_rbf | 0.6236 | 1.646 | 1.646 | 0.6236 | 0.1 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 74 | Estimée : prix, puis issue, puis médiane | SVR quantile, noyau polynomial (degré 2) | svm | estimee | svr_q_polynomial | 0.6268 | 1.739 | 1.739 | 0.6268 | 3.7 |  |  |  | non testé (trop peu de jours) |  | — référence |
| 75 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile RBF (niveau 3) | svm | knn | svr_q_rbf | 0.6279 | 1.763 | 1.763 | 0.6279 | 2.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 76 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile, noyau polynomial (degré 2) | svm | regression | svr_q_polynomial | 0.6285 | 1.755 | 1.755 | 0.6285 | 4.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 77 | Loi normale multivariée par EM | SVR quantile, noyau polynomial (degré 2) | svm | em | svr_q_polynomial | 0.6292 | 1.762 | 1.762 | 0.6292 | 3.9 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 78 | Loi normale multivariée par EM | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | em | lssvr_rbf | 0.6311 | 1.679 | 1.679 | 0.6311 | 0.1 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 79 | Régressions enchaînées (ridge, principe de MICE) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | regression | lssvr_rbf | 0.6318 | 1.677 | 1.677 | 0.6318 | 0.1 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 80 | Exclure les séjours sans durée | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | exclure | lssvr_rbf | 0.6325 | 1.818 | 1.982 | 0.6102 | 0.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 81 | Médiane de la tranche d'âge | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | mediane_age | lssvr_rbf | 0.6351 | 1.733 | 1.733 | 0.6796 | 0.1 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 82 | Médiane du service | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | mediane | lssvr_rbf | 0.6351 | 1.733 | 1.733 | 0.6796 | 0.1 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 83 | Estimée : prix, puis issue, puis médiane | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | estimee | lssvr_rbf | 0.6396 | 1.656 | 1.656 | 0.6396 | 0.1 |  |  |  | non testé (trop peu de jours) |  | — référence |
| 84 | Moyenne du service | SVR quantile, noyau laplacien | svm | moyenne | svr_q_laplacien | 0.6408 | 1.8 | 1.812 | 0.663 | 2.4 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 85 | ACP itérative (rang faible) | C · perceptron multicouche quantile | concurrent | acp_iterative | mlp | 0.6419 | 2.133 | 2.133 | 0.6419 | 1.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 86 | Loi normale multivariée par EM | SVR quantile composite (niveau 4, retenu) | svm | em | svr_q_composite | 0.6465 | 1.809 | 1.809 | 0.6465 | 4.4 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 87 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile composite (niveau 4, retenu) | svm | regression | svr_q_composite | 0.6484 | 1.806 | 1.806 | 0.6484 | 4.9 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 88 | Estimée : prix, puis issue, puis médiane | SVR quantile composite (niveau 4, retenu) | svm | estimee | svr_q_composite | 0.6511 | 1.811 | 1.811 | 0.6511 | 4.2 |  |  |  | — référence |  | — référence |
| 89 | SoftImpute (norme nucléaire) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | softimpute | lssvr_rbf | 0.6544 | 1.719 | 1.608 | 0.6766 | 0.1 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 90 | Exclure les séjours sans durée | SVR quantile, noyau polynomial (degré 2) | svm | exclure | svr_q_polynomial | 0.6553 | 2.156 | 2.378 | 0.7442 | 2.2 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 91 | Moyenne du service | A · forêt aléatoire quantile | concurrent | moyenne | foret | 0.6565 | 1.667 | 1.556 | 0.6787 | 9.9 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 92 | Moyenne du service | SVR quantile RBF (niveau 3) | svm | moyenne | svr_q_rbf | 0.6611 | 1.815 | 1.865 | 0.6833 | 2.1 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 93 | SoftImpute (norme nucléaire) | SVR quantile composite (niveau 4, retenu) | svm | softimpute | svr_q_composite | 0.6611 | 1.813 | 1.807 | 0.6833 | 4.5 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 94 | Médiane de la tranche d'âge | SVR quantile composite (niveau 4, retenu) | svm | mediane_age | svr_q_composite | 0.6617 | 1.819 | 1.929 | 0.7061 | 4.4 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 95 | Médiane du service | SVR quantile composite (niveau 4, retenu) | svm | mediane | svr_q_composite | 0.6617 | 1.819 | 1.929 | 0.7061 | 4.5 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 96 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile composite (niveau 4, retenu) | svm | knn | svr_q_composite | 0.6626 | 1.808 | 1.808 | 0.6626 | 4.2 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 97 | XGBoost (avec le diagnostic) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | xgboost | lssvr_rbf | 0.6663 | 1.686 | 1.686 | 0.6663 | 0.1 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 98 | ACP itérative (rang faible) | E · XGBoost quantile (second ordre) | concurrent | acp_iterative | xgboost | 0.667 | 1.577 | 1.577 | 0.667 | 10.3 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 99 | Hybride : prix, sinon XGBoost | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | hybride | lssvr_rbf | 0.668 | 1.675 | 1.675 | 0.668 | 0.1 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 100 | k plus proches voisins (prix, âge, sexe, issue, mois) | D · LSTM quantile | concurrent | knn | lstm | 0.6699 | 2.137 | 2.137 | 0.6699 | 6.8 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 101 | Moyenne du service | SVR quantile, noyau polynomial (degré 2) | svm | moyenne | svr_q_polynomial | 0.6803 | 1.927 | 2.038 | 0.7025 | 4.8 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 102 | Exclure les séjours sans durée | D · LSTM quantile | concurrent | exclure | lstm | 0.6831 | 2.962 | 3.406 | 0.772 | 1.4 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 103 | Moyenne du service | SVR quantile composite (niveau 4, retenu) | svm | moyenne | svr_q_composite | 0.6883 | 1.868 | 1.919 | 0.7105 | 4.6 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 104 | ACP itérative (rang faible) | B · gradient boosting quantile | concurrent | acp_iterative | boosting | 0.6962 | 1.499 | 1.499 | 0.6962 | 8.9 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 105 | Moyenne du service | D · LSTM quantile | concurrent | moyenne | lstm | 0.7049 | 2.074 | 1.984 | 0.7271 | 6.1 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 106 | Estimée : prix, puis issue, puis médiane | D · LSTM quantile | concurrent | estimee | lstm | 0.7069 | 1.906 | 1.906 | 0.7069 | 6.0 |  |  |  | non testé (trop peu de jours) |  | — référence |
| 107 | Loi normale multivariée par EM | D · LSTM quantile | concurrent | em | lstm | 0.7186 | 2.372 | 2.372 | 0.7186 | 7.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 108 | Régressions enchaînées (ridge, principe de MICE) | D · LSTM quantile | concurrent | regression | lstm | 0.7218 | 2.345 | 2.345 | 0.7218 | 7.2 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 109 | SoftImpute (norme nucléaire) | D · LSTM quantile | concurrent | softimpute | lstm | 0.7295 | 2.327 | 2.278 | 0.7517 | 7.5 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 110 | Hybride : prix, sinon XGBoost | D · LSTM quantile | concurrent | hybride | lstm | 0.7306 | 2.236 | 2.236 | 0.7306 | 7.4 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 111 | ACP itérative (rang faible) | D · LSTM quantile | concurrent | acp_iterative | lstm | 0.7342 | 2.567 | 2.567 | 0.7342 | 6.6 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 112 | Exclure les séjours sans durée | B · gradient boosting quantile | concurrent | exclure | boosting | 0.7515 | 2.01 | 2.232 | 0.7293 | 2.9 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 113 | Médiane du service | D · LSTM quantile | concurrent | mediane | lstm | 0.7555 | 2.008 | 2.041 | 0.7999 | 6.6 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 114 | Médiane de la tranche d'âge | D · LSTM quantile | concurrent | mediane_age | lstm | 0.7555 | 2.008 | 2.041 | 0.7999 | 6.7 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 115 | Exclure les séjours sans durée | SVR quantile RBF (niveau 3) | svm | exclure | svr_q_rbf | 0.7578 | 1.91 | 2.132 | 0.8467 | 0.8 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 116 | Exclure les séjours sans durée | SVR quantile composite (niveau 4, retenu) | svm | exclure | svr_q_composite | 0.764 | 1.902 | 2.124 | 0.8529 | 3.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 117 | Exclure les séjours sans durée | SVR quantile, noyau laplacien | svm | exclure | svr_q_laplacien | 0.7756 | 1.863 | 2.085 | 0.8645 | 1.5 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 118 | Exclure les séjours sans durée | SVR linéaire (niveau 1) | svm | exclure | svr_lineaire | 0.8252 | 2.488 | 2.932 | 0.9141 | 0.3 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 119 | XGBoost (avec le diagnostic) | D · LSTM quantile | concurrent | xgboost | lstm | 0.8663 | 2.456 | 2.456 | 0.8663 | 7.5 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 120 | Moyenne du service | SVR RBF (niveau 2) | svm | moyenne | svr_rbf | 0.8694 | 1.78 | 1.683 | 0.7876 | 0.8 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 121 | Exclure les séjours sans durée | SVR RBF (niveau 2) | svm | exclure | svr_rbf | 0.9017 | 1.877 | 2.1 | 0.8795 | 0.5 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 122 | Moyenne du service | SVR linéaire (niveau 1) | svm | moyenne | svr_lineaire | 0.9103 | 1.871 | 1.92 | 0.9014 | 0.7 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 123 | ACP itérative (rang faible) | SVR RBF (niveau 2) | svm | acp_iterative | svr_rbf | 0.9361 | 1.698 | 1.698 | 0.9361 | 1.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 124 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR RBF (niveau 2) | svm | knn | svr_rbf | 0.9402 | 1.829 | 1.829 | 0.9402 | 1.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 125 | Estimée : prix, puis issue, puis médiane | SVR RBF (niveau 2) | svm | estimee | svr_rbf | 0.9522 | 1.857 | 1.857 | 0.9522 | 1.3 |  |  |  | non testé (trop peu de jours) |  | — référence |
| 126 | Médiane du service | SVR RBF (niveau 2) | svm | mediane | svr_rbf | 0.9586 | 1.876 | 1.884 | 0.8963 | 1.3 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 127 | Médiane de la tranche d'âge | SVR RBF (niveau 2) | svm | mediane_age | svr_rbf | 0.9586 | 1.876 | 1.884 | 0.8963 | 1.3 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 128 | SoftImpute (norme nucléaire) | SVR linéaire (niveau 1) | svm | softimpute | svr_lineaire | 0.9662 | 1.879 | 1.925 | 0.956 | 0.7 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 129 | Médiane du service | SVR linéaire (niveau 1) | svm | mediane | svr_lineaire | 0.9745 | 1.906 | 2.067 | 0.9885 | 0.9 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 130 | Médiane de la tranche d'âge | SVR linéaire (niveau 1) | svm | mediane_age | svr_lineaire | 0.9745 | 1.906 | 2.067 | 0.9885 | 0.8 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 131 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR linéaire (niveau 1) | svm | knn | svr_lineaire | 0.9764 | 1.867 | 1.867 | 0.9764 | 0.7 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 132 | Régressions enchaînées (ridge, principe de MICE) | SVR RBF (niveau 2) | svm | regression | svr_rbf | 0.9795 | 1.895 | 1.895 | 0.9795 | 1.0 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 133 | Loi normale multivariée par EM | SVR RBF (niveau 2) | svm | em | svr_rbf | 0.9828 | 1.906 | 1.906 | 0.9828 | 1.2 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 134 | Estimée : prix, puis issue, puis médiane | SVR linéaire (niveau 1) | svm | estimee | svr_lineaire | 0.9868 | 1.946 | 1.946 | 0.9868 | 0.8 |  |  |  | non testé (trop peu de jours) |  | — référence |
| 135 | SoftImpute (norme nucléaire) | SVR RBF (niveau 2) | svm | softimpute | svr_rbf | 0.9874 | 1.912 | 1.807 | 0.9016 | 1.1 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 136 | XGBoost (avec le diagnostic) | SVR RBF (niveau 2) | svm | xgboost | svr_rbf | 0.9876 | 1.887 | 1.887 | 0.9876 | 1.4 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 137 | Hybride : prix, sinon XGBoost | SVR RBF (niveau 2) | svm | hybride | svr_rbf | 0.9895 | 1.898 | 1.898 | 0.9895 | 1.4 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 138 | Hybride : prix, sinon XGBoost | SVR linéaire (niveau 1) | svm | hybride | svr_lineaire | 1.0083 | 1.982 | 1.982 | 1.0083 | 0.8 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 139 | XGBoost (avec le diagnostic) | SVR linéaire (niveau 1) | svm | xgboost | svr_lineaire | 1.0105 | 1.992 | 1.992 | 1.0105 | 0.8 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 140 | Exclure les séjours sans durée | C · perceptron multicouche quantile | concurrent | exclure | mlp | 1.015 | 2.887 | 3.11 | 1.1039 | 0.3 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 141 | Loi normale multivariée par EM | SVR linéaire (niveau 1) | svm | em | svr_lineaire | 1.0268 | 1.979 | 1.979 | 1.0268 | 0.8 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 142 | Régressions enchaînées (ridge, principe de MICE) | SVR linéaire (niveau 1) | svm | regression | svr_lineaire | 1.0281 | 1.982 | 1.982 | 1.0281 | 0.7 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |
| 143 | ACP itérative (rang faible) | SVR linéaire (niveau 1) | svm | acp_iterative | svr_lineaire | 1.0626 | 1.92 | 1.92 | 1.0626 | 0.8 |  |  |  | non testé (trop peu de jours) |  | non testé (trop peu de jours) |


Meilleure paire : **Médiane de la tranche d'âge × E · XGBoost quantile (second ordre)**.
