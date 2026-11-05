"""Interface Streamlit : ``streamlit run app.py``."""

import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split

from credit_risk.data import load_data
from credit_risk.evaluation import evaluate_model
from credit_risk.prediction import predict, predict_proba, save_model
from credit_risk.preprocessing import clean_data, split_features_target
from credit_risk.trainers import LogisticRegressionTrainer, RandomForestTrainer
from credit_risk.training import train_model

DATA_PATH = "data/raw/credit.csv"
TRAINERS = {
    "Random Forest": RandomForestTrainer,
    "Régression logistique": LogisticRegressionTrainer,
}

st.set_page_config(page_title="Risque de crédit", page_icon="💳")
st.title("💳 Prédiction du risque de crédit")

# --- 1. Données -------------------------------------------------------------
data = clean_data(load_data(DATA_PATH))
features, target = split_features_target(data)
with st.expander(f"Aperçu des données ({len(data)} lignes propres)"):
    st.dataframe(data.head(10))

# --- 2. Entraînement --------------------------------------------------------
st.header("1. Entraîner un modèle")
model_name = st.selectbox("Modèle", list(TRAINERS))
if st.button("Entraîner"):
    x_train, x_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42
    )
    model = train_model(x_train, y_train, TRAINERS[model_name]())
    st.session_state["model"] = model
    st.session_state["model_name"] = model_name
    st.session_state["score"] = evaluate_model(model, x_test, y_test)
    save_model(model, "models/model.pkl")

if "model" in st.session_state:
    st.success(
        f"{st.session_state['model_name']} entraîné. "
        f"Accuracy (jeu de test) : {st.session_state['score']:.3f}"
    )

    # --- 3. Prédiction ------------------------------------------------------
    st.header("2. Prédire pour un client")
    values = {}
    for column in features.columns:
        series = features[column]
        values[column] = st.number_input(
            column, value=float(series.median()), min_value=float(series.min())
        )
    if st.button("Prédire"):
        client = pd.DataFrame([values])
        model = st.session_state["model"]
        probability = predict_proba(model, client)[0]
        if predict(model, client)[0] == 1:
            st.error(f"⚠️ Risque de défaut (probabilité : {probability:.0%})")
        else:
            st.success(f"✅ Pas de défaut prévu (risque : {probability:.0%})")
else:
    st.info("Choisissez un modèle puis cliquez sur « Entraîner ».")
