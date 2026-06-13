"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product

Module:
    app.ml.feature_builder

Purpose:
    Build machine learning feature matrix from enterprise clinical datasets.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


# ---------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "synthetic"


# ---------------------------------------------------------------------
# Dataset loader
# ---------------------------------------------------------------------

def load_dataset(filename: str) -> pd.DataFrame:
    """
    Load CSV dataset.

    Parameters
    ----------
    filename : str

    Returns
    -------
    pd.DataFrame
    """

    path = DATA_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    return pd.read_csv(path)


# ---------------------------------------------------------------------
# Feature engineering
# ---------------------------------------------------------------------

def build_feature_matrix() -> pd.DataFrame:
    """
    Build ML-ready dataframe.

    Returns
    -------
    pd.DataFrame
    """

    patients = load_dataset("01_patients.csv")

    # ---------------------------------------------------------
    # Basic feature engineering
    # ---------------------------------------------------------

    if "age" in patients.columns:

        patients["age_group"] = pd.cut(
            patients["age"],
            bins=[0, 18, 40, 60, 80, 120],
            labels=[
                "Child",
                "Young Adult",
                "Adult",
                "Senior",
                "Elderly",
            ],
        )

    if "bmi" in patients.columns:

        patients["obese"] = (
            patients["bmi"] >= 30
        ).astype(int)

    # ---------------------------------------------------------
    # Fill missing values
    # ---------------------------------------------------------

    numeric_columns = patients.select_dtypes(
        include="number"
    ).columns

    patients[numeric_columns] = (
        patients[numeric_columns]
        .fillna(
            patients[numeric_columns].median()
        )
    )

    categorical_columns = patients.select_dtypes(
        exclude="number"
    ).columns

    patients[categorical_columns] = (
        patients[categorical_columns]
        .fillna("Unknown")
    )

    return patients


# ---------------------------------------------------------------------
# Test
# ---------------------------------------------------------------------

if __name__ == "__main__":

    df = build_feature_matrix()

    print(df.head())

    print()

    print(df.shape)