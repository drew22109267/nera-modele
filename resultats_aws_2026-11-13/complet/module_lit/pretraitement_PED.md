# Banc de comparaison du prétraitement — service PED

Une décision change à la fois ; « (retenu) » = choix retenu. MAE « propre » : contre la série de la variante ; MAE « retenue » : contre la série du choix retenu, mêmes jours pour toutes les variantes. Diebold-Mariano (perte pinball au quantile τ=0.8, correction HLN) contre la série retenue, puis correction de Holm sur les variantes d'une même dimension ; la p-valeur sur la MAE reste affichée.


## Horizon J+1


### P1 · Durées inconnues

179 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Exclure les séjours sans durée | 15/07/2024 | 4 | 7.21 | 40.0 | -0.0 | 1.856 | 0.6537 | 0.3 | 2.508 | 6.8 | 1.0556 | 0.0 | 0.0 | 0.0 | moins bon |
| Médiane du service | 15/07/2024 | 4 | 8.62 | 47.9 | -1.6 | 1.955 | 0.7221 | 3.2 | 1.964 | 8.2 | 0.6986 | 0.6463 | 1.0 | 0.8192 | équivalent |
| Moyenne du service | 15/07/2024 | 4 | 8.62 | 47.9 | -1.6 | 1.955 | 0.7221 | 3.2 | 1.964 | 9.8 | 0.6986 | 0.6463 | 1.0 | 0.8192 | équivalent |
| Médiane de la tranche d'âge | 15/07/2024 | 4 | 8.62 | 47.9 | -1.6 | 1.955 | 0.7221 | 3.2 | 1.964 | 8.8 | 0.6986 | 0.6463 | 1.0 | 0.8192 | équivalent |
| Estimée : prix, puis issue, puis médiane (retenu) | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 1.958 | 0.7022 | 3.1 | 1.958 | 8.7 | 0.7022 |  |  |  | — choix retenu |
| k plus proches voisins (prix, âge, sexe, issue, mois) | 15/07/2024 | 4 | 8.48 | 47.1 | -3.2 | 1.937 | 0.7073 | 2.6 | 1.966 | 12.9 | 0.6998 | 0.7854 | 1.0 | 0.7258 | équivalent |
| Régressions enchaînées (ridge, principe de MICE) | 15/07/2024 | 4 | 8.46 | 47.0 | -3.4 | 1.968 | 0.7113 | 2.6 | 1.972 | 16.8 | 0.6987 | 0.3456 | 1.0 | 0.2791 | équivalent |
| Loi normale multivariée par EM | 15/07/2024 | 4 | 8.46 | 47.0 | -3.4 | 1.971 | 0.707 | 1.9 | 1.977 | 20.8 | 0.6991 | 0.3878 | 1.0 | 0.1356 | équivalent |
| ACP itérative (rang faible) | 15/07/2024 | 4 | 8.68 | 48.2 | -0.9 | 2.001 | 0.7223 | -0.7 | 2.009 | 23.6 | 0.699 | 0.8403 | 1.0 | 0.304 | équivalent |
| SoftImpute (norme nucléaire) | 15/07/2024 | 4 | 8.48 | 47.1 | -3.2 | 1.954 | 0.7131 | 3.8 | 1.944 | 14.3 | 0.6925 | 0.1247 | 1.0 | 0.4266 | équivalent |
| XGBoost (avec le diagnostic) | 15/07/2024 | 4 | 8.26 | 45.9 | -5.8 | 1.981 | 0.7032 | -0.2 | 2.011 | 62.1 | 0.7107 | 0.497 | 1.0 | 0.1031 | équivalent |
| Hybride : prix, sinon XGBoost | 15/07/2024 | 4 | 8.26 | 45.9 | -5.8 | 1.982 | 0.7003 | 0.3 | 2.014 | 66.1 | 0.7064 | 0.7393 | 1.0 | 0.0825 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Estimée : prix, puis issue, puis médiane (retenu)).



### P2 · Fenêtre de censure (encore hospitalisé)

179 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 14 jours | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 1.958 | 0.7022 | 3.1 | 1.958 | 15.3 | 0.7022 |  |  |  | identique |
| 30 jours | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 1.958 | 0.7022 | 3.1 | 1.958 | 15.9 | 0.7022 |  |  |  | identique |
| p95 des durées connues (retenu) | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 1.958 | 0.7022 | 3.1 | 1.958 | 13.9 | 0.7022 |  |  |  | — choix retenu |
| 60 jours | 15/07/2024 | 4 | 8.7 | 48.3 | -2.8 | 2.082 | 0.7518 | -3.4 | 2.195 | 15.2 | 0.7578 | 0.0068 | 0.0068 | 0.0013 | moins bon |


Aucune variante ne fait significativement mieux que le choix retenu (p95 des durées connues (retenu)).



### P3 · Convention du nombre de jours

179 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Attendue (nuit incertaine = 1 − p) (retenu) | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 1.958 | 0.7022 | 3.1 | 1.958 | 15.0 | 0.7022 |  |  |  | — choix retenu |
| Tout inclusif (borne basse) | 15/07/2024 | 4 | 7.94 | 44.1 | -6.8 | 1.935 | 0.6825 | 2.4 | 2.008 | 13.9 | 0.7241 | 0.267 | 0.3184 | 0.2233 | équivalent |
| Tout en nuits (borne haute) | 15/07/2024 | 4 | 9.02 | 50.1 | 2.4 | 2.071 | 0.7349 | 3.0 | 2.062 | 16.4 | 0.7234 | 0.1592 | 0.3184 | 0.062 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Attendue (nuit incertaine = 1 − p) (retenu)).



### P4 · Patients « Ancien » reportés

179 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Garder toutes les lignes (retenu) | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 1.958 | 0.7022 | 3.1 | 1.958 | 12.5 | 0.7022 |  |  |  | — choix retenu |
| Fusionner les reports confirmés | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 1.958 | 0.7022 | 3.1 | 1.958 | 13.6 | 0.7022 |  |  |  | identique |


Aucune variante ne fait significativement mieux que le choix retenu (Garder toutes les lignes (retenu)).



### P5 · Période exploitable

179 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Durées connues ≥ 80 % | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 1.958 | 0.7022 | 3.1 | 1.958 | 11.4 | 0.7022 |  |  |  | identique |
| Durées connues ≥ 90 % (retenu) | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 1.958 | 0.7022 | 3.1 | 1.958 | 13.5 | 0.7022 |  |  |  | — choix retenu |
| Durées connues ≥ 95 % | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 1.958 | 0.7022 | 3.1 | 1.958 | 12.7 | 0.7022 |  |  |  | identique |
| ≥ 90 %, sans rodage au début (premier mois = début réel du registre) | 01/07/2024 | 4 | 8.41 | 46.7 | -3.2 | 1.97 | 0.705 | 2.5 | 1.97 | 19.2 | 0.705 | 0.3975 | 0.3975 | 0.0088 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Durées connues ≥ 90 % (retenu)).



### P6 · Fin de série (délai d'inscription)

176 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Aucune coupe | 15/07/2024 | 0 | 8.44 | 46.9 | -3.4 | 1.942 | 0.6953 | 4.1 | 1.942 | 12.6 | 0.6953 |  |  |  | identique |
| 7 derniers jours retirés | 15/07/2024 | 7 | 8.49 | 47.2 | -3.6 | 1.942 | 0.6953 | 4.1 | 1.942 | 13.2 | 0.6953 |  |  |  | identique |
| p95 du délai d'inscription (retenu) | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 1.942 | 0.6953 | 4.1 | 1.942 | 14.3 | 0.6953 |  |  |  | — choix retenu |


Aucune variante ne fait significativement mieux que le choix retenu (p95 du délai d'inscription (retenu)).



### P7 · Trous de saisie (≥ 4 jours sans admission)

179 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Gardés tels quels (retenu) | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 1.958 | 0.7022 | 3.1 | 1.958 | 12.9 | 0.7022 |  |  |  | — choix retenu |
| Lignes d'apprentissage qui les touchent exclues | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 1.955 | 0.7015 | 3.2 | 1.955 | 12.1 | 0.7015 | 0.7592 | 0.7592 | 0.5331 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Gardés tels quels (retenu)).



### P8 · Méthode de comptage des présents

179 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Recensement de minuit (nuits passées) (retenu) | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 1.958 | 0.7022 | 3.1 | 1.958 | 15.2 | 0.7022 |  |  |  | — choix retenu |
| Présence dans la journée (jour de sortie compris) | 15/07/2024 | 4 | 11.17 | 62.0 | -2.6 | 1.896 | 0.7134 | 18.7 | 2.975 | 12.6 | 0.9805 | 0.0 | 0.0 | 0.0 | moins bon |


Aucune variante ne fait significativement mieux que le choix retenu (Recensement de minuit (nuits passées) (retenu)).



### P1 × modèles (J+1) : chaque méthode des durées inconnues avec chaque modèle

179 jours évalués ; tri par perte pinball τ=0.8 contre la série retenue.

| variante | imputation | modèle | famille | cle_imputation | cle_modele | pinball τ=0.8 retenue | MAE retenue | MAE propre | pinball τ=0.8 propre | temps (s) | DM p vs paire retenue | DM p vs imputation retenue, même modèle | p Holm vs paire retenue | vs paire retenue | p Holm vs imputation retenue, même modèle | vs imputation retenue, même modèle |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | SoftImpute (norme nucléaire) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | softimpute | lssvr_rbf | 0.6482 | 1.864 | 1.884 | 0.6676 | 0.5 | 0.0088 | 0.3062 | 0.9592 | équivalent | 1.0 | équivalent |
| 1 | Loi normale multivariée par EM | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | em | lssvr_rbf | 0.6511 | 1.868 | 1.863 | 0.6637 | 0.5 | 0.0165 | 0.3009 | 1.0 | équivalent | 1.0 | équivalent |
| 2 | Régressions enchaînées (ridge, principe de MICE) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | regression | lssvr_rbf | 0.652 | 1.874 | 1.864 | 0.6664 | 0.4 | 0.0194 | 0.3251 | 1.0 | équivalent | 1.0 | équivalent |
| 3 | k plus proches voisins (prix, âge, sexe, issue, mois) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | knn | lssvr_rbf | 0.6525 | 1.881 | 1.894 | 0.6643 | 0.5 | 0.0194 | 0.7242 | 1.0 | équivalent | 1.0 | équivalent |
| 4 | ACP itérative (rang faible) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | acp_iterative | lssvr_rbf | 0.6531 | 1.868 | 1.907 | 0.6917 | 0.3 | 0.0116 | 0.8943 | 1.0 | équivalent | 1.0 | équivalent |
| 5 | Moyenne du service | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | moyenne | lssvr_rbf | 0.6533 | 1.882 | 1.869 | 0.6771 | 0.5 | 0.0231 | 0.812 | 1.0 | équivalent | 1.0 | équivalent |
| 6 | Médiane de la tranche d'âge | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | mediane_age | lssvr_rbf | 0.6533 | 1.882 | 1.869 | 0.6771 | 0.7 | 0.0231 | 0.812 | 1.0 | équivalent | 1.0 | équivalent |
| 7 | Médiane du service | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | mediane | lssvr_rbf | 0.6533 | 1.882 | 1.869 | 0.6771 | 0.4 | 0.0231 | 0.812 | 1.0 | équivalent | 1.0 | équivalent |
| 8 | Régressions enchaînées (ridge, principe de MICE) | C · perceptron multicouche quantile | concurrent | regression | mlp | 0.6554 | 1.868 | 1.894 | 0.6729 | 1.6 | 0.0849 | 0.4783 | 1.0 | équivalent | 1.0 | équivalent |
| 9 | Estimée : prix, puis issue, puis médiane | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | estimee | lssvr_rbf | 0.6555 | 1.853 | 1.853 | 0.6555 | 0.6 | 0.0265 |  | 1.0 | équivalent |  | — référence |
| 10 | ACP itérative (rang faible) | C · perceptron multicouche quantile | concurrent | acp_iterative | mlp | 0.661 | 1.945 | 1.993 | 0.7064 | 1.1 | 0.09 | 0.9663 | 1.0 | équivalent | 1.0 | équivalent |
| 11 | Loi normale multivariée par EM | C · perceptron multicouche quantile | concurrent | em | mlp | 0.6613 | 1.887 | 1.92 | 0.6806 | 1.4 | 0.1082 | 0.9702 | 1.0 | équivalent | 1.0 | équivalent |
| 12 | Estimée : prix, puis issue, puis médiane | C · perceptron multicouche quantile | concurrent | estimee | mlp | 0.6618 | 1.887 | 1.887 | 0.6618 | 2.2 | 0.12 |  | 1.0 | équivalent |  | — référence |
| 13 | XGBoost (avec le diagnostic) | SVR quantile, noyau polynomial (degré 2) | svm | xgboost | svr_q_polynomial | 0.6618 | 1.901 | 1.888 | 0.6799 | 7.7 | 0.041 | 0.1861 | 1.0 | équivalent | 1.0 | équivalent |
| 14 | k plus proches voisins (prix, âge, sexe, issue, mois) | C · perceptron multicouche quantile | concurrent | knn | mlp | 0.6636 | 1.86 | 1.875 | 0.6732 | 2.1 | 0.1176 | 0.883 | 1.0 | équivalent | 1.0 | équivalent |
| 15 | Hybride : prix, sinon XGBoost | SVR quantile, noyau polynomial (degré 2) | svm | hybride | svr_q_polynomial | 0.6643 | 1.911 | 1.887 | 0.677 | 7.3 | 0.0615 | 0.3094 | 1.0 | équivalent | 1.0 | équivalent |
| 16 | SoftImpute (norme nucléaire) | C · perceptron multicouche quantile | concurrent | softimpute | mlp | 0.6654 | 1.84 | 1.881 | 0.6823 | 1.8 | 0.1371 | 0.7477 | 1.0 | équivalent | 1.0 | équivalent |
| 17 | SoftImpute (norme nucléaire) | SVR quantile, noyau polynomial (degré 2) | svm | softimpute | svr_q_polynomial | 0.6672 | 1.848 | 1.86 | 0.69 | 9.2 | 0.0566 | 0.2392 | 1.0 | équivalent | 1.0 | équivalent |
| 18 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile, noyau polynomial (degré 2) | svm | regression | svr_q_polynomial | 0.6687 | 1.871 | 1.865 | 0.6871 | 7.0 | 0.1032 | 0.1453 | 1.0 | équivalent | 1.0 | équivalent |
| 19 | ACP itérative (rang faible) | SVR quantile RBF (niveau 3) | svm | acp_iterative | svr_q_rbf | 0.6687 | 1.966 | 1.975 | 0.7036 | 3.4 | 0.037 | 0.1595 | 1.0 | équivalent | 1.0 | équivalent |
| 20 | Loi normale multivariée par EM | SVR quantile, noyau polynomial (degré 2) | svm | em | svr_q_polynomial | 0.6687 | 1.881 | 1.868 | 0.6816 | 6.3 | 0.0945 | 0.2103 | 1.0 | équivalent | 1.0 | équivalent |
| 21 | XGBoost (avec le diagnostic) | D · LSTM quantile | concurrent | xgboost | lstm | 0.6702 | 1.9 | 1.882 | 0.6958 | 8.9 | 0.1366 | 0.4097 | 1.0 | équivalent | 1.0 | équivalent |
| 22 | XGBoost (avec le diagnostic) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | xgboost | lssvr_rbf | 0.6707 | 1.931 | 1.87 | 0.6797 | 0.4 | 0.1944 | 0.313 | 1.0 | équivalent | 1.0 | équivalent |
| 23 | Loi normale multivariée par EM | D · LSTM quantile | concurrent | em | lstm | 0.672 | 1.897 | 1.903 | 0.6816 | 10.3 | 0.1789 | 0.193 | 1.0 | équivalent | 1.0 | équivalent |
| 24 | ACP itérative (rang faible) | SVR quantile, noyau polynomial (degré 2) | svm | acp_iterative | svr_q_polynomial | 0.6733 | 1.93 | 1.927 | 0.692 | 7.3 | 0.1898 | 0.8893 | 1.0 | équivalent | 1.0 | équivalent |
| 25 | Hybride : prix, sinon XGBoost | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | hybride | lssvr_rbf | 0.6734 | 1.931 | 1.871 | 0.676 | 0.3 | 0.2536 | 0.2552 | 1.0 | équivalent | 1.0 | équivalent |
| 26 | Médiane du service | SVR quantile, noyau polynomial (degré 2) | svm | mediane | svr_q_polynomial | 0.6748 | 1.855 | 1.841 | 0.6974 | 6.8 | 0.1093 | 0.8983 | 1.0 | équivalent | 1.0 | équivalent |
| 27 | Médiane de la tranche d'âge | SVR quantile, noyau polynomial (degré 2) | svm | mediane_age | svr_q_polynomial | 0.6748 | 1.855 | 1.841 | 0.6974 | 12.4 | 0.1093 | 0.8983 | 1.0 | équivalent | 1.0 | équivalent |
| 28 | Moyenne du service | SVR quantile, noyau polynomial (degré 2) | svm | moyenne | svr_q_polynomial | 0.6748 | 1.855 | 1.841 | 0.6974 | 6.0 | 0.1093 | 0.8983 | 1.0 | équivalent | 1.0 | équivalent |
| 29 | Estimée : prix, puis issue, puis médiane | SVR quantile, noyau polynomial (degré 2) | svm | estimee | svr_q_polynomial | 0.6759 | 1.873 | 1.873 | 0.6759 | 10.4 | 0.1622 |  | 1.0 | équivalent |  | — référence |
| 30 | SoftImpute (norme nucléaire) | D · LSTM quantile | concurrent | softimpute | lstm | 0.6775 | 1.837 | 1.871 | 0.6977 | 13.0 | 0.2843 | 0.6387 | 1.0 | équivalent | 1.0 | équivalent |
| 31 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile, noyau polynomial (degré 2) | svm | knn | svr_q_polynomial | 0.6776 | 1.883 | 1.873 | 0.6849 | 9.9 | 0.1578 | 0.8585 | 1.0 | équivalent | 1.0 | équivalent |
| 32 | ACP itérative (rang faible) | D · LSTM quantile | concurrent | acp_iterative | lstm | 0.6784 | 1.947 | 1.904 | 0.679 | 9.3 | 0.3121 | 0.8776 | 1.0 | équivalent | 1.0 | équivalent |
| 33 | Hybride : prix, sinon XGBoost | D · LSTM quantile | concurrent | hybride | lstm | 0.6808 | 1.901 | 1.885 | 0.699 | 9.6 | 0.3727 | 0.9651 | 1.0 | équivalent | 1.0 | équivalent |
| 34 | Estimée : prix, puis issue, puis médiane | D · LSTM quantile | concurrent | estimee | lstm | 0.6814 | 1.855 | 1.855 | 0.6814 | 18.0 | 0.3532 |  | 1.0 | équivalent |  | — référence |
| 35 | Régressions enchaînées (ridge, principe de MICE) | D · LSTM quantile | concurrent | regression | lstm | 0.6815 | 1.895 | 1.906 | 0.6992 | 9.0 | 0.3527 | 0.9787 | 1.0 | équivalent | 1.0 | équivalent |
| 36 | Médiane de la tranche d'âge | D · LSTM quantile | concurrent | mediane_age | lstm | 0.6826 | 1.843 | 1.856 | 0.6977 | 15.3 | 0.3927 | 0.9066 | 1.0 | équivalent | 1.0 | équivalent |
| 37 | Moyenne du service | D · LSTM quantile | concurrent | moyenne | lstm | 0.6826 | 1.843 | 1.856 | 0.6977 | 15.2 | 0.3927 | 0.9066 | 1.0 | équivalent | 1.0 | équivalent |
| 38 | Médiane du service | D · LSTM quantile | concurrent | mediane | lstm | 0.6826 | 1.843 | 1.856 | 0.6977 | 8.7 | 0.3927 | 0.9066 | 1.0 | équivalent | 1.0 | équivalent |
| 39 | k plus proches voisins (prix, âge, sexe, issue, mois) | D · LSTM quantile | concurrent | knn | lstm | 0.6842 | 1.849 | 1.842 | 0.6967 | 12.4 | 0.4096 | 0.7722 | 1.0 | équivalent | 1.0 | équivalent |
| 40 | Médiane du service | C · perceptron multicouche quantile | concurrent | mediane | mlp | 0.6847 | 1.904 | 1.921 | 0.6992 | 0.9 | 0.5103 | 0.1333 | 1.0 | équivalent | 1.0 | équivalent |
| 41 | Moyenne du service | C · perceptron multicouche quantile | concurrent | moyenne | mlp | 0.6847 | 1.904 | 1.921 | 0.6992 | 2.0 | 0.5103 | 0.1333 | 1.0 | équivalent | 1.0 | équivalent |
| 42 | Médiane de la tranche d'âge | C · perceptron multicouche quantile | concurrent | mediane_age | mlp | 0.6847 | 1.904 | 1.921 | 0.6992 | 1.9 | 0.5103 | 0.1333 | 1.0 | équivalent | 1.0 | équivalent |
| 43 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile RBF (niveau 3) | svm | knn | svr_q_rbf | 0.6862 | 1.944 | 1.932 | 0.6923 | 6.1 | 0.0705 | 0.574 | 1.0 | équivalent | 1.0 | équivalent |
| 44 | Loi normale multivariée par EM | SVR quantile RBF (niveau 3) | svm | em | svr_q_rbf | 0.6868 | 1.952 | 1.937 | 0.696 | 4.4 | 0.0753 | 0.3592 | 1.0 | équivalent | 1.0 | équivalent |
| 45 | Médiane de la tranche d'âge | SVR quantile RBF (niveau 3) | svm | mediane_age | svr_q_rbf | 0.687 | 1.941 | 1.94 | 0.7099 | 5.6 | 0.1439 | 0.6466 | 1.0 | équivalent | 1.0 | équivalent |
| 46 | Moyenne du service | SVR quantile RBF (niveau 3) | svm | moyenne | svr_q_rbf | 0.687 | 1.941 | 1.94 | 0.7099 | 4.1 | 0.1439 | 0.6466 | 1.0 | équivalent | 1.0 | équivalent |
| 47 | Médiane du service | SVR quantile RBF (niveau 3) | svm | mediane | svr_q_rbf | 0.687 | 1.941 | 1.94 | 0.7099 | 3.2 | 0.1439 | 0.6466 | 1.0 | équivalent | 1.0 | équivalent |
| 48 | SoftImpute (norme nucléaire) | SVR quantile RBF (niveau 3) | svm | softimpute | svr_q_rbf | 0.6871 | 1.937 | 1.951 | 0.7058 | 3.2 | 0.0825 | 0.5416 | 1.0 | équivalent | 1.0 | équivalent |
| 49 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile RBF (niveau 3) | svm | regression | svr_q_rbf | 0.6893 | 1.953 | 1.939 | 0.701 | 5.8 | 0.1416 | 0.7088 | 1.0 | équivalent | 1.0 | équivalent |
| 50 | XGBoost (avec le diagnostic) | C · perceptron multicouche quantile | concurrent | xgboost | mlp | 0.6897 | 1.932 | 1.935 | 0.6897 | 1.6 | 0.6865 | 0.1573 | 1.0 | équivalent | 1.0 | équivalent |
| 51 | Estimée : prix, puis issue, puis médiane | SVR quantile RBF (niveau 3) | svm | estimee | svr_q_rbf | 0.6909 | 1.932 | 1.932 | 0.6909 | 6.5 | 0.1391 |  | 1.0 | équivalent |  | — référence |
| 52 | SoftImpute (norme nucléaire) | SVR quantile composite (niveau 4, retenu) | svm | softimpute | svr_q_composite | 0.6925 | 1.944 | 1.954 | 0.7131 | 5.3 | 0.1247 | 0.1247 | 1.0 | équivalent | 1.0 | équivalent |
| 53 | ACP itérative (rang faible) | SVR quantile, noyau laplacien | svm | acp_iterative | svr_q_laplacien | 0.6926 | 2.053 | 2.083 | 0.75 | 4.5 | 0.6125 | 0.1684 | 1.0 | équivalent | 1.0 | équivalent |
| 54 | Hybride : prix, sinon XGBoost | A · forêt aléatoire quantile | concurrent | hybride | foret | 0.6947 | 2.034 | 1.978 | 0.7014 | 16.7 | 0.7913 | 0.3241 | 1.0 | équivalent | 1.0 | équivalent |
| 55 | XGBoost (avec le diagnostic) | A · forêt aléatoire quantile | concurrent | xgboost | foret | 0.6968 | 2.063 | 1.987 | 0.6934 | 16.8 | 0.8461 | 0.4313 | 1.0 | équivalent | 1.0 | équivalent |
| 56 | ACP itérative (rang faible) | A · forêt aléatoire quantile | concurrent | acp_iterative | foret | 0.6972 | 1.976 | 1.992 | 0.7095 | 18.6 | 0.8409 | 0.619 | 1.0 | équivalent | 1.0 | équivalent |
| 57 | XGBoost (avec le diagnostic) | SVR quantile RBF (niveau 3) | svm | xgboost | svr_q_rbf | 0.6977 | 1.966 | 1.93 | 0.6867 | 2.6 | 0.7394 | 0.5689 | 1.0 | équivalent | 1.0 | équivalent |
| 58 | Hybride : prix, sinon XGBoost | SVR quantile RBF (niveau 3) | svm | hybride | svr_q_rbf | 0.698 | 1.962 | 1.92 | 0.6849 | 3.1 | 0.7774 | 0.5766 | 1.0 | équivalent | 1.0 | équivalent |
| 59 | Médiane du service | SVR quantile composite (niveau 4, retenu) | svm | mediane | svr_q_composite | 0.6986 | 1.964 | 1.955 | 0.7221 | 6.8 | 0.6463 | 0.6463 | 1.0 | équivalent | 1.0 | équivalent |
| 60 | Médiane de la tranche d'âge | SVR quantile composite (niveau 4, retenu) | svm | mediane_age | svr_q_composite | 0.6986 | 1.964 | 1.955 | 0.7221 | 9.3 | 0.6463 | 0.6463 | 1.0 | équivalent | 1.0 | équivalent |
| 61 | Moyenne du service | SVR quantile composite (niveau 4, retenu) | svm | moyenne | svr_q_composite | 0.6986 | 1.964 | 1.955 | 0.7221 | 8.3 | 0.6463 | 0.6463 | 1.0 | équivalent | 1.0 | équivalent |
| 62 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile composite (niveau 4, retenu) | svm | regression | svr_q_composite | 0.6987 | 1.972 | 1.968 | 0.7113 | 9.1 | 0.3456 | 0.3456 | 1.0 | équivalent | 1.0 | équivalent |
| 63 | ACP itérative (rang faible) | SVR quantile composite (niveau 4, retenu) | svm | acp_iterative | svr_q_composite | 0.699 | 2.009 | 2.001 | 0.7223 | 11.1 | 0.8403 | 0.8403 | 1.0 | équivalent | 1.0 | équivalent |
| 64 | Loi normale multivariée par EM | SVR quantile composite (niveau 4, retenu) | svm | em | svr_q_composite | 0.6991 | 1.977 | 1.971 | 0.707 | 6.4 | 0.3878 | 0.3878 | 1.0 | équivalent | 1.0 | équivalent |
| 65 | ACP itérative (rang faible) | E · XGBoost quantile (second ordre) | concurrent | acp_iterative | xgboost | 0.6995 | 2.016 | 2.038 | 0.778 | 10.1 | 0.8952 | 0.1939 | 1.0 | équivalent | 1.0 | équivalent |
| 66 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile composite (niveau 4, retenu) | svm | knn | svr_q_composite | 0.6998 | 1.966 | 1.937 | 0.7073 | 14.9 | 0.7854 | 0.7854 | 1.0 | équivalent | 1.0 | équivalent |
| 67 | Hybride : prix, sinon XGBoost | C · perceptron multicouche quantile | concurrent | hybride | mlp | 0.701 | 1.932 | 1.924 | 0.6952 | 1.7 | 0.9704 | 0.0706 | 1.0 | équivalent | 1.0 | équivalent |
| 68 | Estimée : prix, puis issue, puis médiane | SVR quantile composite (niveau 4, retenu) | svm | estimee | svr_q_composite | 0.7022 | 1.958 | 1.958 | 0.7022 | 12.7 |  |  |  | — référence |  | — référence |
| 69 | Hybride : prix, sinon XGBoost | SVR quantile composite (niveau 4, retenu) | svm | hybride | svr_q_composite | 0.7064 | 2.014 | 1.982 | 0.7003 | 6.7 | 0.7393 | 0.7393 | 1.0 | équivalent | 1.0 | équivalent |
| 70 | Médiane du service | A · forêt aléatoire quantile | concurrent | mediane | foret | 0.708 | 1.973 | 1.959 | 0.7252 | 17.7 | 0.8251 | 0.8844 | 1.0 | équivalent | 1.0 | équivalent |
| 71 | Moyenne du service | A · forêt aléatoire quantile | concurrent | moyenne | foret | 0.708 | 1.973 | 1.959 | 0.7252 | 24.0 | 0.8251 | 0.8844 | 1.0 | équivalent | 1.0 | équivalent |
| 72 | Médiane de la tranche d'âge | A · forêt aléatoire quantile | concurrent | mediane_age | foret | 0.708 | 1.973 | 1.959 | 0.7252 | 23.8 | 0.8251 | 0.8844 | 1.0 | équivalent | 1.0 | équivalent |
| 73 | ACP itérative (rang faible) | B · gradient boosting quantile | concurrent | acp_iterative | boosting | 0.7101 | 2.016 | 2.006 | 0.7675 | 9.5 | 0.7735 | 0.3871 | 1.0 | équivalent | 1.0 | équivalent |
| 74 | Médiane du service | SVR quantile, noyau laplacien | svm | mediane | svr_q_laplacien | 0.7102 | 2.023 | 2.034 | 0.7383 | 4.7 | 0.6059 | 0.6246 | 1.0 | équivalent | 1.0 | équivalent |
| 75 | Moyenne du service | SVR quantile, noyau laplacien | svm | moyenne | svr_q_laplacien | 0.7102 | 2.023 | 2.034 | 0.7383 | 9.0 | 0.6059 | 0.6246 | 1.0 | équivalent | 1.0 | équivalent |
| 76 | Médiane de la tranche d'âge | SVR quantile, noyau laplacien | svm | mediane_age | svr_q_laplacien | 0.7102 | 2.023 | 2.034 | 0.7383 | 5.0 | 0.6059 | 0.6246 | 1.0 | équivalent | 1.0 | équivalent |
| 77 | Estimée : prix, puis issue, puis médiane | A · forêt aléatoire quantile | concurrent | estimee | foret | 0.7102 | 1.944 | 1.944 | 0.7102 | 21.2 | 0.7431 |  | 1.0 | équivalent |  | — référence |
| 78 | XGBoost (avec le diagnostic) | SVR quantile composite (niveau 4, retenu) | svm | xgboost | svr_q_composite | 0.7107 | 2.011 | 1.981 | 0.7032 | 7.3 | 0.497 | 0.497 | 1.0 | équivalent | 1.0 | équivalent |
| 79 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile, noyau laplacien | svm | knn | svr_q_laplacien | 0.7118 | 2.021 | 2.025 | 0.7174 | 6.7 | 0.5253 | 0.8528 | 1.0 | équivalent | 1.0 | équivalent |
| 80 | Loi normale multivariée par EM | SVR quantile, noyau laplacien | svm | em | svr_q_laplacien | 0.7121 | 2.023 | 2.026 | 0.7195 | 6.4 | 0.5153 | 0.823 | 1.0 | équivalent | 1.0 | équivalent |
| 81 | SoftImpute (norme nucléaire) | SVR quantile, noyau laplacien | svm | softimpute | svr_q_laplacien | 0.7127 | 2.009 | 2.038 | 0.7339 | 5.1 | 0.5142 | 0.9545 | 1.0 | équivalent | 1.0 | équivalent |
| 82 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile, noyau laplacien | svm | regression | svr_q_laplacien | 0.7128 | 2.023 | 2.023 | 0.7241 | 4.9 | 0.4841 | 0.9714 | 1.0 | équivalent | 1.0 | équivalent |
| 83 | Estimée : prix, puis issue, puis médiane | SVR quantile, noyau laplacien | svm | estimee | svr_q_laplacien | 0.7129 | 2.012 | 2.012 | 0.7129 | 7.8 | 0.4582 |  | 1.0 | équivalent |  | — référence |
| 84 | Régressions enchaînées (ridge, principe de MICE) | A · forêt aléatoire quantile | concurrent | regression | foret | 0.7135 | 1.927 | 1.916 | 0.7314 | 16.7 | 0.6644 | 0.7407 | 1.0 | équivalent | 1.0 | équivalent |
| 85 | SoftImpute (norme nucléaire) | A · forêt aléatoire quantile | concurrent | softimpute | foret | 0.7153 | 1.939 | 1.951 | 0.7356 | 17.2 | 0.6249 | 0.7367 | 1.0 | équivalent | 1.0 | équivalent |
| 86 | Médiane du service | E · XGBoost quantile (second ordre) | concurrent | mediane | xgboost | 0.7168 | 1.915 | 1.904 | 0.7444 | 10.3 | 0.518 | 0.4507 | 1.0 | équivalent | 1.0 | équivalent |
| 87 | Médiane de la tranche d'âge | E · XGBoost quantile (second ordre) | concurrent | mediane_age | xgboost | 0.7168 | 1.915 | 1.904 | 0.7444 | 12.5 | 0.518 | 0.4507 | 1.0 | équivalent | 1.0 | équivalent |
| 88 | Moyenne du service | E · XGBoost quantile (second ordre) | concurrent | moyenne | xgboost | 0.7168 | 1.915 | 1.904 | 0.7444 | 13.4 | 0.518 | 0.4507 | 1.0 | équivalent | 1.0 | équivalent |
| 89 | Loi normale multivariée par EM | E · XGBoost quantile (second ordre) | concurrent | em | xgboost | 0.7171 | 1.916 | 1.921 | 0.7273 | 13.4 | 0.5228 | 0.3021 | 1.0 | équivalent | 1.0 | équivalent |
| 90 | Régressions enchaînées (ridge, principe de MICE) | E · XGBoost quantile (second ordre) | concurrent | regression | xgboost | 0.7218 | 1.909 | 1.915 | 0.7332 | 11.5 | 0.428 | 0.6238 | 1.0 | équivalent | 1.0 | équivalent |
| 91 | Loi normale multivariée par EM | A · forêt aléatoire quantile | concurrent | em | foret | 0.7224 | 1.941 | 1.924 | 0.7347 | 15.7 | 0.4338 | 0.1915 | 1.0 | équivalent | 1.0 | équivalent |
| 92 | k plus proches voisins (prix, âge, sexe, issue, mois) | A · forêt aléatoire quantile | concurrent | knn | foret | 0.725 | 1.972 | 1.956 | 0.7339 | 23.5 | 0.3769 | 0.2678 | 1.0 | équivalent | 1.0 | équivalent |
| 93 | Estimée : prix, puis issue, puis médiane | E · XGBoost quantile (second ordre) | concurrent | estimee | xgboost | 0.7264 | 1.911 | 1.911 | 0.7264 | 14.2 | 0.2858 |  | 1.0 | équivalent |  | — référence |
| 94 | Hybride : prix, sinon XGBoost | SVR quantile, noyau laplacien | svm | hybride | svr_q_laplacien | 0.7273 | 2.042 | 1.987 | 0.7039 | 5.0 | 0.1935 | 0.1669 | 1.0 | équivalent | 1.0 | équivalent |
| 95 | XGBoost (avec le diagnostic) | SVR quantile, noyau laplacien | svm | xgboost | svr_q_laplacien | 0.7275 | 2.043 | 1.997 | 0.7049 | 4.5 | 0.2007 | 0.1734 | 1.0 | équivalent | 1.0 | équivalent |
| 96 | Loi normale multivariée par EM | B · gradient boosting quantile | concurrent | em | boosting | 0.7285 | 1.889 | 1.885 | 0.7438 | 11.4 | 0.3717 | 0.8068 | 1.0 | équivalent | 1.0 | équivalent |
| 97 | Régressions enchaînées (ridge, principe de MICE) | B · gradient boosting quantile | concurrent | regression | boosting | 0.7287 | 1.859 | 1.862 | 0.7444 | 8.7 | 0.3464 | 0.8338 | 1.0 | équivalent | 1.0 | équivalent |
| 98 | SoftImpute (norme nucléaire) | E · XGBoost quantile (second ordre) | concurrent | softimpute | xgboost | 0.7288 | 1.884 | 1.909 | 0.7509 | 11.9 | 0.2824 | 0.8421 | 1.0 | équivalent | 1.0 | équivalent |
| 99 | Estimée : prix, puis issue, puis médiane | B · gradient boosting quantile | concurrent | estimee | boosting | 0.7314 | 1.863 | 1.863 | 0.7314 | 12.7 | 0.3072 |  | 1.0 | équivalent |  | — référence |
| 100 | SoftImpute (norme nucléaire) | B · gradient boosting quantile | concurrent | softimpute | boosting | 0.7314 | 1.874 | 1.886 | 0.7538 | 9.4 | 0.3129 | 0.9999 | 1.0 | équivalent | 1.0 | équivalent |
| 101 | k plus proches voisins (prix, âge, sexe, issue, mois) | E · XGBoost quantile (second ordre) | concurrent | knn | xgboost | 0.7339 | 1.918 | 1.921 | 0.7318 | 14.1 | 0.1708 | 0.5832 | 1.0 | équivalent | 1.0 | équivalent |
| 102 | Hybride : prix, sinon XGBoost | E · XGBoost quantile (second ordre) | concurrent | hybride | xgboost | 0.7363 | 1.999 | 1.927 | 0.7116 | 9.8 | 0.2408 | 0.5767 | 1.0 | équivalent | 1.0 | équivalent |
| 103 | Hybride : prix, sinon XGBoost | B · gradient boosting quantile | concurrent | hybride | boosting | 0.7378 | 1.984 | 1.939 | 0.7194 | 7.7 | 0.2794 | 0.7751 | 1.0 | équivalent | 1.0 | équivalent |
| 104 | XGBoost (avec le diagnostic) | E · XGBoost quantile (second ordre) | concurrent | xgboost | xgboost | 0.7388 | 1.982 | 1.92 | 0.7141 | 10.7 | 0.2013 | 0.524 | 1.0 | équivalent | 1.0 | équivalent |
| 105 | k plus proches voisins (prix, âge, sexe, issue, mois) | B · gradient boosting quantile | concurrent | knn | boosting | 0.7419 | 1.876 | 1.872 | 0.7355 | 12.6 | 0.1955 | 0.5453 | 1.0 | équivalent | 1.0 | équivalent |
| 106 | Médiane du service | B · gradient boosting quantile | concurrent | mediane | boosting | 0.7481 | 1.888 | 1.882 | 0.7805 | 6.5 | 0.1057 | 0.3288 | 1.0 | équivalent | 1.0 | équivalent |
| 107 | Moyenne du service | B · gradient boosting quantile | concurrent | moyenne | boosting | 0.7481 | 1.888 | 1.882 | 0.7805 | 14.0 | 0.1057 | 0.3288 | 1.0 | équivalent | 1.0 | équivalent |
| 108 | Médiane de la tranche d'âge | B · gradient boosting quantile | concurrent | mediane_age | boosting | 0.7481 | 1.888 | 1.882 | 0.7805 | 13.5 | 0.1057 | 0.3288 | 1.0 | équivalent | 1.0 | équivalent |
| 109 | XGBoost (avec le diagnostic) | B · gradient boosting quantile | concurrent | xgboost | boosting | 0.7561 | 1.985 | 1.93 | 0.736 | 9.8 | 0.1067 | 0.2834 | 1.0 | équivalent | 1.0 | équivalent |
| 110 | ACP itérative (rang faible) | SVR RBF (niveau 2) | svm | acp_iterative | svr_rbf | 0.8707 | 1.936 | 1.94 | 0.972 | 2.4 | 0.0011 | 0.0018 | 0.1254 | équivalent | 0.2088 | équivalent |
| 111 | ACP itérative (rang faible) | SVR linéaire (niveau 1) | svm | acp_iterative | svr_lineaire | 0.8907 | 1.961 | 1.938 | 0.9785 | 0.6 | 0.0014 | 0.1566 | 0.154 | équivalent | 1.0 | équivalent |
| 112 | Médiane de la tranche d'âge | SVR linéaire (niveau 1) | svm | mediane_age | svr_lineaire | 0.9062 | 1.837 | 1.845 | 0.9321 | 1.0 | 0.0012 | 0.1261 | 0.1356 | équivalent | 1.0 | équivalent |
| 113 | Moyenne du service | SVR linéaire (niveau 1) | svm | moyenne | svr_lineaire | 0.9062 | 1.837 | 1.845 | 0.9321 | 0.5 | 0.0012 | 0.1261 | 0.1356 | équivalent | 1.0 | équivalent |
| 114 | Médiane du service | SVR linéaire (niveau 1) | svm | mediane | svr_lineaire | 0.9062 | 1.837 | 1.845 | 0.9321 | 0.5 | 0.0012 | 0.1261 | 0.1356 | équivalent | 1.0 | équivalent |
| 115 | Médiane de la tranche d'âge | SVR RBF (niveau 2) | svm | mediane_age | svr_rbf | 0.933 | 1.894 | 1.879 | 0.9477 | 2.9 | 0.0001 | 0.3 | 0.0125 | moins bon | 1.0 | équivalent |
| 116 | Moyenne du service | SVR RBF (niveau 2) | svm | moyenne | svr_rbf | 0.933 | 1.894 | 1.879 | 0.9477 | 1.4 | 0.0001 | 0.3 | 0.0125 | moins bon | 1.0 | équivalent |
| 117 | Médiane du service | SVR RBF (niveau 2) | svm | mediane | svr_rbf | 0.933 | 1.894 | 1.879 | 0.9477 | 1.5 | 0.0001 | 0.3 | 0.0125 | moins bon | 1.0 | équivalent |
| 118 | Estimée : prix, puis issue, puis médiane | SVR linéaire (niveau 1) | svm | estimee | svr_lineaire | 0.9335 | 1.832 | 1.832 | 0.9335 | 0.9 | 0.0003 |  | 0.0345 | moins bon |  | — référence |
| 119 | SoftImpute (norme nucléaire) | SVR linéaire (niveau 1) | svm | softimpute | svr_lineaire | 0.9374 | 1.829 | 1.854 | 0.9482 | 0.7 | 0.0002 | 0.7796 | 0.0236 | moins bon | 1.0 | équivalent |
| 120 | Régressions enchaînées (ridge, principe de MICE) | SVR linéaire (niveau 1) | svm | regression | svr_lineaire | 0.9403 | 1.841 | 1.849 | 0.934 | 1.0 | 0.0002 | 0.4655 | 0.0236 | moins bon | 1.0 | équivalent |
| 121 | Loi normale multivariée par EM | SVR linéaire (niveau 1) | svm | em | svr_lineaire | 0.941 | 1.847 | 1.851 | 0.9345 | 0.6 | 0.0002 | 0.4068 | 0.0236 | moins bon | 1.0 | équivalent |
| 122 | SoftImpute (norme nucléaire) | SVR RBF (niveau 2) | svm | softimpute | svr_rbf | 0.9429 | 1.865 | 1.878 | 0.9477 | 1.5 | 0.0001 | 0.776 | 0.0125 | moins bon | 1.0 | équivalent |
| 123 | Estimée : prix, puis issue, puis médiane | SVR RBF (niveau 2) | svm | estimee | svr_rbf | 0.9456 | 1.877 | 1.877 | 0.9456 | 2.8 | 0.0001 |  | 0.0125 | moins bon |  | — référence |
| 124 | Régressions enchaînées (ridge, principe de MICE) | SVR RBF (niveau 2) | svm | regression | svr_rbf | 0.9542 | 1.892 | 1.891 | 0.9434 | 2.0 | 0.0 | 0.2299 | 0.0 | moins bon | 1.0 | équivalent |
| 125 | Loi normale multivariée par EM | SVR RBF (niveau 2) | svm | em | svr_rbf | 0.9545 | 1.89 | 1.885 | 0.9438 | 1.8 | 0.0 | 0.2371 | 0.0 | moins bon | 1.0 | équivalent |
| 126 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR linéaire (niveau 1) | svm | knn | svr_lineaire | 0.9551 | 1.862 | 1.841 | 0.9366 | 1.8 | 0.0001 | 0.2836 | 0.0125 | moins bon | 1.0 | équivalent |
| 127 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR RBF (niveau 2) | svm | knn | svr_rbf | 0.9589 | 1.897 | 1.879 | 0.9412 | 3.4 | 0.0 | 0.3782 | 0.0 | moins bon | 1.0 | équivalent |
| 128 | Exclure les séjours sans durée | A · forêt aléatoire quantile | concurrent | exclure | foret | 0.9722 | 2.411 | 1.805 | 0.6523 | 15.7 | 0.0001 | 0.0004 | 0.0125 | moins bon | 0.0468 | moins bon |
| 129 | Exclure les séjours sans durée | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | exclure | lssvr_rbf | 1.0018 | 2.466 | 1.835 | 0.6302 | 0.5 | 0.0 | 0.0 | 0.0 | moins bon | 0.0 | moins bon |
| 130 | Exclure les séjours sans durée | SVR quantile RBF (niveau 3) | svm | exclure | svr_q_rbf | 1.0489 | 2.459 | 1.856 | 0.6559 | 6.5 | 0.0 | 0.0 | 0.0 | moins bon | 0.0 | moins bon |
| 131 | Exclure les séjours sans durée | E · XGBoost quantile (second ordre) | concurrent | exclure | xgboost | 1.0532 | 2.423 | 1.896 | 0.6511 | 8.5 | 0.0 | 0.0 | 0.0 | moins bon | 0.0 | moins bon |
| 132 | Exclure les séjours sans durée | SVR quantile composite (niveau 4, retenu) | svm | exclure | svr_q_composite | 1.0556 | 2.508 | 1.856 | 0.6537 | 13.6 | 0.0 | 0.0 | 0.0 | moins bon | 0.0 | moins bon |
| 133 | Exclure les séjours sans durée | SVR quantile, noyau polynomial (degré 2) | svm | exclure | svr_q_polynomial | 1.0561 | 2.475 | 1.743 | 0.6289 | 10.4 | 0.0 | 0.0 | 0.0 | moins bon | 0.0 | moins bon |
| 134 | Exclure les séjours sans durée | SVR quantile, noyau laplacien | svm | exclure | svr_q_laplacien | 1.0623 | 2.504 | 1.874 | 0.6553 | 5.3 | 0.0 | 0.0 | 0.0 | moins bon | 0.0 | moins bon |
| 135 | Exclure les séjours sans durée | C · perceptron multicouche quantile | concurrent | exclure | mlp | 1.0639 | 2.44 | 1.771 | 0.6255 | 1.4 | 0.0 | 0.0 | 0.0 | moins bon | 0.0 | moins bon |
| 136 | Exclure les séjours sans durée | D · LSTM quantile | concurrent | exclure | lstm | 1.0671 | 2.445 | 1.751 | 0.6196 | 8.8 | 0.0 | 0.0 | 0.0 | moins bon | 0.0 | moins bon |
| 137 | Exclure les séjours sans durée | B · gradient boosting quantile | concurrent | exclure | boosting | 1.075 | 2.45 | 1.819 | 0.6578 | 11.2 | 0.0 | 0.0 | 0.0 | moins bon | 0.0 | moins bon |
| 138 | Hybride : prix, sinon XGBoost | SVR RBF (niveau 2) | svm | hybride | svr_rbf | 1.0824 | 1.948 | 1.901 | 0.9566 | 1.4 | 0.0 | 0.0 | 0.0 | moins bon | 0.0 | moins bon |
| 139 | Hybride : prix, sinon XGBoost | SVR linéaire (niveau 1) | svm | hybride | svr_lineaire | 1.0906 | 1.935 | 1.909 | 0.9754 | 0.8 | 0.0 | 0.0 | 0.0 | moins bon | 0.0 | moins bon |
| 140 | XGBoost (avec le diagnostic) | SVR RBF (niveau 2) | svm | xgboost | svr_rbf | 1.0906 | 1.959 | 1.91 | 0.9619 | 1.4 | 0.0 | 0.0 | 0.0 | moins bon | 0.0 | moins bon |
| 141 | XGBoost (avec le diagnostic) | SVR linéaire (niveau 1) | svm | xgboost | svr_lineaire | 1.0939 | 1.938 | 1.915 | 0.9782 | 0.7 | 0.0 | 0.0 | 0.0 | moins bon | 0.0 | moins bon |
| 142 | Exclure les séjours sans durée | SVR RBF (niveau 2) | svm | exclure | svr_rbf | 1.657 | 2.451 | 1.816 | 0.8781 | 3.4 | 0.0 | 0.0 | 0.0 | moins bon | 0.0 | moins bon |
| 143 | Exclure les séjours sans durée | SVR linéaire (niveau 1) | svm | exclure | svr_lineaire | 1.7268 | 2.538 | 1.722 | 0.8577 | 0.7 | 0.0 | 0.0 | 0.0 | moins bon | 0.0 | moins bon |


Meilleure paire : **SoftImpute (norme nucléaire) × LS-SVR (moindres carrés), noyau RBF, quantiles LOO**.


## Horizon J+7


### P1 · Durées inconnues

173 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Exclure les séjours sans durée | 15/07/2024 | 4 | 7.21 | 40.0 | -0.0 | 2.451 | 0.8337 | 30.7 | 3.006 | 8.0 | 1.0838 | 0.0611 | 0.6721 | 0.054 | équivalent |
| Médiane du service | 15/07/2024 | 4 | 8.62 | 47.9 | -1.6 | 2.705 | 0.9582 | 31.3 | 2.672 | 7.0 | 0.927 | 0.3683 | 1.0 | 0.3194 | équivalent |
| Moyenne du service | 15/07/2024 | 4 | 8.62 | 47.9 | -1.6 | 2.705 | 0.9582 | 31.3 | 2.672 | 10.0 | 0.927 | 0.3683 | 1.0 | 0.3194 | équivalent |
| Médiane de la tranche d'âge | 15/07/2024 | 4 | 8.62 | 47.9 | -1.6 | 2.705 | 0.9582 | 31.3 | 2.672 | 9.6 | 0.927 | 0.3683 | 1.0 | 0.3194 | équivalent |
| Estimée : prix, puis issue, puis médiane (retenu) | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 2.641 | 0.9433 | 32.5 | 2.641 | 8.9 | 0.9433 |  |  |  | — choix retenu |
| k plus proches voisins (prix, âge, sexe, issue, mois) | 15/07/2024 | 4 | 8.48 | 47.1 | -3.2 | 2.681 | 0.9647 | 31.4 | 2.65 | 9.7 | 0.9448 | 0.5304 | 1.0 | 0.4984 | équivalent |
| Régressions enchaînées (ridge, principe de MICE) | 15/07/2024 | 4 | 8.46 | 47.0 | -3.4 | 2.68 | 0.9555 | 32.5 | 2.653 | 8.5 | 0.9428 | 0.5183 | 1.0 | 0.1248 | équivalent |
| Loi normale multivariée par EM | 15/07/2024 | 4 | 8.46 | 47.0 | -3.4 | 2.685 | 0.9579 | 32.6 | 2.654 | 8.8 | 0.9428 | 0.7112 | 1.0 | 0.1047 | équivalent |
| ACP itérative (rang faible) | 15/07/2024 | 4 | 8.68 | 48.2 | -0.9 | 2.809 | 1.0075 | 31.2 | 2.677 | 11.6 | 0.9279 | 0.5397 | 1.0 | 0.2925 | équivalent |
| SoftImpute (norme nucléaire) | 15/07/2024 | 4 | 8.48 | 47.1 | -3.2 | 2.705 | 0.964 | 32.1 | 2.657 | 11.6 | 0.9397 | 0.5149 | 1.0 | 0.1202 | équivalent |
| XGBoost (avec le diagnostic) | 15/07/2024 | 4 | 8.26 | 45.9 | -5.8 | 2.56 | 0.9064 | 33.8 | 2.64 | 37.5 | 0.9619 | 0.1585 | 1.0 | 0.9539 | équivalent |
| Hybride : prix, sinon XGBoost | 15/07/2024 | 4 | 8.26 | 45.9 | -5.8 | 2.554 | 0.8998 | 33.9 | 2.643 | 41.2 | 0.9622 | 0.1572 | 1.0 | 0.9489 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Estimée : prix, puis issue, puis médiane (retenu)).



### P2 · Fenêtre de censure (encore hospitalisé)

173 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 14 jours | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 2.641 | 0.9433 | 32.5 | 2.641 | 11.3 | 0.9433 |  |  |  | identique |
| 30 jours | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 2.641 | 0.9433 | 32.5 | 2.641 | 13.4 | 0.9433 |  |  |  | identique |
| p95 des durées connues (retenu) | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 2.641 | 0.9433 | 32.5 | 2.641 | 11.8 | 0.9433 |  |  |  | — choix retenu |
| 60 jours | 15/07/2024 | 4 | 8.7 | 48.3 | -2.8 | 3.025 | 1.1111 | 22.8 | 2.645 | 11.9 | 0.9435 | 0.357 | 0.357 | 0.3416 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (p95 des durées connues (retenu)).



### P3 · Convention du nombre de jours

173 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Attendue (nuit incertaine = 1 − p) (retenu) | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 2.641 | 0.9433 | 32.5 | 2.641 | 11.7 | 0.9433 |  |  |  | — choix retenu |
| Tout inclusif (borne basse) | 15/07/2024 | 4 | 7.94 | 44.1 | -6.8 | 2.542 | 0.9002 | 33.3 | 2.659 | 11.5 | 0.9916 | 0.1504 | 0.3008 | 0.7733 | équivalent |
| Tout en nuits (borne haute) | 15/07/2024 | 4 | 9.02 | 50.1 | 2.4 | 2.824 | 1.023 | 30.1 | 2.685 | 9.9 | 0.92 | 0.5187 | 0.5187 | 0.4591 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Attendue (nuit incertaine = 1 − p) (retenu)).



### P4 · Patients « Ancien » reportés

173 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Garder toutes les lignes (retenu) | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 2.641 | 0.9433 | 32.5 | 2.641 | 13.3 | 0.9433 |  |  |  | — choix retenu |
| Fusionner les reports confirmés | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 2.641 | 0.9433 | 32.5 | 2.641 | 12.8 | 0.9433 |  |  |  | identique |


Aucune variante ne fait significativement mieux que le choix retenu (Garder toutes les lignes (retenu)).



### P5 · Période exploitable

173 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Durées connues ≥ 80 % | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 2.641 | 0.9433 | 32.5 | 2.641 | 10.9 | 0.9433 |  |  |  | identique |
| Durées connues ≥ 90 % (retenu) | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 2.641 | 0.9433 | 32.5 | 2.641 | 13.9 | 0.9433 |  |  |  | — choix retenu |
| Durées connues ≥ 95 % | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 2.641 | 0.9433 | 32.5 | 2.641 | 11.7 | 0.9433 |  |  |  | identique |
| ≥ 90 %, sans rodage au début (premier mois = début réel du registre) | 01/07/2024 | 4 | 8.41 | 46.7 | -3.2 | 2.659 | 0.9562 | 32.1 | 2.659 | 11.3 | 0.9562 | 0.0991 | 0.0991 | 0.3649 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Durées connues ≥ 90 % (retenu)).



### P6 · Fin de série (délai d'inscription)

170 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Aucune coupe | 15/07/2024 | 0 | 8.44 | 46.9 | -3.4 | 2.583 | 0.9277 | 33.3 | 2.583 | 12.5 | 0.9277 |  |  |  | identique |
| 7 derniers jours retirés | 15/07/2024 | 7 | 8.49 | 47.2 | -3.6 | 2.583 | 0.9277 | 33.3 | 2.583 | 11.1 | 0.9277 |  |  |  | identique |
| p95 du délai d'inscription (retenu) | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 2.583 | 0.9277 | 33.3 | 2.583 | 12.0 | 0.9277 |  |  |  | — choix retenu |


Aucune variante ne fait significativement mieux que le choix retenu (p95 du délai d'inscription (retenu)).



### P7 · Trous de saisie (≥ 4 jours sans admission)

173 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Gardés tels quels (retenu) | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 2.641 | 0.9433 | 32.5 | 2.641 | 14.0 | 0.9433 |  |  |  | — choix retenu |
| Lignes d'apprentissage qui les touchent exclues | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 2.635 | 0.9341 | 32.7 | 2.635 | 9.4 | 0.9341 | 0.264 | 0.264 | 0.7433 | équivalent |


Aucune variante ne fait significativement mieux que le choix retenu (Gardés tels quels (retenu)).



### P8 · Méthode de comptage des présents

173 jours évalués.

| variante | début série | jours coupés en fin | présents moyens | TOM % | écart Little % | MAE propre | pinball τ=0.8 propre | gain / persistance % | MAE retenue | temps (s) | pinball τ=0.8 retenue | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Recensement de minuit (nuits passées) (retenu) | 15/07/2024 | 4 | 8.47 | 47.0 | -3.3 | 2.641 | 0.9433 | 32.5 | 2.641 | 11.2 | 0.9433 |  |  |  | — choix retenu |
| Présence dans la journée (jour de sortie compris) | 15/07/2024 | 4 | 11.17 | 62.0 | -2.6 | 3.154 | 1.058 | 27.8 | 3.324 | 11.6 | 1.1743 | 0.0308 | 0.0308 | 0.0255 | moins bon |


Aucune variante ne fait significativement mieux que le choix retenu (Recensement de minuit (nuits passées) (retenu)).



### P1 × modèles (J+7) : chaque méthode des durées inconnues avec chaque modèle

173 jours évalués ; tri par perte pinball τ=0.8 contre la série retenue.

| variante | imputation | modèle | famille | cle_imputation | cle_modele | pinball τ=0.8 retenue | MAE retenue | MAE propre | pinball τ=0.8 propre | temps (s) | DM p vs paire retenue | DM p vs imputation retenue, même modèle | p Holm vs paire retenue | vs paire retenue | p Holm vs imputation retenue, même modèle | vs imputation retenue, même modèle |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Médiane de la tranche d'âge | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | mediane_age | lssvr_rbf | 0.9218 | 2.736 | 2.761 | 0.9536 | 0.3 | 0.603 | 0.7158 | 1.0 | équivalent | 1.0 | équivalent |
| 1 | Médiane du service | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | mediane | lssvr_rbf | 0.9218 | 2.736 | 2.761 | 0.9536 | 0.6 | 0.603 | 0.7158 | 1.0 | équivalent | 1.0 | équivalent |
| 2 | Moyenne du service | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | moyenne | lssvr_rbf | 0.9218 | 2.736 | 2.761 | 0.9536 | 0.4 | 0.603 | 0.7158 | 1.0 | équivalent | 1.0 | équivalent |
| 3 | Médiane du service | SVR quantile composite (niveau 4, retenu) | svm | mediane | svr_q_composite | 0.927 | 2.672 | 2.705 | 0.9582 | 11.3 | 0.3683 | 0.3683 | 1.0 | équivalent | 1.0 | équivalent |
| 4 | Médiane de la tranche d'âge | SVR quantile composite (niveau 4, retenu) | svm | mediane_age | svr_q_composite | 0.927 | 2.672 | 2.705 | 0.9582 | 10.4 | 0.3683 | 0.3683 | 1.0 | équivalent | 1.0 | équivalent |
| 5 | Moyenne du service | SVR quantile composite (niveau 4, retenu) | svm | moyenne | svr_q_composite | 0.927 | 2.672 | 2.705 | 0.9582 | 9.0 | 0.3683 | 0.3683 | 1.0 | équivalent | 1.0 | équivalent |
| 6 | ACP itérative (rang faible) | SVR quantile composite (niveau 4, retenu) | svm | acp_iterative | svr_q_composite | 0.9279 | 2.677 | 2.809 | 1.0075 | 5.5 | 0.5397 | 0.5397 | 1.0 | équivalent | 1.0 | équivalent |
| 7 | Estimée : prix, puis issue, puis médiane | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | estimee | lssvr_rbf | 0.9287 | 2.74 | 2.74 | 0.9287 | 0.2 | 0.5803 |  | 1.0 | équivalent |  | — référence |
| 8 | Loi normale multivariée par EM | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | em | lssvr_rbf | 0.9313 | 2.736 | 2.773 | 0.9475 | 0.5 | 0.6382 | 0.4007 | 1.0 | équivalent | 1.0 | équivalent |
| 9 | Médiane du service | SVR quantile RBF (niveau 3) | svm | mediane | svr_q_rbf | 0.9318 | 2.704 | 2.735 | 0.9622 | 2.6 | 0.7439 | 0.5783 | 1.0 | équivalent | 1.0 | équivalent |
| 10 | Médiane de la tranche d'âge | SVR quantile RBF (niveau 3) | svm | mediane_age | svr_q_rbf | 0.9318 | 2.704 | 2.735 | 0.9622 | 1.7 | 0.7439 | 0.5783 | 1.0 | équivalent | 1.0 | équivalent |
| 11 | Moyenne du service | SVR quantile RBF (niveau 3) | svm | moyenne | svr_q_rbf | 0.9318 | 2.704 | 2.735 | 0.9622 | 1.9 | 0.7439 | 0.5783 | 1.0 | équivalent | 1.0 | équivalent |
| 12 | Régressions enchaînées (ridge, principe de MICE) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | regression | lssvr_rbf | 0.9319 | 2.745 | 2.778 | 0.9447 | 0.3 | 0.6626 | 0.288 | 1.0 | équivalent | 1.0 | équivalent |
| 13 | ACP itérative (rang faible) | SVR quantile RBF (niveau 3) | svm | acp_iterative | svr_q_rbf | 0.9321 | 2.688 | 2.828 | 1.0059 | 1.7 | 0.7736 | 0.6868 | 1.0 | équivalent | 1.0 | équivalent |
| 14 | k plus proches voisins (prix, âge, sexe, issue, mois) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | knn | lssvr_rbf | 0.9325 | 2.753 | 2.769 | 0.9534 | 0.6 | 0.7098 | 0.6668 | 1.0 | équivalent | 1.0 | équivalent |
| 15 | SoftImpute (norme nucléaire) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | softimpute | lssvr_rbf | 0.9341 | 2.733 | 2.785 | 0.9609 | 0.2 | 0.7482 | 0.5092 | 1.0 | équivalent | 1.0 | équivalent |
| 16 | SoftImpute (norme nucléaire) | SVR quantile RBF (niveau 3) | svm | softimpute | svr_q_rbf | 0.9364 | 2.699 | 2.745 | 0.9607 | 1.5 | 0.7939 | 0.5139 | 1.0 | équivalent | 1.0 | équivalent |
| 17 | ACP itérative (rang faible) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | acp_iterative | lssvr_rbf | 0.9373 | 2.721 | 2.819 | 0.9875 | 0.2 | 0.8878 | 0.6814 | 1.0 | équivalent | 1.0 | équivalent |
| 18 | Estimée : prix, puis issue, puis médiane | SVR quantile RBF (niveau 3) | svm | estimee | svr_q_rbf | 0.938 | 2.689 | 2.689 | 0.938 | 1.8 | 0.8388 |  | 1.0 | équivalent |  | — référence |
| 19 | Médiane du service | SVR quantile, noyau laplacien | svm | mediane | svr_q_laplacien | 0.9386 | 2.704 | 2.735 | 0.9692 | 4.5 | 0.8929 | 0.4798 | 1.0 | équivalent | 1.0 | équivalent |
| 20 | Moyenne du service | SVR quantile, noyau laplacien | svm | moyenne | svr_q_laplacien | 0.9386 | 2.704 | 2.735 | 0.9692 | 4.6 | 0.8929 | 0.4798 | 1.0 | équivalent | 1.0 | équivalent |
| 21 | Médiane de la tranche d'âge | SVR quantile, noyau laplacien | svm | mediane_age | svr_q_laplacien | 0.9386 | 2.704 | 2.735 | 0.9692 | 2.5 | 0.8929 | 0.4798 | 1.0 | équivalent | 1.0 | équivalent |
| 22 | ACP itérative (rang faible) | SVR quantile, noyau laplacien | svm | acp_iterative | svr_q_laplacien | 0.9391 | 2.692 | 2.838 | 1.0134 | 1.5 | 0.9127 | 0.634 | 1.0 | équivalent | 1.0 | équivalent |
| 23 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile RBF (niveau 3) | svm | regression | svr_q_rbf | 0.9396 | 2.691 | 2.711 | 0.9523 | 1.4 | 0.8802 | 0.458 | 1.0 | équivalent | 1.0 | équivalent |
| 24 | SoftImpute (norme nucléaire) | SVR quantile composite (niveau 4, retenu) | svm | softimpute | svr_q_composite | 0.9397 | 2.657 | 2.705 | 0.964 | 5.3 | 0.5149 | 0.5149 | 1.0 | équivalent | 1.0 | équivalent |
| 25 | XGBoost (avec le diagnostic) | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | xgboost | lssvr_rbf | 0.9404 | 2.753 | 2.678 | 0.8946 | 0.2 | 0.886 | 0.3677 | 1.0 | équivalent | 1.0 | équivalent |
| 26 | Loi normale multivariée par EM | SVR quantile RBF (niveau 3) | svm | em | svr_q_rbf | 0.9407 | 2.69 | 2.715 | 0.9511 | 1.6 | 0.9185 | 0.2104 | 1.0 | équivalent | 1.0 | équivalent |
| 27 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile RBF (niveau 3) | svm | knn | svr_q_rbf | 0.9415 | 2.692 | 2.718 | 0.9632 | 1.8 | 0.944 | 0.363 | 1.0 | équivalent | 1.0 | équivalent |
| 28 | SoftImpute (norme nucléaire) | SVR quantile, noyau laplacien | svm | softimpute | svr_q_laplacien | 0.9422 | 2.692 | 2.739 | 0.9664 | 1.1 | 0.9682 | 0.038 | 1.0 | équivalent | 1.0 | équivalent |
| 29 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile composite (niveau 4, retenu) | svm | regression | svr_q_composite | 0.9428 | 2.653 | 2.68 | 0.9555 | 9.6 | 0.5183 | 0.5183 | 1.0 | équivalent | 1.0 | équivalent |
| 30 | Loi normale multivariée par EM | SVR quantile composite (niveau 4, retenu) | svm | em | svr_q_composite | 0.9428 | 2.654 | 2.685 | 0.9579 | 6.7 | 0.7112 | 0.7112 | 1.0 | équivalent | 1.0 | équivalent |
| 31 | Hybride : prix, sinon XGBoost | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | hybride | lssvr_rbf | 0.9432 | 2.755 | 2.665 | 0.8909 | 0.2 | 0.9973 | 0.2967 | 1.0 | équivalent | 1.0 | équivalent |
| 32 | Estimée : prix, puis issue, puis médiane | SVR quantile composite (niveau 4, retenu) | svm | estimee | svr_q_composite | 0.9433 | 2.641 | 2.641 | 0.9433 | 9.3 |  |  |  | — référence |  | — référence |
| 33 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile composite (niveau 4, retenu) | svm | knn | svr_q_composite | 0.9448 | 2.65 | 2.681 | 0.9647 | 8.6 | 0.5304 | 0.5304 | 1.0 | équivalent | 1.0 | équivalent |
| 34 | Estimée : prix, puis issue, puis médiane | SVR quantile, noyau laplacien | svm | estimee | svr_q_laplacien | 0.9457 | 2.687 | 2.687 | 0.9457 | 2.4 | 0.9271 |  | 1.0 | équivalent |  | — référence |
| 35 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile, noyau laplacien | svm | regression | svr_q_laplacien | 0.9462 | 2.687 | 2.71 | 0.959 | 1.7 | 0.9062 | 0.8068 | 1.0 | équivalent | 1.0 | équivalent |
| 36 | Loi normale multivariée par EM | SVR quantile, noyau laplacien | svm | em | svr_q_laplacien | 0.9474 | 2.686 | 2.713 | 0.9575 | 2.0 | 0.8733 | 0.4101 | 1.0 | équivalent | 1.0 | équivalent |
| 37 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile, noyau laplacien | svm | knn | svr_q_laplacien | 0.9485 | 2.687 | 2.715 | 0.9681 | 2.8 | 0.8343 | 0.5068 | 1.0 | équivalent | 1.0 | équivalent |
| 38 | XGBoost (avec le diagnostic) | SVR quantile RBF (niveau 3) | svm | xgboost | svr_q_rbf | 0.9505 | 2.679 | 2.596 | 0.8987 | 1.3 | 0.6119 | 0.6503 | 1.0 | équivalent | 1.0 | équivalent |
| 39 | Hybride : prix, sinon XGBoost | SVR quantile RBF (niveau 3) | svm | hybride | svr_q_rbf | 0.951 | 2.679 | 2.59 | 0.8921 | 1.4 | 0.5912 | 0.6399 | 1.0 | équivalent | 1.0 | équivalent |
| 40 | XGBoost (avec le diagnostic) | SVR quantile, noyau laplacien | svm | xgboost | svr_q_laplacien | 0.9548 | 2.669 | 2.59 | 0.902 | 1.6 | 0.4233 | 0.7472 | 1.0 | équivalent | 1.0 | équivalent |
| 41 | Hybride : prix, sinon XGBoost | SVR quantile, noyau laplacien | svm | hybride | svr_q_laplacien | 0.9549 | 2.671 | 2.585 | 0.8953 | 1.6 | 0.4142 | 0.743 | 1.0 | équivalent | 1.0 | équivalent |
| 42 | Médiane du service | A · forêt aléatoire quantile | concurrent | mediane | foret | 0.956 | 2.751 | 2.773 | 0.9876 | 16.7 | 0.6873 | 0.2116 | 1.0 | équivalent | 1.0 | équivalent |
| 43 | Moyenne du service | A · forêt aléatoire quantile | concurrent | moyenne | foret | 0.956 | 2.751 | 2.773 | 0.9876 | 14.6 | 0.6873 | 0.2116 | 1.0 | équivalent | 1.0 | équivalent |
| 44 | Médiane de la tranche d'âge | A · forêt aléatoire quantile | concurrent | mediane_age | foret | 0.956 | 2.751 | 2.773 | 0.9876 | 16.1 | 0.6873 | 0.2116 | 1.0 | équivalent | 1.0 | équivalent |
| 45 | ACP itérative (rang faible) | A · forêt aléatoire quantile | concurrent | acp_iterative | foret | 0.9565 | 2.693 | 2.786 | 1.0074 | 15.2 | 0.7592 | 0.4948 | 1.0 | équivalent | 1.0 | équivalent |
| 46 | SoftImpute (norme nucléaire) | A · forêt aléatoire quantile | concurrent | softimpute | foret | 0.9592 | 2.757 | 2.809 | 0.9839 | 11.3 | 0.6091 | 0.3056 | 1.0 | équivalent | 1.0 | équivalent |
| 47 | XGBoost (avec le diagnostic) | SVR quantile composite (niveau 4, retenu) | svm | xgboost | svr_q_composite | 0.9619 | 2.64 | 2.56 | 0.9064 | 5.7 | 0.1585 | 0.1585 | 1.0 | équivalent | 1.0 | équivalent |
| 48 | Hybride : prix, sinon XGBoost | SVR quantile composite (niveau 4, retenu) | svm | hybride | svr_q_composite | 0.9622 | 2.643 | 2.554 | 0.8998 | 8.8 | 0.1572 | 0.1572 | 1.0 | équivalent | 1.0 | équivalent |
| 49 | ACP itérative (rang faible) | SVR quantile, noyau polynomial (degré 2) | svm | acp_iterative | svr_q_polynomial | 0.9681 | 2.778 | 2.912 | 1.0409 | 4.0 | 0.4118 | 0.3773 | 1.0 | équivalent | 1.0 | équivalent |
| 50 | k plus proches voisins (prix, âge, sexe, issue, mois) | A · forêt aléatoire quantile | concurrent | knn | foret | 0.9714 | 2.752 | 2.763 | 0.9888 | 14.9 | 0.338 | 0.6003 | 1.0 | équivalent | 1.0 | équivalent |
| 51 | Loi normale multivariée par EM | A · forêt aléatoire quantile | concurrent | em | foret | 0.9781 | 2.793 | 2.833 | 0.9955 | 14.5 | 0.2585 | 0.7741 | 1.0 | équivalent | 1.0 | équivalent |
| 52 | Médiane du service | D · LSTM quantile | concurrent | mediane | lstm | 0.9789 | 2.841 | 2.875 | 1.0011 | 15.5 | 0.4411 | 0.3538 | 1.0 | équivalent | 1.0 | équivalent |
| 53 | Moyenne du service | D · LSTM quantile | concurrent | moyenne | lstm | 0.9789 | 2.841 | 2.875 | 1.0011 | 13.3 | 0.4411 | 0.3538 | 1.0 | équivalent | 1.0 | équivalent |
| 54 | Médiane de la tranche d'âge | D · LSTM quantile | concurrent | mediane_age | lstm | 0.9789 | 2.841 | 2.875 | 1.0011 | 10.3 | 0.4411 | 0.3538 | 1.0 | équivalent | 1.0 | équivalent |
| 55 | Médiane du service | SVR quantile, noyau polynomial (degré 2) | svm | mediane | svr_q_polynomial | 0.9805 | 2.775 | 2.797 | 1.0114 | 3.6 | 0.2371 | 0.168 | 1.0 | équivalent | 1.0 | équivalent |
| 56 | Moyenne du service | SVR quantile, noyau polynomial (degré 2) | svm | moyenne | svr_q_polynomial | 0.9805 | 2.775 | 2.797 | 1.0114 | 6.8 | 0.2371 | 0.168 | 1.0 | équivalent | 1.0 | équivalent |
| 57 | Médiane de la tranche d'âge | SVR quantile, noyau polynomial (degré 2) | svm | mediane_age | svr_q_polynomial | 0.9805 | 2.775 | 2.797 | 1.0114 | 5.4 | 0.2371 | 0.168 | 1.0 | équivalent | 1.0 | équivalent |
| 58 | Estimée : prix, puis issue, puis médiane | A · forêt aléatoire quantile | concurrent | estimee | foret | 0.982 | 2.722 | 2.722 | 0.982 | 16.4 | 0.1955 |  | 1.0 | équivalent |  | — référence |
| 59 | ACP itérative (rang faible) | E · XGBoost quantile (second ordre) | concurrent | acp_iterative | xgboost | 0.9834 | 2.747 | 2.851 | 1.0703 | 7.5 | 0.1192 | 0.631 | 1.0 | équivalent | 1.0 | équivalent |
| 60 | Médiane du service | E · XGBoost quantile (second ordre) | concurrent | mediane | xgboost | 0.9853 | 2.765 | 2.801 | 1.0223 | 13.4 | 0.1671 | 0.3826 | 1.0 | équivalent | 1.0 | équivalent |
| 61 | Moyenne du service | E · XGBoost quantile (second ordre) | concurrent | moyenne | xgboost | 0.9853 | 2.765 | 2.801 | 1.0223 | 13.4 | 0.1671 | 0.3826 | 1.0 | équivalent | 1.0 | équivalent |
| 62 | Médiane de la tranche d'âge | E · XGBoost quantile (second ordre) | concurrent | mediane_age | xgboost | 0.9853 | 2.765 | 2.801 | 1.0223 | 11.4 | 0.1671 | 0.3826 | 1.0 | équivalent | 1.0 | équivalent |
| 63 | ACP itérative (rang faible) | B · gradient boosting quantile | concurrent | acp_iterative | boosting | 0.9879 | 2.795 | 2.885 | 1.0784 | 8.4 | 0.3077 | 0.4169 | 1.0 | équivalent | 1.0 | équivalent |
| 64 | Régressions enchaînées (ridge, principe de MICE) | E · XGBoost quantile (second ordre) | concurrent | regression | xgboost | 0.9879 | 2.831 | 2.861 | 1.0006 | 11.3 | 0.1464 | 0.1141 | 1.0 | équivalent | 1.0 | équivalent |
| 65 | Régressions enchaînées (ridge, principe de MICE) | A · forêt aléatoire quantile | concurrent | regression | foret | 0.9882 | 2.802 | 2.841 | 1.0009 | 11.8 | 0.1449 | 0.6449 | 1.0 | équivalent | 1.0 | équivalent |
| 66 | k plus proches voisins (prix, âge, sexe, issue, mois) | E · XGBoost quantile (second ordre) | concurrent | knn | xgboost | 0.9888 | 2.804 | 2.829 | 1.0117 | 11.4 | 0.2527 | 0.4744 | 1.0 | équivalent | 1.0 | équivalent |
| 67 | XGBoost (avec le diagnostic) | A · forêt aléatoire quantile | concurrent | xgboost | foret | 0.9931 | 2.749 | 2.675 | 0.9279 | 11.4 | 0.1103 | 0.6473 | 1.0 | équivalent | 1.0 | équivalent |
| 68 | SoftImpute (norme nucléaire) | E · XGBoost quantile (second ordre) | concurrent | softimpute | xgboost | 0.9934 | 2.798 | 2.847 | 1.0228 | 7.5 | 0.1407 | 0.5574 | 1.0 | équivalent | 1.0 | équivalent |
| 69 | Hybride : prix, sinon XGBoost | A · forêt aléatoire quantile | concurrent | hybride | foret | 0.9958 | 2.773 | 2.67 | 0.9322 | 11.9 | 0.1433 | 0.6106 | 1.0 | équivalent | 1.0 | équivalent |
| 70 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR quantile, noyau polynomial (degré 2) | svm | knn | svr_q_polynomial | 0.9967 | 2.79 | 2.798 | 1.0168 | 5.6 | 0.082 | 0.4588 | 1.0 | équivalent | 1.0 | équivalent |
| 71 | SoftImpute (norme nucléaire) | SVR quantile, noyau polynomial (degré 2) | svm | softimpute | svr_q_polynomial | 1.0002 | 2.775 | 2.808 | 1.0252 | 3.0 | 0.0855 | 0.8422 | 1.0 | équivalent | 1.0 | équivalent |
| 72 | Estimée : prix, puis issue, puis médiane | E · XGBoost quantile (second ordre) | concurrent | estimee | xgboost | 1.0004 | 2.813 | 2.813 | 1.0004 | 10.9 | 0.0769 |  | 1.0 | équivalent |  | — référence |
| 73 | Estimée : prix, puis issue, puis médiane | SVR quantile, noyau polynomial (degré 2) | svm | estimee | svr_q_polynomial | 1.0009 | 2.766 | 2.766 | 1.0009 | 4.1 | 0.0615 |  | 1.0 | équivalent |  | — référence |
| 74 | Régressions enchaînées (ridge, principe de MICE) | SVR quantile, noyau polynomial (degré 2) | svm | regression | svr_q_polynomial | 1.0014 | 2.777 | 2.788 | 1.0142 | 3.3 | 0.0593 | 0.8853 | 1.0 | équivalent | 1.0 | équivalent |
| 75 | Estimée : prix, puis issue, puis médiane | C · perceptron multicouche quantile | concurrent | estimee | mlp | 1.0025 | 2.801 | 2.801 | 1.0025 | 0.9 | 0.0924 |  | 1.0 | équivalent |  | — référence |
| 76 | Loi normale multivariée par EM | SVR quantile, noyau polynomial (degré 2) | svm | em | svr_q_polynomial | 1.003 | 2.78 | 2.796 | 1.0199 | 3.8 | 0.0517 | 0.6394 | 1.0 | équivalent | 1.0 | équivalent |
| 77 | Estimée : prix, puis issue, puis médiane | D · LSTM quantile | concurrent | estimee | lstm | 1.0069 | 2.914 | 2.914 | 1.0069 | 9.4 | 0.0489 |  | 1.0 | équivalent |  | — référence |
| 78 | Loi normale multivariée par EM | E · XGBoost quantile (second ordre) | concurrent | em | xgboost | 1.0112 | 2.806 | 2.849 | 1.0279 | 10.0 | 0.0475 | 0.0884 | 1.0 | équivalent | 1.0 | équivalent |
| 79 | Médiane du service | B · gradient boosting quantile | concurrent | mediane | boosting | 1.0123 | 2.787 | 2.834 | 1.0484 | 9.5 | 0.0793 | 0.6373 | 1.0 | équivalent | 1.0 | équivalent |
| 80 | Moyenne du service | B · gradient boosting quantile | concurrent | moyenne | boosting | 1.0123 | 2.787 | 2.834 | 1.0484 | 10.9 | 0.0793 | 0.6373 | 1.0 | équivalent | 1.0 | équivalent |
| 81 | Médiane de la tranche d'âge | B · gradient boosting quantile | concurrent | mediane_age | boosting | 1.0123 | 2.787 | 2.834 | 1.0484 | 9.3 | 0.0793 | 0.6373 | 1.0 | équivalent | 1.0 | équivalent |
| 82 | SoftImpute (norme nucléaire) | B · gradient boosting quantile | concurrent | softimpute | boosting | 1.0132 | 2.796 | 2.84 | 1.0433 | 6.3 | 0.1478 | 0.5572 | 1.0 | équivalent | 1.0 | équivalent |
| 83 | XGBoost (avec le diagnostic) | SVR quantile, noyau polynomial (degré 2) | svm | xgboost | svr_q_polynomial | 1.0133 | 2.778 | 2.675 | 0.9451 | 3.3 | 0.0577 | 0.5548 | 1.0 | équivalent | 1.0 | équivalent |
| 84 | Médiane de la tranche d'âge | C · perceptron multicouche quantile | concurrent | mediane_age | mlp | 1.0156 | 2.769 | 2.825 | 1.0411 | 1.0 | 0.1141 | 0.594 | 1.0 | équivalent | 1.0 | équivalent |
| 85 | Médiane du service | C · perceptron multicouche quantile | concurrent | mediane | mlp | 1.0156 | 2.769 | 2.825 | 1.0411 | 0.9 | 0.1141 | 0.594 | 1.0 | équivalent | 1.0 | équivalent |
| 86 | Moyenne du service | C · perceptron multicouche quantile | concurrent | moyenne | mlp | 1.0156 | 2.769 | 2.825 | 1.0411 | 1.9 | 0.1141 | 0.594 | 1.0 | équivalent | 1.0 | équivalent |
| 87 | Hybride : prix, sinon XGBoost | SVR quantile, noyau polynomial (degré 2) | svm | hybride | svr_q_polynomial | 1.0161 | 2.782 | 2.676 | 0.9405 | 4.1 | 0.0513 | 0.4631 | 1.0 | équivalent | 1.0 | équivalent |
| 88 | ACP itérative (rang faible) | D · LSTM quantile | concurrent | acp_iterative | lstm | 1.017 | 2.916 | 3.059 | 1.0786 | 8.1 | 0.0596 | 0.7171 | 1.0 | équivalent | 1.0 | équivalent |
| 89 | XGBoost (avec le diagnostic) | B · gradient boosting quantile | concurrent | xgboost | boosting | 1.0173 | 2.89 | 2.778 | 0.9446 | 6.2 | 0.1912 | 0.779 | 1.0 | équivalent | 1.0 | équivalent |
| 90 | Régressions enchaînées (ridge, principe de MICE) | C · perceptron multicouche quantile | concurrent | regression | mlp | 1.019 | 2.81 | 2.843 | 1.03 | 0.8 | 0.0366 | 0.0024 | 1.0 | équivalent | 0.2832 | équivalent |
| 91 | SoftImpute (norme nucléaire) | D · LSTM quantile | concurrent | softimpute | lstm | 1.021 | 2.9 | 2.948 | 1.0416 | 7.6 | 0.046 | 0.3173 | 1.0 | équivalent | 1.0 | équivalent |
| 92 | Régressions enchaînées (ridge, principe de MICE) | D · LSTM quantile | concurrent | regression | lstm | 1.0211 | 2.938 | 2.98 | 1.0332 | 8.3 | 0.0113 | 0.2115 | 1.0 | équivalent | 1.0 | équivalent |
| 93 | Régressions enchaînées (ridge, principe de MICE) | B · gradient boosting quantile | concurrent | regression | boosting | 1.0212 | 2.839 | 2.872 | 1.0339 | 8.9 | 0.1099 | 0.866 | 1.0 | équivalent | 1.0 | équivalent |
| 94 | k plus proches voisins (prix, âge, sexe, issue, mois) | D · LSTM quantile | concurrent | knn | lstm | 1.0237 | 2.914 | 2.948 | 1.0468 | 6.9 | 0.0132 | 0.2216 | 1.0 | équivalent | 1.0 | équivalent |
| 95 | Estimée : prix, puis issue, puis médiane | B · gradient boosting quantile | concurrent | estimee | boosting | 1.026 | 2.877 | 2.877 | 1.026 | 9.7 | 0.0888 |  | 1.0 | équivalent |  | — référence |
| 96 | SoftImpute (norme nucléaire) | C · perceptron multicouche quantile | concurrent | softimpute | mlp | 1.0261 | 2.777 | 2.843 | 1.0444 | 0.8 | 0.0468 | 0.1041 | 1.0 | équivalent | 1.0 | équivalent |
| 97 | Hybride : prix, sinon XGBoost | B · gradient boosting quantile | concurrent | hybride | boosting | 1.0273 | 2.934 | 2.806 | 0.9489 | 6.7 | 0.1379 | 0.961 | 1.0 | équivalent | 1.0 | équivalent |
| 98 | ACP itérative (rang faible) | C · perceptron multicouche quantile | concurrent | acp_iterative | mlp | 1.0277 | 2.771 | 2.92 | 1.0611 | 1.1 | 0.1147 | 0.3829 | 1.0 | équivalent | 1.0 | équivalent |
| 99 | XGBoost (avec le diagnostic) | D · LSTM quantile | concurrent | xgboost | lstm | 1.0281 | 2.94 | 2.868 | 0.9809 | 7.0 | 0.0183 | 0.358 | 1.0 | équivalent | 1.0 | équivalent |
| 100 | k plus proches voisins (prix, âge, sexe, issue, mois) | B · gradient boosting quantile | concurrent | knn | boosting | 1.0322 | 2.881 | 2.926 | 1.0543 | 7.8 | 0.1323 | 0.8652 | 1.0 | équivalent | 1.0 | équivalent |
| 101 | Hybride : prix, sinon XGBoost | E · XGBoost quantile (second ordre) | concurrent | hybride | xgboost | 1.0331 | 2.835 | 2.732 | 0.9433 | 8.2 | 0.109 | 0.258 | 1.0 | équivalent | 1.0 | équivalent |
| 102 | XGBoost (avec le diagnostic) | E · XGBoost quantile (second ordre) | concurrent | xgboost | xgboost | 1.0332 | 2.835 | 2.761 | 0.9535 | 7.7 | 0.1227 | 0.2777 | 1.0 | équivalent | 1.0 | équivalent |
| 103 | XGBoost (avec le diagnostic) | C · perceptron multicouche quantile | concurrent | xgboost | mlp | 1.0338 | 2.745 | 2.664 | 0.9902 | 0.8 | 0.0089 | 0.0691 | 1.0 | équivalent | 1.0 | équivalent |
| 104 | Hybride : prix, sinon XGBoost | D · LSTM quantile | concurrent | hybride | lstm | 1.0365 | 2.951 | 2.858 | 0.9835 | 8.8 | 0.0483 | 0.3266 | 1.0 | équivalent | 1.0 | équivalent |
| 105 | k plus proches voisins (prix, âge, sexe, issue, mois) | C · perceptron multicouche quantile | concurrent | knn | mlp | 1.0373 | 2.799 | 2.862 | 1.0622 | 0.8 | 0.0136 | 0.0092 | 1.0 | équivalent | 1.0 | équivalent |
| 106 | Loi normale multivariée par EM | C · perceptron multicouche quantile | concurrent | em | mlp | 1.0389 | 2.806 | 2.844 | 1.0563 | 0.8 | 0.0126 | 0.0 | 1.0 | équivalent | 0.0 | moins bon |
| 107 | Loi normale multivariée par EM | D · LSTM quantile | concurrent | em | lstm | 1.0426 | 2.956 | 3.005 | 1.0551 | 7.3 | 0.0103 | 0.0569 | 1.0 | équivalent | 1.0 | équivalent |
| 108 | Hybride : prix, sinon XGBoost | C · perceptron multicouche quantile | concurrent | hybride | mlp | 1.043 | 2.773 | 2.646 | 0.9916 | 0.9 | 0.0092 | 0.0435 | 1.0 | équivalent | 1.0 | équivalent |
| 109 | Loi normale multivariée par EM | B · gradient boosting quantile | concurrent | em | boosting | 1.046 | 2.901 | 2.921 | 1.0633 | 8.7 | 0.0725 | 0.562 | 1.0 | équivalent | 1.0 | équivalent |
| 110 | Exclure les séjours sans durée | SVR quantile, noyau laplacien | svm | exclure | svr_q_laplacien | 1.065 | 3.007 | 2.454 | 0.8197 | 2.9 | 0.095 | 0.1976 | 1.0 | équivalent | 1.0 | équivalent |
| 111 | Exclure les séjours sans durée | SVR quantile RBF (niveau 3) | svm | exclure | svr_q_rbf | 1.0745 | 3.023 | 2.462 | 0.827 | 2.7 | 0.0757 | 0.1463 | 1.0 | équivalent | 1.0 | équivalent |
| 112 | Exclure les séjours sans durée | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | svm | exclure | lssvr_rbf | 1.0806 | 3.099 | 2.52 | 0.8549 | 0.5 | 0.0343 | 0.0674 | 1.0 | équivalent | 1.0 | équivalent |
| 113 | Exclure les séjours sans durée | SVR quantile composite (niveau 4, retenu) | svm | exclure | svr_q_composite | 1.0838 | 3.006 | 2.451 | 0.8337 | 9.8 | 0.0611 | 0.0611 | 1.0 | équivalent | 1.0 | équivalent |
| 114 | Exclure les séjours sans durée | A · forêt aléatoire quantile | concurrent | exclure | foret | 1.1069 | 3.076 | 2.56 | 0.8476 | 14.2 | 0.0336 | 0.1386 | 1.0 | équivalent | 1.0 | équivalent |
| 115 | Exclure les séjours sans durée | D · LSTM quantile | concurrent | exclure | lstm | 1.1224 | 3.153 | 2.564 | 0.8773 | 10.7 | 0.0481 | 0.2508 | 1.0 | équivalent | 1.0 | équivalent |
| 116 | Exclure les séjours sans durée | SVR quantile, noyau polynomial (degré 2) | svm | exclure | svr_q_polynomial | 1.1363 | 3.059 | 2.492 | 0.8627 | 7.0 | 0.0445 | 0.1146 | 1.0 | équivalent | 1.0 | équivalent |
| 117 | Exclure les séjours sans durée | C · perceptron multicouche quantile | concurrent | exclure | mlp | 1.139 | 3.026 | 2.499 | 0.9072 | 1.7 | 0.0162 | 0.1111 | 1.0 | équivalent | 1.0 | équivalent |
| 118 | Exclure les séjours sans durée | E · XGBoost quantile (second ordre) | concurrent | exclure | xgboost | 1.1581 | 3.136 | 2.618 | 0.8289 | 12.6 | 0.0595 | 0.0886 | 1.0 | équivalent | 1.0 | équivalent |
| 119 | Exclure les séjours sans durée | B · gradient boosting quantile | concurrent | exclure | boosting | 1.2361 | 3.079 | 2.613 | 0.8637 | 11.1 | 0.0319 | 0.0425 | 1.0 | équivalent | 1.0 | équivalent |
| 120 | ACP itérative (rang faible) | SVR RBF (niveau 2) | svm | acp_iterative | svr_rbf | 1.2966 | 2.691 | 2.816 | 1.4386 | 0.6 | 0.0159 | 0.0001 | 1.0 | équivalent | 0.0129 | meilleur |
| 121 | Médiane du service | SVR RBF (niveau 2) | svm | mediane | svr_rbf | 1.3178 | 2.716 | 2.745 | 1.3544 | 0.9 | 0.0126 | 0.0005 | 1.0 | équivalent | 0.0615 | équivalent |
| 122 | Moyenne du service | SVR RBF (niveau 2) | svm | moyenne | svr_rbf | 1.3178 | 2.716 | 2.745 | 1.3544 | 0.9 | 0.0126 | 0.0005 | 1.0 | équivalent | 0.0615 | équivalent |
| 123 | Médiane de la tranche d'âge | SVR RBF (niveau 2) | svm | mediane_age | svr_rbf | 1.3178 | 2.716 | 2.745 | 1.3544 | 0.5 | 0.0126 | 0.0005 | 1.0 | équivalent | 0.0615 | équivalent |
| 124 | SoftImpute (norme nucléaire) | SVR RBF (niveau 2) | svm | softimpute | svr_rbf | 1.36 | 2.718 | 2.764 | 1.381 | 0.4 | 0.0095 | 0.0054 | 1.0 | équivalent | 0.6318 | équivalent |
| 125 | Estimée : prix, puis issue, puis médiane | SVR RBF (niveau 2) | svm | estimee | svr_rbf | 1.3769 | 2.718 | 2.718 | 1.3769 | 0.7 | 0.0079 |  | 1.0 | équivalent |  | — référence |
| 126 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR RBF (niveau 2) | svm | knn | svr_rbf | 1.3772 | 2.727 | 2.747 | 1.3786 | 0.6 | 0.0078 | 0.974 | 0.9984 | équivalent | 1.0 | équivalent |
| 127 | Régressions enchaînées (ridge, principe de MICE) | SVR RBF (niveau 2) | svm | regression | svr_rbf | 1.3804 | 2.724 | 2.748 | 1.3822 | 0.7 | 0.0083 | 0.3422 | 1.0 | équivalent | 1.0 | équivalent |
| 128 | Loi normale multivariée par EM | SVR RBF (niveau 2) | svm | em | svr_rbf | 1.3843 | 2.725 | 2.754 | 1.3902 | 0.4 | 0.008 | 0.0723 | 1.0 | équivalent | 1.0 | équivalent |
| 129 | XGBoost (avec le diagnostic) | SVR RBF (niveau 2) | svm | xgboost | svr_rbf | 1.4213 | 2.714 | 2.641 | 1.2787 | 0.4 | 0.0053 | 0.0003 | 0.6996 | équivalent | 0.0372 | moins bon |
| 130 | Hybride : prix, sinon XGBoost | SVR RBF (niveau 2) | svm | hybride | svr_rbf | 1.4323 | 2.72 | 2.635 | 1.2857 | 0.4 | 0.0051 | 0.0002 | 0.6783 | équivalent | 0.025 | moins bon |
| 131 | Moyenne du service | SVR linéaire (niveau 1) | svm | moyenne | svr_lineaire | 1.4577 | 2.824 | 2.856 | 1.4965 | 0.7 | 0.0057 | 0.0001 | 0.7467 | équivalent | 0.0129 | meilleur |
| 132 | Médiane de la tranche d'âge | SVR linéaire (niveau 1) | svm | mediane_age | svr_lineaire | 1.4577 | 2.824 | 2.856 | 1.4965 | 0.5 | 0.0057 | 0.0001 | 0.7467 | équivalent | 0.0129 | meilleur |
| 133 | Médiane du service | SVR linéaire (niveau 1) | svm | mediane | svr_lineaire | 1.4577 | 2.824 | 2.856 | 1.4965 | 0.5 | 0.0057 | 0.0001 | 0.7467 | équivalent | 0.0129 | meilleur |
| 134 | ACP itérative (rang faible) | SVR linéaire (niveau 1) | svm | acp_iterative | svr_lineaire | 1.4628 | 2.822 | 2.953 | 1.6079 | 0.5 | 0.0045 | 0.0387 | 0.6075 | équivalent | 1.0 | équivalent |
| 135 | SoftImpute (norme nucléaire) | SVR linéaire (niveau 1) | svm | softimpute | svr_lineaire | 1.4868 | 2.818 | 2.859 | 1.5058 | 0.4 | 0.0048 | 0.0006 | 0.6432 | équivalent | 0.072 | équivalent |
| 136 | k plus proches voisins (prix, âge, sexe, issue, mois) | SVR linéaire (niveau 1) | svm | knn | svr_lineaire | 1.5292 | 2.82 | 2.85 | 1.5358 | 0.4 | 0.0039 | 0.8582 | 0.5304 | équivalent | 1.0 | équivalent |
| 137 | Estimée : prix, puis issue, puis médiane | SVR linéaire (niveau 1) | svm | estimee | svr_lineaire | 1.5319 | 2.822 | 2.822 | 1.5319 | 0.5 | 0.0035 |  | 0.4795 | équivalent |  | — référence |
| 138 | Régressions enchaînées (ridge, principe de MICE) | SVR linéaire (niveau 1) | svm | regression | svr_lineaire | 1.5385 | 2.832 | 2.86 | 1.5419 | 0.4 | 0.0032 | 0.1985 | 0.4448 | équivalent | 1.0 | équivalent |
| 139 | Loi normale multivariée par EM | SVR linéaire (niveau 1) | svm | em | svr_lineaire | 1.5417 | 2.828 | 2.861 | 1.5496 | 0.3 | 0.0032 | 0.0775 | 0.4448 | équivalent | 1.0 | équivalent |
| 140 | XGBoost (avec le diagnostic) | SVR linéaire (niveau 1) | svm | xgboost | svr_lineaire | 1.5714 | 2.803 | 2.724 | 1.4257 | 0.3 | 0.0029 | 0.0059 | 0.406 | équivalent | 0.6844 | équivalent |
| 141 | Hybride : prix, sinon XGBoost | SVR linéaire (niveau 1) | svm | hybride | svr_lineaire | 1.5908 | 2.817 | 2.715 | 1.4356 | 0.5 | 0.0024 | 0.0008 | 0.3384 | équivalent | 0.0952 | équivalent |
| 142 | Exclure les séjours sans durée | SVR RBF (niveau 2) | svm | exclure | svr_rbf | 1.9548 | 3.013 | 2.481 | 1.2309 | 0.9 | 0.0001 | 0.0 | 0.0143 | moins bon | 0.0 | moins bon |
| 143 | Exclure les séjours sans durée | SVR linéaire (niveau 1) | svm | exclure | svr_lineaire | 2.0828 | 3.147 | 2.579 | 1.3408 | 0.7 | 0.0001 | 0.0 | 0.0143 | moins bon | 0.0 | moins bon |


Meilleure paire : **Médiane de la tranche d'âge × LS-SVR (moindres carrés), noyau RBF, quantiles LOO**.
