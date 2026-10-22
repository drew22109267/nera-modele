# NERA, module lit : prévision de l'occupation des lits

*Modèle NERA, module lit. Prévision de l'occupation des lits d'un service de pédiatrie par une architecture SVR
révisée : coûts asymétriques (régression quantile), noyau composite à poids appris, empilement de modèles.*

Ce dossier contient tout le code du **module lit** du modèle NERA : construction du tableau d'apprentissage,
modèles (SVR niveaux 1 à 5, références, concurrents), entraînement, validation, bancs d'essai, figures, test
final, modèle de survie et transfert vers les autres services. Ce document est écrit pour qu'une personne qui
reprend le travail puisse, sans autre aide :

1. installer et lancer le module ;
2. retrouver **toutes les formules mathématiques** du modèle, avec leur justification ;
3. savoir quel fichier fait quoi, dans quel ordre lancer les scripts et comment lire les résultats ;
4. savoir ce qui reste à faire.

Tous les calculs sont écrits à la main. PyTorch sert uniquement de bibliothèque de tenseurs : les gradients
sont dérivés analytiquement, les optimiseurs (descente de gradient, momentum, Adam) et les métriques sont codés
dans le dépôt. **Aucune importation de scikit-learn, statsmodels ou bibliothèque statistique.** pandas sert à
lire les fichiers et à manipuler les dates, matplotlib à dessiner.

**Pour comprendre les choix** : [`METHODE.md`](METHODE.md) explique, en français et pas à pas, pour chaque
modèle la fonction de coût, la fonction minimisée et la technique de minimisation, puis donne le registre de
toutes les décisions (retenu, alternatives, raison, banc qui la vérifie).

**D'où viennent les données** : la collecte (registres papier, outil de saisie, contrôle qualité), le
traitement (conversion, statuts des séjours, reconstitution de l'occupation selon trois méthodes de comptage,
pic de la journée, capacité variable) et les statistiques descriptives sont dans le dépôt
[outil-saisi](https://github.com/drew22109267/outil-saisi), avec leurs mathématiques (`MATHEMATIQUES.md`).
Le module lit utilise son paquet Python `traitement`.

Les nombres cités en exemple dans les parties mathématiques sont **fictifs**.

## Sommaire

1. [Organisation](#1-organisation)
2. [Installation et lancement](#2-installation-et-lancement)
3. [Mathématiques A : le SVR](#3-mathématiques-a--le-svr)
4. [Mathématiques B : évaluation et comparaison des modèles](#4-mathématiques-b--évaluation-et-comparaison-des-modèles)
5. [Mathématiques C : survie, classification et transfert](#5-mathématiques-c--survie-classification-et-transfert)
6. [Fichier par fichier](#6-fichier-par-fichier)
7. [Les scripts, dans l'ordre](#7-les-scripts-dans-lordre)
8. [Les figures et leur lecture](#8-les-figures-et-leur-lecture)
9. [Tests](#9-tests)
10. [État d'avancement et suite du travail](#10-état-davancement-et-suite-du-travail)
11. [Références](#11-références)

---

## 1. Organisation

```
module_lit/
├── README.md                  ce document
├── METHODE.md                 fonctions de coût, minimisation, registre de toutes les décisions
├── svr/                       les modèles, écrits à la main (pertes, noyaux, optimiseurs, SVR, validation…)
├── tests/                     tests automatiques (pytest)
├── lancer_tout.sh             toute la chaîne en une commande
├── pipeline.ipynb             toute la chaîne dans un notebook, avec les explications (recréé par creer_notebook.py)
├── lancer_niveaux.py          étape 2 : ablation des niveaux 0 à 5
├── sensibilite.py             étape 3 : sensibilité à la convention des jours
├── benchmark_choix.py         banc de chaque choix de conception (D1 à D11)
├── benchmark_pretraitement.py banc de chaque choix de prétraitement (P1 à P8)
├── benchmark_parametres.py    sensibilité de tous les paramètres
├── visualisations.py          toutes les figures
├── validation_finale.py       test final sur la période verrouillée (une seule fois)
├── modele_survie.py           probabilités de sortie J0 / J1 / J2
├── transfert.py               services à historique court et total de l'hôpital
└── demo_entrainement.py       démonstration pas à pas de l'entraînement d'un SVR
```

Deux dossiers sont créés à l'usage et **ne sont jamais versionnés** (données de patients) :
`donnees/` (fichiers d'entrée) et `resultats/` (sorties). Le `.gitignore` les exclut, ainsi que tous les CSV,
JSON et images.

## 2. Installation et lancement

Les scripts s'exécutent sous Linux. Sous Windows, ils tournent dans **WSL (Ubuntu)** : la politique de sécurité
de Windows (Smart App Control) bloque les bibliothèques compilées de PyTorch lancées directement depuis Windows.

Installation une seule fois, dans un terminal Ubuntu. Les deux dépôts sont clonés côte à côte :

```bash
cd /mnt/c/Users/<utilisateur>/Desktop
git clone https://github.com/drew22109267/outil-saisi.git
git clone https://github.com/drew22109267/nera-modele.git
python3 -m venv ~/memoire-env
~/memoire-env/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
~/memoire-env/bin/pip install pandas matplotlib pytest jupyterlab
~/memoire-env/bin/pip install -e outil-saisi            # le paquet « traitement » (données)
```

(Avec `uv` : `uv pip install --python ~/memoire-env/bin/python -e outil-saisi`.)

Toutes les commandes se lancent depuis ce dossier :

```bash
cd /mnt/c/Users/<utilisateur>/Desktop/nera-modele/module_lit
bash lancer_tout.sh                              # toute la chaîne (journaux dans resultats/journaux)
~/memoire-env/bin/jupyter lab pipeline.ipynb     # ou pas à pas, avec les explications
```

`lancer_tout.sh` enchaîne : 0 vérification des calculs (dans outil-saisi), 1 conversion et occupation
(paquet `traitement`), 2 entraînement des niveaux, 3 à 5 bancs d'essai, 6 sensibilité, 7 figures, 8 modèle de
survie. Réglages par variables d'environnement (`SOURCE`, `LITS`, `LITS_FICHIER`, `COMPTAGES`, `HORIZONS`,
`ETAPES`, `RAPIDE`, `OUTIL`) : voir l'en-tête du script.

Tous les calculs sont faits en double précision (`torch.float64`) sur processeur.

**Période verrouillée.** Les données vont de juillet 2024 à octobre 2026. À partir du 01/09/2026, rien n'est lu
pendant le développement (`traitement/verrou.py`, dépôt outil-saisi). Seul `validation_finale.py` (et
`transfert.py` avec la même confirmation) ouvre le coffre, avec une phrase de confirmation obligatoire ;
chaque ouverture est inscrite dans `resultats/coffre_ouvertures.log`. Le test final porte sur septembre, puis
le modèle est réentraîné avec septembre et testé sur octobre (réentraînement mensuel).

---

## 3. Mathématiques A : le SVR

Code : `svr/pertes.py`, `svr/noyaux.py`, `svr/optimiseurs.py`, `svr/modeles.py`,
`svr/empilement.py`, `svr/caracteristiques.py`, `svr/validation.py`, `svr/recherche.py`,
`svr/niveaux.py`.

### 3.1 Les niveaux du modèle (ablation)

Chaque niveau ajoute une brique et doit prouver qu'elle améliore le précédent.

| Niveau | Modèle | Ce qu'il ajoute |
|---|---|---|
| 0 | persistance, saisonnier, moyenne mobile | la barre à battre, sans apprentissage |
| 1 | SVR linéaire, perte ε-insensible | un hyperplan f(x) = w·x + b et son tube ± ε |
| 2 | SVR à noyau RBF | des relations non linéaires |
| 3 | SVR quantile (perte pinball) | les coûts asymétriques (τ = 0,8) et l'intervalle à 90 % |
| 4 | SVR quantile à noyau composite | deux blocs de variables mélangés par un poids β appris |
| 5 | empilement | combinaison apprise des niveaux 3, 4 et de la persistance |

### 3.2 Objectif minimisé (forme primale)

```
J(w, b) = ½ ‖w‖² + C Σ_i L(y_i − f(x_i))          f(x) = w·x + b             (linéaire)
J(α, b) = ½ αᵀKα + C Σ_i L(y_i − f(x_i))          f = Kα + b                 (noyau)
```

Le premier terme garde le modèle simple (grande marge), le second fait payer les erreurs ; C règle
l'équilibre. On note r_i = y_i − f_i le résidu (r > 0 : sous-estimation, risque de manquer de
lits) et g_i = ∂L/∂f_i la dérivée de la perte par rapport à la prévision (∂L/∂f = −L'(r)).

### 3.3 Fonctions de perte

| Perte | Formule | Dérivée ∂L/∂f |
|---|---|---|
| ε-insensible | L_ε(r) = max(0, |r| − ε) | −signe(r) · 1(|r| > ε) |
| pinball (quantile τ) | ρ_τ(r) = max(τ r, (τ − 1) r) | −τ si r > 0 ; 1 − τ si r < 0 |
| pinball ε-insensible | τ max(0, r − ε) + (1 − τ) max(0, −r − ε) | −τ si r > ε ; 1 − τ si r < −ε ; 0 sinon |
| hinge (classification) | max(0, 1 − y f) | −y · 1(y f < 1) |

Aux points anguleux, on prend le sous-gradient 0.

**Pourquoi la pinball donne le quantile.** En minimisant E[ρ_τ(Y − q)] en q :
dE/dq = −τ P(Y > q) + (1 − τ) P(Y < q) = 0, soit P(Y < q) = τ. La prévision optimale est le
quantile τ de l'occupation.

**Le tube déforme le quantile.** Avec la pinball ε-insensible, la condition devient
τ P(Y > q + ε) = (1 − τ) P(Y < q − ε) : les jours à moins de ε de q ne comptent plus. Pour un
intervalle calibré, les niveaux quantiles utilisent ε = 0 (paramètre `epsilon_quantile`).

### 3.4 Noyaux

```
linéaire :   K(x, z) = x · z
RBF :        K(x, z) = exp(−γ ‖x − z‖²)        ‖x − z‖² = ‖x‖² + ‖z‖² − 2 x·z (valeurs < 0 ramenées à 0)
composite :  K(x, z) = β K₁(x⁽¹⁾, z⁽¹⁾) + (1 − β) K₂(x⁽²⁾, z⁽²⁾),    β = σ(θ) = 1 / (1 + e^{−θ})
             ∂K/∂θ = β (1 − β) (K₁ − K₂)
```

Par le théorème du représentant, f(x) = Σ_j α_j K(x_j, x) + b : chaque jour d'entraînement vote
pour la prévision, d'autant plus fort que la situation lui ressemble ; les jours avec α_j ≠ 0 sont
les vecteurs de support. γ règle la portée du noyau RBF. Une somme pondérée positive de noyaux
valides est un noyau valide (matrice semi-définie positive). Les deux blocs du noyau composite
sont : (1) l'occupation des 7 derniers jours ; (2) les flux récents et la saison.

### 3.5 Gradients (dérivés à la main, vérifiés par différences finies)

```
Niveau 1 :  ∂J/∂w = w + C Xᵀ g                 ∂J/∂b = C Σ_i g_i
Niveaux 2-3 : ∂J/∂α = Kα + C K g = K(α + C g)   ∂J/∂b = C Σ_i g_i
Niveau 4 :  avec D = K₁ − K₂,
            ∂J/∂θ = β(1 − β) · [ ½ αᵀ D α + C gᵀ D α ]
```

**Direction préconditionnée** (modèles à noyau) : on descend selon α + C g au lieu de K(α + C g).
La matrice K, souvent presque singulière, ralentit la descente dans certaines directions ; la
direction α + C g est le gradient dans l'espace des fonctions. Elle s'annule au même point : même
solution, atteinte plus vite.

### 3.6 Optimiseurs

```
Descente de gradient :  θ ← θ − η g
Momentum :              v ← μ v + g ;  θ ← θ − η v                         (μ ≈ 0,9)
Adam :                  m ← β₁ m + (1 − β₁) g ;  v ← β₂ v + (1 − β₂) g²    (β₁ = 0,9, β₂ = 0,999)
                        m̂ = m / (1 − β₁^t) ;  v̂ = v / (1 − β₂^t)
                        θ ← θ − η m̂ / (√v̂ + ε)                              (ε = 10⁻⁸)
Décroissance du pas :   η_t = η₀ / √(1 + t/T)                               (η₀ = 0,05, T = 500)
```

La correction de biais compense le démarrage de m et v à 0 (E[m_t] ≈ (1 − β₁^t) E[g]). Avec une
perte linéaire par morceaux, le gradient ne s'annule pas près du minimum : la décroissance du pas
garantit la convergence.

**Moyenne de Polyak.** Les itérés oscillent autour du minimum ; on calcule leur moyenne sur la fin
de l'entraînement (à partir de la moitié des pas) :

```
θ̄ = (1/K) Σ_{t=T₀}^{T₀+K−1} θ_t        mise à jour : θ̄ ← θ̄ + (θ_t − θ̄)/k
```

J étant convexe, J(θ̄) ≤ (1/K) Σ J(θ_t) (inégalité de Jensen). On garde, entre la moyenne et le
meilleur point rencontré, celui dont J est le plus petit. Arrêt anticipé si J ne baisse plus
(relativement, tolérance 10⁻⁷) sur 100 pas ; dans ce cas, la moyenne porte sur les 100 derniers
points visités. Réglages par défaut : Adam, 3 000 pas au plus.

### 3.7 Intervalle de prévision

Un modèle quantile par niveau τ ∈ {0,05 ; 0,5 ; 0,95}, entraînés séparément ; les prévisions sont
triées jour par jour pour que les quantiles ne se croisent jamais. Intervalle à 90 % = [q̂_0,05 ;
q̂_0,95], prévision centrale = q̂_0,5, prévision décisionnelle = q̂_τ (τ = 0,8).

### 3.8 Empilement (niveau 5)

```
f = Σ_k w_k p_k + b         w_k = softplus(u_k) = ln(1 + e^{u_k}) > 0
J(u, b) = ½ λ Σ_k w_k² + C Σ_i L(y_i − f_i)
∂J/∂u_k = σ(u_k) · [ λ w_k + C Σ_i g_i p_ik ]         ∂J/∂b = C Σ_i g_i
```

p_k sont des prévisions **hors échantillon** (obtenues en validation glissante), sinon le
méta-modèle ferait confiance au modèle qui a appris l'entraînement par cœur. Les poids positifs
interdisent de « parier contre » un modèle.

### 3.9 Tableau d'apprentissage

Le soir du jour t (l'origine), on prévoit l'occupation du jour t + h. Chaque ligne n'utilise que
ce qui est connu au jour t.

| Bloc | Variables |
|---|---|
| occupation | y_t, y_{t−1}, …, y_{t−6} |
| flux et saison | admissions des 3 et des 7 derniers jours ; sorties des 7 derniers jours ; jour de la semaine du jour cible (7 indicatrices) ; mois du jour cible sin(2π(m − 1)/12), cos(2π(m − 1)/12) ; en option : jour cible férié, veille de férié, vacances scolaires |

Codage circulaire du mois : décembre et janvier sont voisins sur le cercle.

**Standardisation** z = (x − μ)/σ des variables continues, avec μ et σ calculés sur les **seules
lignes d'entraînement** de chaque découpage (sinon le test voit le futur). Le noyau RBF dépend des
distances : sans standardisation, une variable en dizaines écraserait une variable entre −1 et 1.
Les indicatrices 0/1 ne sont pas standardisées.

### 3.10 Validation glissante

Une ligne (origine t, cible t + h) n'est utilisable pour entraîner un modèle à l'origine O que si
t + h ≤ O.

- **Validation glissante** : l'origine O avance par pas de 14 jours (au moins 60 jours
  d'entraînement) ; à chaque O, entraînement sur toutes les lignes de cible ≤ O, validation sur
  les lignes d'origine dans [O, O + pas[. Le modèle et la standardisation sont réappris à chaque
  origine.
- **Test final** : entraînement sur les lignes dont la cible précède la période verrouillée, test
  sur les lignes dont l'origine est dans la période verrouillée ; les lignes à cheval sont écartées.
  En mode mensuel (`decoupages_test_mensuels`), un bloc par mois : le bloc du mois m est appris sur
  toutes les lignes de cible antérieure au 1er du mois m (mois de test écoulés compris).

### 3.11 Recherche des hyperparamètres

- **Grille** sur toutes les combinaisons de valeurs.
- **Essaim particulaire (PSO)** :

```
v_i ← ω v_i + c₁ r₁ (p_i − x_i) + c₂ r₂ (g − x_i)        x_i ← x_i + v_i (ramené dans les bornes)
```

p_i meilleure position de la particule, g meilleure de l'essaim, r₁ et r₂ uniformes sur [0, 1].
C et γ sont explorés en log₁₀. Graine fixe : la recherche est reproductible.

Valeurs de départ (`svr/niveaux.py`) : C = 1 ; ε = 1 lit (niveaux 1 et 2) ; ε = 0 (niveaux
quantiles) ; γ = 0,05 ; γ₁ = 0,05 et γ₂ = 0,1 (noyau composite) ; τ = 0,8.

## 4. Mathématiques B : évaluation et comparaison des modèles

Code : `svr/metriques.py`, `svr/analyse.py`, `sensibilite.py`, `benchmark_choix.py`.

### 4.1 Métriques

| Mesure | Formule |
|---|---|
| MAE | (1/n) Σ |y − ŷ| |
| RMSE | √((1/n) Σ (y − ŷ)²) |
| MAPE | (100/n) Σ |y − ŷ| / y (jours y > 0) |
| sMAPE | (100/n) Σ 2|y − ŷ| / (|y| + |ŷ|) |
| MASE | MAE / MAE du saisonnier naïf sur l'entraînement (< 1 : meilleur que la référence) |
| Biais | (1/n) Σ (ŷ − y) en Python (> 0 : surestimation) ; l'outil affiche (1/n) Σ (y − ŷ) |
| Sous-estimations | part des jours où ŷ < y |
| Pinball moyenne | (1/n) Σ ρ_τ(y − q̂_τ) |
| Couverture | part des jours où bas ≤ y ≤ haut (cible 90 % pour un intervalle à 90 %) |
| Largeur moyenne | (1/n) Σ (haut − bas) |
| Gain sur la persistance | 1 − perte(modèle) / perte(persistance) |
| Coût des décisions | c_p · lits manquants + c_s · lits vides |

Un modèle quantile à τ = 0,8 doit surestimer volontairement : il se juge sur la pinball et sur la
part de jours au-dessus de la prévision (cible ≈ 20 %), pas sur la MAE seule.

**Calibration des quantiles** : pour chaque niveau demandé τ, part observée des jours sous q̂_τ ; un
modèle bien calibré est sur la diagonale. **Importance par permutation** : hausse de l'erreur
quand on mélange un groupe de variables. **Courbe d'apprentissage** : erreur d'entraînement et de
validation selon la taille de l'historique.

### 4.2 Test de Diebold-Mariano

Deux modèles A et B sur les mêmes jours, d_t = L(e_t^A) − L(e_t^B) (valeur absolue ou carré).
Hypothèse nulle : E[d_t] = 0.

```
DM = d̄ / √(V̂ / n)        V̂ = γ̂₀ + 2 Σ_{k=1}^{h−1} γ̂_k        (autocovariances de d)
DM* = DM · √[(n + 1 − 2h + h(h − 1)/n) / n]                    (Harvey, Leybourne et Newbold)
p = 2 (1 − Φ(|DM*|))
```

Les autocovariances jusqu'au décalage h − 1 tiennent compte du fait que des prévisions à h jours
faites des jours voisins partagent des jours futurs. DM* < 0 et p < 0,05 : A est
significativement plus précis que B. Sans p < 0,05, on écrit « meilleur en moyenne, mais pas
significativement ».

### 4.3 Analyse de sensibilité à la convention des jours

Mêmes origines et mêmes hyperparamètres sur les trois séries (basse, attendue, haute). Chaque
niveau est noté en MAE (prévision centrale) et en pinball au τ décisionnel. La conclusion est
**robuste** si le meilleur niveau est le même dans les trois scénarios et si aucun gain ne change
de signe en dépassant 3 points en valeur absolue.

### 4.4 Banc de comparaison des choix (D1 à D10)

Chaque dimension change une seule chose ; chaque variante est comparée au choix retenu par
Diebold-Mariano (meilleure, équivalente ou moins bonne).

| Dimension | Question | Variantes |
|---|---|---|
| D1 | Le SVR bat-il les références et les autres modèles d'apprentissage ? | persistance, saisonnier naïf, moyennes historique et mobile, lissage simple, Thêta, Holt linéaire et amorti, lissage saisonnier, Holt-Winters additif et multiplicatif, AR(p), SARIMA, ridge, forêt aléatoire, gradient boosting, perceptron multicouche, LSTM, SVR niveaux 1 à 4 |
| D2 | Quel noyau ? | linéaire, RBF, composite |
| D3 | Quelle perte ? | carrée (ridge), ε-insensible avec ε = 0 / 0,5 / 1 / 2 |
| D4 | Quel τ selon le coût d'une pénurie ? | τ de 0,5 à 0,9 ; coût moyen pour des rapports pénurie / lit vide de 1, 2, 4, 9 |
| D5 | Quelles variables ? | retards seuls, + flux, + calendrier, complet, + fériés, + vacances, + fériés et vacances, 3 / 7 / 14 retards |
| D6 | Faut-il standardiser ? | avec, sans |
| D7 | Tout le passé ou une fenêtre ? | croissante ; 365, 180, 90 derniers jours |
| D8 | Comment optimiser ? | Adam complet, sans Polyak, sans préconditionnement, sans décroissance, momentum, descente simple |
| D9 | Combiner apporte-t-il ? | meilleur modèle seul, moyenne simple, empilement |
| D10 | La recherche d'hyperparamètres paie-t-elle ? | défaut, grille, essaim particulaire |

### 4.5 Ce que les analyses apportent aux choix du SVR

| Analyse | Choix du modèle qu'elle justifie |
|---|---|
| ACF / PACF | nombre de retards d'occupation (7, testé contre 3 et 14 en D5) |
| Corrélation croisée, Kaplan-Meier | admissions sur 3 et 7 jours ; au-delà, une admission ne pèse plus |
| Loi de Little | sorties sur 7 jours, qui complètent le bilan des flux |
| ADF + KPSS, force de la tendance | mois en sinus / cosinus ; validation glissante réentraînée |
| Kruskal-Wallis sur le jour de la semaine | indicatrices du jour, gardées seulement si D5 montre un gain |
| Surdispersion (M/G/∞), Erlang B | perte quantile τ = 0,8 |
| Spearman nettement supérieur à Pearson, résidus en courbe | noyau RBF plutôt que linéaire |
| Écarts d'échelle (CV, écart-type) | standardisation (D6) |
| Monte-Carlo | plancher d'erreur dû à la reconstitution de la cible |
| Ljung-Box des résidus du SVR | diagnostic final : p < 0,05 signifie qu'il manque un retard ou une variable |

## 5. Mathématiques C : survie, classification et transfert

### 5.1 Probabilités de sortie J0 / J1 / J2 (`svr/survie.py`, `modele_survie.py`)

**Tableau patient-jour.** Chaque séjour est découpé en jours de présence : une ligne par jour, avec
l'ancienneté k (0 = jour d'entrée) et l'événement (1 si l'enfant sort ce jour-là). Un séjour
censuré donne des lignes toutes à 0. Sortie non écrite : au jour n − 1, deux lignes « sort »
(poids p) et « reste » (poids 1 − p), puis au jour n une ligne « sort » de poids 1 − p.

**Hasard journalier** h(k, x) = P(sortir le jour d | présent au début du jour d, ancienneté k,
variables x). Pour un enfant présent ce matin :

```
P(J0) = h₀        P(J1) = (1 − h₀) h₁        P(J2) = (1 − h₀)(1 − h₁) h₂
```

Sorties attendues d'un jour = somme des probabilités des enfants présents.

**Risques concurrents** : un hasard par cause c (domicile, transfert, décès, autre), h = Σ_c h_c,
P(sortie par c le jour J1) = (1 − h₀) h_{c,1}.

**Références** :
- table de survie (actuarielle) : h(k) = Σ poids des sorties à k / Σ poids des présents à k ;
- loi gamma ajustée par les moments (a = m²/v, θ = v/m), sortie le jour ⌊T⌋ :
  h(k) = [F(k + 1) − F(k)] / [1 − F(k)], F(x) = P(a, x/θ) (gamma incomplète régularisée).

### 5.2 SVM de classification à coûts asymétriques (`svr/classification.py`)

```
J(w, b) = ½ ‖w‖² + Σ_i C_i max(0, 1 − y_i f(x_i))        y_i ∈ {−1, +1},  f(x) = w·x + b
∂J/∂w = w − Σ_i C_i y_i x_i 1(y_i f_i < 1)               ∂J/∂b = −Σ_i C_i y_i 1(y_i f_i < 1)
```

C_i = C₊ pour les positifs, C₋ pour les négatifs, multiplié par le poids de l'exemple. Choix
usuel pour des classes déséquilibrées : C₊ / C₋ = n₋ / n₊.

**Calibration de Platt** sur des données non utilisées pour l'entraînement :

```
P(y = 1 | f) = 1 / (1 + exp(A f + B))
cibles adoucies : t₊ = (N₊ + 1)/(N₊ + 2),  t₋ = 1/(N₋ + 2)
L = −Σ w_i [t_i ln p_i + (1 − t_i) ln(1 − p_i)]
∂L/∂A = Σ w_i (t_i − p_i) f_i        ∂L/∂B = Σ w_i (t_i − p_i)
```

**Mesures** : score de Brier (1/Σw) Σ w_i (p_i − y_i)² ; log-loss
−(1/Σw) Σ w_i [y ln p + (1 − y) ln(1 − p)] ; AUC = probabilité qu'un positif ait un score plus
élevé qu'un négatif (statistique de Mann-Whitney, calcul en O(n log n), ex æquo comptés pour
moitié).

### 5.3 Modèle propre ou transfert, pour les autres services (`transfert.py`)

Six stratégies sur les mêmes jours du service cible, plus la persistance :

| Stratégie | Apprend sur | Réglages (hyperparamètres) |
|---|---|---|
| **P · modèle propre** (retenue) | la cible seule | choisis sur la cible, par validation imbriquée |
| A · local | la cible seule | ceux de la pédiatrie, gelés |
| B · transfert direct | la pédiatrie seule, en taux | ceux de la pédiatrie |
| C · groupé | pédiatrie et cible réunies, en taux | ceux de la pédiatrie |
| G1 · modèle unique, période commune | tous les services, en taux, jours où tous ont des données | ceux de la pédiatrie |
| G2 · modèle unique, toute la période | tous les services, en taux, tous leurs jours | ceux de la pédiatrie |

**Pourquoi un modèle propre.** Avec environ un an d'historique (médecine femme : août 2025 → octobre 2026),
un service a assez de jours pour apprendre seul et pour régler ses propres hyperparamètres ; une population
adulte ne ressemble pas à la pédiatrie (durées, causes, saisons). A, B et C restent dans le banc : le test de
Diebold-Mariano contre P dit si le transfert apporte encore quelque chose.

**Modèle unique (G1, G2).** Les registres des services se chevauchent dans le temps : un seul modèle peut
apprendre sur tous les services à la fois, en taux d'occupation (présents ÷ lits, pour comparer des services de
tailles différentes), avec une variable indicatrice par service x_s ∈ {0, 1} pour que chaque service garde son
niveau. Dans le noyau composite, les indicatrices entrent dans le bloc « flux et saison » :

```
K(x, z) = β K₁(occupation) + (1 − β) K₂(flux, saison, service)
```

deux jours de services différents se ressemblent donc moins que deux jours du même service. Tous les services
sont évalués aux mêmes origines (une seule validation, un seul verrou). G1 n'apprend que sur la période où
tous les services ont des données ; G2 garde toute la période de chaque service (plus de données, mais la
pédiatrie pèse davantage). Le modèle unique apprend les rythmes communs à tout l'hôpital (semaine, fériés,
épidémies) ; il impose en revanche des réponses proches à des populations différentes. Le test de
Diebold-Mariano contre P tranche, service par service et pour le total de l'hôpital.

**Validation imbriquée (rien du futur).** À chaque origine O de la validation glissante, avec les seules
lignes connues au soir de O : apprentissage interne sur les cibles ≤ O − v, évaluation interne sur les
origines de ]O − v, O] (v = 56 jours, `--validation-interne`) ; la grille part des réglages de la pédiatrie,
C × {0,3 ; 1 ; 3} et portées γ, γ₁, γ₂ × {0,5 ; 1 ; 2} (9 modèles), critère pinball au quantile τ ; à égalité,
les réglages de la pédiatrie sont gardés. Le modèle est ensuite réentraîné sur tout ce qui est connu avec les
réglages gagnants. Le rapport compte les réglages choisis à chaque origine : s'ils changent sans cesse, le
réglage est instable (trop peu de jours) et A est plus sûre.

**Limite.** Un an ne montre chaque saison qu'une fois : le modèle propre ne sépare pas un effet de saison d'un
hasard de cette année-là (la variable « mois » est à tester dans le banc, pas à supposer utile).

**Passage aux taux.** Avec N lits, Y = N y. Les pertes ε-insensible et pinball sont positivement
homogènes : L_ε(N r) = N L_{ε/N}(r). En posant f = N f_r et α = N α_r :

```
J_N = N² · [ ½ α_rᵀ K α_r + (C/N) Σ L_{ε/N}(y − f_r) ]
⇒  C_taux = C / N        ε_taux = ε / N        (γ inchangé : variables standardisées)
```

**Total de l'hôpital** = somme des prévisions centrales des services. La somme des quantiles 80 %
n'est pas le quantile 80 % de la somme : le total n'est noté que sur sa prévision centrale.

## 6. Fichier par fichier

### `svr/` : les modèles

| Fichier | Contenu |
|---|---|
| `pertes.py` | ε-insensible, pinball, pinball ε-insensible, hinge, et leurs dérivées |
| `noyaux.py` | noyaux linéaire, RBF, composite |
| `optimiseurs.py` | descente de gradient, momentum, Adam, décroissance du pas |
| `modeles.py` | `ModeleSVR` (boucle, meilleur point, moyenne de Polyak), `SVRLineaire`, `SVRNoyau`, `SVRNoyauComposite`, `IntervalleQuantile` |
| `niveaux.py` | `Hyperparametres` et `fabrique(niveau, hp)` des niveaux 1 à 4 |
| `empilement.py` | niveau 5 (poids softplus) |
| `caracteristiques.py` | tableau d'apprentissage, standardisation, options de variables (fériés, vacances, nombre de retards) |
| `validation.py` | validation glissante, découpage final |
| `references.py` | niveau 0 et intervalle naïf |
| `classiques.py` | Holt-Winters additif amorti (réglé par grille), régression ridge |
| `series_classiques.py` | références sur la série seule : Nelder-Mead, lissages exponentiels, Thêta, Holt-Winters, AR(p), SARIMA (CSS, choix d'ordre) ; évaluation réestimée à chaque origine avec quantiles empiriques |
| `metriques.py` | métriques et Diebold-Mariano avec correction HLN |
| `recherche.py` | grille et essaim particulaire |
| `analyse.py` | Pearson, Spearman, ACF, PACF, profils, calibration, courbe d'apprentissage, importance par permutation, coût des décisions |
| `classification.py` | SVM à coûts par exemple, Platt, Brier, log-loss, AUC |
| `survie.py` | tableau patient-jour, hasard, J0/J1/J2, table de survie, loi gamma |
| `calendrier.py` | jours fériés (Pâques calculée), fêtes musulmanes et vacances lues dans `donnees/` |
| `reproductibilite.py` | fiche d'environnement (versions, commande, commit, paramètres), la même que celle du traitement des données |
| `concurrents.py` | concurrents du SVR, écrits à la main : arbre CART, forêt aléatoire quantile (Meinshausen), gradient boosting quantile, perceptron multicouche et LSTM quantiles (rétropropagation à la main) ; même tableau de variables et même validation que le SVR ; dans la dimension D1 |

## 7. Les scripts, dans l'ordre

Toutes les sorties vont dans `resultats/`. Chaque script écrit une fiche
`*_environnement.json` (versions, commande, commit, paramètres) pour la reproductibilité.

### Étape 1 : `traitement.rapport_occupation`, de l'export à l'occupation

Le traitement des données vient du dépôt [outil-saisi](https://github.com/drew22109267/outil-saisi) (paquet
`traitement`, installé une fois, voir section 2) ; on le lance d'ici pour que ses résultats arrivent dans
`resultats/`, où les étapes suivantes les lisent :

```bash
~/memoire-env/bin/python -m traitement.depuis_outil <CSV de l'outil> --service PED --sortie donnees/export_outil_PED.csv
~/memoire-env/bin/python -m traitement.rapport_occupation donnees/export_outil_PED.csv --service PED --lits <N> --comptage minuit
```

Affiche la convention des jours mesurée, les séjours gardés et écartés, la période exploitable,
l'occupation et sa fourchette, la loi de Little et Erlang B, les indicateurs par mois. Écrit
`occupation_PED.csv` (et ses versions basse et haute), `indicateurs_PED_par_mois.csv`,
`indicateurs_PED_par_annee.csv`, `occupation_PED.png`, le diagramme de flux des données
(`flux_donnees_PED.csv` / `.png`) et la liste des reports suspects (`reports_PED.csv`).

Options : `--lits-fichier donnees/lits_PED.csv` (capacité variable, fichier `date_debut;lits`) ;
`--reports retirer` (fusion des reports confirmés, seulement après confirmation par le service).

### Étape 2 : `lancer_niveaux.py`, ablation des niveaux 0 à 5

```bash
~/memoire-env/bin/python lancer_niveaux.py --service PED --horizons 1 3 7 --tau 0.8 --recherche grille
```

Validation glissante sur les 6 mois avant le verrou, une origine tous les 14 jours. Options :
`--recherche pso`, `--scenario basse|haute`, `--pas`, `--debut-validation`. Écrit
`ablation_PED_h<h>.csv`, `ablation_PED_tests.csv` (Diebold-Mariano) et
`hyperparametres_PED_h<h>.json` (relu par les étapes suivantes).

### Étape 3 : `sensibilite.py`, robustesse à la convention des jours

```bash
~/memoire-env/bin/python sensibilite.py --service PED --horizons 1 3 7
```

Écrit `sensibilite_PED.csv` et `sensibilite_PED_synthese.csv` (verdict robuste ou sensible).

### Étape 3 bis : `benchmark_choix.py`, chaque choix face à ses alternatives

```bash
~/memoire-env/bin/python benchmark_choix.py --service PED --horizons 1 7
```

Options : `--dimensions D1 D5`, `--pas` (28 par défaut), `--rapide`. Écrit
`benchmark_PED_<D>_h<h>.csv` et `benchmark_PED.md` (tableaux et conclusions prêts pour le mémoire).

### Étape 3 ter : `benchmark_pretraitement.py`, chaque choix de prétraitement

```bash
~/memoire-env/bin/python benchmark_pretraitement.py donnees/<export>.csv --service PED --lits 20 --horizons 1 7
```

Sept dimensions, une décision changée à la fois : durées inconnues (P1), fenêtre de censure (P2),
convention des jours (P3), patients reportés (P4), période exploitable (P5), fin de série (P6), trous de
saisie (P7). Comme la série cible change avec le prétraitement, chaque variante est jugée deux fois : contre
sa propre série (reste-t-elle prévisible ?) et contre la série retenue sur les mêmes jours (change-t-elle les
prévisions ? test de Diebold-Mariano). Écrit `pretraitement_PED_<P>_h<h>.csv` et `pretraitement_PED.md`.

### Étape 3 quater : `benchmark_parametres.py`, sensibilité de tous les paramètres

```bash
~/memoire-env/bin/python benchmark_parametres.py --service PED --horizons 1 7
```

Un paramètre varie à la fois autour de sa valeur retenue, tout le reste fixé, sur les mêmes jours :
SVR niveau 4 (C, ε, γ₁, γ₂, τ, η₀, itérations, décroissance, Polyak, tolérance, préconditionnement,
optimiseur), SVR niveau 2 (C, ε, γ), forêt, boosting, perceptron, LSTM, nombre de jours de retard.
Pour chaque paramètre : tableau, Diebold-Mariano contre la valeur retenue, figure de l'erreur selon la valeur,
et amplitude (MAE max − MAE min) / MAE retenue. Option `--familles svr4 foret …`. Écrit
`parametres_PED_<famille>_<paramètre>_h<h>.csv` / `.png`, `parametres_PED_synthese.csv` et `parametres_PED.md`.

### Étape 4 : `visualisations.py`, toutes les figures

```bash
~/memoire-env/bin/python visualisations.py --service PED
```

### Étape 5 : `validation_finale.py`, une seule fois, à la toute fin

```bash
~/memoire-env/bin/python validation_finale.py donnees/<export>.csv --service PED --lits <N> \
    --extraction <aaaa-mm-jj> --confirmation "J'ouvre le coffre pour la validation finale"
```

Chaque niveau, avec ses hyperparamètres retenus, est entraîné sur tout ce qui précède le verrou,
puis prévoit septembre ; il est réentraîné au 30 septembre (septembre inclus), puis prévoit octobre.
Écrit `validation_finale_PED_h<h>.csv` (total), `validation_finale_PED_h<h>_par_mois.csv` (septembre seul =
test à 1 mois, octobre) et les tests de Diebold-Mariano. Option `--reentrainement aucun` : un seul
entraînement pour les deux mois (fichiers suffixés `_sans_reentrainement`), pour mesurer l'apport du
réentraînement mensuel. Les deux variantes se lancent dans la même séance d'ouverture du coffre.

### Étape 6 : `modele_survie.py`, probabilités de sortie J0 / J1 / J2

```bash
~/memoire-env/bin/python modele_survie.py donnees/<export>.csv --service PED --lits <N> --causes
```

Écrit `survie_PED.md` / `.csv`, trois figures et `survie_PED_modele.json` (paramètres du modèle,
sans aucune donnée de patient).

### Étape 7 : `transfert.py`, services à historique court et total de l'hôpital

```bash
~/memoire-env/bin/python transfert.py donnees/<export>.csv --source PED --cibles MED CHI \
    --lits PED=20 MED=24 CHI=18 --horizons 1 7
```

Écrit `transfert_<SERVICE>_h<h>.csv`, `transfert_total_h<h>.csv` et `transfert.md`.

### À part

```bash
~/memoire-env/bin/python demo_entrainement.py --exercice
```

`demo_entrainement.py` affiche J, ‖∇J‖ et les paramètres pendant l'entraînement d'un petit exemple
dont la solution exacte est connue (J = 1,5833).

## 8. Les figures et leur lecture

Écrites dans `resultats/figures_<SERVICE>/`.

| Figure | Contenu | Lecture |
|---|---|---|
| `01_serie_occupation` | occupation chaque soir, fourchette, capacité | bande large = beaucoup de sorties non écrites |
| `02_profils` | moyennes par jour de la semaine et par mois | justifie ou non les variables de calendrier |
| `03_autocorrelation` | ACF et PACF jusqu'à 35 jours | décroissance lente = forte mémoire ; pics à 7, 14, 21 = rythme hebdomadaire |
| `04_correlations` | Pearson et Spearman entre variables et cible | Pearson différent de Spearman = relation courbe |
| `05_relations` | cible face aux principales variables | nuage serré = variable informative |
| `06_nuage_3d` | jours dans l'espace (occupation, admissions 7 j, cible) | plan suffisant ou surface courbe nécessaire |
| `07_hyperplan_svr_3d` | SVR linéaire : plan, tube ± ε, vecteurs de support | seuls les points sur ou hors du tube déterminent le plan |
| `08_surface_svr_rbf_3d` | SVR RBF : surface médiane et quantiles 5 % / 95 % | les points doivent tomber entre les deux grilles 9 fois sur 10 |
| `09_convergence` | J(t)/J(0) pendant l'entraînement | doit descendre puis se stabiliser |
| `10_courbe_apprentissage` | erreurs selon la longueur de l'historique | courbes qui se rapprochent = assez de données |
| `11_hyperparametres` | erreur de validation selon C et γ | large zone sombre = choix peu sensible |
| `12_previsions` | médiane, quantile τ, intervalle 90 %, réalité, persistance | la réalité doit rester dans la bande |
| `13_residus` | histogramme et évolution des erreurs | centré sur 0 = pas de biais ; dérive = réentraîner |
| `14_calibration` | couverture observée contre niveau demandé | sous la diagonale = sous-estimation des besoins |
| `15_ablation` | MAE et RMSE des niveaux 0 à 5 | chaque niveau doit améliorer le précédent |
| `16_sensibilite` | gain selon la convention des jours | barres de même signe = conclusion robuste |
| `17_importance_variables` | importance par permutation | barre proche de 0 = variable inutile |

Le module lit fait de la **régression** : l'hyperplan ne sépare pas deux classes, il passe au
milieu des données avec un tube de tolérance ± ε. L'hyperplan séparateur viendra avec le module
triage (classification).

## 9. Tests

```bash
~/memoire-env/bin/python -m pytest tests -q
```

| Fichier | Ce qui est vérifié |
|---|---|
| `test_svr.py` | pertes et dérivées, noyaux, gradients des SVR par différences finies, Adam, convergence vers la solution exacte, tableau sans fuite |
| `test_analyse.py` | Pearson, rangs avec ex æquo, Spearman, ACF, PACF, calibration, profils |
| `test_survie_transfert.py` | Polyak après arrêt anticipé, gradient du SVM classifieur, Platt, AUC et Brier, gamma incomplète, tableau patient-jour, table de survie, J0/J1/J2, conversion des hyperparamètres en taux |
| `test_series_classiques.py` | Nelder-Mead, lissage sur série constante, Holt sur une droite exacte, Holt-Winters sur une semaine exacte, AR(1) retrouvé, SARIMA AR(1) retrouvé, quantiles ordonnés, **aucune fuite du futur** pour tous les modèles de référence |
| `test_concurrents.py` | gradients du perceptron et du LSTM par différences finies, arbre sur une marche, forêt (quantiles ordonnés, couverture), boosting (baisse de la perte), interface commune des quatre concurrents |
| `test_ajouts.py` | Pâques et fériés, Holt-Winters, ridge, options des variables, coût des décisions, importance par permutation |
| `test_calendrier.py` | concordance des jours fériés et des vacances entre Python, JavaScript et les fichiers de données |

`test_calendrier.py` lit les fichiers de `donnees/` (présents localement) et `calendrier.js` du dépôt
outil-saisi, cherché à côté de ce dépôt ou dans la variable `OUTIL_SAISI` ; sans lui, ce test est sauté.

Les tests du traitement des données (occupation, indicateurs, verrou, reports, capacité variable) et la
vérification complète des calculs (outil de saisie = Python = calcul direct, statistiques contre scipy et
statsmodels) sont dans le dépôt [outil-saisi](https://github.com/drew22109267/outil-saisi).

## 10. État d'avancement et suite du travail

| Partie | État |
|---|---|
| Traitement des données (dépôt outil-saisi) : occupation selon trois méthodes, pic, capacité variable, indicateurs, garde-fous | fait, testé, vérifié (outil = Python = calcul direct) |
| **Module lit** : SVR niveaux 1 à 5, optimiseurs, validation glissante, Diebold-Mariano, recherche d'hyperparamètres | fait, gradients vérifiés |
| Module lit : bancs D1 à D11, P1 à P8, paramètres ; références (lissages, Thêta, AR, SARIMA) ; concurrents (forêt, boosting, MLP, LSTM) | fait, à lancer sur la version finale de la saisie |
| Module lit : jours fériés et vacances camerounais, modèle de survie J0/J1/J2, transfert, total de l'hôpital | fait, testé |
| Module lit : exécution complète sur les données réelles | en cours (saisie corrigée progressivement) |
| Module lit : validation finale sur la période verrouillée (septembre puis octobre 2026, réentraînement mensuel) | écrite, à lancer une seule fois à la toute fin |
| **Module triage** | non opérationnel : voir [`../module_triage/README.md`](../module_triage/README.md) |
| Branchement à l'application NERA (`PrevisionCapaciteService` de l'API) | à faire, quand le module lit sera validé |

Suite du travail, dans l'ordre :

1. Terminer la saisie et corriger les données (dates incohérentes, doublons, numéros manquants),
   puis mesurer le taux d'erreur de saisie (onglet Contrôle qualité, au moins 20 pages).
2. Valider la reconstitution : comptages réels dans le bilan des flux, intervalle de Monte-Carlo.
3. Faire l'analyse descriptive et l'analyse de la série (outil-saisi, `MATHEMATIQUES.md`, sections 3 et 4)
   pour fixer les entrées.
4. Exporter le dataset harmonisé, lancer les étapes 1 à 4 et le banc de comparaison.
5. Comparer le SVR retenu au naïf, aux lissages, à AR et SARIMA (MAE, RMSE, MASE, pinball,
   couverture, Diebold-Mariano) ; vérifier ses résidus (ACF, Ljung-Box).
6. Lancer la validation finale une seule fois.
7. Pistes à mesurer par le banc avant adoption : sorties attendues du modèle de survie comme
   variable d'entrée ; variable « présents attendus » Σ_k A_{t−k} Ŝ(k) ; référence quantile d'une
   loi de Poisson ou binomiale négative de moyenne λ̂W.

## 11. Références

- Kaplan E. L., Meier P. (1958). Nonparametric estimation from incomplete observations. *JASA*.
- Greenwood M. (1926). The natural duration of cancer. *Reports on Public Health and Medical Subjects*.
- Mantel N. (1966). Evaluation of survival data and two new rank order statistics. *Cancer Chemotherapy Reports*.
- Little J. D. C. (1961). A proof for the queuing formula L = λW. *Operations Research*.
- Erlang A. K. (1917). Solution of some problems in the theory of probabilities of significance in automatic telephone exchanges.
- Vapnik V. (1995). *The Nature of Statistical Learning Theory*. Springer.
- Smola A. J., Schölkopf B. (2004). A tutorial on support vector regression. *Statistics and Computing*.
- Koenker R., Bassett G. (1978). Regression quantiles. *Econometrica*.
- Gönen M., Alpaydın E. (2011). Multiple kernel learning algorithms. *JMLR*.
- Wolpert D. H. (1992). Stacked generalization. *Neural Networks*.
- Kingma D. P., Ba J. (2015). Adam: a method for stochastic optimization. *ICLR*.
- Polyak B. T., Juditsky A. B. (1992). Acceleration of stochastic approximation by averaging. *SIAM J. Control Optim.*
- Kennedy J., Eberhart R. (1995). Particle swarm optimization. *IEEE ICNN*.
- Platt J. (1999). Probabilistic outputs for support vector machines.
- Diebold F. X., Mariano R. S. (1995). Comparing predictive accuracy. *JBES*.
- Harvey D., Leybourne S., Newbold P. (1997). Testing the equality of prediction mean squared errors. *IJF*.
- Hyndman R. J., Athanasopoulos G. *Forecasting: Principles and Practice*.
- Wang X., Smith K., Hyndman R. J. (2006). Characteristic-based clustering for time series data. *DMKD*.
- Ljung G. M., Box G. E. P. (1978). On a measure of lack of fit in time series models. *Biometrika*.
- Dickey D. A., Fuller W. A. (1979). Distribution of the estimators for autoregressive time series with a unit root. *JASA*.
- Kwiatkowski D., Phillips P., Schmidt P., Shin Y. (1992). Testing the null hypothesis of stationarity. *J. Econometrics*.
- Horn J. L. (1965). A rationale and test for the number of factors in factor analysis. *Psychometrika*.
- Kaiser H. F. (1974). An index of factorial simplicity. *Psychometrika*.
- Meeus J. (1991). *Astronomical Algorithms*.
- Press W. H. et al. *Numerical Recipes* (fonctions gamma et bêta incomplètes).

