# Banc de comparaison des choix — service MEDF_pic

Validation glissante du 01/03/2026 au verrou (01/09/2026), une origine tous les 28 jours, modèle réentraîné à chaque origine. « (retenu) » = choix retenu. Test de Diebold-Mariano (perte absolue, correction HLN) contre le choix retenu.


## Horizon J+1 — 183 jours évalués, 7 origines


### D1 · Modèles de référence, concurrents et SVR

*Le SVR fait-il mieux que les méthodes statistiques usuelles et que les autres modèles d'apprentissage ?*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | couverture 90 % | réglages | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Persistance | 1.29 | 1.876 | -0.004 | 0.6461 | 0.0 |  |  | 0.015 | 0.2235 | équivalent |
| Saisonnière hebdomadaire | 2.357 | 2.92 | 0.018 | 1.1733 | 0.0 |  |  | 0.0 | 0.0 | moins bon |
| Moyenne mobile 7 j | 1.979 | 2.482 | -0.001 | 0.9898 | 0.0 |  |  | 0.0 | 0.0 | moins bon |
| Moyenne historique | 2.787 | 3.333 | -1.636 | 0.8122 | 0.0 | 90.7 |  | 0.0 | 0.0 | moins bon |
| Lissage exponentiel simple | 1.29 | 1.876 | -0.004 | 0.4994 | 0.0 | 90.7 |  | 0.4447 | 1.0 | équivalent |
| Méthode Thêta | 1.29 | 1.876 | 0.005 | 0.4994 | 0.0 | 90.7 |  | 0.4447 | 1.0 | équivalent |
| Holt linéaire | 1.29 | 1.876 | -0.004 | 0.4994 | 0.0 | 90.7 |  | 0.4447 | 1.0 | équivalent |
| Holt amorti | 1.29 | 1.876 | -0.004 | 0.4994 | 0.0 | 90.7 |  | 0.4447 | 1.0 | équivalent |
| Lissage saisonnier sans tendance | 1.29 | 1.876 | -0.004 | 0.4994 | 0.0 | 90.7 |  | 0.4447 | 1.0 | équivalent |
| Holt-Winters additif amorti | 1.29 | 1.876 | -0.004 | 0.4994 | 0.1 | 90.7 |  | 0.4447 | 1.0 | équivalent |
| Holt-Winters multiplicatif amorti | 1.29 | 1.876 | -0.004 | 0.4994 | 0.0 | 90.7 |  | 0.4447 | 1.0 | équivalent |
| AR(p) par AIC | 1.298 | 1.752 | -0.153 | 0.4767 | 0.1 | 89.1 |  | 0.1504 | 1.0 | équivalent |
| SARIMA(2,0,0)(1,0,0)7 (ordre choisi sur l'apprentissage) | 1.278 | 1.714 | -0.258 | 0.4482 | 4.9 | 89.6 |  | 0.0103 | 0.1751 | équivalent |
| Holt-Winters additif, grille fixée avant la validation | 1.286 | 1.854 | -0.002 | 0.6435 | 0.1 |  | alpha=0.9, beta=0.0, gamma=0.05, phi=0.8 | 0.0139 | 0.2224 | équivalent |
| Régression ridge (λ = 1) | 1.264 | 1.587 | -0.403 | 0.7529 | 0.1 |  |  | 0.0 | 0.0 | moins bon |
| A · forêt aléatoire quantile | 1.431 | 1.816 | -0.285 | 0.5017 | 9.9 | 94.0 |  | 0.3168 | 1.0 | équivalent |
| B · gradient boosting quantile | 1.34 | 1.759 | -0.323 | 0.5542 | 9.1 | 71.0 |  | 0.3302 | 1.0 | équivalent |
| C · perceptron multicouche quantile | 1.675 | 2.004 | -0.91 | 0.5466 | 1.0 | 84.7 |  | 0.5148 | 1.0 | équivalent |
| D · LSTM quantile | 1.413 | 1.769 | -0.528 | 0.5125 | 8.6 | 75.4 |  | 0.6244 | 1.0 | équivalent |
| E · XGBoost quantile (second ordre) | 1.437 | 1.81 | -0.379 | 0.5895 | 9.0 | 84.2 |  | 0.0149 | 0.2235 | équivalent |
| SVR linéaire (niveau 1) | 1.236 | 1.589 | -0.358 | 0.7253 | 0.7 |  |  | 0.0 | 0.0 | moins bon |
| SVR RBF (niveau 2) | 1.341 | 1.708 | -0.406 | 0.7926 | 1.4 |  |  | 0.0 | 0.0 | moins bon |
| SVR quantile RBF (niveau 3) | 1.423 | 1.772 | -0.501 | 0.5302 | 4.7 | 85.8 |  | 0.7263 | 1.0 | équivalent |
| SVR quantile composite (niveau 4) (retenu) | 1.399 | 1.782 | -0.38 | 0.5262 | 6.7 | 85.2 |  |  |  | — choix retenu |


Plus petite perte pinball à τ = 0.8 : **SARIMA(2,0,0)(1,0,0)7 (ordre choisi sur l'apprentissage)** (0.4482). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4) (retenu)) après correction de Holm.



### D2 · Noyau

*Quel noyau décrit le mieux la dynamique ? (même perte ε-insensible, même C)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Linéaire | 1.222 | 1.569 | -0.348 | 0.7155 | 0.8 | 0.0153 | 0.0306 | meilleur |
| RBF (γ = 0.02) | 1.341 | 1.708 | -0.406 | 0.7926 | 1.4 | 0.8534 | 0.8534 | équivalent |
| Composite occupation / flux et saison (β appris) (retenu) | 1.366 | 1.753 | -0.354 | 0.7891 | 2.1 |  |  | — choix retenu |


Plus petite perte pinball à τ = 0.8 : **Linéaire** (0.7155). ⚠ Significativement meilleur que le choix retenu (Holm, 5 %) : Linéaire — le choix est à revoir.



### D3 · Fonction de perte

*Quelle perte pour un modèle linéaire identique ? (isole l'effet de la perte)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Carrée (ridge, λ = 1/C) | 1.265 | 1.591 | -0.415 | 0.7568 | 0.1 | 0.0044 | 0.0088 | moins bon |
| ε-insensible, ε = 0 lit (= valeur absolue) | 1.237 | 1.603 | -0.359 | 0.7264 | 0.8 | 0.9188 | 0.9188 | équivalent |
| ε-insensible, ε = 0.5 lit (retenu) | 1.236 | 1.589 | -0.358 | 0.7253 | 0.7 |  |  | — choix retenu |
| ε-insensible, ε = 1 lit | 1.295 | 1.635 | -0.475 | 0.79 | 0.7 | 0.0 | 0.0 | moins bon |
| ε-insensible, ε = 2 lit | 1.394 | 1.696 | -0.655 | 0.8937 | 1.1 | 0.0 | 0.0 | moins bon |


Plus petite perte pinball à τ = 0.8 : **ε-insensible, ε = 0.5 lit (retenu)** (0.7253). Aucune variante ne bat significativement le choix retenu (ε-insensible, ε = 0.5 lit (retenu)) après correction de Holm.



### D4 · Quantile décisionnel τ et coût des décisions

*Quel τ minimise le coût réel selon le rapport pénurie / lit vide ? (τ optimal théorique = r/(1+r))*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | jours sous-estimés % | lits prévus en moyenne | coût r=1 | coût r=2 | coût r=4 | coût r=9 | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| τ = 0.5 | 1.423 | 1.772 | -0.501 | 0.8619 | 0.9 | 63.4 | 11.76 | 1.423 | 2.385 | 4.309 | 9.12 | 0.0 | 0.0 | moins bon |
| τ = 0.6 | 1.393 | 1.78 | 0.007 | 0.6943 | 1.3 | 52.5 | 12.26 | 1.393 | 2.086 | 3.471 | 6.936 | 0.0 | 0.0 | moins bon |
| τ = 0.7 | 1.424 | 1.848 | 0.41 | 0.5891 | 1.2 | 45.9 | 12.67 | 1.424 | 1.931 | 2.945 | 5.48 | 0.0021 | 0.0042 | moins bon |
| τ = 0.8 (retenu) | 1.586 | 2.046 | 0.876 | 0.5302 | 1.2 | 32.2 | 13.13 | 1.586 | 1.941 | 2.651 | 4.427 |  |  | — choix retenu |
| τ = 0.9 | 2.054 | 2.615 | 1.743 | 0.5042 | 1.3 | 21.3 | 14.0 | 2.054 | 2.21 | 2.521 | 3.3 | 0.3346 | 0.3346 | équivalent |


τ le moins coûteux pour chaque rapport de coûts r = c_pénurie / c_lit vide : r = 1 → τ = 0.6, r = 2 → τ = 0.7, r = 4 → τ = 0.9, r = 9 → τ = 0.9. Le choix τ = 0.8 correspond à r = 4.


### D5 · Variables d'entrée

*Que rapporte chaque groupe de variables ? (même modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| 7 retards seuls | 1.321 | 1.786 | -0.252 | 0.7362 | 0.8 | 7 | 0.0452 | 0.1808 | équivalent |
| 7 retards + flux | 1.392 | 1.786 | -0.545 | 0.8596 | 1.1 | 10 | 0.002 | 0.016 | moins bon |
| 7 retards + calendrier (jour, mois) | 1.352 | 1.791 | -0.245 | 0.7494 | 0.8 | 16 | 0.0764 | 0.2292 | équivalent |
| Complet : retards + flux + calendrier (retenu) | 1.341 | 1.708 | -0.406 | 0.7926 | 1.4 | 19 |  |  | — choix retenu |
| Complet + jours fériés camerounais | 1.35 | 1.72 | -0.408 | 0.7977 | 1.4 | 21 | 0.0868 | 0.2292 | équivalent |
| Complet + vacances scolaires | 1.359 | 1.73 | -0.413 | 0.8033 | 1.4 | 20 | 0.0091 | 0.0455 | moins bon |
| Complet + fériés + vacances scolaires | 1.369 | 1.743 | -0.413 | 0.8084 | 1.4 | 22 | 0.0031 | 0.0217 | moins bon |
| 3 retards + flux + calendrier | 1.383 | 1.761 | -0.461 | 0.8299 | 1.1 | 15 | 0.0065 | 0.039 | moins bon |
| 14 retards + flux + calendrier | 1.391 | 1.766 | -0.38 | 0.8096 | 1.4 | 26 | 0.2698 | 0.2698 | équivalent |
| Complet + diagnostics d'entrée des présents | 1.536 | 1.934 | -0.612 | 0.9515 | 1.4 | 30 | 0.0 | 0.0 | moins bon |


Plus petite perte pinball à τ = 0.8 : **7 retards seuls** (0.7362). Aucune variante ne bat significativement le choix retenu (Complet : retards + flux + calendrier (retenu)) après correction de Holm.



### D6 · Prétraitement

*Quelle mise à l'échelle des variables ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| z-score : (x − moyenne)/écart-type (retenu) | 1.341 | 1.708 | -0.406 | 0.7926 | 1.4 |  |  | — choix retenu |
| Robuste : (x − médiane)/(Q3 − Q1) | 1.337 | 1.699 | -0.414 | 0.7928 | 1.1 | 0.9747 | 0.9747 | équivalent |
| Min-max : (x − min)/(max − min) | 1.928 | 2.298 | -0.564 | 1.133 | 0.8 | 0.0 | 0.0 | moins bon |
| Aucune mise à l'échelle | 1.63 | 2.066 | -0.477 | 0.9578 | 1.3 | 0.0001 | 0.0002 | moins bon |


Plus petite perte pinball à τ = 0.8 : **z-score : (x − moyenne)/écart-type (retenu)** (0.7926). Aucune variante ne bat significativement le choix retenu (z-score : (x − moyenne)/écart-type (retenu)) après correction de Holm.



### D7 · Fenêtre d'entraînement

*Faut-il tout le passé, ou seulement les derniers mois ? (mesure aussi le coût d'un historique court)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Croissante (tout le passé) (retenu) | 1.399 | 1.782 | -0.38 | 0.5262 | 85.2 | 6.8 |  |  | — choix retenu |
| Glissante : 365 derniers jours | 1.396 | 1.782 | -0.372 | 0.5233 | 85.2 | 6.7 | 0.2866 | 0.2866 | équivalent |
| Glissante : 180 derniers jours | 1.453 | 1.844 | 0.001 | 0.4939 | 77.0 | 6.3 | 0.1359 | 0.2718 | équivalent |
| Glissante : 90 derniers jours | 1.737 | 2.211 | 0.042 | 0.6525 | 69.9 | 6.2 | 0.0001 | 0.0003 | moins bon |


Plus petite perte pinball à τ = 0.8 : **Glissante : 180 derniers jours** (0.4939). Aucune variante ne bat significativement le choix retenu (Croissante (tout le passé) (retenu)) après correction de Holm.



### D8 · Optimisation

*Comment atteindre le minimum de J le plus sûrement ? (SVR RBF, un découpage)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | J final | pas effectués | arrêt | solution gardée | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Adam + Polyak + préconditionnement + décroissance η (retenu) | 1.782 | 2.141 | -1.124 | 1.228 | 0.6 | 696.54 | 3000 | 3000 pas atteints | meilleur point rencontré |  |  | — choix retenu |
| Adam sans moyenne de Polyak | 1.782 | 2.141 | -1.124 | 1.228 | 0.6 | 696.54 | 3000 | 3000 pas atteints | meilleur point rencontré |  |  | identique |
| Adam sans préconditionnement | 1.717 | 2.074 | -1.024 | 1.1655 | 0.7 | 710.29 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | meilleur |
| Adam sans décroissance de η | 1.781 | 2.14 | -1.126 | 1.2282 | 0.2 | 696.69 | 768 | J stable depuis 100 pas (pas 767) | meilleur point rencontré | 0.6946 | 0.6946 | équivalent |
| Momentum | 2.034 | 2.393 | -0.437 | 1.1478 | 0.5 | 1116.33 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0853 | 0.2559 | équivalent |
| Descente de gradient simple | 2.034 | 2.393 | -0.437 | 1.1478 | 0.4 | 1116.33 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0853 | 0.2559 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Momentum** (1.1478). ⚠ Significativement meilleur que le choix retenu (Holm, 5 %) : Adam sans préconditionnement — le choix est à revoir.



### D9 · Combinaison des modèles

*Apprendre les poids de combinaison apporte-t-il plus qu'une moyenne ? (jours où l'empilement prédit)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Niveau 4 seul (meilleur modèle unique) | 1.421 | 1.802 | -0.547 | 0.5356 | 85.2 | 5.7 | 0.1186 | 0.2372 | équivalent |
| Moyenne simple persistance + niv. 3 + niv. 4 | 1.316 | 1.745 | -0.427 | 0.5326 | 71.6 | 11.5 | 0.0385 | 0.154 | équivalent |
| Empilement appris (poids positifs) (retenu) | 1.296 | 1.791 | -0.063 | 0.491 | 81.3 | 22.2 |  |  | — choix retenu |
| XGBoost quantile seul | 1.406 | 1.77 | -0.588 | 0.5986 | 83.9 | 9.1 | 0.0032 | 0.016 | moins bon |
| Moyenne SVR niv. 4 + XGBoost | 1.394 | 1.752 | -0.567 | 0.5496 | 84.5 | 14.8 | 0.0462 | 0.154 | équivalent |
| Empilement persistance + niv. 3 + niv. 4 + XGBoost | 1.299 | 1.783 | -0.034 | 0.4893 | 80.0 | 31.8 | 0.6183 | 0.6183 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Empilement persistance + niv. 3 + niv. 4 + XGBoost** (0.4893). Aucune variante ne bat significativement le choix retenu (Empilement appris (poids positifs) (retenu)) après correction de Holm.



### D13 · Variantes de SVM

*Quel SVM est le plus adapté à la série du service ? (mêmes jours, mêmes variables)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | cle | couverture 90 % | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| SVR linéaire (niveau 1) | 1.236 | 1.589 | -0.358 | 0.7253 | 0.7 | svr_lineaire |  | 0.0 | 0.0 | moins bon |
| SVR RBF (niveau 2) | 1.341 | 1.708 | -0.406 | 0.7926 | 1.4 | svr_rbf |  | 0.0 | 0.0 | moins bon |
| SVR quantile RBF (niveau 3) | 1.423 | 1.772 | -0.501 | 0.5302 | 4.7 | svr_q_rbf | 85.8 | 0.7263 | 0.7263 | équivalent |
| SVR quantile composite (niveau 4, retenu) (retenu) | 1.399 | 1.782 | -0.38 | 0.5262 | 6.7 | svr_q_composite | 85.2 |  |  | — choix retenu |
| SVR quantile, noyau laplacien | 1.626 | 1.993 | -0.371 | 0.5658 | 5.1 | svr_q_laplacien | 87.4 | 0.0161 | 0.0483 | moins bon |
| SVR quantile, noyau polynomial (degré 2) | 1.238 | 1.617 | -0.334 | 0.4771 | 5.6 | svr_q_polynomial | 83.1 | 0.0174 | 0.0483 | meilleur |
| LS-SVR (moindres carrés), noyau RBF, quantiles LOO | 1.342 | 1.681 | -0.43 | 0.4411 | 0.1 | lssvr_rbf | 91.3 | 0.0001 | 0.0004 | meilleur |


Plus petite perte pinball à τ = 0.8 : **LS-SVR (moindres carrés), noyau RBF, quantiles LOO** (0.4411). ⚠ Significativement meilleur que le choix retenu (Holm, 5 %) : SVR quantile, noyau polynomial (degré 2), LS-SVR (moindres carrés), noyau RBF, quantiles LOO — le choix est à revoir.



### D11 · Chaque variable, une à une

*Que perd le modèle si on lui retire cette seule variable ? (modèle RBF du niveau 2, mêmes jours)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 1.341 | 1.708 | -0.406 | 0.7926 | 1.4 |  |  | — choix retenu |
| Sans occ_j-0 | 1.624 | 1.984 | -0.504 | 0.9633 | 1.3 | 0.0 | 0.0 | moins bon |
| Sans occ_j-1 | 1.341 | 1.7 | -0.417 | 0.7955 | 1.4 | 0.4742 | 1.0 | équivalent |
| Sans occ_j-2 | 1.329 | 1.694 | -0.391 | 0.7819 | 1.3 | 0.0034 | 0.0544 | équivalent |
| Sans occ_j-3 | 1.324 | 1.692 | -0.393 | 0.7799 | 1.0 | 0.0 | 0.0 | meilleur |
| Sans occ_j-4 | 1.333 | 1.698 | -0.409 | 0.789 | 1.4 | 0.1788 | 1.0 | équivalent |
| Sans occ_j-5 | 1.35 | 1.715 | -0.429 | 0.8034 | 1.4 | 0.0123 | 0.1845 | équivalent |
| Sans occ_j-6 | 1.374 | 1.749 | -0.404 | 0.8082 | 1.4 | 0.1627 | 1.0 | équivalent |
| Sans adm_3j | 1.31 | 1.704 | -0.352 | 0.7608 | 1.3 | 0.0331 | 0.4634 | équivalent |
| Sans adm_7j | 1.331 | 1.721 | -0.374 | 0.778 | 1.1 | 0.2881 | 1.0 | équivalent |
| Sans sorties_7j | 1.381 | 1.744 | -0.261 | 0.769 | 1.3 | 0.2021 | 1.0 | équivalent |
| Sans cible_jour_0 | 1.343 | 1.715 | -0.417 | 0.7968 | 0.7 | 0.1722 | 1.0 | équivalent |
| Sans cible_jour_1 | 1.335 | 1.706 | -0.421 | 0.7937 | 1.3 | 0.67 | 1.0 | équivalent |
| Sans cible_jour_2 | 1.366 | 1.727 | -0.435 | 0.8135 | 1.3 | 0.0021 | 0.0357 | moins bon |
| Sans cible_jour_3 | 1.334 | 1.698 | -0.403 | 0.7877 | 1.2 | 0.0479 | 0.6227 | équivalent |
| Sans cible_jour_4 | 1.338 | 1.704 | -0.416 | 0.794 | 1.3 | 0.6992 | 1.0 | équivalent |
| Sans cible_jour_5 | 1.354 | 1.73 | -0.396 | 0.7956 | 1.3 | 0.7179 | 1.0 | équivalent |
| Sans cible_jour_6 | 1.337 | 1.701 | -0.41 | 0.7913 | 1.3 | 0.6556 | 1.0 | équivalent |
| Sans mois_sin | 1.346 | 1.718 | -0.392 | 0.7907 | 0.9 | 0.8709 | 1.0 | équivalent |
| Sans mois_cos | 1.336 | 1.714 | -0.475 | 0.8107 | 1.3 | 0.0768 | 0.9216 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Sans adm_3j** (0.7608). ⚠ Significativement meilleur que le choix retenu (Holm, 5 %) : Sans occ_j-3 — le choix est à revoir.



### D14 · Sélection des variables par le lasso

*Le modèle gagne-t-il à ne garder que les variables choisies par le lasso ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 1.341 | 1.708 | -0.406 | 0.7926 | 1.3 | 19.0 |  |  | — choix retenu |
| Lasso, λ de plus petite erreur | 1.3 | 1.671 | -0.405 | 0.7716 | 17.0 | 13.1 | 0.0558 | 0.1116 | équivalent |
| Lasso à un écart-type (λ_1se) | 1.371 | 1.748 | -0.418 | 0.8108 | 14.6 | 9.9 | 0.2041 | 0.2041 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Lasso, λ de plus petite erreur** (0.7716). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)) après correction de Holm.



## Horizon J+7 — 177 jours évalués, 7 origines


### D1 · Modèles de référence, concurrents et SVR

*Le SVR fait-il mieux que les méthodes statistiques usuelles et que les autres modèles d'apprentissage ?*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | couverture 90 % | réglages | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Persistance | 2.686 | 3.323 | -0.004 | 1.3441 | 0.0 |  |  | 0.0265 | 0.5035 | équivalent |
| Saisonnière hebdomadaire | 2.384 | 2.944 | 0.048 | 1.1776 | 0.0 |  |  | 0.1212 | 1.0 | équivalent |
| Moyenne mobile 7 j | 2.592 | 3.178 | 0.055 | 1.2796 | 0.0 |  |  | 0.106 | 1.0 | équivalent |
| Moyenne historique | 2.873 | 3.416 | -1.681 | 0.8365 | 0.0 | 89.3 |  | 0.5575 | 1.0 | équivalent |
| Lissage exponentiel simple | 2.686 | 3.323 | -0.004 | 0.9723 | 0.0 | 92.1 |  | 0.4299 | 1.0 | équivalent |
| Méthode Thêta | 2.682 | 3.324 | 0.061 | 0.9723 | 0.0 | 92.1 |  | 0.4299 | 1.0 | équivalent |
| Holt linéaire | 2.686 | 3.323 | -0.004 | 0.9723 | 0.0 | 92.1 |  | 0.4299 | 1.0 | équivalent |
| Holt amorti | 2.686 | 3.323 | -0.004 | 0.9723 | 0.0 | 92.1 |  | 0.4299 | 1.0 | équivalent |
| Lissage saisonnier sans tendance | 2.686 | 3.323 | -0.004 | 0.9723 | 0.0 | 92.1 |  | 0.4299 | 1.0 | équivalent |
| Holt-Winters additif amorti | 2.686 | 3.323 | -0.004 | 0.9723 | 0.1 | 92.1 |  | 0.4299 | 1.0 | équivalent |
| Holt-Winters multiplicatif amorti | 2.686 | 3.323 | -0.004 | 0.9723 | 0.0 | 92.1 |  | 0.4299 | 1.0 | équivalent |
| AR(p) par AIC | 2.54 | 2.98 | -0.711 | 0.7927 | 0.1 | 95.5 |  | 0.1188 | 1.0 | équivalent |
| SARIMA(2,0,0)(1,0,0)7 (ordre choisi sur l'apprentissage) | 2.562 | 3.026 | -1.037 | 0.8057 | 4.9 | 91.5 |  | 0.0499 | 0.7984 | équivalent |
| Holt-Winters additif, grille fixée avant la validation | 2.421 | 2.942 | 0.046 | 1.1967 | 0.1 |  | alpha=0.1, beta=0.0, gamma=0.05, phi=0.8 | 0.1189 | 1.0 | équivalent |
| Régression ridge (λ = 1) | 3.019 | 3.576 | -1.462 | 1.9484 | 0.1 |  |  | 0.0002 | 0.0046 | moins bon |
| A · forêt aléatoire quantile | 2.604 | 3.082 | -0.997 | 0.895 | 9.6 | 89.3 |  | 0.8629 | 1.0 | équivalent |
| B · gradient boosting quantile | 2.734 | 3.275 | -1.202 | 1.2295 | 8.6 | 64.4 |  | 0.0356 | 0.6408 | équivalent |
| C · perceptron multicouche quantile | 3.12 | 3.681 | -1.402 | 0.9601 | 1.0 | 81.9 |  | 0.2975 | 1.0 | équivalent |
| D · LSTM quantile | 3.389 | 3.983 | -1.914 | 1.0421 | 7.5 | 67.8 |  | 0.0094 | 0.188 | équivalent |
| E · XGBoost quantile (second ordre) | 2.791 | 3.364 | -1.204 | 1.1756 | 9.0 | 74.0 |  | 0.0367 | 0.6408 | équivalent |
| SVR linéaire (niveau 1) | 2.957 | 3.497 | -1.272 | 1.86 | 0.7 |  |  | 0.0002 | 0.0046 | moins bon |
| SVR RBF (niveau 2) | 2.534 | 3.011 | -0.998 | 1.5663 | 0.8 |  |  | 0.0006 | 0.0126 | moins bon |
| SVR quantile RBF (niveau 3) | 2.719 | 3.196 | -1.041 | 0.871 | 1.9 | 91.5 |  | 0.2855 | 1.0 | équivalent |
| SVR quantile composite (niveau 4) (retenu) | 2.698 | 3.166 | -0.978 | 0.8824 | 5.0 | 89.8 |  |  |  | — choix retenu |


Plus petite perte pinball à τ = 0.8 : **AR(p) par AIC** (0.7927). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4) (retenu)) après correction de Holm.



### D2 · Noyau

*Quel noyau décrit le mieux la dynamique ? (même perte ε-insensible, même C)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Linéaire | 3.099 | 3.693 | -1.446 | 1.9835 | 0.9 | 0.003 | 0.006 | moins bon |
| RBF (γ = 0.05) | 2.534 | 3.011 | -0.998 | 1.5663 | 0.9 | 0.5305 | 0.5305 | équivalent |
| Composite occupation / flux et saison (β appris) (retenu) | 2.536 | 3.03 | -1.079 | 1.5917 | 1.3 |  |  | — choix retenu |


Plus petite perte pinball à τ = 0.8 : **RBF (γ = 0.05)** (1.5663). Aucune variante ne bat significativement le choix retenu (Composite occupation / flux et saison (β appris) (retenu)) après correction de Holm.



### D3 · Fonction de perte

*Quelle perte pour un modèle linéaire identique ? (isole l'effet de la perte)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Carrée (ridge, λ = 1/C) | 3.004 | 3.55 | -1.439 | 1.9337 | 0.1 | 0.0761 | 0.2283 | équivalent |
| ε-insensible, ε = 0 lit (= valeur absolue) | 2.911 | 3.429 | -1.225 | 1.8229 | 0.9 | 0.0092 | 0.0368 | meilleur |
| ε-insensible, ε = 0.5 lit (retenu) | 2.957 | 3.497 | -1.272 | 1.86 | 0.7 |  |  | — choix retenu |
| ε-insensible, ε = 1 lit | 3.007 | 3.57 | -1.237 | 1.8748 | 0.6 | 0.3873 | 0.7746 | équivalent |
| ε-insensible, ε = 2 lit | 3.043 | 3.578 | -1.221 | 1.8879 | 0.7 | 0.7243 | 0.7746 | équivalent |


Plus petite perte pinball à τ = 0.8 : **ε-insensible, ε = 0 lit (= valeur absolue)** (1.8229). ⚠ Significativement meilleur que le choix retenu (Holm, 5 %) : ε-insensible, ε = 0 lit (= valeur absolue) — le choix est à revoir.



### D4 · Quantile décisionnel τ et coût des décisions

*Quel τ minimise le coût réel selon le rapport pénurie / lit vide ? (τ optimal théorique = r/(1+r))*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | jours sous-estimés % | lits prévus en moyenne | coût r=1 | coût r=2 | coût r=4 | coût r=9 | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| τ = 0.5 | 2.719 | 3.196 | -1.041 | 1.6718 | 0.4 | 62.7 | 11.25 | 2.719 | 4.599 | 8.359 | 17.759 | 0.0007 | 0.0028 | moins bon |
| τ = 0.6 | 2.6 | 3.065 | -0.134 | 1.3404 | 0.3 | 55.9 | 12.15 | 2.6 | 3.968 | 6.702 | 13.539 | 0.0035 | 0.0105 | moins bon |
| τ = 0.7 | 2.573 | 3.127 | 0.695 | 1.0777 | 0.3 | 46.9 | 12.98 | 2.573 | 3.511 | 5.389 | 10.082 | 0.0149 | 0.0298 | moins bon |
| τ = 0.8 (retenu) | 2.745 | 3.454 | 1.671 | 0.871 | 0.7 | 32.8 | 13.96 | 2.745 | 3.282 | 4.355 | 7.039 |  |  | — choix retenu |
| τ = 0.9 | 3.378 | 4.254 | 3.083 | 0.7642 | 0.3 | 16.4 | 15.37 | 3.378 | 3.526 | 3.821 | 4.559 | 0.2874 | 0.2874 | équivalent |


τ le moins coûteux pour chaque rapport de coûts r = c_pénurie / c_lit vide : r = 1 → τ = 0.7, r = 2 → τ = 0.8 (retenu), r = 4 → τ = 0.9, r = 9 → τ = 0.9. Le choix τ = 0.8 correspond à r = 4.


### D5 · Variables d'entrée

*Que rapporte chaque groupe de variables ? (même modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| 7 retards seuls | 2.682 | 3.15 | -1.059 | 1.6584 | 0.4 | 7 | 0.3493 | 1.0 | équivalent |
| 7 retards + flux | 2.644 | 3.147 | -1.273 | 1.7038 | 0.6 | 10 | 0.17 | 1.0 | équivalent |
| 7 retards + calendrier (jour, mois) | 2.608 | 3.053 | -0.866 | 1.5639 | 0.8 | 16 | 0.974 | 1.0 | équivalent |
| Complet : retards + flux + calendrier (retenu) | 2.534 | 3.011 | -0.998 | 1.5663 | 0.9 | 19 |  |  | — choix retenu |
| Complet + jours fériés camerounais | 2.55 | 3.026 | -1.014 | 1.5792 | 1.4 | 21 | 0.1262 | 1.0 | équivalent |
| Complet + vacances scolaires | 2.57 | 3.055 | -0.968 | 1.5754 | 1.2 | 20 | 0.732 | 1.0 | équivalent |
| Complet + fériés + vacances scolaires | 2.582 | 3.065 | -0.989 | 1.5875 | 0.9 | 22 | 0.4936 | 1.0 | équivalent |
| 3 retards + flux + calendrier | 2.583 | 3.08 | -1.055 | 1.6078 | 1.0 | 15 | 0.3375 | 1.0 | équivalent |
| 14 retards + flux + calendrier | 2.592 | 3.108 | -0.723 | 1.5129 | 0.9 | 26 | 0.4611 | 1.0 | équivalent |
| Complet + diagnostics d'entrée des présents | 2.56 | 3.045 | -0.677 | 1.4831 | 1.4 | 30 | 0.4816 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Complet + diagnostics d'entrée des présents** (1.4831). Aucune variante ne bat significativement le choix retenu (Complet : retards + flux + calendrier (retenu)) après correction de Holm.



### D6 · Prétraitement

*Quelle mise à l'échelle des variables ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| z-score : (x − moyenne)/écart-type (retenu) | 2.534 | 3.011 | -0.998 | 1.5663 | 0.9 |  |  | — choix retenu |
| Robuste : (x − médiane)/(Q3 − Q1) | 2.693 | 3.219 | -1.092 | 1.6739 | 1.3 | 0.0855 | 0.2565 | équivalent |
| Min-max : (x − min)/(max − min) | 2.77 | 3.275 | -1.014 | 1.689 | 0.6 | 0.1691 | 0.3382 | équivalent |
| Aucune mise à l'échelle | 2.608 | 3.032 | -1.054 | 1.62 | 0.9 | 0.6445 | 0.6445 | équivalent |


Plus petite perte pinball à τ = 0.8 : **z-score : (x − moyenne)/écart-type (retenu)** (1.5663). Aucune variante ne bat significativement le choix retenu (z-score : (x − moyenne)/écart-type (retenu)) après correction de Holm.



### D7 · Fenêtre d'entraînement

*Faut-il tout le passé, ou seulement les derniers mois ? (mesure aussi le coût d'un historique court)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Croissante (tout le passé) (retenu) | 2.698 | 3.166 | -0.978 | 0.8824 | 89.8 | 5.2 |  |  | — choix retenu |
| Glissante : 365 derniers jours | 2.698 | 3.166 | -0.975 | 0.8826 | 89.8 | 5.2 | 0.3476 | 0.6952 | équivalent |
| Glissante : 180 derniers jours | 2.619 | 3.091 | -0.382 | 0.8637 | 87.6 | 4.4 | 0.4903 | 0.6952 | équivalent |
| Glissante : 90 derniers jours | 2.735 | 3.233 | -0.188 | 0.9872 | 80.8 | 3.8 | 0.039 | 0.117 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Glissante : 180 derniers jours** (0.8637). Aucune variante ne bat significativement le choix retenu (Croissante (tout le passé) (retenu)) après correction de Holm.



### D8 · Optimisation

*Comment atteindre le minimum de J le plus sûrement ? (SVR RBF, un découpage)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | J final | pas effectués | arrêt | solution gardée | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Adam + Polyak + préconditionnement + décroissance η (retenu) | 3.708 | 4.381 | -3.001 | 2.754 | 0.1 | 1080.3 | 618 | J stable depuis 100 pas (pas 617) | meilleur point rencontré |  |  | — choix retenu |
| Adam sans moyenne de Polyak | 3.708 | 4.381 | -3.001 | 2.754 | 0.1 | 1080.3 | 618 | J stable depuis 100 pas (pas 617) | meilleur point rencontré |  |  | identique |
| Adam sans préconditionnement | 3.667 | 4.333 | -2.936 | 2.7142 | 0.7 | 1094.35 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | meilleur |
| Adam sans décroissance de η | 3.7 | 4.373 | -2.991 | 2.7475 | 0.6 | 1080.37 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | meilleur |
| Momentum | 2.749 | 3.265 | -1.343 | 1.7774 | 0.4 | 1318.4 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | meilleur |
| Descente de gradient simple | 2.749 | 3.265 | -1.343 | 1.7774 | 0.4 | 1318.4 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | meilleur |


Plus petite perte pinball à τ = 0.8 : **Momentum** (1.7774). ⚠ Significativement meilleur que le choix retenu (Holm, 5 %) : Adam sans préconditionnement, Adam sans décroissance de η, Momentum, Descente de gradient simple — le choix est à revoir.



### D9 · Combinaison des modèles

*Apprendre les poids de combinaison apporte-t-il plus qu'une moyenne ? (jours où l'empilement prédit)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Niveau 4 seul (meilleur modèle unique) | 2.717 | 3.163 | -1.475 | 0.8577 | 89.9 | 3.6 | 0.6485 | 1.0 | équivalent |
| Moyenne simple persistance + niv. 3 + niv. 4 | 2.43 | 2.842 | -1.024 | 0.9066 | 73.2 | 7.2 | 0.9583 | 1.0 | équivalent |
| Empilement appris (poids positifs) (retenu) | 2.737 | 3.247 | -0.482 | 0.913 | 88.6 | 18.3 |  |  | — choix retenu |
| XGBoost quantile seul | 2.844 | 3.43 | -1.68 | 1.249 | 74.5 | 9.3 | 0.1267 | 0.6335 | équivalent |
| Moyenne SVR niv. 4 + XGBoost | 2.749 | 3.252 | -1.578 | 1.0222 | 84.6 | 12.9 | 0.5008 | 1.0 | équivalent |
| Empilement persistance + niv. 3 + niv. 4 + XGBoost | 2.712 | 3.247 | -0.43 | 0.9252 | 88.6 | 27.8 | 0.8551 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Niveau 4 seul (meilleur modèle unique)** (0.8577). Aucune variante ne bat significativement le choix retenu (Empilement appris (poids positifs) (retenu)) après correction de Holm.



### D13 · Variantes de SVM

*Quel SVM est le plus adapté à la série du service ? (mêmes jours, mêmes variables)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | cle | couverture 90 % | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| SVR linéaire (niveau 1) | 2.957 | 3.497 | -1.272 | 1.86 | 0.7 | svr_lineaire |  | 0.0002 | 0.0012 | moins bon |
| SVR RBF (niveau 2) | 2.534 | 3.011 | -0.998 | 1.5663 | 0.9 | svr_rbf |  | 0.0006 | 0.003 | moins bon |
| SVR quantile RBF (niveau 3) | 2.719 | 3.196 | -1.041 | 0.871 | 2.0 | svr_q_rbf | 91.5 | 0.2855 | 1.0 | équivalent |
| SVR quantile composite (niveau 4, retenu) (retenu) | 2.698 | 3.166 | -0.978 | 0.8824 | 5.3 | svr_q_composite | 89.8 |  |  | — choix retenu |
| SVR quantile, noyau laplacien | 2.713 | 3.195 | -1.089 | 0.8739 | 1.9 | svr_q_laplacien | 91.0 | 0.7022 | 1.0 | équivalent |
| SVR quantile, noyau polynomial (degré 2) | 2.701 | 3.17 | -0.935 | 0.8832 | 4.2 | svr_q_polynomial | 90.4 | 0.9783 | 1.0 | équivalent |
| LS-SVR (moindres carrés), noyau RBF, quantiles LOO | 2.508 | 3.047 | -1.114 | 0.8943 | 0.1 | lssvr_rbf | 88.7 | 0.818 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **SVR quantile RBF (niveau 3)** (0.871). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4, retenu) (retenu)) après correction de Holm.



### D11 · Chaque variable, une à une

*Que perd le modèle si on lui retire cette seule variable ? (modèle RBF du niveau 2, mêmes jours)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 2.534 | 3.011 | -0.998 | 1.5663 | 0.9 |  |  | — choix retenu |
| Sans occ_j-0 | 2.546 | 3.038 | -1.022 | 1.5793 | 1.3 | 0.1717 | 1.0 | équivalent |
| Sans occ_j-1 | 2.519 | 3.005 | -0.989 | 1.5563 | 0.8 | 0.4111 | 1.0 | équivalent |
| Sans occ_j-2 | 2.521 | 3.005 | -0.948 | 1.5448 | 1.2 | 0.1953 | 1.0 | équivalent |
| Sans occ_j-3 | 2.524 | 3.011 | -1.006 | 1.5636 | 1.0 | 0.7907 | 1.0 | équivalent |
| Sans occ_j-4 | 2.532 | 3.008 | -1.019 | 1.5719 | 1.0 | 0.5718 | 1.0 | équivalent |
| Sans occ_j-5 | 2.556 | 3.035 | -1.003 | 1.5792 | 0.7 | 0.2312 | 1.0 | équivalent |
| Sans occ_j-6 | 2.556 | 3.027 | -0.998 | 1.5775 | 0.9 | 0.5528 | 1.0 | équivalent |
| Sans adm_3j | 2.515 | 3.012 | -1.021 | 1.5639 | 0.8 | 0.8788 | 1.0 | équivalent |
| Sans adm_7j | 2.592 | 3.047 | -0.94 | 1.5778 | 0.9 | 0.7399 | 1.0 | équivalent |
| Sans sorties_7j | 2.539 | 3.011 | -0.865 | 1.5289 | 1.1 | 0.4379 | 1.0 | équivalent |
| Sans cible_jour_0 | 2.547 | 3.014 | -0.987 | 1.5698 | 1.2 | 0.6118 | 1.0 | équivalent |
| Sans cible_jour_1 | 2.515 | 2.987 | -0.961 | 1.5459 | 1.1 | 0.0 | 0.0 | meilleur |
| Sans cible_jour_2 | 2.526 | 3.002 | -0.964 | 1.5524 | 0.8 | 0.0025 | 0.045 | meilleur |
| Sans cible_jour_3 | 2.523 | 3.0 | -0.946 | 1.5452 | 1.1 | 0.1738 | 1.0 | équivalent |
| Sans cible_jour_4 | 2.542 | 3.023 | -0.991 | 1.5683 | 1.1 | 0.8368 | 1.0 | équivalent |
| Sans cible_jour_5 | 2.547 | 3.025 | -1.006 | 1.5752 | 1.1 | 0.0278 | 0.4726 | équivalent |
| Sans cible_jour_6 | 2.529 | 3.013 | -0.984 | 1.5596 | 1.1 | 0.3643 | 1.0 | équivalent |
| Sans mois_sin | 2.673 | 3.172 | -0.819 | 1.5823 | 0.9 | 0.835 | 1.0 | équivalent |
| Sans mois_cos | 2.641 | 3.184 | -1.358 | 1.7281 | 0.7 | 0.1257 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Sans sorties_7j** (1.5289). ⚠ Significativement meilleur que le choix retenu (Holm, 5 %) : Sans cible_jour_1, Sans cible_jour_2 — le choix est à revoir.



### D14 · Sélection des variables par le lasso

*Le modèle gagne-t-il à ne garder que les variables choisies par le lasso ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 2.534 | 3.011 | -0.998 | 1.5663 | 0.9 | 19.0 |  |  | — choix retenu |
| Lasso, λ de plus petite erreur | 2.819 | 3.317 | -1.265 | 1.789 | 19.6 | 4.3 | 0.0214 | 0.0428 | moins bon |
| Lasso à un écart-type (λ_1se) | 2.733 | 3.207 | -1.043 | 1.6792 | 19.1 | 1.0 | 0.3262 | 0.3262 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Toutes les variables (retenu)** (1.5663). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)) après correction de Holm.

