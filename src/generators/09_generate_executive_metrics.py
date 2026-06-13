"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: src.generators.09_generate_executive_metrics
Purpose:
    Generate executive KPI metrics for the ClariPulse™ Executive Command Center.

Author: Samuel Israel, MD
License: MIT
===============================================================================
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.reference.executive_config import (  # noqa: E402
    ALERT_RECOMMENDATION,
    CRITICAL_RISK_ALERT_THRESHOLD,
    DEFAULT_GOVERNANCE_STATUS,
    HUMAN_REVIEW_ALERT_THRESHOLD,
    NORMAL_RECOMMENDATION,
)

from src.reference.model_registry import ACTIVE_MODEL  # noqa: E402


DATA_DIR = PROJECT_ROOT / "data" / "synthetic"

PATIENTS_PATH = DATA_DIR / "01_patients.csv"
ENCOUNTERS_PATH = DATA_DIR / "02_encounters.csv"
DIAGNOSES_PATH = DATA_DIR / "03_diagnoses.csv"
MEDICATIONS_PATH = DATA_DIR / "04_medications.csv"
LABS_PATH = DATA_DIR / "05_laboratory_results.csv"
VITALS_PATH = DATA_DIR / "06_vital_signs.csv"
PREDICTIONS_PATH = DATA_DIR / "07_predictions.csv"
GOVERNANCE_PATH = DATA_DIR / "08_governance_logs.csv"
OUTPUT_PATH = DATA_DIR / "09_executive_metrics.csv"


def load_csv(path: Path, label: str) -> pd.DataFrame:
    """Load a required CSV file."""
    if not path.exists():
        raise FileNotFoundError(f"{label} file not found: {path}")

    return pd.read_csv(path)

# =============================================================================
# EXECUTIVE KPI CALCULATIONS
# =============================================================================


def calculate_ai_approval_rate(governance_logs: pd.DataFrame) -> float:
    """Calculate percentage of governance logs approved for automated use."""
    if governance_logs.empty:
        return 0.0

    approved = governance_logs[
        governance_logs["governance_decision"] == "Approved for Automated Use"
    ]

    return round((len(approved) / len(governance_logs)) * 100, 2)


def calculate_bias_pass_rate(governance_logs: pd.DataFrame) -> float:
    """Calculate percentage of records passing bias checks."""
    if governance_logs.empty:
        return 0.0

    passed = governance_logs[
        governance_logs["bias_check_status"] == "Passed"
    ]

    return round((len(passed) / len(governance_logs)) * 100, 2)


def get_drift_status(governance_logs: pd.DataFrame) -> str:
    """Return dominant drift status."""
    if governance_logs.empty:
        return "Unknown"

    return str(
        governance_logs["drift_check_status"]
        .mode()
        .iloc[0]
    )


def calculate_risk_counts(predictions: pd.DataFrame) -> dict[str, int]:
    """Calculate counts by risk category."""
    counts = predictions["risk_category"].value_counts().to_dict()

    return {
        "low_risk_patients": int(counts.get("Low", 0)),
        "moderate_risk_patients": int(counts.get("Moderate", 0)),
        "high_risk_patients": int(counts.get("High", 0)),
        "critical_risk_patients": int(counts.get("Critical", 0)),
    }


def get_executive_recommendation(
    *,
    total_predictions: int,
    critical_risk_patients: int,
    human_review_queue: int,
) -> str:
    """Generate executive recommendation based on risk and review queue."""
    if total_predictions == 0:
        return ALERT_RECOMMENDATION

    critical_rate = critical_risk_patients / total_predictions

    if (
        critical_rate >= CRITICAL_RISK_ALERT_THRESHOLD
        or human_review_queue >= HUMAN_REVIEW_ALERT_THRESHOLD
    ):
        return ALERT_RECOMMENDATION

    return NORMAL_RECOMMENDATION

# =============================================================================
# EXECUTIVE METRIC BUILDER
# =============================================================================


def build_executive_metrics(
    *,
    patients: pd.DataFrame,
    encounters: pd.DataFrame,
    diagnoses: pd.DataFrame,
    medications: pd.DataFrame,
    labs: pd.DataFrame,
    vitals: pd.DataFrame,
    predictions: pd.DataFrame,
    governance_logs: pd.DataFrame,
) -> pd.DataFrame:
    """Build one executive KPI snapshot row."""

    risk_counts = calculate_risk_counts(predictions)

    total_predictions = len(predictions)

    human_review_queue = int(
        (predictions["human_review_required"] == "Yes").sum()
    )

    critical_risk_patients = risk_counts["critical_risk_patients"]

    recommendation = get_executive_recommendation(
        total_predictions=total_predictions,
        critical_risk_patients=critical_risk_patients,
        human_review_queue=human_review_queue,
    )

    metrics = {
        "report_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "total_patients": len(patients),
        "total_encounters": len(encounters),
        "total_diagnoses": len(diagnoses),
        "total_medications": len(medications),
        "total_lab_results": len(labs),
        "total_vital_signs": len(vitals),
        "total_predictions": total_predictions,
        "total_governance_logs": len(governance_logs),
        "average_composite_risk": round(
            float(predictions["composite_risk_score"].mean()),
            4,
        ),
        **risk_counts,
        "human_review_queue": human_review_queue,
        "ai_approval_rate": calculate_ai_approval_rate(governance_logs),
        "bias_pass_rate": calculate_bias_pass_rate(governance_logs),
        "drift_status": get_drift_status(governance_logs),
        "champion_model": ACTIVE_MODEL["model_name"],
        "model_version": ACTIVE_MODEL["version"],
        "governance_status": DEFAULT_GOVERNANCE_STATUS,
        "executive_recommendation": recommendation,
    }

    return pd.DataFrame([metrics])

# =============================================================================
# VALIDATION
# =============================================================================


def validate_output(metrics: pd.DataFrame) -> None:
    """Validate executive metrics output."""

    if metrics.empty:
        raise ValueError("Executive metrics dataset is empty.")

    if len(metrics) != 1:
        raise ValueError("Executive metrics should contain exactly one row.")

    required_columns = {
        "report_date",
        "total_patients",
        "total_encounters",
        "total_diagnoses",
        "total_medications",
        "total_lab_results",
        "total_vital_signs",
        "total_predictions",
        "total_governance_logs",
        "average_composite_risk",
        "low_risk_patients",
        "moderate_risk_patients",
        "high_risk_patients",
        "critical_risk_patients",
        "human_review_queue",
        "ai_approval_rate",
        "bias_pass_rate",
        "drift_status",
        "champion_model",
        "model_version",
        "governance_status",
        "executive_recommendation",
    }

    missing = required_columns - set(metrics.columns)

    if missing:
        raise ValueError(f"Missing executive metric columns: {sorted(missing)}")


# =============================================================================
# SAVE OUTPUT
# =============================================================================


def save_executive_metrics(
    metrics: pd.DataFrame,
    output_path: Path = OUTPUT_PATH,
) -> None:
    """Save executive metrics dataset."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(output_path, index=False)


# =============================================================================
# MAIN
# =============================================================================


def main() -> None:
    """CLI entry point."""

    parser = argparse.ArgumentParser(
        description="Generate ClariPulse executive KPI metrics."
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Reserved for future executive scenario simulation.",
    )

    parser.parse_args()

    print("\nLoading datasets...")

    patients = load_csv(PATIENTS_PATH, "Patients")
    encounters = load_csv(ENCOUNTERS_PATH, "Encounters")
    diagnoses = load_csv(DIAGNOSES_PATH, "Diagnoses")
    medications = load_csv(MEDICATIONS_PATH, "Medications")
    labs = load_csv(LABS_PATH, "Laboratory Results")
    vitals = load_csv(VITALS_PATH, "Vital Signs")
    predictions = load_csv(PREDICTIONS_PATH, "Predictions")
    governance_logs = load_csv(GOVERNANCE_PATH, "Governance Logs")

    print(f"Loaded {len(patients):,} patients")
    print(f"Loaded {len(encounters):,} encounters")
    print(f"Loaded {len(diagnoses):,} diagnoses")
    print(f"Loaded {len(medications):,} medications")
    print(f"Loaded {len(labs):,} laboratory results")
    print(f"Loaded {len(vitals):,} vital sign records")
    print(f"Loaded {len(predictions):,} predictions")
    print(f"Loaded {len(governance_logs):,} governance logs")

    print("\nGenerating executive metrics...")

    metrics = build_executive_metrics(
        patients=patients,
        encounters=encounters,
        diagnoses=diagnoses,
        medications=medications,
        labs=labs,
        vitals=vitals,
        predictions=predictions,
        governance_logs=governance_logs,
    )

    validate_output(metrics)
    save_executive_metrics(metrics)

    print(f"\nGenerated {len(metrics):,} executive metrics row")
    print(f"Saved to: {OUTPUT_PATH}")


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()