"""Chargement des données."""

import pandas as pd


def load_data(path):
    """Charge un fichier CSV."""
    return pd.read_csv(path)
