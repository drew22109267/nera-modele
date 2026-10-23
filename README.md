# NERA : modèle de prévision pour la gestion hospitalière

*Mémoire : application des machines à vecteurs de support (SVM) aux projets de santé au Cameroun.*

NERA est le modèle d'aide à la décision de l'application hospitalière du même nom. Il est découpé en **deux
modules**, qui répondent à deux questions différentes et n'utilisent pas les mêmes données :

| Module | Question | Méthode | Données | État |
|---|---|---|---|---|
| [**Module lit**](module_lit/) | Combien de lits seront occupés demain, dans 3 jours, dans 7 jours ? | **régression** : SVR quantile à coûts asymétriques, noyau composite, empilement | registre d'hospitalisation (entrées, sorties) → occupation jour par jour | **presque complètement opérationnel** |
| [**Module triage**](module_triage/) | Ce patient qui arrive aux urgences est-il grave ? | **classification** : SVM à coûts asymétriques, probabilité de Platt, seuil de coût | registre des urgences (constantes, plaintes, décision) | code écrit et testé, en attente des données |

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

## Démarrer

```bash
cd /mnt/c/Users/<utilisateur>/Desktop
git clone https://github.com/drew22109267/outil-saisi.git
git clone https://github.com/drew22109267/nera-modele.git
~/memoire-env/bin/pip install -e outil-saisi                # le traitement des données
cd nera-modele/module_lit
bash lancer_tout.sh                                         # toute la chaîne du module lit
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
