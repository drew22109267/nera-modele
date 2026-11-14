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
| 16 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 0 | 99 | -0.072 | -0.24 | 0.077 | 0.5927 |
| 17 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 1 | 99 | 0.117 | -0.081 | 0.294 | 0.3681 |
| 18 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 2 | 99 | -0.039 | -0.258 | 0.231 | 0.7755 |
| 19 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 3 | 99 | 0.033 | -0.172 | 0.262 | 0.8185 |
| 20 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 0 | 99 | -0.152 | -0.27 | -0.025 | 0.2258 |
| 21 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 1 | 99 | -0.021 | -0.181 | 0.139 | 0.8773 |
| 22 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 2 | 99 | -0.024 | -0.258 | 0.212 | 0.8564 |
| 23 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 3 | 99 | -0.041 | -0.227 | 0.188 | 0.7546 |
| 24 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 0 | 99 | -0.079 | -0.249 | 0.043 | 0.5718 |
| 25 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 1 | 99 | 0.121 | -0.072 | 0.293 | 0.3616 |
| 26 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 2 | 99 | 0.023 | -0.194 | 0.237 | 0.8943 |
| 27 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 3 | 99 | 0.055 | -0.164 | 0.263 | 0.7076 |
| 28 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 0 | 99 | -0.175 | -0.354 | -0.038 | 0.1554 |
| 29 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 1 | 99 | -0.041 | -0.232 | 0.129 | 0.7507 |
| 30 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 2 | 99 | -0.007 | -0.245 | 0.184 | 0.9608 |
| 31 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 3 | 99 | -0.004 | -0.223 | 0.207 | 0.9687 |
| 32 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 0 | 99 | -0.119 | -0.303 | 0.016 | 0.376 |
| 33 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 1 | 99 | 0.119 | -0.104 | 0.312 | 0.3721 |
| 34 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 2 | 99 | 0.135 | -0.067 | 0.335 | 0.3068 |
| 35 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 3 | 99 | 0.081 | -0.108 | 0.266 | 0.5587 |
| 36 | charge Σ P(grave), modèle transféré (source_seule) | presents | 0 | 99 | -0.12 | -0.29 | 0.012 | 0.3146 |
| 37 | charge Σ P(grave), modèle transféré (source_seule) | presents | 1 | 99 | -0.04 | -0.25 | 0.141 | 0.7676 |
| 38 | charge Σ P(grave), modèle transféré (source_seule) | presents | 2 | 99 | 0.056 | -0.203 | 0.26 | 0.6567 |
| 39 | charge Σ P(grave), modèle transféré (source_seule) | presents | 3 | 99 | 0.079 | -0.131 | 0.267 | 0.5287 |
| 40 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 0 | 99 | -0.129 | -0.291 | -0.013 | 0.3473 |
| 41 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 1 | 99 | 0.115 | -0.12 | 0.327 | 0.4138 |
| 42 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 2 | 99 | 0.128 | -0.068 | 0.337 | 0.3564 |
| 43 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 3 | 99 | 0.061 | -0.112 | 0.235 | 0.6671 |
| 44 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 0 | 99 | -0.162 | -0.335 | -0.029 | 0.1789 |
| 45 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 1 | 99 | -0.047 | -0.25 | 0.124 | 0.7206 |
| 46 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 2 | 99 | 0.055 | -0.18 | 0.241 | 0.671 |
| 47 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 3 | 99 | 0.071 | -0.119 | 0.257 | 0.5927 |
| 48 | charge Σ P(grave), modèle transféré (reunies) | admissions | 0 | 99 | -0.045 | -0.254 | 0.08 | 0.7428 |
| 49 | charge Σ P(grave), modèle transféré (reunies) | admissions | 1 | 99 | 0.16 | -0.095 | 0.361 | 0.201 |
| 50 | charge Σ P(grave), modèle transféré (reunies) | admissions | 2 | 99 | 0.031 | -0.184 | 0.242 | 0.812 |
| 51 | charge Σ P(grave), modèle transféré (reunies) | admissions | 3 | 99 | 0.014 | -0.178 | 0.197 | 0.9178 |
| 52 | charge Σ P(grave), modèle transféré (reunies) | presents | 0 | 99 | -0.083 | -0.323 | 0.06 | 0.4948 |
| 53 | charge Σ P(grave), modèle transféré (reunies) | presents | 1 | 99 | 0.029 | -0.247 | 0.242 | 0.8133 |
| 54 | charge Σ P(grave), modèle transféré (reunies) | presents | 2 | 99 | 0.047 | -0.216 | 0.251 | 0.6997 |
| 55 | charge Σ P(grave), modèle transféré (reunies) | presents | 3 | 99 | 0.025 | -0.203 | 0.213 | 0.842 |
| 56 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 0 | 99 | -0.071 | -0.256 | 0.05 | 0.611 |
| 57 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 1 | 99 | 0.133 | -0.12 | 0.338 | 0.3029 |
| 58 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 2 | 99 | 0.047 | -0.163 | 0.268 | 0.7272 |
| 59 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 3 | 99 | -0.001 | -0.196 | 0.207 | 0.9961 |
| 60 | charge Σ P(grave), modèle transféré (augmentation) | presents | 0 | 99 | -0.12 | -0.321 | 0.021 | 0.3564 |
| 61 | charge Σ P(grave), modèle transféré (augmentation) | presents | 1 | 99 | 0.001 | -0.232 | 0.203 | 0.9909 |
| 62 | charge Σ P(grave), modèle transféré (augmentation) | presents | 2 | 99 | 0.045 | -0.203 | 0.248 | 0.7219 |
| 63 | charge Σ P(grave), modèle transféré (augmentation) | presents | 3 | 99 | -0.005 | -0.207 | 0.196 | 0.9739 |
| 64 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 0 | 99 | -0.1 | -0.284 | 0.035 | 0.4687 |
| 65 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 1 | 99 | 0.141 | -0.074 | 0.334 | 0.2911 |
| 66 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 2 | 99 | 0.063 | -0.142 | 0.299 | 0.6501 |
| 67 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 3 | 99 | 0.063 | -0.137 | 0.255 | 0.6488 |
| 68 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 0 | 99 | -0.145 | -0.335 | -0.01 | 0.2285 |
| 69 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 1 | 99 | -0.033 | -0.238 | 0.152 | 0.7872 |
| 70 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 2 | 99 | 0.011 | -0.246 | 0.234 | 0.9282 |
| 71 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 3 | 99 | 0.03 | -0.172 | 0.234 | 0.8133 |
| 72 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 0 | 99 | -0.093 | -0.278 | 0.038 | 0.5039 |
| 73 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 1 | 99 | 0.108 | -0.117 | 0.294 | 0.4452 |
| 74 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 2 | 99 | 0.08 | -0.124 | 0.315 | 0.5862 |
| 75 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 3 | 99 | 0.057 | -0.138 | 0.257 | 0.6984 |
| 76 | charge Σ P(grave), modèle transféré (a_svm) | presents | 0 | 99 | -0.13 | -0.301 | -0.009 | 0.2742 |
| 77 | charge Σ P(grave), modèle transféré (a_svm) | presents | 1 | 99 | -0.028 | -0.231 | 0.142 | 0.829 |
| 78 | charge Σ P(grave), modèle transféré (a_svm) | presents | 2 | 99 | 0.035 | -0.205 | 0.239 | 0.7833 |
| 79 | charge Σ P(grave), modèle transféré (a_svm) | presents | 3 | 99 | 0.052 | -0.146 | 0.259 | 0.6893 |
| 80 | charge Σ P(grave), modèle transféré (score_source) | admissions | 0 | 99 | -0.096 | -0.266 | 0.033 | 0.4869 |
| 81 | charge Σ P(grave), modèle transféré (score_source) | admissions | 1 | 99 | 0.134 | -0.078 | 0.334 | 0.3172 |
| 82 | charge Σ P(grave), modèle transféré (score_source) | admissions | 2 | 99 | 0.056 | -0.144 | 0.298 | 0.705 |
| 83 | charge Σ P(grave), modèle transféré (score_source) | admissions | 3 | 99 | 0.043 | -0.15 | 0.248 | 0.7559 |
| 84 | charge Σ P(grave), modèle transféré (score_source) | presents | 0 | 99 | -0.15 | -0.325 | -0.012 | 0.248 |
| 85 | charge Σ P(grave), modèle transféré (score_source) | presents | 1 | 99 | -0.031 | -0.219 | 0.149 | 0.8159 |
| 86 | charge Σ P(grave), modèle transféré (score_source) | presents | 2 | 99 | 0.017 | -0.233 | 0.244 | 0.8982 |
| 87 | charge Σ P(grave), modèle transféré (score_source) | presents | 3 | 99 | 0.019 | -0.177 | 0.244 | 0.8851 |


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
| 0 | D12-0 · sans les urgences (même fenêtre) (retenu) | 2.51 | 2.887 | 0.233 | 0.7854 | 87.2 |  |  |  | — choix retenu |  |  |  |
| 1 | D12-1 · + passages enfants aux urgences | 2.5 | 2.888 | 0.335 | 0.7883 | 79.5 | 0.9308 | 1.0 | 0.8093 | équivalent |  |  |  |
| 2 | D12-2 · + enfants graves orientés (décision observée) | 2.508 | 2.888 | 0.248 | 0.7892 | 82.1 | 0.713 | 1.0 | 0.9544 | équivalent |  |  |  |
| 3 | D12-3 · + charge grave attendue Σ P(grave) (module triage) | 2.484 | 2.856 | 0.252 | 0.7768 | 82.1 | 0.6143 | 1.0 | 0.492 | équivalent |  |  |  |
| 4 | D12-4 · + graves observés + charge | 2.473 | 2.853 | 0.204 | 0.7953 | 82.1 | 0.8217 | 1.0 | 0.5838 | équivalent |  |  |  |
| 5 | D12-T · + charge du modèle transféré (cible_fourier) | 2.484 | 2.856 | 0.224 | 0.7611 | 79.5 | 0.1022 | 1.0 | 0.4871 | équivalent | 0.1491 | 1.0 | équivalent |
| 6 | D12-T · + charge du modèle transféré (source_seule) | 2.49 | 2.882 | 0.298 | 0.7671 | 84.6 | 0.1526 | 1.0 | 0.6529 | équivalent | 0.5266 | 1.0 | équivalent |
| 7 | D12-T · + charge du modèle transféré (source_recalibree) | 2.494 | 2.875 | 0.246 | 0.761 | 74.4 | 0.427 | 1.0 | 0.6484 | équivalent | 0.3753 | 1.0 | équivalent |
| 8 | D12-T · + charge du modèle transféré (reunies) | 2.512 | 2.89 | 0.177 | 0.7827 | 79.5 | 0.8268 | 1.0 | 0.9463 | équivalent | 0.7024 | 1.0 | équivalent |
| 9 | D12-T · + charge du modèle transféré (augmentation) | 2.507 | 2.88 | 0.173 | 0.7785 | 76.9 | 0.6161 | 1.0 | 0.9218 | équivalent | 0.9145 | 1.0 | équivalent |
| 10 | D12-T · + charge du modèle transféré (regularisation_biaisee) | 2.474 | 2.859 | 0.291 | 0.7696 | 76.9 | 0.239 | 1.0 | 0.3974 | équivalent | 0.6182 | 1.0 | équivalent |
| 11 | D12-T · + charge du modèle transféré (a_svm) | 2.476 | 2.865 | 0.315 | 0.7642 | 82.1 | 0.3951 | 1.0 | 0.4618 | équivalent | 0.2103 | 1.0 | équivalent |
| 12 | D12-T · + charge du modèle transféré (score_source) | 2.466 | 2.847 | 0.293 | 0.77 | 76.9 | 0.2644 | 1.0 | 0.3236 | équivalent | 0.4699 | 1.0 | équivalent |
| 13 | modèle habituel, tout l'historique de la pédiatrie (sans urgences) | 1.784 | 2.171 | 0.373 | 0.6252 | 97.4 | 0.1477 | 1.0 | 0.0002 | équivalent |  |  |  |
| 14 | persistance | 2.256 | 2.864 | -0.103 | 1.159 |  | 0.0884 | 1.0 | 0.4595 | équivalent |  |  |  |


Plus petite MAE : **modèle habituel, tout l'historique de la pédiatrie (sans urgences)** (1.784). Aucune variante ne bat significativement le choix retenu (D12-0 · sans les urgences (même fenêtre) (retenu)).



### Horizon J+7 (33 jours évalués, 8 origines)

| variante | variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu | DM p (pinball τ=0.8) vs charge locale | p Holm vs charge locale | vs charge locale (D12-3) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | D12-0 · sans les urgences (même fenêtre) (retenu) | 3.552 | 4.264 | 1.485 | 1.0482 | 81.8 |  |  |  | — choix retenu |  |  |  |
| 1 | D12-1 · + passages enfants aux urgences | 3.325 | 3.952 | 1.187 | 1.041 | 78.8 | 0.9324 | 1.0 | 0.1998 | équivalent |  |  |  |
| 2 | D12-2 · + enfants graves orientés (décision observée) | 3.427 | 4.048 | 1.287 | 1.0947 | 81.8 | 0.041 | 0.574 | 0.324 | équivalent |  |  |  |
| 3 | D12-3 · + charge grave attendue Σ P(grave) (module triage) | 3.325 | 3.963 | 1.082 | 1.0555 | 78.8 | 0.8989 | 1.0 | 0.0358 | équivalent |  |  |  |
| 4 | D12-4 · + graves observés + charge | 3.29 | 3.88 | 0.984 | 1.0957 | 81.8 | 0.469 | 1.0 | 0.0984 | équivalent |  |  |  |
| 5 | D12-T · + charge du modèle transféré (cible_fourier) | 3.299 | 3.957 | 1.149 | 1.0707 | 81.8 | 0.6013 | 1.0 | 0.0178 | équivalent | 0.243 | 1.0 | équivalent |
| 6 | D12-T · + charge du modèle transféré (source_seule) | 3.36 | 4.051 | 1.234 | 1.0192 | 81.8 | 0.2019 | 1.0 | 0.0704 | équivalent | 0.3858 | 1.0 | équivalent |
| 7 | D12-T · + charge du modèle transféré (source_recalibree) | 3.335 | 4.021 | 1.292 | 1.0173 | 81.8 | 0.4681 | 1.0 | 0.0506 | équivalent | 0.0184 | 0.1472 | équivalent |
| 8 | D12-T · + charge du modèle transféré (reunies) | 3.352 | 4.011 | 1.235 | 1.0525 | 81.8 | 0.9154 | 1.0 | 0.0753 | équivalent | 0.8936 | 1.0 | équivalent |
| 9 | D12-T · + charge du modèle transféré (augmentation) | 3.418 | 4.079 | 1.257 | 1.0557 | 78.8 | 0.749 | 1.0 | 0.0 | équivalent | 0.9937 | 1.0 | équivalent |
| 10 | D12-T · + charge du modèle transféré (regularisation_biaisee) | 3.292 | 3.947 | 1.118 | 1.0457 | 81.8 | 0.9407 | 1.0 | 0.0571 | équivalent | 0.5559 | 1.0 | équivalent |
| 11 | D12-T · + charge du modèle transféré (a_svm) | 3.306 | 3.982 | 1.182 | 1.0338 | 81.8 | 0.7951 | 1.0 | 0.0464 | équivalent | 0.1057 | 0.7399 | équivalent |
| 12 | D12-T · + charge du modèle transféré (score_source) | 3.283 | 3.932 | 1.067 | 1.0479 | 78.8 | 0.9928 | 1.0 | 0.0599 | équivalent | 0.7347 | 1.0 | équivalent |
| 13 | modèle habituel, tout l'historique de la pédiatrie (sans urgences) | 3.873 | 4.836 | 3.089 | 1.3349 | 87.9 | 0.3545 | 1.0 | 0.265 | équivalent |  |  |  |
| 14 | persistance | 3.336 | 4.192 | 0.73 | 1.449 |  | 0.3031 | 1.0 | 0.8314 | équivalent |  |  |  |


Plus petite MAE : **D12-T · + charge du modèle transféré (score_source)** (3.283). Aucune variante ne bat significativement le choix retenu (D12-0 · sans les urgences (même fenêtre) (retenu)).

