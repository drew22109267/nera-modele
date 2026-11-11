# Banc de comparaison des choix — service PED

Validation glissante du 01/03/2026 au verrou (01/09/2026), une origine tous les 28 jours, modèle réentraîné à chaque origine. « (retenu) » = choix retenu. Test de Diebold-Mariano (perte absolue, correction HLN) contre le choix retenu.


## Horizon J+1 — 183 jours évalués, 7 origines


### D1 · Modèles de référence, concurrents et SVR

*Le SVR fait-il mieux que les méthodes statistiques usuelles et que les autres modèles d'apprentissage ?*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | couverture 90 % | réglages | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Persistance | 1.992 | 2.631 | 0.016 | 0.9911 | 0.0 |  |  | 0.0 | 0.0 | moins bon |
| Saisonnière hebdomadaire | 3.059 | 3.713 | 0.316 | 1.4347 | 0.0 |  |  | 0.0 | 0.0 | moins bon |
| Moyenne mobile 7 j | 2.724 | 3.378 | 0.099 | 1.3323 | 0.0 |  |  | 0.0 | 0.0 | moins bon |
| Moyenne historique | 2.75 | 3.346 | 0.063 | 1.0111 | 0.0 | 89.1 |  | 0.0 | 0.0 | moins bon |
| Lissage exponentiel simple | 2.01 | 2.628 | 0.017 | 0.7365 | 0.0 | 88.0 |  | 0.0685 | 0.959 | équivalent |
| Méthode Thêta | 2.01 | 2.628 | 0.016 | 0.7365 | 0.0 | 88.0 |  | 0.0685 | 0.959 | équivalent |
| Holt linéaire | 2.01 | 2.628 | 0.017 | 0.7365 | 0.2 | 88.0 |  | 0.0685 | 0.959 | équivalent |
| Holt amorti | 2.01 | 2.628 | 0.017 | 0.7365 | 0.2 | 88.0 |  | 0.0685 | 0.959 | équivalent |
| Lissage saisonnier sans tendance | 1.976 | 2.628 | 0.016 | 0.7239 | 0.2 | 87.4 |  | 0.1717 | 1.0 | équivalent |
| Holt-Winters additif amorti | 1.977 | 2.631 | 0.014 | 0.7231 | 0.5 | 87.4 |  | 0.1962 | 1.0 | équivalent |
| Holt-Winters multiplicatif amorti | 2.047 | 2.747 | 0.087 | 0.7444 | 0.9 | 88.0 |  | 0.0529 | 0.7935 | équivalent |
| AR(p) par AIC | 1.917 | 2.417 | 0.085 | 0.6752 | 0.1 | 88.0 |  | 0.882 | 1.0 | équivalent |
| SARIMA(2,1,1)(1,0,0)7 (ordre choisi sur l'apprentissage) | 1.917 | 2.449 | 0.061 | 0.6843 | 14.2 | 88.0 |  | 0.8221 | 1.0 | équivalent |
| Holt-Winters additif, grille fixée avant la validation | 1.958 | 2.601 | 0.017 | 0.9739 | 0.2 |  | alpha=0.9, beta=0.0, gamma=0.3, phi=0.98 | 0.0 | 0.0 | moins bon |
| Régression ridge (λ = 1) | 1.791 | 2.342 | -0.028 | 0.9036 | 0.1 |  |  | 0.0 | 0.0 | moins bon |
| A · forêt aléatoire quantile | 1.929 | 2.483 | -0.122 | 0.709 | 22.6 | 92.3 |  | 0.2966 | 1.0 | équivalent |
| B · gradient boosting quantile | 1.854 | 2.406 | -0.079 | 0.7244 | 11.3 | 81.4 |  | 0.0805 | 0.959 | équivalent |
| C · perceptron multicouche quantile | 1.86 | 2.369 | -0.164 | 0.6581 | 1.3 | 88.0 |  | 0.3159 | 1.0 | équivalent |
| D · LSTM quantile | 1.83 | 2.405 | 0.038 | 0.6753 | 13.9 | 88.5 |  | 0.869 | 1.0 | équivalent |
| E · XGBoost quantile (second ordre) | 1.902 | 2.44 | -0.124 | 0.7281 | 15.2 | 86.9 |  | 0.0726 | 0.959 | équivalent |
| SVR linéaire (niveau 1) | 1.809 | 2.371 | -0.038 | 0.916 | 0.4 |  |  | 0.0 | 0.0 | moins bon |
| SVR RBF (niveau 2) | 1.819 | 2.344 | -0.024 | 0.9167 | 2.2 |  |  | 0.0 | 0.0 | moins bon |
| SVR quantile RBF (niveau 3) | 1.862 | 2.374 | -0.093 | 0.6703 | 6.9 | 86.9 |  | 0.5135 | 1.0 | équivalent |
| SVR quantile composite (niveau 4) (retenu) | 1.839 | 2.348 | 0.018 | 0.6789 | 11.8 | 85.8 |  |  |  | — choix retenu |


Plus petite perte pinball à τ = 0.8 : **C · perceptron multicouche quantile** (0.6581). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4) (retenu)) après correction de Holm.



### D2 · Noyau

*Quel noyau décrit le mieux la dynamique ? (même perte ε-insensible, même C)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Linéaire | 1.807 | 2.371 | -0.039 | 0.915 | 0.5 | 0.4982 | 0.8462 | équivalent |
| RBF (γ = 0.02) | 1.819 | 2.344 | -0.024 | 0.9167 | 1.8 | 0.4231 | 0.8462 | équivalent |
| Composite occupation / flux et saison (β appris) (retenu) | 1.816 | 2.341 | 0.028 | 0.8995 | 3.7 |  |  | — choix retenu |


Plus petite perte pinball à τ = 0.8 : **Composite occupation / flux et saison (β appris) (retenu)** (0.8995). Aucune variante ne bat significativement le choix retenu (Composite occupation / flux et saison (β appris) (retenu)) après correction de Holm.



### D3 · Fonction de perte

*Quelle perte pour un modèle linéaire identique ? (isole l'effet de la perte)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Carrée (ridge, λ = 1/C) | 1.791 | 2.34 | -0.026 | 0.9031 | 0.1 | 0.1687 | 0.3374 | équivalent |
| ε-insensible, ε = 0 lit (= valeur absolue) | 1.823 | 2.385 | -0.118 | 0.9467 | 0.7 | 0.0006 | 0.0024 | moins bon |
| ε-insensible, ε = 0.5 lit (retenu) | 1.809 | 2.371 | -0.038 | 0.916 | 0.5 |  |  | — choix retenu |
| ε-insensible, ε = 1 lit | 1.808 | 2.364 | -0.043 | 0.9168 | 0.6 | 0.9269 | 0.9269 | équivalent |
| ε-insensible, ε = 2 lit | 1.772 | 2.319 | -0.018 | 0.8914 | 0.4 | 0.0361 | 0.1083 | équivalent |


Plus petite perte pinball à τ = 0.8 : **ε-insensible, ε = 2 lit** (0.8914). Aucune variante ne bat significativement le choix retenu (ε-insensible, ε = 0.5 lit (retenu)) après correction de Holm.



### D4 · Quantile décisionnel τ et coût des décisions

*Quel τ minimise le coût réel selon le rapport pénurie / lit vide ? (τ optimal théorique = r/(1+r))*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | jours sous-estimés % | lits prévus en moyenne | coût r=1 | coût r=2 | coût r=4 | coût r=9 | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| τ = 0.5 | 1.862 | 2.374 | -0.093 | 0.9589 | 1.9 | 49.2 | 8.35 | 1.862 | 2.839 | 4.794 | 9.682 | 0.0 | 0.0 | moins bon |
| τ = 0.6 | 1.906 | 2.41 | 0.468 | 0.8123 | 1.4 | 42.6 | 8.91 | 1.906 | 2.624 | 4.062 | 7.655 | 0.0008 | 0.0024 | moins bon |
| τ = 0.7 | 2.119 | 2.629 | 1.153 | 0.7135 | 1.1 | 31.7 | 9.59 | 2.119 | 2.602 | 3.567 | 5.982 | 0.0448 | 0.0896 | équivalent |
| τ = 0.8 (retenu) | 2.425 | 2.972 | 1.807 | 0.6703 | 1.1 | 23.5 | 10.25 | 2.425 | 2.733 | 3.351 | 4.896 |  |  | — choix retenu |
| τ = 0.9 | 3.206 | 3.816 | 2.924 | 0.7256 | 1.0 | 12.0 | 11.36 | 3.206 | 3.346 | 3.628 | 4.332 | 0.0508 | 0.0896 | équivalent |


τ le moins coûteux pour chaque rapport de coûts r = c_pénurie / c_lit vide : r = 1 → τ = 0.5, r = 2 → τ = 0.7, r = 4 → τ = 0.8 (retenu), r = 9 → τ = 0.9. Le choix τ = 0.8 correspond à r = 4.


### D5 · Variables d'entrée

*Que rapporte chaque groupe de variables ? (même modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| 7 retards seuls | 1.931 | 2.457 | 0.029 | 0.9569 | 1.1 | 7 | 0.0454 | 0.3328 | équivalent |
| 7 retards + flux | 1.907 | 2.42 | 0.01 | 0.9506 | 1.3 | 10 | 0.0846 | 0.5076 | équivalent |
| 7 retards + calendrier (jour, mois) | 1.839 | 2.372 | -0.015 | 0.924 | 1.9 | 16 | 0.5044 | 1.0 | équivalent |
| Complet : retards + flux + calendrier (retenu) | 1.819 | 2.344 | -0.024 | 0.9167 | 1.9 | 19 |  |  | — choix retenu |
| Complet + jours fériés camerounais | 1.824 | 2.348 | -0.033 | 0.9218 | 2.1 | 21 | 0.0416 | 0.3328 | équivalent |
| Complet + vacances scolaires | 1.812 | 2.34 | -0.034 | 0.9161 | 1.6 | 20 | 0.8127 | 1.0 | équivalent |
| Complet + fériés + vacances scolaires | 1.819 | 2.345 | -0.043 | 0.9222 | 2.2 | 22 | 0.1152 | 0.576 | équivalent |
| 3 retards + flux + calendrier | 1.812 | 2.347 | -0.029 | 0.9148 | 1.7 | 15 | 0.8626 | 1.0 | équivalent |
| 14 retards + flux + calendrier | 1.839 | 2.402 | -0.014 | 0.9236 | 2.1 | 26 | 0.6798 | 1.0 | équivalent |
| Complet + diagnostics d'entrée des présents | 1.963 | 2.491 | -0.125 | 1.0189 | 2.0 | 30 | 0.0027 | 0.0243 | moins bon |


Plus petite perte pinball à τ = 0.8 : **3 retards + flux + calendrier** (0.9148). Aucune variante ne bat significativement le choix retenu (Complet : retards + flux + calendrier (retenu)) après correction de Holm.



### D6 · Prétraitement

*Quelle mise à l'échelle des variables ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| z-score : (x − moyenne)/écart-type (retenu) | 1.819 | 2.344 | -0.024 | 0.9167 | 1.8 |  |  | — choix retenu |
| Robuste : (x − médiane)/(Q3 − Q1) | 1.821 | 2.351 | 0.008 | 0.9082 | 1.8 | 0.3223 | 0.3223 | équivalent |
| Min-max : (x − min)/(max − min) | 2.116 | 2.665 | -0.12 | 1.0941 | 0.9 | 0.0004 | 0.0012 | moins bon |
| Aucune mise à l'échelle | 2.196 | 2.775 | 0.156 | 1.0512 | 1.6 | 0.0012 | 0.0024 | moins bon |


Plus petite perte pinball à τ = 0.8 : **Robuste : (x − médiane)/(Q3 − Q1)** (0.9082). Aucune variante ne bat significativement le choix retenu (z-score : (x − moyenne)/écart-type (retenu)) après correction de Holm.



### D7 · Fenêtre d'entraînement

*Faut-il tout le passé, ou seulement les derniers mois ? (mesure aussi le coût d'un historique court)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Croissante (tout le passé) (retenu) | 1.839 | 2.348 | 0.018 | 0.6789 | 85.8 | 12.8 |  |  | — choix retenu |
| Glissante : 365 derniers jours | 1.928 | 2.416 | -0.075 | 0.6911 | 80.9 | 8.1 | 0.5404 | 0.5404 | équivalent |
| Glissante : 180 derniers jours | 2.173 | 2.728 | 0.336 | 0.7841 | 78.7 | 6.6 | 0.0133 | 0.0266 | moins bon |
| Glissante : 90 derniers jours | 2.409 | 3.048 | 0.322 | 0.8833 | 74.3 | 5.9 | 0.0002 | 0.0006 | moins bon |


Plus petite perte pinball à τ = 0.8 : **Croissante (tout le passé) (retenu)** (0.6789). Aucune variante ne bat significativement le choix retenu (Croissante (tout le passé) (retenu)) après correction de Holm.



### D8 · Optimisation

*Comment atteindre le minimum de J le plus sûrement ? (SVR RBF, un découpage)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | J final | pas effectués | arrêt | solution gardée | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Adam + Polyak + préconditionnement + décroissance η (retenu) | 1.82 | 2.354 | -0.057 | 0.927 | 0.2 | 1938.55 | 724 | J stable depuis 100 pas (pas 723) | meilleur point rencontré |  |  | — choix retenu |
| Adam sans moyenne de Polyak | 1.82 | 2.354 | -0.057 | 0.927 | 0.2 | 1938.55 | 724 | J stable depuis 100 pas (pas 723) | meilleur point rencontré |  |  | identique |
| Adam sans préconditionnement | 1.829 | 2.359 | -0.017 | 0.9197 | 1.1 | 1985.34 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.2769 | 0.5538 | équivalent |
| Adam sans décroissance de η | 1.821 | 2.354 | -0.053 | 0.9265 | 0.8 | 1938.58 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.3654 | 0.5538 | équivalent |
| Momentum | 2.717 | 3.373 | -0.441 | 1.4908 | 0.7 | 3641.13 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | moins bon |
| Descente de gradient simple | 2.717 | 3.373 | -0.441 | 1.4908 | 0.6 | 3641.13 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | moins bon |


Plus petite perte pinball à τ = 0.8 : **Adam sans préconditionnement** (0.9197). Aucune variante ne bat significativement le choix retenu (Adam + Polyak + préconditionnement + décroissance η (retenu)) après correction de Holm.



### D9 · Combinaison des modèles

*Apprendre les poids de combinaison apporte-t-il plus qu'une moyenne ? (jours où l'empilement prédit)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Niveau 4 seul (meilleur modèle unique) | 1.811 | 2.306 | -0.026 | 0.6582 | 85.8 | 8.8 | 0.7081 | 1.0 | équivalent |
| Moyenne simple persistance + niv. 3 + niv. 4 | 1.825 | 2.345 | -0.058 | 0.6937 | 76.1 | 17.5 | 0.5131 | 1.0 | équivalent |
| Empilement appris (poids positifs) (retenu) | 1.9 | 2.404 | -0.215 | 0.6675 | 87.7 | 28.6 |  |  | — choix retenu |
| XGBoost quantile seul | 1.905 | 2.438 | -0.188 | 0.7197 | 85.8 | 14.5 | 0.0568 | 0.284 | équivalent |
| Moyenne SVR niv. 4 + XGBoost | 1.834 | 2.329 | -0.107 | 0.6715 | 87.7 | 23.2 | 0.8464 | 1.0 | équivalent |
| Empilement persistance + niv. 3 + niv. 4 + XGBoost | 1.913 | 2.409 | -0.255 | 0.6832 | 87.7 | 42.6 | 0.1441 | 0.5764 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Niveau 4 seul (meilleur modèle unique)** (0.6582). Aucune variante ne bat significativement le choix retenu (Empilement appris (poids positifs) (retenu)) après correction de Holm.



### D13 · Variantes de SVM

*Quel SVM est le plus adapté à la série du service ? (mêmes jours, mêmes variables)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | cle | couverture 90 % | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| SVR linéaire (niveau 1) | 1.809 | 2.371 | -0.038 | 0.916 | 0.4 | svr_lineaire |  | 0.0 | 0.0 | moins bon |
| SVR RBF (niveau 2) | 1.819 | 2.344 | -0.024 | 0.9167 | 1.9 | svr_rbf |  | 0.0 | 0.0 | moins bon |
| SVR quantile RBF (niveau 3) | 1.862 | 2.374 | -0.093 | 0.6703 | 6.6 | svr_q_rbf | 86.9 | 0.5135 | 1.0 | équivalent |
| SVR quantile composite (niveau 4, retenu) (retenu) | 1.839 | 2.348 | 0.018 | 0.6789 | 12.5 | svr_q_composite | 85.8 |  |  | — choix retenu |
| SVR quantile, noyau laplacien | 1.944 | 2.442 | -0.192 | 0.7001 | 5.6 | svr_q_laplacien | 89.1 | 0.258 | 0.8624 | équivalent |
| SVR quantile, noyau polynomial (degré 2) | 1.822 | 2.375 | -0.096 | 0.6765 | 7.4 | svr_q_polynomial | 82.5 | 0.9097 | 1.0 | équivalent |
| LS-SVR (moindres carrés), noyau RBF, quantiles LOO | 1.829 | 2.367 | -0.186 | 0.6529 | 0.2 | lssvr_rbf | 89.6 | 0.2156 | 0.8624 | équivalent |


Plus petite perte pinball à τ = 0.8 : **LS-SVR (moindres carrés), noyau RBF, quantiles LOO** (0.6529). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4, retenu) (retenu)) après correction de Holm.



### D11 · Chaque variable, une à une

*Que perd le modèle si on lui retire cette seule variable ? (modèle RBF du niveau 2, mêmes jours)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 1.819 | 2.344 | -0.024 | 0.9167 | 2.0 |  |  | — choix retenu |
| Sans occ_j-0 | 1.978 | 2.483 | -0.034 | 0.9992 | 1.5 | 0.0173 | 0.3114 | équivalent |
| Sans occ_j-1 | 1.817 | 2.338 | -0.024 | 0.9155 | 2.0 | 0.8713 | 1.0 | équivalent |
| Sans occ_j-2 | 1.822 | 2.355 | -0.045 | 0.9244 | 1.8 | 0.3261 | 1.0 | équivalent |
| Sans occ_j-3 | 1.828 | 2.356 | -0.022 | 0.9206 | 1.6 | 0.5437 | 1.0 | équivalent |
| Sans occ_j-4 | 1.816 | 2.339 | -0.037 | 0.919 | 1.7 | 0.4636 | 1.0 | équivalent |
| Sans occ_j-5 | 1.812 | 2.344 | -0.035 | 0.9165 | 1.6 | 0.9644 | 1.0 | équivalent |
| Sans occ_j-6 | 1.794 | 2.323 | -0.035 | 0.9072 | 1.9 | 0.1467 | 1.0 | équivalent |
| Sans adm_3j | 1.829 | 2.35 | -0.007 | 0.9168 | 2.1 | 0.992 | 1.0 | équivalent |
| Sans adm_7j | 1.813 | 2.344 | -0.031 | 0.9158 | 1.7 | 0.8195 | 1.0 | équivalent |
| Sans sorties_7j | 1.829 | 2.364 | -0.024 | 0.9215 | 2.1 | 0.5612 | 1.0 | équivalent |
| Sans cible_jour_0 | 1.821 | 2.347 | -0.037 | 0.9218 | 1.6 | 0.057 | 0.969 | équivalent |
| Sans cible_jour_1 | 1.819 | 2.333 | -0.043 | 0.9223 | 2.0 | 0.4623 | 1.0 | équivalent |
| Sans cible_jour_2 | 1.818 | 2.343 | -0.032 | 0.9186 | 2.2 | 0.2294 | 1.0 | équivalent |
| Sans cible_jour_3 | 1.817 | 2.34 | -0.032 | 0.9178 | 2.2 | 0.4255 | 1.0 | équivalent |
| Sans cible_jour_4 | 1.83 | 2.347 | -0.001 | 0.9152 | 2.1 | 0.8189 | 1.0 | équivalent |
| Sans cible_jour_5 | 1.831 | 2.345 | -0.002 | 0.9159 | 1.9 | 0.8938 | 1.0 | équivalent |
| Sans cible_jour_6 | 1.834 | 2.359 | -0.041 | 0.9292 | 2.1 | 0.0873 | 1.0 | équivalent |
| Sans mois_sin | 1.845 | 2.37 | -0.024 | 0.9296 | 1.6 | 0.0894 | 1.0 | équivalent |
| Sans mois_cos | 1.811 | 2.351 | 0.063 | 0.8865 | 1.9 | 0.0021 | 0.0399 | meilleur |


Plus petite perte pinball à τ = 0.8 : **Sans mois_cos** (0.8865). ⚠ Significativement meilleur que le choix retenu (Holm, 5 %) : Sans mois_cos — le choix est à revoir.



### D14 · Sélection des variables par le lasso

*Le modèle gagne-t-il à ne garder que les variables choisies par le lasso ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 1.819 | 2.344 | -0.024 | 0.9167 | 2.1 | 19.0 |  |  | — choix retenu |
| Lasso, λ de plus petite erreur | 1.844 | 2.373 | -0.043 | 0.9349 | 17.6 | 16.4 | 0.021 | 0.042 | moins bon |
| Lasso à un écart-type (λ_1se) | 1.911 | 2.431 | -0.062 | 0.974 | 15.1 | 1.0 | 0.021 | 0.042 | moins bon |


Plus petite perte pinball à τ = 0.8 : **Toutes les variables (retenu)** (0.9167). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)) après correction de Holm.



## Horizon J+7 — 177 jours évalués, 7 origines


### D1 · Modèles de référence, concurrents et SVR

*Le SVR fait-il mieux que les méthodes statistiques usuelles et que les autres modèles d'apprentissage ?*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | couverture 90 % | réglages | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Persistance | 3.934 | 4.828 | 0.249 | 1.8923 | 0.0 |  |  | 0.0002 | 0.0032 | moins bon |
| Saisonnière hebdomadaire | 3.055 | 3.704 | 0.339 | 1.4259 | 0.0 |  |  | 0.0133 | 0.1512 | équivalent |
| Moyenne mobile 7 j | 3.61 | 4.287 | 0.246 | 1.7309 | 0.0 |  |  | 0.002 | 0.03 | moins bon |
| Moyenne historique | 2.736 | 3.347 | 0.1 | 0.9891 | 0.0 | 89.3 |  | 0.5094 | 1.0 | équivalent |
| Lissage exponentiel simple | 3.919 | 4.805 | 0.249 | 1.389 | 0.0 | 87.0 |  | 0.0 | 0.0 | moins bon |
| Méthode Thêta | 3.917 | 4.804 | 0.239 | 1.389 | 0.0 | 87.0 |  | 0.0 | 0.0 | moins bon |
| Holt linéaire | 3.919 | 4.805 | 0.249 | 1.389 | 0.2 | 87.0 |  | 0.0 | 0.0 | moins bon |
| Holt amorti | 3.919 | 4.805 | 0.249 | 1.389 | 0.2 | 87.0 |  | 0.0 | 0.0 | moins bon |
| Lissage saisonnier sans tendance | 3.913 | 4.797 | 0.25 | 1.3877 | 0.2 | 87.0 |  | 0.0 | 0.0 | moins bon |
| Holt-Winters additif amorti | 3.934 | 4.828 | 0.249 | 1.3911 | 0.5 | 88.1 |  | 0.0 | 0.0 | moins bon |
| Holt-Winters multiplicatif amorti | 3.93 | 4.821 | 0.25 | 1.3908 | 1.0 | 87.6 |  | 0.0 | 0.0 | moins bon |
| AR(p) par AIC | 2.829 | 3.465 | 0.25 | 1.0301 | 0.2 | 84.2 |  | 0.1506 | 1.0 | équivalent |
| SARIMA(2,1,1)(1,0,0)7 (ordre choisi sur l'apprentissage) | 2.871 | 3.509 | 0.241 | 0.9972 | 14.1 | 88.1 |  | 0.331 | 1.0 | équivalent |
| Holt-Winters additif, grille fixée avant la validation | 3.111 | 3.73 | 0.292 | 1.4679 | 0.3 |  | alpha=0.1, beta=0.0, gamma=0.05, phi=0.98 | 0.0128 | 0.1512 | équivalent |
| Régression ridge (λ = 1) | 2.839 | 3.507 | -0.158 | 1.4668 | 0.1 |  |  | 0.0074 | 0.0962 | équivalent |
| A · forêt aléatoire quantile | 2.756 | 3.353 | -0.183 | 0.9926 | 22.4 | 91.5 |  | 0.2397 | 1.0 | équivalent |
| B · gradient boosting quantile | 2.885 | 3.54 | -0.349 | 1.0299 | 13.1 | 73.4 |  | 0.1525 | 1.0 | équivalent |
| C · perceptron multicouche quantile | 2.838 | 3.5 | -0.334 | 1.008 | 1.3 | 84.7 |  | 0.1598 | 1.0 | équivalent |
| D · LSTM quantile | 2.953 | 3.62 | -0.15 | 1.0173 | 12.2 | 85.3 |  | 0.0627 | 0.5643 | équivalent |
| E · XGBoost quantile (second ordre) | 2.839 | 3.459 | -0.266 | 1.0095 | 16.0 | 83.6 |  | 0.1113 | 0.8904 | équivalent |
| SVR linéaire (niveau 1) | 2.849 | 3.54 | -0.303 | 1.5155 | 0.2 |  |  | 0.0059 | 0.0826 | équivalent |
| SVR RBF (niveau 2) | 2.763 | 3.371 | 0.048 | 1.3671 | 0.3 |  |  | 0.0126 | 0.1512 | équivalent |
| SVR quantile RBF (niveau 3) | 2.738 | 3.353 | 0.02 | 0.9531 | 1.7 | 89.3 |  | 0.8655 | 1.0 | équivalent |
| SVR quantile composite (niveau 4) (retenu) | 2.687 | 3.306 | -0.123 | 0.9574 | 12.0 | 89.3 |  |  |  | — choix retenu |


Plus petite perte pinball à τ = 0.8 : **SVR quantile RBF (niveau 3)** (0.9531). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4) (retenu)) après correction de Holm.



### D2 · Noyau

*Quel noyau décrit le mieux la dynamique ? (même perte ε-insensible, même C)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Linéaire | 2.849 | 3.54 | -0.303 | 1.5155 | 0.2 | 0.0579 | 0.1158 | équivalent |
| RBF (γ = 0.2) | 2.763 | 3.371 | 0.048 | 1.3671 | 0.3 | 0.2835 | 0.2835 | équivalent |
| Composite occupation / flux et saison (β appris) (retenu) | 2.682 | 3.308 | -0.217 | 1.4064 | 1.5 |  |  | — choix retenu |


Plus petite perte pinball à τ = 0.8 : **RBF (γ = 0.2)** (1.3671). Aucune variante ne bat significativement le choix retenu (Composite occupation / flux et saison (β appris) (retenu)) après correction de Holm.



### D3 · Fonction de perte

*Quelle perte pour un modèle linéaire identique ? (isole l'effet de la perte)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Carrée (ridge, λ = 1/C) | 2.837 | 3.505 | -0.157 | 1.4656 | 0.1 | 0.0032 | 0.0128 | meilleur |
| ε-insensible, ε = 0 lit (= valeur absolue) | 2.852 | 3.529 | -0.238 | 1.4973 | 0.4 | 0.0992 | 0.1984 | équivalent |
| ε-insensible, ε = 0.5 lit (retenu) | 2.849 | 3.54 | -0.303 | 1.5155 | 0.2 |  |  | — choix retenu |
| ε-insensible, ε = 1 lit | 2.851 | 3.537 | -0.281 | 1.5097 | 0.3 | 0.1833 | 0.1984 | équivalent |
| ε-insensible, ε = 2 lit | 2.881 | 3.554 | -0.176 | 1.4936 | 0.5 | 0.066 | 0.198 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Carrée (ridge, λ = 1/C)** (1.4656). ⚠ Significativement meilleur que le choix retenu (Holm, 5 %) : Carrée (ridge, λ = 1/C) — le choix est à revoir.



### D4 · Quantile décisionnel τ et coût des décisions

*Quel τ minimise le coût réel selon le rapport pénurie / lit vide ? (τ optimal théorique = r/(1+r))*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | jours sous-estimés % | lits prévus en moyenne | coût r=1 | coût r=2 | coût r=4 | coût r=9 | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| τ = 0.5 | 2.738 | 3.353 | 0.02 | 1.3627 | 0.3 | 45.8 | 8.43 | 2.738 | 4.096 | 6.813 | 13.607 | 0.0256 | 0.1024 | équivalent |
| τ = 0.6 | 2.874 | 3.478 | 0.86 | 1.179 | 0.3 | 38.4 | 9.27 | 2.874 | 3.881 | 5.895 | 10.93 | 0.0815 | 0.2055 | équivalent |
| τ = 0.7 | 3.144 | 3.807 | 1.762 | 1.0435 | 0.3 | 31.6 | 10.17 | 3.144 | 3.836 | 5.218 | 8.673 | 0.2321 | 0.2321 | équivalent |
| τ = 0.8 (retenu) | 3.78 | 4.592 | 3.122 | 0.9531 | 0.3 | 20.9 | 11.53 | 3.78 | 4.108 | 4.766 | 6.409 |  |  | — choix retenu |
| τ = 0.9 | 5.082 | 5.944 | 4.899 | 1.0712 | 0.3 | 7.9 | 13.3 | 5.082 | 5.173 | 5.356 | 5.813 | 0.0685 | 0.2055 | équivalent |


τ le moins coûteux pour chaque rapport de coûts r = c_pénurie / c_lit vide : r = 1 → τ = 0.5, r = 2 → τ = 0.7, r = 4 → τ = 0.8 (retenu), r = 9 → τ = 0.9. Le choix τ = 0.8 correspond à r = 4.


### D5 · Variables d'entrée

*Que rapporte chaque groupe de variables ? (même modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| 7 retards seuls | 2.869 | 3.543 | 0.125 | 1.3969 | 0.3 | 7 | 0.4839 | 1.0 | équivalent |
| 7 retards + flux | 2.861 | 3.495 | 0.087 | 1.4042 | 0.4 | 10 | 0.0378 | 0.3024 | équivalent |
| 7 retards + calendrier (jour, mois) | 2.76 | 3.387 | -0.015 | 1.3846 | 0.3 | 16 | 0.018 | 0.162 | équivalent |
| Complet : retards + flux + calendrier (retenu) | 2.763 | 3.371 | 0.048 | 1.3671 | 0.3 | 19 |  |  | — choix retenu |
| Complet + jours fériés camerounais | 2.758 | 3.365 | 0.048 | 1.3649 | 0.4 | 21 | 0.4975 | 1.0 | équivalent |
| Complet + vacances scolaires | 2.763 | 3.372 | 0.04 | 1.3693 | 0.3 | 20 | 0.6273 | 1.0 | équivalent |
| Complet + fériés + vacances scolaires | 2.759 | 3.367 | 0.039 | 1.3678 | 0.4 | 22 | 0.8683 | 1.0 | équivalent |
| 3 retards + flux + calendrier | 2.729 | 3.334 | -0.053 | 1.3803 | 0.3 | 15 | 0.4564 | 1.0 | équivalent |
| 14 retards + flux + calendrier | 2.743 | 3.35 | 0.052 | 1.3561 | 0.3 | 26 | 0.7071 | 1.0 | équivalent |
| Complet + diagnostics d'entrée des présents | 2.738 | 3.353 | 0.053 | 1.3531 | 0.4 | 30 | 0.6848 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Complet + diagnostics d'entrée des présents** (1.3531). Aucune variante ne bat significativement le choix retenu (Complet : retards + flux + calendrier (retenu)) après correction de Holm.



### D6 · Prétraitement

*Quelle mise à l'échelle des variables ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| z-score : (x − moyenne)/écart-type (retenu) | 2.763 | 3.371 | 0.048 | 1.3671 | 0.3 |  |  | — choix retenu |
| Robuste : (x − médiane)/(Q3 − Q1) | 2.802 | 3.44 | 0.003 | 1.4003 | 0.8 | 0.0309 | 0.0927 | équivalent |
| Min-max : (x − min)/(max − min) | 2.758 | 3.414 | -0.125 | 1.4166 | 0.5 | 0.1741 | 0.3482 | équivalent |
| Aucune mise à l'échelle | 2.727 | 3.341 | 0.065 | 1.3443 | 0.5 | 0.6253 | 0.6253 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Aucune mise à l'échelle** (1.3443). Aucune variante ne bat significativement le choix retenu (z-score : (x − moyenne)/écart-type (retenu)) après correction de Holm.



### D7 · Fenêtre d'entraînement

*Faut-il tout le passé, ou seulement les derniers mois ? (mesure aussi le coût d'un historique court)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Croissante (tout le passé) (retenu) | 2.687 | 3.306 | -0.123 | 0.9574 | 89.3 | 11.6 |  |  | — choix retenu |
| Glissante : 365 derniers jours | 2.699 | 3.348 | -0.444 | 1.0049 | 82.5 | 8.1 | 0.2079 | 0.6237 | équivalent |
| Glissante : 180 derniers jours | 2.732 | 3.377 | -0.382 | 0.9628 | 85.3 | 5.4 | 0.894 | 1.0 | équivalent |
| Glissante : 90 derniers jours | 2.841 | 3.447 | -0.046 | 0.965 | 81.9 | 4.7 | 0.8943 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Croissante (tout le passé) (retenu)** (0.9574). Aucune variante ne bat significativement le choix retenu (Croissante (tout le passé) (retenu)) après correction de Holm.



### D8 · Optimisation

*Comment atteindre le minimum de J le plus sûrement ? (SVR RBF, un découpage)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | J final | pas effectués | arrêt | solution gardée | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Adam + Polyak + préconditionnement + décroissance η (retenu) | 2.748 | 3.358 | 0.004 | 1.3731 | 0.1 | 398.35 | 302 | J stable depuis 100 pas (pas 301) | moyenne de Polyak sur 100 pas |  |  | — choix retenu |
| Adam sans moyenne de Polyak | 2.749 | 3.359 | 0.002 | 1.3738 | 0.1 | 398.36 | 302 | J stable depuis 100 pas (pas 301) | meilleur point rencontré | 0.0003 | 0.0015 | moins bon |
| Adam sans préconditionnement | 2.749 | 3.358 | -0.001 | 1.3745 | 1.1 | 398.38 | 2362 | J stable depuis 100 pas (pas 2361) | moyenne de Polyak sur 861 pas | 0.0005 | 0.002 | moins bon |
| Adam sans décroissance de η | 2.749 | 3.358 | 0.004 | 1.373 | 0.1 | 398.36 | 310 | J stable depuis 100 pas (pas 309) | moyenne de Polyak sur 100 pas | 0.2151 | 0.2151 | équivalent |
| Momentum | 2.749 | 3.359 | -0.0 | 1.3747 | 0.8 | 398.38 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0007 | 0.0021 | moins bon |
| Descente de gradient simple | 2.748 | 3.358 | -0.006 | 1.3759 | 0.8 | 398.41 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0009 | 0.0021 | moins bon |


Plus petite perte pinball à τ = 0.8 : **Adam sans décroissance de η** (1.373). Aucune variante ne bat significativement le choix retenu (Adam + Polyak + préconditionnement + décroissance η (retenu)) après correction de Holm.



### D9 · Combinaison des modèles

*Apprendre les poids de combinaison apporte-t-il plus qu'une moyenne ? (jours où l'empilement prédit)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Niveau 4 seul (meilleur modèle unique) | 2.782 | 3.381 | -0.333 | 0.9719 | 89.3 | 7.3 | 0.2479 | 0.9916 | équivalent |
| Moyenne simple persistance + niv. 3 + niv. 4 | 3.08 | 3.734 | -0.106 | 1.1556 | 62.4 | 14.6 | 0.5059 | 1.0 | équivalent |
| Empilement appris (poids positifs) (retenu) | 2.944 | 3.552 | -0.375 | 1.0873 | 80.5 | 26.5 |  |  | — choix retenu |
| XGBoost quantile seul | 2.93 | 3.559 | -0.572 | 1.0405 | 82.6 | 16.1 | 0.6262 | 1.0 | équivalent |
| Moyenne SVR niv. 4 + XGBoost | 2.841 | 3.45 | -0.452 | 0.9998 | 85.9 | 23.5 | 0.3584 | 1.0 | équivalent |
| Empilement persistance + niv. 3 + niv. 4 + XGBoost | 3.002 | 3.62 | -0.444 | 1.1026 | 81.2 | 42.5 | 0.0852 | 0.426 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Niveau 4 seul (meilleur modèle unique)** (0.9719). Aucune variante ne bat significativement le choix retenu (Empilement appris (poids positifs) (retenu)) après correction de Holm.



### D13 · Variantes de SVM

*Quel SVM est le plus adapté à la série du service ? (mêmes jours, mêmes variables)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | cle | couverture 90 % | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| SVR linéaire (niveau 1) | 2.849 | 3.54 | -0.303 | 1.5155 | 0.2 | svr_lineaire |  | 0.0059 | 0.0354 | moins bon |
| SVR RBF (niveau 2) | 2.763 | 3.371 | 0.048 | 1.3671 | 0.3 | svr_rbf |  | 0.0126 | 0.063 | équivalent |
| SVR quantile RBF (niveau 3) | 2.738 | 3.353 | 0.02 | 0.9531 | 1.6 | svr_q_rbf | 89.3 | 0.8655 | 1.0 | équivalent |
| SVR quantile composite (niveau 4, retenu) (retenu) | 2.687 | 3.306 | -0.123 | 0.9574 | 11.0 | svr_q_composite | 89.3 |  |  | — choix retenu |
| SVR quantile, noyau laplacien | 2.735 | 3.367 | -0.006 | 0.9609 | 2.5 | svr_q_laplacien | 89.3 | 0.8938 | 1.0 | équivalent |
| SVR quantile, noyau polynomial (degré 2) | 2.805 | 3.46 | -0.212 | 1.0115 | 5.9 | svr_q_polynomial | 88.7 | 0.0776 | 0.3104 | équivalent |
| LS-SVR (moindres carrés), noyau RBF, quantiles LOO | 2.77 | 3.364 | 0.023 | 0.9397 | 0.2 | lssvr_rbf | 89.3 | 0.4951 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **LS-SVR (moindres carrés), noyau RBF, quantiles LOO** (0.9397). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4, retenu) (retenu)) après correction de Holm.



### D11 · Chaque variable, une à une

*Que perd le modèle si on lui retire cette seule variable ? (modèle RBF du niveau 2, mêmes jours)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 2.763 | 3.371 | 0.048 | 1.3671 | 0.3 |  |  | — choix retenu |
| Sans occ_j-0 | 2.766 | 3.37 | 0.014 | 1.3789 | 0.4 | 0.0841 | 1.0 | équivalent |
| Sans occ_j-1 | 2.763 | 3.37 | 0.031 | 1.3722 | 0.5 | 0.231 | 1.0 | équivalent |
| Sans occ_j-2 | 2.764 | 3.374 | 0.026 | 1.374 | 0.3 | 0.0335 | 0.6365 | équivalent |
| Sans occ_j-3 | 2.762 | 3.374 | 0.032 | 1.3713 | 0.5 | 0.238 | 1.0 | équivalent |
| Sans occ_j-4 | 2.763 | 3.371 | 0.036 | 1.3703 | 0.4 | 0.089 | 1.0 | équivalent |
| Sans occ_j-5 | 2.761 | 3.363 | 0.027 | 1.3726 | 0.3 | 0.0689 | 1.0 | équivalent |
| Sans occ_j-6 | 2.758 | 3.363 | 0.024 | 1.3718 | 0.4 | 0.4809 | 1.0 | équivalent |
| Sans adm_3j | 2.765 | 3.374 | 0.013 | 1.3784 | 0.3 | 0.104 | 1.0 | équivalent |
| Sans adm_7j | 2.764 | 3.376 | 0.045 | 1.3684 | 0.3 | 0.7757 | 1.0 | équivalent |
| Sans sorties_7j | 2.754 | 3.367 | 0.03 | 1.3682 | 0.4 | 0.8344 | 1.0 | équivalent |
| Sans cible_jour_0 | 2.764 | 3.367 | 0.047 | 1.368 | 0.4 | 0.6289 | 1.0 | équivalent |
| Sans cible_jour_1 | 2.768 | 3.374 | 0.06 | 1.366 | 0.3 | 0.4128 | 1.0 | équivalent |
| Sans cible_jour_2 | 2.763 | 3.371 | 0.049 | 1.367 | 0.5 | 0.9664 | 1.0 | équivalent |
| Sans cible_jour_3 | 2.764 | 3.372 | 0.042 | 1.3693 | 0.6 | 0.2633 | 1.0 | équivalent |
| Sans cible_jour_4 | 2.769 | 3.369 | 0.053 | 1.3689 | 0.4 | 0.4696 | 1.0 | équivalent |
| Sans cible_jour_5 | 2.766 | 3.37 | 0.043 | 1.3702 | 0.4 | 0.1054 | 1.0 | équivalent |
| Sans cible_jour_6 | 2.762 | 3.37 | 0.041 | 1.3687 | 0.4 | 0.4635 | 1.0 | équivalent |
| Sans mois_sin | 2.795 | 3.426 | -0.001 | 1.3979 | 0.5 | 0.2114 | 1.0 | équivalent |
| Sans mois_cos | 2.8 | 3.425 | 0.104 | 1.3687 | 0.4 | 0.9022 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Sans cible_jour_1** (1.366). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)) après correction de Holm.



### D14 · Sélection des variables par le lasso

*Le modèle gagne-t-il à ne garder que les variables choisies par le lasso ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 2.763 | 3.371 | 0.048 | 1.3671 | 0.3 | 19.0 |  |  | — choix retenu |
| Lasso, λ de plus petite erreur | 2.823 | 3.484 | 0.063 | 1.3926 | 20.2 | 1.0 | 0.5249 | 1.0 | équivalent |
| Lasso à un écart-type (λ_1se) | 2.823 | 3.484 | 0.063 | 1.3926 | 19.7 | 1.0 | 0.5249 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Toutes les variables (retenu)** (1.3671). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)) après correction de Holm.

