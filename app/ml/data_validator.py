"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product

Module:
    app.ml.data_validator

Purpose:
    Validate enterprise synthetic datasets before feature engineering
    and model training.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "synthetic"


def validate_dataset(filename: str) -> dict:
    """
    Validate a CSV dataset.

    Returns
    -------
    dict
        Validation summary.
    """

    path = DATA_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Missing dataset: {path}")

    df = pd.read_csv(path)

    return {
        "dataset": filename,
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }


def validate_all() -> pd.DataFrame:
    """
    Validate all synthetic datasets.
    """

    datasets = [
        "01_patients.csv",
        "02_encounters.csv",
        "03_diagnoses.csv",
        "04_medications.csv",
        "05_laboratory_results.csv",
        "06_vital_signs.csv",
        "07_predictions.csv",
        "08_governance_logs.csv",
        "09_executive_metrics.csv",
    ]

    results = [validate_dataset(ds) for ds in datasets]

    return pd.DataFrame(results)


if __name__ == "__main__":

    summary = validate_all()

    print(summary)