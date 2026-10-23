# Modèle NERA, module triage : mathématiques et justification de chaque choix

Ce document explique, pour le triage aux urgences : la cible, les variables, chaque modèle (fonction de coût,
fonction minimisée, gradients), la calibration, la décision, la validation, les mesures et les bancs. Les
briques communes avec le module lit (Adam, meilleur point, arrêt anticipé, moyenne de Polyak, SVM linéaire à
coûts, Platt, AUC, Brier) sont démontrées dans [`../module_lit/README.md`](../module_lit/README.md) et dans
`../module_lit/svr/classification.py`.

## 1. La cible

Chaque passage i reçoit une étiquette y_i ∈ {−1, +1} tirée de la décision écrite par le médecin :

| Décision | Classe | Raison |
|---|---|---|
| Hospitalisé, référé, décédé | +1 (grave) | le patient avait besoin de soins hospitaliers |
| Sortie contre avis médical (SCAM) | +1 | le médecin voulait le garder : il le jugeait grave |
| Externe | −1 (non grave) | retour à domicile |
| Mise en observation (MEO) | selon le banc T1 | cas intermédiaire : grave, non grave ou exclue |

**Limite à écrire dans le mémoire.** La cible est la décision du médecin, pas l'état réel du patient : le
modèle apprend à reproduire les décisions du service. Un patient renvoyé à tort à domicile compte comme non
grave.

## 2. Les variables

Toutes sont connues **à l'arrivée** du patient.

- **Base** : âge (années), sexe féminin (0/1), poids, et les constantes sous l'une des trois formes du banc T5 :
  - brute : x ;
  - écart à la norme de l'âge : e⁺ = max(0, (x − haut)/haut), e⁻ = max(0, (bas − x)/bas) ;
  - seuil : 1(x > haut), 1(x < bas).
- **Plaintes** : 18 indicatrices de familles (fièvre, convulsions, détresse respiratoire, trouble de la
  conscience, traumatisme…) et le nombre de plaintes. La liste des familles est **fixée à l'avance** : choisir
  les mots les plus fréquents sur les données serait déjà apprendre sur les passages à prévoir.
- **Contexte** : garde de nuit, permanence, week-end, mois (sinus et cosinus de 2π(m − 1)/12, voir le guide des
  modèles, section 1.1).
- **Valeurs manquantes** : une indicatrice par constante (1 si elle n'a pas été prise).

**Pourquoi l'écart à la norme.** Le danger d'une constante est souvent des deux côtés : un pouls trop rapide
ou trop lent est grave. Avec la variable brute, un modèle linéaire ne peut dire que « plus c'est haut, plus
c'est grave » (ou l'inverse) ; avec e⁺ et e⁻, il donne un poids à chaque côté. Et la même valeur n'a pas le
même sens à tout âge : 140/min est normal à 1 an, inquiétant à 30 ans. L'écart à la norme de l'âge rend les
patients comparables.

**Plages normales retenues** (`triage/normes.py`, à valider avec le service) :

| Constante | Enfant | Adulte |
|---|---|---|
| Pouls | < 1 an 100–160 ; 1–2 ans 90–150 ; 2–5 ans 80–140 ; 5–12 ans 70–120 ; 12–15 ans 60–100 | 50–100 |
| FR | haut : < 2 mois 60 ; < 1 an 50 ; < 5 ans 40 ; < 12 ans 30 ; sinon 24 (OMS) ; bas : 25, 20, 14, 10 | 10–22 (qSOFA) |
| TA systolique | bas : < 1 mois 60 ; < 1 an 70 ; 1–10 ans 70 + 2 × âge ; > 10 ans 90 | 90–180 |
| TA diastolique | — | haut 110 |
| Température | 36–38 °C | 36–38 °C |
| SpO2 | bas 92 % | bas 92 % |
| Glycémie | 0,6–2,5 g/L | 0,6–2,5 g/L |

**Préparation sans fuite.** Pour chaque mois évalué, la médiane de chaque colonne (pour remplacer les valeurs
manquantes), puis la moyenne μ et l'écart-type σ des colonnes continues (z = (x − μ)/σ) sont calculés sur les
passages d'apprentissage seulement, puis appliqués tels quels aux autres passages (`Preparateur`).

## 3. Les modèles

Chaque modèle donne un score f(x) (grand = grave). Le coût d'une erreur dépend de la classe :
C_i = C · C₊ si le passage i est grave, C · C₋ sinon (section 5).

### 3.1 Règle de seuils (référence)

f(x) = nombre de constantes hors de leur plage normale. Rien n'est appris. C'est ce que fait un soignant qui
applique une grille d'alerte : c'est la **barre à battre**.

### 3.2 Régression logistique pondérée

    f(x) = w·x + b
    J(w, b) = ½ ‖w‖² + Σ_i C_i ln(1 + e^{−y_i f_i})

Avec m = y f, la dérivée de ln(1 + e^{−m}) est −e^{−m}/(1 + e^{−m}) = −1/(1 + e^{m}) = −σ(−m). Donc, avec
g_i = −C_i y_i σ(−y_i f_i) :

    ∂J/∂w = w + Σ_i g_i x_i = w + Xᵀ g          ∂J/∂b = Σ_i g_i

### 3.3 SVM linéaire à coûts

    J(w, b) = ½ ‖w‖² + Σ_i C_i max(0, 1 − y_i f_i)
    ∂J/∂w = w − Σ_i C_i y_i x_i 1(y_i f_i < 1)          ∂J/∂b = − Σ_i C_i y_i 1(y_i f_i < 1)

La logistique et le SVM ont la même forme de modèle ; seule la perte change : la perte log ne s'annule jamais
(tous les passages comptent un peu), la hinge s'annule au-delà de la marge 1 (seuls les passages difficiles,
les vecteurs de support, fixent la frontière).

### 3.4 SVM à noyau (RBF et composite)

Par le théorème du représentant, f(x) = Σ_j α_j K(x_j, x) + b, donc f = Kα + b sur l'apprentissage, et

    J(α, b) = ½ αᵀ K α + Σ_i C_i max(0, 1 − y_i f_i)

Avec g_i = ∂L_i/∂f_i = −C_i y_i 1(y_i f_i < 1) et ∂f_i/∂α = K[i, :] (K symétrique) :

    ∂J/∂α = Kα + K g = K(α + g)          ∂J/∂b = Σ_i g_i

La descente suit la direction préconditionnée α + g : quand K est inversible, K(α + g) = 0 ⇔ α + g = 0, donc la
solution est la même, atteinte plus vite (même démonstration que le SVR à noyau du module lit). Les tests
vérifient que le vrai gradient K(α + g) coïncide avec les différences finies.

- **RBF** : K(x, z) = exp(−γ ‖x − z‖²), γ = portée/d (d variables standardisées : ‖x − z‖² grandit comme d).
- **Composite** : K = ½ K₁ + ½ K₂, K₁ RBF sur l'âge et les constantes (γ₁ = portée/d₁), K₂ RBF sur les plaintes,
  le contexte et les indicatrices (γ₂ = portée/d₂). Deux patients se ressemblent s'ils se ressemblent par
  leurs constantes **ou** par leurs plaintes : une variable sans rapport avec la gravité dilue moins la
  ressemblance que dans un seul RBF sur toutes les variables. Le poids est fixé à ½ : avec quelques centaines
  de passages, apprendre β en plus serait fragile.

**Constat sur un cas d'essai** (deux variables utiles sur 32, environ 90 passages d'apprentissage) : le RBF à
portée trop courte surapprend (AUC de 0,98 à γ = 0,01, de 0,63 à γ = 0,2), d'où une grille de portées qui
descend jusqu'à 0,25/d, et l'intérêt du noyau composite.

### 3.5 Arbre et forêt

Un arbre CART (celui du module lit, `svr.concurrents.Arbre`) est appris sur la cible 0/1. Dans une feuille de
n passages dont n₁ graves, avec p = n₁/n, la somme des carrés des écarts vaut
Σ (y − p)² = n₁(1 − p)² + (n − n₁)p² = n p(1 − p) : minimiser la somme des carrés, c'est minimiser l'impureté
de Gini. La valeur d'une feuille est p. La forêt fait la moyenne de 200 arbres appris sur des échantillons
bootstrap, avec √d variables tirées à chaque coupure.

## 4. La calibration de Platt et la décision

Le score f n'est pas une probabilité. On ajuste, sur des passages **non utilisés pour apprendre le modèle**,

    P(grave | f) = 1 / (1 + exp(A f + B))

par maximum de vraisemblance avec les cibles adoucies de Platt (`svr.classification.CalibrationPlatt`). Tous
les modèles passent par la même calibration : ils sont comparés à armes égales.

**Le seuil.** Avec c₊ le coût d'un grave manqué et c₋ celui d'une fausse alerte, pour un patient de
probabilité p : alerter coûte en moyenne c₋(1 − p), ne pas alerter coûte c₊ p. On alerte si
c₊ p ≥ c₋ (1 − p), c'est-à-dire

    p ≥ s* = c₋ / (c₊ + c₋) = 1 / (1 + c₊/c₋)          (c₊/c₋ = 4 : s* = 0,2)

C'est le même raisonnement que le quantile τ = c_pénurie/(c_pénurie + c_surcapacité) du module lit.

## 5. Les coûts de classe C₊/C₋ (banc T3)

- **égaux** : C₊ = C₋ = 1 ;
- **équilibrés** : C₊/C₋ = n₋/n₊ ; alors Σ_{graves} C₊ = n₊ · n₋/n₊ = n₋ = Σ_{non graves} C₋ : chaque classe
  pèse autant au total ;
- **rapport du service** : C₊/C₋ = c₊/c₋.

Les coûts de classe déplacent la frontière **pendant l'apprentissage** ; le seuil s* décide **après** la
calibration. Les deux ne font pas double emploi : Platt corrige l'échelle des scores, de sorte que la décision
finale dépend surtout de s* ; le banc T3 mesure ce que les coûts de classe ajoutent.

## 6. La validation

Pour chaque mois M (à partir du troisième mois de données, `--mois-min 2`) :

1. **entraînement** : tous les passages avant le 1er du mois M, rangés dans l'ordre du temps ;
   - les premiers 75 % : **apprentissage** du modèle (et de la préparation des variables) ;
   - les derniers 25 % : **calibration** : choix des réglages (C ∈ {0,1 ; 1 ; 10}, portée ∈ {0,25 ; 0,5 ; 1 ; 2})
     par la meilleure AUC, puis ajustement de Platt sur les scores du modèle choisi ;
2. **évaluation** : les passages du mois M, jamais vus.

La calibration suit l'apprentissage dans le temps : elle ressemble au mois à prévoir. Le choix des réglages et
la calibration utilisent les mêmes passages : la probabilité peut en être un peu trop confiante, ce que le
score de Brier mesure. Rien n'est lu à partir du 01/09/2026 (verrou du test final, `traitement.verrou`).

## 7. Les mesures

Matrice de confusion (alerte si P ≥ s*) : VP, FN (graves manqués), FP (fausses alertes), VN.

| Mesure | Formule | Lecture |
|---|---|---|
| sensibilité | VP/(VP + FN) | part des graves détectés : **prioritaire** |
| sous-triage | FN/(VP + FN) | graves manqués |
| spécificité | VN/(VN + FP) | |
| sur-triage | FP/(VN + FP) | fausses alertes parmi les non graves |
| VPP | VP/(VP + FP) | part des alertes justifiées |
| coût moyen | (c₊ FN + c₋ FP)/n | la quantité que le seuil s* rend la plus petite possible |
| AUC | P(score d'un grave > score d'un non grave) | indépendante du seuil |
| Brier, log-loss | (1/n) Σ (p − y)² ; −(1/n) Σ [y ln p + (1 − y) ln(1 − p)] | qualité des probabilités |

**Test de McNemar.** Deux modèles A et B, mêmes passages. Seuls les désaccords comptent : b = A juste et B faux,
c = A faux et B juste. Si A et B se valent, chaque désaccord est un « pile ou face » : b suit une loi
binomiale (b + c, ½).
- b + c ≥ 25 : χ² = (|b − c| − 1)²/(b + c) (correction de continuité), et p = P(χ²₁ ≥ χ²) = 2(1 − Φ(√χ²)), car un
  χ² à un degré de liberté est le carré d'une loi normale centrée réduite.
- b + c < 25 : test exact, p = min(1, 2 Σ_{k ≤ min(b, c)} C(b + c, k)/2^{b+c}).
Exemple : b = 20, c = 10 donne χ² = 81/30 = 2,7 et p ≈ 0,10 : pas de différence significative.

## 8. Registre des décisions

| Décision | Retenu | Alternatives | Raison | Banc |
|---|---|---|---|---|
| Unité | le passage | le jour | la décision se prend patient par patient | — |
| Groupes | enfants et adultes séparés | un modèle commun | physiologie et normes différentes (protocole) | T6 |
| Cible MEO | grave | non grave, exclue | l'observation traduit une inquiétude du médecin | T1 |
| Modèle | SVM RBF | règle, logistique, arbre, forêt, SVM linéaire, composite | relations non linéaires, coûts dans la perte | T2 |
| Coûts de classe | équilibrés | égaux, rapport du service | classes souvent déséquilibrées | T3 |
| Variables | constantes, plaintes, contexte, manquants | sous-ensembles | ne garder que ce qui aide | T4 |
| Constantes | écart à la norme de l'âge | brutes, seuils | danger des deux côtés, âges comparables | T5 |
| Diagnostic | exclu | variable | écrit après l'examen : fuite | — |
| Probabilité | Platt sur la calibration | score brut | une alerte se décide sur une probabilité | — |
| Seuil | s* = 1/(1 + c₊/c₋) | 0,5 | minimise le coût moyen attendu | — |
