# Banc de comparaison des choix — service PED_journee

Validation glissante du 01/03/2026 au verrou (01/09/2026), une origine tous les 28 jours, modèle réentraîné à chaque origine. « (retenu) » = choix retenu. Test de Diebold-Mariano (perte absolue, correction HLN) contre le choix retenu.


## Horizon J+1 — 183 jours évalués, 7 origines


### D1 · Modèles de référence, concurrents et SVR

*Le SVR fait-il mieux que les méthodes statistiques usuelles et que les autres modèles d'apprentissage ?*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | couverture 90 % | réglages | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Persistance | 2.324 | 2.977 | 0.022 | 1.1557 | 0.0 |  |  | 0.0 | 0.0 | 0.0 | moins bon |
| Saisonnière hebdomadaire | 3.498 | 4.285 | 0.34 | 1.6472 | 0.0 |  |  | 0.0 | 0.0 | 0.0 | moins bon |
| Moyenne mobile 7 j | 3.104 | 3.913 | 0.128 | 1.5133 | 0.0 |  |  | 0.0 | 0.0 | 0.0 | moins bon |
| Moyenne historique | 3.287 | 3.96 | 0.185 | 1.1891 | 0.0 | 91.3 |  | 0.0 | 0.0 | 0.0 | moins bon |
| Lissage exponentiel simple | 2.324 | 2.977 | 0.022 | 0.8358 | 0.0 | 92.9 |  | 0.0002 | 0.0036 | 0.0 | moins bon |
| Méthode Thêta | 2.325 | 2.977 | 0.02 | 0.8358 | 0.0 | 92.9 |  | 0.0002 | 0.0036 | 0.0 | moins bon |
| Holt linéaire | 2.335 | 2.981 | 0.073 | 0.8371 | 0.2 | 89.6 |  | 0.0002 | 0.0036 | 0.0 | moins bon |
| Holt amorti | 2.324 | 2.977 | 0.022 | 0.8358 | 0.2 | 89.6 |  | 0.0002 | 0.0036 | 0.0 | moins bon |
| Lissage saisonnier sans tendance | 2.028 | 2.582 | 0.037 | 0.7276 | 0.2 | 90.7 |  | 0.098 | 0.784 | 0.0082 | équivalent |
| Holt-Winters additif amorti | 2.028 | 2.582 | 0.037 | 0.7275 | 0.6 | 90.7 |  | 0.0981 | 0.784 | 0.0082 | équivalent |
| Holt-Winters multiplicatif amorti | 2.027 | 2.57 | 0.077 | 0.7308 | 0.7 | 92.9 |  | 0.1047 | 0.784 | 0.018 | équivalent |
| AR(p) par AIC | 2.084 | 2.668 | 0.122 | 0.7757 | 0.1 | 88.0 |  | 0.0016 | 0.0176 | 0.0002 | moins bon |
| SARIMA(2,0,0)(0,1,1)7 (ordre choisi sur l'apprentissage) | 1.935 | 2.505 | 0.07 | 0.7112 | 14.7 | 90.2 |  | 0.1474 | 0.784 | 0.0694 | équivalent |
| Holt-Winters additif, grille fixée avant la validation | 2.053 | 2.594 | 0.039 | 1.0147 | 0.2 |  | alpha=0.9, beta=0.0, gamma=0.3, phi=0.8 | 0.0 | 0.0 | 0.0033 | moins bon |
| Régression ridge (λ = 1) | 1.748 | 2.227 | 0.114 | 0.8396 | 0.2 |  |  | 0.0012 | 0.0144 | 0.4176 | moins bon |
| A · forêt aléatoire quantile | 1.921 | 2.533 | 0.044 | 0.7303 | 16.7 | 94.0 |  | 0.0278 | 0.252 | 0.0523 | équivalent |
| B · gradient boosting quantile | 1.812 | 2.375 | 0.053 | 0.6955 | 9.7 | 83.6 |  | 0.3057 | 1.0 | 0.7346 | équivalent |
| C · perceptron multicouche quantile | 1.738 | 2.226 | -0.042 | 0.6385 | 1.8 | 89.1 |  | 0.4275 | 1.0 | 0.3526 | équivalent |
| D · LSTM quantile | 1.73 | 2.241 | 0.064 | 0.6398 | 11.4 | 89.6 |  | 0.4639 | 1.0 | 0.2679 | équivalent |
| E · XGBoost quantile (second ordre) | 1.833 | 2.37 | -0.031 | 0.7238 | 11.4 | 91.3 |  | 0.0252 | 0.252 | 0.4227 | équivalent |
| SVR linéaire (niveau 1) | 1.748 | 2.232 | 0.036 | 0.8633 | 0.6 |  |  | 0.0004 | 0.0052 | 0.3327 | moins bon |
| SVR RBF (niveau 2) | 1.719 | 2.191 | -0.043 | 0.8724 | 2.3 |  |  | 0.0002 | 0.0036 | 0.0073 | moins bon |
| SVR quantile RBF (niveau 3) | 1.773 | 2.244 | -0.118 | 0.6516 | 4.9 | 88.5 |  | 0.5976 | 1.0 | 0.5709 | équivalent |
| SVR quantile composite (niveau 4) (retenu) | 1.793 | 2.283 | -0.079 | 0.6614 | 9.9 | 89.1 |  |  |  |  | — choix retenu |


Plus petite MAE : **SVR RBF (niveau 2)** (1.719). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4) (retenu)).



### D2 · Noyau

*Quel noyau décrit le mieux la dynamique ? (même perte ε-insensible, même C)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Linéaire | 1.749 | 2.24 | 0.046 | 0.8608 | 0.7 | 0.4558 | 0.9116 | 0.8599 | équivalent |
| RBF (γ = 0.02) | 1.719 | 2.191 | -0.043 | 0.8724 | 1.2 | 0.5593 | 0.9116 | 0.0558 | équivalent |
| Composite occupation / flux et saison (β appris) (retenu) | 1.756 | 2.242 | -0.002 | 0.8787 | 3.6 |  |  |  | — choix retenu |


Plus petite MAE : **RBF (γ = 0.02)** (1.719). Aucune variante ne bat significativement le choix retenu (Composite occupation / flux et saison (β appris) (retenu)).



### D3 · Fonction de perte

*Quelle perte pour un modèle linéaire identique ? (isole l'effet de la perte)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Carrée (ridge, λ = 1/C) | 1.747 | 2.226 | 0.113 | 0.8396 | 0.2 | 0.0095 | 0.0285 | 0.9371 | meilleur |
| ε-insensible, ε = 0 lit (= valeur absolue) | 1.765 | 2.256 | 0.007 | 0.8803 | 1.7 | 0.0482 | 0.0964 | 0.2796 | équivalent |
| ε-insensible, ε = 0.5 lit | 1.755 | 2.24 | -0.014 | 0.8815 | 0.6 | 0.0069 | 0.0276 | 0.5938 | moins bon |
| ε-insensible, ε = 1 lit (retenu) | 1.748 | 2.232 | 0.036 | 0.8633 | 0.5 |  |  |  | — choix retenu |
| ε-insensible, ε = 2 lit | 1.764 | 2.252 | 0.073 | 0.8599 | 0.9 | 0.7632 | 0.7632 | 0.4407 | équivalent |


Plus petite MAE : **Carrée (ridge, λ = 1/C)** (1.747). ⚠ Significativement meilleur que le choix retenu : Carrée (ridge, λ = 1/C) — le choix est à revoir.



### D4 · Quantile décisionnel τ et coût des décisions

*Quel τ minimise le coût réel selon le rapport pénurie / lit vide ? (τ optimal théorique = r/(1+r))*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | jours sous-estimés % | lits prévus en moyenne | coût r=1 | coût r=2 | coût r=4 | coût r=9 | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| τ = 0.5 | 1.773 | 2.244 | -0.118 | 0.9217 | 2.1 | 50.3 | 10.91 | 1.773 | 2.718 | 4.609 | 9.335 | 0.0 | 0.0 | 0.0 | moins bon |
| τ = 0.6 | 1.812 | 2.269 | 0.308 | 0.8136 | 1.5 | 43.2 | 11.34 | 1.812 | 2.564 | 4.068 | 7.828 | 0.0001 | 0.0003 | 0.0 | moins bon |
| τ = 0.7 | 1.941 | 2.41 | 0.89 | 0.7036 | 1.3 | 33.3 | 11.92 | 1.941 | 2.467 | 3.518 | 6.146 | 0.0292 | 0.0292 | 0.0 | moins bon |
| τ = 0.8 (retenu) | 2.264 | 2.767 | 1.601 | 0.6516 | 1.7 | 21.3 | 12.63 | 2.264 | 2.595 | 3.258 | 4.916 |  |  |  | — choix retenu |
| τ = 0.9 | 3.461 | 3.993 | 3.221 | 0.7644 | 2.2 | 8.2 | 14.25 | 3.461 | 3.581 | 3.822 | 4.423 | 0.0018 | 0.0036 | 0.0 | moins bon |


τ le moins coûteux pour chaque rapport de coûts r = c_pénurie / c_lit vide : r = 1 → τ = 0.5, r = 2 → τ = 0.7, r = 4 → τ = 0.8 (retenu), r = 9 → τ = 0.9. Le choix τ = 0.8 correspond à r = 4.


### D5 · Variables d'entrée

*Que rapporte chaque groupe de variables ? (même modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| 7 retards seuls | 2.205 | 2.791 | -0.01 | 1.1054 | 2.0 | 7 | 0.0 | 0.0 | 0.0 | moins bon |
| 7 retards + flux | 1.978 | 2.437 | 0.117 | 0.9541 | 2.2 | 10 | 0.0026 | 0.0208 | 0.0 | moins bon |
| 7 retards + calendrier (jour, mois) | 1.906 | 2.503 | -0.127 | 0.9912 | 1.8 | 16 | 0.0061 | 0.0427 | 0.0052 | moins bon |
| Complet : retards + flux + calendrier (retenu) | 1.719 | 2.191 | -0.043 | 0.8724 | 2.5 | 19 |  |  |  | — choix retenu |
| Complet + jours fériés camerounais | 1.719 | 2.196 | -0.043 | 0.8722 | 2.3 | 21 | 0.9586 | 1.0 | 0.9731 | équivalent |
| Complet + vacances scolaires | 1.711 | 2.178 | -0.031 | 0.8648 | 2.7 | 20 | 0.0209 | 0.1045 | 0.1244 | équivalent |
| Complet + fériés + vacances scolaires | 1.71 | 2.182 | -0.026 | 0.8625 | 1.7 | 22 | 0.0323 | 0.1292 | 0.2643 | équivalent |
| 3 retards + flux + calendrier | 1.734 | 2.26 | -0.149 | 0.9118 | 2.1 | 15 | 0.1387 | 0.4161 | 0.7136 | équivalent |
| 14 retards + flux + calendrier | 1.746 | 2.214 | 0.01 | 0.8699 | 1.2 | 26 | 0.8944 | 1.0 | 0.357 | équivalent |
| Complet + diagnostics d'entrée des présents | 1.807 | 2.312 | -0.122 | 0.94 | 2.5 | 30 | 0.014 | 0.084 | 0.0525 | équivalent |


Plus petite MAE : **Complet + fériés + vacances scolaires** (1.71). Aucune variante ne bat significativement le choix retenu (Complet : retards + flux + calendrier (retenu)).



### D6 · Prétraitement

*Quelle mise à l'échelle des variables ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| z-score : (x − moyenne)/écart-type (retenu) | 1.719 | 2.191 | -0.043 | 0.8724 | 1.9 |  |  |  | — choix retenu |
| Robuste : (x − médiane)/(Q3 − Q1) | 1.734 | 2.216 | 0.009 | 0.8641 | 1.7 | 0.4328 | 0.4328 | 0.4307 | équivalent |
| Min-max : (x − min)/(max − min) | 2.334 | 2.933 | -0.186 | 1.2227 | 0.9 | 0.0 | 0.0 | 0.0 | moins bon |
| Aucune mise à l'échelle | 2.277 | 2.864 | 0.253 | 1.0626 | 2.2 | 0.0009 | 0.0018 | 0.0 | moins bon |


Plus petite MAE : **z-score : (x − moyenne)/écart-type (retenu)** (1.719). Aucune variante ne bat significativement le choix retenu (z-score : (x − moyenne)/écart-type (retenu)).



### D7 · Fenêtre d'entraînement

*Faut-il tout le passé, ou seulement les derniers mois ? (mesure aussi le coût d'un historique court)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Croissante (tout le passé) (retenu) | 1.793 | 2.283 | -0.079 | 0.6614 | 89.1 | 10.3 |  |  |  | — choix retenu |
| Glissante : 365 derniers jours | 1.809 | 2.301 | -0.227 | 0.6716 | 88.0 | 6.9 | 0.5031 | 0.5031 | 0.5683 | équivalent |
| Glissante : 180 derniers jours | 2.049 | 2.586 | 0.088 | 0.7662 | 85.8 | 6.2 | 0.0009 | 0.0018 | 0.0007 | moins bon |
| Glissante : 90 derniers jours | 2.359 | 2.979 | -0.055 | 0.9191 | 78.1 | 4.2 | 0.0 | 0.0 | 0.0 | moins bon |


Plus petite MAE : **Croissante (tout le passé) (retenu)** (1.793). Aucune variante ne bat significativement le choix retenu (Croissante (tout le passé) (retenu)).



### D8 · Optimisation

*Comment atteindre le minimum de J le plus sûrement ? (SVR RBF, un découpage)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | J final | pas effectués | arrêt | solution gardée | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Adam + Polyak + préconditionnement + décroissance η (retenu) | 1.736 | 2.208 | -0.047 | 0.882 | 1.4 | 2079.03 | 3000 | 3000 pas atteints | meilleur point rencontré |  |  |  | — choix retenu |
| Adam sans moyenne de Polyak | 1.736 | 2.208 | -0.047 | 0.882 | 0.9 | 2079.03 | 3000 | 3000 pas atteints | meilleur point rencontré |  |  |  | identique |
| Adam sans préconditionnement | 1.753 | 2.233 | -0.065 | 0.896 | 1.3 | 2118.64 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.073 | 0.073 | 0.1881 | équivalent |
| Adam sans décroissance de η | 1.735 | 2.208 | -0.057 | 0.8846 | 1.0 | 2079.3 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | 0.7614 | moins bon |
| Momentum | 2.568 | 3.269 | -0.782 | 1.5188 | 0.8 | 3228.02 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | 0.0 | moins bon |
| Descente de gradient simple | 2.568 | 3.269 | -0.782 | 1.5188 | 1.0 | 3228.02 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | 0.0 | moins bon |


Plus petite MAE : **Adam sans décroissance de η** (1.735). Aucune variante ne bat significativement le choix retenu (Adam + Polyak + préconditionnement + décroissance η (retenu)).



### D9 · Combinaison des modèles

*Apprendre les poids de combinaison apporte-t-il plus qu'une moyenne ? (jours où l'empilement prédit)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Niveau 4 seul (meilleur modèle unique) | 1.728 | 2.219 | -0.132 | 0.6464 | 89.7 | 6.9 | 0.804 | 1.0 | 0.6555 | équivalent |
| Moyenne simple persistance + niv. 3 + niv. 4 | 1.776 | 2.306 | -0.101 | 0.7053 | 75.5 | 13.8 | 0.0743 | 0.2972 | 0.512 | équivalent |
| Empilement appris (poids positifs) (retenu) | 1.743 | 2.237 | -0.276 | 0.6515 | 83.9 | 28.7 |  |  |  | — choix retenu |
| XGBoost quantile seul | 1.8 | 2.34 | -0.032 | 0.7212 | 90.3 | 10.5 | 0.034 | 0.17 | 0.2733 | équivalent |
| Moyenne SVR niv. 4 + XGBoost | 1.729 | 2.248 | -0.082 | 0.6643 | 92.3 | 17.4 | 0.5837 | 1.0 | 0.6864 | équivalent |
| Empilement persistance + niv. 3 + niv. 4 + XGBoost | 1.748 | 2.248 | -0.252 | 0.6515 | 83.2 | 38.5 | 0.9954 | 1.0 | 0.7246 | équivalent |


Plus petite MAE : **Niveau 4 seul (meilleur modèle unique)** (1.728). Aucune variante ne bat significativement le choix retenu (Empilement appris (poids positifs) (retenu)).



### D13 · Variantes de SVM

*Quel SVM est le plus adapté à la série du service ? (mêmes jours, mêmes variables)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | cle | couverture 90 % | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SVR linéaire (niveau 1) | 1.748 | 2.232 | 0.036 | 0.8633 | 0.5 | svr_lineaire |  | 0.0004 | 0.002 | 0.3327 | moins bon |
| SVR RBF (niveau 2) | 1.719 | 2.191 | -0.043 | 0.8724 | 2.2 | svr_rbf |  | 0.0002 | 0.0012 | 0.0073 | moins bon |
| SVR quantile RBF (niveau 3) | 1.773 | 2.244 | -0.118 | 0.6516 | 6.0 | svr_q_rbf | 88.5 | 0.5976 | 1.0 | 0.5709 | équivalent |
| SVR quantile composite (niveau 4, retenu) (retenu) | 1.793 | 2.283 | -0.079 | 0.6614 | 11.0 | svr_q_composite | 89.1 |  |  |  | — choix retenu |
| SVR quantile, noyau laplacien | 1.854 | 2.338 | -0.091 | 0.6618 | 4.8 | svr_q_laplacien | 89.1 | 0.9789 | 1.0 | 0.0804 | équivalent |
| SVR quantile, noyau polynomial (degré 2) | 1.772 | 2.258 | -0.091 | 0.6349 | 7.4 | svr_q_polynomial | 86.9 | 0.3245 | 1.0 | 0.6864 | équivalent |
| LS-SVR (moindres carrés), noyau RBF, quantiles LOO | 1.68 | 2.159 | -0.099 | 0.6322 | 0.3 | lssvr_rbf | 92.3 | 0.2955 | 1.0 | 0.0204 | équivalent |


Plus petite MAE : **LS-SVR (moindres carrés), noyau RBF, quantiles LOO** (1.68). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4, retenu) (retenu)).



### D11 · Chaque variable, une à une

*Que perd le modèle si on lui retire cette seule variable ? (modèle RBF du niveau 2, mêmes jours)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 1.719 | 2.191 | -0.043 | 0.8724 | 2.1 |  |  |  | — choix retenu |
| Sans occ_j-0 | 1.849 | 2.261 | -0.037 | 0.9355 | 2.4 | 0.0319 | 0.4785 | 0.0093 | équivalent |
| Sans occ_j-1 | 1.722 | 2.198 | -0.05 | 0.8761 | 2.1 | 0.7006 | 1.0 | 0.8281 | équivalent |
| Sans occ_j-2 | 1.725 | 2.191 | -0.047 | 0.8766 | 2.1 | 0.2883 | 1.0 | 0.4268 | équivalent |
| Sans occ_j-3 | 1.726 | 2.208 | -0.028 | 0.8716 | 1.1 | 0.8449 | 1.0 | 0.3525 | équivalent |
| Sans occ_j-4 | 1.721 | 2.196 | -0.037 | 0.8715 | 1.9 | 0.7849 | 1.0 | 0.7563 | équivalent |
| Sans occ_j-5 | 1.727 | 2.198 | -0.017 | 0.8686 | 2.6 | 0.4492 | 1.0 | 0.333 | équivalent |
| Sans occ_j-6 | 1.705 | 2.204 | -0.108 | 0.8849 | 1.5 | 0.4251 | 1.0 | 0.5891 | équivalent |
| Sans adm_3j | 1.725 | 2.24 | -0.003 | 0.8633 | 2.2 | 0.5584 | 1.0 | 0.8301 | équivalent |
| Sans adm_7j | 1.746 | 2.228 | -0.035 | 0.8832 | 1.8 | 0.2982 | 1.0 | 0.1333 | équivalent |
| Sans sorties_7j | 1.852 | 2.407 | -0.094 | 0.9541 | 2.2 | 0.0264 | 0.4224 | 0.0227 | équivalent |
| Sans cible_jour_0 | 1.795 | 2.286 | -0.092 | 0.9251 | 2.7 | 0.0031 | 0.0558 | 0.0029 | équivalent |
| Sans cible_jour_1 | 1.72 | 2.194 | -0.042 | 0.8725 | 2.2 | 0.9389 | 1.0 | 0.6892 | équivalent |
| Sans cible_jour_2 | 1.718 | 2.189 | -0.037 | 0.8703 | 2.1 | 0.473 | 1.0 | 0.9093 | équivalent |
| Sans cible_jour_3 | 1.719 | 2.192 | -0.035 | 0.87 | 2.4 | 0.0958 | 1.0 | 0.9214 | équivalent |
| Sans cible_jour_4 | 1.724 | 2.194 | -0.049 | 0.8766 | 2.2 | 0.2062 | 1.0 | 0.4101 | équivalent |
| Sans cible_jour_5 | 1.767 | 2.239 | -0.025 | 0.8906 | 1.4 | 0.0574 | 0.8036 | 0.0129 | équivalent |
| Sans cible_jour_6 | 1.718 | 2.19 | -0.053 | 0.875 | 2.1 | 0.0648 | 0.8424 | 0.893 | équivalent |
| Sans mois_sin | 1.719 | 2.185 | 0.041 | 0.8472 | 1.9 | 0.0 | 0.0 | 0.9812 | meilleur |
| Sans mois_cos | 1.75 | 2.22 | 0.126 | 0.8373 | 1.6 | 0.0037 | 0.0629 | 0.1727 | équivalent |


Plus petite MAE : **Sans occ_j-6** (1.705). ⚠ Significativement meilleur que le choix retenu : Sans mois_sin — le choix est à revoir.



### D14 · Sélection des variables par le lasso

*Le modèle gagne-t-il à ne garder que les variables choisies par le lasso ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 1.719 | 2.191 | -0.043 | 0.8724 | 2.0 | 19.0 |  |  |  | — choix retenu |
| Lasso, λ de plus petite erreur | 1.726 | 2.2 | -0.034 | 0.8731 | 20.9 | 16.3 | 0.906 | 0.906 | 0.4964 | équivalent |
| Lasso à un écart-type (λ_1se) | 1.779 | 2.251 | 0.172 | 0.8378 | 20.2 | 8.0 | 0.0602 | 0.1204 | 0.085 | équivalent |


Plus petite MAE : **Toutes les variables (retenu)** (1.719). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)).



## Horizon J+7 — 177 jours évalués, 7 origines


### D1 · Modèles de référence, concurrents et SVR

*Le SVR fait-il mieux que les méthodes statistiques usuelles et que les autres modèles d'apprentissage ?*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | couverture 90 % | réglages | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Persistance | 4.454 | 5.532 | 0.351 | 2.1217 | 0.0 |  |  | 0.0004 | 0.0064 | 0.0 | moins bon |
| Saisonnière hebdomadaire | 3.487 | 4.274 | 0.414 | 1.6193 | 0.0 |  |  | 0.0119 | 0.0833 | 0.142 | équivalent |
| Moyenne mobile 7 j | 4.268 | 5.137 | 0.319 | 2.0383 | 0.0 |  |  | 0.0011 | 0.0165 | 0.0 | moins bon |
| Moyenne historique | 3.265 | 3.941 | 0.276 | 1.1493 | 0.0 | 93.2 |  | 0.0738 | 0.238 | 0.8264 | équivalent |
| Lissage exponentiel simple | 4.454 | 5.532 | 0.351 | 1.5953 | 0.0 | 85.3 |  | 0.0001 | 0.0023 | 0.0 | moins bon |
| Méthode Thêta | 4.453 | 5.532 | 0.336 | 1.5953 | 0.1 | 85.3 |  | 0.0001 | 0.0023 | 0.0 | moins bon |
| Holt linéaire | 4.551 | 5.618 | 0.717 | 1.6135 | 0.4 | 84.7 |  | 0.0001 | 0.0023 | 0.0 | moins bon |
| Holt amorti | 4.454 | 5.532 | 0.351 | 1.5953 | 0.4 | 84.7 |  | 0.0001 | 0.0023 | 0.0 | moins bon |
| Lissage saisonnier sans tendance | 4.454 | 5.532 | 0.351 | 1.5953 | 0.4 | 83.6 |  | 0.0001 | 0.0023 | 0.0 | moins bon |
| Holt-Winters additif amorti | 4.454 | 5.532 | 0.351 | 1.5953 | 0.6 | 84.2 |  | 0.0001 | 0.0023 | 0.0 | moins bon |
| Holt-Winters multiplicatif amorti | 4.454 | 5.532 | 0.351 | 1.5953 | 0.7 | 84.7 |  | 0.0001 | 0.0023 | 0.0 | moins bon |
| AR(p) par AIC | 3.332 | 4.09 | 0.405 | 1.1666 | 0.1 | 84.7 |  | 0.0595 | 0.238 | 0.4505 | équivalent |
| SARIMA(2,0,0)(0,1,1)7 (ordre choisi sur l'apprentissage) | 3.267 | 4.029 | 0.29 | 1.1411 | 16.1 | 87.6 |  | 0.2005 | 0.401 | 0.8348 | équivalent |
| Holt-Winters additif, grille fixée avant la validation | 3.612 | 4.375 | 0.359 | 1.6982 | 0.3 |  | alpha=0.1, beta=0.0, gamma=0.05, phi=0.98 | 0.0104 | 0.0832 | 0.0202 | équivalent |
| Régression ridge (λ = 1) | 3.275 | 4.032 | -0.18 | 1.6916 | 0.1 |  |  | 0.0037 | 0.0444 | 0.4309 | moins bon |
| A · forêt aléatoire quantile | 3.244 | 3.915 | -0.259 | 1.1275 | 15.8 | 93.2 |  | 0.0087 | 0.0783 | 0.8667 | équivalent |
| B · gradient boosting quantile | 3.161 | 3.886 | -0.525 | 1.1944 | 8.9 | 78.5 |  | 0.0016 | 0.0224 | 0.6152 | moins bon |
| C · perceptron multicouche quantile | 3.23 | 3.999 | -0.289 | 1.1661 | 1.3 | 88.7 |  | 0.0442 | 0.221 | 0.98 | équivalent |
| D · LSTM quantile | 3.295 | 4.043 | -0.091 | 1.1959 | 11.2 | 82.5 |  | 0.018 | 0.108 | 0.4985 | équivalent |
| E · XGBoost quantile (second ordre) | 3.164 | 3.876 | -0.328 | 1.1209 | 10.4 | 87.0 |  | 0.0059 | 0.059 | 0.5336 | équivalent |
| SVR linéaire (niveau 1) | 3.29 | 4.065 | -0.161 | 1.6931 | 0.4 |  |  | 0.0045 | 0.0495 | 0.3005 | moins bon |
| SVR RBF (niveau 2) | 3.233 | 3.939 | -0.193 | 1.6744 | 0.9 |  |  | 0.0022 | 0.0286 | 0.9397 | moins bon |
| SVR quantile RBF (niveau 3) | 3.261 | 3.934 | 0.143 | 1.0755 | 1.6 | 89.3 |  | 0.4193 | 0.4193 | 0.7914 | équivalent |
| SVR quantile composite (niveau 4) (retenu) | 3.227 | 3.949 | -0.331 | 1.0548 | 5.6 | 84.2 |  |  |  |  | — choix retenu |


Plus petite MAE : **B · gradient boosting quantile** (3.161). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4) (retenu)).



### D2 · Noyau

*Quel noyau décrit le mieux la dynamique ? (même perte ε-insensible, même C)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Linéaire | 3.292 | 4.07 | -0.163 | 1.6951 | 0.4 | 0.9228 | 1.0 | 0.0767 | équivalent |
| RBF (γ = 0.05) | 3.233 | 3.939 | -0.193 | 1.6744 | 1.1 | 0.6833 | 1.0 | 0.5784 | équivalent |
| Composite occupation / flux et saison (β appris) (retenu) | 3.192 | 3.935 | -0.321 | 1.6922 | 2.0 |  |  |  | — choix retenu |


Plus petite MAE : **Composite occupation / flux et saison (β appris) (retenu)** (3.192). Aucune variante ne bat significativement le choix retenu (Composite occupation / flux et saison (β appris) (retenu)).



### D3 · Fonction de perte

*Quelle perte pour un modèle linéaire identique ? (isole l'effet de la perte)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Carrée (ridge, λ = 1/C) | 3.275 | 4.032 | -0.18 | 1.6917 | 0.1 | 0.9503 | 1.0 | 0.6817 | équivalent |
| ε-insensible, ε = 0 lit (= valeur absolue) | 3.355 | 4.155 | -0.126 | 1.715 | 0.6 | 0.4154 | 1.0 | 0.1149 | équivalent |
| ε-insensible, ε = 0.5 lit | 3.315 | 4.095 | -0.122 | 1.6941 | 0.4 | 0.9502 | 1.0 | 0.3498 | équivalent |
| ε-insensible, ε = 1 lit (retenu) | 3.29 | 4.065 | -0.161 | 1.6931 | 0.4 |  |  |  | — choix retenu |
| ε-insensible, ε = 2 lit | 3.265 | 4.03 | -0.245 | 1.7061 | 0.4 | 0.5531 | 1.0 | 0.521 | équivalent |


Plus petite MAE : **ε-insensible, ε = 2 lit** (3.265). Aucune variante ne bat significativement le choix retenu (ε-insensible, ε = 1 lit (retenu)).



### D4 · Quantile décisionnel τ et coût des décisions

*Quel τ minimise le coût réel selon le rapport pénurie / lit vide ? (τ optimal théorique = r/(1+r))*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | jours sous-estimés % | lits prévus en moyenne | coût r=1 | coût r=2 | coût r=4 | coût r=9 | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| τ = 0.5 | 3.261 | 3.934 | 0.143 | 1.5877 | 0.5 | 48.6 | 11.08 | 3.261 | 4.82 | 7.939 | 15.735 | 0.0069 | 0.0276 | 0.0251 | moins bon |
| τ = 0.6 | 3.362 | 4.097 | 1.126 | 1.3432 | 0.5 | 41.2 | 12.07 | 3.362 | 4.48 | 6.716 | 12.306 | 0.0338 | 0.1014 | 0.0026 | équivalent |
| τ = 0.7 | 3.654 | 4.508 | 2.212 | 1.1632 | 0.4 | 33.3 | 13.15 | 3.654 | 4.375 | 5.816 | 9.42 | 0.1532 | 0.3064 | 0.0002 | équivalent |
| τ = 0.8 (retenu) | 4.133 | 5.128 | 3.304 | 1.0755 | 0.7 | 22.6 | 14.25 | 4.133 | 4.548 | 5.378 | 7.452 |  |  |  | — choix retenu |
| τ = 0.9 | 5.505 | 6.508 | 5.207 | 1.1907 | 0.6 | 9.6 | 16.15 | 5.505 | 5.655 | 5.953 | 6.7 | 0.1642 | 0.3064 | 0.0 | équivalent |


τ le moins coûteux pour chaque rapport de coûts r = c_pénurie / c_lit vide : r = 1 → τ = 0.5, r = 2 → τ = 0.7, r = 4 → τ = 0.8 (retenu), r = 9 → τ = 0.9. Le choix τ = 0.8 correspond à r = 4.


### D5 · Variables d'entrée

*Que rapporte chaque groupe de variables ? (même modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| 7 retards seuls | 3.401 | 4.17 | 0.253 | 1.6245 | 0.6 | 7 | 0.439 | 1.0 | 0.065 | équivalent |
| 7 retards + flux | 3.417 | 4.2 | 0.281 | 1.6245 | 0.5 | 10 | 0.307 | 1.0 | 0.0642 | équivalent |
| 7 retards + calendrier (jour, mois) | 3.246 | 3.961 | -0.269 | 1.7036 | 0.9 | 16 | 0.1833 | 1.0 | 0.6472 | équivalent |
| Complet : retards + flux + calendrier (retenu) | 3.233 | 3.939 | -0.193 | 1.6744 | 1.4 | 19 |  |  |  | — choix retenu |
| Complet + jours fériés camerounais | 3.23 | 3.937 | -0.192 | 1.6728 | 1.1 | 21 | 0.4244 | 1.0 | 0.2983 | équivalent |
| Complet + vacances scolaires | 3.229 | 3.941 | -0.291 | 1.7018 | 0.8 | 20 | 0.2619 | 1.0 | 0.9083 | équivalent |
| Complet + fériés + vacances scolaires | 3.225 | 3.937 | -0.286 | 1.6984 | 1.3 | 22 | 0.3104 | 1.0 | 0.8188 | équivalent |
| 3 retards + flux + calendrier | 3.235 | 3.942 | -0.286 | 1.7032 | 1.4 | 15 | 0.2446 | 1.0 | 0.9609 | équivalent |
| 14 retards + flux + calendrier | 3.274 | 4.002 | -0.179 | 1.6908 | 1.2 | 26 | 0.7397 | 1.0 | 0.5614 | équivalent |
| Complet + diagnostics d'entrée des présents | 3.205 | 3.886 | -0.31 | 1.6954 | 2.1 | 30 | 0.7633 | 1.0 | 0.7317 | équivalent |


Plus petite MAE : **Complet + diagnostics d'entrée des présents** (3.205). Aucune variante ne bat significativement le choix retenu (Complet : retards + flux + calendrier (retenu)).



### D6 · Prétraitement

*Quelle mise à l'échelle des variables ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| z-score : (x − moyenne)/écart-type (retenu) | 3.233 | 3.939 | -0.193 | 1.6744 | 1.3 |  |  |  | — choix retenu |
| Robuste : (x − médiane)/(Q3 − Q1) | 3.296 | 4.053 | 0.002 | 1.6475 | 1.4 | 0.5678 | 1.0 | 0.3675 | équivalent |
| Min-max : (x − min)/(max − min) | 3.245 | 3.934 | -0.081 | 1.6469 | 1.1 | 0.5884 | 1.0 | 0.8584 | équivalent |
| Aucune mise à l'échelle | 3.264 | 3.931 | 0.251 | 1.5566 | 0.7 | 0.0817 | 0.2451 | 0.7841 | équivalent |


Plus petite MAE : **z-score : (x − moyenne)/écart-type (retenu)** (3.233). Aucune variante ne bat significativement le choix retenu (z-score : (x − moyenne)/écart-type (retenu)).



### D7 · Fenêtre d'entraînement

*Faut-il tout le passé, ou seulement les derniers mois ? (mesure aussi le coût d'un historique court)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Croissante (tout le passé) (retenu) | 3.227 | 3.949 | -0.331 | 1.0548 | 84.2 | 8.3 |  |  |  | — choix retenu |
| Glissante : 365 derniers jours | 3.246 | 3.929 | -0.472 | 1.0966 | 84.2 | 6.2 | 0.0558 | 0.1674 | 0.7944 | équivalent |
| Glissante : 180 derniers jours | 3.206 | 3.862 | 0.015 | 1.0377 | 83.1 | 5.7 | 0.7937 | 1.0 | 0.9261 | équivalent |
| Glissante : 90 derniers jours | 3.354 | 4.04 | 0.4 | 1.0855 | 84.2 | 4.2 | 0.7135 | 1.0 | 0.694 | équivalent |


Plus petite MAE : **Glissante : 180 derniers jours** (3.206). Aucune variante ne bat significativement le choix retenu (Croissante (tout le passé) (retenu)).



### D8 · Optimisation

*Comment atteindre le minimum de J le plus sûrement ? (SVR RBF, un découpage)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | J final | pas effectués | arrêt | solution gardée | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Adam + Polyak + préconditionnement + décroissance η (retenu) | 3.213 | 3.936 | -0.301 | 1.6968 | 0.2 | 1312.79 | 376 | J stable depuis 100 pas (pas 375) | moyenne de Polyak sur 100 pas |  |  |  | — choix retenu |
| Adam sans moyenne de Polyak | 3.213 | 3.936 | -0.299 | 1.6961 | 0.1 | 1312.8 | 376 | J stable depuis 100 pas (pas 375) | meilleur point rencontré | 0.0115 | 0.0575 | 0.9724 | équivalent |
| Adam sans préconditionnement | 3.202 | 3.926 | -0.3 | 1.6911 | 1.0 | 1315.51 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0214 | 0.0856 | 0.017 | équivalent |
| Adam sans décroissance de η | 3.213 | 3.936 | -0.304 | 1.6975 | 0.1 | 1312.8 | 385 | J stable depuis 100 pas (pas 384) | moyenne de Polyak sur 100 pas | 0.0272 | 0.0856 | 0.4835 | équivalent |
| Momentum | 3.53 | 4.34 | -0.095 | 1.7933 | 0.6 | 1398.69 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.1551 | 0.3102 | 0.0038 | équivalent |
| Descente de gradient simple | 3.388 | 4.149 | 0.202 | 1.6336 | 0.6 | 1393.14 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.1679 | 0.3102 | 0.0702 | équivalent |


Plus petite MAE : **Adam sans préconditionnement** (3.202). Aucune variante ne bat significativement le choix retenu (Adam + Polyak + préconditionnement + décroissance η (retenu)).



### D9 · Combinaison des modèles

*Apprendre les poids de combinaison apporte-t-il plus qu'une moyenne ? (jours où l'empilement prédit)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Niveau 4 seul (meilleur modèle unique) | 3.291 | 3.999 | -0.749 | 1.0675 | 82.6 | 4.6 | 0.2181 | 1.0 | 0.147 | équivalent |
| Moyenne simple persistance + niv. 3 + niv. 4 | 3.583 | 4.395 | -0.252 | 1.3361 | 61.7 | 9.2 | 0.3309 | 1.0 | 0.8698 | équivalent |
| Empilement appris (poids positifs) (retenu) | 3.56 | 4.376 | -0.177 | 1.2213 | 73.2 | 22.0 |  |  |  | — choix retenu |
| XGBoost quantile seul | 3.231 | 3.932 | -0.753 | 1.1471 | 85.9 | 9.8 | 0.5822 | 1.0 | 0.0312 | équivalent |
| Moyenne SVR niv. 4 + XGBoost | 3.257 | 3.941 | -0.751 | 1.101 | 85.2 | 14.4 | 0.3526 | 1.0 | 0.0593 | équivalent |
| Empilement persistance + niv. 3 + niv. 4 + XGBoost | 3.519 | 4.317 | -0.379 | 1.2197 | 70.5 | 34.8 | 0.6316 | 1.0 | 0.4221 | équivalent |


Plus petite MAE : **XGBoost quantile seul** (3.231). Aucune variante ne bat significativement le choix retenu (Empilement appris (poids positifs) (retenu)).



### D13 · Variantes de SVM

*Quel SVM est le plus adapté à la série du service ? (mêmes jours, mêmes variables)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | cle | couverture 90 % | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SVR linéaire (niveau 1) | 3.29 | 4.065 | -0.161 | 1.6931 | 0.7 | svr_lineaire |  | 0.0045 | 0.0225 | 0.3005 | moins bon |
| SVR RBF (niveau 2) | 3.233 | 3.939 | -0.193 | 1.6744 | 1.0 | svr_rbf |  | 0.0022 | 0.0132 | 0.9397 | moins bon |
| SVR quantile RBF (niveau 3) | 3.261 | 3.934 | 0.143 | 1.0755 | 2.6 | svr_q_rbf | 89.3 | 0.4193 | 0.8386 | 0.7914 | équivalent |
| SVR quantile composite (niveau 4, retenu) (retenu) | 3.227 | 3.949 | -0.331 | 1.0548 | 9.2 | svr_q_composite | 84.2 |  |  |  | — choix retenu |
| SVR quantile, noyau laplacien | 3.256 | 3.953 | 0.036 | 1.086 | 2.9 | svr_q_laplacien | 89.3 | 0.164 | 0.492 | 0.7835 | équivalent |
| SVR quantile, noyau polynomial (degré 2) | 3.28 | 4.033 | -0.261 | 1.1032 | 4.3 | svr_q_polynomial | 85.3 | 0.0871 | 0.3484 | 0.4626 | équivalent |
| LS-SVR (moindres carrés), noyau RBF, quantiles LOO | 3.21 | 3.89 | -0.33 | 1.071 | 0.4 | lssvr_rbf | 92.7 | 0.5949 | 0.8386 | 0.8892 | équivalent |


Plus petite MAE : **LS-SVR (moindres carrés), noyau RBF, quantiles LOO** (3.21). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4, retenu) (retenu)).



### D11 · Chaque variable, une à une

*Que perd le modèle si on lui retire cette seule variable ? (modèle RBF du niveau 2, mêmes jours)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 3.233 | 3.939 | -0.193 | 1.6744 | 1.9 |  |  |  | — choix retenu |
| Sans occ_j-0 | 3.247 | 3.956 | -0.212 | 1.6873 | 2.3 | 0.344 | 1.0 | 0.5193 | équivalent |
| Sans occ_j-1 | 3.227 | 3.936 | -0.231 | 1.6829 | 2.0 | 0.1343 | 1.0 | 0.5966 | équivalent |
| Sans occ_j-2 | 3.239 | 3.952 | -0.208 | 1.6819 | 1.4 | 0.1891 | 1.0 | 0.6376 | équivalent |
| Sans occ_j-3 | 3.231 | 3.944 | -0.197 | 1.6744 | 0.9 | 0.9906 | 1.0 | 0.8283 | équivalent |
| Sans occ_j-4 | 3.234 | 3.94 | -0.219 | 1.6827 | 1.0 | 0.2193 | 1.0 | 0.9386 | équivalent |
| Sans occ_j-5 | 3.25 | 3.94 | -0.216 | 1.6899 | 0.8 | 0.0346 | 0.6228 | 0.1577 | équivalent |
| Sans occ_j-6 | 3.233 | 3.94 | -0.28 | 1.7007 | 0.7 | 0.0465 | 0.7905 | 0.9953 | équivalent |
| Sans adm_3j | 3.247 | 3.943 | -0.22 | 1.6894 | 0.9 | 0.0078 | 0.1482 | 0.3602 | équivalent |
| Sans adm_7j | 3.234 | 3.946 | -0.209 | 1.6796 | 0.8 | 0.7246 | 1.0 | 0.9775 | équivalent |
| Sans sorties_7j | 3.235 | 3.952 | -0.243 | 1.6902 | 0.7 | 0.3716 | 1.0 | 0.9451 | équivalent |
| Sans cible_jour_0 | 3.258 | 3.971 | -0.187 | 1.6852 | 0.9 | 0.0563 | 0.9008 | 0.0607 | équivalent |
| Sans cible_jour_1 | 3.233 | 3.942 | -0.192 | 1.6744 | 1.3 | 0.9982 | 1.0 | 0.9836 | équivalent |
| Sans cible_jour_2 | 3.23 | 3.94 | -0.214 | 1.6792 | 0.7 | 0.3454 | 1.0 | 0.7545 | équivalent |
| Sans cible_jour_3 | 3.228 | 3.932 | -0.214 | 1.678 | 0.9 | 0.3921 | 1.0 | 0.4703 | équivalent |
| Sans cible_jour_4 | 3.231 | 3.935 | -0.192 | 1.6728 | 0.7 | 0.6417 | 1.0 | 0.53 | équivalent |
| Sans cible_jour_5 | 3.242 | 3.944 | -0.17 | 1.6719 | 1.0 | 0.7398 | 1.0 | 0.6152 | équivalent |
| Sans cible_jour_6 | 3.235 | 3.95 | -0.211 | 1.6806 | 0.7 | 0.4349 | 1.0 | 0.9169 | équivalent |
| Sans mois_sin | 3.293 | 4.026 | -0.098 | 1.676 | 0.4 | 0.9707 | 1.0 | 0.3368 | équivalent |
| Sans mois_cos | 3.29 | 4.045 | 0.168 | 1.5946 | 0.9 | 0.0673 | 1.0 | 0.5302 | équivalent |


Plus petite MAE : **Sans occ_j-1** (3.227). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)).



### D14 · Sélection des variables par le lasso

*Le modèle gagne-t-il à ne garder que les variables choisies par le lasso ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 3.233 | 3.939 | -0.193 | 1.6744 | 1.5 | 19.0 |  |  |  | — choix retenu |
| Lasso, λ de plus petite erreur | 3.394 | 4.204 | -0.003 | 1.6977 | 12.9 | 3.6 | 0.7314 | 0.7314 | 0.0845 | équivalent |
| Lasso à un écart-type (λ_1se) | 3.347 | 4.124 | 0.206 | 1.6116 | 13.3 | 1.0 | 0.2575 | 0.515 | 0.2516 | équivalent |


Plus petite MAE : **Toutes les variables (retenu)** (3.233). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)).

