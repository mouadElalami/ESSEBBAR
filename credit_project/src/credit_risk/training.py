"""Entraînement : dépend de l'abstraction ``ModelTrainer`` (DIP)."""

from credit_risk.trainers import ModelTrainer, RandomForestTrainer


def train_model(features, target, trainer: ModelTrainer | None = None):
    """Entraîne un modèle avec l'entraîneur fourni (Random Forest par défaut)."""
    if trainer is None:
        trainer = RandomForestTrainer()
    return trainer.train(features, target)
