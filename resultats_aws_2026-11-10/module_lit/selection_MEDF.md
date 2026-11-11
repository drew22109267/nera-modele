# Sélection — MEDF

Règle : significatif. Critère : perte pinball au quantile décisionnel, moyenne sur les horizons.

**SVM retenu : LS-SVR (moindres carrés), noyau RBF, quantiles LOO** (pinball moyen 0.7626 ; contre le choix d'origine : meilleur, équivalent).

**Durées inconnues : estimee** (pinball moyenne 0.6222 (knn) ; contre « estimee » pour ce modèle : non testé (trop peu de jours), équivalent : non significatif, méthode retenue gardée).

Meilleur modèle toutes familles confondues : AR(p) par AIC.

| variante | famille | modèle | pinball_moyen | MAE_moyenne | horizons | significatif |
|---|---|---|---|---|---|---|
| 1 | autre (D1) | AR(p) par AIC | 0.7078 | 2.2055 | 2 | équivalent |
| 18 | autre (D1) | SARIMA(1,0,0)(1,0,0)7 (ordre choisi sur l'apprentissage) | 0.7199 | 2.2095 | 2 | meilleur, équivalent |
| 21 | svm | LS-SVR (moindres carrés), noyau RBF, quantiles LOO | 0.7626 | 2.235 | 2 | meilleur, équivalent |
| 0 | autre (D1) | A · forêt aléatoire quantile | 0.7908 | 2.2955 | 2 | équivalent |
| 27 | svm | SVR quantile, noyau polynomial (degré 2) | 0.7994 | 2.2575 | 2 | équivalent |
| 24 | svm | SVR quantile RBF (niveau 3) | 0.8119 | 2.3295 | 2 | équivalent |
| 25 | svm | SVR quantile composite (niveau 4, retenu) | 0.8172 | 2.33 | 2 | — choix retenu |
| 19 | autre (D1) | SVR quantile composite (niveau 4) | 0.8172 | 2.33 | 2 | — choix retenu |
| 26 | svm | SVR quantile, noyau laplacien | 0.8225 | 2.355 | 2 | équivalent |
| 6 | autre (D1) | Holt amorti | 0.8389 | 2.3515 | 2 | équivalent |
| 11 | autre (D1) | Lissage exponentiel simple | 0.8389 | 2.3515 | 2 | équivalent |
| 15 | autre (D1) | Méthode Thêta | 0.8389 | 2.3535 | 2 | équivalent |
| 7 | autre (D1) | Holt linéaire | 0.839 | 2.3515 | 2 | équivalent |
| 8 | autre (D1) | Holt-Winters additif amorti | 0.8418 | 2.3585 | 2 | équivalent |
| 12 | autre (D1) | Lissage saisonnier sans tendance | 0.8419 | 2.338 | 2 | équivalent |
| 10 | autre (D1) | Holt-Winters multiplicatif amorti | 0.8466 | 2.364 | 2 | équivalent |
| 13 | autre (D1) | Moyenne historique | 0.8601 | 2.8435 | 2 | moins bon, équivalent |
| 3 | autre (D1) | C · perceptron multicouche quantile | 0.8894 | 2.5245 | 2 | équivalent |
| 4 | autre (D1) | D · LSTM quantile | 0.955 | 2.639 | 2 | équivalent |
| 5 | autre (D1) | E · XGBoost quantile (second ordre) | 0.9621 | 2.37 | 2 | équivalent |
| 2 | autre (D1) | B · gradient boosting quantile | 0.9756 | 2.3605 | 2 | équivalent |
| 9 | autre (D1) | Holt-Winters additif, grille fixée avant la validation | 1.066 | 2.14 | 2 | moins bon, équivalent |
| 16 | autre (D1) | Persistance | 1.185 | 2.364 | 2 | moins bon, équivalent |
| 14 | autre (D1) | Moyenne mobile 7 j | 1.2221 | 2.4535 | 2 | moins bon, équivalent |
| 20 | autre (D1) | Saisonnière hebdomadaire | 1.2686 | 2.55 | 2 | moins bon, équivalent |
| 22 | svm | SVR RBF (niveau 2) | 1.325 | 2.2405 | 2 | moins bon |
| 23 | svm | SVR linéaire (niveau 1) | 1.3912 | 2.35 | 2 | moins bon |
| 17 | autre (D1) | Régression ridge (λ = 1) | 1.4652 | 2.3835 | 2 | moins bon |