"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: app.ml.explainability
Purpose: Generate and serve SHAP explainability outputs.
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


def load_artifacts() -> tuple:
    """
    Load champion model, X_test, and feature names.

    Used only for local SHAP generation where X_test.pkl exists.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    if not X_TEST_PATH.exists():
        raise FileNotFoundError(f"X_test not found: {X_TEST_PATH}")

    if not FEATURE_NAMES_PATH.exists():
        raise FileNotFoundError(f"Feature names not found: {FEATURE_NAMES_PATH}")

    model = joblib.load(MODEL_PATH)
    X_test = joblib.load(X_TEST_PATH)
    feature_names = joblib.load(FEATURE_NAMES_PATH)

    X_test = pd.DataFrame(X_test, columns=feature_names)

    return model, X_test


def generate_shap_importance(sample_size: int = 1000) -> pd.DataFrame:
    """
    Generate global SHAP feature importance.

    This function is intended for local/offline use because it requires X_test.pkl.
    """

    if shap is None:
        raise ImportError("SHAP is not installed. Add `shap` to requirements.txt.")

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
    """
    Generate SHAP explanation for one patient.

    This is intended for local/offline use because it requires X_test.pkl.
    """

    if shap is None:
        raise ImportError("SHAP is not installed. Add `shap` to requirements.txt.")

    model, X_test = load_artifacts()

    patient = X_test.iloc[[index]]

    explainer = shap.Explainer(
        model,
        X_test.sample(
            n=min(1000, len(X_test)),
            random_state=42,
        ),
    )

    shap_values = explainer(patient)

    explanation = pd.DataFrame(
        {
            "feature": patient.columns,
            "value": patient.iloc[0].values,
            "shap": shap_values.values[0],
        }
    )

    explanation["abs_shap"] = explanation["shap"].abs()

    return explanation.sort_values(
        "abs_shap",
        ascending=False,
    )


def explain_patient(patient: dict) -> pd.DataFrame:
    """
    Deployment-safe patient explanation.

    Returns a DataFrame compatible with Patient Explorer without requiring X_test.pkl.
    Uses precomputed global SHAP feature importance from reports/shap_feature_importance.csv.
    """

    if not SHAP_OUTPUT_PATH.exists():
        return pd.DataFrame(
            columns=["feature", "value", "shap", "abs_shap"]
        )

    shap_df = pd.read_csv(SHAP_OUTPUT_PATH)

    if shap_df.empty or "feature" not in shap_df.columns or "mean_abs_shap" not in shap_df.columns:
        return pd.DataFrame(
            columns=["feature", "value", "shap", "abs_shap"]
        )

    explanation = pd.DataFrame(
        {
            "feature": shap_df["feature"],
            "value": ["Global Driver"] * len(shap_df),
            "shap": shap_df["mean_abs_shap"],
        }
    )

    explanation["abs_shap"] = explanation["shap"].abs()

    return explanation.sort_values(
        "abs_shap",
        ascending=False,
    )


if __name__ == "__main__":
    print("\nGenerating SHAP global feature importance...")

    importance_df = generate_shap_importance()

    print(importance_df.head(10))

    print(f"\nSaved SHAP importance to: {SHAP_OUTPUT_PATH}")

    print("\nGenerating single-patient explanation...")

    patient_explanation = explain_single_patient(index=0)

    print(patient_explanation.head(10))