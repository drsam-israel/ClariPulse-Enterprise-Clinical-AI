"""
===============================================================================
ClariPulse™ V2 - Dataset Registry Service

Purpose:
    Persistent dataset registry service for staged, production, approved,
    rejected, and pending healthcare datasets.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]

REPORT_DIR = PROJECT_ROOT / "reports" / "v2"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

REGISTRY_PATH = REPORT_DIR / "dataset_registry.csv"


REGISTRY_COLUMNS = [
    "dataset_name",
    "source",
    "status",
    "upload_timestamp",
    "rows",
    "columns",
    "missing_values",
    "duplicate_rows",
    "schema_compatible",
    "quality_score",
]


def initialize_registry() -> None:
    """Create dataset registry if it does not exist."""

    if not REGISTRY_PATH.exists():
        pd.DataFrame(columns=REGISTRY_COLUMNS).to_csv(
            REGISTRY_PATH,
            index=False,
        )


def load_dataset_registry() -> pd.DataFrame:
    """Load dataset registry safely."""

    initialize_registry()

    registry = pd.read_csv(REGISTRY_PATH)

    for column in REGISTRY_COLUMNS:
        if column not in registry.columns:
            registry[column] = pd.NA

    return registry[REGISTRY_COLUMNS]


def calculate_quality_score(
    rows: int,
    columns: int,
    missing_values: int,
    duplicate_rows: int,
    schema_compatible: bool,
) -> int:
    """
    Calculate simple enterprise data quality score.

    Score logic:
    - Starts at 100.
    - Penalizes missingness.
    - Penalizes duplicates.
    - Penalizes schema incompatibility.
    """

    if rows <= 0 or columns <= 0:
        return 0

    total_cells = rows * columns

    missing_rate = missing_values / total_cells if total_cells > 0 else 1
    duplicate_rate = duplicate_rows / rows if rows > 0 else 1

    score = 100

    score -= int(missing_rate * 100)
    score -= int(duplicate_rate * 100)

    if not schema_compatible:
        score -= 20

    return max(0, min(100, score))


def dataset_exists(dataset_name: str) -> bool:
    """Check whether a dataset already exists in the registry."""

    registry = load_dataset_registry()

    if registry.empty:
        return False

    return dataset_name in registry["dataset_name"].astype(str).tolist()


def register_dataset(
    dataset_name: str,
    source: str,
    rows: int,
    columns: int,
    missing_values: int,
    duplicate_rows: int,
    schema_compatible: bool,
    status: str = "Staged",
) -> dict:
    """
    Register a dataset in the persistent dataset registry.

    This does not activate the dataset, does not retrain models,
    and does not overwrite production data.
    """

    initialize_registry()

    registry = load_dataset_registry()

    quality_score = calculate_quality_score(
        rows=rows,
        columns=columns,
        missing_values=missing_values,
        duplicate_rows=duplicate_rows,
        schema_compatible=schema_compatible,
    )

    new_record = {
        "dataset_name": dataset_name,
        "source": source,
        "status": status,
        "upload_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rows": int(rows),
        "columns": int(columns),
        "missing_values": int(missing_values),
        "duplicate_rows": int(duplicate_rows),
        "schema_compatible": bool(schema_compatible),
        "quality_score": int(quality_score),
    }

    registry = pd.concat(
        [
            registry,
            pd.DataFrame([new_record]),
        ],
        ignore_index=True,
    )

    registry.to_csv(
        REGISTRY_PATH,
        index=False,
    )

    return new_record


def register_staged_dataset_from_summary(
    dataset_name: str,
    summary: dict,
    validation: dict,
) -> dict:
    """Register a staged dataset using upload summary and schema validation."""

    return register_dataset(
        dataset_name=dataset_name,
        source="Uploaded CSV",
        rows=int(summary.get("rows", 0)),
        columns=int(summary.get("columns", 0)),
        missing_values=int(summary.get("missing_values", 0)),
        duplicate_rows=int(summary.get("duplicate_rows", 0)),
        schema_compatible=bool(validation.get("valid", False)),
        status="Staged",
    )


def ensure_default_production_dataset() -> None:
    """Ensure the default V2 diabetes dataset is registered as production."""

    registry = load_dataset_registry()

    if "diabetes_readmission.csv" in registry["dataset_name"].astype(str).tolist():
        return

    production_record = {
        "dataset_name": "diabetes_readmission.csv",
        "source": "Default V2 Dataset",
        "status": "Production",
        "upload_timestamp": "2026-06-12 00:00:00",
        "rows": 101766,
        "columns": 50,
        "missing_values": "N/A",
        "duplicate_rows": 0,
        "schema_compatible": True,
        "quality_score": 98,
    }

    registry = pd.concat(
        [
            registry,
            pd.DataFrame([production_record]),
        ],
        ignore_index=True,
    )

    registry.to_csv(
        REGISTRY_PATH,
        index=False,
    )


def get_registry_summary() -> dict:
    """Return high-level dataset registry summary."""

    ensure_default_production_dataset()

    registry = load_dataset_registry()

    return {
        "total_datasets": int(len(registry)),
        "production_datasets": int((registry["status"] == "Production").sum()),
        "staged_datasets": int((registry["status"] == "Staged").sum()),
        "approved_datasets": int((registry["status"] == "Approved").sum()),
        "rejected_datasets": int((registry["status"] == "Rejected").sum()),
        "average_quality_score": round(
            pd.to_numeric(
                registry["quality_score"],
                errors="coerce",
            ).mean(),
            2,
        )
        if not registry.empty
        else "N/A",
    }


if __name__ == "__main__":
    ensure_default_production_dataset()
    print(load_dataset_registry())
    print(get_registry_summary())