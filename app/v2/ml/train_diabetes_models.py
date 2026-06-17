"""
===============================================================================
ClariPulse™ V2 - Real-World Diabetes Readmission Model Training

Purpose:
    Train and benchmark ML models for 30-day readmission prediction using
    the real-world diabetes readmission dataset.

Author:
    Samuel Israel, MD

License:
    MIT
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
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.preprocessing import StandardScaler

from app.v2.ml.diabetes_preprocessor import (
    build_feature_matrix,
    split_features_target,
    train_test_split_v2,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_DIR = PROJECT_ROOT / "models" / "v2"
REPORT_DIR = PROJECT_ROOT / "reports" / "v2"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

BENCHMARK_PATH = REPORT_DIR / "diabetes_model_benchmark_results.csv"
REGISTRY_PATH = MODEL_DIR / "diabetes_model_registry.json"
METADATA_PATH = MODEL_DIR / "diabetes_training_metadata.json"

CHAMPION_MODEL_PATH = MODEL_DIR / "diabetes_champion_model.pkl"
SCALER_PATH = MODEL_DIR / "diabetes_scaler.pkl"
FEATURE_NAMES_PATH = MODEL_DIR / "diabetes_feature_names.pkl"


def get_candidate_models() -> dict:
    """Return candidate models for benchmarking."""

    models = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            n_jobs=-1,
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
            n_jobs=-1,
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
            n_jobs=-1,
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


def benchmark_models(X_train: pd.DataFrame, y_train: pd.Series) -> pd.DataFrame:
    """Benchmark candidate models using Stratified 5-Fold Cross-Validation."""

    scoring = {
        "accuracy": "accuracy",
        "precision": "precision",
        "recall": "recall",
        "f1": "f1",
        "auc": "roc_auc",
    }

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42,
    )

    results = []

    for model_name, model in get_candidate_models().items():
        print(f"\nTraining and validating: {model_name}")

        scores = cross_validate(
            model,
            X_train,
            y_train,
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

    return pd.DataFrame(results).sort_values("auc", ascending=False)


def train_champion_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    champion_model_name: str,
):
    """Train champion model on full training set."""

    models = get_candidate_models()
    champion = models[champion_model_name]

    champion.fit(X_train, y_train)

    joblib.dump(champion, CHAMPION_MODEL_PATH)

    return champion


def evaluate_champion_model(
    model,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict:
    """Evaluate champion model on holdout test set."""

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    return {
        "test_accuracy": round(accuracy_score(y_test, y_pred), 4),
        "test_precision": round(precision_score(y_test, y_pred), 4),
        "test_recall": round(recall_score(y_test, y_pred), 4),
        "test_f1": round(f1_score(y_test, y_pred), 4),
        "test_auc": round(roc_auc_score(y_test, y_proba), 4),
    }


def save_registry(
    champion_model_name: str,
    benchmark_results: pd.DataFrame,
    test_metrics: dict,
) -> None:
    """Save V2 model registry."""

    champion_row = benchmark_results[
        benchmark_results["model"] == champion_model_name
    ].iloc[0]

    registry = {
        "product": "ClariPulse™",
        "version": "2.0-realworld-diabetes",
        "status": "Approved",
        "use_case": "30-Day Diabetes Readmission Prediction",
        "champion_model": champion_model_name,
        "cv_accuracy": float(champion_row["accuracy"]),
        "cv_precision": float(champion_row["precision"]),
        "cv_recall": float(champion_row["recall"]),
        "cv_f1": float(champion_row["f1"]),
        "cv_auc": float(champion_row["auc"]),
        **test_metrics,
        "created_at": datetime.now().isoformat(),
    }

    with open(REGISTRY_PATH, "w", encoding="utf-8") as file:
        json.dump(registry, file, indent=4)


def save_metadata(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y: pd.Series,
    champion_model_name: str,
) -> None:
    """Save V2 training metadata."""

    metadata = {
        "product": "ClariPulse™",
        "version": "2.0-realworld-diabetes",
        "module": "app.v2.ml.train_diabetes_models",
        "training_timestamp": datetime.now().isoformat(),
        "dataset": "UCI Diabetes 130-US Hospitals Readmission Dataset",
        "use_case": "30-Day Readmission Prediction",
        "feature_count": int(X_train.shape[1]),
        "train_rows": int(X_train.shape[0]),
        "test_rows": int(X_test.shape[0]),
        "target_positive_rate": float(round(y.mean() * 100, 2)),
        "champion_model": champion_model_name,
    }

    with open(METADATA_PATH, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=4)


def main() -> None:
    """Run V2 model training pipeline."""

    print("\nBuilding V2 diabetes feature matrix...")
    df = build_feature_matrix()

    X, y = split_features_target(df)

    print(f"Feature matrix shape: {df.shape}")
    print(f"X shape: {X.shape}")
    print(f"Target positive rate: {round(y.mean() * 100, 2)}%")

    X_train, X_test, y_train, y_test = train_test_split_v2(X, y)

    scaler = StandardScaler()

    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train),
        columns=X_train.columns,
        index=X_train.index,
    )

    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test),
        columns=X_test.columns,
        index=X_test.index,
    )

    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(list(X_train.columns), FEATURE_NAMES_PATH)

    print("\nBenchmarking V2 candidate models...")
    benchmark_results = benchmark_models(X_train_scaled, y_train)

    benchmark_results.to_csv(BENCHMARK_PATH, index=False)

    champion_model_name = benchmark_results.iloc[0]["model"]

    print("\nV2 Benchmark Results")
    print(benchmark_results)

    print(f"\nV2 Champion Model: {champion_model_name}")

    champion_model = train_champion_model(
        X_train_scaled,
        y_train,
        champion_model_name,
    )

    test_metrics = evaluate_champion_model(
        champion_model,
        X_test_scaled,
        y_test,
    )

    save_registry(
        champion_model_name,
        benchmark_results,
        test_metrics,
    )

    save_metadata(
        X_train_scaled,
        X_test_scaled,
        y,
        champion_model_name,
    )

    print("\nV2 Holdout Test Metrics")
    print(test_metrics)

    print(f"\nSaved benchmark results to: {BENCHMARK_PATH}")
    print(f"Saved champion model to: {CHAMPION_MODEL_PATH}")
    print(f"Saved scaler to: {SCALER_PATH}")
    print(f"Saved feature names to: {FEATURE_NAMES_PATH}")
    print(f"Saved registry to: {REGISTRY_PATH}")
    print(f"Saved metadata to: {METADATA_PATH}")


if __name__ == "__main__":
    main()