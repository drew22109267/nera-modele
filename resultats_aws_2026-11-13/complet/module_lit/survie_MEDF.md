# Modèle de survie J0/J1/J2 — MEDF

Validation : 2477 jours-patients, 182 matins. « (retenu) » = modèle retenu. Brier et log-loss : plus petit = meilleur ; AUC : plus grand = meilleur ; MAE J0/J1/J2 : écart moyen entre sorties attendues et réelles par jour.

| modèle | Brier | log-loss | AUC | MAE J0 (sorties/jour) | MAE J1 (sorties/jour) | MAE J2 (sorties/jour) | biais J0 |
|---|---|---|---|---|---|---|---|
| Table de survie (ancienneté seule) | 0.1487 | 0.5033 | 0.698 | 1.51 | 1.509 | 1.365 | -0.174 |
| Loi gamma de la durée (a = 1.89, θ = 2.31) | 0.1518 | 0.4719 | 0.657 | 1.563 | 1.485 | 1.35 | -0.001 |
| SVM linéaire, coûts symétriques + Platt | 0.1535 | 0.4818 | 0.72 | 1.486 | 1.408 | 1.274 | 0.214 |
| SVM linéaire, coûts asymétriques C+/C− = 3.9 + Platt (retenu) | 0.1423 | 0.4456 | 0.741 | 1.242 | 1.245 | 1.109 | 0.078 |
| SVM par cause (risques concurrents), somme des hasards | 0.1424 | 0.4459 | 0.732 | 1.24 | 1.222 | 1.085 | 0.222 |


Meilleur score de Brier : **SVM linéaire, coûts asymétriques C+/C− = 3.9 + Platt (retenu)**.


## Par cause de sortie

| cause | sorties réelles | sorties attendues |
|---|---|---|
| autre | 80.0 | 84.5 |
| domicile | 359.8 | 366.6 |

