# Banc de comparaison des choix — service PED_journee

Validation glissante du 01/03/2026 au verrou (01/09/2026), une origine tous les 28 jours, modèle réentraîné à chaque origine. « (retenu) » = choix retenu. Test de Diebold-Mariano (perte absolue, correction HLN) contre le choix retenu.


## Horizon J+1 — 183 jours évalués, 7 origines


### D1 · Modèles de référence, concurrents et SVR

*Le SVR fait-il mieux que les méthodes statistiques usuelles et que les autres modèles d'apprentissage ?*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | couverture 90 % | réglages | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Persistance | 2.324 | 2.977 | 0.022 | 1.1557 | 0.0 |  |  | 0.0 | 0.0 | moins bon |
| Saisonnière hebdomadaire | 3.498 | 4.285 | 0.34 | 1.6472 | 0.0 |  |  | 0.0 | 0.0 | moins bon |
| Moyenne mobile 7 j | 3.104 | 3.913 | 0.128 | 1.5133 | 0.0 |  |  | 0.0 | 0.0 | moins bon |
| Moyenne historique | 3.287 | 3.96 | 0.185 | 1.1891 | 0.0 | 91.3 |  | 0.0 | 0.0 | moins bon |
| Lissage exponentiel simple | 2.324 | 2.977 | 0.022 | 0.8358 | 0.0 | 92.9 |  | 0.0002 | 0.0036 | moins bon |
| Méthode Thêta | 2.325 | 2.977 | 0.02 | 0.8358 | 0.0 | 92.9 |  | 0.0002 | 0.0036 | moins bon |
| Holt linéaire | 2.335 | 2.981 | 0.073 | 0.8371 | 0.2 | 89.6 |  | 0.0002 | 0.0036 | moins bon |
| Holt amorti | 2.324 | 2.977 | 0.022 | 0.8358 | 0.2 | 89.6 |  | 0.0002 | 0.0036 | moins bon |
| Lissage saisonnier sans tendance | 2.028 | 2.582 | 0.037 | 0.7276 | 0.2 | 90.7 |  | 0.098 | 0.784 | équivalent |
| Holt-Winters additif amorti | 2.028 | 2.582 | 0.037 | 0.7275 | 0.6 | 90.7 |  | 0.0981 | 0.784 | équivalent |
| Holt-Winters multiplicatif amorti | 2.027 | 2.57 | 0.077 | 0.7308 | 0.7 | 92.9 |  | 0.1047 | 0.784 | équivalent |
| AR(p) par AIC | 2.084 | 2.668 | 0.122 | 0.7757 | 0.1 | 88.0 |  | 0.0016 | 0.0176 | moins bon |
| SARIMA(2,0,0)(0,1,1)7 (ordre choisi sur l'apprentissage) | 1.935 | 2.505 | 0.07 | 0.7112 | 12.1 | 90.2 |  | 0.1474 | 0.784 | équivalent |
| Holt-Winters additif, grille fixée avant la validation | 2.053 | 2.594 | 0.039 | 1.0147 | 0.2 |  | alpha=0.9, beta=0.0, gamma=0.3, phi=0.8 | 0.0 | 0.0 | moins bon |
| Régression ridge (λ = 1) | 1.748 | 2.227 | 0.114 | 0.8396 | 0.1 |  |  | 0.0012 | 0.0144 | moins bon |
| A · forêt aléatoire quantile | 1.921 | 2.533 | 0.044 | 0.7303 | 21.0 | 94.0 |  | 0.0278 | 0.252 | équivalent |
| B · gradient boosting quantile | 1.812 | 2.375 | 0.053 | 0.6955 | 11.9 | 83.6 |  | 0.3057 | 1.0 | équivalent |
| C · perceptron multicouche quantile | 1.738 | 2.226 | -0.042 | 0.6385 | 1.4 | 89.1 |  | 0.4275 | 1.0 | équivalent |
| D · LSTM quantile | 1.73 | 2.241 | 0.064 | 0.6398 | 17.6 | 89.6 |  | 0.4639 | 1.0 | équivalent |
| E · XGBoost quantile (second ordre) | 1.833 | 2.37 | -0.031 | 0.7238 | 13.4 | 91.3 |  | 0.0252 | 0.252 | équivalent |
| SVR linéaire (niveau 1) | 1.748 | 2.232 | 0.036 | 0.8633 | 0.3 |  |  | 0.0004 | 0.0052 | moins bon |
| SVR RBF (niveau 2) | 1.719 | 2.191 | -0.043 | 0.8724 | 1.7 |  |  | 0.0002 | 0.0036 | moins bon |
| SVR quantile RBF (niveau 3) | 1.773 | 2.244 | -0.118 | 0.6516 | 5.5 | 88.5 |  | 0.5976 | 1.0 | équivalent |
| SVR quantile composite (niveau 4) (retenu) | 1.793 | 2.283 | -0.079 | 0.6614 | 7.1 | 89.1 |  |  |  | — choix retenu |


Plus petite perte pinball à τ = 0.8 : **C · perceptron multicouche quantile** (0.6385). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4) (retenu)) après correction de Holm.



### D2 · Noyau

*Quel noyau décrit le mieux la dynamique ? (même perte ε-insensible, même C)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Linéaire | 1.749 | 2.24 | 0.046 | 0.8608 | 0.4 | 0.4558 | 0.9116 | équivalent |
| RBF (γ = 0.02) | 1.719 | 2.191 | -0.043 | 0.8724 | 1.6 | 0.5593 | 0.9116 | équivalent |
| Composite occupation / flux et saison (β appris) (retenu) | 1.756 | 2.242 | -0.002 | 0.8787 | 2.8 |  |  | — choix retenu |


Plus petite perte pinball à τ = 0.8 : **Linéaire** (0.8608). Aucune variante ne bat significativement le choix retenu (Composite occupation / flux et saison (β appris) (retenu)) après correction de Holm.



### D3 · Fonction de perte

*Quelle perte pour un modèle linéaire identique ? (isole l'effet de la perte)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Carrée (ridge, λ = 1/C) | 1.747 | 2.226 | 0.113 | 0.8396 | 0.1 | 0.0095 | 0.0285 | meilleur |
| ε-insensible, ε = 0 lit (= valeur absolue) | 1.765 | 2.256 | 0.007 | 0.8803 | 0.7 | 0.0482 | 0.0964 | équivalent |
| ε-insensible, ε = 0.5 lit | 1.755 | 2.24 | -0.014 | 0.8815 | 0.3 | 0.0069 | 0.0276 | moins bon |
| ε-insensible, ε = 1 lit (retenu) | 1.748 | 2.232 | 0.036 | 0.8633 | 0.3 |  |  | — choix retenu |
| ε-insensible, ε = 2 lit | 1.764 | 2.252 | 0.073 | 0.8599 | 0.5 | 0.7632 | 0.7632 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Carrée (ridge, λ = 1/C)** (0.8396). ⚠ Significativement meilleur que le choix retenu (Holm, 5 %) : Carrée (ridge, λ = 1/C) — le choix est à revoir.



### D4 · Quantile décisionnel τ et coût des décisions

*Quel τ minimise le coût réel selon le rapport pénurie / lit vide ? (τ optimal théorique = r/(1+r))*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | jours sous-estimés % | lits prévus en moyenne | coût r=1 | coût r=2 | coût r=4 | coût r=9 | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| τ = 0.5 | 1.773 | 2.244 | -0.118 | 0.9217 | 1.7 | 50.3 | 10.91 | 1.773 | 2.718 | 4.609 | 9.335 | 0.0 | 0.0 | moins bon |
| τ = 0.6 | 1.812 | 2.269 | 0.308 | 0.8136 | 1.1 | 43.2 | 11.34 | 1.812 | 2.564 | 4.068 | 7.828 | 0.0001 | 0.0003 | moins bon |
| τ = 0.7 | 1.941 | 2.41 | 0.89 | 0.7036 | 1.3 | 33.3 | 11.92 | 1.941 | 2.467 | 3.518 | 6.146 | 0.0292 | 0.0292 | moins bon |
| τ = 0.8 (retenu) | 2.264 | 2.767 | 1.601 | 0.6516 | 1.2 | 21.3 | 12.63 | 2.264 | 2.595 | 3.258 | 4.916 |  |  | — choix retenu |
| τ = 0.9 | 3.461 | 3.993 | 3.221 | 0.7644 | 1.2 | 8.2 | 14.25 | 3.461 | 3.581 | 3.822 | 4.423 | 0.0018 | 0.0036 | moins bon |


τ le moins coûteux pour chaque rapport de coûts r = c_pénurie / c_lit vide : r = 1 → τ = 0.5, r = 2 → τ = 0.7, r = 4 → τ = 0.8 (retenu), r = 9 → τ = 0.9. Le choix τ = 0.8 correspond à r = 4.


### D5 · Variables d'entrée

*Que rapporte chaque groupe de variables ? (même modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| 7 retards seuls | 2.205 | 2.791 | -0.01 | 1.1054 | 1.2 | 7 | 0.0 | 0.0 | moins bon |
| 7 retards + flux | 1.978 | 2.437 | 0.117 | 0.9541 | 1.4 | 10 | 0.0026 | 0.0208 | moins bon |
| 7 retards + calendrier (jour, mois) | 1.906 | 2.503 | -0.127 | 0.9912 | 1.2 | 16 | 0.0061 | 0.0427 | moins bon |
| Complet : retards + flux + calendrier (retenu) | 1.719 | 2.191 | -0.043 | 0.8724 | 1.7 | 19 |  |  | — choix retenu |
| Complet + jours fériés camerounais | 1.719 | 2.196 | -0.043 | 0.8722 | 1.3 | 21 | 0.9586 | 1.0 | équivalent |
| Complet + vacances scolaires | 1.711 | 2.178 | -0.031 | 0.8648 | 1.6 | 20 | 0.0209 | 0.1045 | équivalent |
| Complet + fériés + vacances scolaires | 1.71 | 2.182 | -0.026 | 0.8625 | 1.1 | 22 | 0.0323 | 0.1292 | équivalent |
| 3 retards + flux + calendrier | 1.734 | 2.26 | -0.149 | 0.9118 | 1.4 | 15 | 0.1387 | 0.4161 | équivalent |
| 14 retards + flux + calendrier | 1.746 | 2.214 | 0.01 | 0.8699 | 1.4 | 26 | 0.8944 | 1.0 | équivalent |
| Complet + diagnostics d'entrée des présents | 1.807 | 2.312 | -0.122 | 0.94 | 1.2 | 30 | 0.014 | 0.084 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Complet + fériés + vacances scolaires** (0.8625). Aucune variante ne bat significativement le choix retenu (Complet : retards + flux + calendrier (retenu)) après correction de Holm.



### D6 · Prétraitement

*Quelle mise à l'échelle des variables ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| z-score : (x − moyenne)/écart-type (retenu) | 1.719 | 2.191 | -0.043 | 0.8724 | 1.7 |  |  | — choix retenu |
| Robuste : (x − médiane)/(Q3 − Q1) | 1.734 | 2.216 | 0.009 | 0.8641 | 1.4 | 0.4328 | 0.4328 | équivalent |
| Min-max : (x − min)/(max − min) | 2.334 | 2.933 | -0.186 | 1.2227 | 0.3 | 0.0 | 0.0 | moins bon |
| Aucune mise à l'échelle | 2.277 | 2.864 | 0.253 | 1.0626 | 1.0 | 0.0009 | 0.0018 | moins bon |


Plus petite perte pinball à τ = 0.8 : **Robuste : (x − médiane)/(Q3 − Q1)** (0.8641). Aucune variante ne bat significativement le choix retenu (z-score : (x − moyenne)/écart-type (retenu)) après correction de Holm.



### D7 · Fenêtre d'entraînement

*Faut-il tout le passé, ou seulement les derniers mois ? (mesure aussi le coût d'un historique court)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Croissante (tout le passé) (retenu) | 1.793 | 2.283 | -0.079 | 0.6614 | 89.1 | 7.1 |  |  | — choix retenu |
| Glissante : 365 derniers jours | 1.809 | 2.301 | -0.227 | 0.6716 | 88.0 | 6.1 | 0.5031 | 0.5031 | équivalent |
| Glissante : 180 derniers jours | 2.049 | 2.586 | 0.088 | 0.7662 | 85.8 | 4.7 | 0.0009 | 0.0018 | moins bon |
| Glissante : 90 derniers jours | 2.359 | 2.979 | -0.055 | 0.9191 | 78.1 | 4.9 | 0.0 | 0.0 | moins bon |


Plus petite perte pinball à τ = 0.8 : **Croissante (tout le passé) (retenu)** (0.6614). Aucune variante ne bat significativement le choix retenu (Croissante (tout le passé) (retenu)) après correction de Holm.



### D8 · Optimisation

*Comment atteindre le minimum de J le plus sûrement ? (SVR RBF, un découpage)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | J final | pas effectués | arrêt | solution gardée | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Adam + Polyak + préconditionnement + décroissance η (retenu) | 1.736 | 2.208 | -0.047 | 0.882 | 0.8 | 2079.03 | 3000 | 3000 pas atteints | meilleur point rencontré |  |  | — choix retenu |
| Adam sans moyenne de Polyak | 1.736 | 2.208 | -0.047 | 0.882 | 0.7 | 2079.03 | 3000 | 3000 pas atteints | meilleur point rencontré |  |  | identique |
| Adam sans préconditionnement | 1.753 | 2.233 | -0.065 | 0.896 | 1.0 | 2118.64 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.073 | 0.073 | équivalent |
| Adam sans décroissance de η | 1.735 | 2.208 | -0.057 | 0.8846 | 0.8 | 2079.3 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | moins bon |
| Momentum | 2.568 | 3.269 | -0.782 | 1.5188 | 0.6 | 3228.02 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | moins bon |
| Descente de gradient simple | 2.568 | 3.269 | -0.782 | 1.5188 | 0.6 | 3228.02 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0 | 0.0 | moins bon |


Plus petite perte pinball à τ = 0.8 : **Adam + Polyak + préconditionnement + décroissance η (retenu)** (0.882). Aucune variante ne bat significativement le choix retenu (Adam + Polyak + préconditionnement + décroissance η (retenu)) après correction de Holm.



### D9 · Combinaison des modèles

*Apprendre les poids de combinaison apporte-t-il plus qu'une moyenne ? (jours où l'empilement prédit)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Niveau 4 seul (meilleur modèle unique) | 1.728 | 2.219 | -0.132 | 0.6464 | 89.7 | 7.6 | 0.804 | 1.0 | équivalent |
| Moyenne simple persistance + niv. 3 + niv. 4 | 1.776 | 2.306 | -0.101 | 0.7053 | 75.5 | 15.2 | 0.0743 | 0.2972 | équivalent |
| Empilement appris (poids positifs) (retenu) | 1.743 | 2.237 | -0.276 | 0.6515 | 83.9 | 26.4 |  |  | — choix retenu |
| XGBoost quantile seul | 1.8 | 2.34 | -0.032 | 0.7212 | 90.3 | 14.5 | 0.034 | 0.17 | équivalent |
| Moyenne SVR niv. 4 + XGBoost | 1.729 | 2.248 | -0.082 | 0.6643 | 92.3 | 22.1 | 0.5837 | 1.0 | équivalent |
| Empilement persistance + niv. 3 + niv. 4 + XGBoost | 1.748 | 2.248 | -0.252 | 0.6515 | 83.2 | 40.6 | 0.9954 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Niveau 4 seul (meilleur modèle unique)** (0.6464). Aucune variante ne bat significativement le choix retenu (Empilement appris (poids positifs) (retenu)) après correction de Holm.



### D13 · Variantes de SVM

*Quel SVM est le plus adapté à la série du service ? (mêmes jours, mêmes variables)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | cle | couverture 90 % | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| SVR linéaire (niveau 1) | 1.748 | 2.232 | 0.036 | 0.8633 | 0.3 | svr_lineaire |  | 0.0004 | 0.002 | moins bon |
| SVR RBF (niveau 2) | 1.719 | 2.191 | -0.043 | 0.8724 | 2.0 | svr_rbf |  | 0.0002 | 0.0012 | moins bon |
| SVR quantile RBF (niveau 3) | 1.773 | 2.244 | -0.118 | 0.6516 | 6.7 | svr_q_rbf | 88.5 | 0.5976 | 1.0 | équivalent |
| SVR quantile composite (niveau 4, retenu) (retenu) | 1.793 | 2.283 | -0.079 | 0.6614 | 9.0 | svr_q_composite | 89.1 |  |  | — choix retenu |
| SVR quantile, noyau laplacien | 1.854 | 2.338 | -0.091 | 0.6618 | 5.9 | svr_q_laplacien | 89.1 | 0.9789 | 1.0 | équivalent |
| SVR quantile, noyau polynomial (degré 2) | 1.772 | 2.258 | -0.091 | 0.6349 | 7.8 | svr_q_polynomial | 86.9 | 0.3245 | 1.0 | équivalent |
| LS-SVR (moindres carrés), noyau RBF, quantiles LOO | 1.68 | 2.159 | -0.099 | 0.6322 | 0.2 | lssvr_rbf | 92.3 | 0.2955 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **LS-SVR (moindres carrés), noyau RBF, quantiles LOO** (0.6322). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4, retenu) (retenu)) après correction de Holm.



### D11 · Chaque variable, une à une

*Que perd le modèle si on lui retire cette seule variable ? (modèle RBF du niveau 2, mêmes jours)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 1.719 | 2.191 | -0.043 | 0.8724 | 1.9 |  |  | — choix retenu |
| Sans occ_j-0 | 1.849 | 2.261 | -0.037 | 0.9355 | 1.3 | 0.0319 | 0.4785 | équivalent |
| Sans occ_j-1 | 1.722 | 2.198 | -0.05 | 0.8761 | 1.7 | 0.7006 | 1.0 | équivalent |
| Sans occ_j-2 | 1.725 | 2.191 | -0.047 | 0.8766 | 1.7 | 0.2883 | 1.0 | équivalent |
| Sans occ_j-3 | 1.726 | 2.208 | -0.028 | 0.8716 | 1.3 | 0.8449 | 1.0 | équivalent |
| Sans occ_j-4 | 1.721 | 2.196 | -0.037 | 0.8715 | 1.8 | 0.7849 | 1.0 | équivalent |
| Sans occ_j-5 | 1.727 | 2.198 | -0.017 | 0.8686 | 2.1 | 0.4492 | 1.0 | équivalent |
| Sans occ_j-6 | 1.705 | 2.204 | -0.108 | 0.8849 | 2.0 | 0.4251 | 1.0 | équivalent |
| Sans adm_3j | 1.725 | 2.24 | -0.003 | 0.8633 | 1.8 | 0.5584 | 1.0 | équivalent |
| Sans adm_7j | 1.746 | 2.228 | -0.035 | 0.8832 | 1.7 | 0.2982 | 1.0 | équivalent |
| Sans sorties_7j | 1.852 | 2.407 | -0.094 | 0.9541 | 1.6 | 0.0264 | 0.4224 | équivalent |
| Sans cible_jour_0 | 1.795 | 2.286 | -0.092 | 0.9251 | 1.3 | 0.0031 | 0.0558 | équivalent |
| Sans cible_jour_1 | 1.72 | 2.194 | -0.042 | 0.8725 | 2.1 | 0.9389 | 1.0 | équivalent |
| Sans cible_jour_2 | 1.718 | 2.189 | -0.037 | 0.8703 | 1.4 | 0.473 | 1.0 | équivalent |
| Sans cible_jour_3 | 1.719 | 2.192 | -0.035 | 0.87 | 2.0 | 0.0958 | 1.0 | équivalent |
| Sans cible_jour_4 | 1.724 | 2.194 | -0.049 | 0.8766 | 2.0 | 0.2062 | 1.0 | équivalent |
| Sans cible_jour_5 | 1.767 | 2.239 | -0.025 | 0.8906 | 1.9 | 0.0574 | 0.8036 | équivalent |
| Sans cible_jour_6 | 1.718 | 2.19 | -0.053 | 0.875 | 1.8 | 0.0648 | 0.8424 | équivalent |
| Sans mois_sin | 1.719 | 2.185 | 0.041 | 0.8472 | 1.5 | 0.0 | 0.0 | meilleur |
| Sans mois_cos | 1.75 | 2.22 | 0.126 | 0.8373 | 1.7 | 0.0037 | 0.0629 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Sans mois_cos** (0.8373). ⚠ Significativement meilleur que le choix retenu (Holm, 5 %) : Sans mois_sin — le choix est à revoir.



### D14 · Sélection des variables par le lasso

*Le modèle gagne-t-il à ne garder que les variables choisies par le lasso ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 1.719 | 2.191 | -0.043 | 0.8724 | 1.8 | 19.0 |  |  | — choix retenu |
| Lasso, λ de plus petite erreur | 1.726 | 2.2 | -0.034 | 0.8731 | 17.4 | 16.3 | 0.906 | 0.906 | équivalent |
| Lasso à un écart-type (λ_1se) | 1.779 | 2.251 | 0.172 | 0.8378 | 16.1 | 8.0 | 0.0602 | 0.1204 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Lasso à un écart-type (λ_1se)** (0.8378). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)) après correction de Holm.



## Horizon J+7 — 177 jours évalués, 7 origines


### D1 · Modèles de référence, concurrents et SVR

*Le SVR fait-il mieux que les méthodes statistiques usuelles et que les autres modèles d'apprentissage ?*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | couverture 90 % | réglages | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| Persistance | 4.454 | 5.532 | 0.351 | 2.1217 | 0.0 |  |  | 0.0004 | 0.0064 | moins bon |
| Saisonnière hebdomadaire | 3.487 | 4.274 | 0.414 | 1.6193 | 0.0 |  |  | 0.0119 | 0.0833 | équivalent |
| Moyenne mobile 7 j | 4.268 | 5.137 | 0.319 | 2.0383 | 0.0 |  |  | 0.0011 | 0.0165 | moins bon |
| Moyenne historique | 3.265 | 3.941 | 0.276 | 1.1493 | 0.0 | 93.2 |  | 0.0738 | 0.238 | équivalent |
| Lissage exponentiel simple | 4.454 | 5.532 | 0.351 | 1.5953 | 0.0 | 85.3 |  | 0.0001 | 0.0023 | moins bon |
| Méthode Thêta | 4.453 | 5.532 | 0.336 | 1.5953 | 0.0 | 85.3 |  | 0.0001 | 0.0023 | moins bon |
| Holt linéaire | 4.551 | 5.618 | 0.717 | 1.6135 | 0.2 | 84.7 |  | 0.0001 | 0.0023 | moins bon |
| Holt amorti | 4.454 | 5.532 | 0.351 | 1.5953 | 0.2 | 84.7 |  | 0.0001 | 0.0023 | moins bon |
| Lissage saisonnier sans tendance | 4.454 | 5.532 | 0.351 | 1.5953 | 0.2 | 83.6 |  | 0.0001 | 0.0023 | moins bon |
| Holt-Winters additif amorti | 4.454 | 5.532 | 0.351 | 1.5953 | 0.6 | 84.2 |  | 0.0001 | 0.0023 | moins bon |
| Holt-Winters multiplicatif amorti | 4.454 | 5.532 | 0.351 | 1.5953 | 0.7 | 84.7 |  | 0.0001 | 0.0023 | moins bon |
| AR(p) par AIC | 3.332 | 4.09 | 0.405 | 1.1666 | 0.1 | 84.7 |  | 0.0595 | 0.238 | équivalent |
| SARIMA(2,0,0)(0,1,1)7 (ordre choisi sur l'apprentissage) | 3.267 | 4.029 | 0.29 | 1.1411 | 12.0 | 87.6 |  | 0.2005 | 0.401 | équivalent |
| Holt-Winters additif, grille fixée avant la validation | 3.612 | 4.375 | 0.359 | 1.6982 | 0.3 |  | alpha=0.1, beta=0.0, gamma=0.05, phi=0.98 | 0.0104 | 0.0832 | équivalent |
| Régression ridge (λ = 1) | 3.275 | 4.032 | -0.18 | 1.6916 | 0.1 |  |  | 0.0037 | 0.0444 | moins bon |
| A · forêt aléatoire quantile | 3.244 | 3.915 | -0.259 | 1.1275 | 19.7 | 93.2 |  | 0.0087 | 0.0783 | équivalent |
| B · gradient boosting quantile | 3.161 | 3.886 | -0.525 | 1.1944 | 12.4 | 78.5 |  | 0.0016 | 0.0224 | moins bon |
| C · perceptron multicouche quantile | 3.23 | 3.999 | -0.289 | 1.1661 | 1.3 | 88.7 |  | 0.0442 | 0.221 | équivalent |
| D · LSTM quantile | 3.295 | 4.043 | -0.091 | 1.1959 | 15.8 | 82.5 |  | 0.018 | 0.108 | équivalent |
| E · XGBoost quantile (second ordre) | 3.164 | 3.876 | -0.328 | 1.1209 | 15.3 | 87.0 |  | 0.0059 | 0.059 | équivalent |
| SVR linéaire (niveau 1) | 3.29 | 4.065 | -0.161 | 1.6931 | 0.4 |  |  | 0.0045 | 0.0495 | moins bon |
| SVR RBF (niveau 2) | 3.233 | 3.939 | -0.193 | 1.6744 | 1.2 |  |  | 0.0022 | 0.0286 | moins bon |
| SVR quantile RBF (niveau 3) | 3.261 | 3.934 | 0.143 | 1.0755 | 1.8 | 89.3 |  | 0.4193 | 0.4193 | équivalent |
| SVR quantile composite (niveau 4) (retenu) | 3.227 | 3.949 | -0.331 | 1.0548 | 10.3 | 84.2 |  |  |  | — choix retenu |


Plus petite perte pinball à τ = 0.8 : **SVR quantile composite (niveau 4) (retenu)** (1.0548). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4) (retenu)) après correction de Holm.



### D2 · Noyau

*Quel noyau décrit le mieux la dynamique ? (même perte ε-insensible, même C)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Linéaire | 3.292 | 4.07 | -0.163 | 1.6951 | 0.2 | 0.9228 | 1.0 | équivalent |
| RBF (γ = 0.05) | 3.233 | 3.939 | -0.193 | 1.6744 | 1.1 | 0.6833 | 1.0 | équivalent |
| Composite occupation / flux et saison (β appris) (retenu) | 3.192 | 3.935 | -0.321 | 1.6922 | 1.4 |  |  | — choix retenu |


Plus petite perte pinball à τ = 0.8 : **RBF (γ = 0.05)** (1.6744). Aucune variante ne bat significativement le choix retenu (Composite occupation / flux et saison (β appris) (retenu)) après correction de Holm.



### D3 · Fonction de perte

*Quelle perte pour un modèle linéaire identique ? (isole l'effet de la perte)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Carrée (ridge, λ = 1/C) | 3.275 | 4.032 | -0.18 | 1.6917 | 0.1 | 0.9503 | 1.0 | équivalent |
| ε-insensible, ε = 0 lit (= valeur absolue) | 3.355 | 4.155 | -0.126 | 1.715 | 0.5 | 0.4154 | 1.0 | équivalent |
| ε-insensible, ε = 0.5 lit | 3.315 | 4.095 | -0.122 | 1.6941 | 0.3 | 0.9502 | 1.0 | équivalent |
| ε-insensible, ε = 1 lit (retenu) | 3.29 | 4.065 | -0.161 | 1.6931 | 0.5 |  |  | — choix retenu |
| ε-insensible, ε = 2 lit | 3.265 | 4.03 | -0.245 | 1.7061 | 0.4 | 0.5531 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Carrée (ridge, λ = 1/C)** (1.6917). Aucune variante ne bat significativement le choix retenu (ε-insensible, ε = 1 lit (retenu)) après correction de Holm.



### D4 · Quantile décisionnel τ et coût des décisions

*Quel τ minimise le coût réel selon le rapport pénurie / lit vide ? (τ optimal théorique = r/(1+r))*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | jours sous-estimés % | lits prévus en moyenne | coût r=1 | coût r=2 | coût r=4 | coût r=9 | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| τ = 0.5 | 3.261 | 3.934 | 0.143 | 1.5877 | 0.6 | 48.6 | 11.08 | 3.261 | 4.82 | 7.939 | 15.735 | 0.0069 | 0.0276 | moins bon |
| τ = 0.6 | 3.362 | 4.097 | 1.126 | 1.3432 | 0.4 | 41.2 | 12.07 | 3.362 | 4.48 | 6.716 | 12.306 | 0.0338 | 0.1014 | équivalent |
| τ = 0.7 | 3.654 | 4.508 | 2.212 | 1.1632 | 0.4 | 33.3 | 13.15 | 3.654 | 4.375 | 5.816 | 9.42 | 0.1532 | 0.3064 | équivalent |
| τ = 0.8 (retenu) | 4.133 | 5.128 | 3.304 | 1.0755 | 0.7 | 22.6 | 14.25 | 4.133 | 4.548 | 5.378 | 7.452 |  |  | — choix retenu |
| τ = 0.9 | 5.505 | 6.508 | 5.207 | 1.1907 | 0.6 | 9.6 | 16.15 | 5.505 | 5.655 | 5.953 | 6.7 | 0.1642 | 0.3064 | équivalent |


τ le moins coûteux pour chaque rapport de coûts r = c_pénurie / c_lit vide : r = 1 → τ = 0.5, r = 2 → τ = 0.7, r = 4 → τ = 0.8 (retenu), r = 9 → τ = 0.9. Le choix τ = 0.8 correspond à r = 4.


### D5 · Variables d'entrée

*Que rapporte chaque groupe de variables ? (même modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| 7 retards seuls | 3.401 | 4.17 | 0.253 | 1.6245 | 0.5 | 7 | 0.439 | 1.0 | équivalent |
| 7 retards + flux | 3.417 | 4.2 | 0.281 | 1.6245 | 0.6 | 10 | 0.307 | 1.0 | équivalent |
| 7 retards + calendrier (jour, mois) | 3.246 | 3.961 | -0.269 | 1.7036 | 0.6 | 16 | 0.1833 | 1.0 | équivalent |
| Complet : retards + flux + calendrier (retenu) | 3.233 | 3.939 | -0.193 | 1.6744 | 1.0 | 19 |  |  | — choix retenu |
| Complet + jours fériés camerounais | 3.23 | 3.937 | -0.192 | 1.6728 | 0.7 | 21 | 0.4244 | 1.0 | équivalent |
| Complet + vacances scolaires | 3.229 | 3.941 | -0.291 | 1.7018 | 0.4 | 20 | 0.2619 | 1.0 | équivalent |
| Complet + fériés + vacances scolaires | 3.225 | 3.937 | -0.286 | 1.6984 | 0.8 | 22 | 0.3104 | 1.0 | équivalent |
| 3 retards + flux + calendrier | 3.235 | 3.942 | -0.286 | 1.7032 | 0.7 | 15 | 0.2446 | 1.0 | équivalent |
| 14 retards + flux + calendrier | 3.274 | 4.002 | -0.179 | 1.6908 | 0.9 | 26 | 0.7397 | 1.0 | équivalent |
| Complet + diagnostics d'entrée des présents | 3.205 | 3.886 | -0.31 | 1.6954 | 0.9 | 30 | 0.7633 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **7 retards seuls** (1.6245). Aucune variante ne bat significativement le choix retenu (Complet : retards + flux + calendrier (retenu)) après correction de Holm.



### D6 · Prétraitement

*Quelle mise à l'échelle des variables ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| z-score : (x − moyenne)/écart-type (retenu) | 3.233 | 3.939 | -0.193 | 1.6744 | 1.1 |  |  | — choix retenu |
| Robuste : (x − médiane)/(Q3 − Q1) | 3.296 | 4.053 | 0.002 | 1.6475 | 0.9 | 0.5678 | 1.0 | équivalent |
| Min-max : (x − min)/(max − min) | 3.245 | 3.934 | -0.081 | 1.6469 | 0.8 | 0.5884 | 1.0 | équivalent |
| Aucune mise à l'échelle | 3.264 | 3.931 | 0.251 | 1.5566 | 0.4 | 0.0817 | 0.2451 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Aucune mise à l'échelle** (1.5566). Aucune variante ne bat significativement le choix retenu (z-score : (x − moyenne)/écart-type (retenu)) après correction de Holm.



### D7 · Fenêtre d'entraînement

*Faut-il tout le passé, ou seulement les derniers mois ? (mesure aussi le coût d'un historique court)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Croissante (tout le passé) (retenu) | 3.227 | 3.949 | -0.331 | 1.0548 | 84.2 | 9.0 |  |  | — choix retenu |
| Glissante : 365 derniers jours | 3.246 | 3.929 | -0.472 | 1.0966 | 84.2 | 6.3 | 0.0558 | 0.1674 | équivalent |
| Glissante : 180 derniers jours | 3.206 | 3.862 | 0.015 | 1.0377 | 83.1 | 4.7 | 0.7937 | 1.0 | équivalent |
| Glissante : 90 derniers jours | 3.354 | 4.04 | 0.4 | 1.0855 | 84.2 | 5.1 | 0.7135 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Glissante : 180 derniers jours** (1.0377). Aucune variante ne bat significativement le choix retenu (Croissante (tout le passé) (retenu)) après correction de Holm.



### D8 · Optimisation

*Comment atteindre le minimum de J le plus sûrement ? (SVR RBF, un découpage)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | J final | pas effectués | arrêt | solution gardée | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Adam + Polyak + préconditionnement + décroissance η (retenu) | 3.213 | 3.936 | -0.301 | 1.6968 | 0.1 | 1312.79 | 376 | J stable depuis 100 pas (pas 375) | moyenne de Polyak sur 100 pas |  |  | — choix retenu |
| Adam sans moyenne de Polyak | 3.213 | 3.936 | -0.299 | 1.6961 | 0.1 | 1312.8 | 376 | J stable depuis 100 pas (pas 375) | meilleur point rencontré | 0.0115 | 0.0575 | équivalent |
| Adam sans préconditionnement | 3.202 | 3.926 | -0.3 | 1.6911 | 1.1 | 1315.51 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.0214 | 0.0856 | équivalent |
| Adam sans décroissance de η | 3.213 | 3.936 | -0.304 | 1.6975 | 0.1 | 1312.8 | 385 | J stable depuis 100 pas (pas 384) | moyenne de Polyak sur 100 pas | 0.0272 | 0.0856 | équivalent |
| Momentum | 3.53 | 4.34 | -0.095 | 1.7933 | 0.7 | 1398.69 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.1551 | 0.3102 | équivalent |
| Descente de gradient simple | 3.388 | 4.149 | 0.202 | 1.6336 | 0.6 | 1393.14 | 3000 | 3000 pas atteints | meilleur point rencontré | 0.1679 | 0.3102 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Descente de gradient simple** (1.6336). Aucune variante ne bat significativement le choix retenu (Adam + Polyak + préconditionnement + décroissance η (retenu)) après correction de Holm.



### D9 · Combinaison des modèles

*Apprendre les poids de combinaison apporte-t-il plus qu'une moyenne ? (jours où l'empilement prédit)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Niveau 4 seul (meilleur modèle unique) | 3.291 | 3.999 | -0.749 | 1.0675 | 82.6 | 4.8 | 0.2181 | 1.0 | équivalent |
| Moyenne simple persistance + niv. 3 + niv. 4 | 3.583 | 4.395 | -0.252 | 1.3361 | 61.7 | 9.6 | 0.3309 | 1.0 | équivalent |
| Empilement appris (poids positifs) (retenu) | 3.56 | 4.376 | -0.177 | 1.2213 | 73.2 | 20.1 |  |  | — choix retenu |
| XGBoost quantile seul | 3.231 | 3.932 | -0.753 | 1.1471 | 85.9 | 14.6 | 0.5822 | 1.0 | équivalent |
| Moyenne SVR niv. 4 + XGBoost | 3.257 | 3.941 | -0.751 | 1.101 | 85.2 | 19.4 | 0.3526 | 1.0 | équivalent |
| Empilement persistance + niv. 3 + niv. 4 + XGBoost | 3.519 | 4.317 | -0.379 | 1.2197 | 70.5 | 34.8 | 0.6316 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Niveau 4 seul (meilleur modèle unique)** (1.0675). Aucune variante ne bat significativement le choix retenu (Empilement appris (poids positifs) (retenu)) après correction de Holm.



### D13 · Variantes de SVM

*Quel SVM est le plus adapté à la série du service ? (mêmes jours, mêmes variables)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | cle | couverture 90 % | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|---|
| SVR linéaire (niveau 1) | 3.29 | 4.065 | -0.161 | 1.6931 | 0.4 | svr_lineaire |  | 0.0045 | 0.0225 | moins bon |
| SVR RBF (niveau 2) | 3.233 | 3.939 | -0.193 | 1.6744 | 1.0 | svr_rbf |  | 0.0022 | 0.0132 | moins bon |
| SVR quantile RBF (niveau 3) | 3.261 | 3.934 | 0.143 | 1.0755 | 1.7 | svr_q_rbf | 89.3 | 0.4193 | 0.8386 | équivalent |
| SVR quantile composite (niveau 4, retenu) (retenu) | 3.227 | 3.949 | -0.331 | 1.0548 | 8.6 | svr_q_composite | 84.2 |  |  | — choix retenu |
| SVR quantile, noyau laplacien | 3.256 | 3.953 | 0.036 | 1.086 | 2.3 | svr_q_laplacien | 89.3 | 0.164 | 0.492 | équivalent |
| SVR quantile, noyau polynomial (degré 2) | 3.28 | 4.033 | -0.261 | 1.1032 | 4.9 | svr_q_polynomial | 85.3 | 0.0871 | 0.3484 | équivalent |
| LS-SVR (moindres carrés), noyau RBF, quantiles LOO | 3.21 | 3.89 | -0.33 | 1.071 | 0.1 | lssvr_rbf | 92.7 | 0.5949 | 0.8386 | équivalent |


Plus petite perte pinball à τ = 0.8 : **SVR quantile composite (niveau 4, retenu) (retenu)** (1.0548). Aucune variante ne bat significativement le choix retenu (SVR quantile composite (niveau 4, retenu) (retenu)) après correction de Holm.



### D11 · Chaque variable, une à une

*Que perd le modèle si on lui retire cette seule variable ? (modèle RBF du niveau 2, mêmes jours)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 3.233 | 3.939 | -0.193 | 1.6744 | 1.0 |  |  | — choix retenu |
| Sans occ_j-0 | 3.247 | 3.956 | -0.212 | 1.6873 | 1.0 | 0.344 | 1.0 | équivalent |
| Sans occ_j-1 | 3.227 | 3.936 | -0.231 | 1.6829 | 0.6 | 0.1343 | 1.0 | équivalent |
| Sans occ_j-2 | 3.239 | 3.952 | -0.208 | 1.6819 | 0.5 | 0.1891 | 1.0 | équivalent |
| Sans occ_j-3 | 3.231 | 3.944 | -0.197 | 1.6744 | 0.7 | 0.9906 | 1.0 | équivalent |
| Sans occ_j-4 | 3.234 | 3.94 | -0.219 | 1.6827 | 0.9 | 0.2193 | 1.0 | équivalent |
| Sans occ_j-5 | 3.25 | 3.94 | -0.216 | 1.6899 | 0.8 | 0.0346 | 0.6228 | équivalent |
| Sans occ_j-6 | 3.233 | 3.94 | -0.28 | 1.7007 | 0.9 | 0.0465 | 0.7905 | équivalent |
| Sans adm_3j | 3.247 | 3.943 | -0.22 | 1.6894 | 0.8 | 0.0078 | 0.1482 | équivalent |
| Sans adm_7j | 3.234 | 3.946 | -0.209 | 1.6796 | 0.8 | 0.7246 | 1.0 | équivalent |
| Sans sorties_7j | 3.235 | 3.952 | -0.243 | 1.6902 | 0.7 | 0.3716 | 1.0 | équivalent |
| Sans cible_jour_0 | 3.258 | 3.971 | -0.187 | 1.6852 | 0.8 | 0.0563 | 0.9008 | équivalent |
| Sans cible_jour_1 | 3.233 | 3.942 | -0.192 | 1.6744 | 1.3 | 0.9982 | 1.0 | équivalent |
| Sans cible_jour_2 | 3.23 | 3.94 | -0.214 | 1.6792 | 0.9 | 0.3454 | 1.0 | équivalent |
| Sans cible_jour_3 | 3.228 | 3.932 | -0.214 | 1.678 | 0.8 | 0.3921 | 1.0 | équivalent |
| Sans cible_jour_4 | 3.231 | 3.935 | -0.192 | 1.6728 | 0.7 | 0.6417 | 1.0 | équivalent |
| Sans cible_jour_5 | 3.242 | 3.944 | -0.17 | 1.6719 | 0.9 | 0.7398 | 1.0 | équivalent |
| Sans cible_jour_6 | 3.235 | 3.95 | -0.211 | 1.6806 | 0.5 | 0.4349 | 1.0 | équivalent |
| Sans mois_sin | 3.293 | 4.026 | -0.098 | 1.676 | 0.6 | 0.9707 | 1.0 | équivalent |
| Sans mois_cos | 3.29 | 4.045 | 0.168 | 1.5946 | 0.6 | 0.0673 | 1.0 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Sans mois_cos** (1.5946). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)) après correction de Holm.



### D14 · Sélection des variables par le lasso

*Le modèle gagne-t-il à ne garder que les variables choisies par le lasso ? (modèle RBF du niveau 2)*

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | variables | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| Toutes les variables (retenu) | 3.233 | 3.939 | -0.193 | 1.6744 | 1.2 | 19.0 |  |  | — choix retenu |
| Lasso, λ de plus petite erreur | 3.394 | 4.204 | -0.003 | 1.6977 | 12.1 | 3.6 | 0.7314 | 0.7314 | équivalent |
| Lasso à un écart-type (λ_1se) | 3.347 | 4.124 | 0.206 | 1.6116 | 12.2 | 1.0 | 0.2575 | 0.515 | équivalent |


Plus petite perte pinball à τ = 0.8 : **Lasso à un écart-type (λ_1se)** (1.6116). Aucune variante ne bat significativement le choix retenu (Toutes les variables (retenu)) après correction de Holm.

