"""
===============================================================================
ClariPulse™ V2 - Real-World Diabetes Readmission Data Loader
Author: Samuel Israel, MD
===============================================================================
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = PROJECT_ROOT / "data" / "realworld" / "diabetes_readmission.csv"


def load_diabetes_data() -> pd.DataFrame:
    """Load real-world diabetes readmission dataset."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    df = df.replace("?", pd.NA)

    return df


def summarize_diabetes_data() -> dict:
    """Return high-level dataset summary."""

    df = load_diabetes_data()

    readmission_rate_any = float(
        round((df["readmitted"] != "NO").mean() * 100, 2)
    )

    readmission_rate_30day = float(
        round((df["readmitted"] == "<30").mean() * 100, 2)
    )

    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "unique_patients": int(df["patient_nbr"].nunique())
        if "patient_nbr" in df.columns
        else "N/A",
        "encounters": int(df["encounter_id"].nunique())
        if "encounter_id" in df.columns
        else int(len(df)),
        "readmission_rate_any": readmission_rate_any,
        "readmission_rate_30day": readmission_rate_30day,
    }


if __name__ == "__main__":
    print(summarize_diabetes_data())