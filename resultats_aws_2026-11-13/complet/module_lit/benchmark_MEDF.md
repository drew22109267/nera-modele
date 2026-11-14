# Banc de comparaison des choix — service MEDF

Validation glissante du 01/03/2026 au verrou (01/09/2026), une origine tous les 28 jours, modèle réentraîné à chaque origine. « (retenu) » = choix retenu. Test de Diebold-Mariano (perte absolue, correction HLN) contre le choix retenu.


## Horizon J+1 — 183 jours évalués, 7 origines


### D1 · Modèles de référence, concurrents et SVR

*Le SVR fait-il mieux que les méthodes statistiques usuelles et que les autres modèles d'apprentissage ?*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | couverture 90 % | réglages | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Persistance | 1.795 | 2.482 | 0.0 | 0.8975 | 0.0 |  |  | 0.0011 | 0.0187 | 0.1298 | moins bon |
| Saisonnière hebdomadaire | 2.531 | 3.056 | 0.009 | 1.2628 | 0.0 |  |  | 0.0 | 0.0 | 0.0 | moins bon |
| Moyenne mobile 7 j | 2.215 | 2.727 | -0.005 | 1.1094 | 0.0 |  |  | 0.0 | 0.0 | 0.0197 | moins bon |
| Moyenne historique | 2.807 | 3.401 | -1.576 | 0.8539 | 0.0 | 90.2 |  | 0.0005 | 0.009 | 0.0 | moins bon |
| Lissage exponentiel simple | 1.792 | 2.468 | -0.001 | 0.6195 | 0.0 | 88.5 |  | 0.1184 | 1.0 | 0.1173 | équivalent |
| Méthode Thêta | 1.792 | 2.468 | 0.008 | 0.6195 | 0.0 | 88.5 |  | 0.1184 | 1.0 | 0.1178 | équivalent |
| Holt linéaire | 1.792 | 2.469 | -0.0 | 0.6192 | 0.1 | 88.5 |  | 0.1168 | 1.0 | 0.1159 | équivalent |
| Holt amorti | 1.792 | 2.468 | -0.001 | 0.6195 | 0.1 | 88.5 |  | 0.1184 | 1.0 | 0.1173 | équivalent |
| Lissage saisonnier sans tendance | 1.764 | 2.401 | -0.003 | 0.6225 | 0.1 | 88.5 |  | 0.1159 | 1.0 | 0.0547 | équivalent |
| Holt-Winters additif amorti | 1.784 | 2.467 | -0.004 | 0.6104 | 0.1 | 89.1 |  | 0.0779 | 0.9348 | 0.1015 | équivalent |
| Holt-Winters multiplicatif amorti | 1.795 | 2.482 | 0.0 | 0.6202 | 0.0 | 88.5 |  | 0.1264 | 1.0 | 0.1298 | équivalent |
| AR(p) par AIC | 1.789 | 2.311 | -0.219 | 0.5897 | 0.1 | 89.6 |  | 0.0044 | 0.0616 | 0.0137 | équivalent |
| SARIMA(1,0,0)(1,0,0)7 (ordre choisi sur l'apprentissage) | 1.747 | 2.278 | -0.307 | 0.5889 | 7.2 | 90.2 |  | 0.003 | 0.048 | 0.0016 | meilleur |
| Holt-Winters additif, grille fixée avant la validation | 1.739 | 2.358 | -0.002 | 0.8702 | 0.1 |  | alpha=0.9, beta=0.0, gamma=0.15, phi=0.8 | 0.0031 | 0.048 | 0.0263 | moins bon |
| Régression ridge (λ = 1) | 1.763 | 2.236 | -0.418 | 1.0071 | 0.2 |  |  | 0.0 | 0.0 | 0.0003 | moins bon |
| A · forêt aléatoire quantile | 1.9 | 2.383 | -0.407 | 0.6229 | 13.7 | 95.1 |  | 0.0146 | 0.1898 | 0.4288 | équivalent |
| B · gradient boosting quantile | 1.904 | 2.407 | -0.341 | 0.7442 | 10.5 | 74.3 |  | 0.0788 | 0.9348 | 0.5163 | équivalent |
| C · perceptron multicouche quantile | 1.962 | 2.395 | -0.689 | 0.7201 | 1.4 | 85.2 |  | 0.3695 | 1.0 | 0.7353 | équivalent |
| D · LSTM quantile | 1.987 | 2.431 | -0.665 | 0.714 | 13.9 | 78.1 |  | 0.4031 | 1.0 | 0.4038 | équivalent |
| E · XGBoost quantile (second ordre) | 1.896 | 2.377 | -0.316 | 0.744 | 10.3 | 85.8 |  | 0.1128 | 1.0 | 0.4052 | équivalent |
| SVR linéaire (niveau 1) | 1.762 | 2.225 | -0.28 | 0.9647 | 1.5 |  |  | 0.0 | 0.0 | 0.0001 | moins bon |
| SVR RBF (niveau 2) | 1.799 | 2.24 | -0.32 | 0.9955 | 1.8 |  |  | 0.0 | 0.0 | 0.0002 | moins bon |
| SVR quantile RBF (niveau 3) | 1.915 | 2.363 | -0.585 | 0.6838 | 5.3 | 88.5 |  | 0.664 | 1.0 | 0.4997 | équivalent |
| SVR quantile composite (niveau 4) (retenu) | 1.941 | 2.361 | -0.495 | 0.6897 | 6.2 | 85.8 |  |  |  |  | — choix retenu |


Plus petite MAE : **Holt-Winters additif, grille fixée avant la validation** (1.739). ⚠ Significativement meilleur que le choix retenu : SARIMA(1,0,0)(1,0,0)7 (ordre choisi sur l'apprentissage) — le choix est à revoir.



### D2 · Noyau

*Quel noyau décrit le mieux la dynamique ? (même perte ε-insensible, même C)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Linéaire | 1.751 | 2.22 | -0.328 | 0.9739 | 1.1 | 0.0532 | 0.0748 | 0.0407 | équivalent |
| RBF (γ = 0.02) | 1.799 | 2.24 | -0.32 | 0.9955 | 2.0 | 0.0374 | 0.0748 | 0.1063 | équivalent |
| Composite occupation / flux et saison (β appris) (retenu) | 1.856 | 2.3 | -0.364 | 1.0371 | 2.5 |  |  |  | — choix retenu |


Plus petite MAE : **Linéaire** (1.751). Aucune variante ne bat significativement le choix retenu (Composite occupation / flux et saison (β appris) (retenu)).



### D3 · Fonction de perte

*Quelle perte pour un modèle linéaire identique ? (isole l'effet de la perte)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Carrée (ridge, λ = 1/C) | 1.766 | 2.236 | -0.426 | 1.0109 | 0.2 | 0.0002 | 0.0006 | 0.8395 | moins bon |
| ε-insensible, ε = 0 lit (= valeur absolue) | 1.744 | 2.235 | -0.461 | 1.0104 | 1.2 | 0.0088 | 0.0176 | 0.5802 | moins bon |
| ε-insensible, ε = 0.5 lit | 1.766 | 2.243 | -0.369 | 0.994 | 0.9 | 0.0256 | 0.0256 | 0.8239 | moins bon |
| ε-insensible, ε = 1 lit (retenu) | 1.762 | 2.225 | -0.28 | 0.9647 | 1.4 |  |  |  | — choix retenu |
| ε-insensible, ε = 2 lit | 1.786 | 2.253 | -0.472 | 1.0343 | 1.5 | 0.0 | 0.0 | 0.3725 | moins bon |


Plus petite MAE : **ε-insensible, ε = 0 lit (= valeur absolue)** (1.744). Aucune variante ne bat significativement le choix retenu (ε-insensible, ε = 1 lit (retenu)).



### D4 · Quantile décisionnel τ et coût des décisions

*Quel τ minimise le coût réel selon le rapport pénurie / lit vide ? (τ optimal théorique = r/(1+r))*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | jours sous-estimés % | lits prévus en moyenne | coût r=1 | coût r=2 | coût r=4 | coût r=9 | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| τ = 0.5 | 1.915 | 2.363 | -0.585 | 1.1333 | 1.8 | 60.7 | 10.28 | 1.915 | 3.166 | 5.666 | 11.918 | 0.0 | 0.0 | 0.0313 | moins bon |
| τ = 0.6 | 1.885 | 2.336 | 0.048 | 0.9282 | 1.7 | 53.0 | 10.91 | 1.885 | 2.804 | 4.641 | 9.234 | 0.0 | 0.0 | 0.0008 | moins bon |
| τ = 0.7 | 2.012 | 2.499 | 0.826 | 0.7583 | 1.8 | 36.6 | 11.69 | 2.012 | 2.605 | 3.792 | 6.758 | 0.0006 | 0.0012 | 0.0 | moins bon |
| τ = 0.8 (retenu) | 2.197 | 2.75 | 1.382 | 0.6838 | 1.8 | 31.1 | 12.24 | 2.197 | 2.604 | 3.419 | 5.456 |  |  |  | — choix retenu |
| τ = 0.9 | 2.691 | 3.37 | 2.369 | 0.6351 | 1.8 | 17.5 | 13.23 | 2.691 | 2.853 | 3.176 | 3.983 | 0.1379 | 0.1379 | 0.0 | équivalent |


τ le moins coûteux pour chaque rapport de coûts r = c_pénurie / c_lit vide : r = 1 → τ = 0.6, r = 2 → τ = 0.8 (retenu), r = 4 → τ = 0.9, r = 9 → τ = 0.9. Le choix τ = 0.8 correspond à r = 4.


### D5 · Variables d'entrée

*Que rapporte chaque groupe de variables ? (même modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| 7 retards seuls | 1.822 | 2.283 | -0.346 | 1.0146 | 1.9 | 7 | 0.4466 | 1.0 | 0.5954 | équivalent |
| 7 retards + flux | 1.869 | 2.323 | -0.456 | 1.0715 | 1.9 | 10 | 0.0002 | 0.0014 | 0.0286 | moins bon |
| 7 retards + calendrier (jour, mois) | 1.781 | 2.247 | -0.311 | 0.984 | 1.9 | 16 | 0.5371 | 1.0 | 0.5823 | équivalent |
| Complet : retards + flux + calendrier (retenu) | 1.799 | 2.24 | -0.32 | 0.9955 | 1.9 | 19 |  |  |  | — choix retenu |
| Complet + jours fériés camerounais | 1.801 | 2.245 | -0.324 | 0.9976 | 2.0 | 21 | 0.236 | 0.944 | 0.4372 | équivalent |
| Complet + vacances scolaires | 1.823 | 2.269 | -0.355 | 1.018 | 1.8 | 20 | 0.0 | 0.0 | 0.0002 | moins bon |
| Complet + fériés + vacances scolaires | 1.823 | 2.273 | -0.359 | 1.0194 | 1.9 | 22 | 0.0 | 0.0 | 0.0004 | moins bon |
| 3 retards + flux + calendrier | 1.803 | 2.265 | -0.349 | 1.0061 | 1.9 | 15 | 0.4311 | 1.0 | 0.8713 | équivalent |
| 14 retards + flux + calendrier | 1.878 | 2.346 | -0.387 | 1.055 | 2.2 | 26 | 0.0004 | 0.0024 | 0.0021 | moins bon |
| Complet + diagnostics d'entrée des présents | 1.904 | 2.374 | -0.472 | 1.0936 | 1.8 | 30 | 0.0006 | 0.003 | 0.0146 | moins bon |


Plus petite MAE : **7 retards + calendrier (jour, mois)** (1.781). Aucune variante ne bat significativement le choix retenu (Complet : retards + flux + calendrier (retenu)).



### D6 · Prétraitement

*Quelle mise à l'échelle des variables ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| z-score : (x − moyenne)/écart-type (retenu) | 1.799 | 2.24 | -0.32 | 0.9955 | 1.3 |  |  |  | — choix retenu |
| Robuste : (x − médiane)/(Q3 − Q1) | 1.825 | 2.265 | -0.38 | 1.0265 | 1.8 | 0.0004 | 0.0004 | 0.0804 | moins bon |
| Min-max : (x − min)/(max − min) | 2.236 | 2.699 | -0.759 | 1.3458 | 0.8 | 0.0 | 0.0 | 0.0 | moins bon |
| Aucune mise à l'échelle | 2.104 | 2.587 | -0.497 | 1.2014 | 1.9 | 0.0 | 0.0 | 0.0001 | moins bon |


Plus petite MAE : **z-score : (x − moyenne)/écart-type (retenu)** (1.799). Aucune variante ne bat significativement le choix retenu (z-score : (x − moyenne)/écart-type (retenu)).



### D7 · Fenêtre d'entraînement

*Faut-il tout le passé, ou seulement les derniers mois ? (mesure aussi le coût d'un historique court)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Croissante (tout le passé) (retenu) | 1.941 | 2.361 | -0.495 | 0.6897 | 85.8 | 6.4 |  |  |  | — choix retenu |
| Glissante : 365 derniers jours | 1.952 | 2.369 | -0.474 | 0.6919 | 86.3 | 6.3 | 0.0889 | 0.1778 | 0.1525 | équivalent |
| Glissante : 180 derniers jours | 1.991 | 2.431 | -0.047 | 0.6591 | 83.6 | 7.8 | 0.142 | 0.1778 | 0.3732 | équivalent |
| Glissante : 90 derniers jours | 2.124 | 2.605 | -0.124 | 0.7661 | 75.4 | 7.9 | 0.0195 | 0.0585 | 0.0224 | équivalent |


Plus petite MAE : **Croissante (tout le passé) (retenu)** (1.941). Aucune variante ne bat significativement le choix retenu (Croissante (tout le passé) (retenu)).



### D8 · Optimisation

*Comment atteindre le minimum de J le plus sûrement ? (SVR RBF, un découpage)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | J final | pas effectués | arrêt | solution gardée | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Adam + Polyak + préconditionnement + décroissance η (retenu) | 2.01 | 2.459 | -0.878 | 1.2682 | 1.5 | 723.77 | 3000 | 3000 pas atteints | meilleur point rencontré |  |  |  | — choix retenu |
| Adam sans moyenne de Polyak | 2.01 | 2.459 | -0.878 | 1.2682 | 0.8 | 723.77 | 3000 | 3000 pas atteints | meilleur point rencontré |  |  |  | identique |
| Adam sans préconditionnement | 2.015 | 2.462 | -0.859 | 1.2649 | 0.7 | 736.18 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.5466 | 0.5466 | 0.549 | équivalent |
| Adam sans décroissance de η | 2.012 | 2.461 | -0.879 | 1.2696 | 0.5 | 723.87 | 2283 | J stable depuis 100 pas (pas 2282) | meilleur point rencontré | 0.0025 | 0.005 | 0.0038 | moins bon |
| Momentum | 2.676 | 3.239 | -1.119 | 1.6736 | 0.5 | 1237.84 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | 0.0 | moins bon |
| Descente de gradient simple | 3.102 | 3.77 | -2.316 | 2.2461 | 0.7 | 1229.03 | 3000 | 3000 pas atteints | moyenne de Polyak sur 1500 pas | 0.0 | 0.0 | 0.0 | moins bon |


Plus petite MAE : **Adam + Polyak + préconditionnement + décroissance η (retenu)** (2.01). Aucune variante ne bat significativement le choix retenu (Adam + Polyak + préconditionnement + décroissance η (retenu)).



### D9 · Combinaison des modèles

*Apprendre les poids de combinaison apporte-t-il plus qu'une moyenne ? (jours où l'empilement prédit)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Niveau 4 seul (meilleur modèle unique) | 1.985 | 2.417 | -0.68 | 0.6973 | 83.9 | 5.7 | 0.7006 | 1.0 | 0.378 | équivalent |
| Moyenne simple persistance + niv. 3 + niv. 4 | 1.836 | 2.338 | -0.498 | 0.7046 | 68.4 | 11.5 | 0.8426 | 1.0 | 0.2676 | équivalent |
| Empilement appris (poids positifs) (retenu) | 1.911 | 2.538 | -0.078 | 0.7128 | 76.8 | 26.8 |  |  |  | — choix retenu |
| XGBoost quantile seul | 1.868 | 2.348 | -0.517 | 0.7573 | 83.9 | 9.3 | 0.4261 | 1.0 | 0.6513 | équivalent |
| Moyenne SVR niv. 4 + XGBoost | 1.903 | 2.354 | -0.598 | 0.707 | 83.9 | 15.1 | 0.8974 | 1.0 | 0.9289 | équivalent |
| Empilement persistance + niv. 3 + niv. 4 + XGBoost | 1.906 | 2.53 | -0.072 | 0.7078 | 78.1 | 35.7 | 0.176 | 0.88 | 0.2978 | équivalent |


Plus petite MAE : **Moyenne simple persistance + niv. 3 + niv. 4** (1.836). Aucune variante ne bat significativement le choix retenu (Empilement appris (poids positifs) (retenu)).



### D13 · Variantes de SVM

*Quel SVM est le plus adapté à la série du service ? (mêmes jours, mêmes variables)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | cle | couverture 90 % | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SVR linéaire (niveau 1) | 1.762 | 2.225 | -0.28 | 0.9647 | 1.1 | svr_lineaire |  | 0.0 | 0.0 | 0.0001 | moins bon |
| SVR RBF (niveau 2) | 1.799 | 2.24 | -0.32 | 0.9955 | 0.8 | svr_rbf |  | 0.0 | 0.0 | 0.0002 | moins bon |
| SVR quantile RBF (niveau 3) | 1.915 | 2.363 | -0.585 | 0.6838 | 2.3 | svr_q_rbf | 88.5 | 0.664 | 0.664 | 0.4997 | équivalent |
| SVR quantile composite (niveau 4, retenu) (retenu) | 1.941 | 2.361 | -0.495 | 0.6897 | 3.4 | svr_q_composite | 85.8 |  |  |  | — choix retenu |
| SVR quantile, noyau laplacien | 2.003 | 2.423 | -0.485 | 0.7176 | 2.7 | svr_q_laplacien | 88.5 | 0.1634 | 0.3268 | 0.2427 | équivalent |
| SVR quantile, noyau polynomial (degré 2) | 1.726 | 2.214 | -0.447 | 0.6449 | 4.5 | svr_q_polynomial | 81.4 | 0.091 | 0.273 | 0.0 | équivalent |
| LS-SVR (moindres carrés), noyau RBF, quantiles LOO | 1.811 | 2.259 | -0.458 | 0.5902 | 0.2 | lssvr_rbf | 92.9 | 0.0005 | 0.002 | 0.0002 | meilleur |


Plus petite MAE : **SVR quantile, noyau polynomial (degré 2)** (1.726). ⚠ Significativement meilleur que le choix retenu : LS-SVR (moindres carrés), noyau RBF, quantiles LOO — le choix est à revoir.



### D11 · Chaque variable, une à une

*Que perd le modèle si on lui retire cette seule variable ? (modèle RBF du niveau 2, mêmes jours)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 1.799 | 2.24 | -0.32 | 0.9955 | 1.5 |  |  |  | — choix retenu |
| Sans occ_j-0 | 2.087 | 2.514 | -0.631 | 1.2327 | 1.3 | 0.0 | 0.0 | 0.0 | moins bon |
| Sans occ_j-1 | 1.791 | 2.24 | -0.341 | 0.9979 | 1.6 | 0.6471 | 1.0 | 0.412 | équivalent |
| Sans occ_j-2 | 1.788 | 2.239 | -0.279 | 0.9775 | 1.9 | 0.0287 | 0.3731 | 0.4274 | équivalent |
| Sans occ_j-3 | 1.788 | 2.253 | -0.285 | 0.9797 | 1.6 | 0.0749 | 0.8239 | 0.462 | équivalent |
| Sans occ_j-4 | 1.787 | 2.239 | -0.36 | 1.0018 | 1.6 | 0.4801 | 1.0 | 0.4258 | équivalent |
| Sans occ_j-5 | 1.789 | 2.233 | -0.32 | 0.9908 | 1.6 | 0.1423 | 1.0 | 0.0645 | équivalent |
| Sans occ_j-6 | 1.833 | 2.273 | -0.378 | 1.0296 | 1.3 | 0.0 | 0.0 | 0.005 | moins bon |
| Sans adm_3j | 1.781 | 2.237 | -0.32 | 0.9865 | 1.6 | 0.3802 | 1.0 | 0.3163 | équivalent |
| Sans adm_7j | 1.815 | 2.263 | -0.354 | 1.0136 | 1.7 | 0.0545 | 0.654 | 0.3277 | équivalent |
| Sans sorties_7j | 1.787 | 2.221 | -0.272 | 0.9749 | 1.9 | 0.0107 | 0.1498 | 0.342 | équivalent |
| Sans cible_jour_0 | 1.811 | 2.25 | -0.295 | 0.9939 | 1.3 | 0.8027 | 1.0 | 0.3034 | équivalent |
| Sans cible_jour_1 | 1.822 | 2.28 | -0.373 | 1.0228 | 1.4 | 0.0075 | 0.1125 | 0.1558 | équivalent |
| Sans cible_jour_2 | 1.806 | 2.245 | -0.324 | 1.0 | 1.7 | 0.2967 | 1.0 | 0.3043 | équivalent |
| Sans cible_jour_3 | 1.795 | 2.236 | -0.323 | 0.9941 | 1.4 | 0.5026 | 1.0 | 0.1931 | équivalent |
| Sans cible_jour_4 | 1.816 | 2.263 | -0.337 | 1.009 | 1.0 | 0.0009 | 0.0153 | 0.0127 | moins bon |
| Sans cible_jour_5 | 1.791 | 2.242 | -0.318 | 0.9908 | 1.2 | 0.3467 | 1.0 | 0.3249 | équivalent |
| Sans cible_jour_6 | 1.795 | 2.236 | -0.334 | 0.9979 | 0.8 | 0.376 | 1.0 | 0.4438 | équivalent |
| Sans mois_sin | 1.83 | 2.276 | -0.314 | 1.0092 | 0.9 | 0.2221 | 1.0 | 0.0996 | équivalent |
| Sans mois_cos | 1.801 | 2.248 | -0.415 | 1.0248 | 0.9 | 0.0028 | 0.0448 | 0.927 | moins bon |


Plus petite MAE : **Sans adm_3j** (1.781). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)).



### D14 · Sélection des variables par le lasso

*Le modèle gagne-t-il à ne garder que les variables choisies par le lasso ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 1.799 | 2.24 | -0.32 | 0.9955 | 0.9 | 19.0 |  |  |  | — choix retenu |
| Lasso, λ de plus petite erreur | 1.778 | 2.268 | -0.327 | 0.9874 | 13.8 | 12.1 | 0.5954 | 0.5954 | 0.4391 | équivalent |
| Lasso à un écart-type (λ_1se) | 1.836 | 2.303 | -0.431 | 1.0473 | 15.0 | 2.4 | 0.0769 | 0.1538 | 0.39 | équivalent |


Plus petite MAE : **Lasso, λ de plus petite erreur** (1.778). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)).



## Horizon J+7 — 177 jours évalués, 7 origines


### D1 · Modèles de référence, concurrents et SVR

*Le SVR fait-il mieux que les méthodes statistiques usuelles et que les autres modèles d'apprentissage ?*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | couverture 90 % | réglages | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Persistance | 2.933 | 3.67 | -0.02 | 1.4725 | 0.0 |  |  | 0.0047 | 0.0893 | 0.4096 | équivalent |
| Saisonnière hebdomadaire | 2.569 | 3.09 | 0.034 | 1.2745 | 0.0 |  |  | 0.0561 | 0.9316 | 0.4977 | équivalent |
| Moyenne mobile 7 j | 2.692 | 3.299 | 0.037 | 1.3348 | 0.0 |  |  | 0.0883 | 1.0 | 0.93 | équivalent |
| Moyenne historique | 2.88 | 3.48 | -1.619 | 0.8663 | 0.0 | 88.7 |  | 0.3176 | 1.0 | 0.1604 | équivalent |
| Lissage exponentiel simple | 2.911 | 3.636 | -0.018 | 1.0583 | 0.0 | 92.7 |  | 0.2184 | 1.0 | 0.4587 | équivalent |
| Méthode Thêta | 2.915 | 3.636 | 0.041 | 1.0583 | 0.0 | 92.7 |  | 0.2186 | 1.0 | 0.4485 | équivalent |
| Holt linéaire | 2.911 | 3.637 | -0.017 | 1.0587 | 0.1 | 92.7 |  | 0.2159 | 1.0 | 0.4592 | équivalent |
| Holt amorti | 2.911 | 3.636 | -0.018 | 1.0583 | 0.1 | 92.7 |  | 0.2184 | 1.0 | 0.4587 | équivalent |
| Lissage saisonnier sans tendance | 2.912 | 3.639 | -0.018 | 1.0613 | 0.1 | 92.7 |  | 0.205 | 1.0 | 0.4566 | équivalent |
| Holt-Winters additif amorti | 2.933 | 3.67 | -0.02 | 1.0731 | 0.1 | 93.2 |  | 0.1639 | 1.0 | 0.4096 | équivalent |
| Holt-Winters multiplicatif amorti | 2.933 | 3.67 | -0.02 | 1.0731 | 0.0 | 93.2 |  | 0.1639 | 1.0 | 0.4096 | équivalent |
| AR(p) par AIC | 2.622 | 3.095 | -0.776 | 0.8259 | 0.1 | 96.0 |  | 0.0668 | 1.0 | 0.2002 | équivalent |
| SARIMA(1,0,0)(1,0,0)7 (ordre choisi sur l'apprentissage) | 2.672 | 3.178 | -1.069 | 0.8509 | 4.4 | 93.8 |  | 0.0695 | 1.0 | 0.4606 | équivalent |
| Holt-Winters additif, grille fixée avant la validation | 2.541 | 3.076 | 0.029 | 1.2618 | 0.1 |  | alpha=0.1, beta=0.0, gamma=0.05, phi=0.8 | 0.0869 | 1.0 | 0.4775 | équivalent |
| Régression ridge (λ = 1) | 3.004 | 3.632 | -1.404 | 1.9233 | 0.2 |  |  | 0.0001 | 0.0023 | 0.0456 | moins bon |
| A · forêt aléatoire quantile | 2.691 | 3.236 | -1.059 | 0.9587 | 11.6 | 91.0 |  | 0.7914 | 1.0 | 0.8202 | équivalent |
| B · gradient boosting quantile | 2.817 | 3.386 | -1.163 | 1.2069 | 6.9 | 67.2 |  | 0.0291 | 0.5238 | 0.5542 | équivalent |
| C · perceptron multicouche quantile | 3.087 | 3.692 | -1.262 | 1.0586 | 1.2 | 79.1 |  | 0.0696 | 1.0 | 0.0001 | équivalent |
| D · LSTM quantile | 3.291 | 3.911 | -1.708 | 1.196 | 8.3 | 70.6 |  | 0.0031 | 0.062 | 0.0 | équivalent |
| E · XGBoost quantile (second ordre) | 2.844 | 3.374 | -1.193 | 1.1802 | 12.8 | 75.7 |  | 0.0548 | 0.9316 | 0.4076 | équivalent |
| SVR linéaire (niveau 1) | 2.938 | 3.526 | -1.162 | 1.8176 | 0.8 |  |  | 0.0001 | 0.0023 | 0.0238 | moins bon |
| SVR RBF (niveau 2) | 2.682 | 3.188 | -1.044 | 1.6544 | 1.6 |  |  | 0.0001 | 0.0023 | 0.6899 | moins bon |
| SVR quantile RBF (niveau 3) | 2.744 | 3.281 | -0.978 | 0.9401 | 3.1 | 88.7 |  | 0.538 | 1.0 | 0.1649 | équivalent |
| SVR quantile composite (niveau 4) (retenu) | 2.719 | 3.246 | -0.904 | 0.9447 | 6.1 | 87.6 |  |  |  |  | — choix retenu |


Plus petite MAE : **Holt-Winters additif, grille fixée avant la validation** (2.541). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4) (retenu)).



### D2 · Noyau

*Quel noyau décrit le mieux la dynamique ? (même perte ε-insensible, même C)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Linéaire | 3.051 | 3.71 | -1.363 | 1.9347 | 1.1 | 0.0176 | 0.0352 | 0.0054 | moins bon |
| RBF (γ = 0.05) | 2.682 | 3.188 | -1.044 | 1.6544 | 1.8 | 0.974 | 0.974 | 0.6833 | équivalent |
| Composite occupation / flux et saison (β appris) (retenu) | 2.661 | 3.208 | -1.086 | 1.6562 | 3.1 |  |  |  | — choix retenu |


Plus petite MAE : **Composite occupation / flux et saison (β appris) (retenu)** (2.661). Aucune variante ne bat significativement le choix retenu (Composite occupation / flux et saison (β appris) (retenu)).



### D3 · Fonction de perte

*Quelle perte pour un modèle linéaire identique ? (isole l'effet de la perte)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Carrée (ridge, λ = 1/C) | 2.988 | 3.604 | -1.379 | 1.9079 | 0.2 | 0.0018 | 0.0072 | 0.4664 | moins bon |
| ε-insensible, ε = 0 lit (= valeur absolue) | 2.985 | 3.608 | -1.211 | 1.8556 | 1.3 | 0.6234 | 0.7866 | 0.5975 | équivalent |
| ε-insensible, ε = 0.5 lit | 2.986 | 3.597 | -1.19 | 1.85 | 0.9 | 0.3933 | 0.7866 | 0.2886 | équivalent |
| ε-insensible, ε = 1 lit (retenu) | 2.938 | 3.526 | -1.162 | 1.8176 | 0.9 |  |  |  | — choix retenu |
| ε-insensible, ε = 2 lit | 3.022 | 3.609 | -1.235 | 1.8812 | 1.2 | 0.1763 | 0.5289 | 0.128 | équivalent |


Plus petite MAE : **ε-insensible, ε = 1 lit (retenu)** (2.938). Aucune variante ne bat significativement le choix retenu (ε-insensible, ε = 1 lit (retenu)).



### D4 · Quantile décisionnel τ et coût des décisions

*Quel τ minimise le coût réel selon le rapport pénurie / lit vide ? (τ optimal théorique = r/(1+r))*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | jours sous-estimés % | lits prévus en moyenne | coût r=1 | coût r=2 | coût r=4 | coût r=9 | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| τ = 0.5 | 2.744 | 3.281 | -0.978 | 1.6654 | 0.6 | 60.5 | 9.91 | 2.744 | 4.605 | 8.327 | 17.632 | 0.0003 | 0.0012 | 0.7165 | moins bon |
| τ = 0.6 | 2.661 | 3.134 | -0.281 | 1.4149 | 0.8 | 54.2 | 10.61 | 2.661 | 4.132 | 7.074 | 14.43 | 0.002 | 0.006 | 0.4593 | moins bon |
| τ = 0.7 | 2.726 | 3.282 | 0.749 | 1.1382 | 0.7 | 45.8 | 11.64 | 2.726 | 3.714 | 5.691 | 10.634 | 0.0087 | 0.0174 | 0.2341 | moins bon |
| τ = 0.8 (retenu) | 2.892 | 3.568 | 1.687 | 0.9401 | 0.8 | 33.3 | 12.58 | 2.892 | 3.495 | 4.701 | 7.715 |  |  |  | — choix retenu |
| τ = 0.9 | 3.682 | 4.527 | 3.287 | 0.8548 | 1.1 | 16.9 | 14.18 | 3.682 | 3.879 | 4.274 | 5.262 | 0.389 | 0.389 | 0.0 | équivalent |


τ le moins coûteux pour chaque rapport de coûts r = c_pénurie / c_lit vide : r = 1 → τ = 0.6, r = 2 → τ = 0.8 (retenu), r = 4 → τ = 0.9, r = 9 → τ = 0.9. Le choix τ = 0.8 correspond à r = 4.


### D5 · Variables d'entrée

*Que rapporte chaque groupe de variables ? (même modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| 7 retards seuls | 2.77 | 3.279 | -1.165 | 1.7343 | 1.0 | 7 | 0.3701 | 1.0 | 0.4309 | équivalent |
| 7 retards + flux | 2.795 | 3.328 | -1.382 | 1.812 | 1.1 | 10 | 0.0801 | 0.6408 | 0.3333 | équivalent |
| 7 retards + calendrier (jour, mois) | 2.685 | 3.168 | -0.848 | 1.5967 | 1.9 | 16 | 0.4974 | 1.0 | 0.9842 | équivalent |
| Complet : retards + flux + calendrier (retenu) | 2.682 | 3.188 | -1.044 | 1.6544 | 1.4 | 19 |  |  |  | — choix retenu |
| Complet + jours fériés camerounais | 2.691 | 3.204 | -1.079 | 1.6693 | 1.1 | 21 | 0.0016 | 0.0144 | 0.2027 | moins bon |
| Complet + vacances scolaires | 2.728 | 3.236 | -1.057 | 1.6811 | 1.7 | 20 | 0.3864 | 1.0 | 0.2218 | équivalent |
| Complet + fériés + vacances scolaires | 2.734 | 3.249 | -1.087 | 1.6929 | 1.4 | 22 | 0.2411 | 1.0 | 0.2035 | équivalent |
| 3 retards + flux + calendrier | 2.655 | 3.196 | -1.1 | 1.6576 | 1.0 | 15 | 0.928 | 1.0 | 0.511 | équivalent |
| 14 retards + flux + calendrier | 2.701 | 3.245 | -0.863 | 1.6091 | 1.2 | 26 | 0.3914 | 1.0 | 0.8126 | équivalent |
| Complet + diagnostics d'entrée des présents | 2.778 | 3.31 | -0.841 | 1.6412 | 1.9 | 30 | 0.9008 | 1.0 | 0.387 | équivalent |


Plus petite MAE : **3 retards + flux + calendrier** (2.655). Aucune variante ne bat significativement le choix retenu (Complet : retards + flux + calendrier (retenu)).



### D6 · Prétraitement

*Quelle mise à l'échelle des variables ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| z-score : (x − moyenne)/écart-type (retenu) | 2.682 | 3.188 | -1.044 | 1.6544 | 1.1 |  |  |  | — choix retenu |
| Robuste : (x − médiane)/(Q3 − Q1) | 2.845 | 3.403 | -1.169 | 1.773 | 1.6 | 0.0152 | 0.0456 | 0.0036 | moins bon |
| Min-max : (x − min)/(max − min) | 2.756 | 3.329 | -0.988 | 1.6745 | 0.7 | 0.8136 | 1.0 | 0.4586 | équivalent |
| Aucune mise à l'échelle | 2.705 | 3.229 | -1.199 | 1.7124 | 1.6 | 0.559 | 1.0 | 0.8522 | équivalent |


Plus petite MAE : **z-score : (x − moyenne)/écart-type (retenu)** (2.682). Aucune variante ne bat significativement le choix retenu (z-score : (x − moyenne)/écart-type (retenu)).



### D7 · Fenêtre d'entraînement

*Faut-il tout le passé, ou seulement les derniers mois ? (mesure aussi le coût d'un historique court)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Croissante (tout le passé) (retenu) | 2.719 | 3.246 | -0.904 | 0.9447 | 87.6 | 6.9 |  |  |  | — choix retenu |
| Glissante : 365 derniers jours | 2.72 | 3.246 | -0.904 | 0.9458 | 87.6 | 4.4 | 0.3042 | 0.9126 | 0.3157 | équivalent |
| Glissante : 180 derniers jours | 2.649 | 3.142 | -0.427 | 0.9206 | 89.3 | 7.9 | 0.3335 | 0.9126 | 0.4467 | équivalent |
| Glissante : 90 derniers jours | 2.862 | 3.423 | -0.14 | 0.9678 | 81.9 | 5.1 | 0.542 | 0.9126 | 0.4484 | équivalent |


Plus petite MAE : **Glissante : 180 derniers jours** (2.649). Aucune variante ne bat significativement le choix retenu (Croissante (tout le passé) (retenu)).



### D8 · Optimisation

*Comment atteindre le minimum de J le plus sûrement ? (SVR RBF, un découpage)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | J final | pas effectués | arrêt | solution gardée | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Adam + Polyak + préconditionnement + décroissance η (retenu) | 3.545 | 4.27 | -2.801 | 2.6127 | 0.7 | 1125.19 | 1599 | J stable depuis 100 pas (pas 1598) | moyenne de Polyak sur 98 pas |  |  |  | — choix retenu |
| Adam sans moyenne de Polyak | 3.541 | 4.266 | -2.796 | 2.6092 | 0.3 | 1125.19 | 1599 | J stable depuis 100 pas (pas 1598) | meilleur point rencontré | 0.0 | 0.0 | 0.0 | meilleur |
| Adam sans préconditionnement | 3.491 | 4.209 | -2.716 | 2.5604 | 0.8 | 1139.14 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | 0.0025 | meilleur |
| Adam sans décroissance de η | 3.542 | 4.268 | -2.798 | 2.6105 | 0.7 | 1125.33 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0029 | 0.0029 | 0.0015 | meilleur |
| Momentum | 2.717 | 3.266 | -1.085 | 1.6841 | 0.5 | 1383.59 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | 0.0002 | meilleur |
| Descente de gradient simple | 2.717 | 3.266 | -1.085 | 1.6841 | 0.4 | 1383.59 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | 0.0002 | meilleur |


Plus petite MAE : **Momentum** (2.717). ⚠ Significativement meilleur que le choix retenu : Adam sans moyenne de Polyak, Adam sans préconditionnement, Adam sans décroissance de η, Momentum, Descente de gradient simple — le choix est à revoir.



### D9 · Combinaison des modèles

*Apprendre les poids de combinaison apporte-t-il plus qu'une moyenne ? (jours où l'empilement prédit)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Niveau 4 seul (meilleur modèle unique) | 2.699 | 3.227 | -1.374 | 0.936 | 88.6 | 5.1 | 0.4174 | 1.0 | 0.7101 | équivalent |
| Moyenne simple persistance + niv. 3 + niv. 4 | 2.546 | 3.01 | -0.954 | 0.9678 | 70.5 | 10.2 | 0.6044 | 1.0 | 0.1674 | équivalent |
| Empilement appris (poids positifs) (retenu) | 2.778 | 3.317 | -0.783 | 1.0295 | 91.3 | 21.8 |  |  |  | — choix retenu |
| XGBoost quantile seul | 2.907 | 3.449 | -1.519 | 1.2333 | 77.2 | 14.1 | 0.3409 | 1.0 | 0.5883 | équivalent |
| Moyenne SVR niv. 4 + XGBoost | 2.754 | 3.278 | -1.447 | 1.0546 | 82.6 | 19.2 | 0.8746 | 1.0 | 0.9089 | équivalent |
| Empilement persistance + niv. 3 + niv. 4 + XGBoost | 2.863 | 3.484 | -0.221 | 1.0256 | 91.3 | 39.3 | 0.9443 | 1.0 | 0.0 | équivalent |


Plus petite MAE : **Moyenne simple persistance + niv. 3 + niv. 4** (2.546). Aucune variante ne bat significativement le choix retenu (Empilement appris (poids positifs) (retenu)).



### D13 · Variantes de SVM

*Quel SVM est le plus adapté à la série du service ? (mêmes jours, mêmes variables)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | cle | couverture 90 % | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SVR linéaire (niveau 1) | 2.938 | 3.526 | -1.162 | 1.8176 | 1.5 | svr_lineaire |  | 0.0001 | 0.0006 | 0.0238 | moins bon |
| SVR RBF (niveau 2) | 2.682 | 3.188 | -1.044 | 1.6544 | 1.8 | svr_rbf |  | 0.0001 | 0.0006 | 0.6899 | moins bon |
| SVR quantile RBF (niveau 3) | 2.744 | 3.281 | -0.978 | 0.9401 | 2.9 | svr_q_rbf | 88.7 | 0.538 | 1.0 | 0.1649 | équivalent |
| SVR quantile composite (niveau 4, retenu) (retenu) | 2.719 | 3.246 | -0.904 | 0.9447 | 5.9 | svr_q_composite | 87.6 |  |  |  | — choix retenu |
| SVR quantile, noyau laplacien | 2.707 | 3.24 | -0.978 | 0.9274 | 4.0 | svr_q_laplacien | 88.1 | 0.189 | 0.756 | 0.7106 | équivalent |
| SVR quantile, noyau polynomial (degré 2) | 2.789 | 3.333 | -1.026 | 0.954 | 5.5 | svr_q_polynomial | 87.6 | 0.6129 | 1.0 | 0.011 | équivalent |
| LS-SVR (moindres carrés), noyau RBF, quantiles LOO | 2.659 | 3.23 | -1.254 | 0.935 | 0.3 | lssvr_rbf | 88.1 | 0.7618 | 1.0 | 0.6842 | équivalent |


Plus petite MAE : **LS-SVR (moindres carrés), noyau RBF, quantiles LOO** (2.659). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4, retenu) (retenu)).



### D11 · Chaque variable, une à une

*Que perd le modèle si on lui retire cette seule variable ? (modèle RBF du niveau 2, mêmes jours)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 2.682 | 3.188 | -1.044 | 1.6544 | 1.8 |  |  |  | — choix retenu |
| Sans occ_j-0 | 2.705 | 3.232 | -1.092 | 1.6802 | 1.0 | 0.2187 | 1.0 | 0.3307 | équivalent |
| Sans occ_j-1 | 2.655 | 3.171 | -1.001 | 1.6278 | 1.8 | 0.1066 | 1.0 | 0.2593 | équivalent |
| Sans occ_j-2 | 2.67 | 3.175 | -1.019 | 1.6407 | 1.5 | 0.4648 | 1.0 | 0.6077 | équivalent |
| Sans occ_j-3 | 2.682 | 3.202 | -1.02 | 1.6472 | 1.7 | 0.6362 | 1.0 | 0.9987 | équivalent |
| Sans occ_j-4 | 2.659 | 3.163 | -1.036 | 1.6403 | 1.8 | 0.101 | 1.0 | 0.1261 | équivalent |
| Sans occ_j-5 | 2.671 | 3.169 | -1.018 | 1.641 | 2.0 | 0.1601 | 1.0 | 0.4287 | équivalent |
| Sans occ_j-6 | 2.685 | 3.2 | -1.047 | 1.6564 | 1.8 | 0.8883 | 1.0 | 0.892 | équivalent |
| Sans adm_3j | 2.678 | 3.2 | -1.075 | 1.6614 | 1.9 | 0.4938 | 1.0 | 0.8056 | équivalent |
| Sans adm_7j | 2.713 | 3.214 | -1.035 | 1.6672 | 2.1 | 0.6986 | 1.0 | 0.5006 | équivalent |
| Sans sorties_7j | 2.677 | 3.163 | -0.879 | 1.6024 | 1.7 | 0.2383 | 1.0 | 0.9407 | équivalent |
| Sans cible_jour_0 | 2.674 | 3.168 | -1.012 | 1.6406 | 1.7 | 0.1896 | 1.0 | 0.7107 | équivalent |
| Sans cible_jour_1 | 2.676 | 3.181 | -1.031 | 1.6472 | 1.9 | 0.029 | 0.522 | 0.2556 | équivalent |
| Sans cible_jour_2 | 2.67 | 3.174 | -1.001 | 1.6354 | 1.9 | 0.1175 | 1.0 | 0.4378 | équivalent |
| Sans cible_jour_3 | 2.679 | 3.193 | -1.066 | 1.659 | 1.5 | 0.3886 | 1.0 | 0.7656 | équivalent |
| Sans cible_jour_4 | 2.671 | 3.177 | -1.004 | 1.6368 | 1.7 | 0.1151 | 1.0 | 0.4703 | équivalent |
| Sans cible_jour_5 | 2.684 | 3.194 | -1.058 | 1.6595 | 1.6 | 0.2609 | 1.0 | 0.7398 | équivalent |
| Sans cible_jour_6 | 2.663 | 3.167 | -1.032 | 1.641 | 1.3 | 0.0087 | 0.1653 | 0.0162 | équivalent |
| Sans mois_sin | 2.845 | 3.387 | -1.067 | 1.7424 | 1.9 | 0.1838 | 1.0 | 0.0908 | équivalent |
| Sans mois_cos | 2.76 | 3.33 | -1.389 | 1.7969 | 1.7 | 0.1566 | 1.0 | 0.4605 | équivalent |


Plus petite MAE : **Sans occ_j-1** (2.655). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)).



### D14 · Sélection des variables par le lasso

*Le modèle gagne-t-il à ne garder que les variables choisies par le lasso ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 2.682 | 3.188 | -1.044 | 1.6544 | 1.7 | 19.0 |  |  |  | — choix retenu |
| Lasso, λ de plus petite erreur | 2.724 | 3.302 | -1.134 | 1.7021 | 21.5 | 3.0 | 0.6427 | 1.0 | 0.7063 | équivalent |
| Lasso à un écart-type (λ_1se) | 2.729 | 3.296 | -1.165 | 1.7139 | 19.6 | 1.0 | 0.5505 | 1.0 | 0.6583 | équivalent |


Plus petite MAE : **Toutes les variables (retenu)** (2.682). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)).

