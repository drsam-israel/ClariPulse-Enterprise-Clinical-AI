"""
===============================================================================
ClariPulse™ V2 - Real-World Diabetes Explainability Engine
Author: Samuel Israel, MD
License: MIT
===============================================================================
"""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd

try:
    import shap
except ImportError:
    shap = None


PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_DIR = PROJECT_ROOT / "models" / "v2"
REPORT_DIR = PROJECT_ROOT / "reports" / "v2"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

CHAMPION_MODEL_PATH = MODEL_DIR / "diabetes_champion_model.pkl"
SCALER_PATH = MODEL_DIR / "diabetes_scaler.pkl"
FEATURE_NAMES_PATH = MODEL_DIR / "diabetes_feature_names.pkl"

FEATURE_MATRIX_PATH = (
    PROJECT_ROOT / "data" / "processed" / "v2" / "diabetes_feature_matrix.csv"
)

SHAP_IMPORTANCE_PATH = REPORT_DIR / "diabetes_shap_feature_importance.csv"

TARGET_COLUMN = "target_readmitted_30day"


def load_v2_artifacts() -> tuple:
    """Load V2 Champion Model, scaler, feature names, and clean feature matrix."""

    if shap is None:
        raise ImportError("SHAP is not installed. Add `shap` to requirements.txt.")

    model = joblib.load(CHAMPION_MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    feature_names = joblib.load(FEATURE_NAMES_PATH)

    df = pd.read_csv(FEATURE_MATRIX_PATH)

    X = df.drop(columns=[TARGET_COLUMN])
    X = X[feature_names]

    # Force all values to numeric float64
    X = X.apply(pd.to_numeric, errors="coerce")
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(0)
    X = X.astype("float64")

    # Apply the same scaler used during model training
    X_scaled = pd.DataFrame(
        scaler.transform(X),
        columns=feature_names,
        index=X.index,
    )

    X_scaled = X_scaled.astype("float64")

    return model, X_scaled


def generate_v2_shap_importance(sample_size: int = 1000) -> pd.DataFrame:
    """Generate global SHAP feature importance for V2."""

    model, X = load_v2_artifacts()

    sample = X.sample(
        n=min(sample_size, len(X)),
        random_state=42,
    )

    sample = sample.astype("float64")

    explainer = shap.Explainer(model, sample)
    shap_values = explainer(sample)

    values = shap_values.values

    if values.ndim == 3:
        values = values[:, :, 1]

    importance = pd.DataFrame(
        {
            "feature": sample.columns,
            "mean_abs_shap": np.abs(values).mean(axis=0),
        }
    ).sort_values("mean_abs_shap", ascending=False)

    importance.to_csv(SHAP_IMPORTANCE_PATH, index=False)

    return importance


def explain_v2_patient(patient_features: dict) -> pd.DataFrame:
    """Deployment-safe V2 patient explanation using precomputed SHAP importance."""

    if not SHAP_IMPORTANCE_PATH.exists():
        return pd.DataFrame(columns=["feature", "value", "shap", "abs_shap"])

    shap_df = pd.read_csv(SHAP_IMPORTANCE_PATH)

    explanation = pd.DataFrame(
        {
            "feature": shap_df["feature"],
            "value": ["Global Driver"] * len(shap_df),
            "shap": shap_df["mean_abs_shap"],
        }
    )

    explanation["abs_shap"] = explanation["shap"].abs()

    return explanation.sort_values("abs_shap", ascending=False)


if __name__ == "__main__":
    print("\nGenerating ClariPulse™ V2 SHAP feature importance...\n")

    shap_importance = generate_v2_shap_importance(sample_size=1000)

    print(shap_importance.head(15))

    print(f"\nSaved V2 SHAP importance to: {SHAP_IMPORTANCE_PATH}")