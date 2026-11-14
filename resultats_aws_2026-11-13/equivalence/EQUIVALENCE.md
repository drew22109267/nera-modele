# Équivalence sur données réelles : main de drew (e2bcc17) contre main actuel (abe05ba = 11e164b + avertissement)

Pédiatrie, comptage minuit : occupation, niveaux, banc des choix (étapes 1 à 3 du module lit) ; triage enfants,
tous les bancs (T9 avec NHAMCS). Calcul du 13/11/2026 sur AWS (m7g.8xlarge). 60 fichiers de chaque côté.

## Résultat

- **25 fichiers identiques à l'octet**, dont l'occupation et les niveaux.
- **Module lit : identique.** Dans les 24 tableaux du banc des choix (D1 à D14, horizons 1 et 7), seule la colonne
  « temps (s) » diffère (durée de calcul). Les autres différences sont des journaux et des fichiers d'environnement
  (horodatages, versions).
- **Triage : tous les écarts sont ceux annoncés par 11e164b.**
  1. Banc T9 (transfert NHAMCS) seulement : calibration partagée (`calibration_partagee` dans `choix_enfant.json`),
     d'où d'autres réglages C, d'autres probabilités T9 (`p_croisee_*` et `p_chronologique_*` des 6 variantes de
     transfert) et d'autres mesures sur les lignes T9 de `bancs.csv`. Les 257 autres lignes sont identiques.
  2. Colonnes ajoutées : `spec_s90_b`, `spec_s90_c`, `spec_s90_p`, `spec_s90_p_holm` (spécificité au seuil s₉₀).
  3. Règle de sélection : le modèle retenu passe de « T10 · mediane_age × svm_lineaire » à
     « T11 · familles + mots × lssvm ». Les mesures de ces deux lignes sont identiques dans les deux versions : le
     changement vient de la règle, pas du calcul.
- Aucun écart inexpliqué.

Les fichiers par passage ou par jour ne sont pas dans ce dossier public ; ils restent dans le bucket chiffré.
