# NERA : modèle de prévision pour la gestion hospitalière

*Mémoire : application des machines à vecteurs de support (SVM) aux projets de santé au Cameroun.*

NERA est le modèle d'aide à la décision de l'application hospitalière du même nom. Il est découpé en **deux
modules**, qui répondent à deux questions différentes et n'utilisent pas les mêmes données :

| Module | Question | Méthode | Données | État |
|---|---|---|---|---|
| [**Module lit**](module_lit/) | Combien de lits seront occupés demain, dans 3 jours, dans 7 jours ? | **régression** : SVR quantile à coûts asymétriques, noyau composite, empilement | registres d'hospitalisation de la pédiatrie (18 lits) et de la médecine femme (17 lits) → occupation jour par jour ; charge grave venue du triage | **presque complètement opérationnel** ; transfert entre services et lien avec le triage codés |
| [**Module triage**](module_triage/) | Ce patient qui arrive aux urgences est-il grave ? | **classification** : SVM à coûts asymétriques, probabilité de Platt, seuil de coût ; SVM pré-entraîné sur NHAMCS puis transféré | registre des urgences (constantes, plaintes, décision) ; source externe NHAMCS-ED | code écrit et testé (bancs T1 à T9), registre saisi : premiers essais faits, bancs complets à lancer |

Les trois dépôts du projet :

| Dépôt | Contenu |
|---|---|
| **nera-modele** (celui-ci) | le modèle NERA : modules lit et triage, avec toutes les mathématiques et les bancs d'essai |
| [outil-saisi](https://github.com/drew22109267/outil-saisi) | collecte des données (outil de saisie des registres), traitement (occupation), statistiques, décisions sur les données |
| [NERA-api](https://github.com/drew22109267/NERA-api) | l'API de l'application hospitalière NERA (.NET, PostgreSQL), où le modèle sera branché |

## Du registre à la prévision

```
Registres papier
    │  outil-saisi : photos masquées, saisie, contrôle qualité, statistiques
    ▼
CSV de l'outil ──► traitement (paquet Python « traitement » du dépôt outil-saisi)
    │              conversion, statuts des séjours, occupation jour par jour (3 méthodes), indicateurs
    ▼
Module lit (ce dépôt) : tableau d'apprentissage, SVR niveaux 0 à 5, validation glissante, bancs d'essai,
    │                   validation finale sur la période verrouillée (septembre-octobre 2026)
    ▼
Prévisions de l'occupation (quantile τ = 0,8 et intervalle à 90 %) ──► application NERA
```

## Pourquoi le transfert d'apprentissage

Deux constats sur le terrain ont conduit à ce choix.

1. **Les registres sont petits et incomplets.** Le registre des urgences compte environ 2 900 passages sur
   cinq mois, dont une partie sans décision lisible. Les constantes y sont rarement toutes notées : chez l'enfant,
   le pouls n'est écrit qu'environ une fois sur sept. Les premiers essais du modèle de triage donnent une AUC
   modeste (de l'ordre de 0,64 chez l'adulte et 0,71 chez l'enfant) : le modèle apprend, mais il manque de
   matière.
2. **La validation dans un second hôpital a été abandonnée**, faute de temps et de moyens. Il fallait une autre
   façon de profiter de données plus nombreuses que celles d'un seul service.

D'où deux transferts, chacun benchmarké contre le modèle qui n'utilise que les données locales :

| Module | Source | Cible | Ce qui est transféré |
|---|---|---|---|
| **Triage** | NHAMCS-ED : urgences des États-Unis (CDC, données publiques), 2015-2022, environ 144 000 passages, constantes notées à plus de 90 % | registre des urgences du Cameroun (enfants et adultes séparés) | un SVM **pré-entraîné** sur la source, puis adapté |
| **Lits** | pédiatrie (27 mois) et médecine femme (12 mois) | l'autre service | la méthode et les réglages, ou un modèle commun aux deux services |

Ce qu'on en fait :

- **Dans le triage (banc T9)**, huit façons d'utiliser le modèle pré-entraîné sont comparées, sur les mêmes mois
  du Cameroun, au modèle principal et au même modèle appris sur le Cameroun seul : données locales seules,
  données externes seules (modèle appliqué tel quel, ou seulement recalibré), et les deux réunies (données
  réunies, augmentation de Daumé, régularisation biaisée vers le modèle source, A-SVM qui ajoute au modèle source
  une correction apprise sur les variables locales, score de la source comme variable). Si une variante gagne
  (McNemar), elle devient le modèle principal ; si le transfert dégrade les résultats (transfert négatif), c'est
  un résultat du mémoire.
- **Dans le module lit (banc D12)**, la probabilité de gravité donnée par chaque modèle de triage, sommée sur les
  enfants passés aux urgences dans la journée (la « charge grave attendue »), devient une variable de la
  prévision de l'occupation. Diebold-Mariano dit si elle améliore la prévision des lits, et si le triage
  pré-entraîné fait mieux que le triage local. C'est le lien entre les deux modules prévu par le protocole
  (Document 11, § 1.4) : faute d'identifiant patient commun aux deux registres, il est fait jour par jour.
- **Entre services (module lit, étape 10)**, pédiatrie vers médecine femme et médecine femme vers pédiatrie :
  modèle propre de chaque service, réglages de l'autre gelés, modèle de l'autre appliqué tel quel, données
  réunies, et modèle unique pour les deux services (période commune ou toute la période), mêmes jours évalués.

Les données externes (NHAMCS) restent sur l'ordinateur, dans `MEMOIRE/donnees_externes/`, comme les registres :
rien n'est envoyé sur GitHub.

## Le lien entre les deux modules

```
Urgences ──► triage SVM (local, ou pré-entraîné sur NHAMCS puis transféré) ──► P(grave) de chaque enfant
                                                                                  │ somme par jour
                                                                                  ▼
Registre de pédiatrie ──► occupation ──► SVR quantile + « charge grave attendue » ──► lits nécessaires demain
```

`module_lit/lien_triage_lits.py` : corrélation de Spearman entre les urgences du jour d et les admissions des
jours d à d + 3 (intervalle par bootstrap en blocs, p-valeur par décalage circulaire), part des admissions passées
par les urgences, et banc D12 (le modèle lit avec et sans chaque signal des urgences).

## Démarrer

```bash
cd /mnt/c/Users/<utilisateur>/Desktop
git clone https://github.com/drew22109267/outil-saisi.git
git clone https://github.com/drew22109267/nera-modele.git
~/memoire-env/bin/pip install -e outil-saisi                # le traitement des données
cd nera-modele/module_triage
~/memoire-env/bin/python preparer_nhamcs.py /mnt/c/Users/<utilisateur>/Desktop/MEMOIRE/donnees_externes/nhamcs/dta
~/memoire-env/bin/python lancer_triage.py <registre-urgences.csv>   # triage : bancs T1 à T9, raccordement
cd ../module_lit
bash lancer_tout.sh            # lits : pédiatrie et médecine femme, transferts, lien avec le triage
```

Installation complète, toutes les formules, les scripts et la lecture des résultats :
[`module_lit/README.md`](module_lit/README.md). Fonctions de coût, minimisation et justification de chaque
décision, avec le banc d'essai qui la vérifie : [`module_lit/METHODE.md`](module_lit/METHODE.md).

## Principes communs aux deux modules

- **Tout est écrit à la main** : PyTorch sert seulement de bibliothèque de tenseurs ; gradients dérivés
  analytiquement et vérifiés par différences finies, optimiseurs et métriques codés dans le dépôt, aucune
  bibliothèque d'apprentissage automatique.
- **Le coût d'une erreur est asymétrique** et il est mis **dans la fonction minimisée** : manquer de lits (ou
  sous-trier un patient grave) coûte plus cher que l'erreur inverse.
- **Tout choix est comparé** à ses alternatives (bancs d'essai, test de Diebold-Mariano), et la décision est
  écrite dans un registre avec sa raison.
- **Validation dans le temps, sans fuite** : les deux derniers mois sont verrouillés jusqu'au test final.
- **Aucune donnée de patient sur GitHub** : `donnees/` et `resultats/` restent sur l'ordinateur.
