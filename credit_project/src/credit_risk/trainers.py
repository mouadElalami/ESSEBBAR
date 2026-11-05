"""Entraîneurs de modèles (OCP + DIP).

Chaque modèle est une classe qui implémente ``ModelTrainer``.
Ajouter un modèle = ajouter une classe, sans modifier le code existant.
"""

from abc import ABC, abstractmethod

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


class ModelTrainer(ABC):
    """Abstraction : tout entraîneur expose la méthode ``train``."""

    @abstractmethod
    def train(self, features, target):
        """Entraîne et retourne un modèle."""


class RandomForestTrainer(ModelTrainer):
    """Entraîne un Random Forest."""

    def train(self, features, target):
        model = RandomForestClassifier(random_state=42)
        model.fit(features, target)
        return model


class LogisticRegressionTrainer(ModelTrainer):
    """Entraîne une régression logistique."""

    def train(self, features, target):
        model = LogisticRegression(max_iter=1000)
        model.fit(features, target)
        return model


class XGBoostTrainer(ModelTrainer):
    """Entraîne un XGBoost (bonus, nécessite le paquet ``xgboost``)."""

    def train(self, features, target):
        from xgboost import XGBClassifier  # import local : dépendance optionnelle

        model = XGBClassifier(random_state=42)
        model.fit(features, target)
        return model
