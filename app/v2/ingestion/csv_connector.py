"""
===============================================================================
ClariPulse™ V2 - CSV Ingestion Connector
Author: Samuel Israel, MD
License: MIT
===============================================================================
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_csv_file(file_path: str | Path) -> pd.DataFrame:
    """Load a CSV file into a DataFrame."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    df = pd.read_csv(path)
    df = df.replace("?", pd.NA)

    return df


def validate_csv_schema(
    df: pd.DataFrame,
    required_columns: list[str],
) -> dict:
    """Validate that required columns exist in CSV data."""

    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]

    return {
        "valid": len(missing_columns) == 0,
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_columns": missing_columns,
    }


def summarize_csv(df: pd.DataFrame) -> dict:
    """Return summary of ingested CSV data."""

    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }