# Résultats du 13/11/2026 : équivalence puis calcul complet de développement

Calcul de **développement** : la validation finale n'a pas été lancée (ni `validation_finale.py`, ni
`--confirmation`, ni `--extraction`). Les registres de patients ne sont pas dans ce dépôt.

## Code et réglages

- Calcul complet : `main` **abe05ba** (= 11e164b + avertissement du calendrier), outil-saisi `main` **28e39ce**.
- Module lit : `lancer_tout.sh` avec `ETAPES="0 1 2 3 4 5 6 7 8 9 10"`, puis `"9 11 12"` ; comptages minuit, pic,
  journée ; horizons 1 et 7 jours ; `OMP_NUM_THREADS=1`.
- Triage : `lancer_triage.py registre-urg.csv --source-externe passages_nhamcs.csv.gz` (coffre par défaut au
  01/01/2026 ; NHAMCS-ED 2015-2022 pour le banc T9), triage à trois niveaux.
- Fériés et vacances : `feries_supplementaires.csv` et `vacances_scolaires.csv` reconstitués depuis
  `outil-saisie/calendrier.js` (aucune date ajoutée).
- Machine AWS eu-north-1 : m7g.8xlarge (32 cœurs). Calcul complet fini le 13/11 à 21:44 UTC, **0 échec**.

## Contenu

- `complet/` : `module_lit/` (rapports `.md`, tableaux de scores `.csv`, réglages `.json`, figures, journaux),
  `module_triage/triage/` (rapport, bancs, choix retenus, sélection), `journaux/` (sorties des lanceurs).
- `equivalence/` : `ancien/` (main e2bcc17) et `nouveau/` (abe05ba), pédiatrie au comptage minuit (occupation,
  niveaux, banc des choix) et triage enfants ; **`EQUIVALENCE.md`** donne la comparaison.

## Équivalence (résumé)

Module lit identique (occupation et niveaux à l'octet ; dans le banc des choix, seule la durée de calcul diffère).
Triage : écarts uniquement là où 11e164b change la méthode (banc T9, colonnes `spec_s90_*`, règle de sélection :
modèle retenu T10 → T11, avec des mesures identiques pour ces deux lignes). Aucun écart inexpliqué.

## Fichiers volontairement absents (données par jour ou par passage)

Ils restent dans le stockage chiffré privé : `module_triage/triage/passages_*.csv` et `probabilites_*.csv`,
`module_lit/occupation_*.csv`, `module_lit/lien_triage_PED*_series.csv`.
