# Rapport de TP : Qualité et organisation d'un projet IA

## Exercice 1 : Diagnostic du projet initial (10 problèmes)

1. **Fichiers** : données, modèle, notebook et code mélangés à la racine.
2. **Nommage** : `d`, `X`, `y`, `m`, `run` n'expriment aucune intention.
3. **Indentation / structure** : une seule fonction monolithique, pas de séparation visuelle des étapes.
4. **Espaces** : pas d'espaces autour de `=` et des virgules, deux lignes vides manquantes avant `def` (violations PEP 8, détectées par Black).
5. **Imports** : `import os` inutilisé, imports non triés (Ruff : F401 et I001).
6. **`run()`** : charge, nettoie, sépare, entraîne, évalue et affiche : 6 responsabilités.
7. **Séparation des traitements** : aucune étape réutilisable indépendamment.
8. **Testabilité** : chemin `"credit.csv"` en dur, `print` au lieu d'un `return`, impossible de tester une étape seule.
9. **Documentation** : aucune docstring, aucun README.
10. **Maintenabilité / fiabilité** : `model = run()` s'exécute à l'import (pas de `if __name__ == "__main__"`), pas de `random_state` (résultats non reproductibles), score calculé sur les données d'entraînement (trompeur, pas de train/test split), modèle jamais sauvegardé.

**Un programme peut-il fonctionner tout en étant de mauvaise qualité ?** Oui. « Fonctionner » signifie produire un résultat aujourd'hui. La qualité logicielle concerne la lisibilité, la testabilité, l'évolutivité et la reproductibilité. Ici le script tourne, mais il est impossible à tester, à faire évoluer ou à partager sans risque, et son score affiché est même trompeur. Cette dette technique coûte cher dès qu'il faut maintenir ou déployer.

## Exercice 2 : Structuration

Arborescence créée (voir `README.md`). Réponses :
- **Séparer notebooks et `src`** : le notebook sert à l'exploration (état caché, ordre d'exécution aléatoire, difficile à versionner/tester). Le code réutilisable et testable vit dans `src` et peut être importé par tout le monde.
- **Séparer données et code** : les données évoluent à un autre rythme, sont volumineuses ou sensibles, et ne se versionnent pas avec Git comme le code (d'où `.gitignore`). Cela évite aussi les chemins en dur.
- **Dossier `tests`** : vérifier automatiquement que le code fonctionne, détecter les régressions à chaque modification, et documenter le comportement attendu.

## Exercice 3 : Modularisation et SRP

| Module | Responsabilité unique |
|---|---|
| `data.py` | charger le CSV |
| `preprocessing.py` | nettoyer, séparer features/cible |
| `training.py` | entraîner via un trainer |
| `evaluation.py` | évaluer |
| `prediction.py` | prédire, sauvegarder/recharger un modèle |
| `pipeline.py` | orchestrer les étapes |

**Pourquoi mieux pour SRP ?** Dans `main.py`, `run()` avait six raisons de changer. Désormais chaque module n'en a qu'une : si le format de données change, on ne touche que `data.py` ; si on change de métrique, que `evaluation.py`. Chaque fonction est testable isolément.

## Exercice 4 : OCP et DIP

Implémenté dans `trainers.py` : `ModelTrainer` (abstraite), `RandomForestTrainer`, `LogisticRegressionTrainer`, plus `XGBoostTrainer` en bonus.

- **Même méthode `train()`** : vérifié par le test `test_trainers_share_same_interface` (isinstance + même appel).
- **Ajout d'un modèle plus facile** : on ajoute une classe héritant de `ModelTrainer`, sans toucher à `training.py` ni au pipeline, et sans `if/elif`.
- **Principes dans le projet** :
  - **SRP** : un module = une responsabilité (tableau ci-dessus).
  - **OCP** : le système est ouvert à l'extension (nouvelle classe trainer) et fermé à la modification (`training.py` et `pipeline.py` restent inchangés).
  - **DIP** : `train_model()` et `run_pipeline()` dépendent de l'abstraction `ModelTrainer`, pas de `RandomForestClassifier` directement.

## Exercice 5 : Ruff

Résultats mesurés :
- **Projet initial** (`ruff check .`) : **2 problèmes** : `F401` (import `os` inutilisé) et `I001` (imports non triés), tous deux corrigeables avec `--fix`.
- **Après restructuration** : 0 problème sur le code du projet.
- **Ce qui reste manuel** en général : noms peu parlants, fonction trop longue, absence de tests/docstrings, logique erronée (ex. évaluation sur le jeu d'entraînement). Ruff corrige des problèmes de forme, pas de conception.

**Pourquoi Ruff ne garantit-il pas la qualité complète ?** C'est une analyse statique de règles syntaxiques et stylistiques. Il ne vérifie ni la logique métier, ni la pertinence de l'architecture, ni la couverture de tests, ni la qualité du modèle (fuite de données, sur-apprentissage).

## Exercice 6 : Black

- **Avant** : `black --check .` sur le projet initial → « 1 file would be reformatted » (`main.py` : espaces autour de `=` et des virgules, lignes vides avant `def`).
- **Après `black .`** : « All done ! 11 files would be left unchanged ».
- Relance de `ruff check .` : aucun problème.

**Différence Ruff / Black** : Ruff *détecte* des problèmes (imports/variables inutilisés, erreurs potentielles) et peut en corriger certains. Black *reformate* uniquement la présentation (espaces, retours à la ligne, guillemets) sans jamais changer le comportement du code. Les deux sont complémentaires.

## Exercice 7 : Configuration `pyproject.toml`

Fichier créé à la racine (`line-length = 88`, règles Ruff `E4, E7, E9, F`).

1. **Intérêt** : la configuration est versionnée avec le code ; tout le monde applique les mêmes règles.
2. **Nouveau développeur** : il clone, installe les outils, et `ruff check .` / `black .` utilisent automatiquement la même configuration, sans réglage manuel.
3. **Reproductibilité** : mêmes règles → mêmes résultats sur toutes les machines et en intégration continue ; plus de débats de style.

## Comparaison avant / après

| Critère | Avant | Après |
|---|---|---|
| Fichiers | 4 en vrac | arborescence standard, package `credit_risk` |
| Responsabilités | 1 fonction = 6 tâches | 1 module = 1 responsabilité |
| Extension | modifier le code existant | ajouter une classe (OCP/DIP) |
| Tests | 0 | 5 tests pytest, tous passent |
| Ruff | 2 problèmes | 0 |
| Black | à reformater | conforme |
| Évaluation | sur données d'entraînement (trompeur) | train/test split (accuracy test ≈ 0.58 sur données synthétiques) |
| Reproductibilité | aucune graine, rien de sauvegardé | `random_state=42`, config centralisée, modèle sauvegardé |

> Note : `credit.csv` est un jeu de **données synthétiques** que j'ai généré (l'original n'a pas été fourni). Remplacez-le par votre vrai fichier dans `data/raw/`.
