"""Pipeline complet : chargement -> nettoyage -> entraînement -> évaluation."""

from sklearn.model_selection import train_test_split

from credit_risk.data import load_data
from credit_risk.evaluation import evaluate_model
from credit_risk.prediction import save_model
from credit_risk.preprocessing import clean_data, split_features_target
from credit_risk.training import train_model


def run_pipeline(data_path, trainer=None, model_path=None):
    """Exécute le pipeline et retourne (modèle, score sur le jeu de test)."""
    data = clean_data(load_data(data_path))
    features, target = split_features_target(data)
    x_train, x_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42
    )
    model = train_model(x_train, y_train, trainer)
    score = evaluate_model(model, x_test, y_test)
    if model_path is not None:
        save_model(model, model_path)
    return model, score
