# Résultats du calcul complet NERA (10/11/2026)

Calcul de **développement** (la validation finale n'a pas été lancée : ni `validation_finale.py`, ni
`--confirmation`, ni `--extraction`).

## Code et réglages

- Code : branche `pytorch-optimisation`, commit `911e453` pour le calcul principal, `4933535` pour l'étape 11
  (lien triage → lits) refaite après correction.
- Module lit : `lancer_tout.sh` avec `ETAPES="0 1 2 3 4 5 6 7 8 9 10"`, puis `"9 11 12"` ; comptages minuit, pic,
  journée ; horizons 1 et 7 jours ; `OMP_NUM_THREADS=1`.
- Triage : `lancer_triage.py registre-urg.csv --source-externe passages_nhamcs.csv.gz --fin-developpement 2026-01-01`
  (NHAMCS-ED 2015-2022 pour le banc T9).
- Machines AWS (eu-north-1) : m7g.8xlarge (32 cœurs) pour le calcul principal, 05:30 → 08:51 UTC ;
  c7g.xlarge pour l'étape 11 refaite, 09:16 → 09:29 UTC.

## Contenu

- `module_lit/` : rapports `.md`, tableaux de scores `.csv`, réglages `.json`, figures, journaux.
- `module_triage/triage/` : rapport du triage, bancs, choix retenus, sélection lasso.
- `journaux/` : journaux d'exécution (`prod*.log`, `lien*.log`, `prod.out`, `lien.out`).

Dans `journaux/prod_lit.log`, les 5 « ÉCHEC » viennent d'avant les corrections : 2 pour le banc du prétraitement
(refait sans erreur, voir `prod_pretraitement.log`) et 3 pour l'étape 11 (refaite sans erreur, voir `lien_lit.log`).

## Fichiers volontairement absents (données au niveau du jour ou du passage)

Ils restent dans le stockage chiffré privé, pas sur GitHub :

- `module_triage/triage/passages_*.csv`, `probabilites_*.csv` (une ligne par passage ou par jour) ;
- `module_lit/occupation_*.csv` (occupation jour par jour) ;
- `module_lit/lien_triage_PED*_series.csv` (séries quotidiennes urgences / service).
