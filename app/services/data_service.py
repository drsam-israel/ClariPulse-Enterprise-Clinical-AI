"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: app.services.data_service
Purpose: Single source of truth for live product, model, benchmark, and SHAP data.
Author: Samuel Israel, MD
License: MIT
===============================================================================
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_REGISTRY_PATH = PROJECT_ROOT / "models" / "model_registry.json"
TRAINING_METADATA_PATH = PROJECT_ROOT / "models" / "training_metadata.json"
BENCHMARK_RESULTS_PATH = PROJECT_ROOT / "reports" / "model_benchmark_results.csv"
SHAP_IMPORTANCE_PATH = PROJECT_ROOT / "reports" / "shap_feature_importance.csv"


def load_json(path: Path) -> dict:
    """Load JSON safely."""
    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_csv(path: Path) -> pd.DataFrame:
    """Load CSV safely."""
    if not path.exists():
        return pd.DataFrame()

    return pd.read_csv(path)


def get_model_registry() -> dict:
    """Return model registry metadata."""
    return load_json(MODEL_REGISTRY_PATH)


def get_training_metadata() -> dict:
    """Return training metadata."""
    return load_json(TRAINING_METADATA_PATH)


def get_benchmark_results() -> pd.DataFrame:
    """Return model benchmark results."""
    return load_csv(BENCHMARK_RESULTS_PATH)


def get_shap_importance() -> pd.DataFrame:
    """Return SHAP feature importance."""
    return load_csv(SHAP_IMPORTANCE_PATH)


def get_champion_model() -> str:
    """Return champion model name."""
    registry = get_model_registry()
    return registry.get("champion_model", "Unknown")


def get_champion_auc() -> str:
    """Return champion model AUC."""
    registry = get_model_registry()
    auc = registry.get("auc", "N/A")

    if isinstance(auc, float):
        return str(round(auc, 4))

    return str(auc)


def get_product_status() -> dict:
    """Return consolidated product status."""
    registry = get_model_registry()
    training = get_training_metadata()
    benchmark = get_benchmark_results()
    shap_df = get_shap_importance()

    return {
        "champion_model": registry.get("champion_model", "Unknown"),
        "champion_auc": get_champion_auc(),
        "model_status": registry.get("status", "Unknown"),
        "models_benchmarked": len(benchmark) if not benchmark.empty else 0,
        "features_used": training.get("feature_count", "N/A"),
        "training_rows": training.get("train_rows", "N/A"),
        "test_rows": training.get("test_rows", "N/A"),
        "shap_features": len(shap_df) if not shap_df.empty else 0,
        "explainability_status": "Ready" if not shap_df.empty else "Pending",
    }