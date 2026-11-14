# Banc de comparaison des choix — service MEDF_journee

Validation glissante du 01/03/2026 au verrou (01/09/2026), une origine tous les 28 jours, modèle réentraîné à chaque origine. « (retenu) » = choix retenu. Test de Diebold-Mariano (perte absolue, correction HLN) contre le choix retenu.


## Horizon J+1 — 183 jours évalués, 7 origines


### D1 · Modèles de référence, concurrents et SVR

*Le SVR fait-il mieux que les méthodes statistiques usuelles et que les autres modèles d'apprentissage ?*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | couverture 90 % | réglages | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Persistance | 2.127 | 2.795 | -0.016 | 1.0686 | 0.0 |  |  | 0.0001 | 0.0018 | 0.2858 | moins bon |
| Saisonnière hebdomadaire | 2.669 | 3.416 | 0.039 | 1.3226 | 0.0 |  |  | 0.0 | 0.0 | 0.0 | moins bon |
| Moyenne mobile 7 j | 2.451 | 3.019 | 0.007 | 1.2234 | 0.0 |  |  | 0.0 | 0.0 | 0.002 | moins bon |
| Moyenne historique | 3.243 | 3.952 | -1.885 | 0.9688 | 0.0 | 89.1 |  | 0.0002 | 0.0034 | 0.0 | moins bon |
| Lissage exponentiel simple | 2.122 | 2.786 | -0.016 | 0.7748 | 0.0 | 88.5 |  | 0.985 | 1.0 | 0.3017 | équivalent |
| Méthode Thêta | 2.123 | 2.786 | -0.005 | 0.7748 | 0.0 | 88.5 |  | 0.985 | 1.0 | 0.2984 | équivalent |
| Holt linéaire | 2.122 | 2.786 | -0.016 | 0.7748 | 0.1 | 88.5 |  | 0.985 | 1.0 | 0.3017 | équivalent |
| Holt amorti | 2.126 | 2.79 | -0.016 | 0.7743 | 0.1 | 88.5 |  | 0.9777 | 1.0 | 0.286 | équivalent |
| Lissage saisonnier sans tendance | 1.961 | 2.498 | -0.004 | 0.6918 | 0.1 | 90.7 |  | 0.1455 | 1.0 | 0.6931 | équivalent |
| Holt-Winters additif amorti | 1.965 | 2.531 | -0.002 | 0.7062 | 0.2 | 90.7 |  | 0.2341 | 1.0 | 0.7206 | équivalent |
| Holt-Winters multiplicatif amorti | 2.127 | 2.795 | -0.016 | 0.7757 | 0.0 | 89.1 |  | 0.9972 | 1.0 | 0.2858 | équivalent |
| AR(p) par AIC | 1.935 | 2.486 | -0.258 | 0.696 | 0.1 | 88.5 |  | 0.0744 | 1.0 | 0.411 | équivalent |
| SARIMA(2,0,0)(1,0,0)7 (ordre choisi sur l'apprentissage) | 1.961 | 2.535 | -0.293 | 0.7133 | 5.0 | 88.5 |  | 0.1767 | 1.0 | 0.6037 | équivalent |
| Holt-Winters additif, grille fixée avant la validation | 1.872 | 2.418 | -0.004 | 0.9371 | 0.1 |  | alpha=0.9, beta=0.0, gamma=0.3, phi=0.8 | 0.013 | 0.195 | 0.2178 | équivalent |
| Régression ridge (λ = 1) | 1.839 | 2.264 | -0.617 | 1.1044 | 0.2 |  |  | 0.0 | 0.0 | 0.0153 | moins bon |
| A · forêt aléatoire quantile | 2.027 | 2.562 | -0.51 | 0.7136 | 13.3 | 94.5 |  | 0.0938 | 1.0 | 0.6823 | équivalent |
| B · gradient boosting quantile | 1.921 | 2.429 | -0.587 | 0.8012 | 11.5 | 75.4 |  | 0.5116 | 1.0 | 0.179 | équivalent |
| C · perceptron multicouche quantile | 2.116 | 2.577 | -1.156 | 0.8087 | 1.5 | 80.9 |  | 0.519 | 1.0 | 0.1935 | équivalent |
| D · LSTM quantile | 2.12 | 2.618 | -1.027 | 0.8186 | 18.5 | 81.4 |  | 0.2768 | 1.0 | 0.0542 | équivalent |
| E · XGBoost quantile (second ordre) | 1.97 | 2.486 | -0.55 | 0.7714 | 12.2 | 85.8 |  | 0.8915 | 1.0 | 0.5401 | équivalent |
| SVR linéaire (niveau 1) | 1.817 | 2.282 | -0.723 | 1.1255 | 1.3 |  |  | 0.0 | 0.0 | 0.0016 | moins bon |
| SVR RBF (niveau 2) | 1.852 | 2.358 | -0.712 | 1.1395 | 1.8 |  |  | 0.0 | 0.0 | 0.0 | moins bon |
| SVR quantile RBF (niveau 3) | 2.002 | 2.507 | -0.752 | 0.7261 | 5.9 | 88.0 |  | 0.0004 | 0.0064 | 0.9514 | meilleur |
| SVR quantile composite (niveau 4) (retenu) | 2.004 | 2.51 | -0.745 | 0.7759 | 8.1 | 86.3 |  |  |  |  | — choix retenu |


Plus petite MAE : **SVR linéaire (niveau 1)** (1.817). ⚠ Significativement meilleur que le choix retenu : SVR quantile RBF (niveau 3) — le choix est à revoir.



### D2 · Noyau

*Quel noyau décrit le mieux la dynamique ? (même perte ε-insensible, même C)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Linéaire | 1.83 | 2.299 | -0.701 | 1.1255 | 1.6 | 0.5613 | 1.0 | 0.2452 | équivalent |
| RBF (γ = 0.02) | 1.852 | 2.358 | -0.712 | 1.1395 | 1.9 | 0.5971 | 1.0 | 0.1071 | équivalent |
| Composite occupation / flux et saison (β appris) (retenu) | 1.898 | 2.39 | -0.667 | 1.1491 | 2.5 |  |  |  | — choix retenu |


Plus petite MAE : **Linéaire** (1.83). Aucune variante ne bat significativement le choix retenu (Composite occupation / flux et saison (β appris) (retenu)).



### D3 · Fonction de perte

*Quelle perte pour un modèle linéaire identique ? (isole l'effet de la perte)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Carrée (ridge, λ = 1/C) | 1.831 | 2.26 | -0.626 | 1.1034 | 0.3 | 0.1323 | 0.3969 | 0.5603 | équivalent |
| ε-insensible, ε = 0 lit (= valeur absolue) | 1.831 | 2.298 | -0.739 | 1.1373 | 1.5 | 0.3183 | 0.6366 | 0.4602 | équivalent |
| ε-insensible, ε = 0.5 lit (retenu) | 1.817 | 2.282 | -0.723 | 1.1255 | 1.1 |  |  |  | — choix retenu |
| ε-insensible, ε = 1 lit | 1.86 | 2.317 | -0.731 | 1.1494 | 1.0 | 0.0661 | 0.2644 | 0.027 | équivalent |
| ε-insensible, ε = 2 lit | 1.888 | 2.343 | -0.678 | 1.1471 | 1.5 | 0.3621 | 0.6366 | 0.0537 | équivalent |


Plus petite MAE : **ε-insensible, ε = 0.5 lit (retenu)** (1.817). Aucune variante ne bat significativement le choix retenu (ε-insensible, ε = 0.5 lit (retenu)).



### D4 · Quantile décisionnel τ et coût des décisions

*Quel τ minimise le coût réel selon le rapport pénurie / lit vide ? (τ optimal théorique = r/(1+r))*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | jours sous-estimés % | lits prévus en moyenne | coût r=1 | coût r=2 | coût r=4 | coût r=9 | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| τ = 0.5 | 2.002 | 2.507 | -0.752 | 1.2265 | 1.9 | 64.5 | 12.88 | 2.002 | 3.379 | 6.132 | 13.017 | 0.0 | 0.0 | 0.553 | moins bon |
| τ = 0.6 | 1.885 | 2.369 | -0.224 | 1.0099 | 1.9 | 53.6 | 13.4 | 1.885 | 2.94 | 5.049 | 10.323 | 0.0 | 0.0 | 0.0415 | moins bon |
| τ = 0.7 | 1.878 | 2.38 | 0.253 | 0.8633 | 1.8 | 45.9 | 13.88 | 1.878 | 2.691 | 4.317 | 8.381 | 0.0 | 0.0 | 0.001 | moins bon |
| τ = 0.8 (retenu) | 2.077 | 2.645 | 1.041 | 0.7261 | 1.9 | 37.2 | 14.67 | 2.077 | 2.594 | 3.63 | 6.22 |  |  |  | — choix retenu |
| τ = 0.9 | 2.905 | 3.58 | 2.478 | 0.7093 | 1.8 | 13.7 | 16.1 | 2.905 | 3.119 | 3.547 | 4.615 | 0.6653 | 0.6653 | 0.0 | équivalent |


τ le moins coûteux pour chaque rapport de coûts r = c_pénurie / c_lit vide : r = 1 → τ = 0.7, r = 2 → τ = 0.8 (retenu), r = 4 → τ = 0.9, r = 9 → τ = 0.9. Le choix τ = 0.8 correspond à r = 4.


### D5 · Variables d'entrée

*Que rapporte chaque groupe de variables ? (même modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| 7 retards seuls | 2.005 | 2.57 | -0.478 | 1.1459 | 1.1 | 7 | 0.8561 | 1.0 | 0.0097 | équivalent |
| 7 retards + flux | 1.95 | 2.515 | -0.8 | 1.2151 | 2.0 | 10 | 0.0108 | 0.0648 | 0.0211 | équivalent |
| 7 retards + calendrier (jour, mois) | 1.937 | 2.458 | -0.543 | 1.1315 | 1.8 | 16 | 0.7471 | 1.0 | 0.0386 | équivalent |
| Complet : retards + flux + calendrier (retenu) | 1.852 | 2.358 | -0.712 | 1.1395 | 1.8 | 19 |  |  |  | — choix retenu |
| Complet + jours fériés camerounais | 1.857 | 2.363 | -0.707 | 1.1405 | 1.9 | 21 | 0.7771 | 1.0 | 0.3051 | équivalent |
| Complet + vacances scolaires | 1.873 | 2.377 | -0.714 | 1.1506 | 1.8 | 20 | 0.0143 | 0.0715 | 0.0014 | équivalent |
| Complet + fériés + vacances scolaires | 1.884 | 2.388 | -0.725 | 1.1593 | 2.0 | 22 | 0.0012 | 0.0096 | 0.0002 | moins bon |
| 3 retards + flux + calendrier | 2.004 | 2.519 | -0.807 | 1.2443 | 2.1 | 15 | 0.0 | 0.0 | 0.0 | moins bon |
| 14 retards + flux + calendrier | 1.881 | 2.399 | -0.659 | 1.1379 | 2.0 | 26 | 0.9404 | 1.0 | 0.3501 | équivalent |
| Complet + diagnostics d'entrée des présents | 2.012 | 2.557 | -0.816 | 1.2508 | 1.9 | 30 | 0.0012 | 0.0096 | 0.0011 | moins bon |


Plus petite MAE : **Complet : retards + flux + calendrier (retenu)** (1.852). Aucune variante ne bat significativement le choix retenu (Complet : retards + flux + calendrier (retenu)).



### D6 · Prétraitement

*Quelle mise à l'échelle des variables ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| z-score : (x − moyenne)/écart-type (retenu) | 1.852 | 2.358 | -0.712 | 1.1395 | 1.8 |  |  |  | — choix retenu |
| Robuste : (x − médiane)/(Q3 − Q1) | 1.892 | 2.374 | -0.708 | 1.1581 | 2.0 | 0.0895 | 0.0895 | 0.0167 | équivalent |
| Min-max : (x − min)/(max − min) | 2.454 | 2.96 | -0.863 | 1.4858 | 0.8 | 0.0 | 0.0 | 0.0 | moins bon |
| Aucune mise à l'échelle | 2.317 | 2.887 | -0.878 | 1.422 | 2.0 | 0.0 | 0.0 | 0.0 | moins bon |


Plus petite MAE : **z-score : (x − moyenne)/écart-type (retenu)** (1.852). Aucune variante ne bat significativement le choix retenu (z-score : (x − moyenne)/écart-type (retenu)).



### D7 · Fenêtre d'entraînement

*Faut-il tout le passé, ou seulement les derniers mois ? (mesure aussi le coût d'un historique court)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Croissante (tout le passé) (retenu) | 2.004 | 2.51 | -0.745 | 0.7759 | 86.3 | 9.2 |  |  |  | — choix retenu |
| Glissante : 365 derniers jours | 2.0 | 2.509 | -0.724 | 0.7773 | 86.3 | 8.4 | 0.4123 | 0.4123 | 0.6267 | équivalent |
| Glissante : 180 derniers jours | 2.103 | 2.593 | -0.075 | 0.7197 | 82.5 | 7.3 | 0.0416 | 0.0832 | 0.2088 | équivalent |
| Glissante : 90 derniers jours | 2.551 | 3.147 | -0.091 | 0.9089 | 79.8 | 7.7 | 0.0002 | 0.0006 | 0.0 | moins bon |


Plus petite MAE : **Glissante : 365 derniers jours** (2.0). Aucune variante ne bat significativement le choix retenu (Croissante (tout le passé) (retenu)).



### D8 · Optimisation

*Comment atteindre le minimum de J le plus sûrement ? (SVR RBF, un découpage)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | J final | pas effectués | arrêt | solution gardée | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Adam + Polyak + préconditionnement + décroissance η (retenu) | 2.487 | 3.06 | -1.802 | 1.7843 | 1.6 | 965.91 | 3000 | 3000 pas atteints | meilleur point rencontré |  |  |  | — choix retenu |
| Adam sans moyenne de Polyak | 2.487 | 3.06 | -1.802 | 1.7843 | 1.4 | 965.91 | 3000 | 3000 pas atteints | meilleur point rencontré |  |  |  | identique |
| Adam sans préconditionnement | 2.463 | 3.032 | -1.753 | 1.7574 | 1.1 | 977.97 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | 0.0032 | meilleur |
| Adam sans décroissance de η | 2.486 | 3.059 | -1.801 | 1.7835 | 0.7 | 966.01 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0884 | 0.0884 | 0.0863 | équivalent |
| Momentum | 2.925 | 3.556 | -1.851 | 2.0179 | 0.5 | 1371.14 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0001 | 0.0003 | 0.0 | moins bon |
| Descente de gradient simple | 2.925 | 3.556 | -1.851 | 2.0179 | 0.4 | 1371.14 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0001 | 0.0003 | 0.0 | moins bon |


Plus petite MAE : **Adam sans préconditionnement** (2.463). ⚠ Significativement meilleur que le choix retenu : Adam sans préconditionnement — le choix est à revoir.



### D9 · Combinaison des modèles

*Apprendre les poids de combinaison apporte-t-il plus qu'une moyenne ? (jours où l'empilement prédit)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Niveau 4 seul (meilleur modèle unique) | 2.016 | 2.524 | -1.026 | 0.7935 | 87.7 | 6.6 | 0.0425 | 0.17 | 0.2654 | équivalent |
| Moyenne simple persistance + niv. 3 + niv. 4 | 1.914 | 2.457 | -0.719 | 0.8115 | 76.1 | 13.2 | 0.0236 | 0.118 | 0.9347 | équivalent |
| Empilement appris (poids positifs) (retenu) | 1.92 | 2.509 | -0.256 | 0.6949 | 87.7 | 29.6 |  |  |  | — choix retenu |
| XGBoost quantile seul | 1.979 | 2.457 | -0.827 | 0.7797 | 85.2 | 11.5 | 0.1026 | 0.3078 | 0.5328 | équivalent |
| Moyenne SVR niv. 4 + XGBoost | 1.964 | 2.458 | -0.927 | 0.7679 | 91.0 | 18.1 | 0.1227 | 0.3078 | 0.6139 | équivalent |
| Empilement persistance + niv. 3 + niv. 4 + XGBoost | 1.939 | 2.518 | -0.277 | 0.6869 | 85.8 | 39.3 | 0.3795 | 0.3795 | 0.3334 | équivalent |


Plus petite MAE : **Moyenne simple persistance + niv. 3 + niv. 4** (1.914). Aucune variante ne bat significativement le choix retenu (Empilement appris (poids positifs) (retenu)).



### D13 · Variantes de SVM

*Quel SVM est le plus adapté à la série du service ? (mêmes jours, mêmes variables)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | cle | couverture 90 % | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SVR linéaire (niveau 1) | 1.817 | 2.282 | -0.723 | 1.1255 | 0.8 | svr_lineaire |  | 0.0 | 0.0 | 0.0016 | moins bon |
| SVR RBF (niveau 2) | 1.852 | 2.358 | -0.712 | 1.1395 | 1.1 | svr_rbf |  | 0.0 | 0.0 | 0.0 | moins bon |
| SVR quantile RBF (niveau 3) | 2.002 | 2.507 | -0.752 | 0.7261 | 3.2 | svr_q_rbf | 88.0 | 0.0004 | 0.0012 | 0.9514 | meilleur |
| SVR quantile composite (niveau 4, retenu) (retenu) | 2.004 | 2.51 | -0.745 | 0.7759 | 4.6 | svr_q_composite | 86.3 |  |  |  | — choix retenu |
| SVR quantile, noyau laplacien | 2.226 | 2.714 | -0.723 | 0.7635 | 3.0 | svr_q_laplacien | 89.1 | 0.5732 | 0.5732 | 0.0001 | équivalent |
| SVR quantile, noyau polynomial (degré 2) | 1.722 | 2.206 | -0.523 | 0.6584 | 4.6 | svr_q_polynomial | 86.9 | 0.0007 | 0.0014 | 0.0 | meilleur |
| LS-SVR (moindres carrés), noyau RBF, quantiles LOO | 1.802 | 2.293 | -0.549 | 0.6433 | 0.4 | lssvr_rbf | 88.5 | 0.0003 | 0.0012 | 0.0 | meilleur |


Plus petite MAE : **SVR quantile, noyau polynomial (degré 2)** (1.722). ⚠ Significativement meilleur que le choix retenu : SVR quantile RBF (niveau 3), SVR quantile, noyau polynomial (degré 2), LS-SVR (moindres carrés), noyau RBF, quantiles LOO — le choix est à revoir.



### D11 · Chaque variable, une à une

*Que perd le modèle si on lui retire cette seule variable ? (modèle RBF du niveau 2, mêmes jours)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 1.852 | 2.358 | -0.712 | 1.1395 | 1.8 |  |  |  | — choix retenu |
| Sans occ_j-0 | 2.119 | 2.586 | -0.788 | 1.2956 | 1.8 | 0.0 | 0.0 | 0.0 | moins bon |
| Sans occ_j-1 | 1.881 | 2.378 | -0.742 | 1.1631 | 1.1 | 0.031 | 0.403 | 0.0647 | équivalent |
| Sans occ_j-2 | 1.847 | 2.354 | -0.692 | 1.1313 | 1.7 | 0.1749 | 1.0 | 0.6295 | équivalent |
| Sans occ_j-3 | 1.84 | 2.348 | -0.691 | 1.127 | 1.5 | 0.004 | 0.06 | 0.0749 | équivalent |
| Sans occ_j-4 | 1.854 | 2.361 | -0.72 | 1.1429 | 1.6 | 0.4807 | 1.0 | 0.7523 | équivalent |
| Sans occ_j-5 | 1.864 | 2.367 | -0.716 | 1.1468 | 1.3 | 0.1954 | 1.0 | 0.1622 | équivalent |
| Sans occ_j-6 | 1.966 | 2.479 | -0.75 | 1.2081 | 1.9 | 0.0001 | 0.0017 | 0.0001 | moins bon |
| Sans adm_3j | 1.864 | 2.384 | -0.656 | 1.129 | 1.5 | 0.4917 | 1.0 | 0.5844 | équivalent |
| Sans adm_7j | 1.857 | 2.363 | -0.665 | 1.1279 | 1.7 | 0.3772 | 1.0 | 0.8117 | équivalent |
| Sans sorties_7j | 1.961 | 2.46 | -0.605 | 1.1619 | 1.9 | 0.2486 | 1.0 | 0.0007 | équivalent |
| Sans cible_jour_0 | 1.878 | 2.408 | -0.73 | 1.1581 | 0.8 | 0.0598 | 0.6578 | 0.0737 | équivalent |
| Sans cible_jour_1 | 1.848 | 2.354 | -0.713 | 1.1377 | 1.3 | 0.1036 | 0.984 | 0.0143 | équivalent |
| Sans cible_jour_2 | 1.862 | 2.367 | -0.747 | 1.155 | 1.5 | 0.0495 | 0.594 | 0.4068 | équivalent |
| Sans cible_jour_3 | 1.853 | 2.356 | -0.707 | 1.1389 | 1.3 | 0.8542 | 1.0 | 0.7055 | équivalent |
| Sans cible_jour_4 | 1.843 | 2.351 | -0.703 | 1.1325 | 1.2 | 0.0074 | 0.1036 | 0.0119 | équivalent |
| Sans cible_jour_5 | 1.928 | 2.456 | -0.779 | 1.198 | 1.3 | 0.0001 | 0.0017 | 0.0008 | moins bon |
| Sans cible_jour_6 | 1.876 | 2.388 | -0.768 | 1.1684 | 1.0 | 0.0 | 0.0 | 0.0245 | moins bon |
| Sans mois_sin | 1.864 | 2.372 | -0.61 | 1.1151 | 0.8 | 0.0984 | 0.984 | 0.5733 | équivalent |
| Sans mois_cos | 1.848 | 2.356 | -0.701 | 1.1343 | 0.8 | 0.7299 | 1.0 | 0.8695 | équivalent |


Plus petite MAE : **Sans occ_j-3** (1.84). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)).



### D14 · Sélection des variables par le lasso

*Le modèle gagne-t-il à ne garder que les variables choisies par le lasso ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 1.852 | 2.358 | -0.712 | 1.1395 | 0.8 | 19.0 |  |  |  | — choix retenu |
| Lasso, λ de plus petite erreur | 1.9 | 2.373 | -0.71 | 1.1632 | 14.0 | 10.1 | 0.2416 | 0.2416 | 0.1046 | équivalent |
| Lasso à un écart-type (λ_1se) | 1.867 | 2.332 | -0.5 | 1.0834 | 14.0 | 6.6 | 0.0156 | 0.0312 | 0.7101 | meilleur |


Plus petite MAE : **Toutes les variables (retenu)** (1.852). ⚠ Significativement meilleur que le choix retenu : Lasso à un écart-type (λ_1se) — le choix est à revoir.



## Horizon J+7 — 177 jours évalués, 7 origines


### D1 · Modèles de référence, concurrents et SVR

*Le SVR fait-il mieux que les méthodes statistiques usuelles et que les autres modèles d'apprentissage ?*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | couverture 90 % | réglages | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Persistance | 3.077 | 3.83 | 0.008 | 1.5359 | 0.0 |  |  | 0.0195 | 0.3705 | 0.9737 | équivalent |
| Saisonnière hebdomadaire | 2.687 | 3.425 | 0.086 | 1.3176 | 0.0 |  |  | 0.159 | 1.0 | 0.1517 | équivalent |
| Moyenne mobile 7 j | 3.056 | 3.742 | 0.087 | 1.5023 | 0.0 |  |  | 0.0728 | 1.0 | 0.974 | équivalent |
| Moyenne historique | 3.32 | 4.025 | -1.923 | 0.9892 | 0.0 | 89.3 |  | 0.5896 | 1.0 | 0.0995 | équivalent |
| Lissage exponentiel simple | 3.062 | 3.806 | 0.011 | 1.0956 | 0.0 | 95.5 |  | 0.6977 | 1.0 | 0.9897 | équivalent |
| Méthode Thêta | 3.063 | 3.807 | 0.085 | 1.0956 | 0.0 | 95.5 |  | 0.6979 | 1.0 | 0.9912 | équivalent |
| Holt linéaire | 3.062 | 3.806 | 0.011 | 1.0956 | 0.1 | 95.5 |  | 0.6977 | 1.0 | 0.9898 | équivalent |
| Holt amorti | 3.067 | 3.816 | 0.01 | 1.1013 | 0.1 | 95.5 |  | 0.6646 | 1.0 | 0.9975 | équivalent |
| Lissage saisonnier sans tendance | 3.076 | 3.829 | 0.008 | 1.1054 | 0.1 | 95.5 |  | 0.6437 | 1.0 | 0.9746 | équivalent |
| Holt-Winters additif amorti | 3.077 | 3.83 | 0.008 | 1.1056 | 0.2 | 95.5 |  | 0.6427 | 1.0 | 0.9737 | équivalent |
| Holt-Winters multiplicatif amorti | 3.077 | 3.83 | 0.008 | 1.1056 | 0.0 | 95.5 |  | 0.6427 | 1.0 | 0.9737 | équivalent |
| AR(p) par AIC | 2.928 | 3.514 | -0.847 | 0.958 | 0.1 | 91.5 |  | 0.2074 | 1.0 | 0.1163 | équivalent |
| SARIMA(2,0,0)(1,0,0)7 (ordre choisi sur l'apprentissage) | 2.874 | 3.463 | -1.065 | 0.9118 | 5.0 | 91.5 |  | 0.0805 | 1.0 | 0.0761 | équivalent |
| Holt-Winters additif, grille fixée avant la validation | 2.711 | 3.386 | 0.08 | 1.3317 | 0.1 |  | alpha=0.1, beta=0.0, gamma=0.05, phi=0.8 | 0.1663 | 1.0 | 0.202 | équivalent |
| Régression ridge (λ = 1) | 3.455 | 4.129 | -1.684 | 2.2328 | 0.2 |  |  | 0.0001 | 0.0023 | 0.0068 | moins bon |
| A · forêt aléatoire quantile | 3.032 | 3.688 | -1.237 | 1.0699 | 9.9 | 94.9 |  | 0.6488 | 1.0 | 0.744 | équivalent |
| B · gradient boosting quantile | 3.261 | 3.991 | -1.541 | 1.3966 | 8.6 | 68.4 |  | 0.0345 | 0.6174 | 0.3106 | équivalent |
| C · perceptron multicouche quantile | 3.6 | 4.266 | -1.612 | 1.1508 | 1.5 | 84.7 |  | 0.1857 | 1.0 | 0.008 | équivalent |
| D · LSTM quantile | 3.993 | 4.704 | -2.003 | 1.3046 | 7.7 | 65.5 |  | 0.0013 | 0.026 | 0.0 | moins bon |
| E · XGBoost quantile (second ordre) | 3.199 | 3.916 | -1.502 | 1.2463 | 13.7 | 79.7 |  | 0.0343 | 0.6174 | 0.4709 | équivalent |
| SVR linéaire (niveau 1) | 3.401 | 4.092 | -1.415 | 2.1249 | 1.5 |  |  | 0.0002 | 0.0044 | 0.0005 | moins bon |
| SVR RBF (niveau 2) | 3.018 | 3.664 | -1.244 | 1.8823 | 1.8 |  |  | 0.0004 | 0.0084 | 0.4437 | moins bon |
| SVR quantile RBF (niveau 3) | 3.12 | 3.75 | -1.119 | 1.0188 | 4.0 | 89.8 |  | 0.1698 | 1.0 | 0.2242 | équivalent |
| SVR quantile composite (niveau 4) (retenu) | 3.066 | 3.677 | -1.108 | 1.0456 | 6.6 | 89.8 |  |  |  |  | — choix retenu |


Plus petite MAE : **Saisonnière hebdomadaire** (2.687). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4) (retenu)).



### D2 · Noyau

*Quel noyau décrit le mieux la dynamique ? (même perte ε-insensible, même C)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Linéaire | 3.568 | 4.288 | -1.617 | 2.2689 | 1.5 | 0.0034 | 0.0068 | 0.0 | moins bon |
| RBF (γ = 0.05) | 3.018 | 3.664 | -1.244 | 1.8823 | 1.3 | 0.9657 | 0.9657 | 0.5996 | équivalent |
| Composite occupation / flux et saison (β appris) (retenu) | 2.98 | 3.634 | -1.315 | 1.8846 | 2.7 |  |  |  | — choix retenu |


Plus petite MAE : **Composite occupation / flux et saison (β appris) (retenu)** (2.98). Aucune variante ne bat significativement le choix retenu (Composite occupation / flux et saison (β appris) (retenu)).



### D3 · Fonction de perte

*Quelle perte pour un modèle linéaire identique ? (isole l'effet de la perte)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Carrée (ridge, λ = 1/C) | 3.424 | 4.096 | -1.653 | 2.2076 | 0.2 | 0.083 | 0.332 | 0.7452 | équivalent |
| ε-insensible, ε = 0 lit (= valeur absolue) | 3.403 | 4.09 | -1.454 | 2.1374 | 1.5 | 0.6559 | 1.0 | 0.9553 | équivalent |
| ε-insensible, ε = 0.5 lit (retenu) | 3.401 | 4.092 | -1.415 | 2.1249 | 1.1 |  |  |  | — choix retenu |
| ε-insensible, ε = 1 lit | 3.427 | 4.114 | -1.396 | 2.1322 | 1.5 | 0.7586 | 1.0 | 0.4546 | équivalent |
| ε-insensible, ε = 2 lit | 3.338 | 4.025 | -1.443 | 2.1022 | 1.3 | 0.3327 | 0.9981 | 0.0278 | équivalent |


Plus petite MAE : **ε-insensible, ε = 2 lit** (3.338). Aucune variante ne bat significativement le choix retenu (ε-insensible, ε = 0.5 lit (retenu)).



### D4 · Quantile décisionnel τ et coût des décisions

*Quel τ minimise le coût réel selon le rapport pénurie / lit vide ? (τ optimal théorique = r/(1+r))*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | jours sous-estimés % | lits prévus en moyenne | coût r=1 | coût r=2 | coût r=4 | coût r=9 | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| τ = 0.5 | 3.12 | 3.75 | -1.119 | 1.8957 | 1.9 | 59.9 | 12.53 | 3.12 | 5.24 | 9.478 | 20.075 | 0.0006 | 0.0024 | 0.9908 | moins bon |
| τ = 0.6 | 3.044 | 3.625 | -0.171 | 1.5732 | 1.1 | 54.2 | 13.48 | 3.044 | 4.651 | 7.866 | 15.902 | 0.0011 | 0.0033 | 0.8231 | moins bon |
| τ = 0.7 | 3.0 | 3.673 | 0.747 | 1.2756 | 0.6 | 47.5 | 14.4 | 3.0 | 4.126 | 6.378 | 12.008 | 0.0048 | 0.0096 | 0.4803 | moins bon |
| τ = 0.8 (retenu) | 3.114 | 3.928 | 1.795 | 1.0188 | 1.2 | 32.8 | 15.44 | 3.114 | 3.774 | 5.094 | 8.393 |  |  |  | — choix retenu |
| τ = 0.9 | 3.999 | 4.904 | 3.458 | 0.9623 | 1.1 | 16.4 | 17.11 | 3.999 | 4.27 | 4.812 | 6.166 | 0.5832 | 0.5832 | 0.0 | équivalent |


τ le moins coûteux pour chaque rapport de coûts r = c_pénurie / c_lit vide : r = 1 → τ = 0.7, r = 2 → τ = 0.8 (retenu), r = 4 → τ = 0.9, r = 9 → τ = 0.9. Le choix τ = 0.8 correspond à r = 4.


### D5 · Variables d'entrée

*Que rapporte chaque groupe de variables ? (même modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| 7 retards seuls | 3.076 | 3.695 | -1.206 | 1.8995 | 0.9 | 7 | 0.8519 | 1.0 | 0.566 | équivalent |
| 7 retards + flux | 3.076 | 3.692 | -1.336 | 1.9388 | 1.2 | 10 | 0.5664 | 1.0 | 0.6429 | équivalent |
| 7 retards + calendrier (jour, mois) | 3.097 | 3.766 | -1.194 | 1.9064 | 1.1 | 16 | 0.7499 | 1.0 | 0.418 | équivalent |
| Complet : retards + flux + calendrier (retenu) | 3.018 | 3.664 | -1.244 | 1.8823 | 1.5 | 19 |  |  |  | — choix retenu |
| Complet + jours fériés camerounais | 3.022 | 3.669 | -1.272 | 1.8925 | 1.4 | 21 | 0.1036 | 0.7368 | 0.7174 | équivalent |
| Complet + vacances scolaires | 3.087 | 3.742 | -1.262 | 1.9223 | 1.7 | 20 | 0.0921 | 0.7368 | 0.033 | équivalent |
| Complet + fériés + vacances scolaires | 3.092 | 3.748 | -1.286 | 1.9321 | 1.3 | 22 | 0.0551 | 0.4959 | 0.0347 | équivalent |
| 3 retards + flux + calendrier | 2.972 | 3.612 | -1.233 | 1.856 | 1.4 | 15 | 0.4418 | 1.0 | 0.3046 | équivalent |
| 14 retards + flux + calendrier | 3.051 | 3.696 | -0.942 | 1.8081 | 1.8 | 26 | 0.2991 | 1.0 | 0.7751 | équivalent |
| Complet + diagnostics d'entrée des présents | 3.007 | 3.611 | -0.938 | 1.7851 | 1.7 | 30 | 0.3819 | 1.0 | 0.9332 | équivalent |


Plus petite MAE : **3 retards + flux + calendrier** (2.972). Aucune variante ne bat significativement le choix retenu (Complet : retards + flux + calendrier (retenu)).



### D6 · Prétraitement

*Quelle mise à l'échelle des variables ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| z-score : (x − moyenne)/écart-type (retenu) | 3.018 | 3.664 | -1.244 | 1.8823 | 1.9 |  |  |  | — choix retenu |
| Robuste : (x − médiane)/(Q3 − Q1) | 3.149 | 3.815 | -1.303 | 1.9654 | 1.6 | 0.0459 | 0.1377 | 0.0025 | équivalent |
| Min-max : (x − min)/(max − min) | 3.16 | 3.775 | -1.106 | 1.9118 | 0.9 | 0.6791 | 1.0 | 0.1274 | équivalent |
| Aucune mise à l'échelle | 3.07 | 3.618 | -1.141 | 1.8774 | 1.3 | 0.9694 | 1.0 | 0.7505 | équivalent |


Plus petite MAE : **z-score : (x − moyenne)/écart-type (retenu)** (3.018). Aucune variante ne bat significativement le choix retenu (z-score : (x − moyenne)/écart-type (retenu)).



### D7 · Fenêtre d'entraînement

*Faut-il tout le passé, ou seulement les derniers mois ? (mesure aussi le coût d'un historique court)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Croissante (tout le passé) (retenu) | 3.066 | 3.677 | -1.108 | 1.0456 | 89.8 | 5.0 |  |  |  | — choix retenu |
| Glissante : 365 derniers jours | 3.07 | 3.678 | -1.103 | 1.0455 | 89.8 | 5.2 |  |  | 0.3168 | identique |
| Glissante : 180 derniers jours | 2.928 | 3.566 | -0.192 | 0.9773 | 88.7 | 5.8 | 0.1118 | 0.1118 | 0.4576 | équivalent |
| Glissante : 90 derniers jours | 3.151 | 3.798 | -0.083 | 1.1284 | 79.7 | 3.8 | 0.0134 | 0.0268 | 0.7171 | moins bon |


Plus petite MAE : **Glissante : 180 derniers jours** (2.928). Aucune variante ne bat significativement le choix retenu (Croissante (tout le passé) (retenu)).



### D8 · Optimisation

*Comment atteindre le minimum de J le plus sûrement ? (SVR RBF, un découpage)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | J final | pas effectués | arrêt | solution gardée | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Adam + Polyak + préconditionnement + décroissance η (retenu) | 4.048 | 4.894 | -3.171 | 2.9754 | 0.3 | 1029.61 | 800 | J stable depuis 100 pas (pas 799) | meilleur point rencontré |  |  |  | — choix retenu |
| Adam sans moyenne de Polyak | 4.048 | 4.894 | -3.171 | 2.9754 | 0.2 | 1029.61 | 800 | J stable depuis 100 pas (pas 799) | meilleur point rencontré |  |  |  | identique |
| Adam sans préconditionnement | 4.013 | 4.851 | -3.11 | 2.9396 | 1.0 | 1039.68 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0001 | 0.0002 | 0.0155 | meilleur |
| Adam sans décroissance de η | 4.048 | 4.892 | -3.167 | 2.9739 | 1.1 | 1029.72 | 2190 | J stable depuis 100 pas (pas 2189) | meilleur point rencontré | 0.0354 | 0.0354 | 0.407 | meilleur |
| Momentum | 3.153 | 3.793 | -1.3 | 1.9663 | 1.2 | 1229.52 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | 0.0005 | meilleur |
| Descente de gradient simple | 3.153 | 3.793 | -1.3 | 1.9663 | 1.0 | 1229.52 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | 0.0005 | meilleur |


Plus petite MAE : **Momentum** (3.153). ⚠ Significativement meilleur que le choix retenu : Adam sans préconditionnement, Adam sans décroissance de η, Momentum, Descente de gradient simple — le choix est à revoir.



### D9 · Combinaison des modèles

*Apprendre les poids de combinaison apporte-t-il plus qu'une moyenne ? (jours où l'empilement prédit)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Niveau 4 seul (meilleur modèle unique) | 3.148 | 3.749 | -1.602 | 1.0525 | 89.9 | 4.7 | 0.8096 | 1.0 | 0.7739 | équivalent |
| Moyenne simple persistance + niv. 3 + niv. 4 | 2.803 | 3.364 | -1.104 | 1.0687 | 75.2 | 9.4 | 0.8828 | 1.0 | 0.1357 | équivalent |
| Empilement appris (poids positifs) (retenu) | 3.234 | 3.973 | -0.583 | 1.094 | 89.3 | 27.7 |  |  |  | — choix retenu |
| XGBoost quantile seul | 3.313 | 4.033 | -2.115 | 1.3144 | 79.9 | 12.1 | 0.3754 | 1.0 | 0.8497 | équivalent |
| Moyenne SVR niv. 4 + XGBoost | 3.185 | 3.835 | -1.858 | 1.1672 | 85.9 | 16.8 | 0.7231 | 1.0 | 0.8877 | équivalent |
| Empilement persistance + niv. 3 + niv. 4 + XGBoost | 3.089 | 3.798 | -0.302 | 1.0945 | 87.2 | 39.0 | 0.9887 | 1.0 | 0.2163 | équivalent |


Plus petite MAE : **Moyenne simple persistance + niv. 3 + niv. 4** (2.803). Aucune variante ne bat significativement le choix retenu (Empilement appris (poids positifs) (retenu)).



### D13 · Variantes de SVM

*Quel SVM est le plus adapté à la série du service ? (mêmes jours, mêmes variables)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | cle | couverture 90 % | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SVR linéaire (niveau 1) | 3.401 | 4.092 | -1.415 | 2.1249 | 1.5 | svr_lineaire |  | 0.0002 | 0.0012 | 0.0005 | moins bon |
| SVR RBF (niveau 2) | 3.018 | 3.664 | -1.244 | 1.8823 | 1.9 | svr_rbf |  | 0.0004 | 0.002 | 0.4437 | moins bon |
| SVR quantile RBF (niveau 3) | 3.12 | 3.75 | -1.119 | 1.0188 | 3.7 | svr_q_rbf | 89.8 | 0.1698 | 0.5604 | 0.2242 | équivalent |
| SVR quantile composite (niveau 4, retenu) (retenu) | 3.066 | 3.677 | -1.108 | 1.0456 | 6.7 | svr_q_composite | 89.8 |  |  |  | — choix retenu |
| SVR quantile, noyau laplacien | 3.105 | 3.72 | -1.149 | 1.0126 | 3.6 | svr_q_laplacien | 88.1 | 0.4428 | 0.8856 | 0.6344 | équivalent |
| SVR quantile, noyau polynomial (degré 2) | 3.122 | 3.797 | -1.278 | 1.1085 | 5.0 | svr_q_polynomial | 87.6 | 0.1401 | 0.5604 | 0.4713 | équivalent |
| LS-SVR (moindres carrés), noyau RBF, quantiles LOO | 2.959 | 3.647 | -1.377 | 1.0371 | 0.3 | lssvr_rbf | 84.7 | 0.8549 | 0.8856 | 0.4323 | équivalent |


Plus petite MAE : **LS-SVR (moindres carrés), noyau RBF, quantiles LOO** (2.959). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4, retenu) (retenu)).



### D11 · Chaque variable, une à une

*Que perd le modèle si on lui retire cette seule variable ? (modèle RBF du niveau 2, mêmes jours)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 3.018 | 3.664 | -1.244 | 1.8823 | 1.8 |  |  |  | — choix retenu |
| Sans occ_j-0 | 3.043 | 3.704 | -1.276 | 1.9042 | 2.0 | 0.0988 | 1.0 | 0.1728 | équivalent |
| Sans occ_j-1 | 3.014 | 3.664 | -1.21 | 1.87 | 1.8 | 0.5037 | 1.0 | 0.8614 | équivalent |
| Sans occ_j-2 | 2.99 | 3.635 | -1.24 | 1.8671 | 1.6 | 0.1737 | 1.0 | 0.0583 | équivalent |
| Sans occ_j-3 | 3.006 | 3.663 | -1.25 | 1.8781 | 1.4 | 0.7128 | 1.0 | 0.5085 | équivalent |
| Sans occ_j-4 | 2.999 | 3.641 | -1.224 | 1.8666 | 1.9 | 0.0398 | 0.6239 | 0.0371 | équivalent |
| Sans occ_j-5 | 2.993 | 3.636 | -1.21 | 1.8592 | 2.0 | 0.0386 | 0.6239 | 0.0664 | équivalent |
| Sans occ_j-6 | 3.018 | 3.652 | -1.232 | 1.8786 | 1.9 | 0.8062 | 1.0 | 0.9796 | équivalent |
| Sans adm_3j | 3.024 | 3.664 | -1.239 | 1.8839 | 1.6 | 0.8801 | 1.0 | 0.6857 | équivalent |
| Sans adm_7j | 3.03 | 3.691 | -1.24 | 1.8869 | 1.8 | 0.8952 | 1.0 | 0.7961 | équivalent |
| Sans sorties_7j | 3.051 | 3.702 | -1.233 | 1.8952 | 1.7 | 0.7696 | 1.0 | 0.488 | équivalent |
| Sans cible_jour_0 | 3.006 | 3.651 | -1.234 | 1.8731 | 1.7 | 0.0053 | 0.0954 | 0.0078 | équivalent |
| Sans cible_jour_1 | 3.026 | 3.676 | -1.239 | 1.8845 | 1.8 | 0.8204 | 1.0 | 0.576 | équivalent |
| Sans cible_jour_2 | 3.003 | 3.646 | -1.214 | 1.8656 | 1.4 | 0.0046 | 0.0874 | 0.1386 | équivalent |
| Sans cible_jour_3 | 3.037 | 3.697 | -1.246 | 1.8926 | 1.1 | 0.4124 | 1.0 | 0.2766 | équivalent |
| Sans cible_jour_4 | 3.028 | 3.668 | -1.255 | 1.8903 | 1.8 | 0.0367 | 0.6239 | 0.2036 | équivalent |
| Sans cible_jour_5 | 3.024 | 3.672 | -1.223 | 1.8789 | 1.7 | 0.5053 | 1.0 | 0.425 | équivalent |
| Sans cible_jour_6 | 3.047 | 3.711 | -1.263 | 1.9021 | 1.7 | 0.2332 | 1.0 | 0.2419 | équivalent |
| Sans mois_sin | 3.123 | 3.75 | -1.096 | 1.8904 | 2.0 | 0.9006 | 1.0 | 0.306 | équivalent |
| Sans mois_cos | 3.03 | 3.664 | -1.352 | 1.9205 | 1.9 | 0.6739 | 1.0 | 0.9191 | équivalent |


Plus petite MAE : **Sans occ_j-2** (2.99). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)).



### D14 · Sélection des variables par le lasso

*Le modèle gagne-t-il à ne garder que les variables choisies par le lasso ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 3.018 | 3.664 | -1.244 | 1.8823 | 1.7 | 19.0 |  |  |  | — choix retenu |
| Lasso, λ de plus petite erreur | 3.365 | 4.039 | -1.565 | 2.1523 | 25.3 | 4.9 | 0.0019 | 0.0038 | 0.0009 | moins bon |
| Lasso à un écart-type (λ_1se) | 3.117 | 3.752 | -1.319 | 1.9544 | 29.1 | 1.0 | 0.5617 | 0.5617 | 0.4942 | équivalent |


Plus petite MAE : **Toutes les variables (retenu)** (3.018). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)).

