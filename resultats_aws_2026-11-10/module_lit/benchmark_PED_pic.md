# Banc de comparaison des choix — service PED_pic

Validation glissante du 01/03/2026 au verrou (01/09/2026), une origine tous les 28 jours, modèle réentraîné à chaque origine. « (retenu) » = choix retenu. Test de Diebold-Mariano (perte absolue, correction HLN) contre le choix retenu.


## Horizon J+1 — 183 jours évalués, 7 origines


### D1 · Modèles de référence, concurrents et SVR

*Le SVR fait-il mieux que les méthodes statistiques usuelles et que les autres modèles d'apprentissage ?*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | couverture 90 % | réglages | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Persistance | 1.631 | 2.205 | 0.019 | 0.8097 | 0.0 |  |  | 0.0 | 0.0 | moins bon |
| Saisonnière hebdomadaire | 3.056 | 3.66 | 0.327 | 1.4302 | 0.0 |  |  | 0.0 | 0.0 | moins bon |
| Moyenne mobile 7 j | 2.62 | 3.281 | 0.112 | 1.2766 | 0.0 |  |  | 0.0 | 0.0 | moins bon |
| Moyenne historique | 2.759 | 3.326 | 0.103 | 0.9696 | 0.0 | 89.1 |  | 0.0 | 0.0 | moins bon |
| Lissage exponentiel simple | 1.631 | 2.205 | 0.019 | 0.6078 | 0.0 | 88.5 |  | 0.0003 | 0.0054 | moins bon |
| Méthode Thêta | 1.631 | 2.205 | 0.017 | 0.6078 | 0.0 | 88.5 |  | 0.0003 | 0.0054 | moins bon |
| Holt linéaire | 1.637 | 2.212 | 0.03 | 0.6098 | 0.2 | 88.5 |  | 0.0003 | 0.0054 | moins bon |
| Holt amorti | 1.631 | 2.205 | 0.019 | 0.6078 | 0.1 | 88.5 |  | 0.0003 | 0.0054 | moins bon |
| Lissage saisonnier sans tendance | 1.55 | 2.097 | 0.025 | 0.5899 | 0.2 | 88.5 |  | 0.0013 | 0.0156 | moins bon |
| Holt-Winters additif amorti | 1.55 | 2.097 | 0.025 | 0.5899 | 0.6 | 88.5 |  | 0.0013 | 0.0156 | moins bon |
| Holt-Winters multiplicatif amorti | 1.686 | 2.224 | 0.073 | 0.6029 | 0.6 | 89.6 |  | 0.0009 | 0.0126 | moins bon |
| AR(p) par AIC | 1.483 | 2.013 | 0.079 | 0.563 | 0.1 | 88.5 |  | 0.0547 | 0.2735 | équivalent |
| SARIMA(2,1,1)(1,0,0)7 (ordre choisi sur l'apprentissage) | 1.495 | 2.02 | 0.104 | 0.5682 | 14.3 | 89.1 |  | 0.0164 | 0.0984 | équivalent |
| Holt-Winters additif, grille fixée avant la validation | 1.592 | 2.13 | 0.028 | 0.7875 | 0.2 |  | alpha=0.9, beta=0.0, gamma=0.3, phi=0.8 | 0.0 | 0.0 | moins bon |
| Régression ridge (λ = 1) | 1.282 | 1.751 | 0.067 | 0.6209 | 0.1 |  |  | 0.0022 | 0.0168 | moins bon |
| A · forêt aléatoire quantile | 1.52 | 2.011 | 0.052 | 0.575 | 22.3 | 94.0 |  | 0.0015 | 0.0156 | moins bon |
| B · gradient boosting quantile | 1.377 | 1.907 | 0.067 | 0.5388 | 11.8 | 80.3 |  | 0.0731 | 0.2924 | équivalent |
| C · perceptron multicouche quantile | 1.314 | 1.761 | -0.045 | 0.4678 | 1.4 | 90.7 |  | 0.1426 | 0.4278 | équivalent |
| D · LSTM quantile | 1.287 | 1.761 | -0.029 | 0.5004 | 15.6 | 89.1 |  | 0.9572 | 1.0 | équivalent |
| E · XGBoost quantile (second ordre) | 1.426 | 1.899 | 0.047 | 0.5732 | 15.0 | 90.2 |  | 0.0021 | 0.0168 | moins bon |
| SVR linéaire (niveau 1) | 1.265 | 1.771 | 0.002 | 0.6319 | 0.4 |  |  | 0.0013 | 0.0156 | moins bon |
| SVR RBF (niveau 2) | 1.256 | 1.724 | -0.008 | 0.6302 | 2.0 |  |  | 0.001 | 0.013 | moins bon |
| SVR quantile RBF (niveau 3) | 1.307 | 1.783 | -0.048 | 0.4914 | 6.5 | 87.4 |  | 0.5074 | 1.0 | équivalent |
| SVR quantile composite (niveau 4) (retenu) | 1.336 | 1.823 | 0.039 | 0.4993 | 13.5 | 89.1 |  |  |  | — choix retenu |


Plus petite perte pinball à τ = 0.8 : **C · perceptron multicouche quantile** (0.4678). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4) (retenu)) après correction de Holm.



### D2 · Noyau

*Quel noyau décrit le mieux la dynamique ? (même perte ε-insensible, même C)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Linéaire | 1.271 | 1.768 | -0.022 | 0.6418 | 0.5 | 0.8313 | 0.8313 | équivalent |
| RBF (γ = 0.02) | 1.256 | 1.724 | -0.008 | 0.6302 | 2.1 | 0.3772 | 0.7544 | équivalent |
| Composite occupation / flux et saison (β appris) (retenu) | 1.305 | 1.789 | 0.019 | 0.6468 | 3.6 |  |  | — choix retenu |


Plus petite perte pinball à τ = 0.8 : **RBF (γ = 0.02)** (0.6302). Aucune variante ne bat significativement le choix retenu (Composite occupation / flux et saison (β appris) (retenu)) après correction de Holm.



### D3 · Fonction de perte

*Quelle perte pour un modèle linéaire identique ? (isole l'effet de la perte)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Carrée (ridge, λ = 1/C) | 1.277 | 1.749 | 0.067 | 0.6188 | 0.1 | 0.0691 | 0.2073 | équivalent |
| ε-insensible, ε = 0 lit (= valeur absolue) | 1.259 | 1.761 | -0.04 | 0.6414 | 0.5 | 0.2774 | 0.5548 | équivalent |
| ε-insensible, ε = 0.5 lit | 1.261 | 1.76 | -0.007 | 0.6328 | 0.4 | 0.8709 | 0.8709 | équivalent |
| ε-insensible, ε = 1 lit (retenu) | 1.265 | 1.771 | 0.002 | 0.6319 | 0.4 |  |  | — choix retenu |
| ε-insensible, ε = 2 lit | 1.285 | 1.748 | 0.164 | 0.5932 | 0.7 | 0.0007 | 0.0028 | meilleur |


Plus petite perte pinball à τ = 0.8 : **ε-insensible, ε = 2 lit** (0.5932). ⚠ Significativement meilleur que le choix retenu (Holm, 5 %) : ε-insensible, ε = 2 lit — le choix est à revoir.



### D4 · Quantile décisionnel τ et coût des décisions

*Quel τ minimise le coût réel selon le rapport pénurie / lit vide ? (τ optimal théorique = r/(1+r))*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | jours sous-estimés % | lits prévus en moyenne | coût r=1 | coût r=2 | coût r=4 | coût r=9 | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| τ = 0.5 | 1.307 | 1.782 | -0.048 | 0.6676 | 2.0 | 51.4 | 9.81 | 1.307 | 1.984 | 3.338 | 6.724 | 0.0 | 0.0 | moins bon |
| τ = 0.6 | 1.318 | 1.794 | 0.314 | 0.5648 | 2.0 | 42.1 | 10.17 | 1.318 | 1.82 | 2.824 | 5.334 | 0.0058 | 0.0174 | moins bon |
| τ = 0.7 | 1.405 | 1.869 | 0.629 | 0.514 | 2.1 | 33.3 | 10.49 | 1.405 | 1.793 | 2.57 | 4.511 | 0.1427 | 0.1427 | équivalent |
| τ = 0.8 (retenu) | 1.626 | 2.071 | 1.072 | 0.4915 | 1.7 | 21.3 | 10.93 | 1.626 | 1.903 | 2.458 | 3.843 |  |  | — choix retenu |
| τ = 0.9 | 2.452 | 2.936 | 2.223 | 0.559 | 1.8 | 10.4 | 12.08 | 2.452 | 2.566 | 2.795 | 3.367 | 0.0188 | 0.0376 | moins bon |


τ le moins coûteux pour chaque rapport de coûts r = c_pénurie / c_lit vide : r = 1 → τ = 0.5, r = 2 → τ = 0.7, r = 4 → τ = 0.8 (retenu), r = 9 → τ = 0.9. Le choix τ = 0.8 correspond à r = 4.


### D5 · Variables d'entrée

*Que rapporte chaque groupe de variables ? (même modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| 7 retards seuls | 1.509 | 2.05 | 0.048 | 0.7403 | 1.3 | 7 | 0.0003 | 0.0027 | moins bon |
| 7 retards + flux | 1.397 | 1.869 | 0.096 | 0.6695 | 1.6 | 10 | 0.0164 | 0.082 | équivalent |
| 7 retards + calendrier (jour, mois) | 1.392 | 1.909 | -0.079 | 0.7199 | 1.8 | 16 | 0.0015 | 0.0105 | moins bon |
| Complet : retards + flux + calendrier (retenu) | 1.256 | 1.724 | -0.008 | 0.6302 | 2.1 | 19 |  |  | — choix retenu |
| Complet + jours fériés camerounais | 1.262 | 1.729 | -0.009 | 0.6337 | 2.0 | 21 | 0.0292 | 0.1168 | équivalent |
| Complet + vacances scolaires | 1.249 | 1.714 | -0.001 | 0.6247 | 2.1 | 20 | 0.1044 | 0.3132 | équivalent |
| Complet + fériés + vacances scolaires | 1.253 | 1.716 | 0.006 | 0.6248 | 1.9 | 22 | 0.1651 | 0.3302 | équivalent |
| 3 retards + flux + calendrier | 1.277 | 1.772 | -0.144 | 0.6817 | 2.1 | 15 | 0.0042 | 0.0252 | moins bon |
| 14 retards + flux + calendrier | 1.285 | 1.746 | 0.012 | 0.6387 | 2.2 | 26 | 0.5608 | 0.5608 | équivalent |
| Complet + diagnostics d'entrée des présents | 1.428 | 1.868 | -0.032 | 0.7234 | 2.3 | 30 | 0.0003 | 0.0027 | moins bon |


Plus petite perte pinball à τ = 0.8 : **Complet + vacances scolaires** (0.6247). Aucune variante ne bat significativement le choix retenu (Complet : retards + flux + calendrier (retenu)) après correction de Holm.



### D6 · Prétraitement

*Quelle mise à l'échelle des variables ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| z-score : (x − moyenne)/écart-type (retenu) | 1.256 | 1.724 | -0.008 | 0.6302 | 2.1 |  |  | — choix retenu |
| Robuste : (x − médiane)/(Q3 − Q1) | 1.258 | 1.74 | 0.002 | 0.6281 | 1.4 | 0.7879 | 0.7879 | équivalent |
| Min-max : (x − min)/(max − min) | 1.823 | 2.262 | -0.131 | 0.9507 | 1.2 | 0.0 | 0.0 | moins bon |
| Aucune mise à l'échelle | 1.666 | 2.16 | 0.184 | 0.7775 | 2.1 | 0.0005 | 0.001 | moins bon |


Plus petite perte pinball à τ = 0.8 : **Robuste : (x − médiane)/(Q3 − Q1)** (0.6281). Aucune variante ne bat significativement le choix retenu (z-score : (x − moyenne)/écart-type (retenu)) après correction de Holm.



### D7 · Fenêtre d'entraînement

*Faut-il tout le passé, ou seulement les derniers mois ? (mesure aussi le coût d'un historique court)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Croissante (tout le passé) (retenu) | 1.336 | 1.823 | 0.039 | 0.4993 | 89.1 | 13.2 |  |  | — choix retenu |
| Glissante : 365 derniers jours | 1.439 | 1.872 | -0.022 | 0.5536 | 78.1 | 8.9 | 0.0092 | 0.0092 | moins bon |
| Glissante : 180 derniers jours | 1.886 | 2.362 | 0.325 | 0.7014 | 73.2 | 6.7 | 0.0 | 0.0 | moins bon |
| Glissante : 90 derniers jours | 2.306 | 2.848 | 0.273 | 0.883 | 69.9 | 6.3 | 0.0 | 0.0 | moins bon |


Plus petite perte pinball à τ = 0.8 : **Croissante (tout le passé) (retenu)** (0.4993). Aucune variante ne bat significativement le choix retenu (Croissante (tout le passé) (retenu)) après correction de Holm.



### D8 · Optimisation

*Comment atteindre le minimum de J le plus sûrement ? (SVR RBF, un découpage)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | J final | pas effectués | arrêt | solution gardée | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Adam + Polyak + préconditionnement + décroissance η (retenu) | 1.265 | 1.734 | 0.015 | 0.6279 | 0.8 | 1826.81 | 3000 | 3000 pas atteints | meilleur point rencontré |  |  | — choix retenu |
| Adam sans moyenne de Polyak | 1.265 | 1.734 | 0.015 | 0.6279 | 0.7 | 1826.81 | 3000 | 3000 pas atteints | meilleur point rencontré |  |  | identique |
| Adam sans préconditionnement | 1.291 | 1.758 | 0.037 | 0.6345 | 1.0 | 1884.28 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.3391 | 0.3391 | équivalent |
| Adam sans décroissance de η | 1.266 | 1.736 | 0.012 | 0.6297 | 0.8 | 1827.66 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0068 | 0.0136 | moins bon |
| Momentum | 2.764 | 3.324 | -0.019 | 1.3876 | 0.6 | 4529.01 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | moins bon |
| Descente de gradient simple | 2.764 | 3.324 | -0.019 | 1.3876 | 0.6 | 4529.01 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | moins bon |


Plus petite perte pinball à τ = 0.8 : **Adam + Polyak + préconditionnement + décroissance η (retenu)** (0.6279). Aucune variante ne bat significativement le choix retenu (Adam + Polyak + préconditionnement + décroissance η (retenu)) après correction de Holm.



### D9 · Combinaison des modèles

*Apprendre les poids de combinaison apporte-t-il plus qu'une moyenne ? (jours où l'empilement prédit)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Niveau 4 seul (meilleur modèle unique) | 1.29 | 1.755 | 0.03 | 0.4776 | 89.0 | 9.3 | 0.4528 | 0.9056 | équivalent |
| Moyenne simple persistance + niv. 3 + niv. 4 | 1.279 | 1.781 | -0.007 | 0.5065 | 74.8 | 18.6 | 0.4687 | 0.9056 | équivalent |
| Empilement appris (poids positifs) (retenu) | 1.268 | 1.717 | -0.014 | 0.4895 | 85.2 | 30.3 |  |  | — choix retenu |
| XGBoost quantile seul | 1.413 | 1.882 | 0.027 | 0.5741 | 89.0 | 14.0 | 0.0002 | 0.001 | moins bon |
| Moyenne SVR niv. 4 + XGBoost | 1.322 | 1.785 | 0.029 | 0.5092 | 91.0 | 23.3 | 0.1789 | 0.5367 | équivalent |
| Empilement persistance + niv. 3 + niv. 4 + XGBoost | 1.292 | 1.755 | -0.063 | 0.5114 | 84.5 | 43.9 | 0.0959 | 0.3836 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Niveau 4 seul (meilleur modèle unique)** (0.4776). Aucune variante ne bat significativement le choix retenu (Empilement appris (poids positifs) (retenu)) après correction de Holm.



### D13 · Variantes de SVM

*Quel SVM est le plus adapté à la série du service ? (mêmes jours, mêmes variables)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | cle | couverture 90 % | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| SVR linéaire (niveau 1) | 1.265 | 1.771 | 0.002 | 0.6319 | 0.4 | svr_lineaire |  | 0.0013 | 0.0065 | moins bon |
| SVR RBF (niveau 2) | 1.256 | 1.724 | -0.008 | 0.6302 | 2.3 | svr_rbf |  | 0.001 | 0.006 | moins bon |
| SVR quantile RBF (niveau 3) | 1.307 | 1.783 | -0.048 | 0.4914 | 6.5 | svr_q_rbf | 87.4 | 0.5074 | 1.0 | équivalent |
| SVR quantile composite (niveau 4, retenu) (retenu) | 1.336 | 1.823 | 0.039 | 0.4993 | 13.1 | svr_q_composite | 89.1 |  |  | — choix retenu |
| SVR quantile, noyau laplacien | 1.374 | 1.822 | 0.064 | 0.5167 | 8.2 | svr_q_laplacien | 88.0 | 0.2644 | 1.0 | équivalent |
| SVR quantile, noyau polynomial (degré 2) | 1.255 | 1.746 | -0.087 | 0.491 | 8.6 | svr_q_polynomial | 86.9 | 0.6754 | 1.0 | équivalent |
| LS-SVR (moindres carrés), noyau RBF, quantiles LOO | 1.27 | 1.718 | -0.09 | 0.4898 | 0.2 | lssvr_rbf | 91.3 | 0.6116 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **LS-SVR (moindres carrés), noyau RBF, quantiles LOO** (0.4898). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4, retenu) (retenu)) après correction de Holm.



### D11 · Chaque variable, une à une

*Que perd le modèle si on lui retire cette seule variable ? (modèle RBF du niveau 2, mêmes jours)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 1.256 | 1.724 | -0.008 | 0.6302 | 2.3 |  |  | — choix retenu |
| Sans occ_j-0 | 1.468 | 1.874 | 0.034 | 0.7236 | 1.9 | 0.0028 | 0.0476 | moins bon |
| Sans occ_j-1 | 1.29 | 1.763 | 0.004 | 0.6436 | 2.2 | 0.2506 | 1.0 | équivalent |
| Sans occ_j-2 | 1.25 | 1.72 | -0.002 | 0.6254 | 2.1 | 0.0904 | 1.0 | équivalent |
| Sans occ_j-3 | 1.261 | 1.734 | 0.008 | 0.6283 | 2.1 | 0.6525 | 1.0 | équivalent |
| Sans occ_j-4 | 1.256 | 1.729 | -0.002 | 0.6285 | 2.2 | 0.5226 | 1.0 | équivalent |
| Sans occ_j-5 | 1.261 | 1.732 | -0.009 | 0.6333 | 2.1 | 0.2431 | 1.0 | équivalent |
| Sans occ_j-6 | 1.276 | 1.743 | -0.057 | 0.6551 | 2.2 | 0.0104 | 0.156 | équivalent |
| Sans adm_3j | 1.281 | 1.753 | -0.022 | 0.6473 | 2.0 | 0.174 | 1.0 | équivalent |
| Sans adm_7j | 1.295 | 1.768 | -0.071 | 0.6686 | 1.8 | 0.0001 | 0.0019 | moins bon |
| Sans sorties_7j | 1.353 | 1.864 | -0.106 | 0.7082 | 2.3 | 0.002 | 0.036 | moins bon |
| Sans cible_jour_0 | 1.271 | 1.734 | -0.011 | 0.639 | 2.1 | 0.1961 | 1.0 | équivalent |
| Sans cible_jour_1 | 1.256 | 1.727 | -0.007 | 0.6303 | 2.1 | 0.9282 | 1.0 | équivalent |
| Sans cible_jour_2 | 1.259 | 1.721 | -0.003 | 0.6307 | 2.2 | 0.8121 | 1.0 | équivalent |
| Sans cible_jour_3 | 1.253 | 1.721 | -0.006 | 0.6286 | 2.1 | 0.3768 | 1.0 | équivalent |
| Sans cible_jour_4 | 1.263 | 1.722 | -0.007 | 0.6336 | 2.1 | 0.1262 | 1.0 | équivalent |
| Sans cible_jour_5 | 1.292 | 1.759 | 0.023 | 0.639 | 2.0 | 0.1294 | 1.0 | équivalent |
| Sans cible_jour_6 | 1.265 | 1.735 | -0.025 | 0.6399 | 2.1 | 0.005 | 0.08 | équivalent |
| Sans mois_sin | 1.263 | 1.738 | 0.008 | 0.6289 | 2.0 | 0.8423 | 1.0 | équivalent |
| Sans mois_cos | 1.28 | 1.752 | 0.048 | 0.6257 | 2.2 | 0.5266 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Sans occ_j-2** (0.6254). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)) après correction de Holm.



### D14 · Sélection des variables par le lasso

*Le modèle gagne-t-il à ne garder que les variables choisies par le lasso ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 1.256 | 1.724 | -0.008 | 0.6302 | 2.2 | 19.0 |  |  | — choix retenu |
| Lasso, λ de plus petite erreur | 1.268 | 1.748 | 0.043 | 0.6211 | 24.6 | 13.1 | 0.3072 | 0.597 | équivalent |
| Lasso à un écart-type (λ_1se) | 1.291 | 1.761 | 0.083 | 0.6205 | 24.0 | 11.7 | 0.2985 | 0.597 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Lasso à un écart-type (λ_1se)** (0.6205). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)) après correction de Holm.



## Horizon J+7 — 177 jours évalués, 7 origines


### D1 · Modèles de référence, concurrents et SVR

*Le SVR fait-il mieux que les méthodes statistiques usuelles et que les autres modèles d'apprentissage ?*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | couverture 90 % | réglages | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Persistance | 3.895 | 4.782 | 0.295 | 1.8589 | 0.0 |  |  | 0.0008 | 0.0128 | moins bon |
| Saisonnière hebdomadaire | 3.061 | 3.663 | 0.378 | 1.4169 | 0.0 |  |  | 0.0159 | 0.159 | équivalent |
| Moyenne mobile 7 j | 3.66 | 4.352 | 0.27 | 1.749 | 0.0 |  |  | 0.0026 | 0.039 | moins bon |
| Moyenne historique | 2.753 | 3.331 | 0.165 | 0.9527 | 0.0 | 90.4 |  | 0.5821 | 1.0 | équivalent |
| Lissage exponentiel simple | 3.895 | 4.782 | 0.295 | 1.378 | 0.0 | 84.2 |  | 0.0002 | 0.0044 | moins bon |
| Méthode Thêta | 3.893 | 4.782 | 0.283 | 1.378 | 0.0 | 84.2 |  | 0.0002 | 0.0044 | moins bon |
| Holt linéaire | 3.986 | 4.883 | 0.378 | 1.4075 | 0.2 | 83.6 |  | 0.0001 | 0.0023 | moins bon |
| Holt amorti | 3.895 | 4.782 | 0.295 | 1.378 | 0.1 | 84.2 |  | 0.0002 | 0.0044 | moins bon |
| Lissage saisonnier sans tendance | 3.895 | 4.782 | 0.295 | 1.378 | 0.2 | 84.2 |  | 0.0002 | 0.0044 | moins bon |
| Holt-Winters additif amorti | 3.895 | 4.782 | 0.295 | 1.378 | 0.6 | 84.2 |  | 0.0002 | 0.0044 | moins bon |
| Holt-Winters multiplicatif amorti | 3.895 | 4.782 | 0.295 | 1.378 | 0.6 | 84.2 |  | 0.0002 | 0.0044 | moins bon |
| AR(p) par AIC | 2.877 | 3.478 | 0.316 | 1.0066 | 0.2 | 87.6 |  | 0.169 | 0.836 | équivalent |
| SARIMA(2,1,1)(1,0,0)7 (ordre choisi sur l'apprentissage) | 2.946 | 3.52 | 0.427 | 0.9838 | 14.2 | 89.8 |  | 0.2618 | 0.836 | équivalent |
| Holt-Winters additif, grille fixée avant la validation | 3.149 | 3.74 | 0.32 | 1.4784 | 0.3 |  | alpha=0.1, beta=0.0, gamma=0.05, phi=0.98 | 0.0125 | 0.1375 | équivalent |
| Régression ridge (λ = 1) | 2.839 | 3.476 | -0.16 | 1.4675 | 0.1 |  |  | 0.0093 | 0.1176 | équivalent |
| A · forêt aléatoire quantile | 2.847 | 3.387 | -0.195 | 1.0049 | 22.1 | 90.4 |  | 0.0373 | 0.3177 | équivalent |
| B · gradient boosting quantile | 2.867 | 3.416 | -0.205 | 1.0127 | 12.7 | 76.3 |  | 0.0476 | 0.3332 | équivalent |
| C · perceptron multicouche quantile | 2.865 | 3.51 | -0.323 | 1.029 | 1.4 | 85.3 |  | 0.0536 | 0.3332 | équivalent |
| D · LSTM quantile | 3.035 | 3.644 | -0.105 | 1.05 | 16.8 | 80.2 |  | 0.0353 | 0.3177 | équivalent |
| E · XGBoost quantile (second ordre) | 2.853 | 3.376 | -0.179 | 0.9803 | 15.5 | 84.7 |  | 0.1672 | 0.836 | équivalent |
| SVR linéaire (niveau 1) | 2.846 | 3.509 | -0.24 | 1.4948 | 0.3 |  |  | 0.0084 | 0.1176 | équivalent |
| SVR RBF (niveau 2) | 2.809 | 3.36 | 0.022 | 1.3979 | 0.5 |  |  | 0.0087 | 0.1176 | équivalent |
| SVR quantile RBF (niveau 3) | 2.79 | 3.352 | 0.084 | 0.9149 | 1.4 | 88.7 |  | 0.7374 | 1.0 | équivalent |
| SVR quantile composite (niveau 4) (retenu) | 2.756 | 3.338 | -0.134 | 0.9227 | 12.1 | 89.3 |  |  |  | — choix retenu |


Plus petite perte pinball à τ = 0.8 : **SVR quantile RBF (niveau 3)** (0.9149). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4) (retenu)) après correction de Holm.



### D2 · Noyau

*Quel noyau décrit le mieux la dynamique ? (même perte ε-insensible, même C)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Linéaire | 2.841 | 3.499 | -0.265 | 1.4998 | 0.5 | 0.4174 | 0.4712 | équivalent |
| RBF (γ = 0.2) | 2.809 | 3.36 | 0.022 | 1.3979 | 0.5 | 0.2356 | 0.4712 | équivalent |
| Composite occupation / flux et saison (β appris) (retenu) | 2.762 | 3.321 | -0.239 | 1.4529 | 1.3 |  |  | — choix retenu |


Plus petite perte pinball à τ = 0.8 : **RBF (γ = 0.2)** (1.3979). Aucune variante ne bat significativement le choix retenu (Composite occupation / flux et saison (β appris) (retenu)) après correction de Holm.



### D3 · Fonction de perte

*Quelle perte pour un modèle linéaire identique ? (isole l'effet de la perte)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Carrée (ridge, λ = 1/C) | 2.839 | 3.476 | -0.16 | 1.4674 | 0.1 | 0.1131 | 0.408 | équivalent |
| ε-insensible, ε = 0 lit (= valeur absolue) | 2.858 | 3.531 | -0.16 | 1.4772 | 0.5 | 0.4253 | 0.8506 | équivalent |
| ε-insensible, ε = 0.5 lit | 2.833 | 3.492 | -0.178 | 1.47 | 0.4 | 0.102 | 0.408 | équivalent |
| ε-insensible, ε = 1 lit (retenu) | 2.846 | 3.509 | -0.24 | 1.4948 | 0.3 |  |  | — choix retenu |
| ε-insensible, ε = 2 lit | 2.855 | 3.513 | -0.261 | 1.5057 | 0.5 | 0.6877 | 0.8506 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Carrée (ridge, λ = 1/C)** (1.4674). Aucune variante ne bat significativement le choix retenu (ε-insensible, ε = 1 lit (retenu)) après correction de Holm.



### D4 · Quantile décisionnel τ et coût des décisions

*Quel τ minimise le coût réel selon le rapport pénurie / lit vide ? (τ optimal théorique = r/(1+r))*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | jours sous-estimés % | lits prévus en moyenne | coût r=1 | coût r=2 | coût r=4 | coût r=9 | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| τ = 0.5 | 2.801 | 3.361 | 0.087 | 1.3745 | 0.4 | 48.0 | 9.88 | 2.801 | 4.158 | 6.872 | 13.658 | 0.0229 | 0.0916 | équivalent |
| τ = 0.6 | 2.884 | 3.489 | 0.932 | 1.1623 | 0.4 | 41.8 | 10.73 | 2.884 | 3.86 | 5.812 | 10.691 | 0.0951 | 0.1902 | équivalent |
| τ = 0.7 | 3.149 | 3.897 | 1.941 | 0.9919 | 0.3 | 31.6 | 11.74 | 3.149 | 3.752 | 4.96 | 7.978 | 0.3585 | 0.3585 | équivalent |
| τ = 0.8 (retenu) | 3.847 | 4.738 | 3.352 | 0.9176 | 0.4 | 16.9 | 13.15 | 3.847 | 4.094 | 4.588 | 5.824 |  |  | — choix retenu |
| τ = 0.9 | 4.926 | 5.828 | 4.783 | 1.028 | 0.5 | 9.0 | 14.58 | 4.926 | 4.997 | 5.14 | 5.497 | 0.0585 | 0.1755 | équivalent |


τ le moins coûteux pour chaque rapport de coûts r = c_pénurie / c_lit vide : r = 1 → τ = 0.5, r = 2 → τ = 0.7, r = 4 → τ = 0.8 (retenu), r = 9 → τ = 0.9. Le choix τ = 0.8 correspond à r = 4.


### D5 · Variables d'entrée

*Que rapporte chaque groupe de variables ? (même modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| 7 retards seuls | 2.901 | 3.52 | 0.134 | 1.4103 | 0.3 | 7 | 0.7933 | 1.0 | équivalent |
| 7 retards + flux | 2.874 | 3.464 | 0.191 | 1.3796 | 0.6 | 10 | 0.502 | 1.0 | équivalent |
| 7 retards + calendrier (jour, mois) | 2.803 | 3.343 | -0.057 | 1.4185 | 0.4 | 16 | 0.0643 | 0.5787 | équivalent |
| Complet : retards + flux + calendrier (retenu) | 2.809 | 3.36 | 0.022 | 1.3979 | 0.5 | 19 |  |  | — choix retenu |
| Complet + jours fériés camerounais | 2.803 | 3.355 | 0.024 | 1.3944 | 0.4 | 21 | 0.1777 | 1.0 | équivalent |
| Complet + vacances scolaires | 2.812 | 3.363 | 0.013 | 1.4021 | 0.4 | 20 | 0.5131 | 1.0 | équivalent |
| Complet + fériés + vacances scolaires | 2.806 | 3.359 | 0.016 | 1.3981 | 0.5 | 22 | 0.988 | 1.0 | équivalent |
| 3 retards + flux + calendrier | 2.784 | 3.339 | -0.108 | 1.4246 | 0.4 | 15 | 0.1943 | 1.0 | équivalent |
| 14 retards + flux + calendrier | 2.783 | 3.349 | 0.083 | 1.3667 | 0.4 | 26 | 0.2798 | 1.0 | équivalent |
| Complet + diagnostics d'entrée des présents | 2.766 | 3.338 | 0.137 | 1.3422 | 0.3 | 30 | 0.0891 | 0.7128 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Complet + diagnostics d'entrée des présents** (1.3422). Aucune variante ne bat significativement le choix retenu (Complet : retards + flux + calendrier (retenu)) après correction de Holm.



### D6 · Prétraitement

*Quelle mise à l'échelle des variables ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| z-score : (x − moyenne)/écart-type (retenu) | 2.809 | 3.36 | 0.022 | 1.3979 | 0.5 |  |  | — choix retenu |
| Robuste : (x − médiane)/(Q3 − Q1) | 2.85 | 3.44 | -0.007 | 1.4269 | 0.5 | 0.259 | 0.518 | équivalent |
| Min-max : (x − min)/(max − min) | 2.807 | 3.391 | -0.131 | 1.4425 | 0.5 | 0.2689 | 0.518 | équivalent |
| Aucune mise à l'échelle | 2.747 | 3.324 | 0.151 | 1.3281 | 0.4 | 0.1487 | 0.4461 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Aucune mise à l'échelle** (1.3281). Aucune variante ne bat significativement le choix retenu (z-score : (x − moyenne)/écart-type (retenu)) après correction de Holm.



### D7 · Fenêtre d'entraînement

*Faut-il tout le passé, ou seulement les derniers mois ? (mesure aussi le coût d'un historique court)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Croissante (tout le passé) (retenu) | 2.756 | 3.338 | -0.134 | 0.9227 | 89.3 | 11.4 |  |  | — choix retenu |
| Glissante : 365 derniers jours | 2.766 | 3.338 | -0.559 | 0.9618 | 86.4 | 6.0 | 0.2957 | 0.8871 | équivalent |
| Glissante : 180 derniers jours | 2.771 | 3.374 | -0.197 | 0.9356 | 90.4 | 5.1 | 0.7912 | 1.0 | équivalent |
| Glissante : 90 derniers jours | 2.806 | 3.413 | -0.008 | 0.918 | 87.0 | 4.6 | 0.9318 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Glissante : 90 derniers jours** (0.918). Aucune variante ne bat significativement le choix retenu (Croissante (tout le passé) (retenu)) après correction de Holm.



### D8 · Optimisation

*Comment atteindre le minimum de J le plus sûrement ? (SVR RBF, un découpage)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | J final | pas effectués | arrêt | solution gardée | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Adam + Polyak + préconditionnement + décroissance η (retenu) | 2.797 | 3.353 | -0.105 | 1.43 | 0.3 | 337.68 | 767 | J stable depuis 100 pas (pas 766) | moyenne de Polyak sur 100 pas |  |  | — choix retenu |
| Adam sans moyenne de Polyak | 2.797 | 3.353 | -0.104 | 1.4297 | 0.2 | 337.68 | 767 | J stable depuis 100 pas (pas 766) | meilleur point rencontré | 0.0603 | 0.1809 | équivalent |
| Adam sans préconditionnement | 2.797 | 3.353 | -0.102 | 1.4292 | 1.2 | 337.7 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.1735 | 0.347 | équivalent |
| Adam sans décroissance de η | 2.797 | 3.353 | -0.104 | 1.4295 | 0.1 | 337.68 | 252 | J stable depuis 100 pas (pas 251) | moyenne de Polyak sur 100 pas | 0.0011 | 0.0045 | meilleur |
| Momentum | 2.796 | 3.353 | -0.106 | 1.4298 | 0.4 | 337.71 | 1629 | J stable depuis 100 pas (pas 1628) | meilleur point rencontré | 0.7494 | 0.7494 | équivalent |
| Descente de gradient simple | 2.796 | 3.352 | -0.095 | 1.4266 | 0.3 | 337.73 | 1569 | J stable depuis 100 pas (pas 1568) | meilleur point rencontré | 0.0009 | 0.0045 | meilleur |


Plus petite perte pinball à τ = 0.8 : **Descente de gradient simple** (1.4266). ⚠ Significativement meilleur que le choix retenu (Holm, 5 %) : Adam sans décroissance de η, Descente de gradient simple — le choix est à revoir.



### D9 · Combinaison des modèles

*Apprendre les poids de combinaison apporte-t-il plus qu'une moyenne ? (jours où l'empilement prédit)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Niveau 4 seul (meilleur modèle unique) | 2.821 | 3.402 | -0.421 | 0.9297 | 88.6 | 5.9 | 0.2393 | 1.0 | équivalent |
| Moyenne simple persistance + niv. 3 + niv. 4 | 3.095 | 3.77 | -0.133 | 1.144 | 63.1 | 11.8 | 0.2777 | 1.0 | équivalent |
| Empilement appris (poids positifs) (retenu) | 3.075 | 3.737 | -0.286 | 1.0528 | 77.9 | 23.4 |  |  | — choix retenu |
| XGBoost quantile seul | 2.938 | 3.455 | -0.529 | 0.9931 | 83.2 | 15.6 | 0.6225 | 1.0 | équivalent |
| Moyenne SVR niv. 4 + XGBoost | 2.871 | 3.407 | -0.475 | 0.954 | 86.6 | 21.5 | 0.3701 | 1.0 | équivalent |
| Empilement persistance + niv. 3 + niv. 4 + XGBoost | 3.136 | 3.789 | -0.336 | 1.0524 | 79.9 | 39.7 | 0.9372 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Niveau 4 seul (meilleur modèle unique)** (0.9297). Aucune variante ne bat significativement le choix retenu (Empilement appris (poids positifs) (retenu)) après correction de Holm.



### D13 · Variantes de SVM

*Quel SVM est le plus adapté à la série du service ? (mêmes jours, mêmes variables)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | cle | couverture 90 % | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| SVR linéaire (niveau 1) | 2.846 | 3.509 | -0.24 | 1.4948 | 0.3 | svr_lineaire |  | 0.0084 | 0.0504 | équivalent |
| SVR RBF (niveau 2) | 2.809 | 3.36 | 0.022 | 1.3979 | 0.5 | svr_rbf |  | 0.0087 | 0.0504 | équivalent |
| SVR quantile RBF (niveau 3) | 2.79 | 3.352 | 0.084 | 0.9149 | 1.3 | svr_q_rbf | 88.7 | 0.7374 | 1.0 | équivalent |
| SVR quantile composite (niveau 4, retenu) (retenu) | 2.756 | 3.338 | -0.134 | 0.9227 | 10.2 | svr_q_composite | 89.3 |  |  | — choix retenu |
| SVR quantile, noyau laplacien | 2.792 | 3.368 | 0.077 | 0.9232 | 1.1 | svr_q_laplacien | 88.1 | 0.9848 | 1.0 | équivalent |
| SVR quantile, noyau polynomial (degré 2) | 2.823 | 3.433 | -0.153 | 0.9783 | 5.1 | svr_q_polynomial | 86.4 | 0.1822 | 0.7288 | équivalent |
| LS-SVR (moindres carrés), noyau RBF, quantiles LOO | 2.834 | 3.374 | 0.04 | 0.923 | 0.2 | lssvr_rbf | 92.1 | 0.9911 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **SVR quantile RBF (niveau 3)** (0.9149). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4, retenu) (retenu)) après correction de Holm.



### D11 · Chaque variable, une à une

*Que perd le modèle si on lui retire cette seule variable ? (modèle RBF du niveau 2, mêmes jours)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 2.809 | 3.36 | 0.022 | 1.3979 | 0.4 |  |  | — choix retenu |
| Sans occ_j-0 | 2.809 | 3.361 | 0.002 | 1.4042 | 0.3 | 0.3771 | 1.0 | équivalent |
| Sans occ_j-1 | 2.804 | 3.357 | -0.002 | 1.4024 | 0.4 | 0.1824 | 1.0 | équivalent |
| Sans occ_j-2 | 2.815 | 3.364 | 0.003 | 1.4068 | 0.3 | 0.0508 | 0.8636 | équivalent |
| Sans occ_j-3 | 2.81 | 3.364 | 0.007 | 1.4028 | 0.4 | 0.1917 | 1.0 | équivalent |
| Sans occ_j-4 | 2.807 | 3.363 | 0.005 | 1.4017 | 0.5 | 0.0391 | 0.7038 | équivalent |
| Sans occ_j-5 | 2.815 | 3.361 | -0.007 | 1.4098 | 0.5 | 0.0011 | 0.0209 | moins bon |
| Sans occ_j-6 | 2.808 | 3.351 | -0.018 | 1.4093 | 0.3 | 0.0595 | 0.952 | équivalent |
| Sans adm_3j | 2.815 | 3.361 | 0.01 | 1.4047 | 0.4 | 0.3151 | 1.0 | équivalent |
| Sans adm_7j | 2.808 | 3.36 | 0.007 | 1.4017 | 0.4 | 0.5103 | 1.0 | équivalent |
| Sans sorties_7j | 2.809 | 3.35 | -0.024 | 1.4115 | 0.5 | 0.095 | 1.0 | équivalent |
| Sans cible_jour_0 | 2.809 | 3.357 | 0.024 | 1.3971 | 0.5 | 0.7344 | 1.0 | équivalent |
| Sans cible_jour_1 | 2.811 | 3.36 | 0.018 | 1.4 | 0.4 | 0.414 | 1.0 | équivalent |
| Sans cible_jour_2 | 2.813 | 3.361 | 0.028 | 1.3981 | 0.3 | 0.9619 | 1.0 | équivalent |
| Sans cible_jour_3 | 2.816 | 3.365 | 0.032 | 1.3984 | 0.3 | 0.8636 | 1.0 | équivalent |
| Sans cible_jour_4 | 2.813 | 3.363 | 0.029 | 1.3979 | 0.5 | 0.9951 | 1.0 | équivalent |
| Sans cible_jour_5 | 2.816 | 3.363 | 0.023 | 1.4012 | 0.4 | 0.2742 | 1.0 | équivalent |
| Sans cible_jour_6 | 2.808 | 3.357 | 0.016 | 1.3992 | 0.4 | 0.54 | 1.0 | équivalent |
| Sans mois_sin | 2.852 | 3.414 | 0.008 | 1.4236 | 0.5 | 0.3301 | 1.0 | équivalent |
| Sans mois_cos | 2.832 | 3.425 | 0.141 | 1.3738 | 0.4 | 0.2586 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Sans mois_cos** (1.3738). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)) après correction de Holm.



### D14 · Sélection des variables par le lasso

*Le modèle gagne-t-il à ne garder que les variables choisies par le lasso ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 2.809 | 3.36 | 0.022 | 1.3979 | 0.4 | 19.0 |  |  | — choix retenu |
| Lasso, λ de plus petite erreur | 2.912 | 3.562 | -0.103 | 1.487 | 21.1 | 1.7 | 0.1151 | 0.2302 | équivalent |
| Lasso à un écart-type (λ_1se) | 2.881 | 3.542 | 0.149 | 1.396 | 20.9 | 1.0 | 0.9663 | 0.9663 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Lasso à un écart-type (λ_1se)** (1.396). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)) après correction de Holm.

