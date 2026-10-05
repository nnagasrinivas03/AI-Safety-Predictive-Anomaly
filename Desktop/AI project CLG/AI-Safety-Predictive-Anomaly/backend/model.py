import os
import joblib
import numpy as np


MODEL_PATH = "models/anomaly_model.pkl"


if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        "anomaly_model.pkl not found. "
        "Run train_model.py first."
    )


model = joblib.load(MODEL_PATH)


def predict_anomaly(
    air_temperature,
    process_temperature,
    rotational_speed,
    torque,
    tool_wear
):

    data = np.array([[
        air_temperature,
        process_temperature,
        rotational_speed,
        torque,
        tool_wear
    ]])

    prediction = model.predict(data)[0]

    score = model.decision_function(data)[0]

    if prediction == -1:
        status = "ANOMALY"
    else:
        status = "NORMAL"

    return {
        "prediction": int(prediction),
        "status": status,
        "anomaly_score": round(
            float(score),
            4
        )
    }


# =====================================
# TEST THE MODEL
# =====================================

if __name__ == "__main__":

    result = predict_anomaly(
        air_temperature=300,
        process_temperature=310,
        rotational_speed=1500,
        torque=40,
        tool_wear=100
    )

    print("\n==============================")
    print(" AI ANOMALY PREDICTION")
    print("==============================")

    print(
        "Prediction:",
        result["prediction"]
    )

    print(
        "Status:",
        result["status"]
    )

    print(
        "Anomaly Score:",
        result["anomaly_score"]
    )