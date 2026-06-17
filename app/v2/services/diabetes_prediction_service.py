"""
===============================================================================
ClariPulse™ V2 - Diabetes Readmission Prediction Service

Purpose:
    Load the V2 real-world diabetes Champion Model and generate
    30-day readmission risk predictions.

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


PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_DIR = PROJECT_ROOT / "models" / "v2"

CHAMPION_MODEL_PATH = MODEL_DIR / "diabetes_champion_model.pkl"
SCALER_PATH = MODEL_DIR / "diabetes_scaler.pkl"
FEATURE_NAMES_PATH = MODEL_DIR / "diabetes_feature_names.pkl"


def load_prediction_artifacts():
    """Load V2 prediction artifacts."""

    model = joblib.load(CHAMPION_MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    feature_names = joblib.load(FEATURE_NAMES_PATH)

    return model, scaler, feature_names


def build_patient_feature_row(patient: dict, feature_names: list[str]) -> pd.DataFrame:
    """Convert patient dictionary into model-ready feature row."""

    row = {feature: 0 for feature in feature_names}

    for key, value in patient.items():
        if key in row:
            row[key] = value

    return pd.DataFrame([row], columns=feature_names)


def classify_risk(probability: float) -> str:
    """Classify 30-day readmission risk."""

    if probability < 0.10:
        return "Low"
    if probability < 0.20:
        return "Moderate"
    if probability < 0.35:
        return "High"

    return "Critical"


def predict_diabetes_readmission(patient: dict) -> dict:
    """Predict 30-day diabetes readmission risk."""

    model, scaler, feature_names = load_prediction_artifacts()

    X = build_patient_feature_row(patient, feature_names)
    X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

    X_scaled = scaler.transform(X)

    probability = float(model.predict_proba(X_scaled)[0][1])
    prediction = int(probability >= 0.50)

    return {
        "prediction": prediction,
        "probability": round(probability, 4),
        "risk_percent": round(probability * 100, 2),
        "risk_category": classify_risk(probability),
        "use_case": "30-Day Diabetes Readmission Prediction",
        "model_version": "2.0-realworld-diabetes",
    }


if __name__ == "__main__":
    sample_patient = {
        "time_in_hospital": 5,
        "num_lab_procedures": 45,
        "num_procedures": 1,
        "num_medications": 18,
        "number_outpatient": 0,
        "number_emergency": 1,
        "number_inpatient": 1,
        "number_diagnoses": 8,
    }

    print(predict_diabetes_readmission(sample_patient))