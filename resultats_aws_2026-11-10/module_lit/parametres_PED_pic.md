# Sensibilité de tous les paramètres — service PED_pic

Un paramètre varie à la fois, tout le reste au réglage retenu (marqué « retenu »). Mêmes jours, même validation glissante. Diebold-Mariano (perte pinball au quantile τ, HLN, correction de Holm) contre la valeur retenue. Amplitude = (MAE max − MAE min) / MAE retenue.


## Synthèse

| paramètre | horizon | famille | valeur retenue | meilleure valeur (MAE) | amplitude MAE % | verdict |
|---|---|---|---|---|---|---|
| C (poids des erreurs) | 1 | svr4 | 3 | 10 | 73.7 | défendable |
| ε (tube, niveaux quantiles) | 1 | svr4 | 0,25 | 0,5 | 2.1 | défendable |
| γ₁ (portée, bloc occupation) | 1 | svr4 | 0,02 | 0,02 (retenu) | 11.8 | défendable |
| γ₂ (portée, bloc flux et saison) | 1 | svr4 | 0,2 | 0,1 | 11.3 | défendable |
| τ (quantile décisionnel) | 1 | svr4 | 0,8 | 0,5 | 0.1 | défendable |
| η₀ (taux d'apprentissage d'Adam) | 1 | svr4 | 0,05 | 0,2 | 0.4 | défendable |
| nombre maximal d'itérations | 1 | svr4 | 3000 | 1000 | 0.1 | défendable |
| T (décroissance du pas ; aucune = pas constant) | 1 | svr4 | 500 | aucune | 0.1 | défendable |
| part des pas moyennée (Polyak ; 0 = aucune) | 1 | svr4 | 0,5 | 0 | 0.0 | défendable |
| tolérance d'arrêt anticipé | 1 | svr4 | 1e-07 | 1e-05 | 0.0 | défendable |
| direction préconditionnée α + Cg | 1 | svr4 | True | True (retenu) | 1.6 | défendable |
| optimiseur | 1 | svr4 | adam | adam (retenu) | 72.9 | défendable |
| C | 1 | svr2 | 3 | 3 (retenu) | 53.1 | défendable |
| ε (tube ε-insensible, en lits) | 1 | svr2 | 0,5 | 0,25 | 8.0 | défendable |
| γ (portée du noyau RBF) | 1 | svr2 | 0,02 | 0,02 (retenu) | 67.2 | défendable |
| nombre d'arbres | 1 | foret | 300 | 50 | 1.5 | défendable |
| profondeur maximale | 1 | foret | 12 | 20 | 10.2 | défendable |
| taille minimale d'une feuille | 1 | foret | 5 | 2 | 3.5 | à revoir : 2 |
| part des variables tirées par nœud | 1 | foret | 0,333333 | 0,5 | 6.4 | défendable |
| nombre d'étapes | 1 | boosting | 300 | 600 | 9.2 | défendable |
| taux ν (shrinkage) | 1 | boosting | 0,05 | 0,05 (retenu) | 8.1 | défendable |
| profondeur des arbres | 1 | boosting | 3 | 3 (retenu) | 6.2 | défendable |
| part du sous-échantillon | 1 | boosting | 0,8 | 0,5 | 2.8 | défendable |
| architecture (neurones par couche) | 1 | mlp | 32×16 | 8 | 6.3 | défendable |
| taux d'apprentissage | 1 | mlp | 0,01 | 0,001 | 2.4 | défendable |
| pénalité L2 λ | 1 | mlp | 0,001 | 0,01 | 5.6 | défendable |
| époques maximales | 1 | mlp | 1500 | 300 | 0.0 | défendable |
| patience de l'arrêt anticipé | 1 | mlp | 150 | 50 | 0.2 | défendable |
| nombre d'initialisations moyennées | 1 | mlp | 3 | 3 (retenu) | 7.8 | défendable |
| taille de l'état caché H | 1 | lstm | 16 | 4 | 2.8 | défendable |
| taux d'apprentissage | 1 | lstm | 0,01 | 0,03 | 1.6 | défendable |
| pénalité L2 λ | 1 | lstm | 0,001 | 0,01 | 1.1 | défendable |
| jours d'occupation passée en entrée | 1 | variables | 7 | 5 | 3.8 | défendable |
| C (poids des erreurs) | 7 | svr4 | 0,3 | 1 | 17.4 | défendable |
| ε (tube, niveaux quantiles) | 7 | svr4 | 0 | 0,25 | 0.8 | défendable |
| γ₁ (portée, bloc occupation) | 7 | svr4 | 0,02 | 0,01 | 2.1 | défendable |
| γ₂ (portée, bloc flux et saison) | 7 | svr4 | 0,2 | 0,2 (retenu) | 3.1 | défendable |
| τ (quantile décisionnel) | 7 | svr4 | 0,8 | 0,5 | 0.0 | défendable |
| η₀ (taux d'apprentissage d'Adam) | 7 | svr4 | 0,05 | 0,02 | 0.1 | défendable |
| nombre maximal d'itérations | 7 | svr4 | 3000 | 1000 | 0.0 | défendable |
| T (décroissance du pas ; aucune = pas constant) | 7 | svr4 | 500 | aucune | 0.0 | défendable |
| part des pas moyennée (Polyak ; 0 = aucune) | 7 | svr4 | 0,5 | 0 | 0.0 | défendable |
| tolérance d'arrêt anticipé | 7 | svr4 | 1e-07 | 1e-09 | 0.1 | défendable |
| direction préconditionnée α + Cg | 7 | svr4 | True | True (retenu) | 0.4 | défendable |
| optimiseur | 7 | svr4 | adam | momentum | 0.1 | défendable |
| C | 7 | svr2 | 0,3 | 0,1 | 15.1 | défendable |
| ε (tube ε-insensible, en lits) | 7 | svr2 | 1 | 0,5 | 0.4 | défendable |
| γ (portée du noyau RBF) | 7 | svr2 | 0,2 | 0,5 | 2.8 | défendable |
| nombre d'arbres | 7 | foret | 300 | 50 | 2.5 | défendable |
| profondeur maximale | 7 | foret | 12 | 3 | 1.5 | défendable |
| taille minimale d'une feuille | 7 | foret | 5 | 10 | 2.4 | défendable |
| part des variables tirées par nœud | 7 | foret | 0,333333 | 0,333333 (retenu) | 0.8 | défendable |
| nombre d'étapes | 7 | boosting | 300 | 50 | 2.9 | défendable |
| taux ν (shrinkage) | 7 | boosting | 0,05 | 0,01 | 2.0 | défendable |
| profondeur des arbres | 7 | boosting | 3 | 2 | 1.5 | défendable |
| part du sous-échantillon | 7 | boosting | 0,8 | 0,5 | 0.4 | défendable |
| architecture (neurones par couche) | 7 | mlp | 32×16 | 32×16×8 | 2.1 | défendable |
| taux d'apprentissage | 7 | mlp | 0,01 | 0,003 | 1.1 | défendable |
| pénalité L2 λ | 7 | mlp | 0,001 | 0 | 1.4 | défendable |
| époques maximales | 7 | mlp | 1500 | 300 | 0.0 | défendable |
| patience de l'arrêt anticipé | 7 | mlp | 150 | 50 | 0.0 | défendable |
| nombre d'initialisations moyennées | 7 | mlp | 3 | 5 | 2.1 | défendable |
| taille de l'état caché H | 7 | lstm | 16 | 4 | 5.4 | défendable |
| taux d'apprentissage | 7 | lstm | 0,01 | 0,003 | 2.2 | défendable |
| pénalité L2 λ | 7 | lstm | 0,001 | 0,01 | 2.5 | défendable |
| jours d'occupation passée en entrée | 7 | variables | 7 | 3 | 0.8 | défendable |


## Horizon J+1


### svr4 · C (poids des erreurs)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| C = 0,1 | 2.296 | 2.803 | -0.027 | 0.7981 | 89.6 | 4.5 | 0.0 | 0.0 | moins bon |
| C = 0,3 | 1.868 | 2.318 | -0.053 | 0.6819 | 88.5 | 6.7 | 0.0 | 0.0 | moins bon |
| C = 1 | 1.5 | 1.931 | 0.006 | 0.5509 | 87.4 | 10.1 | 0.01 | 0.0267 | moins bon |
| C = 3 (retenu) | 1.336 | 1.823 | 0.039 | 0.4993 | 89.1 | 13.1 |  |  | — choix retenu |
| C = 10 | 1.311 | 1.805 | 0.01 | 0.5177 | 83.1 | 14.8 | 0.3081 | 0.3081 | équivalent |
| C = 30 | 1.447 | 1.947 | 0.008 | 0.5818 | 63.4 | 14.5 | 0.0089 | 0.0267 | moins bon |


![C (poids des erreurs)](parametres_PED_pic_svr4_C_h1.png)

Amplitude de la MAE : 73.7 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · ε (tube, niveaux quantiles)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| epsilon_quantile = 0 | 1.337 | 1.827 | 0.036 | 0.5049 | 91.3 | 11.2 | 0.1588 | 0.3176 | équivalent |
| epsilon_quantile = 0,25 (retenu) | 1.336 | 1.823 | 0.039 | 0.4993 | 89.1 | 13.7 |  |  | — choix retenu |
| epsilon_quantile = 0,5 | 1.329 | 1.81 | 0.011 | 0.4983 | 85.2 | 13.8 | 0.7908 | 0.7908 | équivalent |
| epsilon_quantile = 1 | 1.357 | 1.815 | -0.01 | 0.5278 | 81.4 | 14.2 | 0.0097 | 0.0291 | moins bon |


![ε (tube, niveaux quantiles)](parametres_PED_pic_svr4_epsilon_quantile_h1.png)

Amplitude de la MAE : 2.1 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · γ₁ (portée, bloc occupation)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| gamma1 = 0,01 | 1.376 | 1.845 | 0.003 | 0.4942 | 89.1 | 13.6 | 0.5738 | 0.5738 | équivalent |
| gamma1 = 0,02 (retenu) | 1.336 | 1.823 | 0.039 | 0.4993 | 89.1 | 12.6 |  |  | — choix retenu |
| gamma1 = 0,05 | 1.336 | 1.818 | 0.023 | 0.5107 | 88.0 | 12.3 | 0.1115 | 0.223 | équivalent |
| gamma1 = 0,1 | 1.37 | 1.849 | 0.045 | 0.5252 | 85.8 | 12.6 | 0.0275 | 0.0825 | équivalent |
| gamma1 = 0,2 | 1.424 | 1.888 | 0.07 | 0.5517 | 84.2 | 12.6 | 0.0002 | 0.0008 | moins bon |
| gamma1 = 0,5 | 1.494 | 1.941 | 0.067 | 0.5912 | 83.6 | 11.4 | 0.0 | 0.0 | moins bon |


![γ₁ (portée, bloc occupation)](parametres_PED_pic_svr4_gamma1_h1.png)

Amplitude de la MAE : 11.8 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · γ₂ (portée, bloc flux et saison)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| gamma2 = 0,02 | 1.376 | 1.849 | 0.013 | 0.546 | 88.5 | 9.3 | 0.0015 | 0.0045 | moins bon |
| gamma2 = 0,05 | 1.321 | 1.805 | 0.03 | 0.521 | 88.5 | 12.6 | 0.0454 | 0.0908 | équivalent |
| gamma2 = 0,1 | 1.31 | 1.801 | 0.032 | 0.5023 | 89.1 | 12.9 | 0.6189 | 0.6189 | équivalent |
| gamma2 = 0,2 (retenu) | 1.336 | 1.823 | 0.039 | 0.4993 | 89.1 | 12.4 |  |  | — choix retenu |
| gamma2 = 0,5 | 1.461 | 1.946 | 0.051 | 0.5469 | 82.5 | 13.5 | 0.0 | 0.0 | moins bon |


![γ₂ (portée, bloc flux et saison)](parametres_PED_pic_svr4_gamma2_h1.png)

Amplitude de la MAE : 11.3 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · τ (quantile décisionnel)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| tau = 0,5 | 1.335 | 1.823 | 0.04 | 0.6558 | 89.1 | 9.3 | 0.0001 | 0.0004 | moins bon |
| tau = 0,6 | 1.336 | 1.824 | 0.039 | 0.6564 | 89.1 | 12.1 | 0.0001 | 0.0004 | moins bon |
| tau = 0,7 | 1.335 | 1.823 | 0.04 | 0.6558 | 89.1 | 13.0 | 0.0001 | 0.0004 | moins bon |
| tau = 0,8 (retenu) | 1.336 | 1.823 | 0.039 | 0.4993 | 89.1 | 14.8 |  |  | — choix retenu |
| tau = 0,9 | 1.336 | 1.823 | 0.039 | 0.6564 | 89.1 | 14.0 | 0.0001 | 0.0004 | moins bon |


![τ (quantile décisionnel)](parametres_PED_pic_svr4_tau_h1.png)

Amplitude de la MAE : 0.1 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · η₀ (taux d'apprentissage d'Adam)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| taux = 0,005 | 1.337 | 1.825 | 0.041 | 0.4971 | 88.5 | 13.4 | 0.182 | 0.91 | équivalent |
| taux = 0,01 | 1.337 | 1.824 | 0.039 | 0.4978 | 89.6 | 12.8 | 0.2472 | 0.9888 | équivalent |
| taux = 0,02 | 1.336 | 1.824 | 0.041 | 0.499 | 89.1 | 12.9 | 0.5818 | 1.0 | équivalent |
| taux = 0,05 (retenu) | 1.336 | 1.823 | 0.039 | 0.4993 | 89.1 | 13.2 |  |  | — choix retenu |
| taux = 0,1 | 1.333 | 1.821 | 0.033 | 0.4991 | 88.5 | 13.5 | 0.4865 | 1.0 | équivalent |
| taux = 0,2 | 1.331 | 1.821 | 0.03 | 0.4995 | 89.6 | 14.5 | 0.9174 | 1.0 | équivalent |


![η₀ (taux d'apprentissage d'Adam)](parametres_PED_pic_svr4_taux_h1.png)

Amplitude de la MAE : 0.4 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · nombre maximal d'itérations

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| iterations = 300 | 1.337 | 1.824 | 0.034 | 0.493 | 89.1 | 1.7 | 0.0351 | 0.1053 | équivalent |
| iterations = 1000 | 1.336 | 1.823 | 0.037 | 0.4991 | 89.6 | 5.2 | 0.6669 | 1.0 | équivalent |
| iterations = 3000 (retenu) | 1.336 | 1.823 | 0.039 | 0.4993 | 89.1 | 12.8 |  |  | — choix retenu |
| iterations = 6000 | 1.336 | 1.823 | 0.04 | 0.4994 | 89.1 | 21.5 | 0.7449 | 1.0 | équivalent |


![nombre maximal d'itérations](parametres_PED_pic_svr4_iterations_h1.png)

Amplitude de la MAE : 0.1 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · T (décroissance du pas ; aucune = pas constant)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| decroissance = aucune | 1.335 | 1.822 | 0.036 | 0.4995 | 88.5 | 14.1 | 0.7515 | 0.9195 | équivalent |
| decroissance = 100 | 1.336 | 1.823 | 0.042 | 0.4988 | 89.1 | 12.0 | 0.3065 | 0.9195 | équivalent |
| decroissance = 500 (retenu) | 1.336 | 1.823 | 0.039 | 0.4993 | 89.1 | 13.0 |  |  | — choix retenu |
| decroissance = 2000 | 1.335 | 1.823 | 0.035 | 0.499 | 89.1 | 13.7 | 0.439 | 0.9195 | équivalent |


![T (décroissance du pas ; aucune = pas constant)](parametres_PED_pic_svr4_decroissance_h1.png)

Amplitude de la MAE : 0.1 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · part des pas moyennée (Polyak ; 0 = aucune)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| moyenne_polyak = 0 | 1.336 | 1.824 | 0.039 | 0.4993 | 89.1 | 11.6 | 0.3173 | 0.6346 | équivalent |
| moyenne_polyak = 0,25 | 1.336 | 1.823 | 0.039 | 0.4993 | 89.1 | 13.3 | 0.3173 | 0.6346 | équivalent |
| moyenne_polyak = 0,5 (retenu) | 1.336 | 1.823 | 0.039 | 0.4993 | 89.1 | 13.0 |  |  | — choix retenu |
| moyenne_polyak = 0,75 | 1.336 | 1.823 | 0.039 | 0.4993 | 89.1 | 12.0 |  |  | identique |


![part des pas moyennée (Polyak ; 0 = aucune)](parametres_PED_pic_svr4_moyenne_polyak_h1.png)

Amplitude de la MAE : 0.0 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · tolérance d'arrêt anticipé

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| tolerance = 1e-05 | 1.336 | 1.823 | 0.033 | 0.4963 | 89.1 | 3.1 | 0.0265 | 0.053 | équivalent |
| tolerance = 1e-07 (retenu) | 1.336 | 1.823 | 0.039 | 0.4993 | 89.1 | 12.1 |  |  | — choix retenu |
| tolerance = 1e-09 | 1.336 | 1.824 | 0.04 | 0.4993 | 88.5 | 14.8 | 0.6598 | 0.6598 | équivalent |


![tolérance d'arrêt anticipé](parametres_PED_pic_svr4_tolerance_h1.png)

Amplitude de la MAE : 0.0 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · direction préconditionnée α + Cg

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| preconditionne = True (retenu) | 1.336 | 1.823 | 0.039 | 0.4993 | 89.1 | 12.6 |  |  | — choix retenu |
| preconditionne = False | 1.357 | 1.843 | 0.029 | 0.5043 | 89.6 | 20.5 | 0.1228 | 0.1228 | équivalent |


![direction préconditionnée α + Cg](parametres_PED_pic_svr4_preconditionne_h1.png)

Amplitude de la MAE : 1.6 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · optimiseur

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| optimiseur = adam (retenu) | 1.336 | 1.823 | 0.039 | 0.4993 | 89.1 | 13.2 |  |  | — choix retenu |
| optimiseur = momentum | 2.31 | 2.951 | -1.026 | 0.7749 | 88.5 | 11.6 | 0.0 | 0.0 | moins bon |
| optimiseur = sgd | 2.258 | 2.873 | -1.114 | 0.5379 | 88.0 | 10.5 | 0.2241 | 0.2241 | équivalent |


![optimiseur](parametres_PED_pic_svr4_optimiseur_h1.png)

Amplitude de la MAE : 72.9 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr2 · C

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| C = 0,1 | 1.923 | 2.372 | -0.042 | 0.9738 | 0.5 | 0.0 | 0.0 | moins bon |
| C = 0,3 | 1.558 | 1.973 | -0.014 | 0.7831 | 0.8 | 0.0001 | 0.0004 | moins bon |
| C = 1 | 1.315 | 1.768 | -0.025 | 0.6649 | 1.3 | 0.0101 | 0.0303 | moins bon |
| C = 3 (retenu) | 1.256 | 1.724 | -0.008 | 0.6302 | 1.9 |  |  | — choix retenu |
| C = 10 | 1.257 | 1.728 | -0.016 | 0.6333 | 2.0 | 0.7643 | 0.7643 | équivalent |
| C = 30 | 1.272 | 1.737 | -0.087 | 0.6622 | 1.8 | 0.099 | 0.198 | équivalent |


![C](parametres_PED_pic_svr2_C_h1.png)

Amplitude de la MAE : 53.1 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr2 · ε (tube ε-insensible, en lits)

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| epsilon = 0 | 1.257 | 1.755 | -0.047 | 0.6429 | 1.8 | 0.1494 | 0.2988 | équivalent |
| epsilon = 0,25 | 1.256 | 1.738 | -0.05 | 0.6426 | 1.8 | 0.0273 | 0.0819 | équivalent |
| epsilon = 0,5 (retenu) | 1.256 | 1.724 | -0.008 | 0.6302 | 1.9 |  |  | — choix retenu |
| epsilon = 1 | 1.295 | 1.733 | 0.001 | 0.6474 | 1.3 | 0.0152 | 0.0608 | équivalent |
| epsilon = 2 | 1.357 | 1.781 | 0.093 | 0.6509 | 1.7 | 0.2509 | 0.2988 | équivalent |


![ε (tube ε-insensible, en lits)](parametres_PED_pic_svr2_epsilon_h1.png)

Amplitude de la MAE : 8.0 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr2 · γ (portée du noyau RBF)

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| gamma = 0,005 | 1.313 | 1.78 | -0.014 | 0.6608 | 1.7 | 0.0354 | 0.0708 | équivalent |
| gamma = 0,01 | 1.266 | 1.744 | -0.005 | 0.6347 | 1.5 | 0.5133 | 0.5133 | équivalent |
| gamma = 0,02 (retenu) | 1.256 | 1.724 | -0.008 | 0.6302 | 1.9 |  |  | — choix retenu |
| gamma = 0,05 | 1.29 | 1.749 | -0.056 | 0.6621 | 1.8 | 0.0117 | 0.0351 | moins bon |
| gamma = 0,1 | 1.412 | 1.852 | -0.054 | 0.722 | 1.9 | 0.0006 | 0.0024 | moins bon |
| gamma = 0,2 | 1.579 | 2.03 | -0.037 | 0.8007 | 1.6 | 0.0 | 0.0 | moins bon |
| gamma = 0,5 | 2.1 | 2.628 | 0.07 | 1.0293 | 1.1 | 0.0 | 0.0 | moins bon |


![γ (portée du noyau RBF)](parametres_PED_pic_svr2_gamma_h1.png)

Amplitude de la MAE : 67.2 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### foret · nombre d'arbres

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| arbres = 25 | 1.538 | 2.047 | 0.083 | 0.5772 | 93.4 | 2.0 | 0.8615 | 1.0 | équivalent |
| arbres = 50 | 1.515 | 2.012 | 0.04 | 0.5733 | 93.4 | 3.8 | 0.8101 | 1.0 | équivalent |
| arbres = 100 | 1.521 | 2.008 | 0.046 | 0.5762 | 92.9 | 7.7 | 0.7854 | 1.0 | équivalent |
| arbres = 300 (retenu) | 1.52 | 2.011 | 0.052 | 0.575 | 94.0 | 22.4 |  |  | — choix retenu |
| arbres = 500 | 1.517 | 2.002 | 0.055 | 0.5729 | 94.0 | 37.8 | 0.3411 | 1.0 | équivalent |


![nombre d'arbres](parametres_PED_pic_foret_arbres_h1.png)

Amplitude de la MAE : 1.5 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### foret · profondeur maximale

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| profondeur_foret = 3 | 1.661 | 2.13 | 0.032 | 0.6126 | 94.5 | 2.5 | 0.0619 | 0.2476 | équivalent |
| profondeur_foret = 5 | 1.535 | 2.023 | 0.018 | 0.5832 | 92.9 | 6.6 | 0.4043 | 0.7814 | équivalent |
| profondeur_foret = 8 | 1.51 | 1.994 | 0.029 | 0.5716 | 94.0 | 16.6 | 0.3907 | 0.7814 | équivalent |
| profondeur_foret = 12 (retenu) | 1.52 | 2.011 | 0.052 | 0.575 | 94.0 | 22.3 |  |  | — choix retenu |
| profondeur_foret = 20 | 1.506 | 1.993 | 0.043 | 0.5694 | 94.5 | 22.7 | 0.0979 | 0.2937 | équivalent |


![profondeur maximale](parametres_PED_pic_foret_profondeur_foret_h1.png)

Amplitude de la MAE : 10.2 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### foret · taille minimale d'une feuille

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| min_feuille = 2 | 1.507 | 1.987 | 0.058 | 0.5571 | 93.4 | 48.1 | 0.0078 | 0.0234 | meilleur |
| min_feuille = 5 (retenu) | 1.52 | 2.011 | 0.052 | 0.575 | 94.0 | 22.4 |  |  | — choix retenu |
| min_feuille = 10 | 1.527 | 2.016 | 0.039 | 0.577 | 94.5 | 12.1 | 0.7311 | 0.7311 | équivalent |
| min_feuille = 20 | 1.56 | 2.037 | 0.038 | 0.5892 | 94.0 | 6.7 | 0.1307 | 0.2614 | équivalent |


![taille minimale d'une feuille](parametres_PED_pic_foret_min_feuille_h1.png)

Amplitude de la MAE : 3.5 %. Valeur(s) significativement meilleure(s) : min_feuille = 2 — réglage à revoir.



### foret · part des variables tirées par nœud

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| part_variables = 0,15 | 1.594 | 2.042 | 0.035 | 0.5839 | 95.6 | 20.9 | 0.5371 | 1.0 | équivalent |
| part_variables = 0,333333 (retenu) | 1.52 | 2.011 | 0.052 | 0.575 | 94.0 | 22.9 |  |  | — choix retenu |
| part_variables = 0,5 | 1.496 | 1.996 | 0.039 | 0.5622 | 92.3 | 23.4 | 0.0609 | 0.1827 | équivalent |
| part_variables = 1 | 1.5 | 2.009 | 0.033 | 0.5748 | 88.5 | 24.1 | 0.9856 | 1.0 | équivalent |


![part des variables tirées par nœud](parametres_PED_pic_foret_part_variables_h1.png)

Amplitude de la MAE : 6.4 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### boosting · nombre d'étapes

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| etapes = 50 | 1.502 | 1.991 | 0.078 | 0.5838 | 89.1 | 2.0 | 0.0586 | 0.1758 | équivalent |
| etapes = 100 | 1.402 | 1.919 | 0.07 | 0.5478 | 87.4 | 4.3 | 0.4527 | 0.9054 | équivalent |
| etapes = 300 (retenu) | 1.377 | 1.907 | 0.067 | 0.5388 | 80.3 | 12.1 |  |  | — choix retenu |
| etapes = 600 | 1.375 | 1.902 | 0.068 | 0.54 | 78.7 | 24.3 | 0.8429 | 0.9054 | équivalent |


![nombre d'étapes](parametres_PED_pic_boosting_etapes_h1.png)

Amplitude de la MAE : 9.2 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### boosting · taux ν (shrinkage)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| taux_boosting = 0,01 | 1.489 | 1.971 | 0.068 | 0.5736 | 87.4 | 12.6 | 0.0966 | 0.2079 | équivalent |
| taux_boosting = 0,05 (retenu) | 1.377 | 1.907 | 0.067 | 0.5388 | 80.3 | 12.3 |  |  | — choix retenu |
| taux_boosting = 0,1 | 1.4 | 1.89 | 0.063 | 0.5429 | 76.5 | 12.2 | 0.7171 | 0.7171 | équivalent |
| taux_boosting = 0,2 | 1.392 | 1.852 | 0.049 | 0.5665 | 71.0 | 12.1 | 0.0693 | 0.2079 | équivalent |


![taux ν (shrinkage)](parametres_PED_pic_boosting_taux_boosting_h1.png)

Amplitude de la MAE : 8.1 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### boosting · profondeur des arbres

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| profondeur_boosting = 1 | 1.462 | 1.983 | 0.042 | 0.5616 | 88.0 | 4.1 | 0.1187 | 0.3561 | équivalent |
| profondeur_boosting = 2 | 1.394 | 1.912 | 0.068 | 0.5357 | 84.2 | 7.6 | 0.7664 | 0.7664 | équivalent |
| profondeur_boosting = 3 (retenu) | 1.377 | 1.907 | 0.067 | 0.5388 | 80.3 | 13.0 |  |  | — choix retenu |
| profondeur_boosting = 5 | 1.394 | 1.896 | 0.077 | 0.5518 | 73.8 | 25.4 | 0.3168 | 0.6336 | équivalent |


![profondeur des arbres](parametres_PED_pic_boosting_profondeur_boosting_h1.png)

Amplitude de la MAE : 6.2 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### boosting · part du sous-échantillon

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| sous_echantillon = 0,5 | 1.366 | 1.86 | 0.096 | 0.5309 | 77.0 | 10.7 | 0.5507 | 0.7818 | équivalent |
| sous_echantillon = 0,8 (retenu) | 1.377 | 1.907 | 0.067 | 0.5388 | 80.3 | 13.1 |  |  | — choix retenu |
| sous_echantillon = 1 | 1.405 | 1.92 | 0.053 | 0.548 | 82.0 | 13.8 | 0.3909 | 0.7818 | équivalent |


![part du sous-échantillon](parametres_PED_pic_boosting_sous_echantillon_h1.png)

Amplitude de la MAE : 2.8 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### mlp · architecture (neurones par couche)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| couches = 8 | 1.258 | 1.72 | 0.012 | 0.47 | 90.2 | 1.8 | 0.9076 | 0.9076 | équivalent |
| couches = 32 | 1.292 | 1.732 | -0.091 | 0.5057 | 88.5 | 1.3 | 0.0141 | 0.0564 | équivalent |
| couches = 32×16 (retenu) | 1.314 | 1.761 | -0.045 | 0.4678 | 90.7 | 1.6 |  |  | — choix retenu |
| couches = 64×32 | 1.329 | 1.772 | 0.04 | 0.4956 | 87.4 | 2.1 | 0.1043 | 0.3093 | équivalent |
| couches = 32×16×8 | 1.341 | 1.738 | 0.024 | 0.4974 | 88.5 | 2.0 | 0.1031 | 0.3093 | équivalent |


![architecture (neurones par couche)](parametres_PED_pic_mlp_couches_h1.png)

Amplitude de la MAE : 6.3 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### mlp · taux d'apprentissage

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| taux_reseau = 0,001 | 1.306 | 1.794 | -0.025 | 0.4915 | 89.6 | 4.4 | 0.072 | 0.216 | équivalent |
| taux_reseau = 0,003 | 1.306 | 1.76 | -0.024 | 0.4762 | 88.5 | 2.5 | 0.4827 | 0.9654 | équivalent |
| taux_reseau = 0,01 (retenu) | 1.314 | 1.761 | -0.045 | 0.4678 | 90.7 | 1.6 |  |  | — choix retenu |
| taux_reseau = 0,03 | 1.338 | 1.754 | -0.072 | 0.4714 | 89.1 | 1.4 | 0.7819 | 0.9654 | équivalent |


![taux d'apprentissage](parametres_PED_pic_mlp_taux_reseau_h1.png)

Amplitude de la MAE : 2.4 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### mlp · pénalité L2 λ

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| lambda_ = 0 | 1.314 | 1.763 | -0.04 | 0.4689 | 88.0 | 1.6 | 0.8253 | 1.0 | équivalent |
| lambda_ = 0,0001 | 1.314 | 1.761 | -0.049 | 0.4693 | 87.4 | 1.6 | 0.7325 | 1.0 | équivalent |
| lambda_ = 0,001 (retenu) | 1.314 | 1.761 | -0.045 | 0.4678 | 90.7 | 1.6 |  |  | — choix retenu |
| lambda_ = 0,01 | 1.294 | 1.723 | -0.066 | 0.483 | 87.4 | 2.1 | 0.2086 | 0.6258 | équivalent |
| lambda_ = 0,1 | 1.368 | 1.827 | 0.024 | 0.5121 | 89.6 | 3.5 | 0.0122 | 0.0488 | moins bon |


![pénalité L2 λ](parametres_PED_pic_mlp_lambda__h1.png)

Amplitude de la MAE : 5.6 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### mlp · époques maximales

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| epoques = 300 | 1.314 | 1.761 | -0.045 | 0.4678 | 90.7 | 1.6 |  |  | identique |
| epoques = 800 | 1.314 | 1.761 | -0.045 | 0.4678 | 90.7 | 1.6 |  |  | identique |
| epoques = 1500 (retenu) | 1.314 | 1.761 | -0.045 | 0.4678 | 90.7 | 1.6 |  |  | — choix retenu |
| epoques = 3000 | 1.314 | 1.761 | -0.045 | 0.4678 | 90.7 | 1.7 |  |  | identique |


![époques maximales](parametres_PED_pic_mlp_epoques_h1.png)

Amplitude de la MAE : 0.0 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### mlp · patience de l'arrêt anticipé

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| patience = 50 | 1.312 | 1.768 | -0.058 | 0.469 | 90.7 | 0.9 | 0.6104 | 0.6104 | équivalent |
| patience = 150 (retenu) | 1.314 | 1.761 | -0.045 | 0.4678 | 90.7 | 1.6 |  |  | — choix retenu |
| patience = 300 | 1.314 | 1.761 | -0.045 | 0.4678 | 90.7 | 2.6 |  |  | identique |


![patience de l'arrêt anticipé](parametres_PED_pic_mlp_patience_h1.png)

Amplitude de la MAE : 0.2 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### mlp · nombre d'initialisations moyennées

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| graines = 1 | 1.416 | 1.895 | 0.087 | 0.5335 | 82.5 | 0.6 | 0.0012 | 0.0024 | moins bon |
| graines = 3 (retenu) | 1.314 | 1.761 | -0.045 | 0.4678 | 90.7 | 1.7 |  |  | — choix retenu |
| graines = 5 | 1.323 | 1.768 | -0.03 | 0.4719 | 88.5 | 2.7 | 0.6287 | 0.6287 | équivalent |


![nombre d'initialisations moyennées](parametres_PED_pic_mlp_graines_h1.png)

Amplitude de la MAE : 7.8 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### lstm · taille de l'état caché H

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| cache_lstm = 4 | 1.271 | 1.762 | -0.041 | 0.5028 | 89.1 | 17.7 | 0.7895 | 1.0 | équivalent |
| cache_lstm = 8 | 1.307 | 1.777 | -0.081 | 0.5016 | 87.4 | 14.1 | 0.8908 | 1.0 | équivalent |
| cache_lstm = 16 (retenu) | 1.287 | 1.761 | -0.029 | 0.5004 | 89.1 | 16.1 |  |  | — choix retenu |
| cache_lstm = 32 | 1.303 | 1.769 | -0.046 | 0.5016 | 85.8 | 30.1 | 0.8852 | 1.0 | équivalent |


![taille de l'état caché H](parametres_PED_pic_lstm_cache_lstm_h1.png)

Amplitude de la MAE : 2.8 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### lstm · taux d'apprentissage

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| taux_reseau = 0,003 | 1.299 | 1.767 | 0.003 | 0.5118 | 90.2 | 26.1 | 0.1113 | 0.2226 | équivalent |
| taux_reseau = 0,01 (retenu) | 1.287 | 1.761 | -0.029 | 0.5004 | 89.1 | 17.0 |  |  | — choix retenu |
| taux_reseau = 0,03 | 1.278 | 1.755 | -0.07 | 0.4874 | 88.5 | 15.3 | 0.1626 | 0.2226 | équivalent |


![taux d'apprentissage](parametres_PED_pic_lstm_taux_reseau_h1.png)

Amplitude de la MAE : 1.6 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### lstm · pénalité L2 λ

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| lambda_ = 0 | 1.3 | 1.771 | -0.013 | 0.5088 | 86.3 | 15.6 | 0.1611 | 0.3222 | équivalent |
| lambda_ = 0,001 (retenu) | 1.287 | 1.761 | -0.029 | 0.5004 | 89.1 | 16.4 |  |  | — choix retenu |
| lambda_ = 0,01 | 1.286 | 1.759 | -0.042 | 0.4962 | 87.4 | 36.6 | 0.6494 | 0.6494 | équivalent |


![pénalité L2 λ](parametres_PED_pic_lstm_lambda__h1.png)

Amplitude de la MAE : 1.1 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### variables · jours d'occupation passée en entrée

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| retards = 3 | 1.324 | 1.811 | -0.063 | 0.4947 | 89.6 | 12.7 | 0.7457 | 1.0 | équivalent |
| retards = 5 | 1.317 | 1.802 | -0.034 | 0.4889 | 90.2 | 12.3 | 0.2289 | 1.0 | équivalent |
| retards = 7 (retenu) | 1.336 | 1.823 | 0.039 | 0.4993 | 89.1 | 11.6 |  |  | — choix retenu |
| retards = 10 | 1.332 | 1.822 | 0.034 | 0.5033 | 88.0 | 12.8 | 0.3331 | 1.0 | équivalent |
| retards = 14 | 1.334 | 1.813 | 0.08 | 0.496 | 88.0 | 11.8 | 0.752 | 1.0 | équivalent |
| retards = 21 | 1.368 | 1.817 | 0.113 | 0.5064 | 87.4 | 10.7 | 0.6295 | 1.0 | équivalent |


![jours d'occupation passée en entrée](parametres_PED_pic_variables_retards_h1.png)

Amplitude de la MAE : 3.8 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



## Horizon J+7


### svr4 · C (poids des erreurs)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| C = 0,1 | 2.752 | 3.332 | -0.033 | 0.9204 | 91.0 | 9.3 | 0.9281 | 1.0 | équivalent |
| C = 0,3 (retenu) | 2.756 | 3.338 | -0.134 | 0.9227 | 89.3 | 9.8 |  |  | — choix retenu |
| C = 1 | 2.731 | 3.319 | -0.192 | 0.9399 | 85.3 | 11.7 | 0.4662 | 1.0 | équivalent |
| C = 3 | 2.793 | 3.41 | -0.291 | 0.955 | 83.1 | 12.6 | 0.3398 | 1.0 | équivalent |
| C = 10 | 2.971 | 3.664 | -0.351 | 1.0368 | 79.1 | 12.8 | 0.1191 | 0.4764 | équivalent |
| C = 30 | 3.21 | 3.997 | -0.52 | 1.1871 | 66.1 | 14.5 | 0.022 | 0.11 | équivalent |


![C (poids des erreurs)](parametres_PED_pic_svr4_C_h7.png)

Amplitude de la MAE : 17.4 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · ε (tube, niveaux quantiles)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| epsilon_quantile = 0 (retenu) | 2.756 | 3.338 | -0.134 | 0.9227 | 89.3 | 10.5 |  |  | — choix retenu |
| epsilon_quantile = 0,25 | 2.744 | 3.327 | -0.126 | 0.9263 | 87.6 | 10.6 | 0.668 | 1.0 | équivalent |
| epsilon_quantile = 0,5 | 2.754 | 3.337 | -0.121 | 0.9312 | 85.3 | 11.0 | 0.6045 | 1.0 | équivalent |
| epsilon_quantile = 1 | 2.766 | 3.334 | -0.182 | 0.9416 | 81.9 | 11.0 | 0.5305 | 1.0 | équivalent |


![ε (tube, niveaux quantiles)](parametres_PED_pic_svr4_epsilon_quantile_h7.png)

Amplitude de la MAE : 0.8 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · γ₁ (portée, bloc occupation)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| gamma1 = 0,01 | 2.755 | 3.337 | -0.132 | 0.9226 | 89.3 | 11.5 | 0.5733 | 0.7488 | équivalent |
| gamma1 = 0,02 (retenu) | 2.756 | 3.338 | -0.134 | 0.9227 | 89.3 | 9.8 |  |  | — choix retenu |
| gamma1 = 0,05 | 2.772 | 3.351 | -0.103 | 0.9229 | 88.7 | 8.5 | 0.3663 | 0.7488 | équivalent |
| gamma1 = 0,1 | 2.807 | 3.385 | -0.059 | 0.9234 | 88.1 | 9.4 | 0.2135 | 0.7488 | équivalent |
| gamma1 = 0,2 | 2.813 | 3.389 | -0.025 | 0.9222 | 88.1 | 5.8 | 0.1872 | 0.7488 | équivalent |
| gamma1 = 0,5 | 2.78 | 3.346 | -0.051 | 0.9221 | 88.7 | 6.5 | 0.1152 | 0.576 | équivalent |


![γ₁ (portée, bloc occupation)](parametres_PED_pic_svr4_gamma1_h7.png)

Amplitude de la MAE : 2.1 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · γ₂ (portée, bloc flux et saison)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| gamma2 = 0,02 | 2.841 | 3.458 | 0.045 | 0.9466 | 89.3 | 7.7 | 0.3192 | 0.6384 | équivalent |
| gamma2 = 0,05 | 2.791 | 3.413 | -0.107 | 0.9485 | 89.3 | 10.0 | 0.0654 | 0.2616 | équivalent |
| gamma2 = 0,1 | 2.769 | 3.369 | -0.147 | 0.9393 | 88.1 | 10.2 | 0.0884 | 0.2652 | équivalent |
| gamma2 = 0,2 (retenu) | 2.756 | 3.338 | -0.134 | 0.9227 | 89.3 | 9.1 |  |  | — choix retenu |
| gamma2 = 0,5 | 2.765 | 3.341 | -0.0 | 0.9147 | 89.8 | 9.2 | 0.7255 | 0.7255 | équivalent |


![γ₂ (portée, bloc flux et saison)](parametres_PED_pic_svr4_gamma2_h7.png)

Amplitude de la MAE : 3.1 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · τ (quantile décisionnel)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| tau = 0,5 | 2.756 | 3.338 | -0.134 | 1.4183 | 89.3 | 6.3 | 0.0091 | 0.0364 | moins bon |
| tau = 0,6 | 2.756 | 3.338 | -0.134 | 1.4183 | 89.3 | 8.4 | 0.0091 | 0.0364 | moins bon |
| tau = 0,7 | 2.756 | 3.338 | -0.134 | 1.4183 | 89.3 | 9.3 | 0.0091 | 0.0364 | moins bon |
| tau = 0,8 (retenu) | 2.756 | 3.338 | -0.134 | 0.9227 | 89.3 | 9.3 |  |  | — choix retenu |
| tau = 0,9 | 2.756 | 3.338 | -0.134 | 1.4183 | 89.3 | 9.2 | 0.0091 | 0.0364 | moins bon |


![τ (quantile décisionnel)](parametres_PED_pic_svr4_tau_h7.png)

Amplitude de la MAE : 0.0 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · η₀ (taux d'apprentissage d'Adam)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| taux = 0,005 | 2.759 | 3.341 | -0.13 | 0.9242 | 88.7 | 14.7 | 0.4112 | 1.0 | équivalent |
| taux = 0,01 | 2.757 | 3.338 | -0.131 | 0.9233 | 89.3 | 15.2 | 0.5027 | 1.0 | équivalent |
| taux = 0,02 | 2.756 | 3.338 | -0.132 | 0.9229 | 89.3 | 11.9 | 0.4459 | 1.0 | équivalent |
| taux = 0,05 (retenu) | 2.756 | 3.338 | -0.134 | 0.9227 | 89.3 | 9.6 |  |  | — choix retenu |
| taux = 0,1 | 2.757 | 3.339 | -0.132 | 0.9229 | 89.3 | 9.9 | 0.1748 | 0.6992 | équivalent |
| taux = 0,2 | 2.758 | 3.339 | -0.131 | 0.9236 | 89.3 | 7.6 | 0.1067 | 0.5335 | équivalent |


![η₀ (taux d'apprentissage d'Adam)](parametres_PED_pic_svr4_taux_h7.png)

Amplitude de la MAE : 0.1 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · nombre maximal d'itérations

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| iterations = 300 | 2.757 | 3.339 | -0.13 | 0.9282 | 90.4 | 1.5 | 0.2549 | 0.7647 | équivalent |
| iterations = 1000 | 2.756 | 3.338 | -0.133 | 0.9239 | 89.3 | 4.2 | 0.5178 | 1.0 | équivalent |
| iterations = 3000 (retenu) | 2.756 | 3.338 | -0.134 | 0.9227 | 89.3 | 9.5 |  |  | — choix retenu |
| iterations = 6000 | 2.756 | 3.338 | -0.134 | 0.9228 | 89.3 | 14.3 | 0.9242 | 1.0 | équivalent |


![nombre maximal d'itérations](parametres_PED_pic_svr4_iterations_h7.png)

Amplitude de la MAE : 0.0 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · T (décroissance du pas ; aucune = pas constant)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| decroissance = aucune | 2.756 | 3.337 | -0.133 | 0.9226 | 89.3 | 11.8 | 0.7525 | 1.0 | équivalent |
| decroissance = 100 | 2.757 | 3.338 | -0.133 | 0.9231 | 89.3 | 9.7 | 0.3661 | 1.0 | équivalent |
| decroissance = 500 (retenu) | 2.756 | 3.338 | -0.134 | 0.9227 | 89.3 | 9.8 |  |  | — choix retenu |
| decroissance = 2000 | 2.756 | 3.338 | -0.134 | 0.9226 | 89.3 | 10.2 | 0.4868 | 1.0 | équivalent |


![T (décroissance du pas ; aucune = pas constant)](parametres_PED_pic_svr4_decroissance_h7.png)

Amplitude de la MAE : 0.0 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · part des pas moyennée (Polyak ; 0 = aucune)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| moyenne_polyak = 0 | 2.756 | 3.338 | -0.134 | 0.9227 | 89.3 | 8.7 |  |  | identique |
| moyenne_polyak = 0,25 | 2.756 | 3.338 | -0.134 | 0.9227 | 89.3 | 9.1 |  |  | identique |
| moyenne_polyak = 0,5 (retenu) | 2.756 | 3.338 | -0.134 | 0.9227 | 89.3 | 8.2 |  |  | — choix retenu |
| moyenne_polyak = 0,75 | 2.756 | 3.338 | -0.134 | 0.9227 | 89.3 | 8.1 |  |  | identique |


![part des pas moyennée (Polyak ; 0 = aucune)](parametres_PED_pic_svr4_moyenne_polyak_h7.png)

Amplitude de la MAE : 0.0 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · tolérance d'arrêt anticipé

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| tolerance = 1e-05 | 2.757 | 3.339 | -0.133 | 0.9228 | 89.3 | 8.0 | 0.1649 | 0.1649 | équivalent |
| tolerance = 1e-07 (retenu) | 2.756 | 3.338 | -0.134 | 0.9227 | 89.3 | 8.7 |  |  | — choix retenu |
| tolerance = 1e-09 | 2.755 | 3.337 | -0.132 | 0.9227 | 89.3 | 12.0 |  |  | identique |


![tolérance d'arrêt anticipé](parametres_PED_pic_svr4_tolerance_h7.png)

Amplitude de la MAE : 0.1 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · direction préconditionnée α + Cg

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| preconditionne = True (retenu) | 2.756 | 3.338 | -0.134 | 0.9227 | 89.3 | 8.2 |  |  | — choix retenu |
| preconditionne = False | 2.766 | 3.348 | -0.104 | 0.9236 | 89.3 | 14.3 | 0.1943 | 0.1943 | équivalent |


![direction préconditionnée α + Cg](parametres_PED_pic_svr4_preconditionne_h7.png)

Amplitude de la MAE : 0.4 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr4 · optimiseur

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| optimiseur = adam (retenu) | 2.756 | 3.338 | -0.134 | 0.9227 | 89.3 | 8.9 |  |  | — choix retenu |
| optimiseur = momentum | 2.755 | 3.337 | -0.133 | 0.9224 | 89.3 | 4.8 | 0.6087 | 0.6087 | équivalent |
| optimiseur = sgd | 2.759 | 3.341 | -0.131 | 0.9223 | 89.3 | 6.0 | 0.21 | 0.42 | équivalent |


![optimiseur](parametres_PED_pic_svr4_optimiseur_h7.png)

Amplitude de la MAE : 0.1 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr2 · C

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| C = 0,1 | 2.775 | 3.341 | 0.053 | 1.3718 | 0.3 | 0.2531 | 1.0 | équivalent |
| C = 0,3 (retenu) | 2.809 | 3.36 | 0.022 | 1.3979 | 0.4 |  |  | — choix retenu |
| C = 1 | 2.871 | 3.402 | -0.033 | 1.4453 | 0.6 | 0.1786 | 0.893 | équivalent |
| C = 3 | 3.006 | 3.559 | 0.123 | 1.466 | 1.2 | 0.3374 | 1.0 | équivalent |
| C = 10 | 3.144 | 3.792 | 0.329 | 1.4734 | 1.8 | 0.4011 | 1.0 | équivalent |
| C = 30 | 3.198 | 3.881 | 0.417 | 1.4739 | 1.8 | 0.4124 | 1.0 | équivalent |


![C](parametres_PED_pic_svr2_C_h7.png)

Amplitude de la MAE : 15.1 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr2 · ε (tube ε-insensible, en lits)

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| epsilon = 0 | 2.819 | 3.367 | 0.085 | 1.384 | 0.3 | 0.1594 | 0.2046 | équivalent |
| epsilon = 0,25 | 2.816 | 3.368 | 0.086 | 1.3821 | 0.3 | 0.0514 | 0.1542 | équivalent |
| epsilon = 0,5 | 2.809 | 3.36 | 0.056 | 1.3876 | 0.4 | 0.0223 | 0.0892 | équivalent |
| epsilon = 1 (retenu) | 2.809 | 3.36 | 0.022 | 1.3979 | 0.4 |  |  | — choix retenu |
| epsilon = 2 | 2.816 | 3.375 | 0.086 | 1.3821 | 0.3 | 0.1023 | 0.2046 | équivalent |


![ε (tube ε-insensible, en lits)](parametres_PED_pic_svr2_epsilon_h7.png)

Amplitude de la MAE : 0.4 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### svr2 · γ (portée du noyau RBF)

| variante | MAE | RMSE | biais | pinball τ=0.8 | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|
| gamma = 0,005 | 2.821 | 3.441 | -0.09 | 1.4377 | 0.4 | 0.391 | 0.5121 | équivalent |
| gamma = 0,01 | 2.842 | 3.469 | -0.124 | 1.4581 | 0.4 | 0.2246 | 0.5121 | équivalent |
| gamma = 0,02 | 2.849 | 3.472 | -0.117 | 1.4598 | 0.5 | 0.1707 | 0.5121 | équivalent |
| gamma = 0,05 | 2.846 | 3.435 | -0.108 | 1.4553 | 0.4 | 0.0706 | 0.312 | équivalent |
| gamma = 0,1 | 2.834 | 3.393 | -0.08 | 1.4409 | 0.3 | 0.0076 | 0.0456 | moins bon |
| gamma = 0,2 (retenu) | 2.809 | 3.36 | 0.022 | 1.3979 | 0.4 |  |  | — choix retenu |
| gamma = 0,5 | 2.769 | 3.335 | 0.147 | 1.3406 | 0.3 | 0.0624 | 0.312 | équivalent |


![γ (portée du noyau RBF)](parametres_PED_pic_svr2_gamma_h7.png)

Amplitude de la MAE : 2.8 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### foret · nombre d'arbres

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| arbres = 25 | 2.869 | 3.442 | -0.304 | 0.9957 | 89.3 | 1.8 | 0.5957 | 1.0 | équivalent |
| arbres = 50 | 2.797 | 3.373 | -0.26 | 1.0054 | 88.7 | 3.5 | 0.9666 | 1.0 | équivalent |
| arbres = 100 | 2.83 | 3.386 | -0.198 | 1.0066 | 89.3 | 7.1 | 0.8071 | 1.0 | équivalent |
| arbres = 300 (retenu) | 2.847 | 3.387 | -0.195 | 1.0049 | 90.4 | 20.7 |  |  | — choix retenu |
| arbres = 500 | 2.854 | 3.388 | -0.181 | 1.0071 | 89.8 | 34.4 | 0.6911 | 1.0 | équivalent |


![nombre d'arbres](parametres_PED_pic_foret_arbres_h7.png)

Amplitude de la MAE : 2.5 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### foret · profondeur maximale

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| profondeur_foret = 3 | 2.804 | 3.394 | -0.133 | 0.9822 | 92.1 | 2.5 | 0.4935 | 0.987 | équivalent |
| profondeur_foret = 5 | 2.819 | 3.379 | -0.2 | 0.9728 | 91.5 | 6.0 | 0.1267 | 0.5068 | équivalent |
| profondeur_foret = 8 | 2.842 | 3.384 | -0.216 | 0.9847 | 89.8 | 13.3 | 0.1291 | 0.5068 | équivalent |
| profondeur_foret = 12 (retenu) | 2.847 | 3.387 | -0.195 | 1.0049 | 90.4 | 20.9 |  |  | — choix retenu |
| profondeur_foret = 20 | 2.843 | 3.368 | -0.186 | 0.999 | 90.4 | 23.3 | 0.5514 | 0.987 | équivalent |


![profondeur maximale](parametres_PED_pic_foret_profondeur_foret_h7.png)

Amplitude de la MAE : 1.5 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### foret · taille minimale d'une feuille

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| min_feuille = 2 | 2.906 | 3.427 | -0.184 | 1.0297 | 91.0 | 40.7 | 0.0763 | 0.2289 | équivalent |
| min_feuille = 5 (retenu) | 2.847 | 3.387 | -0.195 | 1.0049 | 90.4 | 21.2 |  |  | — choix retenu |
| min_feuille = 10 | 2.837 | 3.404 | -0.214 | 0.9978 | 89.3 | 12.3 | 0.3587 | 0.3587 | équivalent |
| min_feuille = 20 | 2.857 | 3.428 | -0.219 | 0.9815 | 89.3 | 7.0 | 0.1788 | 0.3576 | équivalent |


![taille minimale d'une feuille](parametres_PED_pic_foret_min_feuille_h7.png)

Amplitude de la MAE : 2.4 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### foret · part des variables tirées par nœud

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| part_variables = 0,15 | 2.871 | 3.424 | -0.124 | 0.9922 | 92.7 | 19.6 | 0.3481 | 1.0 | équivalent |
| part_variables = 0,333333 (retenu) | 2.847 | 3.387 | -0.195 | 1.0049 | 90.4 | 20.9 |  |  | — choix retenu |
| part_variables = 0,5 | 2.865 | 3.393 | -0.23 | 1.0034 | 88.7 | 21.6 | 0.875 | 1.0 | équivalent |
| part_variables = 1 | 2.853 | 3.374 | -0.253 | 1.0044 | 88.1 | 23.4 | 0.9775 | 1.0 | équivalent |


![part des variables tirées par nœud](parametres_PED_pic_foret_part_variables_h7.png)

Amplitude de la MAE : 0.8 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### boosting · nombre d'étapes

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| etapes = 50 | 2.808 | 3.392 | -0.172 | 0.9603 | 84.2 | 2.1 | 0.2336 | 0.3156 | équivalent |
| etapes = 100 | 2.84 | 3.41 | -0.218 | 0.9739 | 82.5 | 4.1 | 0.1549 | 0.3156 | équivalent |
| etapes = 300 (retenu) | 2.867 | 3.416 | -0.205 | 1.0127 | 76.3 | 11.9 |  |  | — choix retenu |
| etapes = 600 | 2.892 | 3.441 | -0.187 | 1.0528 | 74.6 | 23.2 | 0.1052 | 0.3156 | équivalent |


![nombre d'étapes](parametres_PED_pic_boosting_etapes_h7.png)

Amplitude de la MAE : 2.9 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### boosting · taux ν (shrinkage)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| taux_boosting = 0,01 | 2.818 | 3.371 | -0.142 | 0.9928 | 84.2 | 11.9 | 0.6072 | 0.7458 | équivalent |
| taux_boosting = 0,05 (retenu) | 2.867 | 3.416 | -0.205 | 1.0127 | 76.3 | 11.4 |  |  | — choix retenu |
| taux_boosting = 0,1 | 2.875 | 3.446 | -0.247 | 1.0433 | 72.3 | 11.3 | 0.295 | 0.7458 | équivalent |
| taux_boosting = 0,2 | 2.861 | 3.515 | -0.397 | 1.0756 | 72.9 | 11.9 | 0.2486 | 0.7458 | équivalent |


![taux ν (shrinkage)](parametres_PED_pic_boosting_taux_boosting_h7.png)

Amplitude de la MAE : 2.0 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### boosting · profondeur des arbres

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| profondeur_boosting = 1 | 2.851 | 3.459 | -0.208 | 0.9952 | 80.2 | 4.1 | 0.6774 | 1.0 | équivalent |
| profondeur_boosting = 2 | 2.828 | 3.398 | -0.251 | 1.0082 | 79.7 | 7.5 | 0.8521 | 1.0 | équivalent |
| profondeur_boosting = 3 (retenu) | 2.867 | 3.416 | -0.205 | 1.0127 | 76.3 | 11.5 |  |  | — choix retenu |
| profondeur_boosting = 5 | 2.87 | 3.444 | -0.048 | 1.0519 | 71.2 | 23.4 | 0.311 | 0.933 | équivalent |


![profondeur des arbres](parametres_PED_pic_boosting_profondeur_boosting_h7.png)

Amplitude de la MAE : 1.5 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### boosting · part du sous-échantillon

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| sous_echantillon = 0,5 | 2.855 | 3.429 | -0.456 | 1.0177 | 74.0 | 10.4 | 0.8521 | 1.0 | équivalent |
| sous_echantillon = 0,8 (retenu) | 2.867 | 3.416 | -0.205 | 1.0127 | 76.3 | 11.6 |  |  | — choix retenu |
| sous_echantillon = 1 | 2.863 | 3.371 | -0.138 | 1.0153 | 78.0 | 12.3 | 0.9244 | 1.0 | équivalent |


![part du sous-échantillon](parametres_PED_pic_boosting_sous_echantillon_h7.png)

Amplitude de la MAE : 0.4 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### mlp · architecture (neurones par couche)

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| couches = 8 | 2.887 | 3.478 | -0.177 | 0.9287 | 84.2 | 0.8 | 0.1174 | 0.4696 | équivalent |
| couches = 32 | 2.868 | 3.472 | -0.41 | 0.9906 | 84.7 | 1.0 | 0.4395 | 0.879 | équivalent |
| couches = 32×16 (retenu) | 2.865 | 3.51 | -0.323 | 1.029 | 85.3 | 1.2 |  |  | — choix retenu |
| couches = 64×32 | 2.852 | 3.503 | -0.67 | 1.033 | 85.9 | 1.7 | 0.9164 | 0.9164 | équivalent |
| couches = 32×16×8 | 2.828 | 3.416 | 0.227 | 0.934 | 81.4 | 1.5 | 0.1274 | 0.4696 | équivalent |


![architecture (neurones par couche)](parametres_PED_pic_mlp_couches_h7.png)

Amplitude de la MAE : 2.1 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### mlp · taux d'apprentissage

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| taux_reseau = 0,001 | 2.847 | 3.527 | -0.104 | 1.0269 | 80.2 | 2.4 | 0.9609 | 0.9609 | équivalent |
| taux_reseau = 0,003 | 2.833 | 3.494 | -0.198 | 0.9987 | 83.6 | 1.6 | 0.2208 | 0.6624 | équivalent |
| taux_reseau = 0,01 (retenu) | 2.865 | 3.51 | -0.323 | 1.029 | 85.3 | 1.3 |  |  | — choix retenu |
| taux_reseau = 0,03 | 2.847 | 3.467 | -0.237 | 1.0142 | 86.4 | 1.2 | 0.4145 | 0.829 | équivalent |


![taux d'apprentissage](parametres_PED_pic_mlp_taux_reseau_h7.png)

Amplitude de la MAE : 1.1 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### mlp · pénalité L2 λ

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| lambda_ = 0 | 2.828 | 3.484 | -0.28 | 1.0163 | 85.9 | 1.3 | 0.2602 | 1.0 | équivalent |
| lambda_ = 0,0001 | 2.836 | 3.493 | -0.285 | 1.0186 | 86.4 | 1.3 | 0.3495 | 1.0 | équivalent |
| lambda_ = 0,001 (retenu) | 2.865 | 3.51 | -0.323 | 1.029 | 85.3 | 1.3 |  |  | — choix retenu |
| lambda_ = 0,01 | 2.869 | 3.517 | -0.318 | 1.0478 | 83.1 | 1.3 | 0.4534 | 1.0 | équivalent |
| lambda_ = 0,1 | 2.85 | 3.467 | 0.085 | 0.9904 | 84.2 | 3.5 | 0.5765 | 1.0 | équivalent |


![pénalité L2 λ](parametres_PED_pic_mlp_lambda__h7.png)

Amplitude de la MAE : 1.4 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### mlp · époques maximales

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| epoques = 300 | 2.865 | 3.51 | -0.323 | 1.029 | 85.3 | 1.3 |  |  | identique |
| epoques = 800 | 2.865 | 3.51 | -0.323 | 1.029 | 85.3 | 1.2 |  |  | identique |
| epoques = 1500 (retenu) | 2.865 | 3.51 | -0.323 | 1.029 | 85.3 | 1.2 |  |  | — choix retenu |
| epoques = 3000 | 2.865 | 3.51 | -0.323 | 1.029 | 85.3 | 1.2 |  |  | identique |


![époques maximales](parametres_PED_pic_mlp_epoques_h7.png)

Amplitude de la MAE : 0.0 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### mlp · patience de l'arrêt anticipé

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| patience = 50 | 2.865 | 3.51 | -0.323 | 1.029 | 85.3 | 0.6 |  |  | identique |
| patience = 150 (retenu) | 2.865 | 3.51 | -0.323 | 1.029 | 85.3 | 1.2 |  |  | — choix retenu |
| patience = 300 | 2.865 | 3.51 | -0.323 | 1.029 | 85.3 | 2.3 |  |  | identique |


![patience de l'arrêt anticipé](parametres_PED_pic_mlp_patience_h7.png)

Amplitude de la MAE : 0.0 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### mlp · nombre d'initialisations moyennées

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| graines = 1 | 2.841 | 3.53 | -0.355 | 1.1446 | 85.3 | 0.5 | 0.0036 | 0.0072 | moins bon |
| graines = 3 (retenu) | 2.865 | 3.51 | -0.323 | 1.029 | 85.3 | 1.3 |  |  | — choix retenu |
| graines = 5 | 2.806 | 3.425 | -0.313 | 0.9615 | 85.9 | 2.0 | 0.0869 | 0.0869 | équivalent |


![nombre d'initialisations moyennées](parametres_PED_pic_mlp_graines_h7.png)

Amplitude de la MAE : 2.1 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### lstm · taille de l'état caché H

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| cache_lstm = 4 | 2.905 | 3.559 | 0.131 | 1.0394 | 87.0 | 6.3 | 0.8352 | 1.0 | équivalent |
| cache_lstm = 8 | 3.058 | 3.68 | -0.062 | 1.0329 | 80.2 | 9.7 | 0.6125 | 1.0 | équivalent |
| cache_lstm = 16 (retenu) | 3.035 | 3.644 | -0.105 | 1.05 | 80.2 | 15.8 |  |  | — choix retenu |
| cache_lstm = 32 | 3.069 | 3.684 | -0.25 | 1.0954 | 82.5 | 19.7 | 0.2916 | 0.8748 | équivalent |


![taille de l'état caché H](parametres_PED_pic_lstm_cache_lstm_h7.png)

Amplitude de la MAE : 5.4 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### lstm · taux d'apprentissage

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| taux_reseau = 0,003 | 2.968 | 3.571 | -0.137 | 1.0131 | 83.1 | 15.0 | 0.2497 | 0.4994 | équivalent |
| taux_reseau = 0,01 (retenu) | 3.035 | 3.644 | -0.105 | 1.05 | 80.2 | 14.7 |  |  | — choix retenu |
| taux_reseau = 0,03 | 3.022 | 3.638 | -0.231 | 1.0739 | 81.9 | 10.3 | 0.4978 | 0.4994 | équivalent |


![taux d'apprentissage](parametres_PED_pic_lstm_taux_reseau_h7.png)

Amplitude de la MAE : 2.2 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### lstm · pénalité L2 λ

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| lambda_ = 0 | 2.977 | 3.594 | -0.047 | 1.0197 | 82.5 | 11.2 | 0.3782 | 0.6266 | équivalent |
| lambda_ = 0,001 (retenu) | 3.035 | 3.644 | -0.105 | 1.05 | 80.2 | 15.3 |  |  | — choix retenu |
| lambda_ = 0,01 | 2.959 | 3.579 | -0.16 | 1.0072 | 81.9 | 12.2 | 0.3133 | 0.6266 | équivalent |


![pénalité L2 λ](parametres_PED_pic_lstm_lambda__h7.png)

Amplitude de la MAE : 2.5 %. Aucune valeur ne fait significativement mieux que la valeur retenue.



### variables · jours d'occupation passée en entrée

| variante | MAE | RMSE | biais | pinball τ=0.8 | couverture 90 % | temps (s) | DM p (pinball τ=0.8) | p Holm | vs choix retenu |
|---|---|---|---|---|---|---|---|---|---|
| retards = 3 | 2.756 | 3.337 | -0.133 | 0.9226 | 89.3 | 8.7 | 0.7196 | 1.0 | équivalent |
| retards = 5 | 2.756 | 3.338 | -0.134 | 0.9226 | 89.3 | 7.9 | 0.6397 | 1.0 | équivalent |
| retards = 7 (retenu) | 2.756 | 3.338 | -0.134 | 0.9227 | 89.3 | 8.4 |  |  | — choix retenu |
| retards = 10 | 2.774 | 3.356 | -0.103 | 0.9223 | 89.3 | 8.2 | 0.3137 | 1.0 | équivalent |
| retards = 14 | 2.777 | 3.339 | -0.078 | 0.9207 | 89.8 | 6.3 | 0.1716 | 0.858 | équivalent |
| retards = 21 | 2.766 | 3.311 | 0.005 | 0.9141 | 89.8 | 5.3 | 0.4636 | 1.0 | équivalent |


![jours d'occupation passée en entrée](parametres_PED_pic_variables_retards_h7.png)

Amplitude de la MAE : 0.8 %. Aucune valeur ne fait significativement mieux que la valeur retenue.

