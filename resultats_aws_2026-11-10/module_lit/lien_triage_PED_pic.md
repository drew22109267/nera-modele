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
| 16 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 0 | 99 | -0.072 | -0.238 | 0.079 | 0.5666 |
| 17 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 1 | 99 | 0.096 | -0.1 | 0.262 | 0.453 |
| 18 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 2 | 99 | -0.075 | -0.289 | 0.199 | 0.5574 |
| 19 | charge grave attendue Σ P(grave) (modèle de triage) | admissions | 3 | 99 | 0.019 | -0.191 | 0.255 | 0.8825 |
| 20 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 0 | 99 | -0.13 | -0.269 | 0.025 | 0.2781 |
| 21 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 1 | 99 | -0.026 | -0.172 | 0.121 | 0.8198 |
| 22 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 2 | 99 | -0.046 | -0.271 | 0.175 | 0.7076 |
| 23 | charge grave attendue Σ P(grave) (modèle de triage) | presents | 3 | 99 | -0.044 | -0.244 | 0.199 | 0.7167 |
| 24 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 0 | 99 | -0.073 | -0.24 | 0.046 | 0.5888 |
| 25 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 1 | 99 | 0.125 | -0.077 | 0.297 | 0.3525 |
| 26 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 2 | 99 | -0.002 | -0.214 | 0.217 | 0.9974 |
| 27 | charge Σ P(grave), modèle transféré (cible_fourier) | admissions | 3 | 99 | 0.052 | -0.168 | 0.267 | 0.7102 |
| 28 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 0 | 99 | -0.158 | -0.346 | -0.003 | 0.1645 |
| 29 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 1 | 99 | -0.029 | -0.222 | 0.118 | 0.8185 |
| 30 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 2 | 99 | -0.013 | -0.241 | 0.174 | 0.9164 |
| 31 | charge Σ P(grave), modèle transféré (cible_fourier) | presents | 3 | 99 | 0.019 | -0.214 | 0.243 | 0.8812 |
| 32 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 0 | 99 | -0.133 | -0.322 | 0.01 | 0.3055 |
| 33 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 1 | 99 | 0.113 | -0.1 | 0.313 | 0.3747 |
| 34 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 2 | 99 | 0.121 | -0.062 | 0.319 | 0.3512 |
| 35 | charge Σ P(grave), modèle transféré (source_seule) | admissions | 3 | 99 | 0.091 | -0.103 | 0.284 | 0.4896 |
| 36 | charge Σ P(grave), modèle transféré (source_seule) | presents | 0 | 99 | -0.088 | -0.285 | 0.058 | 0.4308 |
| 37 | charge Σ P(grave), modèle transféré (source_seule) | presents | 1 | 99 | -0.066 | -0.264 | 0.105 | 0.5548 |
| 38 | charge Σ P(grave), modèle transféré (source_seule) | presents | 2 | 99 | 0.021 | -0.223 | 0.232 | 0.8538 |
| 39 | charge Σ P(grave), modèle transféré (source_seule) | presents | 3 | 99 | 0.121 | -0.1 | 0.328 | 0.2676 |
| 40 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 0 | 99 | -0.129 | -0.29 | -0.012 | 0.3525 |
| 41 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 1 | 99 | 0.115 | -0.12 | 0.327 | 0.4164 |
| 42 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 2 | 99 | 0.129 | -0.068 | 0.337 | 0.3538 |
| 43 | charge Σ P(grave), modèle transféré (source_recalibree) | admissions | 3 | 99 | 0.061 | -0.112 | 0.235 | 0.6697 |
| 44 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 0 | 99 | -0.138 | -0.318 | 0.006 | 0.2272 |
| 45 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 1 | 99 | -0.047 | -0.235 | 0.099 | 0.6867 |
| 46 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 2 | 99 | 0.052 | -0.152 | 0.229 | 0.6645 |
| 47 | charge Σ P(grave), modèle transféré (source_recalibree) | presents | 3 | 99 | 0.104 | -0.109 | 0.315 | 0.3773 |
| 48 | charge Σ P(grave), modèle transféré (reunies) | admissions | 0 | 99 | -0.035 | -0.248 | 0.089 | 0.7911 |
| 49 | charge Σ P(grave), modèle transféré (reunies) | admissions | 1 | 99 | 0.157 | -0.099 | 0.362 | 0.2193 |
| 50 | charge Σ P(grave), modèle transféré (reunies) | admissions | 2 | 99 | 0.039 | -0.178 | 0.245 | 0.7715 |
| 51 | charge Σ P(grave), modèle transféré (reunies) | admissions | 3 | 99 | 0.021 | -0.167 | 0.197 | 0.8773 |
| 52 | charge Σ P(grave), modèle transféré (reunies) | presents | 0 | 99 | -0.069 | -0.307 | 0.085 | 0.5483 |
| 53 | charge Σ P(grave), modèle transféré (reunies) | presents | 1 | 99 | 0.036 | -0.247 | 0.236 | 0.7755 |
| 54 | charge Σ P(grave), modèle transféré (reunies) | presents | 2 | 99 | 0.074 | -0.186 | 0.272 | 0.5144 |
| 55 | charge Σ P(grave), modèle transféré (reunies) | presents | 3 | 99 | 0.075 | -0.173 | 0.269 | 0.5117 |
| 56 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 0 | 99 | -0.063 | -0.251 | 0.059 | 0.6345 |
| 57 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 1 | 99 | 0.123 | -0.127 | 0.33 | 0.3368 |
| 58 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 2 | 99 | 0.061 | -0.151 | 0.281 | 0.6514 |
| 59 | charge Σ P(grave), modèle transféré (augmentation) | admissions | 3 | 99 | 0.007 | -0.186 | 0.209 | 0.9726 |
| 60 | charge Σ P(grave), modèle transféré (augmentation) | presents | 0 | 99 | -0.093 | -0.309 | 0.064 | 0.4321 |
| 61 | charge Σ P(grave), modèle transféré (augmentation) | presents | 1 | 99 | 0.02 | -0.223 | 0.206 | 0.8838 |
| 62 | charge Σ P(grave), modèle transféré (augmentation) | presents | 2 | 99 | 0.063 | -0.183 | 0.266 | 0.6097 |
| 63 | charge Σ P(grave), modèle transféré (augmentation) | presents | 3 | 99 | 0.044 | -0.19 | 0.26 | 0.7441 |
| 64 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 0 | 99 | -0.087 | -0.268 | 0.044 | 0.5352 |
| 65 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 1 | 99 | 0.144 | -0.065 | 0.338 | 0.2833 |
| 66 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 2 | 99 | 0.062 | -0.145 | 0.3 | 0.6645 |
| 67 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | admissions | 3 | 99 | 0.06 | -0.138 | 0.25 | 0.6671 |
| 68 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 0 | 99 | -0.141 | -0.339 | -0.002 | 0.2193 |
| 69 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 1 | 99 | -0.036 | -0.235 | 0.129 | 0.7507 |
| 70 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 2 | 99 | 0.028 | -0.206 | 0.238 | 0.8068 |
| 71 | charge Σ P(grave), modèle transféré (regularisation_biaisee) | presents | 3 | 99 | 0.071 | -0.144 | 0.29 | 0.5457 |
| 72 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 0 | 99 | -0.1 | -0.286 | 0.03 | 0.4713 |
| 73 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 1 | 99 | 0.097 | -0.117 | 0.279 | 0.4817 |
| 74 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 2 | 99 | 0.084 | -0.125 | 0.326 | 0.5535 |
| 75 | charge Σ P(grave), modèle transféré (a_svm) | admissions | 3 | 99 | 0.064 | -0.135 | 0.26 | 0.6514 |
| 76 | charge Σ P(grave), modèle transféré (a_svm) | presents | 0 | 99 | -0.132 | -0.333 | 0.012 | 0.2402 |
| 77 | charge Σ P(grave), modèle transféré (a_svm) | presents | 1 | 99 | -0.04 | -0.238 | 0.114 | 0.7376 |
| 78 | charge Σ P(grave), modèle transféré (a_svm) | presents | 2 | 99 | 0.037 | -0.184 | 0.23 | 0.7507 |
| 79 | charge Σ P(grave), modèle transféré (a_svm) | presents | 3 | 99 | 0.094 | -0.127 | 0.329 | 0.4073 |
| 80 | charge Σ P(grave), modèle transféré (score_source) | admissions | 0 | 99 | -0.084 | -0.24 | 0.051 | 0.5483 |
| 81 | charge Σ P(grave), modèle transféré (score_source) | admissions | 1 | 99 | 0.13 | -0.077 | 0.322 | 0.3381 |
| 82 | charge Σ P(grave), modèle transféré (score_source) | admissions | 2 | 99 | 0.032 | -0.175 | 0.282 | 0.8211 |
| 83 | charge Σ P(grave), modèle transféré (score_source) | admissions | 3 | 99 | 0.036 | -0.159 | 0.243 | 0.7963 |
| 84 | charge Σ P(grave), modèle transféré (score_source) | presents | 0 | 99 | -0.159 | -0.341 | 0.006 | 0.2193 |
| 85 | charge Σ P(grave), modèle transféré (score_source) | presents | 1 | 99 | -0.035 | -0.207 | 0.128 | 0.8003 |
| 86 | charge Σ P(grave), modèle transféré (score_source) | presents | 2 | 99 | 0.01 | -0.221 | 0.23 | 0.9439 |
| 87 | charge Σ P(grave), modèle transféré (score_source) | presents | 3 | 99 | 0.04 | -0.168 | 0.279 | 0.7624 |


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
| 0 | D12-0 · sans les urgences (même fenêtre) (retenu) | 2.073 | 2.43 | 0.209 | 0.6869 | 69.2 |  |  | — choix retenu |  |  |  |
| 1 | D12-1 · + passages enfants aux urgences | 2.04 | 2.443 | 0.028 | 0.7457 | 69.2 | 0.0068 | 0.0884 | équivalent |  |  |  |
| 2 | D12-2 · + enfants graves orientés (décision observée) | 2.147 | 2.53 | 0.032 | 0.7403 | 69.2 | 0.0049 | 0.0686 | équivalent |  |  |  |
| 3 | D12-3 · + charge grave attendue Σ P(grave) (module triage) | 2.095 | 2.497 | 0.005 | 0.7255 | 74.4 | 0.0728 | 0.728 | équivalent |  |  |  |
| 4 | D12-4 · + graves observés + charge | 2.167 | 2.559 | -0.095 | 0.7511 | 71.8 | 0.0271 | 0.2981 | équivalent |  |  |  |
| 5 | D12-T · + charge du modèle transféré (cible_fourier) | 2.089 | 2.507 | -0.016 | 0.7092 | 71.8 | 0.1767 | 0.728 | équivalent | 0.068 | 0.476 | équivalent |
| 6 | D12-T · + charge du modèle transféré (source_seule) | 2.085 | 2.488 | -0.011 | 0.7101 | 74.4 | 0.1574 | 0.728 | équivalent | 0.0785 | 0.476 | équivalent |
| 7 | D12-T · + charge du modèle transféré (source_recalibree) | 2.041 | 2.478 | -0.051 | 0.6994 | 69.2 | 0.4837 | 0.9674 | équivalent | 0.012 | 0.096 | équivalent |
| 8 | D12-T · + charge du modèle transféré (reunies) | 2.045 | 2.453 | -0.075 | 0.7095 | 71.8 | 0.0989 | 0.728 | équivalent | 0.1423 | 0.5612 | équivalent |
| 9 | D12-T · + charge du modèle transféré (augmentation) | 2.071 | 2.489 | -0.093 | 0.7084 | 71.8 | 0.1356 | 0.728 | équivalent | 0.1403 | 0.5612 | équivalent |
| 10 | D12-T · + charge du modèle transféré (regularisation_biaisee) | 2.102 | 2.518 | 0.04 | 0.7157 | 69.2 | 0.1202 | 0.728 | équivalent | 0.0704 | 0.476 | équivalent |
| 11 | D12-T · + charge du modèle transféré (a_svm) | 2.048 | 2.444 | 0.096 | 0.7191 | 74.4 | 0.091 | 0.728 | équivalent | 0.4782 | 0.9564 | équivalent |
| 12 | D12-T · + charge du modèle transféré (score_source) | 2.105 | 2.53 | 0.041 | 0.7208 | 69.2 | 0.0746 | 0.728 | équivalent | 0.5271 | 0.9564 | équivalent |
| 13 | modèle habituel, tout l'historique de la pédiatrie (sans urgences) | 1.285 | 1.814 | 0.225 | 0.4353 | 94.9 | 0.0121 | 0.1452 | équivalent |  |  |  |
| 14 | persistance | 1.504 | 2.161 | -0.151 | 0.7973 |  | 0.4849 | 0.9674 | équivalent |  |  |  |


Plus petite perte pinball à τ = 0.8 : **modèle habituel, tout l'historique de la pédiatrie (sans urgences)** (0.4353). Aucune variante ne bat significativement le choix retenu (D12-0 · sans les urgences (même fenêtre) (retenu)) après correction de Holm.



### Horizon J+7 (33 jours évalués, 8 origines)

| variante | variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | DM p (pinball τ=0.8) | p Holm | vs choix retenu | DM p vs charge locale | p Holm vs charge locale | vs charge locale (D12-3) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | D12-0 · sans les urgences (même fenêtre) (retenu) | 2.791 | 3.245 | 0.485 | 0.9113 | 87.9 |  |  | — choix retenu |  |  |  |
| 1 | D12-1 · + passages enfants aux urgences | 2.783 | 3.223 | 0.345 | 0.912 | 87.9 | 0.8767 | 1.0 | équivalent |  |  |  |
| 2 | D12-2 · + enfants graves orientés (décision observée) | 2.815 | 3.248 | 0.363 | 0.9137 | 87.9 | 0.5896 | 1.0 | équivalent |  |  |  |
| 3 | D12-3 · + charge grave attendue Σ P(grave) (module triage) | 2.815 | 3.246 | 0.293 | 0.913 | 87.9 | 0.8063 | 1.0 | équivalent |  |  |  |
| 4 | D12-4 · + graves observés + charge | 2.843 | 3.264 | 0.249 | 0.9131 | 87.9 | 0.8547 | 1.0 | équivalent |  |  |  |
| 5 | D12-T · + charge du modèle transféré (cible_fourier) | 2.797 | 3.233 | 0.314 | 0.9132 | 87.9 | 0.7778 | 1.0 | équivalent | 0.9363 | 1.0 | équivalent |
| 6 | D12-T · + charge du modèle transféré (source_seule) | 2.804 | 3.243 | 0.368 | 0.9089 | 87.9 | 0.7787 | 1.0 | équivalent | 0.0424 | 0.3392 | équivalent |
| 7 | D12-T · + charge du modèle transféré (source_recalibree) | 2.794 | 3.233 | 0.342 | 0.9111 | 87.9 | 0.9817 | 1.0 | équivalent | 0.6265 | 1.0 | équivalent |
| 8 | D12-T · + charge du modèle transféré (reunies) | 2.791 | 3.229 | 0.335 | 0.9129 | 87.9 | 0.7952 | 1.0 | équivalent | 0.8545 | 1.0 | équivalent |
| 9 | D12-T · + charge du modèle transféré (augmentation) | 2.8 | 3.238 | 0.331 | 0.9114 | 87.9 | 0.9903 | 1.0 | équivalent | 0.4909 | 1.0 | équivalent |
| 10 | D12-T · + charge du modèle transféré (regularisation_biaisee) | 2.805 | 3.241 | 0.323 | 0.9114 | 87.9 | 0.9906 | 1.0 | équivalent | 0.1436 | 1.0 | équivalent |
| 11 | D12-T · + charge du modèle transféré (a_svm) | 2.796 | 3.234 | 0.323 | 0.9093 | 87.9 | 0.8157 | 1.0 | équivalent | 0.3886 | 1.0 | équivalent |
| 12 | D12-T · + charge du modèle transféré (score_source) | 2.805 | 3.238 | 0.305 | 0.9122 | 87.9 | 0.9186 | 1.0 | équivalent | 0.7306 | 1.0 | équivalent |
| 13 | modèle habituel, tout l'historique de la pédiatrie (sans urgences) | 3.097 | 3.769 | 1.935 | 1.025 | 93.9 | 0.4311 | 1.0 | équivalent |  |  |  |
| 14 | persistance | 2.677 | 3.514 | 0.626 | 1.1506 |  | 0.5107 | 1.0 | équivalent |  |  |  |


Plus petite perte pinball à τ = 0.8 : **D12-T · + charge du modèle transféré (source_seule)** (0.9089). Aucune variante ne bat significativement le choix retenu (D12-0 · sans les urgences (même fenêtre) (retenu)) après correction de Holm.

