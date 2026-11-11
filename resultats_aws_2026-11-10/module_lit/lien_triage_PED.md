# Lien entre le triage et les lits — PED (comptage : minuit)

Urgences, groupe enfant : 06/07/2025 → 31/12/2025, 111 jours transcrits. Probabilités : validation croisee.

## A · Corrélation entre les urgences au jour d et le service au jour d + k

Spearman ; intervalle à 95 % par bootstrap en blocs de 7 jours ; p-valeur par décalage circulaire.

| variante | signal des urgences (jour d) | service (jour d+k) | k (jours) | jours | spearman | IC95_bas | IC95_haut | p_valeur |
|---|---|---|---|---|---|---|---|---|
| 0 | passages enfants aux urgences | admissions | 0 | 111 | 0.001 | -0.204 | 0.155 | 0.9987 |
| 1 | passages enfants aux urgences | admissions | 1 | 111 | 0.145 | -0.079 | 0.287 | 0.2402 |
| 2 | passages enfants aux urgences | admissions | 2 | 111 | 0.241 | 0.025 | 0.397 | 0.0444 |
| 3 | passages enfants aux urgences | admissions | 3 | 111 | -0.0 | -0.225 | 0.206 | 1.0 |
| 4 | passages enfants aux urgences | presents | 0 | 111 | -0.013 | -0.214 | 0.139 | 0.9099 |
| 5 | passages enfants aux urgences | presents | 1 | 111 | 0.094 | -0.127 | 0.228 | 0.4256 |
| 6 | passages enfants aux urgences | presents | 2 | 111 | 0.143 | -0.122 | 0.317 | 0.2245 |
| 7 | passages enfants aux urgences | presents | 3 | 111 | 0.108 | -0.139 | 0.29 | 0.3734 |
| 8 | enfants graves orientés (décision observée) | admissions | 0 | 111 | 0.006 | -0.213 | 0.181 | 0.9465 |
| 9 | enfants graves orientés (décision observée) | admissions | 1 | 111 | 0.174 | -0.061 | 0.335 | 0.1436 |
| 10 | enfants graves orientés (décision observée) | admissions | 2 | 111 | 0.084 | -0.121 | 0.234 | 0.5 |
| 11 | enfants graves orientés (décision observée) | admissions | 3 | 111 | 0.053 | -0.131 | 0.211 | 0.6658 |
| 12 | enfants graves orientés (décision observée) | presents | 0 | 111 | 0.003 | -0.2 | 0.129 | 0.9687 |
| 13 | enfants graves orientés (décision observée) | presents | 1 | 111 | 0.18 | -0.091 | 0.335 | 0.0705 |
| 14 | enfants graves orientés (décision observée) | presents | 2 | 111 | 0.188 | -0.049 | 0.328 | 0.0601 |
| 15 | enfants graves orientés (décision observée) | presents | 3 | 111 | 0.207 | 0.003 | 0.371 | 0.0444 |
| 16 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 0 | 99 | -0.072 | -0.238 | 0.079 | 0.5666 |
| 17 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 1 | 99 | 0.096 | -0.1 | 0.262 | 0.453 |
| 18 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 2 | 99 | -0.075 | -0.289 | 0.199 | 0.5574 |
| 19 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 3 | 99 | 0.019 | -0.191 | 0.255 | 0.8825 |
| 20 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 0 | 99 | -0.051 | -0.185 | 0.087 | 0.6462 |
| 21 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 1 | 99 | 0.022 | -0.174 | 0.224 | 0.8394 |
| 22 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 2 | 99 | -0.073 | -0.274 | 0.127 | 0.5366 |
| 23 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 3 | 99 | 0.011 | -0.207 | 0.285 | 0.9243 |
| 24 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 0 | 99 | -0.073 | -0.24 | 0.046 | 0.5888 |
| 25 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 1 | 99 | 0.125 | -0.077 | 0.297 | 0.3525 |
| 26 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 2 | 99 | -0.002 | -0.214 | 0.217 | 0.9974 |
| 27 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 3 | 99 | 0.052 | -0.168 | 0.267 | 0.7102 |
| 28 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 0 | 99 | -0.083 | -0.264 | 0.063 | 0.4817 |
| 29 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 1 | 99 | 0.029 | -0.174 | 0.19 | 0.8172 |
| 30 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 2 | 99 | -0.02 | -0.241 | 0.164 | 0.8877 |
| 31 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 3 | 99 | 0.064 | -0.176 | 0.33 | 0.5783 |
| 32 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 0 | 99 | -0.133 | -0.322 | 0.01 | 0.3055 |
| 33 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 1 | 99 | 0.113 | -0.1 | 0.313 | 0.3747 |
| 34 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 2 | 99 | 0.121 | -0.062 | 0.319 | 0.3512 |
| 35 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 3 | 99 | 0.091 | -0.103 | 0.284 | 0.4896 |
| 36 | charge Σ P(grave), modèle transféré (source_seule) | presents | 0 | 99 | -0.07 | -0.261 | 0.07 | 0.5078 |
| 37 | charge Σ P(grave), modèle transféré (source_seule) | presents | 1 | 99 | -0.025 | -0.226 | 0.15 | 0.8094 |
| 38 | charge Σ P(grave), modèle transféré (source_seule) | presents | 2 | 99 | 0.078 | -0.134 | 0.259 | 0.4739 |
| 39 | charge Σ P(grave), modèle transféré (source_seule) | presents | 3 | 99 | 0.174 | -0.037 | 0.393 | 0.1084 |
| 40 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 0 | 99 | -0.129 | -0.29 | -0.012 | 0.3525 |
| 41 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 1 | 99 | 0.115 | -0.12 | 0.327 | 0.4164 |
| 42 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 2 | 99 | 0.129 | -0.068 | 0.337 | 0.3538 |
| 43 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 3 | 99 | 0.061 | -0.112 | 0.235 | 0.6697 |
| 44 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 0 | 99 | -0.072 | -0.251 | 0.062 | 0.5117 |
| 45 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 1 | 99 | 0.007 | -0.166 | 0.157 | 0.9569 |
| 46 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 2 | 99 | 0.09 | -0.112 | 0.253 | 0.4178 |
| 47 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 3 | 99 | 0.13 | -0.095 | 0.374 | 0.2389 |
| 48 | charge Σ P(grave), modèle transféré (reunies) | admissions | 0 | 99 | -0.035 | -0.248 | 0.089 | 0.7911 |
| 49 | charge Σ P(grave), modèle transféré (reunies) | admissions | 1 | 99 | 0.157 | -0.099 | 0.362 | 0.2193 |
| 50 | charge Σ P(grave), modèle transféré (reunies) | admissions | 2 | 99 | 0.039 | -0.178 | 0.245 | 0.7715 |
| 51 | charge Σ P(grave), modèle transféré (reunies) | admissions | 3 | 99 | 0.021 | -0.167 | 0.197 | 0.8773 |
| 52 | charge Σ P(grave), modèle transféré (reunies) | presents | 0 | 99 | -0.007 | -0.26 | 0.162 | 0.9595 |
| 53 | charge Σ P(grave), modèle transféré (reunies) | presents | 1 | 99 | 0.091 | -0.156 | 0.259 | 0.406 |
| 54 | charge Σ P(grave), modèle transféré (reunies) | presents | 2 | 99 | 0.065 | -0.179 | 0.238 | 0.5653 |
| 55 | charge Σ P(grave), modèle transféré (reunies) | presents | 3 | 99 | 0.09 | -0.146 | 0.319 | 0.4099 |
| 56 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 0 | 99 | -0.063 | -0.251 | 0.059 | 0.6345 |
| 57 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 1 | 99 | 0.123 | -0.127 | 0.33 | 0.3368 |
| 58 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 2 | 99 | 0.061 | -0.151 | 0.281 | 0.6514 |
| 59 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 3 | 99 | 0.007 | -0.186 | 0.209 | 0.9726 |
| 60 | charge Σ P(grave), modèle transféré (augmentation) | presents | 0 | 99 | -0.017 | -0.234 | 0.149 | 0.8903 |
| 61 | charge Σ P(grave), modèle transféré (augmentation) | presents | 1 | 99 | 0.077 | -0.14 | 0.241 | 0.5157 |
| 62 | charge Σ P(grave), modèle transféré (augmentation) | presents | 2 | 99 | 0.043 | -0.196 | 0.23 | 0.7311 |
| 63 | charge Σ P(grave), modèle transféré (augmentation) | presents | 3 | 99 | 0.069 | -0.159 | 0.321 | 0.5666 |
| 64 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 0 | 99 | -0.087 | -0.268 | 0.044 | 0.5352 |
| 65 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 1 | 99 | 0.144 | -0.065 | 0.338 | 0.2833 |
| 66 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 2 | 99 | 0.062 | -0.145 | 0.3 | 0.6645 |
| 67 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 3 | 99 | 0.06 | -0.138 | 0.25 | 0.6671 |
| 68 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 0 | 99 | -0.072 | -0.257 | 0.073 | 0.5117 |
| 69 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 1 | 99 | 0.022 | -0.177 | 0.194 | 0.8538 |
| 70 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 2 | 99 | 0.036 | -0.185 | 0.238 | 0.7507 |
| 71 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 3 | 99 | 0.114 | -0.112 | 0.367 | 0.3042 |
| 72 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 0 | 99 | -0.1 | -0.286 | 0.03 | 0.4713 |
| 73 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 1 | 99 | 0.097 | -0.117 | 0.279 | 0.4817 |
| 74 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 2 | 99 | 0.084 | -0.125 | 0.326 | 0.5535 |
| 75 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 3 | 99 | 0.064 | -0.135 | 0.26 | 0.6514 |
| 76 | charge Σ P(grave), modèle transféré (a_svm) | presents | 0 | 99 | -0.065 | -0.249 | 0.071 | 0.5509 |
| 77 | charge Σ P(grave), modèle transféré (a_svm) | presents | 1 | 99 | 0.012 | -0.194 | 0.183 | 0.9086 |
| 78 | charge Σ P(grave), modèle transféré (a_svm) | presents | 2 | 99 | 0.058 | -0.148 | 0.241 | 0.5809 |
| 79 | charge Σ P(grave), modèle transféré (a_svm) | presents | 3 | 99 | 0.128 | -0.1 | 0.387 | 0.2337 |
| 80 | charge Σ P(grave), modèle transféré (score_source) | admissions | 0 | 99 | -0.084 | -0.24 | 0.051 | 0.5483 |
| 81 | charge Σ P(grave), modèle transféré (score_source) | admissions | 1 | 99 | 0.13 | -0.077 | 0.322 | 0.3381 |
| 82 | charge Σ P(grave), modèle transféré (score_source) | admissions | 2 | 99 | 0.032 | -0.175 | 0.282 | 0.8211 |
| 83 | charge Σ P(grave), modèle transféré (score_source) | admissions | 3 | 99 | 0.036 | -0.159 | 0.243 | 0.7963 |
| 84 | charge Σ P(grave), modèle transféré (score_source) | presents | 0 | 99 | -0.077 | -0.252 | 0.074 | 0.5418 |
| 85 | charge Σ P(grave), modèle transféré (score_source) | presents | 1 | 99 | 0.028 | -0.162 | 0.199 | 0.8159 |
| 86 | charge Σ P(grave), modèle transféré (score_source) | presents | 2 | 99 | 0.009 | -0.21 | 0.215 | 0.9439 |
| 87 | charge Σ P(grave), modèle transféré (score_source) | presents | 3 | 99 | 0.096 | -0.123 | 0.371 | 0.4334 |


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
| 0 | D12-0 · sans les urgences (même fenêtre) (retenu) | 2.33 | 2.943 | -0.025 | 0.7773 | 82.1 |  |  | — choix retenu |  |  |  |
| 1 | D12-1 · + passages enfants aux urgences | 2.302 | 2.913 | 0.012 | 0.7715 | 82.1 | 0.643 | 1.0 | équivalent |  |  |  |
| 2 | D12-2 · + enfants graves orientés (décision observée) | 2.269 | 2.843 | 0.021 | 0.7815 | 82.1 | 0.8077 | 1.0 | équivalent |  |  |  |
| 3 | D12-3 · + charge grave attendue Σ P(grave) (module triage) | 2.315 | 2.944 | 0.092 | 0.7806 | 82.1 | 0.8612 | 1.0 | équivalent |  |  |  |
| 4 | D12-4 · + graves observés + charge | 2.262 | 2.838 | -0.01 | 0.7961 | 82.1 | 0.4204 | 1.0 | équivalent |  |  |  |
| 5 | D12-T · + charge du modèle transféré (cible_fourier) | 2.301 | 2.903 | 0.043 | 0.7834 | 82.1 | 0.7224 | 1.0 | équivalent | 0.6366 | 1.0 | équivalent |
| 6 | D12-T · + charge du modèle transféré (source_seule) | 2.338 | 2.951 | 0.005 | 0.7749 | 82.1 | 0.8973 | 1.0 | équivalent | 0.6379 | 1.0 | équivalent |
| 7 | D12-T · + charge du modèle transféré (source_recalibree) | 2.286 | 2.89 | 0.059 | 0.7536 | 82.1 | 0.1572 | 1.0 | équivalent | 0.0166 | 0.1022 | équivalent |
| 8 | D12-T · + charge du modèle transféré (reunies) | 2.302 | 2.896 | -0.051 | 0.787 | 82.1 | 0.577 | 1.0 | équivalent | 0.3336 | 1.0 | équivalent |
| 9 | D12-T · + charge du modèle transféré (augmentation) | 2.308 | 2.9 | -0.042 | 0.7952 | 82.1 | 0.3718 | 1.0 | équivalent | 0.0038 | 0.0304 | moins bon |
| 10 | D12-T · + charge du modèle transféré (regularisation_biaisee) | 2.332 | 2.948 | 0.142 | 0.7795 | 82.1 | 0.8918 | 1.0 | équivalent | 0.8564 | 1.0 | équivalent |
| 11 | D12-T · + charge du modèle transféré (a_svm) | 2.269 | 2.873 | 0.14 | 0.7538 | 82.1 | 0.1461 | 1.0 | équivalent | 0.0146 | 0.1022 | équivalent |
| 12 | D12-T · + charge du modèle transféré (score_source) | 2.323 | 2.947 | 0.144 | 0.7837 | 82.1 | 0.7106 | 1.0 | équivalent | 0.4616 | 1.0 | équivalent |
| 13 | modèle habituel, tout l'historique de la pédiatrie (sans urgences) | 1.995 | 2.473 | 0.187 | 0.6318 | 92.3 | 0.2129 | 1.0 | équivalent |  |  |  |
| 14 | persistance | 2.254 | 2.677 | -0.203 | 1.188 |  | 0.0268 | 0.3752 | équivalent |  |  |  |


Plus petite perte pinball à τ = 0.8 : **modèle habituel, tout l'historique de la pédiatrie (sans urgences)** (0.6318). Aucune variante ne bat significativement le choix retenu (D12-0 · sans les urgences (même fenêtre) (retenu)) après correction de Holm.



### Horizon J+7 (33 jours évalués, 8 origines)

| variante | variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | DM p (pinball τ=0.8) | p Holm | vs choix retenu | DM p vs charge locale | p Holm vs charge locale | vs charge locale (D12-3) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | D12-0 · sans les urgences (même fenêtre) (retenu) | 2.897 | 3.417 | 0.485 | 0.9836 | 90.9 |  |  | — choix retenu |  |  |  |
| 1 | D12-1 · + passages enfants aux urgences | 2.862 | 3.371 | 0.365 | 0.9886 | 90.9 | 0.7573 | 1.0 | équivalent |  |  |  |
| 2 | D12-2 · + enfants graves orientés (décision observée) | 2.862 | 3.37 | 0.346 | 0.987 | 90.9 | 0.8568 | 1.0 | équivalent |  |  |  |
| 3 | D12-3 · + charge grave attendue Σ P(grave) (module triage) | 2.85 | 3.359 | 0.348 | 0.9857 | 90.9 | 0.8966 | 1.0 | équivalent |  |  |  |
| 4 | D12-4 · + graves observés + charge | 2.84 | 3.345 | 0.286 | 0.9887 | 90.9 | 0.841 | 1.0 | équivalent |  |  |  |
| 5 | D12-T · + charge du modèle transféré (cible_fourier) | 2.851 | 3.36 | 0.349 | 0.9851 | 90.9 | 0.9279 | 1.0 | équivalent | 0.0906 | 0.6342 | équivalent |
| 6 | D12-T · + charge du modèle transféré (source_seule) | 2.859 | 3.371 | 0.383 | 0.9876 | 90.9 | 0.8423 | 1.0 | équivalent | 0.6043 | 1.0 | équivalent |
| 7 | D12-T · + charge du modèle transféré (source_recalibree) | 2.858 | 3.368 | 0.381 | 0.9886 | 90.9 | 0.8224 | 1.0 | équivalent | 0.62 | 1.0 | équivalent |
| 8 | D12-T · + charge du modèle transféré (reunies) | 2.853 | 3.363 | 0.367 | 0.9877 | 90.9 | 0.8432 | 1.0 | équivalent | 0.6471 | 1.0 | équivalent |
| 9 | D12-T · + charge du modèle transféré (augmentation) | 2.858 | 3.366 | 0.368 | 0.986 | 90.9 | 0.9007 | 1.0 | équivalent | 0.9276 | 1.0 | équivalent |
| 10 | D12-T · + charge du modèle transféré (regularisation_biaisee) | 2.855 | 3.365 | 0.365 | 0.9848 | 90.9 | 0.9414 | 1.0 | équivalent |  |  | identique |
| 11 | D12-T · + charge du modèle transféré (a_svm) | 2.851 | 3.361 | 0.35 | 0.9874 | 90.9 | 0.8449 | 1.0 | équivalent | 0.5363 | 1.0 | équivalent |
| 12 | D12-T · + charge du modèle transféré (score_source) | 2.854 | 3.363 | 0.355 | 0.9828 | 90.9 | 0.9562 | 1.0 | équivalent | 0.2476 | 1.0 | équivalent |
| 13 | modèle habituel, tout l'historique de la pédiatrie (sans urgences) | 3.081 | 3.663 | 1.453 | 0.9601 | 93.9 | 0.7557 | 1.0 | équivalent |  |  |  |
| 14 | persistance | 2.639 | 3.606 | 0.578 | 1.146 |  | 0.4831 | 1.0 | équivalent |  |  |  |


Plus petite perte pinball à τ = 0.8 : **modèle habituel, tout l'historique de la pédiatrie (sans urgences)** (0.9601). Aucune variante ne bat significativement le choix retenu (D12-0 · sans les urgences (même fenêtre) (retenu)) après correction de Holm.

