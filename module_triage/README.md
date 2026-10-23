# NERA, module triage : priorité des patients aux urgences

**État : code écrit et testé (17 tests), en attente des données.** La chaîne complète (lecture du registre,
variables, sept modèles, validation mensuelle, calibration, seuil de décision, mesures, bancs T1 à T6) tourne
de bout en bout. Elle produira ses premiers résultats dès que le registre des urgences saisi dans l'outil sera
exporté en CSV. Les mathématiques complètes et la justification de chaque choix sont dans
[`METHODE.md`](METHODE.md).

## 1. La question

À l'arrivée d'un patient aux urgences, est-il **grave** (il faudra l'hospitaliser, le référer, ou il risque de
mourir) ou **non grave** (il rentrera chez lui) ? C'est un problème de **classification** : l'hyperplan sépare
deux classes de patients, au lieu de passer au milieu des données comme dans le module lit (régression). La
réponse prend la forme d'une **probabilité** P(grave), puis d'une **alerte** si cette probabilité dépasse un
seuil fixé par les coûts.

## 2. Les données

Elles viennent du **registre des urgences** (registre `URG` de l'outil de saisie, dépôt outil-saisi). La lecture
et le nettoyage sont dans le paquet `traitement` du dépôt outil-saisi (`traitement/urgences.py`).

| Colonne du registre | Utilisation |
|---|---|
| Date de passage | découpage de la validation dans le temps ; mois et week-end (contexte) |
| Garde (jour, garde de nuit, permanence) | contexte |
| Sexe, âge | variables ; l'âge choisit aussi le groupe (enfant < 15 ans, adulte) et les normes des constantes |
| Pouls, TA, glycémie, poids, température, FR, SpO2 | constantes : brutes, en écart à la norme de l'âge, ou en seuils d'alerte (banc T5) |
| Plaintes | 18 familles de plaintes (liste fixée à l'avance) et nombre de plaintes |
| Décision (orientation) | **cible** : grave (hospitalisé, référé, décédé, SCAM), non grave (externe), MEO placée par le banc T1 |
| Profession | sert seulement à reconnaître un nourrisson (« NRS ») quand l'âge manque |
| Diagnostic | **jamais une variable** : il est écrit après l'examen, le donner au modèle serait une fuite de l'avenir |
| N° dossier, résidence | **jamais lus** : identifiants ou quasi-identifiants |

Unité d'analyse : le **passage** (et non le jour comme dans le module lit). Les urgences reçoivent enfants et
adultes : **deux modèles séparés** (protocole), le banc T6 vérifie ce choix.

Règles de lecture (rien n'est inventé : une valeur illisible ou impossible devient manquante, et elle est
comptée dans le rapport de lecture) :
- âge « 4 ans », « 9 mois », « 1 an 6 mois », « 2 sem », « 10 j » converti en années ;
- TA « 120/80 » ou « 12/8 » (cmHg, multipliée par 10) ;
- glycémie convertie en g/L (mmol/L ÷ 5,551 ; mg/dL ÷ 100 ; « HI » = 6 g/L, « LO » = 0,2 g/L) ;
- chaque constante doit être plausible (par exemple température 30 à 44 °C, SpO2 40 à 100 %).

## 3. La méthode, en bref

| Étape | Ce qui est fait | Fichier |
|---|---|---|
| Lecture | CSV de l'outil → passages nettoyés, rapport de lecture, description par groupe | `traitement/urgences.py` (outil-saisi) |
| Normes | plage normale de chaque constante selon l'âge (APLS, OMS, qSOFA), écarts et signes d'alerte | `triage/normes.py` |
| Variables | une ligne par passage ; imputation par la médiane et standardisation apprises sur l'entraînement seulement | `triage/variables.py` |
| Modèles | règle de seuils, logistique, arbre, forêt, SVM linéaire, SVM RBF, SVM composite, tous à coûts de classe | `triage/modeles.py` |
| Validation | un découpage par mois ; dans l'entraînement : apprentissage, puis calibration (choix des réglages et Platt) | `triage/validation.py` |
| Décision | alerte si P(grave) ≥ s* = c₋/(c₊ + c₋) | `triage/mesures.py` |
| Mesures | sensibilité (prioritaire), sous-triage, sur-triage, spécificité, VPP, coût moyen, AUC, Brier, log-loss, McNemar | `triage/mesures.py` |
| Bancs | T1 à T6, chaque variante comparée à la référence par McNemar | `lancer_triage.py` |

Modèle principal : SVM à noyau RBF, constantes en écart à la norme de l'âge, plaintes, contexte et
indicatrices de valeurs manquantes, MEO comptée grave, coûts de classe équilibrés (C₊/C₋ = n₋/n₊),
probabilité de Platt, seuil s* = 1/(1 + c₊/c₋) avec c₊/c₋ = 4 par défaut (un grave manqué coûte autant que
quatre fausses alertes, le même rapport que le quantile τ = 0,8 du module lit). **Les bancs peuvent changer ce
choix** : c'est leur rôle.

| Banc | Question | Variantes |
|---|---|---|
| T1 | place de la mise en observation | grave, non grave, exclue (mesures aussi sur les passages hors MEO, communs aux trois) |
| T2 | modèle | règle de seuils, logistique, arbre, forêt, SVM linéaire, RBF, composite |
| T3 | coûts de classe | égaux, équilibrés (n₋/n₊), rapport du service (c₊/c₋) |
| T4 | variables | constantes seules ; + plaintes ; + contexte ; + indicatrices de valeurs manquantes |
| T5 | forme des constantes | brutes, écart à la norme de l'âge, seuils d'alerte |
| T6 | enfants et adultes séparés ou ensemble | modèle du groupe, modèle commun jugé sur le groupe |

## 4. Lancer

Dans WSL, depuis `nera-modele/module_triage`, après avoir exporté le registre des urgences depuis l'outil
(« CSV du service affiché », service URG) :

```bash
~/memoire-env/bin/python lancer_triage.py <registre-urg.csv>
```

Options : `--groupes enfant`, `--bancs T2 T3`, `--rapport-couts 9` (c₊/c₋), `--mois-min 2` (mois de données
avant le premier mois évalué), `--rapide` (essai de la chaîne). Test final, une seule fois, sur la période
verrouillée (à partir du 01/09/2026) : `--extraction aaaa-mm-jj --confirmation "<phrase du coffre>"` ; seul le
modèle retenu est alors évalué, rien n'est plus choisi.

Sorties dans `resultats/triage/` (jamais sur GitHub) : `description.csv` (passages, constantes renseignées,
classes, par groupe), `bancs.csv` (toutes les mesures), `choix_<groupe>.json` (réglages choisis chaque mois,
coefficients de Platt), `triage_rapport.md` (tableaux lisibles).

Tests :

```bash
PYTHONPATH=. ~/memoire-env/bin/python -m pytest -q tests
```

## 5. Ce qu'il reste à faire

1. Saisir le registre des urgences dans l'outil (registre `URG`), contrôler la saisie, l'exporter en CSV.
2. **Faire valider par le service** les plages normales des constantes (`triage/normes.py`) et le rapport des
   coûts c₊/c₋.
3. Lancer les bancs, retenir les choix qui gagnent (McNemar, p < 0,05), puis le test final.
