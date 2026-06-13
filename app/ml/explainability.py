"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: app.ml.explainability
Purpose: Generate SHAP explainability outputs for the champion model.
Author: Samuel Israel, MD
License: MIT
===============================================================================
"""

from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
try:
    import shap
except ImportError:
    shap = None


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_DIR = PROJECT_ROOT / "models"
REPORT_DIR = PROJECT_ROOT / "reports"

MODEL_PATH = MODEL_DIR / "champion_model.pkl"
X_TEST_PATH = MODEL_DIR / "X_test.pkl"
FEATURE_NAMES_PATH = MODEL_DIR / "feature_names.pkl"

SHAP_OUTPUT_PATH = REPORT_DIR / "shap_feature_importance.csv"


def load_artifacts():
    """Load champion model and test data."""

    model = joblib.load(MODEL_PATH)
    X_test = joblib.load(X_TEST_PATH)
    feature_names = joblib.load(FEATURE_NAMES_PATH)

    X_test = pd.DataFrame(X_test, columns=feature_names)

    return model, X_test


def generate_shap_importance(sample_size: int = 1000) -> pd.DataFrame:
    """Generate global SHAP feature importance."""

    model, X_test = load_artifacts()

    sample = X_test.sample(
        n=min(sample_size, len(X_test)),
        random_state=42,
    )

    explainer = shap.Explainer(model, sample)
    shap_values = explainer(sample)

    importance = pd.DataFrame(
        {
            "feature": sample.columns,
            "mean_abs_shap": abs(shap_values.values).mean(axis=0),
        }
    ).sort_values("mean_abs_shap", ascending=False)

    REPORT_DIR.mkdir(exist_ok=True)
    importance.to_csv(SHAP_OUTPUT_PATH, index=False)

    return importance


def explain_single_patient(index: int = 0) -> pd.DataFrame:
    """Generate SHAP explanation for one patient."""

    model, X_test = load_artifacts()

    patient = X_test.iloc[[index]]

    explainer = shap.Explainer(model, X_test.sample(1000, random_state=42))
    shap_values = explainer(patient)

    explanation = pd.DataFrame(
        {
            "feature": patient.columns,
            "feature_value": patient.iloc[0].values,
            "shap_value": shap_values.values[0],
        }
    ).sort_values("shap_value", key=abs, ascending=False)

    return explanation


if __name__ == "__main__":
    print("\nGenerating SHAP global feature importance...")

    importance_df = generate_shap_importance()

    print(importance_df.head(10))

    print(f"\nSaved SHAP importance to: {SHAP_OUTPUT_PATH}")

    print("\nGenerating single-patient explanation...")

    patient_explanation = explain_single_patient(index=0)

    print(patient_explanation.head(10))

def explain_patient(patient: dict) -> pd.DataFrame:
    """
    Return SHAP explanation for a single patient.
    """

    model, X_test = load_artifacts()

    row = {feature: 0 for feature in X_test.columns}

    for key, value in patient.items():
        if key in row:
            row[key] = value

    patient_df = pd.DataFrame([row])

    explainer = shap.Explainer(
        model,
        X_test.sample(
            min(1000, len(X_test)),
            random_state=42,
        ),
    )
def explain_patient(patient: dict) -> dict:
    """
    Deployment-safe patient explanation.

    Uses precomputed global SHAP feature importance instead of loading X_test.pkl.
    This prevents Streamlit Cloud deployment errors.
    """

    import pandas as pd
    from pathlib import Path

    project_root = Path(__file__).resolve().parents[2]
    shap_path = project_root / "reports" / "shap_feature_importance.csv"

    if not shap_path.exists():
        return {
            "status": "Unavailable",
            "message": "SHAP feature importance file not found.",
            "top_drivers": [],
        }

    shap_df = pd.read_csv(shap_path)

    top_drivers = (
        shap_df.head(5)[["feature", "mean_abs_shap"]]
        .to_dict(orient="records")
    )

    return {
        "status": "Available",
        "message": "Top AI risk drivers are based on global SHAP feature importance.",
        "top_drivers": top_drivers,
    }