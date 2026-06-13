"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product

Module:
    app.ml.predict

Purpose:
    Load the champion model and perform patient risk prediction.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = PROJECT_ROOT / "models" / "champion_model.pkl"
SCALER_PATH = PROJECT_ROOT / "models" / "scaler.pkl"
FEATURE_NAMES_PATH = PROJECT_ROOT / "models" / "feature_names.pkl"


model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
feature_names = joblib.load(FEATURE_NAMES_PATH)


def build_feature_row(patient: dict) -> pd.DataFrame:
    """Convert patient dictionary into model-ready feature row."""

    row = {feature: 0 for feature in feature_names}

    for key, value in patient.items():
        if key in row:
            row[key] = value

    return pd.DataFrame([row], columns=feature_names)


def predict_patient(patient: dict) -> dict:
    """Predict patient risk from named patient features."""

    X = build_feature_row(patient)
    X_scaled = scaler.transform(X)

    probability = float(model.predict_proba(X_scaled)[0][1])
    prediction = int(probability >= 0.50)

    if probability < 0.25:
        risk_category = "Low"
    elif probability < 0.50:
        risk_category = "Moderate"
    elif probability < 0.75:
        risk_category = "High"
    else:
        risk_category = "Critical"

    return {
        "prediction": prediction,
        "probability": round(probability, 4),
        "risk_percent": round(probability * 100, 2),
        "risk_category": risk_category,
    }


if __name__ == "__main__":
    sample_patient = {
        "age": 65,
        "bmi": 28.0,
        "diabetes": 1,
        "hypertension": 1,
        "smoker": 0,
        "ckd": 0,
        "copd": 0,
        "heart_failure": 0,
        "obesity": 0,
        "cancer": 0,
    }

    print(predict_patient(sample_patient))