#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════════════════════
# Modèle NERA, module lit : toute la chaîne, dans l'ordre, sur la dernière version de la saisie,
# pour CHAQUE service (pédiatrie, médecine femme), puis le transfert entre services dans les deux sens.
#
# À relancer à chaque nouvelle version des fichiers exportés par l'outil de saisie (« Aperçu » →
# exporter tous les mois). Les données ne quittent pas l'ordinateur : donnees/ et resultats/
# ne sont jamais envoyés sur GitHub.
#
# Le traitement des données (étapes 0 et 1) vient du dépôt outil-saisi, installé une fois pour toutes :
#     ~/memoire-env/bin/pip install -e ../../outil-saisi
#
# Usage (dans un terminal Ubuntu / WSL, depuis le dossier nera-modele/module_lit) :
#     bash lancer_tout.sh                       # tout, pour les deux services, puis les transferts
#     SERVICES="MEDF" bash lancer_tout.sh       # un seul service
#     ETAPES="10" bash lancer_tout.sh           # seulement certaines étapes (ici : les transferts)
#     RAPIDE=1 bash lancer_tout.sh              # essai rapide (moins d'itérations)
#
# Après une coupure (courant, extinction) : relancer la MÊME commande. Le banc des choix (par dimension) et le
# banc des paramètres (par valeur) reprennent là où ils s'étaient arrêtés (resultats/reprise/, svr/reprise.py) ;
# rien n'est repris si les données, les options ou le code ont changé.
#
# Réglages (variables d'environnement, valeurs par défaut entre crochets) :
#     SERVICES     services traités               ["PED MEDF"]
#     SOURCE_PED   CSV de l'outil, pédiatrie      [MEMOIRE/saisie_ia/registre-ped-tous-les-mois.csv]
#     SOURCE_MEDF  CSV de l'outil, médecine femme [MEMOIRE/saisie_ia/registre-medf-COMPLET.csv]
#     LITS_PED     lits de la pédiatrie            [18 : 20 installés, souvent 2 ou 3 hors service]
#     LITS_MEDF    lits de la médecine femme       [17]
#     OUTIL        dépôt outil-saisi               [../../outil-saisi]
#     COMPTAGES    méthodes de comptage            ["minuit pic journee"]        
#     HORIZONS     horizons en jours               ["1 7"]
#
# Étapes (1 à 9 : pour chaque service ; 10 : entre les services) :
#     0  vérification de tous les calculs sur des données fictives (outil = Python = calcul direct)
#     1  conversion du CSV de l'outil et reconstitution de l'occupation ; réunion des exports des services
#     2  entraînement des niveaux 0 à 5 avec recherche des hyperparamètres par grille
#     3  banc des choix de conception (D1 à D11 et D13 : 23 modèles, noyau, perte, τ, variables, variantes de SVM…)
#     4  banc du prétraitement (P1 à P8) et banc croisé P1 × modèles (9 méthodes × 11 modèles)
#     5  sensibilité de chaque paramètre
#     6  sensibilité à la convention des jours
#     7  toutes les figures
#     8  modèle de survie J0 / J1 / J2
#     9  export des résultats pour l'outil de saisie (resultats/resultats_nera_<SERVICE>.json)
#    10  transfert entre services, dans les deux sens (PED → MEDF et MEDF → PED), pour chaque comptage :
#        P modèle propre · A local · B transfert direct · C groupé · G1 et G2 modèle unique (les deux
#        services comme une seule source) · persistance ; mêmes jours évalués, Diebold-Mariano
#    11  lien triage → lits (pédiatrie, chaque comptage) : corrélation urgences / admissions et banc D12 ;
#        demande d'avoir lancé AVANT module_triage/lancer_triage.py (fichiers probabilites_enfant.csv)
#    12  sélection : le SVM et le traitement des durées inconnues retenus d'après les bancs (selection.py),
#        pour chaque service et chaque comptage ; relue par validation_finale.py
# La validation finale (septembre-octobre 2026) n'est PAS lancée ici : une seule fois, à la fin.
# ═══════════════════════════════════════════════════════════════════════════════════════════════
set -u
cd "$(dirname "$0")"
PY="${PY:-$HOME/memoire-env/bin/python}"
OUTIL="${OUTIL:-../../outil-saisi}"
SAISIE=/mnt/c/Users/User/Desktop/MEMOIRE/saisie_ia
SERVICES="${SERVICES:-PED MEDF}"
declare -A SOURCE=([PED]="${SOURCE_PED:-$SAISIE/registre-ped-tous-les-mois.csv}" [MEDF]="${SOURCE_MEDF:-$SAISIE/registre-medf-COMPLET.csv}")
declare -A LITS=([PED]="${LITS_PED:-18}" [MEDF]="${LITS_MEDF:-17}")
COMPTAGES="${COMPTAGES:-minuit pic journee        }"
HORIZONS="${HORIZONS:-1 7}"
ETAPES="${ETAPES:-0 1 2 3 4 5 6 7 8 9 10 11 12}"
export PYTHONUNBUFFERED=1          # les journaux se remplissent au fur et à mesure (avancement visible)
RAPIDE_OPT=""; [ "${RAPIDE:-0}" = "1" ] && RAPIDE_OPT="--rapide"
GARDER_OPT=""; [ "${GARDER_REPRISE:-0}" = "1" ] && GARDER_OPT="--garder-reprise"   # étape 4 : garde les prévisions déjà calculées
JOURNAL=resultats/journaux; mkdir -p "$JOURNAL" donnees
EXPORT_TOUS=donnees/export_outil_PED_MEDF.csv   # séjours de tous les services réunis (transfert, modèle unique)

etape() { [[ " $ETAPES " == *" $1 "* ]]; }
lancer() {   # lancer <nom du journal> <commande…> : affiche le début et la fin, garde tout dans le journal
  local nom=$1; shift
  echo "── $(date '+%H:%M') $nom"
  if "$@" > "$JOURNAL/$nom.log" 2>&1; then echo "   terminé ($JOURNAL/$nom.log)"; else echo "   ÉCHEC : voir $JOURNAL/$nom.log"; tail -5 "$JOURNAL/$nom.log"; fi
}

etape 0 && lancer verification bash -c "cd '$OUTIL' && '$PY' -m verification.verifier_calculs"

for S in $SERVICES; do
  EXPORT=donnees/export_outil_$S.csv
  L=${LITS[$S]}
  echo "════ Service $S ($L lits)"
  if etape 1; then
    lancer "conversion_$S" "$PY" -m traitement.depuis_outil "${SOURCE[$S]}" --service "$S" --sortie "$EXPORT"
    for c in $COMPTAGES; do
      lancer "occupation_${S}_$c" "$PY" -m traitement.rapport_occupation "$EXPORT" --service "$S" --lits "$L" --inconnues estimee \
        --fenetre-censure p95 --rodage-debut --comptage "$c" --scenarios-lits $(seq $((L - 3)) $((L + 2)))
    done
  fi
  for c in $COMPTAGES; do
    etape 2 && lancer "niveaux_${S}_$c" "$PY" lancer_niveaux.py --service "$S" --horizons $HORIZONS --tau 0.8 --recherche grille --comptage "$c"
    etape 3 && lancer "banc_choix_${S}_$c" "$PY" benchmark_choix.py --service "$S" --horizons $HORIZONS --comptage "$c" $RAPIDE_OPT
    etape 5 && lancer "banc_parametres_${S}_$c" "$PY" benchmark_parametres.py --service "$S" --horizons $HORIZONS --comptage "$c" $RAPIDE_OPT
    etape 6 && lancer "sensibilite_${S}_$c" "$PY" sensibilite.py --service "$S" --horizons $HORIZONS --comptage "$c"
    etape 7 && lancer "figures_${S}_$c" "$PY" visualisations.py --service "$S" --comptage "$c" $RAPIDE_OPT
  done
  etape 4 && lancer "banc_pretraitement_$S" "$PY" benchmark_pretraitement.py "$EXPORT" --service "$S" --lits "$L" --horizons $HORIZONS --croise $RAPIDE_OPT $GARDER_OPT
  etape 8 && lancer "survie_$S" "$PY" modele_survie.py "$EXPORT" --service "$S" --lits "$L" --causes
  etape 9 && lancer "export_resultats_$S" "$PY" exporter_resultats.py --service "$S"
done

# ── Les exports des services réunis en un seul fichier (même en-tête) : source du transfert et du modèle unique.
if etape 1 && [ -f donnees/export_outil_PED.csv ] && [ -f donnees/export_outil_MEDF.csv ]; then
  { cat donnees/export_outil_PED.csv; tail -n +2 donnees/export_outil_MEDF.csv; } > "$EXPORT_TOUS"
  echo "── exports réunis : $EXPORT_TOUS"
fi

if etape 10; then
  echo "════ Transfert entre services (les deux sens, chaque comptage)"
  for c in $COMPTAGES; do
    lancer "transfert_PED_vers_MEDF_$c" "$PY" transfert.py "$EXPORT_TOUS" --source PED --cibles MEDF \
      --lits PED=${LITS[PED]} MEDF=${LITS[MEDF]} --horizons $HORIZONS --comptage "$c"
    lancer "transfert_MEDF_vers_PED_$c" "$PY" transfert.py "$EXPORT_TOUS" --source MEDF --cibles PED \
      --lits PED=${LITS[PED]} MEDF=${LITS[MEDF]} --horizons $HORIZONS --comptage "$c"
  done
fi
if etape 11; then
  echo "════ Lien triage → lits"
  if [ -f ../module_triage/resultats/triage/probabilites_enfant.csv ]; then
    for c in $COMPTAGES; do
      lancer "lien_triage_PED_$c" "$PY" lien_triage_lits.py --service PED --horizons $HORIZONS --comptage "$c"
    done
    etape 9 && lancer export_resultats_PED "$PY" exporter_resultats.py --service PED   # pour inclure le banc D12
  else
    echo "   ignoré : lancez d'abord module_triage/lancer_triage.py (probabilites_enfant.csv absent)"
  fi
fi
if etape 12; then
  echo "════ Sélection du SVM et du prétraitement"
  for S in $SERVICES; do
    for c in $COMPTAGES; do lancer "selection_${S}_$c" "$PY" selection.py --service "$S" --comptage "$c"; done
    etape 9 && lancer "export_resultats_$S" "$PY" exporter_resultats.py --service "$S"     # la sélection dans l'outil
  done
fi
echo "── $(date '+%H:%M') fini. Rapports : resultats/*.md · tableaux : resultats/*.csv · figures : resultats/figures_*/"
