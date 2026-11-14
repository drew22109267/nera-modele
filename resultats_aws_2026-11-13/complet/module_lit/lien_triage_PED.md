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
| 16 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 0 | 99 | -0.072 | -0.24 | 0.077 | 0.5927 |
| 17 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 1 | 99 | 0.117 | -0.081 | 0.294 | 0.3681 |
| 18 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 2 | 99 | -0.039 | -0.258 | 0.231 | 0.7755 |
| 19 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 3 | 99 | 0.033 | -0.172 | 0.262 | 0.8185 |
| 20 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 0 | 99 | -0.065 | -0.196 | 0.064 | 0.5705 |
| 21 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 1 | 99 | 0.025 | -0.172 | 0.227 | 0.8264 |
| 22 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 2 | 99 | -0.044 | -0.232 | 0.159 | 0.7023 |
| 23 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 3 | 99 | 0.033 | -0.18 | 0.31 | 0.7598 |
| 24 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 0 | 99 | -0.079 | -0.249 | 0.043 | 0.5718 |
| 25 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 1 | 99 | 0.121 | -0.072 | 0.293 | 0.3616 |
| 26 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 2 | 99 | 0.023 | -0.194 | 0.237 | 0.8943 |
| 27 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 3 | 99 | 0.055 | -0.164 | 0.263 | 0.7076 |
| 28 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 0 | 99 | -0.088 | -0.262 | 0.056 | 0.4413 |
| 29 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 1 | 99 | 0.021 | -0.176 | 0.177 | 0.8642 |
| 30 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 2 | 99 | -0.011 | -0.226 | 0.172 | 0.9282 |
| 31 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 3 | 99 | 0.074 | -0.161 | 0.334 | 0.5144 |
| 32 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 0 | 99 | -0.119 | -0.303 | 0.016 | 0.376 |
| 33 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 1 | 99 | 0.119 | -0.104 | 0.312 | 0.3721 |
| 34 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 2 | 99 | 0.135 | -0.067 | 0.335 | 0.3068 |
| 35 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 3 | 99 | 0.081 | -0.108 | 0.266 | 0.5587 |
| 36 | charge Σ P(grave), modèle transféré (source_seule) | presents | 0 | 99 | -0.058 | -0.241 | 0.083 | 0.5783 |
| 37 | charge Σ P(grave), modèle transféré (source_seule) | presents | 1 | 99 | 0.001 | -0.193 | 0.166 | 0.9948 |
| 38 | charge Σ P(grave), modèle transféré (source_seule) | presents | 2 | 99 | 0.083 | -0.145 | 0.259 | 0.4491 |
| 39 | charge Σ P(grave), modèle transféré (source_seule) | presents | 3 | 99 | 0.163 | -0.051 | 0.396 | 0.1345 |
| 40 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 0 | 99 | -0.129 | -0.291 | -0.013 | 0.3473 |
| 41 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 1 | 99 | 0.115 | -0.12 | 0.327 | 0.4138 |
| 42 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 2 | 99 | 0.128 | -0.068 | 0.337 | 0.3564 |
| 43 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 3 | 99 | 0.061 | -0.112 | 0.235 | 0.6671 |
| 44 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 0 | 99 | -0.073 | -0.252 | 0.061 | 0.5078 |
| 45 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 1 | 99 | 0.006 | -0.167 | 0.156 | 0.9634 |
| 46 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 2 | 99 | 0.089 | -0.114 | 0.253 | 0.4256 |
| 47 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 3 | 99 | 0.13 | -0.092 | 0.374 | 0.2376 |
| 48 | charge Σ P(grave), modèle transféré (reunies) | admissions | 0 | 99 | -0.045 | -0.254 | 0.08 | 0.7428 |
| 49 | charge Σ P(grave), modèle transféré (reunies) | admissions | 1 | 99 | 0.16 | -0.095 | 0.361 | 0.201 |
| 50 | charge Σ P(grave), modèle transféré (reunies) | admissions | 2 | 99 | 0.031 | -0.184 | 0.242 | 0.812 |
| 51 | charge Σ P(grave), modèle transféré (reunies) | admissions | 3 | 99 | 0.014 | -0.178 | 0.197 | 0.9178 |
| 52 | charge Σ P(grave), modèle transféré (reunies) | presents | 0 | 99 | -0.014 | -0.264 | 0.153 | 0.9138 |
| 53 | charge Σ P(grave), modèle transféré (reunies) | presents | 1 | 99 | 0.08 | -0.164 | 0.251 | 0.4843 |
| 54 | charge Σ P(grave), modèle transféré (reunies) | presents | 2 | 99 | 0.057 | -0.187 | 0.237 | 0.6149 |
| 55 | charge Σ P(grave), modèle transféré (reunies) | presents | 3 | 99 | 0.085 | -0.152 | 0.319 | 0.4504 |
| 56 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 0 | 99 | -0.071 | -0.256 | 0.05 | 0.611 |
| 57 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 1 | 99 | 0.133 | -0.12 | 0.338 | 0.3029 |
| 58 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 2 | 99 | 0.047 | -0.163 | 0.268 | 0.7272 |
| 59 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 3 | 99 | -0.001 | -0.196 | 0.207 | 0.9961 |
| 60 | charge Σ P(grave), modèle transféré (augmentation) | presents | 0 | 99 | -0.031 | -0.244 | 0.132 | 0.8068 |
| 61 | charge Σ P(grave), modèle transféré (augmentation) | presents | 1 | 99 | 0.068 | -0.142 | 0.229 | 0.5888 |
| 62 | charge Σ P(grave), modèle transféré (augmentation) | presents | 2 | 99 | 0.031 | -0.201 | 0.217 | 0.8016 |
| 63 | charge Σ P(grave), modèle transféré (augmentation) | presents | 3 | 99 | 0.057 | -0.168 | 0.315 | 0.6436 |
| 64 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 0 | 99 | -0.1 | -0.284 | 0.035 | 0.4687 |
| 65 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 1 | 99 | 0.141 | -0.074 | 0.334 | 0.2911 |
| 66 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 2 | 99 | 0.063 | -0.142 | 0.299 | 0.6501 |
| 67 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 3 | 99 | 0.063 | -0.137 | 0.255 | 0.6488 |
| 68 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 0 | 99 | -0.078 | -0.262 | 0.064 | 0.4869 |
| 69 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 1 | 99 | 0.014 | -0.189 | 0.182 | 0.9164 |
| 70 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 2 | 99 | 0.03 | -0.194 | 0.233 | 0.8042 |
| 71 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 3 | 99 | 0.119 | -0.1 | 0.363 | 0.2859 |
| 72 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 0 | 99 | -0.093 | -0.278 | 0.038 | 0.5039 |
| 73 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 1 | 99 | 0.108 | -0.117 | 0.294 | 0.4452 |
| 74 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 2 | 99 | 0.08 | -0.124 | 0.315 | 0.5862 |
| 75 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 3 | 99 | 0.057 | -0.138 | 0.257 | 0.6984 |
| 76 | charge Σ P(grave), modèle transféré (a_svm) | presents | 0 | 99 | -0.054 | -0.227 | 0.075 | 0.6162 |
| 77 | charge Σ P(grave), modèle transféré (a_svm) | presents | 1 | 99 | 0.018 | -0.187 | 0.192 | 0.8603 |
| 78 | charge Σ P(grave), modèle transféré (a_svm) | presents | 2 | 99 | 0.051 | -0.16 | 0.239 | 0.6279 |
| 79 | charge Σ P(grave), modèle transféré (a_svm) | presents | 3 | 99 | 0.123 | -0.097 | 0.379 | 0.2507 |
| 80 | charge Σ P(grave), modèle transféré (score_source) | admissions | 0 | 99 | -0.096 | -0.266 | 0.033 | 0.4869 |
| 81 | charge Σ P(grave), modèle transféré (score_source) | admissions | 1 | 99 | 0.134 | -0.078 | 0.334 | 0.3172 |
| 82 | charge Σ P(grave), modèle transféré (score_source) | admissions | 2 | 99 | 0.056 | -0.144 | 0.298 | 0.705 |
| 83 | charge Σ P(grave), modèle transféré (score_source) | admissions | 3 | 99 | 0.043 | -0.15 | 0.248 | 0.7559 |
| 84 | charge Σ P(grave), modèle transféré (score_source) | presents | 0 | 99 | -0.074 | -0.244 | 0.068 | 0.5274 |
| 85 | charge Σ P(grave), modèle transféré (score_source) | presents | 1 | 99 | 0.026 | -0.174 | 0.198 | 0.8225 |
| 86 | charge Σ P(grave), modèle transféré (score_source) | presents | 2 | 99 | 0.026 | -0.189 | 0.234 | 0.8238 |
| 87 | charge Σ P(grave), modèle transféré (score_source) | presents | 3 | 99 | 0.124 | -0.092 | 0.395 | 0.295 |


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

| variante | variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu | DM p (pinball τ=0.8) vs charge locale | p Holm vs charge locale | vs charge locale (D12-3) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | D12-0 · sans les urgences (même fenêtre) (retenu) | 2.33 | 2.943 | -0.025 | 0.7773 | 82.1 |  |  |  | — choix retenu |  |  |  |
| 1 | D12-1 · + passages enfants aux urgences | 2.302 | 2.913 | 0.012 | 0.7715 | 82.1 | 0.643 | 1.0 | 0.7306 | équivalent |  |  |  |
| 2 | D12-2 · + enfants graves orientés (décision observée) | 2.269 | 2.843 | 0.021 | 0.7815 | 82.1 | 0.8077 | 1.0 | 0.484 | équivalent |  |  |  |
| 3 | D12-3 · + charge grave attendue Σ P(grave) (module triage) | 2.316 | 2.944 | 0.116 | 0.7814 | 82.1 | 0.8338 | 1.0 | 0.8702 | équivalent |  |  |  |
| 4 | D12-4 · + graves observés + charge | 2.264 | 2.841 | 0.001 | 0.7948 | 82.1 | 0.4599 | 1.0 | 0.4957 | équivalent |  |  |  |
| 5 | D12-T · + charge du modèle transféré (cible_fourier) | 2.3 | 2.898 | 0.052 | 0.7784 | 82.1 | 0.9431 | 1.0 | 0.7366 | équivalent | 0.7288 | 1.0 | équivalent |
| 6 | D12-T · + charge du modèle transféré (source_seule) | 2.334 | 2.949 | 0.018 | 0.7721 | 82.1 | 0.7798 | 1.0 | 0.9582 | équivalent | 0.3954 | 1.0 | équivalent |
| 7 | D12-T · + charge du modèle transféré (source_recalibree) | 2.285 | 2.89 | 0.059 | 0.7543 | 82.1 | 0.1719 | 1.0 | 0.5982 | équivalent | 0.0248 | 0.1488 | équivalent |
| 8 | D12-T · + charge du modèle transféré (reunies) | 2.299 | 2.891 | -0.056 | 0.7866 | 82.1 | 0.5955 | 1.0 | 0.6904 | équivalent | 0.4309 | 1.0 | équivalent |
| 9 | D12-T · + charge du modèle transféré (augmentation) | 2.304 | 2.895 | -0.046 | 0.7938 | 82.1 | 0.4125 | 1.0 | 0.7654 | équivalent | 0.0184 | 0.144 | équivalent |
| 10 | D12-T · + charge du modèle transféré (regularisation_biaisee) | 2.327 | 2.935 | 0.137 | 0.7787 | 82.1 | 0.9309 | 1.0 | 0.9736 | équivalent | 0.6691 | 1.0 | équivalent |
| 11 | D12-T · + charge du modèle transféré (a_svm) | 2.275 | 2.893 | 0.142 | 0.7574 | 82.1 | 0.235 | 1.0 | 0.5461 | équivalent | 0.018 | 0.144 | équivalent |
| 12 | D12-T · + charge du modèle transféré (score_source) | 2.32 | 2.935 | 0.154 | 0.7818 | 82.1 | 0.7986 | 1.0 | 0.9152 | équivalent | 0.934 | 1.0 | équivalent |
| 13 | modèle habituel, tout l'historique de la pédiatrie (sans urgences) | 1.995 | 2.473 | 0.187 | 0.6318 | 92.3 | 0.2129 | 1.0 | 0.1574 | équivalent |  |  |  |
| 14 | persistance | 2.254 | 2.677 | -0.203 | 1.188 |  | 0.0268 | 0.3752 | 0.8291 | équivalent |  |  |  |


Plus petite MAE : **modèle habituel, tout l'historique de la pédiatrie (sans urgences)** (1.995). Aucune variante ne bat significativement le choix retenu (D12-0 · sans les urgences (même fenêtre) (retenu)).



### Horizon J+7 (33 jours évalués, 8 origines)

| variante | variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu | DM p (pinball τ=0.8) vs charge locale | p Holm vs charge locale | vs charge locale (D12-3) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | D12-0 · sans les urgences (même fenêtre) (retenu) | 2.897 | 3.417 | 0.485 | 0.9836 | 90.9 |  |  |  | — choix retenu |  |  |  |
| 1 | D12-1 · + passages enfants aux urgences | 2.862 | 3.371 | 0.365 | 0.9886 | 90.9 | 0.7573 | 1.0 | 0.4446 | équivalent |  |  |  |
| 2 | D12-2 · + enfants graves orientés (décision observée) | 2.862 | 3.37 | 0.346 | 0.987 | 90.9 | 0.8568 | 1.0 | 0.416 | équivalent |  |  |  |
| 3 | D12-3 · + charge grave attendue Σ P(grave) (module triage) | 2.851 | 3.36 | 0.345 | 0.9874 | 90.9 | 0.8357 | 1.0 | 0.3568 | équivalent |  |  |  |
| 4 | D12-4 · + graves observés + charge | 2.841 | 3.346 | 0.287 | 0.989 | 90.9 | 0.8317 | 1.0 | 0.3626 | équivalent |  |  |  |
| 5 | D12-T · + charge du modèle transféré (cible_fourier) | 2.851 | 3.36 | 0.349 | 0.9852 | 90.9 | 0.9243 | 1.0 | 0.3303 | équivalent | 0.2038 | 1.0 | équivalent |
| 6 | D12-T · + charge du modèle transféré (source_seule) | 2.865 | 3.377 | 0.394 | 0.9882 | 90.9 | 0.8162 | 1.0 | 0.4196 | équivalent | 0.5993 | 1.0 | équivalent |
| 7 | D12-T · + charge du modèle transféré (source_recalibree) | 2.858 | 3.368 | 0.381 | 0.9886 | 90.9 | 0.8226 | 1.0 | 0.4046 | équivalent | 0.7678 | 1.0 | équivalent |
| 8 | D12-T · + charge du modèle transféré (reunies) | 2.851 | 3.361 | 0.366 | 0.9875 | 90.9 | 0.8526 | 1.0 | 0.3304 | équivalent | 0.9616 | 1.0 | équivalent |
| 9 | D12-T · + charge du modèle transféré (augmentation) | 2.857 | 3.365 | 0.367 | 0.9859 | 90.9 | 0.9085 | 1.0 | 0.3811 | équivalent | 0.4986 | 1.0 | équivalent |
| 10 | D12-T · + charge du modèle transféré (regularisation_biaisee) | 2.852 | 3.364 | 0.363 | 0.9843 | 90.9 | 0.964 | 1.0 | 0.3658 | équivalent | 0.2625 | 1.0 | équivalent |
| 11 | D12-T · + charge du modèle transféré (a_svm) | 2.85 | 3.361 | 0.351 | 0.9861 | 90.9 | 0.8879 | 1.0 | 0.3764 | équivalent | 0.1279 | 1.0 | équivalent |
| 12 | D12-T · + charge du modèle transféré (score_source) | 2.85 | 3.361 | 0.352 | 0.9834 | 90.9 | 0.9872 | 1.0 | 0.3547 | équivalent | 0.2518 | 1.0 | équivalent |
| 13 | modèle habituel, tout l'historique de la pédiatrie (sans urgences) | 3.081 | 3.663 | 1.453 | 0.9601 | 93.9 | 0.7557 | 1.0 | 0.1169 | équivalent |  |  |  |
| 14 | persistance | 2.639 | 3.606 | 0.578 | 1.146 |  | 0.4831 | 1.0 | 0.7314 | équivalent |  |  |  |


Plus petite MAE : **persistance** (2.639). Aucune variante ne bat significativement le choix retenu (D12-0 · sans les urgences (même fenêtre) (retenu)).

