"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: src.generators.05_generate_laboratory_results
Purpose:
    Generate clinically plausible laboratory results linked to patients
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

from src.reference.laboratory_reference import LABORATORY_REFERENCE  # noqa: E402


PATIENTS_PATH = PROJECT_ROOT / "data" / "synthetic" / "01_patients.csv"
ENCOUNTERS_PATH = PROJECT_ROOT / "data" / "synthetic" / "02_encounters.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "synthetic" / "05_laboratory_results.csv"


def load_csv(path: Path, label: str) -> pd.DataFrame:
    """Load a required CSV file."""
    if not path.exists():
        raise FileNotFoundError(f"{label} file not found: {path}")

    return pd.read_csv(path)


def generate_lab_value(
    *,
    test_name: str,
    patient: pd.Series,
    encounter: pd.Series,
    rng: np.random.Generator,
) -> float:
    """Generate clinically plausible lab values."""

    if test_name == "Hemoglobin":
        value = rng.normal(13.8, 1.5)
        if int(patient.get("ckd", 0)) == 1:
            value -= rng.normal(1.2, 0.4)
        return round(float(np.clip(value, 6.5, 19.5)), 1)

    if test_name == "WBC":
        value = rng.normal(7.5, 2.0)
        if int(patient.get("sepsis", 0)) == 1:
            value += rng.normal(5.0, 2.2)
        return round(float(np.clip(value, 1.5, 35.0)), 1)

    if test_name == "Platelets":
        value = rng.normal(260, 70)
        if int(patient.get("sepsis", 0)) == 1:
            value -= rng.normal(45, 20)
        return round(float(np.clip(value, 40, 750)), 0)

    if test_name == "Creatinine":
        value = rng.normal(0.95, 0.25)
        if int(patient.get("ckd", 0)) == 1:
            value += rng.normal(1.2, 0.5)
        if int(encounter.get("icu", 0)) == 1:
            value += rng.normal(0.25, 0.1)
        return round(float(np.clip(value, 0.3, 7.5)), 2)

    if test_name == "Sodium":
        value = rng.normal(139, 3)
        if int(encounter.get("sepsis", 0)) == 1:
            value -= rng.normal(2, 1)
        return round(float(np.clip(value, 118, 160)), 1)

    if test_name == "Potassium":
        value = rng.normal(4.2, 0.45)
        if int(patient.get("ckd", 0)) == 1:
            value += rng.normal(0.35, 0.15)
        return round(float(np.clip(value, 2.5, 7.2)), 1)

    if test_name == "Glucose":
        value = rng.normal(115, 30)
        if int(patient.get("diabetes", 0)) == 1:
            value += rng.normal(70, 25)
        return round(float(np.clip(value, 45, 550)), 0)

    if test_name == "HbA1c":
        value = rng.normal(5.5, 0.5)
        if int(patient.get("diabetes", 0)) == 1:
            value += rng.normal(2.0, 0.8)
        return round(float(np.clip(value, 4.0, 14.0)), 1)

    if test_name == "Lactate":
        value = rng.normal(1.3, 0.45)
        if int(encounter.get("sepsis", 0)) == 1:
            value += rng.normal(2.5, 1.0)
        if int(encounter.get("icu", 0)) == 1:
            value += rng.normal(0.8, 0.3)
        return round(float(np.clip(value, 0.4, 12.0)), 1)

    if test_name == "CRP":
        value = rng.normal(6, 4)
        if int(encounter.get("sepsis", 0)) == 1:
            value += rng.normal(95, 35)
        return round(float(np.clip(value, 0, 320)), 1)

    reference = LABORATORY_REFERENCE[test_name]
    return round(float(rng.uniform(reference["low"], reference["high"])), 2)


def interpret_result(test_name: str, value: float) -> str:
    """Classify lab result as Low, Normal, or High."""
    reference = LABORATORY_REFERENCE[test_name]

    if value < float(reference["low"]):
        return "Low"

    if value > float(reference["high"]):
        return "High"

    return "Normal"


def generate_laboratory_results(
    patients: pd.DataFrame,
    encounters: pd.DataFrame,
    seed: int = 42,
) -> pd.DataFrame:
    """Generate lab results for all encounters."""
    rng = np.random.default_rng(seed)

    patient_lookup = patients.set_index("patient_id")
    records = []
    lab_counter = 1

    test_names = list(LABORATORY_REFERENCE.keys())

    for encounter_row in encounters.itertuples(index=False):
        encounter = pd.Series(encounter_row._asdict())
        patient = patient_lookup.loc[encounter["patient_id"]]

        for test_name in test_names:
            value = generate_lab_value(
                test_name=test_name,
                patient=patient,
                encounter=encounter,
                rng=rng,
            )

            reference = LABORATORY_REFERENCE[test_name]

            records.append(
                {
                    "lab_id": f"LAB-{lab_counter:08d}",
                    "encounter_id": str(encounter["encounter_id"]),
                    "patient_id": str(encounter["patient_id"]),
                    "mrn": str(encounter["mrn"]),
                    "test_name": test_name,
                    "test_category": reference["category"],
                    "result_value": value,
                    "unit": reference["unit"],
                    "reference_low": reference["low"],
                    "reference_high": reference["high"],
                    "result_flag": interpret_result(test_name, value),
                    "result_date": str(encounter["encounter_date"]),
                }
            )

            lab_counter += 1

    return pd.DataFrame(records)


def validate_output(labs: pd.DataFrame, encounters: pd.DataFrame) -> None:
    """Validate generated lab output."""
    if labs.empty:
        raise ValueError("Generated laboratory dataset is empty.")

    if labs["lab_id"].duplicated().any():
        raise ValueError("Duplicate lab_id values detected.")

    invalid_encounters = set(labs["encounter_id"]) - set(encounters["encounter_id"])
    if invalid_encounters:
        raise ValueError("Laboratory records contain unknown encounter_id values.")


def save_labs(labs: pd.DataFrame, output_path: Path = OUTPUT_PATH) -> None:
    """Save lab results dataset."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    labs.to_csv(output_path, index=False)


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate ClariPulse synthetic laboratory results dataset."
    )

    parser.add_argument("--seed", type=int, default=42)

    args = parser.parse_args()

    patients = load_csv(PATIENTS_PATH, "Patients")
    encounters = load_csv(ENCOUNTERS_PATH, "Encounters")

    labs = generate_laboratory_results(
        patients=patients,
        encounters=encounters,
        seed=args.seed,
    )

    validate_output(labs, encounters)
    save_labs(labs)

    print(f"Generated {len(labs):,} laboratory results")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()