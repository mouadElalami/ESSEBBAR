"""Prétraitement des données."""

TARGET_COLUMN = "default"


def clean_data(data):
    """Supprime les observations contenant des valeurs manquantes."""
    return data.dropna()


def split_features_target(data, target_column=TARGET_COLUMN):
    """Sépare les variables explicatives (features) de la cible (target)."""
    features = data.drop(columns=target_column)
    target = data[target_column]
    return features, target
