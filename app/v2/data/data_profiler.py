"""
===============================================================================
ClariPulse™ V2 - Real-World Diabetes Data Profiler

Purpose:
    Generate an enterprise data profile for the real-world diabetes
    readmission dataset.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.v2.data.diabetes_loader import load_diabetes_data


PROJECT_ROOT = Path(__file__).resolve().parents[3]

REPORT_DIR = PROJECT_ROOT / "reports" / "v2"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

DATA_PROFILE_PATH = REPORT_DIR / "diabetes_data_profile.csv"
MISSINGNESS_PATH = REPORT_DIR / "diabetes_missingness_profile.csv"
TARGET_PROFILE_PATH = REPORT_DIR / "diabetes_target_profile.csv"
DEMOGRAPHICS_PROFILE_PATH = REPORT_DIR / "diabetes_demographics_profile.csv"
ADMISSION_PROFILE_PATH = REPORT_DIR / "diabetes_admission_profile.csv"


def profile_missingness(df: pd.DataFrame) -> pd.DataFrame:
    """Generate missingness profile."""

    profile = pd.DataFrame(
        {
            "feature": df.columns,
            "missing_count": df.isna().sum().values,
            "missing_percent": (df.isna().mean().values * 100).round(2),
            "dtype": [str(dtype) for dtype in df.dtypes],
        }
    )

    return profile.sort_values("missing_percent", ascending=False)


def profile_target(df: pd.DataFrame) -> pd.DataFrame:
    """Generate readmission target profile."""

    if "readmitted" not in df.columns:
        return pd.DataFrame()

    target = (
        df["readmitted"]
        .value_counts(dropna=False)
        .rename_axis("readmitted")
        .reset_index(name="count")
    )

    target["percent"] = (target["count"] / len(df) * 100).round(2)

    return target


def profile_demographics(df: pd.DataFrame) -> pd.DataFrame:
    """Generate demographic profile."""

    rows = []

    for column in ["race", "gender", "age"]:
        if column in df.columns:
            temp = (
                df[column]
                .value_counts(dropna=False)
                .rename_axis("category")
                .reset_index(name="count")
            )
            temp["feature"] = column
            temp["percent"] = (temp["count"] / len(df) * 100).round(2)
            rows.append(temp[["feature", "category", "count", "percent"]])

    if not rows:
        return pd.DataFrame(columns=["feature", "category", "count", "percent"])

    return pd.concat(rows, ignore_index=True)


def profile_admissions(df: pd.DataFrame) -> pd.DataFrame:
    """Generate admission and utilization profile."""

    admission_columns = [
        "admission_type_id",
        "discharge_disposition_id",
        "admission_source_id",
        "time_in_hospital",
        "num_lab_procedures",
        "num_procedures",
        "num_medications",
        "number_outpatient",
        "number_emergency",
        "number_inpatient",
    ]

    rows = []

    for column in admission_columns:
        if column in df.columns:
            if pd.api.types.is_numeric_dtype(df[column]):
                rows.append(
                    {
                        "feature": column,
                        "metric": "mean",
                        "value": round(df[column].mean(), 2),
                    }
                )
                rows.append(
                    {
                        "feature": column,
                        "metric": "median",
                        "value": round(df[column].median(), 2),
                    }
                )
                rows.append(
                    {
                        "feature": column,
                        "metric": "max",
                        "value": round(df[column].max(), 2),
                    }
                )
            else:
                top_value = df[column].mode(dropna=True)
                rows.append(
                    {
                        "feature": column,
                        "metric": "top_category",
                        "value": top_value.iloc[0] if not top_value.empty else "N/A",
                    }
                )

    return pd.DataFrame(rows)


def generate_data_profile() -> dict:
    """Generate and save all V2 data profile outputs."""

    df = load_diabetes_data()

    data_profile = pd.DataFrame(
        [
            {
                "rows": int(len(df)),
                "columns": int(len(df.columns)),
                "unique_patients": int(df["patient_nbr"].nunique())
                if "patient_nbr" in df.columns
                else "N/A",
                "encounters": int(df["encounter_id"].nunique())
                if "encounter_id" in df.columns
                else int(len(df)),
                "duplicate_rows": int(df.duplicated().sum()),
                "readmission_any_rate": float(
                    round((df["readmitted"] != "NO").mean() * 100, 2)
                )
                if "readmitted" in df.columns
                else "N/A",
                "readmission_30day_rate": float(
                    round((df["readmitted"] == "<30").mean() * 100, 2)
                )
                if "readmitted" in df.columns
                else "N/A",
            }
        ]
    )

    missingness_profile = profile_missingness(df)
    target_profile = profile_target(df)
    demographics_profile = profile_demographics(df)
    admission_profile = profile_admissions(df)

    data_profile.to_csv(DATA_PROFILE_PATH, index=False)
    missingness_profile.to_csv(MISSINGNESS_PATH, index=False)
    target_profile.to_csv(TARGET_PROFILE_PATH, index=False)
    demographics_profile.to_csv(DEMOGRAPHICS_PROFILE_PATH, index=False)
    admission_profile.to_csv(ADMISSION_PROFILE_PATH, index=False)

    return {
        "data_profile": str(DATA_PROFILE_PATH),
        "missingness_profile": str(MISSINGNESS_PATH),
        "target_profile": str(TARGET_PROFILE_PATH),
        "demographics_profile": str(DEMOGRAPHICS_PROFILE_PATH),
        "admission_profile": str(ADMISSION_PROFILE_PATH),
    }


if __name__ == "__main__":
    outputs = generate_data_profile()

    print("\nClariPulse™ V2 Data Profile Generated Successfully\n")

    for name, path in outputs.items():
        print(f"{name}: {path}")