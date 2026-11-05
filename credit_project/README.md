# Credit Risk

Prédiction du risque de défaut de crédit (Random Forest / Régression logistique / XGBoost).

## Installation
```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

## Utilisation
```bash
python -m credit_risk            # entraîne, évalue, sauvegarde models/model.pkl
```

## Qualité
```bash
ruff check .        # analyse statique
black --check .     # vérification du formatage
black .             # formatage automatique
pytest              # tests
```

## Structure
- `data/raw/` : données brutes
- `notebooks/` : exploration
- `src/credit_risk/` : code (data, preprocessing, trainers, training, evaluation, prediction, pipeline)
- `tests/` : tests automatisés
- `docs/` : documentation et ancien `main.py`
