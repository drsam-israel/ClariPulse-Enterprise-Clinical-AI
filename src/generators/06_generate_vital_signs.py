"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: src.generators.06_generate_vital_signs
Purpose:
    Generate clinically plausible vital sign records linked to patients
    and encounters.

Author: Samuel Israel, MD
License: MIT
===============================================================================
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.reference.vital_reference import VITAL_REFERENCE  # noqa: E402


PATIENTS_PATH = PROJECT_ROOT / "data" / "synthetic" / "01_patients.csv"
ENCOUNTERS_PATH = PROJECT_ROOT / "data" / "synthetic" / "02_encounters.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "synthetic" / "06_vital_signs.csv"


def load_csv(path: Path, label: str) -> pd.DataFrame:
    """Load a required CSV file."""
    if not path.exists():
        raise FileNotFoundError(f"{label} file not found: {path}")

    return pd.read_csv(path)


def interpret_vital(vital_name: str, value: float) -> str:
    """Classify vital sign as Low, Normal, or High."""
    reference = VITAL_REFERENCE[vital_name]

    if value < float(reference["low"]):
        return "Low"

    if value > float(reference["high"]):
        return "High"

    return "Normal"


def generate_vital_value(
    *,
    vital_name: str,
    patient: pd.Series,
    encounter: pd.Series,
    rng: np.random.Generator,
) -> float:
    """Generate clinically plausible vital sign values."""

    sepsis = int(encounter.get("sepsis", 0))
    icu = int(encounter.get("icu", 0))
    copd = int(patient.get("copd", 0))
    heart_failure = int(patient.get("heart_failure", 0))

    if vital_name == "Heart Rate":
        value = rng.normal(82, 12)
        if sepsis:
            value += rng.normal(22, 8)
        if icu:
            value += rng.normal(10, 5)
        return round(float(np.clip(value, 35, 180)), 0)

    if vital_name == "Respiratory Rate":
        value = rng.normal(17, 3)
        if sepsis:
            value += rng.normal(7, 2)
        if copd:
            value += rng.normal(4, 1.5)
        return round(float(np.clip(value, 8, 45)), 0)

    if vital_name == "Temperature":
        value = rng.normal(36.9, 0.35)
        if sepsis:
            value += rng.normal(1.2, 0.45)
        return round(float(np.clip(value, 34.0, 41.5)), 1)

    if vital_name == "SpO2":
        value = rng.normal(97, 2)
        if copd:
            value -= rng.normal(4, 1.5)
        if sepsis:
            value -= rng.normal(2, 1)
        if icu:
            value -= rng.normal(1.5, 1)
        return round(float(np.clip(value, 65, 100)), 0)

    if vital_name == "Systolic Blood Pressure":
        value = rng.normal(124, 18)
        if sepsis:
            value -= rng.normal(18, 7)
        if heart_failure:
            value += rng.normal(8, 4)
        return round(float(np.clip(value, 60, 230)), 0)

    if vital_name == "Diastolic Blood Pressure":
        value = rng.normal(76, 10)
        if sepsis:
            value -= rng.normal(9, 4)
        return round(float(np.clip(value, 35, 140)), 0)

    if vital_name == "Mean Arterial Pressure":
        sbp = generate_vital_value(
            vital_name="Systolic Blood Pressure",
            patient=patient,
            encounter=encounter,
            rng=rng,
        )
        dbp = generate_vital_value(
            vital_name="Diastolic Blood Pressure",
            patient=patient,
            encounter=encounter,
            rng=rng,
        )
        value = (float(sbp) + 2 * float(dbp)) / 3
        return round(float(np.clip(value, 40, 160)), 0)

    if vital_name == "BMI":
        return round(float(patient.get("bmi", 0)), 1)

    reference = VITAL_REFERENCE[vital_name]
    return round(float(rng.uniform(reference["low"], reference["high"])), 1)


def generate_vital_signs(
    patients: pd.DataFrame,
    encounters: pd.DataFrame,
    seed: int = 42,
) -> pd.DataFrame:
    """Generate vital signs for all encounters."""
    rng = np.random.default_rng(seed)

    patient_lookup = patients.set_index("patient_id")
    records = []
    vital_counter = 1

    vital_names = list(VITAL_REFERENCE.keys())

    for encounter_row in encounters.itertuples(index=False):
        encounter = pd.Series(encounter_row._asdict())
        patient = patient_lookup.loc[encounter["patient_id"]]

        for vital_name in vital_names:
            value = generate_vital_value(
                vital_name=vital_name,
                patient=patient,
                encounter=encounter,
                rng=rng,
            )

            reference = VITAL_REFERENCE[vital_name]

            records.append(
                {
                    "vital_id": f"VITAL-{vital_counter:08d}",
                    "encounter_id": str(encounter["encounter_id"]),
                    "patient_id": str(encounter["patient_id"]),
                    "mrn": str(encounter["mrn"]),
                    "vital_name": vital_name,
                    "vital_category": reference["category"],
                    "value": value,
                    "unit": reference["unit"],
                    "reference_low": reference["low"],
                    "reference_high": reference["high"],
                    "result_flag": interpret_vital(vital_name, value),
                    "recorded_date": str(encounter["encounter_date"]),
                }
            )

            vital_counter += 1

    return pd.DataFrame(records)


def validate_output(vitals: pd.DataFrame, encounters: pd.DataFrame) -> None:
    """Validate generated vital signs output."""
    if vitals.empty:
        raise ValueError("Generated vital signs dataset is empty.")

    if vitals["vital_id"].duplicated().any():
        raise ValueError("Duplicate vital_id values detected.")

    invalid_encounters = set(vitals["encounter_id"]) - set(encounters["encounter_id"])

    if invalid_encounters:
        raise ValueError("Vital signs contain unknown encounter_id values.")


def save_vitals(vitals: pd.DataFrame, output_path: Path = OUTPUT_PATH) -> None:
    """Save vital signs dataset."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    vitals.to_csv(output_path, index=False)


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate ClariPulse synthetic vital signs dataset."
    )

    parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()

    patients = load_csv(PATIENTS_PATH, "Patients")
    encounters = load_csv(ENCOUNTERS_PATH, "Encounters")

    vitals = generate_vital_signs(
        patients=patients,
        encounters=encounters,
        seed=args.seed,
    )

    validate_output(vitals, encounters)
    save_vitals(vitals)

    print(f"Generated {len(vitals):,} vital sign records")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()