import os
import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest


DATA_PATH = "data/dataset.csv"
MODEL_PATH = "models/anomaly_model.pkl"


FEATURES = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]


def train_model():

    print("\n===================================")
    print(" AI SAFETY ANOMALY MODEL TRAINING")
    print("===================================\n")

    if not os.path.exists(DATA_PATH):
        print("ERROR: Dataset not found!")
        print(f"Expected file: {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)

    print("Dataset loaded.")
    print("Rows:", len(df))

    missing = [
        column
        for column in FEATURES
        if column not in df.columns
    ]

    if missing:
        print("\nMissing columns:")
        for column in missing:
            print("-", column)

        print("\nAvailable columns:")
        print(df.columns.tolist())
        return

    X = df[FEATURES].copy()

    X = X.dropna()

    print("Training features:")
    print(FEATURES)

    pipeline = Pipeline([
        (
            "scaler",
            StandardScaler()
        ),

        (
            "anomaly_detector",
            IsolationForest(
                n_estimators=200,
                contamination=0.05,
                random_state=42
            )
        )
    ])

    print("\nTraining model...")

    pipeline.fit(X)

    os.makedirs("models", exist_ok=True)

    joblib.dump(
        pipeline,
        MODEL_PATH
    )

    print("\n===================================")
    print(" MODEL TRAINING COMPLETED")
    print("===================================")

    print("\nModel saved at:")
    print(MODEL_PATH)


if __name__ == "__main__":
    train_model()