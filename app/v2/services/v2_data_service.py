"""
===============================================================================
ClariPulse™ V2 - Real-World Data Service

Purpose:
    Centralized service layer for V2 real-world diabetes readmission
    model metadata, benchmark results, SHAP outputs, and product status.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_DIR = PROJECT_ROOT / "models" / "v2"
REPORT_DIR = PROJECT_ROOT / "reports" / "v2"

REGISTRY_PATH = MODEL_DIR / "diabetes_model_registry.json"
METADATA_PATH = MODEL_DIR / "diabetes_training_metadata.json"
BENCHMARK_PATH = REPORT_DIR / "diabetes_model_benchmark_results.csv"
SHAP_PATH = REPORT_DIR / "diabetes_shap_feature_importance.csv"
DATA_PROFILE_PATH = REPORT_DIR / "diabetes_data_profile.csv"


def load_json(path: Path) -> dict:
    """Safely load JSON file."""

    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_csv(path: Path) -> pd.DataFrame:
    """Safely load CSV file."""

    if not path.exists():
        return pd.DataFrame()

    return pd.read_csv(path)


def get_v2_registry() -> dict:
    """Return V2 model registry."""

    return load_json(REGISTRY_PATH)


def get_v2_metadata() -> dict:
    """Return V2 training metadata."""

    return load_json(METADATA_PATH)


def get_v2_benchmark_results() -> pd.DataFrame:
    """Return V2 benchmark results."""

    return load_csv(BENCHMARK_PATH)


def get_v2_shap_importance() -> pd.DataFrame:
    """Return V2 SHAP feature importance."""

    return load_csv(SHAP_PATH)


def get_v2_data_profile() -> pd.DataFrame:
    """Return V2 data profile."""

    return load_csv(DATA_PROFILE_PATH)


def get_v2_product_status() -> dict:
    """Return consolidated V2 product status."""

    registry = get_v2_registry()
    metadata = get_v2_metadata()
    benchmark = get_v2_benchmark_results()
    shap_df = get_v2_shap_importance()
    data_profile = get_v2_data_profile()

    if not data_profile.empty:
        data_row = data_profile.iloc[0].to_dict()
    else:
        data_row = {}

    return {
        "product": registry.get("product", "ClariPulse™"),
        "version": registry.get("version", "2.0-realworld-diabetes"),
        "status": registry.get("status", "Unknown"),
        "use_case": registry.get(
            "use_case",
            "30-Day Diabetes Readmission Prediction",
        ),
        "champion_model": registry.get("champion_model", "Unknown"),
        "cv_auc": registry.get("cv_auc", "N/A"),
        "test_auc": registry.get("test_auc", "N/A"),
        "test_recall": registry.get("test_recall", "N/A"),
        "test_f1": registry.get("test_f1", "N/A"),
        "models_benchmarked": len(benchmark) if not benchmark.empty else 0,
        "features_used": metadata.get("feature_count", "N/A"),
        "train_rows": metadata.get("train_rows", "N/A"),
        "test_rows": metadata.get("test_rows", "N/A"),
        "target_positive_rate": metadata.get("target_positive_rate", "N/A"),
        "dataset_rows": data_row.get("rows", "N/A"),
        "unique_patients": data_row.get("unique_patients", "N/A"),
        "readmission_30day_rate": data_row.get("readmission_30day_rate", "N/A"),
        "shap_features": len(shap_df) if not shap_df.empty else 0,
        "explainability_status": "Ready" if not shap_df.empty else "Pending",
    }


if __name__ == "__main__":
    print(get_v2_product_status())