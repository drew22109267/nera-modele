# NERA, module triage : priorité des patients aux urgences

**État : code écrit et testé (36 tests), registre des urgences saisi (environ 2 900 passages, septembre 2025 →
janvier 2026).** La chaîne complète (lecture du registre, variables, sept modèles, valeurs manquantes, validation
mensuelle, calibration, seuil de décision, mesures, bancs T1 à T9, raccordement enfants + adultes, transfert d'un
SVM pré-entraîné sur NHAMCS) tourne de bout en bout ; les premiers essais rapides sont faits, les bancs complets
restent à lancer. Les mathématiques complètes et la justification de chaque choix sont dans
[`METHODE.md`](METHODE.md) et dans le guide mathématique du mémoire (chapitre 13).

## 1. La question

À l'arrivée d'un patient aux urgences, quelle **priorité** lui donner ? Trois niveaux, ordonnés :

| Niveau | Décision écrite au registre | Couleur | Priorité |
|---|---|---|---|
| grave | hospitalisé, référé, décédé, sortie contre avis médical | rouge | 1 |
| moyen | mise en observation (MEO) | jaune | 2 |
| non grave | externe, retour à domicile | vert | 3 |

C'est un problème de **classification ordinale** (`triage/ordinal.py`, Frank et Hall, 2001) : deux SVM binaires
répondent aux deux questions emboîtées, « grave ? » et « grave ou moyen ? », chacun calibré par Platt ; les trois
probabilités s'en déduisent (P(moyen) = P(grave ou moyen) − P(grave)). La priorité donnée est celle de **plus
petit coût attendu**, avec une matrice des coûts qui pénalise le sous-triage r = c₊/c₋ fois plus que le
sur-triage, par niveau d'écart.

## 2. Les données

Elles viennent du **registre des urgences** (registre `URG` de l'outil de saisie, dépôt outil-saisi). La lecture
et le nettoyage sont dans le paquet `traitement` du dépôt outil-saisi (`traitement/urgences.py`).

| Colonne du registre | Utilisation |
|---|---|
| Date de passage | découpage de la validation dans le temps ; mois et week-end (contexte) |
| Garde (jour, garde de nuit, permanence) | contexte |
| Sexe, âge | variables ; l'âge choisit aussi le groupe (enfant < 15 ans, adulte) et les normes des constantes |
| Pouls, TA, glycémie, poids, température, FR, SpO2 | constantes : brutes, en écart à la norme de l'âge, ou en seuils d'alerte (banc T5) |
| Plaintes | 28 familles de plaintes (liste fixée à l'avance, en français et en anglais : le registre est bilingue), nombre de plaintes, et sac de mots (banc T11) |
| Décision (orientation) | **cible** : grave (hospitalisé, référé, décédé, SCAM), non grave (externe), MEO placée par le banc T1 |
| Profession | sert seulement quand l'âge est illisible : nourrisson (« NRS »), et groupe déduit (« enfant », « écolier » → enfant ; profession d'adulte → adulte ; « élève » reste sans groupe), banc T12 |
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
| Variables | une ligne par passage ; imputation (banc T8, médiane par défaut) et standardisation apprises sur l'entraînement seulement | `triage/variables.py` |
| Modèles | règle de seuils, logistique, arbre, forêt, SVM linéaire, SVM RBF, SVM composite, tous à coûts de classe | `triage/modeles.py` |
| Validation | un découpage par mois ; dans l'entraînement : apprentissage, puis calibration (choix des réglages et Platt) | `triage/validation.py` |
| Décision | alerte si P(grave) ≥ s* = c₋/(c₊ + c₋) | `triage/mesures.py` |
| Mesures | trois niveaux : graves en rouge (prioritaire), graves sous-triés, sous-triage, sur-triage, part de rouges / jaunes / verts, exactitude, kappa pondéré quadratique, coût moyen, AUC des deux questions, Brier ; spécificité à 90 % de sensibilité pour les graves ; McNemar sur « priorité juste » | `triage/ordinal.py`, `triage/mesures.py` |
| Bancs | T1 à T7, chaque variante comparée à la référence par McNemar | `lancer_triage.py` |

Modèle principal : SVM à noyau RBF, constantes en écart à la norme de l'âge, plaintes, contexte et
indicatrices de valeurs manquantes, trois niveaux (MEO = moyen), coûts de classe équilibrés (C₊/C₋ = n₋/n₊),
probabilités de Platt, priorité de plus petit coût attendu avec r = c₊/c₋ = 4 par défaut (un niveau de
sous-triage coûte autant que quatre niveaux de sur-triage, le même rapport que le quantile τ = 0,8 du module
lit). Les rapports de coûts et la matrice sont à valider avec le service. **Les bancs peuvent changer ce
choix** : c'est leur rôle.

| Banc | Question | Variantes |
|---|---|---|
| T1 | trois niveaux ou deux | trois niveaux (retenu : MEO = moyen, choix clinique fixé à l'avance) ; l'ancien triage à deux niveaux (rouge ou vert) avec la MEO comptée grave, ou comptée non grave, lu sur les mêmes passages et les mêmes probabilités ; McNemar sur « priorité juste » |
| T2 | modèle | règle de seuils, logistique, arbre, forêt, SVM linéaire, RBF, composite |
| T3 | coûts de classe | égaux, équilibrés (n₋/n₊), rapport du service (c₊/c₋) |
| T4 | variables | constantes seules ; + plaintes ; + contexte ; + indicatrices de valeurs manquantes |
| T5 | forme des constantes | brutes, écart à la norme de l'âge, seuils d'alerte |
| T6 | enfants et adultes séparés ou ensemble | modèle du groupe, modèle commun jugé sur le groupe |
| T7 | résumer les variables avant de classer | originales, ACP (80 % de variance), AFDM (indicatrices recodées (x − p)/√p), k-means (4 groupes), originales + k-means ; tout appris sur l'apprentissage seulement (`triage/representations.py`) |
| T8 | valeurs manquantes | cas complets (passages incomplets retirés, référence comparée sur les mêmes passages), variables à plus de 50 % de manquants retirées, médiane, moyenne, médiane par tranche d'âge, k plus proches voisins, régressions enchaînées (ridge), loi normale par EM, ACP itérative ; tout appris sur l'apprentissage seulement (`triage/imputation.py`) |
| T9 | transfert d'un SVM pré-entraîné | source : NHAMCS-ED (urgences des États-Unis, CDC, 2015-2022, environ 150 000 passages, même groupe d'âge) ; SVM sur caractéristiques de Fourier aléatoires (approximation du noyau RBF) ; variantes : Cameroun seul, source seule, source recalibrée, données réunies, augmentation (Daumé), régularisation biaisée, A-SVM, score de la source ; référence : le modèle principal (`triage/transfert.py`, `triage/nhamcs.py`) |
| T10 | valeurs manquantes × modèles | chaque traitement de T8 avec chaque modèle de T2 |
| T11 | plaintes × modèles | familles fixées à l'avance, sac de mots (mots écrits dans au moins 5 passages avant le verrou, tirés du texte seul), familles + mots, sans plaintes ; chacune avec chaque modèle de T2 |
| T12 | passages d'âge illisible | avec ou sans les passages dont le groupe est déduit de la profession, comparés sur les passages d'âge écrit (McNemar) |
| T13 | rapport des coûts c₊/c₋ | 1, 2, 3, 4, 6 : mêmes probabilités, seuil s* = 1/(1 + c₊/c₋) ; sensibilité, spécificité et taux d'alerte de chaque seuil (le rapport est à valider avec le service) |
| Raccordement | enfants et adultes réunis | les prévisions des deux modèles séparés, réunies, comparées au modèle commun sur TOUS les passages des urgences (mêmes passages, McNemar), avec le détail par groupe |

## 4. Transfert d'apprentissage : pourquoi et comment (banc T9)

**Pourquoi.** Le registre du Cameroun est petit (quelques milliers de passages, cinq mois) et les constantes y
sont rarement notées (chez l'enfant, le pouls environ une fois sur sept) : les premiers essais donnent une AUC
modeste (0,64 chez l'adulte, 0,71 chez l'enfant). La validation dans un second hôpital a été abandonnée (temps
et moyens). On profite donc d'un grand registre public : **NHAMCS-ED** (urgences des États-Unis, CDC, 2015-2022),
environ 144 000 passages dont les constantes sont notées à plus de 90 %.

**Comment.**

1. `triage/nhamcs.py` ramène NHAMCS au format du registre : température °F → °C, codes de motif de consultation
   → les 28 familles de plaintes (table fixée à l'avance), devenir → grave (hospitalisé, transféré, décédé,
   parti contre avis), MEO (observation puis domicile) ou non grave. Enfants avec enfants, adultes avec adultes :
   jamais de transfert enfant → adulte.
2. `triage/transfert.py` pré-entraîne un SVM sur la source. Un SVM à noyau sur 100 000 passages demanderait une
   matrice de 80 Go : on utilise les **caractéristiques de Fourier aléatoires** (Rahimi et Recht, 2007), une
   empreinte de 500 nombres par passage dont le produit scalaire approche le noyau RBF ; le SVM linéaire sur ces
   empreintes est presque le SVM à noyau. Seules les variables communes aux deux registres sont utilisées (la
   glycémie et le poids n'existent pas dans NHAMCS).
3. Le banc T9 compare, sur les mêmes mois du Cameroun :

| Variante | Données pour apprendre | Principe |
|---|---|---|
| Cameroun seul (Fourier) | Cameroun | même représentation que le transfert : le juste témoin |
| source seule | externe | le modèle pré-entraîné appliqué tel quel |
| source recalibrée | externe (+ calibration Cameroun) | seule l'échelle des probabilités est refaite |
| réunies | les deux | un SVM sur la source et le Cameroun, qui pèsent autant au total |
| augmentation | les deux | Daumé (2007) : une partie commune et une partie propre au Cameroun |
| régularisation biaisée | les deux | ½‖w − w_s‖² au lieu de ½‖w‖² : réapprendre en restant près du modèle source |
| A-SVM | les deux | f = f_s + Δ, Δ linéaire sur toutes les variables du registre (glycémie et poids compris) |
| score de la source | les deux | f_s(x) devient une variable du modèle du Cameroun |

Chaque variante est comparée deux fois par McNemar : au modèle principal et au Cameroun seul. Le gagnant peut
devenir le modèle principal ; un transfert négatif est un résultat.

4. **Vers le module lit.** Le triage exporte les probabilités de chaque modèle (`probabilites_<groupe>.csv`) ;
   `module_lit/lien_triage_lits.py` en fait la charge grave du jour et le banc D12 mesure ce qu'elle apporte à la
   prévision des lits, pour le modèle local et pour chaque modèle transféré.

## 5. Valeurs manquantes (banc T8) et raccordement enfants + adultes

Neuf traitements des valeurs manquantes, appris sur l'apprentissage seulement (`triage/imputation.py`) : cas
complets, variables retirées, médiane, moyenne, médiane par tranche d'âge, k plus proches voisins, régressions
enchaînées, loi normale multivariée par EM, ACP itérative. Les indicatrices « constante non prise » restent dans
toutes les variantes.

Enfants et adultes ont chacun leur modèle ; les deux sont ensuite **raccordés** (chaque passage reçoit la
probabilité du modèle de son groupe) et ce système est comparé, sur tous les passages des urgences, au modèle
commun appris sur tout le monde.

## 6. Lancer

Source externe du banc T9, une seule fois (fichiers NHAMCS dans `MEMOIRE/donnees_externes/nhamcs/dta`, jamais sur
GitHub) :

```bash
~/memoire-env/bin/python preparer_nhamcs.py /mnt/c/Users/User/Desktop/MEMOIRE/donnees_externes/nhamcs/dta
```

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

## 7. Ce qu'il reste à faire

1. Lancer les bancs complets (T1 à T9, raccordement), retenir les choix qui gagnent (McNemar, p < 0,05).
2. **Faire valider par le service** les plages normales des constantes (`triage/normes.py`) et le rapport des
   coûts c₊/c₋.
3. Test final, une seule fois, sur la période verrouillée.
