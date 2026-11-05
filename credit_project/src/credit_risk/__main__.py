"""Point d'entrée : ``python -m credit_risk``."""

from credit_risk.pipeline import run_pipeline


def main():
    _, score = run_pipeline("data/raw/credit.csv", model_path="models/model.pkl")
    print(f"Accuracy (jeu de test) : {score:.3f}")


if __name__ == "__main__":
    main()
