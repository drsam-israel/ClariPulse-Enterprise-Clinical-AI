"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: src.generators.08_generate_governance_logs
Purpose:
    Generate AI governance audit logs linked to prediction records.

Author: Samuel Israel, MD
License: MIT
===============================================================================
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.reference.governance_config import (  # noqa: E402
    BIAS_CHECK_STATUS,
    CRITICAL_RISK_THRESHOLD,
    DEFAULT_REVIEWER,
    DRIFT_CHECK_STATUS,
    EXPLAINABILITY_STATUS,
    HIGH_RISK_THRESHOLD,
    MODEL_APPROVAL_STATUS,
    REQUIRE_HUMAN_REVIEW_FOR_CRITICAL,
)


PREDICTIONS_PATH = PROJECT_ROOT / "data" / "synthetic" / "07_predictions.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "synthetic" / "08_governance_logs.csv"


def load_csv(path: Path, label: str) -> pd.DataFrame:
    """Load a required CSV file."""
    if not path.exists():
        raise FileNotFoundError(f"{label} file not found: {path}")

    return pd.read_csv(path)


def classify_governance_decision(row: pd.Series) -> str:
    """Determine governance decision based on risk and review rules."""
    composite_risk = float(row.get("composite_risk_score", 0))
    human_review_required = str(row.get("human_review_required", "No"))

    if composite_risk >= CRITICAL_RISK_THRESHOLD:
        return "Escalate for Clinical Review"

    if human_review_required == "Yes":
        return "Human Review Required"

    if composite_risk >= HIGH_RISK_THRESHOLD:
        return "Monitor Closely"

    return "Approved for Automated Use"


def determine_human_review(row: pd.Series) -> str:
    """Apply governance policy for human review."""
    composite_risk = float(row.get("composite_risk_score", 0))

    if REQUIRE_HUMAN_REVIEW_FOR_CRITICAL and composite_risk >= CRITICAL_RISK_THRESHOLD:
        return "Yes"

    return str(row.get("human_review_required", "No"))

# =============================================================================
# GOVERNANCE LOG BUILDER
# =============================================================================


def build_governance_record(
    *,
    log_id: str,
    prediction_row: pd.Series,
    review_timestamp: str,
) -> dict[str, str | float]:
    """Build one governance audit log record."""

    human_review = determine_human_review(prediction_row)

    return {
        "log_id": log_id,
        "prediction_id": str(prediction_row["prediction_id"]),
        "encounter_id": str(prediction_row["encounter_id"]),
        "patient_id": str(prediction_row["patient_id"]),
        "mrn": str(prediction_row["mrn"]),
        "model_name": str(prediction_row["champion_model"]),
        "model_version": str(prediction_row["model_version"]),
        "model_type": str(prediction_row["model_type"]),
        "prediction_status": str(prediction_row["prediction_status"]),
        "composite_risk_score": float(prediction_row["composite_risk_score"]),
        "risk_category": str(prediction_row["risk_category"]),
        "human_review_required": human_review,
        "bias_check_status": BIAS_CHECK_STATUS,
        "drift_check_status": DRIFT_CHECK_STATUS,
        "explainability_status": EXPLAINABILITY_STATUS,
        "model_approval_status": MODEL_APPROVAL_STATUS,
        "governance_decision": classify_governance_decision(prediction_row),
        "review_timestamp": review_timestamp,
        "reviewed_by": DEFAULT_REVIEWER,
    }


def generate_governance_logs(
    predictions: pd.DataFrame,
) -> pd.DataFrame:
    """Generate governance logs for all prediction records."""

    review_timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    records = []

    for index, prediction_row in enumerate(
        predictions.itertuples(index=False),
        start=1,
    ):
        prediction = pd.Series(prediction_row._asdict())

        records.append(
            build_governance_record(
                log_id=f"GOV-{index:08d}",
                prediction_row=prediction,
                review_timestamp=review_timestamp,
            )
        )

    return pd.DataFrame(records)

# =============================================================================
# VALIDATION
# =============================================================================


def validate_output(
    governance_logs: pd.DataFrame,
    predictions: pd.DataFrame,
) -> None:
    """Validate generated governance logs."""

    if governance_logs.empty:
        raise ValueError("Generated governance logs dataset is empty.")

    if governance_logs["log_id"].duplicated().any():
        raise ValueError("Duplicate log_id values detected.")

    if governance_logs["prediction_id"].duplicated().any():
        raise ValueError("Each prediction should have exactly one governance log.")

    invalid_predictions = set(governance_logs["prediction_id"]) - set(
        predictions["prediction_id"]
    )

    if invalid_predictions:
        raise ValueError("Governance logs contain unknown prediction_id values.")


# =============================================================================
# SAVE OUTPUT
# =============================================================================


def save_governance_logs(
    governance_logs: pd.DataFrame,
    output_path: Path = OUTPUT_PATH,
) -> None:
    """Save governance logs dataset."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    governance_logs.to_csv(output_path, index=False)


# =============================================================================
# MAIN
# =============================================================================


def main() -> None:
    """CLI entry point."""

    parser = argparse.ArgumentParser(
        description="Generate ClariPulse AI governance audit logs."
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Reserved for future stochastic governance simulations.",
    )

    parser.parse_args()

    print("\nLoading predictions...")

    predictions = load_csv(PREDICTIONS_PATH, "Predictions")

    print(f"Loaded {len(predictions):,} predictions")

    print("\nGenerating governance logs...")

    governance_logs = generate_governance_logs(predictions)

    validate_output(
        governance_logs=governance_logs,
        predictions=predictions,
    )

    save_governance_logs(governance_logs)

    print(f"\nGenerated {len(governance_logs):,} governance logs")
    print(f"Saved to: {OUTPUT_PATH}")


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()