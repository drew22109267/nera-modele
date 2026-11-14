# Lien entre le triage et les lits — PED (comptage : pic)

Urgences, groupe enfant : 06/07/2025 → 31/12/2025, 111 jours transcrits. Probabilités : validation croisee.

## A · Corrélation entre les urgences au jour d et le service au jour d + k

Spearman ; intervalle à 95 % par bootstrap en blocs de 7 jours ; p-valeur par décalage circulaire.

| variante | signal des urgences (jour d) | service (jour d+k) | k (jours) | jours | spearman | IC95_bas | IC95_haut | p_valeur |
|---|---|---|---|---|---|---|---|---|
| 0 | passages enfants aux urgences | admissions | 0 | 111 | 0.001 | -0.204 | 0.155 | 0.9987 |
| 1 | passages enfants aux urgences | admissions | 1 | 111 | 0.145 | -0.079 | 0.287 | 0.2402 |
| 2 | passages enfants aux urgences | admissions | 2 | 111 | 0.241 | 0.025 | 0.397 | 0.0444 |
| 3 | passages enfants aux urgences | admissions | 3 | 111 | -0.0 | -0.225 | 0.206 | 1.0 |
| 4 | passages enfants aux urgences | presents | 0 | 111 | -0.093 | -0.29 | 0.051 | 0.4608 |
| 5 | passages enfants aux urgences | presents | 1 | 111 | 0.04 | -0.188 | 0.198 | 0.7546 |
| 6 | passages enfants aux urgences | presents | 2 | 111 | 0.171 | -0.077 | 0.327 | 0.154 |
| 7 | passages enfants aux urgences | presents | 3 | 111 | 0.131 | -0.112 | 0.288 | 0.2937 |
| 8 | enfants graves orientés (décision observée) | admissions | 0 | 111 | 0.006 | -0.213 | 0.181 | 0.9465 |
| 9 | enfants graves orientés (décision observée) | admissions | 1 | 111 | 0.174 | -0.061 | 0.335 | 0.1436 |
| 10 | enfants graves orientés (décision observée) | admissions | 2 | 111 | 0.084 | -0.121 | 0.234 | 0.5 |
| 11 | enfants graves orientés (décision observée) | admissions | 3 | 111 | 0.053 | -0.131 | 0.211 | 0.6658 |
| 12 | enfants graves orientés (décision observée) | presents | 0 | 111 | -0.05 | -0.236 | 0.073 | 0.6292 |
| 13 | enfants graves orientés (décision observée) | presents | 1 | 111 | 0.093 | -0.156 | 0.248 | 0.3512 |
| 14 | enfants graves orientés (décision observée) | presents | 2 | 111 | 0.183 | -0.082 | 0.338 | 0.0679 |
| 15 | enfants graves orientés (décision observée) | presents | 3 | 111 | 0.218 | 0.008 | 0.365 | 0.0352 |
| 16 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 0 | 99 | -0.072 | -0.24 | 0.077 | 0.5927 |
| 17 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 1 | 99 | 0.117 | -0.081 | 0.294 | 0.3681 |
| 18 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 2 | 99 | -0.039 | -0.258 | 0.231 | 0.7755 |
| 19 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 3 | 99 | 0.033 | -0.172 | 0.262 | 0.8185 |
| 20 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 0 | 99 | -0.155 | -0.29 | -0.013 | 0.1893 |
| 21 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 1 | 99 | -0.033 | -0.189 | 0.116 | 0.7715 |
| 22 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 2 | 99 | -0.019 | -0.244 | 0.209 | 0.8864 |
| 23 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 3 | 99 | -0.015 | -0.209 | 0.23 | 0.9138 |
| 24 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 0 | 99 | -0.079 | -0.249 | 0.043 | 0.5718 |
| 25 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 1 | 99 | 0.121 | -0.072 | 0.293 | 0.3616 |
| 26 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 2 | 99 | 0.023 | -0.194 | 0.237 | 0.8943 |
| 27 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 3 | 99 | 0.055 | -0.164 | 0.263 | 0.7076 |
| 28 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 0 | 99 | -0.172 | -0.357 | -0.017 | 0.1214 |
| 29 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 1 | 99 | -0.034 | -0.224 | 0.116 | 0.795 |
| 30 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 2 | 99 | -0.009 | -0.233 | 0.174 | 0.9413 |
| 31 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 3 | 99 | 0.027 | -0.202 | 0.25 | 0.8342 |
| 32 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 0 | 99 | -0.119 | -0.303 | 0.016 | 0.376 |
| 33 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 1 | 99 | 0.119 | -0.104 | 0.312 | 0.3721 |
| 34 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 2 | 99 | 0.135 | -0.067 | 0.335 | 0.3068 |
| 35 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 3 | 99 | 0.081 | -0.108 | 0.266 | 0.5587 |
| 36 | charge Σ P(grave), modèle transféré (source_seule) | presents | 0 | 99 | -0.1 | -0.29 | 0.047 | 0.3825 |
| 37 | charge Σ P(grave), modèle transféré (source_seule) | presents | 1 | 99 | -0.049 | -0.248 | 0.111 | 0.6632 |
| 38 | charge Σ P(grave), modèle transféré (source_seule) | presents | 2 | 99 | 0.052 | -0.183 | 0.251 | 0.641 |
| 39 | charge Σ P(grave), modèle transféré (source_seule) | presents | 3 | 99 | 0.117 | -0.111 | 0.323 | 0.3042 |
| 40 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 0 | 99 | -0.129 | -0.291 | -0.013 | 0.3473 |
| 41 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 1 | 99 | 0.115 | -0.12 | 0.327 | 0.4138 |
| 42 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 2 | 99 | 0.128 | -0.068 | 0.337 | 0.3564 |
| 43 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 3 | 99 | 0.061 | -0.112 | 0.235 | 0.6671 |
| 44 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 0 | 99 | -0.137 | -0.317 | 0.007 | 0.2311 |
| 45 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 1 | 99 | -0.048 | -0.237 | 0.099 | 0.6815 |
| 46 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 2 | 99 | 0.051 | -0.152 | 0.228 | 0.6697 |
| 47 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 3 | 99 | 0.104 | -0.11 | 0.315 | 0.3825 |
| 48 | charge Σ P(grave), modèle transféré (reunies) | admissions | 0 | 99 | -0.045 | -0.254 | 0.08 | 0.7428 |
| 49 | charge Σ P(grave), modèle transféré (reunies) | admissions | 1 | 99 | 0.16 | -0.095 | 0.361 | 0.201 |
| 50 | charge Σ P(grave), modèle transféré (reunies) | admissions | 2 | 99 | 0.031 | -0.184 | 0.242 | 0.812 |
| 51 | charge Σ P(grave), modèle transféré (reunies) | admissions | 3 | 99 | 0.014 | -0.178 | 0.197 | 0.9178 |
| 52 | charge Σ P(grave), modèle transféré (reunies) | presents | 0 | 99 | -0.072 | -0.307 | 0.085 | 0.5431 |
| 53 | charge Σ P(grave), modèle transféré (reunies) | presents | 1 | 99 | 0.027 | -0.254 | 0.229 | 0.8225 |
| 54 | charge Σ P(grave), modèle transféré (reunies) | presents | 2 | 99 | 0.06 | -0.195 | 0.264 | 0.6162 |
| 55 | charge Σ P(grave), modèle transféré (reunies) | presents | 3 | 99 | 0.066 | -0.184 | 0.269 | 0.5757 |
| 56 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 0 | 99 | -0.071 | -0.256 | 0.05 | 0.611 |
| 57 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 1 | 99 | 0.133 | -0.12 | 0.338 | 0.3029 |
| 58 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 2 | 99 | 0.047 | -0.163 | 0.268 | 0.7272 |
| 59 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 3 | 99 | -0.001 | -0.196 | 0.207 | 0.9961 |
| 60 | charge Σ P(grave), modèle transféré (augmentation) | presents | 0 | 99 | -0.106 | -0.315 | 0.048 | 0.3864 |
| 61 | charge Σ P(grave), modèle transféré (augmentation) | presents | 1 | 99 | 0.007 | -0.23 | 0.191 | 0.9634 |
| 62 | charge Σ P(grave), modèle transféré (augmentation) | presents | 2 | 99 | 0.049 | -0.192 | 0.251 | 0.7115 |
| 63 | charge Σ P(grave), modèle transféré (augmentation) | presents | 3 | 99 | 0.03 | -0.2 | 0.252 | 0.8277 |
| 64 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 0 | 99 | -0.1 | -0.284 | 0.035 | 0.4687 |
| 65 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 1 | 99 | 0.141 | -0.074 | 0.334 | 0.2911 |
| 66 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 2 | 99 | 0.063 | -0.142 | 0.299 | 0.6501 |
| 67 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 3 | 99 | 0.063 | -0.137 | 0.255 | 0.6488 |
| 68 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 0 | 99 | -0.133 | -0.337 | 0.014 | 0.248 |
| 69 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 1 | 99 | -0.044 | -0.245 | 0.118 | 0.7089 |
| 70 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 2 | 99 | 0.017 | -0.221 | 0.227 | 0.8812 |
| 71 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 3 | 99 | 0.068 | -0.146 | 0.287 | 0.5757 |
| 72 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 0 | 99 | -0.093 | -0.278 | 0.038 | 0.5039 |
| 73 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 1 | 99 | 0.108 | -0.117 | 0.294 | 0.4452 |
| 74 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 2 | 99 | 0.08 | -0.124 | 0.315 | 0.5862 |
| 75 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 3 | 99 | 0.057 | -0.138 | 0.257 | 0.6984 |
| 76 | charge Σ P(grave), modèle transféré (a_svm) | presents | 0 | 99 | -0.116 | -0.297 | 0.025 | 0.3016 |
| 77 | charge Σ P(grave), modèle transféré (a_svm) | presents | 1 | 99 | -0.032 | -0.221 | 0.117 | 0.7781 |
| 78 | charge Σ P(grave), modèle transféré (a_svm) | presents | 2 | 99 | 0.039 | -0.186 | 0.241 | 0.7363 |
| 79 | charge Σ P(grave), modèle transféré (a_svm) | presents | 3 | 99 | 0.086 | -0.132 | 0.317 | 0.453 |
| 80 | charge Σ P(grave), modèle transféré (score_source) | admissions | 0 | 99 | -0.096 | -0.266 | 0.033 | 0.4869 |
| 81 | charge Σ P(grave), modèle transféré (score_source) | admissions | 1 | 99 | 0.134 | -0.078 | 0.334 | 0.3172 |
| 82 | charge Σ P(grave), modèle transféré (score_source) | admissions | 2 | 99 | 0.056 | -0.144 | 0.298 | 0.705 |
| 83 | charge Σ P(grave), modèle transféré (score_source) | admissions | 3 | 99 | 0.043 | -0.15 | 0.248 | 0.7559 |
| 84 | charge Σ P(grave), modèle transféré (score_source) | presents | 0 | 99 | -0.143 | -0.33 | 0.013 | 0.252 |
| 85 | charge Σ P(grave), modèle transféré (score_source) | presents | 1 | 99 | -0.036 | -0.223 | 0.127 | 0.7755 |
| 86 | charge Σ P(grave), modèle transféré (score_source) | presents | 2 | 99 | 0.022 | -0.217 | 0.244 | 0.8642 |
| 87 | charge Σ P(grave), modèle transféré (score_source) | presents | 3 | 99 | 0.062 | -0.149 | 0.304 | 0.6175 |


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
| 0 | D12-0 · sans les urgences (même fenêtre) (retenu) | 2.073 | 2.43 | 0.209 | 0.6869 | 69.2 |  |  |  | — choix retenu |  |  |  |
| 1 | D12-1 · + passages enfants aux urgences | 2.04 | 2.443 | 0.028 | 0.7457 | 69.2 | 0.0068 | 0.0884 | 0.6408 | équivalent |  |  |  |
| 2 | D12-2 · + enfants graves orientés (décision observée) | 2.147 | 2.53 | 0.032 | 0.7403 | 69.2 | 0.0049 | 0.0686 | 0.4378 | équivalent |  |  |  |
| 3 | D12-3 · + charge grave attendue Σ P(grave) (module triage) | 2.09 | 2.492 | 0.023 | 0.7293 | 74.4 | 0.0577 | 0.577 | 0.8331 | équivalent |  |  |  |
| 4 | D12-4 · + graves observés + charge | 2.167 | 2.561 | -0.087 | 0.7528 | 74.4 | 0.0272 | 0.2992 | 0.397 | équivalent |  |  |  |
| 5 | D12-T · + charge du modèle transféré (cible_fourier) | 2.095 | 2.516 | -0.019 | 0.7088 | 71.8 | 0.2187 | 0.8541 | 0.8012 | équivalent | 0.0374 | 0.2422 | équivalent |
| 6 | D12-T · + charge du modèle transféré (source_seule) | 2.075 | 2.459 | 0.022 | 0.7131 | 74.4 | 0.1326 | 0.8541 | 0.9743 | équivalent | 0.0553 | 0.2765 | équivalent |
| 7 | D12-T · + charge du modèle transféré (source_recalibree) | 2.042 | 2.478 | -0.051 | 0.6998 | 69.2 | 0.471 | 0.942 | 0.717 | équivalent | 0.0097 | 0.0776 | équivalent |
| 8 | D12-T · + charge du modèle transféré (reunies) | 2.042 | 2.452 | -0.076 | 0.7092 | 71.8 | 0.1042 | 0.8541 | 0.6601 | équivalent | 0.0964 | 0.3144 | équivalent |
| 9 | D12-T · + charge du modèle transféré (augmentation) | 2.066 | 2.488 | -0.097 | 0.7096 | 71.8 | 0.1136 | 0.8541 | 0.924 | équivalent | 0.1205 | 0.3144 | équivalent |
| 10 | D12-T · + charge du modèle transféré (regularisation_biaisee) | 2.102 | 2.513 | 0.038 | 0.7162 | 69.2 | 0.12 | 0.8541 | 0.718 | équivalent | 0.0346 | 0.2422 | équivalent |
| 11 | D12-T · + charge du modèle transféré (a_svm) | 2.06 | 2.458 | 0.1 | 0.72 | 71.8 | 0.0949 | 0.8541 | 0.8619 | équivalent | 0.2838 | 0.3144 | équivalent |
| 12 | D12-T · + charge du modèle transféré (score_source) | 2.103 | 2.518 | 0.058 | 0.7161 | 69.2 | 0.1156 | 0.8541 | 0.7136 | équivalent | 0.0786 | 0.3144 | équivalent |
| 13 | modèle habituel, tout l'historique de la pédiatrie (sans urgences) | 1.285 | 1.814 | 0.225 | 0.4353 | 94.9 | 0.0121 | 0.1452 | 0.0001 | équivalent |  |  |  |
| 14 | persistance | 1.504 | 2.161 | -0.151 | 0.7973 |  | 0.4849 | 0.942 | 0.0579 | équivalent |  |  |  |


Plus petite MAE : **modèle habituel, tout l'historique de la pédiatrie (sans urgences)** (1.285). Aucune variante ne bat significativement le choix retenu (D12-0 · sans les urgences (même fenêtre) (retenu)).



### Horizon J+7 (33 jours évalués, 8 origines)

| variante | variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | DM p (pinball τ=0.8) | p Holm | DM p (MAE) | vs choix retenu | DM p (pinball τ=0.8) vs charge locale | p Holm vs charge locale | vs charge locale (D12-3) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | D12-0 · sans les urgences (même fenêtre) (retenu) | 2.791 | 3.245 | 0.485 | 0.9113 | 87.9 |  |  |  | — choix retenu |  |  |  |
| 1 | D12-1 · + passages enfants aux urgences | 2.783 | 3.223 | 0.345 | 0.912 | 87.9 | 0.8767 | 1.0 | 0.9257 | équivalent |  |  |  |
| 2 | D12-2 · + enfants graves orientés (décision observée) | 2.815 | 3.248 | 0.363 | 0.9137 | 87.9 | 0.5896 | 1.0 | 0.7429 | équivalent |  |  |  |
| 3 | D12-3 · + charge grave attendue Σ P(grave) (module triage) | 2.812 | 3.244 | 0.298 | 0.9126 | 87.9 | 0.8474 | 1.0 | 0.8504 | équivalent |  |  |  |
| 4 | D12-4 · + graves observés + charge | 2.841 | 3.262 | 0.255 | 0.9126 | 87.9 | 0.8918 | 1.0 | 0.7308 | équivalent |  |  |  |
| 5 | D12-T · + charge du modèle transféré (cible_fourier) | 2.795 | 3.232 | 0.318 | 0.9126 | 87.9 | 0.8343 | 1.0 | 0.9655 | équivalent | 0.9978 | 1.0 | équivalent |
| 6 | D12-T · + charge du modèle transféré (source_seule) | 2.806 | 3.244 | 0.369 | 0.9086 | 87.9 | 0.7778 | 1.0 | 0.8577 | équivalent | 0.255 | 1.0 | équivalent |
| 7 | D12-T · + charge du modèle transféré (source_recalibree) | 2.793 | 3.232 | 0.341 | 0.911 | 87.9 | 0.9796 | 1.0 | 0.9816 | équivalent | 0.723 | 1.0 | équivalent |
| 8 | D12-T · + charge du modèle transféré (reunies) | 2.79 | 3.228 | 0.335 | 0.9128 | 87.9 | 0.8167 | 1.0 | 0.9894 | équivalent | 0.866 | 1.0 | équivalent |
| 9 | D12-T · + charge du modèle transféré (augmentation) | 2.8 | 3.237 | 0.329 | 0.9116 | 87.9 | 0.975 | 1.0 | 0.9246 | équivalent | 0.6866 | 1.0 | équivalent |
| 10 | D12-T · + charge du modèle transféré (regularisation_biaisee) | 2.802 | 3.238 | 0.319 | 0.9113 | 87.9 | 0.9954 | 1.0 | 0.9143 | équivalent | 0.2165 | 1.0 | équivalent |
| 11 | D12-T · + charge du modèle transféré (a_svm) | 2.798 | 3.234 | 0.321 | 0.9094 | 87.9 | 0.8368 | 1.0 | 0.948 | équivalent | 0.4648 | 1.0 | équivalent |
| 12 | D12-T · + charge du modèle transféré (score_source) | 2.801 | 3.234 | 0.304 | 0.9114 | 87.9 | 0.9872 | 1.0 | 0.93 | équivalent | 0.5357 | 1.0 | équivalent |
| 13 | modèle habituel, tout l'historique de la pédiatrie (sans urgences) | 3.097 | 3.769 | 1.935 | 1.025 | 93.9 | 0.4311 | 1.0 | 0.444 | équivalent |  |  |  |
| 14 | persistance | 2.677 | 3.514 | 0.626 | 1.1506 |  | 0.5107 | 1.0 | 0.8571 | équivalent |  |  |  |


Plus petite MAE : **persistance** (2.677). Aucune variante ne bat significativement le choix retenu (D12-0 · sans les urgences (même fenêtre) (retenu)).

