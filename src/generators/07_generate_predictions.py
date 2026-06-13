"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: src.generators.07_generate_predictions
Purpose:
    Generate explainable clinical AI prediction records using a transparent
    weighted clinical rules engine.

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


from src.reference.prediction_config import (  # noqa: E402
    CHAMPION_MODEL,
    DEFAULT_STATUS,
    HIGH_THRESHOLD,
    HUMAN_REVIEW_THRESHOLD,
    LOW_THRESHOLD,
    MODERATE_THRESHOLD,
    MODEL_TYPE,
    MODEL_VERSION,
)


PATIENTS_PATH = PROJECT_ROOT / "data" / "synthetic" / "01_patients.csv"
ENCOUNTERS_PATH = PROJECT_ROOT / "data" / "synthetic" / "02_encounters.csv"
LABS_PATH = PROJECT_ROOT / "data" / "synthetic" / "05_laboratory_results.csv"
VITALS_PATH = PROJECT_ROOT / "data" / "synthetic" / "06_vital_signs.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "synthetic" / "07_predictions.csv"


def load_csv(path: Path, label: str) -> pd.DataFrame:
    """Load a required CSV file."""
    if not path.exists():
        raise FileNotFoundError(f"{label} file not found: {path}")

    return pd.read_csv(path)


def get_risk_category(score: float) -> str:
    """Convert composite risk score into category."""
    if score < LOW_THRESHOLD:
        return "Low"

    if score < MODERATE_THRESHOLD:
        return "Moderate"

    if score < HIGH_THRESHOLD:
        return "High"

    return "Critical"


def normalize_score(score: float, max_score: float) -> float:
    """Normalize score to probability between 0 and 0.99."""
    if max_score <= 0:
        return 0.0

    return round(float(min(score / max_score, 0.99)), 4)


def get_latest_lab_values(labs: pd.DataFrame) -> pd.DataFrame:
    """Pivot laboratory records into one row per encounter."""
    selected = labs[
        ["encounter_id", "test_name", "result_value"]
    ].copy()

    pivoted = selected.pivot_table(
        index="encounter_id",
        columns="test_name",
        values="result_value",
        aggfunc="mean",
    ).reset_index()

    return pivoted


def get_latest_vital_values(vitals: pd.DataFrame) -> pd.DataFrame:
    """Pivot vital records into one row per encounter."""
    selected = vitals[
        ["encounter_id", "vital_name", "value"]
    ].copy()

    pivoted = selected.pivot_table(
        index="encounter_id",
        columns="vital_name",
        values="value",
        aggfunc="mean",
    ).reset_index()

    return pivoted

# =============================================================================
# CLINICAL RISK SCORING
# =============================================================================


def score_mortality(row: pd.Series) -> tuple[int, list[str]]:
    """Calculate mortality score and contributing risk factors."""
    score = 0
    factors: list[str] = []

    if int(row.get("age", 0)) >= 75:
        score += 15
        factors.append("Advanced Age")

    if int(row.get("icu", 0)) == 1:
        score += 25
        factors.append("ICU Admission")

    if int(row.get("sepsis", 0)) == 1:
        score += 20
        factors.append("Sepsis")

    if float(row.get("Lactate", 0)) > 2.2:
        score += 15
        factors.append("Elevated Lactate")

    if float(row.get("Creatinine", 0)) > 1.3:
        score += 10
        factors.append("Elevated Creatinine")

    if float(row.get("SpO2", 100)) < 92:
        score += 10
        factors.append("Low SpO2")

    if float(row.get("Heart Rate", 0)) > 110:
        score += 5
        factors.append("Tachycardia")

    if float(row.get("Systolic Blood Pressure", 999)) < 90:
        score += 10
        factors.append("Hypotension")

    return score, factors


def score_readmission(row: pd.Series) -> tuple[int, list[str]]:
    """Calculate readmission score and contributing risk factors."""
    score = 0
    factors: list[str] = []

    if int(row.get("diabetes", 0)) == 1:
        score += 10
        factors.append("Diabetes")

    if int(row.get("ckd", 0)) == 1:
        score += 15
        factors.append("CKD")

    if int(row.get("heart_failure", 0)) == 1:
        score += 20
        factors.append("Heart Failure")

    if float(row.get("length_of_stay_days", 0)) > 7:
        score += 15
        factors.append("Long Length of Stay")

    if int(row.get("age", 0)) >= 70:
        score += 10
        factors.append("Older Age")

    if int(row.get("copd", 0)) == 1:
        score += 10
        factors.append("COPD")

    if int(row.get("cancer", 0)) == 1:
        score += 15
        factors.append("Cancer")

    return score, factors


def score_sepsis(row: pd.Series) -> tuple[int, list[str]]:
    """Calculate sepsis score and contributing risk factors."""
    score = 0
    factors: list[str] = []

    if float(row.get("Temperature", 0)) > 38.0:
        score += 15
        factors.append("Fever")

    if float(row.get("WBC", 0)) > 11:
        score += 15
        factors.append("Elevated WBC")

    if float(row.get("Lactate", 0)) > 2.2:
        score += 20
        factors.append("Elevated Lactate")

    if float(row.get("CRP", 0)) > 10:
        score += 15
        factors.append("Elevated CRP")

    if float(row.get("Heart Rate", 0)) > 100:
        score += 10
        factors.append("Tachycardia")

    if float(row.get("Respiratory Rate", 0)) > 20:
        score += 10
        factors.append("Tachypnea")

    if int(row.get("icu", 0)) == 1:
        score += 15
        factors.append("ICU Admission")

    return score, factors


def get_top_risk_factors(*factor_lists: list[str]) -> list[str]:
    """Return top three unique risk factors."""
    combined: list[str] = []

    for factor_list in factor_lists:
        for factor in factor_list:
            if factor not in combined:
                combined.append(factor)

    while len(combined) < 3:
        combined.append("No Major Driver")

    return combined[:3]

# =============================================================================
# FEATURE TABLE
# =============================================================================


def build_feature_table(
    patients: pd.DataFrame,
    encounters: pd.DataFrame,
    labs: pd.DataFrame,
    vitals: pd.DataFrame,
) -> pd.DataFrame:
    """Build one prediction-ready feature row per encounter."""
    lab_features = get_latest_lab_values(labs)
    vital_features = get_latest_vital_values(vitals)

    features = encounters.merge(
        patients,
        on=["patient_id", "mrn"],
        how="left",
        suffixes=("_encounter", "_patient"),
    )

    features = features.merge(
        lab_features,
        on="encounter_id",
        how="left",
    )

    features = features.merge(
        vital_features,
        on="encounter_id",
        how="left",
    )

    return features


def calculate_composite_risk(
    mortality_probability: float,
    readmission_probability: float,
    sepsis_probability: float,
) -> float:
    """Calculate weighted composite risk score."""
    return round(
        float(
            (0.45 * mortality_probability)
            + (0.30 * readmission_probability)
            + (0.25 * sepsis_probability)
        ),
        4,
    )


def human_review_required(composite_risk_score: float) -> str:
    """Determine whether human review is required."""
    return "Yes" if composite_risk_score >= HUMAN_REVIEW_THRESHOLD else "No"


def build_prediction_record(
    *,
    prediction_id: str,
    row: pd.Series,
    timestamp: str,
) -> dict[str, str | int | float]:
    """Build one prediction record."""
    mortality_score, mortality_factors = score_mortality(row)
    readmission_score, readmission_factors = score_readmission(row)
    sepsis_score, sepsis_factors = score_sepsis(row)

    mortality_probability = normalize_score(mortality_score, 110)
    readmission_probability = normalize_score(readmission_score, 80)
    sepsis_probability = normalize_score(sepsis_score, 85)

    composite_risk_score = calculate_composite_risk(
        mortality_probability,
        readmission_probability,
        sepsis_probability,
    )

    top_factors = get_top_risk_factors(
        mortality_factors,
        readmission_factors,
        sepsis_factors,
    )

    return {
        "prediction_id": prediction_id,
        "encounter_id": str(row["encounter_id"]),
        "patient_id": str(row["patient_id"]),
        "mrn": str(row["mrn"]),
        "mortality_score": mortality_score,
        "mortality_probability": mortality_probability,
        "readmission_score": readmission_score,
        "readmission_probability": readmission_probability,
        "sepsis_score": sepsis_score,
        "sepsis_probability": sepsis_probability,
        "composite_risk_score": composite_risk_score,
        "risk_category": get_risk_category(composite_risk_score),
        "champion_model": CHAMPION_MODEL,
        "model_version": MODEL_VERSION,
        "model_type": MODEL_TYPE,
        "prediction_status": DEFAULT_STATUS,
        "human_review_required": human_review_required(composite_risk_score),
        "top_risk_factor_1": top_factors[0],
        "top_risk_factor_2": top_factors[1],
        "top_risk_factor_3": top_factors[2],
        "prediction_timestamp": timestamp,
    }


def generate_predictions(
    patients: pd.DataFrame,
    encounters: pd.DataFrame,
    labs: pd.DataFrame,
    vitals: pd.DataFrame,
) -> pd.DataFrame:
    """Generate prediction records for all encounters."""
    features = build_feature_table(
        patients=patients,
        encounters=encounters,
        labs=labs,
        vitals=vitals,
    )

    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    records = []

    for index, row in enumerate(features.itertuples(index=False), start=1):
        series = pd.Series(row._asdict())

        records.append(
            build_prediction_record(
                prediction_id=f"PRED-{index:08d}",
                row=series,
                timestamp=timestamp,
            )
        )

    return pd.DataFrame(records)

# =============================================================================
# VALIDATION
# =============================================================================


def validate_output(
    predictions: pd.DataFrame,
    encounters: pd.DataFrame,
) -> None:
    """Validate generated prediction records."""
    if predictions.empty:
        raise ValueError("Generated predictions dataset is empty.")

    if predictions["prediction_id"].duplicated().any():
        raise ValueError("Duplicate prediction_id values detected.")

    invalid_encounters = set(predictions["encounter_id"]) - set(
        encounters["encounter_id"]
    )

    if invalid_encounters:
        raise ValueError("Predictions contain unknown encounter_id values.")

    probability_columns = [
        "mortality_probability",
        "readmission_probability",
        "sepsis_probability",
        "composite_risk_score",
    ]

    for column in probability_columns:
        if not predictions[column].between(0, 1).all():
            raise ValueError(f"{column} contains values outside 0–1 range.")


# =============================================================================
# SAVE OUTPUT
# =============================================================================


def save_predictions(
    predictions: pd.DataFrame,
    output_path: Path = OUTPUT_PATH,
) -> None:
    """Save predictions dataset."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(output_path, index=False)


# =============================================================================
# MAIN
# =============================================================================


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate ClariPulse explainable AI prediction records."
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Reserved for future stochastic model simulation.",
    )

    parser.parse_args()

    print("\nLoading datasets...")

    patients = load_csv(PATIENTS_PATH, "Patients")
    encounters = load_csv(ENCOUNTERS_PATH, "Encounters")
    labs = load_csv(LABS_PATH, "Laboratory Results")
    vitals = load_csv(VITALS_PATH, "Vital Signs")

    print(f"Loaded {len(patients):,} patients")
    print(f"Loaded {len(encounters):,} encounters")
    print(f"Loaded {len(labs):,} laboratory results")
    print(f"Loaded {len(vitals):,} vital sign records")

    print("\nGenerating explainable predictions...")

    predictions = generate_predictions(
        patients=patients,
        encounters=encounters,
        labs=labs,
        vitals=vitals,
    )

    validate_output(predictions, encounters)
    save_predictions(predictions)

    print(f"\nGenerated {len(predictions):,} predictions")
    print(f"Saved to: {OUTPUT_PATH}")


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()