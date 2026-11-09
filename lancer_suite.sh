#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════════════════════
# Modèle NERA : la suite des calculs, dans l'ordre, en UNE commande (terminal Ubuntu / WSL).
#
#     cd /mnt/c/Users/User/Desktop/nera-modele
#     nohup bash lancer_suite.sh > journal_suite.log 2>&1 &
#     tail -f journal_suite.log                   # suivre (Ctrl+C arrête l'affichage, pas le calcul)
#
# Après une coupure (extinction, courant) : relancer EXACTEMENT la même commande. Chaque banc reprend là où
# il s'était arrêté (resultats/reprise/) ; une phase finie est marquée dans .suite/ et n'est pas refaite.
#
# Ordre :
#   1  tests unitaires (module lit et triage) : on s'arrête s'ils échouent
#   2  triage, essai rapide de la chaîne (--rapide), puis triage complet ; fin du développement le
#      01/01/2026 (janvier 2026 = coffre du triage, voir lancer_triage.py --fin-developpement)
#   3  lits, pédiatrie, comptage de minuit : banc des choix (3), prétraitement et banc croisé (4, les
#      prévisions déjà calculées sont gardées), paramètres (5), sensibilité (6), figures (7), survie (8),
#      export (9), lien triage → lits (11)
#   4  lits, médecine femme : niveaux (2) puis étapes 3 à 9
#   5  transfert entre services (10) et sélection (12)
# Tests de comparaison : Diebold-Mariano sur la perte pinball au quantile τ = 0,8 avec correction de Holm
# (module lit) ; McNemar et bootstrap apparié du coût moyen par jours (triage).
#
# Réglages : COMPTAGES (défaut « minuit » ; « minuit pic journee » pour la sensibilité au comptage),
#            PHASES (défaut « 1 2 3 4 5 »), RAPIDE=1 pour un essai de toute la suite.
# ═══════════════════════════════════════════════════════════════════════════════════════════════
set -u
cd "$(dirname "$0")"
RACINE=$(pwd)
PY="${PY:-$HOME/memoire-env/bin/python}"
URG="${URG:-/mnt/c/Users/User/Desktop/MEMOIRE/saisie_ia/registre-urgences-COMPLET.csv}"
COMPTAGES="${COMPTAGES:-minuit}"
PHASES="${PHASES:-1 2 3 4 5}"
export PYTHONUNBUFFERED=1
mkdir -p .suite

# Un seul lancement à la fois : deux copies écriraient les mêmes fichiers de reprise.
autres=$(pgrep -f "benchmark_|lancer_triage.py|lancer_niveaux.py|lancer_tout.sh|sensibilite.py|transfert.py" | grep -v "^$$\$" || true)
if [ -n "$autres" ]; then
  echo "Un calcul tourne déjà (pid : $(echo $autres | tr '\n' ' ')). Attendez sa fin ou arrêtez-le avec : kill <pid>"
  ps -o pid,etime,args -p $(echo $autres | tr '\n' ',' | sed 's/,$//')
  exit 1
fi

phase() { [[ " $PHASES " == *" $1 "* ]] && [ ! -f ".suite/phase_$1.fait" ]; }
fini()  { touch ".suite/phase_$1.fait"; echo "── $(date '+%d/%m %H:%M') phase $1 terminée"; }
echec() { echo "── $(date '+%d/%m %H:%M') ÉCHEC : $1 (journal : $2)"; tail -n 15 "$2"; exit 1; }
RAPIDE_OPT=""; [ "${RAPIDE:-0}" = "1" ] && RAPIDE_OPT="--rapide"

echo "════ $(date '+%d/%m/%Y %H:%M') suite NERA · comptages : $COMPTAGES · phases : $PHASES"

if phase 1; then
  echo "── tests unitaires"
  (cd module_lit && "$PY" -m pytest -q tests) > .suite/tests_lit.log 2>&1 || echec "tests du module lit" .suite/tests_lit.log
  (cd module_triage && "$PY" -m pytest -q tests) > .suite/tests_triage.log 2>&1 || echec "tests du triage" .suite/tests_triage.log
  tail -n 1 .suite/tests_lit.log; tail -n 1 .suite/tests_triage.log
  fini 1
fi

if phase 2; then
  cd module_triage
  mkdir -p resultats
  if [ ! -f "$RACINE/.suite/triage_essai.fait" ]; then
    echo "── $(date '+%H:%M') triage, essai rapide (quelques minutes)"
    "$PY" -u lancer_triage.py "$URG" --rapide --bancs T1 T2 > resultats/triage_essai.log 2>&1 \
      || echec "essai rapide du triage" "$RACINE/module_triage/resultats/triage_essai.log"
    touch "$RACINE/.suite/triage_essai.fait"
  fi
  echo "── $(date '+%H:%M') triage complet (long ; reprend après coupure)"
  "$PY" -u lancer_triage.py "$URG" $RAPIDE_OPT > resultats/triage_complet.log 2>&1 \
    || echec "triage complet" "$RACINE/module_triage/resultats/triage_complet.log"
  cd "$RACINE"
  fini 2
fi

cd module_lit
if phase 3; then
  echo "════ $(date '+%H:%M') lits · pédiatrie"
  GARDER_REPRISE=1 SERVICES="PED" COMPTAGES="$COMPTAGES" ETAPES="3 4 5 6 7 8 9 11" RAPIDE="${RAPIDE:-0}" bash lancer_tout.sh
  (cd "$RACINE" && fini 3)
fi
if phase 4; then
  echo "════ $(date '+%H:%M') lits · médecine femme"
  SERVICES="MEDF" COMPTAGES="$COMPTAGES" ETAPES="2 3 4 5 6 7 8 9" RAPIDE="${RAPIDE:-0}" bash lancer_tout.sh
  (cd "$RACINE" && fini 4)
fi
if phase 5; then
  echo "════ $(date '+%H:%M') transfert entre services et sélection"
  SERVICES="PED MEDF" COMPTAGES="$COMPTAGES" ETAPES="10 12 9" RAPIDE="${RAPIDE:-0}" bash lancer_tout.sh
  (cd "$RACINE" && fini 5)
fi
echo "════ $(date '+%d/%m/%Y %H:%M') suite terminée. Rapports : module_lit/resultats/*.md, module_triage/resultats/triage/"
echo "Pour tout refaire : rm -rf .suite"
