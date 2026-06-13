"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: app.ml.train_models
Purpose: Train and benchmark clinical AI models.
Author: Samuel Israel, MD
License: MIT
===============================================================================
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    make_scorer,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate

from app.ml.feature_builder import build_feature_matrix
from app.ml.preprocessor import prepare_features, scale_features, split_train_test


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_DIR = PROJECT_ROOT / "models"
REPORT_DIR = PROJECT_ROOT / "reports"

MODEL_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

FEATURE_NAMES_PATH = MODEL_DIR / "feature_names.pkl"
SCALER_PATH = MODEL_DIR / "scaler.pkl"
CHAMPION_MODEL_PATH = MODEL_DIR / "champion_model.pkl"
TRAINING_METADATA_PATH = MODEL_DIR / "training_metadata.json"

X_TEST_PATH = MODEL_DIR / "X_test.pkl"
Y_TEST_PATH = MODEL_DIR / "y_test.pkl"


def get_models() -> dict:
    """Return candidate models."""

    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            n_jobs=-1,
            class_weight="balanced",
        ),
    }

    try:
        from xgboost import XGBClassifier

        models["XGBoost"] = XGBClassifier(
            n_estimators=250,
            learning_rate=0.05,
            max_depth=5,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="logloss",
            random_state=42,
        )
    except ImportError:
        print("XGBoost not installed. Skipping XGBoost.")

    try:
        from lightgbm import LGBMClassifier

        models["LightGBM"] = LGBMClassifier(
            n_estimators=250,
            learning_rate=0.05,
            random_state=42,
            class_weight="balanced",
        )
    except ImportError:
        print("LightGBM not installed. Skipping LightGBM.")

    try:
        from catboost import CatBoostClassifier

        models["CatBoost"] = CatBoostClassifier(
            iterations=250,
            learning_rate=0.05,
            depth=5,
            verbose=False,
            random_state=42,
            auto_class_weights="Balanced",
        )
    except ImportError:
        print("CatBoost not installed. Skipping CatBoost.")

    return models


def benchmark_models(X: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
    """Benchmark models using stratified 5-fold cross-validation."""

    scoring = {
        "accuracy": make_scorer(accuracy_score),
        "precision": make_scorer(
            precision_score,
            zero_division=0,
        ),
        "recall": make_scorer(
            recall_score,
            zero_division=0,
        ),
        "f1": make_scorer(
            f1_score,
            zero_division=0,
        ),
        "auc": "roc_auc",
    }

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42,
    )

    results = []

    for model_name, model in get_models().items():
        print(f"\nTraining: {model_name}")

        scores = cross_validate(
            model,
            X,
            y,
            cv=cv,
            scoring=scoring,
            n_jobs=-1,
            error_score="raise",
        )

        results.append(
            {
                "model": model_name,
                "accuracy": round(scores["test_accuracy"].mean(), 4),
                "precision": round(scores["test_precision"].mean(), 4),
                "recall": round(scores["test_recall"].mean(), 4),
                "f1": round(scores["test_f1"].mean(), 4),
                "auc": round(scores["test_auc"].mean(), 4),
            }
        )

    return pd.DataFrame(results).sort_values(
        "auc",
        ascending=False,
    )


def train_champion_model(
    X: pd.DataFrame,
    y: pd.Series,
    model_name: str,
):
    """Train champion model on full training data."""

    models = get_models()

    champion = models[model_name]
    champion.fit(X, y)

    joblib.dump(champion, CHAMPION_MODEL_PATH)

    return CHAMPION_MODEL_PATH


def save_training_metadata(
    *,
    feature_count: int,
    train_rows: int,
    test_rows: int,
    champion_model_name: str,
    benchmark_path: Path,
) -> None:
    """Save training metadata."""

    metadata = {
        "product": "ClariPulse™",
        "module": "app.ml.train_models",
        "training_timestamp": datetime.now().isoformat(),
        "feature_count": feature_count,
        "train_rows": train_rows,
        "test_rows": test_rows,
        "champion_model": champion_model_name,
        "benchmark_report": str(benchmark_path),
        "model_path": str(CHAMPION_MODEL_PATH),
        "scaler_path": str(SCALER_PATH),
        "feature_names_path": str(FEATURE_NAMES_PATH),
        "version": "1.0.0",
    }

    with open(TRAINING_METADATA_PATH, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=4)


def main() -> None:
    """Run full training pipeline."""

    print("\nBuilding feature matrix...")
    df = build_feature_matrix()

    print(f"Feature matrix shape: {df.shape}")

    X, y = prepare_features(df)

    print(f"Features: {X.shape}")
    print(f"Target distribution:\n{y.value_counts(normalize=True)}")

    joblib.dump(list(X.columns), FEATURE_NAMES_PATH)
    print(f"\nSaved feature names to: {FEATURE_NAMES_PATH}")

    X_train, X_test, y_train, y_test = split_train_test(X, y)

    X_train_scaled, X_test_scaled, scaler = scale_features(
        X_train,
        X_test,
    )

    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(X_test_scaled, X_TEST_PATH)
    joblib.dump(y_test, Y_TEST_PATH)

    print(f"Saved scaler to: {SCALER_PATH}")
    print(f"Saved X_test to: {X_TEST_PATH}")
    print(f"Saved y_test to: {Y_TEST_PATH}")

    print("\nBenchmarking candidate models...")

    results = benchmark_models(X_train_scaled, y_train)

    results_path = REPORT_DIR / "model_benchmark_results.csv"
    results.to_csv(results_path, index=False)

    champion_model_name = results.iloc[0]["model"]

    print("\nModel Benchmark Results")
    print(results)

    print(f"\nChampion Model: {champion_model_name}")

    model_path = train_champion_model(
        X_train_scaled,
        y_train,
        champion_model_name,
    )

    save_training_metadata(
        feature_count=X_train_scaled.shape[1],
        train_rows=X_train_scaled.shape[0],
        test_rows=X_test_scaled.shape[0],
        champion_model_name=champion_model_name,
        benchmark_path=results_path,
    )

    print(f"\nSaved champion model to: {model_path}")
    print(f"Saved benchmark report to: {results_path}")
    print(f"Saved training metadata to: {TRAINING_METADATA_PATH}")


if __name__ == "__main__":
    main()