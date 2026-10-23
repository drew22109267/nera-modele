# NERA, module triage : priorité des patients aux urgences

**État : en préparation, non opérationnel.** Aucun modèle de triage n'est encore entraîné : les données des
urgences restent à saisir. Ce document fixe ce qui est déjà décidé, pour que le module se construise sur les
mêmes principes que le [module lit](../module_lit/).

## 1. La question

À l'arrivée d'un patient aux urgences, quel niveau de priorité lui donner (et donc quelle orientation :
hospitalisation, observation, retour à domicile, référence vers un hôpital de catégorie supérieure) ? C'est un
problème de **classification** : l'hyperplan sépare des classes de patients, au lieu de passer au milieu des
données comme dans le module lit (régression).

## 2. Les données

Le registre d'hospitalisation ne contient ni constantes, ni décision de triage, ni heure. Les données viennent du
**registre des urgences**, dont les colonnes sont déjà décrites dans l'outil de saisie (dépôt outil-saisi,
`outil-saisie/registres.js`, registre `URG`) :

| Colonne | Rôle |
|---|---|
| Date de passage | unité de temps, découpage de la validation |
| Sexe, âge, résidence | caractéristiques du patient |
| Pouls, tension artérielle, glycémie, poids, température | constantes (signes de gravité) |
| Symptômes, diagnostic | motif et diagnostic des urgences |
| Décision | classe à prédire (orientation écrite par le médecin) |

Unité d'analyse : le **patient** (un passage aux urgences), et non le jour comme dans le module lit. Six mois de
registre suffisent. Les urgences reçoivent enfants et adultes : **deux modèles séparés**, jamais de transfert
d'un modèle enfant vers les adultes (physiologie et seuils des constantes différents).

## 3. Ce qui est prévu

- **Modèle** : SVM de classification à coûts asymétriques. Un sous-triage (patient grave classé non urgent)
  coûte plus cher qu'un sur-triage : le coût est mis dans la fonction minimisée, comme dans le module lit,
  avec une perte de type hinge pondérée par classe. Le SVM linéaire à coûts par exemple, la calibration de
  Platt et les mesures AUC, Brier et log-loss sont déjà écrits et testés (`module_lit/svr/classification.py`,
  utilisés par le modèle de survie) ; ils seront la base du module.
- **Variables** : constantes ramenées à des seuils de gravité selon l'âge, symptômes codés, calendrier.
- **Validation** : dans le temps, sans fuite ; le dernier mois verrouillé jusqu'au test final.
- **Mesures** : sensibilité sur les patients graves (priorité), spécificité, matrice de confusion, coût
  moyen des décisions, comparaison aux règles de triage existantes et à des modèles de référence.
- **Bancs d'essai** : chaque choix (variables, noyau, coûts, seuils) comparé à ses alternatives, comme pour le
  module lit.

## 4. Cible, décision et évaluation

- **Cible principale (binaire)** : « grave » = hospitalisé, référé ou décédé ; « non grave » = externe ; la mise en
  observation, cas intermédiaire, est placée par le banc T1. Cible secondaire : l'orientation elle-même (un SVM par
  orientation, « un contre tous »), pour prévoir la charge d'hospitalisations.
- **Probabilité** : score du SVM calibré par Platt, P(grave | f) = 1 / (1 + exp(A f + B)), sur des passages non
  utilisés pour l'entraînement.
- **Décision** : alerte si P(grave) ≥ s, avec s* = c₋ / (c₊ + c₋) (c₊ coût d'un grave manqué, c₋ coût d'une fausse
  alerte) : le même raisonnement que le quantile τ du module lit.
- **Mesures** : sensibilité sur les graves (prioritaire), sous-triage, sur-triage, spécificité, AUC, Brier, coût
  moyen ; comparaison de deux modèles sur les mêmes passages par le test de McNemar,
  χ² = (|b − c| − 1)² / (b + c).

| Banc prévu | Question |
|---|---|
| T1 | place de la mise en observation (grave, non grave, exclue) |
| T2 | modèle : règle de seuils sur les constantes, régression logistique, arbre, forêt, SVM linéaire, RBF, composite |
| T3 | coût : C₊/C₋ = 1, = n₋/n₊, = rapport fixé avec le service, et le seuil s* correspondant |
| T4 | variables : constantes seules, + plaintes, + contexte, + indicatrices de valeurs manquantes |
| T5 | constantes brutes, rapportées à l'âge (écart à la norme), ou seuils d'alerte |
| T6 | enfants et adultes ensemble ou séparés (protocole : séparés) |

L'outil de saisie donne déjà, pour le registre des urgences, les premières conclusions : constantes assez souvent
écrites pour être utilisées, nombre de passages graves, part d'enfants et d'adultes.

## 5. Étapes pour le rendre opérationnel

1. Photographier et saisir le registre des urgences avec l'outil de saisie (registre `URG`), contrôler la
   qualité de la saisie.
2. Écrire la conversion et la préparation des passages dans le paquet `traitement` (dépôt outil-saisi).
3. Écrire le tableau d'apprentissage, l'entraînement, la validation et les bancs d'essai dans ce dossier, avec
   leurs mathématiques dans un `README.md` et un `METHODE.md` détaillés, sur le modèle du module lit.
