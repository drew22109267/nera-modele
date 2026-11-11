# Lien entre le triage et les lits — PED (comptage : journee)

Urgences, groupe enfant : 06/07/2025 → 31/12/2025, 111 jours transcrits. Probabilités : validation croisee.

## A · Corrélation entre les urgences au jour d et le service au jour d + k

Spearman ; intervalle à 95 % par bootstrap en blocs de 7 jours ; p-valeur par décalage circulaire.

| variante | signal des urgences (jour d) | service (jour d+k) | k (jours) | jours | spearman | IC95_bas | IC95_haut | p_valeur |
|---|---|---|---|---|---|---|---|---|
| 0 | passages enfants aux urgences | admissions | 0 | 111 | 0.001 | -0.204 | 0.155 | 0.9987 |
| 1 | passages enfants aux urgences | admissions | 1 | 111 | 0.145 | -0.079 | 0.287 | 0.2402 |
| 2 | passages enfants aux urgences | admissions | 2 | 111 | 0.241 | 0.025 | 0.397 | 0.0444 |
| 3 | passages enfants aux urgences | admissions | 3 | 111 | -0.0 | -0.225 | 0.206 | 1.0 |
| 4 | passages enfants aux urgences | presents | 0 | 111 | -0.097 | -0.302 | 0.047 | 0.4543 |
| 5 | passages enfants aux urgences | presents | 1 | 111 | 0.04 | -0.204 | 0.21 | 0.7742 |
| 6 | passages enfants aux urgences | presents | 2 | 111 | 0.189 | -0.07 | 0.361 | 0.1292 |
| 7 | passages enfants aux urgences | presents | 3 | 111 | 0.116 | -0.119 | 0.263 | 0.3499 |
| 8 | enfants graves orientés (décision observée) | admissions | 0 | 111 | 0.006 | -0.213 | 0.181 | 0.9465 |
| 9 | enfants graves orientés (décision observée) | admissions | 1 | 111 | 0.174 | -0.061 | 0.335 | 0.1436 |
| 10 | enfants graves orientés (décision observée) | admissions | 2 | 111 | 0.084 | -0.121 | 0.234 | 0.5 |
| 11 | enfants graves orientés (décision observée) | admissions | 3 | 111 | 0.053 | -0.131 | 0.211 | 0.6658 |
| 12 | enfants graves orientés (décision observée) | presents | 0 | 111 | -0.041 | -0.222 | 0.059 | 0.6984 |
| 13 | enfants graves orientés (décision observée) | presents | 1 | 111 | 0.076 | -0.18 | 0.244 | 0.4621 |
| 14 | enfants graves orientés (décision observée) | presents | 2 | 111 | 0.169 | -0.122 | 0.339 | 0.1136 |
| 15 | enfants graves orientés (décision observée) | presents | 3 | 111 | 0.178 | -0.028 | 0.32 | 0.0979 |
| 16 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 0 | 99 | -0.072 | -0.238 | 0.079 | 0.5666 |
| 17 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 1 | 99 | 0.096 | -0.1 | 0.262 | 0.453 |
| 18 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 2 | 99 | -0.075 | -0.289 | 0.199 | 0.5574 |
| 19 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 3 | 99 | 0.019 | -0.191 | 0.255 | 0.8825 |
| 20 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 0 | 99 | -0.133 | -0.261 | -0.0 | 0.2885 |
| 21 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 1 | 99 | -0.015 | -0.163 | 0.145 | 0.9034 |
| 22 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 2 | 99 | -0.054 | -0.285 | 0.178 | 0.6749 |
| 23 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 3 | 99 | -0.07 | -0.268 | 0.165 | 0.5757 |
| 24 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 0 | 99 | -0.073 | -0.24 | 0.046 | 0.5888 |
| 25 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 1 | 99 | 0.125 | -0.077 | 0.297 | 0.3525 |
| 26 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 2 | 99 | -0.002 | -0.214 | 0.217 | 0.9974 |
| 27 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 3 | 99 | 0.052 | -0.168 | 0.267 | 0.7102 |
| 28 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 0 | 99 | -0.16 | -0.343 | -0.019 | 0.1932 |
| 29 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 1 | 99 | -0.034 | -0.223 | 0.137 | 0.8055 |
| 30 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 2 | 99 | -0.016 | -0.258 | 0.178 | 0.8956 |
| 31 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 3 | 99 | -0.011 | -0.234 | 0.206 | 0.9151 |
| 32 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 0 | 99 | -0.133 | -0.322 | 0.01 | 0.3055 |
| 33 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 1 | 99 | 0.113 | -0.1 | 0.313 | 0.3747 |
| 34 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 2 | 99 | 0.121 | -0.062 | 0.319 | 0.3512 |
| 35 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 3 | 99 | 0.091 | -0.103 | 0.284 | 0.4896 |
| 36 | charge Σ P(grave), modèle transféré (source_seule) | presents | 0 | 99 | -0.109 | -0.295 | 0.022 | 0.3512 |
| 37 | charge Σ P(grave), modèle transféré (source_seule) | presents | 1 | 99 | -0.051 | -0.263 | 0.139 | 0.6906 |
| 38 | charge Σ P(grave), modèle transféré (source_seule) | presents | 2 | 99 | 0.021 | -0.236 | 0.233 | 0.8734 |
| 39 | charge Σ P(grave), modèle transféré (source_seule) | presents | 3 | 99 | 0.079 | -0.12 | 0.262 | 0.5117 |
| 40 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 0 | 99 | -0.129 | -0.29 | -0.012 | 0.3525 |
| 41 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 1 | 99 | 0.115 | -0.12 | 0.327 | 0.4164 |
| 42 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 2 | 99 | 0.129 | -0.068 | 0.337 | 0.3538 |
| 43 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 3 | 99 | 0.061 | -0.112 | 0.235 | 0.6697 |
| 44 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 0 | 99 | -0.163 | -0.336 | -0.031 | 0.1775 |
| 45 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 1 | 99 | -0.047 | -0.248 | 0.124 | 0.7258 |
| 46 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 2 | 99 | 0.056 | -0.179 | 0.241 | 0.6632 |
| 47 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 3 | 99 | 0.072 | -0.119 | 0.258 | 0.5862 |
| 48 | charge Σ P(grave), modèle transféré (reunies) | admissions | 0 | 99 | -0.035 | -0.248 | 0.089 | 0.7911 |
| 49 | charge Σ P(grave), modèle transféré (reunies) | admissions | 1 | 99 | 0.157 | -0.099 | 0.362 | 0.2193 |
| 50 | charge Σ P(grave), modèle transféré (reunies) | admissions | 2 | 99 | 0.039 | -0.178 | 0.245 | 0.7715 |
| 51 | charge Σ P(grave), modèle transféré (reunies) | admissions | 3 | 99 | 0.021 | -0.167 | 0.197 | 0.8773 |
| 52 | charge Σ P(grave), modèle transféré (reunies) | presents | 0 | 99 | -0.078 | -0.319 | 0.064 | 0.5209 |
| 53 | charge Σ P(grave), modèle transféré (reunies) | presents | 1 | 99 | 0.036 | -0.243 | 0.244 | 0.7715 |
| 54 | charge Σ P(grave), modèle transféré (reunies) | presents | 2 | 99 | 0.063 | -0.205 | 0.262 | 0.6044 |
| 55 | charge Σ P(grave), modèle transféré (reunies) | presents | 3 | 99 | 0.036 | -0.19 | 0.215 | 0.7663 |
| 56 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 0 | 99 | -0.063 | -0.251 | 0.059 | 0.6345 |
| 57 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 1 | 99 | 0.123 | -0.127 | 0.33 | 0.3368 |
| 58 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 2 | 99 | 0.061 | -0.151 | 0.281 | 0.6514 |
| 59 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 3 | 99 | 0.007 | -0.186 | 0.209 | 0.9726 |
| 60 | charge Σ P(grave), modèle transféré (augmentation) | presents | 0 | 99 | -0.106 | -0.32 | 0.038 | 0.4073 |
| 61 | charge Σ P(grave), modèle transféré (augmentation) | presents | 1 | 99 | 0.012 | -0.229 | 0.215 | 0.9191 |
| 62 | charge Σ P(grave), modèle transféré (augmentation) | presents | 2 | 99 | 0.061 | -0.192 | 0.267 | 0.624 |
| 63 | charge Σ P(grave), modèle transféré (augmentation) | presents | 3 | 99 | 0.009 | -0.193 | 0.202 | 0.9426 |
| 64 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 0 | 99 | -0.087 | -0.268 | 0.044 | 0.5352 |
| 65 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 1 | 99 | 0.144 | -0.065 | 0.338 | 0.2833 |
| 66 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 2 | 99 | 0.062 | -0.145 | 0.3 | 0.6645 |
| 67 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 3 | 99 | 0.06 | -0.138 | 0.25 | 0.6671 |
| 68 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 0 | 99 | -0.15 | -0.338 | -0.021 | 0.2128 |
| 69 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 1 | 99 | -0.026 | -0.23 | 0.161 | 0.8238 |
| 70 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 2 | 99 | 0.022 | -0.234 | 0.243 | 0.8577 |
| 71 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 3 | 99 | 0.034 | -0.162 | 0.237 | 0.7872 |
| 72 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 0 | 99 | -0.1 | -0.286 | 0.03 | 0.4713 |
| 73 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 1 | 99 | 0.097 | -0.117 | 0.279 | 0.4817 |
| 74 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 2 | 99 | 0.084 | -0.125 | 0.326 | 0.5535 |
| 75 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 3 | 99 | 0.064 | -0.135 | 0.26 | 0.6514 |
| 76 | charge Σ P(grave), modèle transféré (a_svm) | presents | 0 | 99 | -0.145 | -0.343 | -0.016 | 0.2206 |
| 77 | charge Σ P(grave), modèle transféré (a_svm) | presents | 1 | 99 | -0.038 | -0.246 | 0.137 | 0.7546 |
| 78 | charge Σ P(grave), modèle transféré (a_svm) | presents | 2 | 99 | 0.033 | -0.195 | 0.228 | 0.7898 |
| 79 | charge Σ P(grave), modèle transféré (a_svm) | presents | 3 | 99 | 0.062 | -0.14 | 0.279 | 0.6319 |
| 80 | charge Σ P(grave), modèle transféré (score_source) | admissions | 0 | 99 | -0.084 | -0.24 | 0.051 | 0.5483 |
| 81 | charge Σ P(grave), modèle transféré (score_source) | admissions | 1 | 99 | 0.13 | -0.077 | 0.322 | 0.3381 |
| 82 | charge Σ P(grave), modèle transféré (score_source) | admissions | 2 | 99 | 0.032 | -0.175 | 0.282 | 0.8211 |
| 83 | charge Σ P(grave), modèle transféré (score_source) | admissions | 3 | 99 | 0.036 | -0.159 | 0.243 | 0.7963 |
| 84 | charge Σ P(grave), modèle transféré (score_source) | presents | 0 | 99 | -0.164 | -0.336 | -0.019 | 0.2167 |
| 85 | charge Σ P(grave), modèle transféré (score_source) | presents | 1 | 99 | -0.031 | -0.206 | 0.149 | 0.8329 |
| 86 | charge Σ P(grave), modèle transféré (score_source) | presents | 2 | 99 | 0.003 | -0.237 | 0.228 | 0.9856 |
| 87 | charge Σ P(grave), modèle transféré (score_source) | presents | 3 | 99 | 0.003 | -0.191 | 0.226 | 0.9856 |


### Part des admissions passées par les urgences

| variante | jour | jours_transcrits | passages_enfants | graves_hors_meo | meo | admissions_service | part_admissions_par_urgences_% |
|---|---|---|---|---|---|---|---|
| 0 | 2025-07 | 1 | 4.0 | 2.0 | 0.0 | 0 | inf |
| 1 | 2025-09 | 23 | 106.0 | 24.0 | 5.0 | 59 | 40.7 |
| 2 | 2025-10 | 31 | 167.0 | 41.0 | 12.0 | 85 | 48.2 |
| 3 | 2025-11 | 29 | 124.0 | 37.0 | 13.0 | 74 | 50.0 |
| 4 | 2025-12 | 27 | 111.0 | 25.0 | 17.0 | 58 | 43.1 |



## B · Banc D12 : le triage améliore-t-il la prévision des lits ?


### Horizon J+1 (39 jours évalués, 9 origines)

| variante | variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | DM p (pinball τ=0.8) | p Holm | vs choix retenu | DM p vs charge locale | p Holm vs charge locale | vs charge locale (D12-3) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | D12-0 · sans les urgences (même fenêtre) (retenu) | 2.51 | 2.887 | 0.233 | 0.7854 | 87.2 |  |  | — choix retenu |  |  |  |
| 1 | D12-1 · + passages enfants aux urgences | 2.5 | 2.888 | 0.335 | 0.7883 | 79.5 | 0.9308 | 1.0 | équivalent |  |  |  |
| 2 | D12-2 · + enfants graves orientés (décision observée) | 2.508 | 2.888 | 0.248 | 0.7892 | 82.1 | 0.713 | 1.0 | équivalent |  |  |  |
| 3 | D12-3 · + charge grave attendue Σ P(grave) (module triage) | 2.483 | 2.854 | 0.228 | 0.7764 | 82.1 | 0.3295 | 1.0 | équivalent |  |  |  |
| 4 | D12-4 · + graves observés + charge | 2.467 | 2.844 | 0.185 | 0.794 | 82.1 | 0.8429 | 1.0 | équivalent |  |  |  |
| 5 | D12-T · + charge du modèle transféré (cible_fourier) | 2.485 | 2.856 | 0.219 | 0.7653 | 79.5 | 0.1055 | 1.0 | équivalent | 0.0266 | 0.2128 | équivalent |
| 6 | D12-T · + charge du modèle transféré (source_seule) | 2.473 | 2.867 | 0.291 | 0.7735 | 84.6 | 0.2573 | 1.0 | équivalent | 0.6003 | 1.0 | équivalent |
| 7 | D12-T · + charge du modèle transféré (source_recalibree) | 2.492 | 2.874 | 0.244 | 0.7611 | 74.4 | 0.4285 | 1.0 | équivalent | 0.5728 | 1.0 | équivalent |
| 8 | D12-T · + charge du modèle transféré (reunies) | 2.515 | 2.892 | 0.18 | 0.7837 | 79.5 | 0.892 | 1.0 | équivalent | 0.2198 | 1.0 | équivalent |
| 9 | D12-T · + charge du modèle transféré (augmentation) | 2.513 | 2.886 | 0.176 | 0.7786 | 76.9 | 0.6141 | 1.0 | équivalent | 0.7741 | 1.0 | équivalent |
| 10 | D12-T · + charge du modèle transféré (regularisation_biaisee) | 2.482 | 2.867 | 0.293 | 0.7724 | 76.9 | 0.3126 | 1.0 | équivalent | 0.435 | 1.0 | équivalent |
| 11 | D12-T · + charge du modèle transféré (a_svm) | 2.482 | 2.871 | 0.322 | 0.7675 | 82.1 | 0.4623 | 1.0 | équivalent | 0.6634 | 1.0 | équivalent |
| 12 | D12-T · + charge du modèle transféré (score_source) | 2.472 | 2.851 | 0.274 | 0.7751 | 76.9 | 0.4108 | 1.0 | équivalent | 0.8027 | 1.0 | équivalent |
| 13 | modèle habituel, tout l'historique de la pédiatrie (sans urgences) | 1.784 | 2.171 | 0.373 | 0.6252 | 97.4 | 0.1477 | 1.0 | équivalent |  |  |  |
| 14 | persistance | 2.256 | 2.864 | -0.103 | 1.159 |  | 0.0884 | 1.0 | équivalent |  |  |  |


Plus petite perte pinball à τ = 0.8 : **modèle habituel, tout l'historique de la pédiatrie (sans urgences)** (0.6252). Aucune variante ne bat significativement le choix retenu (D12-0 · sans les urgences (même fenêtre) (retenu)) après correction de Holm.



### Horizon J+7 (33 jours évalués, 8 origines)

| variante | variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | DM p (pinball τ=0.8) | p Holm | vs choix retenu | DM p vs charge locale | p Holm vs charge locale | vs charge locale (D12-3) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | D12-0 · sans les urgences (même fenêtre) (retenu) | 3.552 | 4.264 | 1.485 | 1.0482 | 81.8 |  |  | — choix retenu |  |  |  |
| 1 | D12-1 · + passages enfants aux urgences | 3.325 | 3.952 | 1.187 | 1.041 | 78.8 | 0.9324 | 1.0 | équivalent |  |  |  |
| 2 | D12-2 · + enfants graves orientés (décision observée) | 3.427 | 4.048 | 1.287 | 1.0947 | 81.8 | 0.041 | 0.574 | équivalent |  |  |  |
| 3 | D12-3 · + charge grave attendue Σ P(grave) (module triage) | 3.331 | 3.958 | 1.042 | 1.0608 | 78.8 | 0.8207 | 1.0 | équivalent |  |  |  |
| 4 | D12-4 · + graves observés + charge | 3.291 | 3.871 | 0.938 | 1.1018 | 81.8 | 0.3939 | 1.0 | équivalent |  |  |  |
| 5 | D12-T · + charge du modèle transféré (cible_fourier) | 3.289 | 3.947 | 1.117 | 1.07 | 78.8 | 0.5863 | 1.0 | équivalent | 0.5378 | 1.0 | équivalent |
| 6 | D12-T · + charge du modèle transféré (source_seule) | 3.327 | 4.004 | 1.172 | 1.0289 | 81.8 | 0.4961 | 1.0 | équivalent | 0.3425 | 1.0 | équivalent |
| 7 | D12-T · + charge du modèle transféré (source_recalibree) | 3.334 | 4.02 | 1.292 | 1.0166 | 81.8 | 0.4496 | 1.0 | équivalent | 0.0044 | 0.0352 | meilleur |
| 8 | D12-T · + charge du modèle transféré (reunies) | 3.359 | 4.019 | 1.242 | 1.0532 | 81.8 | 0.9009 | 1.0 | équivalent | 0.7081 | 1.0 | équivalent |
| 9 | D12-T · + charge du modèle transféré (augmentation) | 3.419 | 4.08 | 1.256 | 1.0529 | 78.8 | 0.8311 | 1.0 | équivalent | 0.8085 | 1.0 | équivalent |
| 10 | D12-T · + charge du modèle transféré (regularisation_biaisee) | 3.32 | 3.972 | 1.145 | 1.0465 | 81.8 | 0.9581 | 1.0 | équivalent | 0.2925 | 1.0 | équivalent |
| 11 | D12-T · + charge du modèle transféré (a_svm) | 3.301 | 3.966 | 1.164 | 1.0397 | 81.8 | 0.8825 | 1.0 | équivalent | 0.0814 | 0.5698 | équivalent |
| 12 | D12-T · + charge du modèle transféré (score_source) | 3.311 | 3.949 | 1.058 | 1.0502 | 78.8 | 0.9502 | 1.0 | équivalent | 0.6429 | 1.0 | équivalent |
| 13 | modèle habituel, tout l'historique de la pédiatrie (sans urgences) | 3.873 | 4.836 | 3.089 | 1.3349 | 87.9 | 0.3545 | 1.0 | équivalent |  |  |  |
| 14 | persistance | 3.336 | 4.192 | 0.73 | 1.449 |  | 0.3031 | 1.0 | équivalent |  |  |  |


Plus petite perte pinball à τ = 0.8 : **D12-T · + charge du modèle transféré (source_recalibree)** (1.0166). Aucune variante ne bat significativement le choix retenu (D12-0 · sans les urgences (même fenêtre) (retenu)) après correction de Holm.

