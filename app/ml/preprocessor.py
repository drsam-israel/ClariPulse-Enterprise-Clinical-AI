"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: app.ml.preprocessor
Purpose: Prepare ML-ready features and target variables.
Author: Samuel Israel, MD
License: MIT
===============================================================================
"""

from __future__ import annotations

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


TARGET_COLUMN = "readmission"


DROP_COLUMNS = [
    "patient_id",
    "mrn",
    "age_group",
]


def prepare_features(
    df: pd.DataFrame,
    target_column: str = TARGET_COLUMN,
) -> tuple[pd.DataFrame, pd.Series]:
    """Split dataframe into features and target."""

    if target_column not in df.columns:
        raise ValueError(f"Target column not found: {target_column}")

    y = df[target_column].astype(int)

    X = df.drop(columns=[target_column], errors="ignore")
    X = X.drop(columns=DROP_COLUMNS, errors="ignore")

    X = pd.get_dummies(X, drop_first=True)

    return X, y


def split_train_test(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42,
):
    """Create stratified train-test split."""

    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )


def scale_features(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, StandardScaler]:
    """Scale numeric feature matrix."""

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

    return X_train_scaled, X_test_scaled, scaler