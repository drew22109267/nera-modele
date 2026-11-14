# Triage — test final

Trois niveaux de priorité : grave (rouge), moyen = MEO (jaune), non grave (vert). Priorité donnée = plus petit coût attendu, matrice c(i, j) = 4 × (i − j) en sous-triage, (j − i) en sur-triage. Mesures sur les passages jamais vus.


## Enfant

| banc | variante | passages | graves | moyens | non_graves | graves_en_rouge | graves_sous_tries | moyens_en_jaune | non_graves_en_vert | sous_triage | sur_triage | rouges | jaunes | exactitude | kappa_pondere | cout_moyen | auc_haut | auc_bas | spec_sens90 | brier3 | sens_s90 | spec_s90 | alertes_s90 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| principal | modèle principal | 90 | 29 | 20 | 41 | 0.586 | 0.414 | 0.25 | 0.122 | 0.156 | 0.544 | 0.422 | 0.5 | 0.3 | 0.294 | 1.256 | 0.704 | 0.669 | 0.361 | 0.648 | 0.828 | 0.475 | 0.622 |

## Adulte

| banc | variante | passages | graves | moyens | non_graves | graves_en_rouge | graves_sous_tries | moyens_en_jaune | non_graves_en_vert | sous_triage | sur_triage | rouges | jaunes | exactitude | kappa_pondere | cout_moyen | auc_haut | auc_bas | spec_sens90 | brier3 | sens_s90 | spec_s90 | alertes_s90 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| principal | modèle principal | 346 | 83 | 109 | 154 | 0.988 | 0.012 | 0.046 | 0.013 | 0.003 | 0.74 | 0.936 | 0.058 | 0.257 | 0.035 | 1.15 | 0.67 | 0.75 | 0.289 | 0.747 | 0.988 | 0.053 | 0.957 |

## Raccordement : enfants et adultes réunis, tous les passages des urgences

Modèles séparés (chacun sur son groupe) réunis, comparés au modèle commun sur les mêmes passages.

| banc | variante | passages | graves | moyens | non_graves | graves_en_rouge | graves_sous_tries | moyens_en_jaune | non_graves_en_vert | sous_triage | sur_triage | rouges | jaunes | exactitude | kappa_pondere | cout_moyen | auc_haut | auc_bas | spec_sens90 | brier3 | mcnemar_p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| raccordement | modèles séparés réunis (référence) | 436 | 112 | 129 | 195 | 0.884 | 0.116 | 0.078 | 0.036 | 0.034 | 0.7 | 0.83 | 0.149 | 0.266 | 0.067 | 1.172 | 0.626 | 0.692 | 0.17 | 0.727 |  |
| raccordement | modèle commun enfants + adultes | 436 | 112 | 129 | 195 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.743 | 1.0 | 0.0 | 0.257 | 0.0 | 1.19 | 0.624 | 0.731 | 0.182 | 0.806 | 0.584 |
| raccordement | dont enfant : modèle séparé | 90 | 29 | 20 | 41 | 0.586 | 0.414 | 0.25 | 0.122 | 0.156 | 0.544 | 0.422 | 0.5 | 0.3 | 0.294 | 1.256 | 0.704 | 0.669 | 0.361 | 0.648 |  |
| raccordement | dont enfant : modèle commun | 90 | 29 | 20 | 41 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.678 | 1.0 | 0.0 | 0.322 | 0.0 | 1.133 | 0.653 | 0.664 | 0.197 | 0.745 |  |
| raccordement | dont adulte : modèle séparé | 346 | 83 | 109 | 154 | 0.988 | 0.012 | 0.046 | 0.013 | 0.003 | 0.74 | 0.936 | 0.058 | 0.257 | 0.035 | 1.15 | 0.67 | 0.75 | 0.289 | 0.747 |  |
| raccordement | dont adulte : modèle commun | 346 | 83 | 109 | 154 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.76 | 1.0 | 0.0 | 0.24 | 0.0 | 1.205 | 0.628 | 0.758 | 0.156 | 0.822 |  |
