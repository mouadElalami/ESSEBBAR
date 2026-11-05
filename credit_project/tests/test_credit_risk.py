import pandas as pd
import pytest

from credit_risk.evaluation import evaluate_model
from credit_risk.pipeline import run_pipeline
from credit_risk.preprocessing import clean_data, split_features_target
from credit_risk.trainers import (
    LogisticRegressionTrainer,
    ModelTrainer,
    RandomForestTrainer,
)


@pytest.fixture
def data():
    return pd.DataFrame(
        {
            "a": [1, 2, None, 4, 5, 6],
            "b": [1, 0, 1, 0, 1, 0],
            "default": [0, 1, 0, 1, 0, 1],
        }
    )


def test_clean_data_removes_missing(data):
    assert len(clean_data(data)) == 5


def test_split_features_target(data):
    features, target = split_features_target(clean_data(data))
    assert "default" not in features.columns
    assert len(features) == len(target)


@pytest.mark.parametrize(
    "trainer_cls", [RandomForestTrainer, LogisticRegressionTrainer]
)
def test_trainers_share_same_interface(trainer_cls, data):
    trainer = trainer_cls()
    assert isinstance(trainer, ModelTrainer)
    features, target = split_features_target(clean_data(data))
    model = trainer.train(features, target)
    assert 0 <= evaluate_model(model, features, target) <= 1


def test_pipeline_runs():
    _, score = run_pipeline("data/raw/credit.csv", LogisticRegressionTrainer())
    assert 0 <= score <= 1


def test_predict_proba_in_range(data):
    from credit_risk.prediction import predict_proba

    features, target = split_features_target(clean_data(data))
    model = LogisticRegressionTrainer().train(features, target)
    assert (
        (predict_proba(model, features) >= 0) & (predict_proba(model, features) <= 1)
    ).all()
