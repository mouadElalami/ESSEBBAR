"""Évaluation d'un modèle."""


def evaluate_model(model, features, target):
    """Retourne le score (accuracy) du modèle."""
    return model.score(features, target)
