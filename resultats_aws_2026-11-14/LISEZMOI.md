# Validation finale, 14/11/2026

Code : nera-modele main abe05ba, outil-saisi main 28e39ce. Choix figés du calcul du 13/11 (hyperparamètres,
sélections, choix retenus du triage), aucun réglage modifié. Machine AWS m7g.8xlarge à la demande, ~40 min.

## Deux ouvertures du coffre (journalisées dans coffre_ouvertures.log)
1. 12:36 UTC, `--extraction 2026-10-31` pour les deux services : **invalide pour octobre**. Le registre PED
   s'arrête le 30/09/2026 et le MEDF le 20/10/2026 ; les jours suivants ont été comptés à 0 lit occupé.
   Conservé dans `passage1_extraction_2026-10-31/` pour trace.
2. 13:08 UTC, dates réelles : PED `2026-09-30`, MEDF `2026-10-20` (transfert : date de la cible). Mêmes modèles,
   mêmes réglages ; seule la période évaluée change. **Résultats de référence : `passage2_extractions_reelles/`.**

Triage : une seule ouverture (12:36 UTC), `--utiliser-selection --extraction 2026-01-25` (coffre du triage :
01/01 au 25/01/2026), résultats dans `triage/`.

## Module lit (passage 2, réentraînement mensuel) : MAE, persistance contre meilleur modèle
| série | h | persistance | meilleur modèle | MAE |
|---|---|---|---|---|
| PED minuit | 1 | 1.49 | 5 · empilement | 1.45 |
| PED minuit | 7 | 2.58 | 1 · SVR linéaire | 2.63 |
| PED pic | 1 | 1.37 | 1 · SVR linéaire | 1.19 |
| PED pic | 7 | 2.58 | 1 · SVR linéaire | 2.48 |
| PED journée | 1 | 2.46 | 1 · SVR linéaire | 1.78 |
| PED journée | 7 | 3.04 | 2 · SVR RBF | 2.70 |
| MEDF minuit | 1 | 2.25 | 1 · SVR linéaire | 1.92 |
| MEDF minuit | 7 | 3.43 | 5 · empilement | 2.64 |
| MEDF pic | 1 | 1.70 | 1 · SVR linéaire | 1.47 |
| MEDF pic | 7 | 3.13 | 5 · empilement | 2.54 |
| MEDF journée | 1 | 2.49 | 1 · SVR linéaire | 2.10 |
| MEDF journée | 7 | 3.26 | 5 · empilement | 2.59 |

PED : septembre seul (registre arrêté au 30/09). MEDF : septembre + 1er au 20 octobre. Tests de Diebold-Mariano :
`validation_finale_*_tests.csv`. Variante sans réentraînement : fichiers `*_sans_reentrainement`.

## Triage (test final, janvier 2026)
- Enfants (90 passages) : graves en rouge 0.586, sous-triage 0.156, kappa pondéré 0.294, AUC grave 0.704.
- Adultes (346) : graves en rouge 0.988, sous-triage 0.003, mais sur-triage 0.74 (93.6 % en rouge), kappa 0.035.
- Modèle commun enfants + adultes : tout en rouge (kappa 0) ; modèles séparés meilleurs.

## Fichiers volontairement absents (données par jour ou par passage)
`triage/passages_*.csv` et `triage/probabilites_*.csv` restent dans le stockage chiffré privé.
