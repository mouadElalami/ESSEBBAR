"""Prédictions et sauvegarde du modèle."""

import joblib


def predict(model, features):
    """Retourne les classes prédites (0 = pas de défaut, 1 = défaut)."""
    return model.predict(features)


def save_model(model, path):
    """Sauvegarde le modèle sur disque."""
    joblib.dump(model, path)


def load_model(path):
    """Recharge un modèle sauvegardé."""
    return joblib.load(path)


def predict_proba(model, features):
    """Retourne la probabilité de défaut (classe 1) pour chaque observation."""
    return model.predict_proba(features)[:, 1]
