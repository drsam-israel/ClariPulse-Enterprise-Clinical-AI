"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: src.generators.03_generate_diagnoses
Purpose:
    Generate clinically coherent ICD-10 diagnosis records linked to
    patients and encounters.

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

from src.reference.icd10_reference import ICD10_REFERENCE


PATIENTS_PATH = PROJECT_ROOT / "data" / "synthetic" / "01_patients.csv"
ENCOUNTERS_PATH = PROJECT_ROOT / "data" / "synthetic" / "02_encounters.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "synthetic" / "03_diagnoses.csv"


CONDITION_TO_DIAGNOSIS_KEY = {
    "hypertension": "hypertension",
    "diabetes": "diabetes",
    "ckd": "ckd",
    "copd": "copd",
    "heart_failure": "heart_failure",
    "sepsis": "sepsis",
    "cancer": "cancer",
}


FALLBACK_PRIMARY_KEYS = [
    "chest_pain",
    "dyspnoea",
    "pneumonia",
    "uti",
    "viral_infection",
    "gerd",
    "osteoarthritis",
]


FALLBACK_SECONDARY_KEYS = [
    "obesity",
    "depression",
    "epilepsy",
    "long_term_insulin",
    "gerd",
    "osteoarthritis",
]


def load_csv(path: Path, label: str) -> pd.DataFrame:
    """Load a required CSV file."""
    if not path.exists():
        raise FileNotFoundError(f"{label} file not found: {path}")

    return pd.read_csv(path)


def get_reference_record(key: str) -> dict[str, str]:
    """Return ICD-10 reference entry by semantic key."""
    if key not in ICD10_REFERENCE:
        raise KeyError(f"ICD-10 reference key not found: {key}")

    return ICD10_REFERENCE[key]


def get_patient_condition_keys(patient_row: pd.Series) -> list[str]:
    """Return diagnosis keys based on patient comorbidity flags."""
    keys: list[str] = []

    for patient_column, diagnosis_key in CONDITION_TO_DIAGNOSIS_KEY.items():
        if int(patient_row.get(patient_column, 0)) == 1:
            keys.append(diagnosis_key)

    if float(patient_row.get("bmi", 0)) >= 30:
        keys.append("obesity")

    return list(dict.fromkeys(keys))


def choose_primary_key(
    condition_keys: list[str],
    encounter_row: pd.Series,
    rng: np.random.Generator,
) -> str:
    """Choose a clinically plausible primary diagnosis."""

    if int(encounter_row.get("sepsis", 0)) == 1:
        return "sepsis"

    if int(encounter_row.get("mortality", 0)) == 1 and condition_keys:
        high_priority = [
            key
            for key in condition_keys
            if key in {"heart_failure", "ckd", "cancer", "copd"}
        ]
        if high_priority:
            return str(rng.choice(high_priority))

    if condition_keys:
        return str(rng.choice(condition_keys))

    return str(rng.choice(FALLBACK_PRIMARY_KEYS))


def choose_secondary_keys(
    primary_key: str,
    condition_keys: list[str],
    rng: np.random.Generator,
) -> list[str]:
    """Choose 0 to 3 secondary diagnoses."""

    candidate_keys = [
        key for key in condition_keys if key != primary_key
    ]

    candidate_keys.extend(
        key for key in FALLBACK_SECONDARY_KEYS if key not in candidate_keys
    )

    candidate_keys = [
        key for key in dict.fromkeys(candidate_keys) if key != primary_key
    ]

    number_secondary = int(rng.choice([0, 1, 2, 3], p=[0.10, 0.25, 0.40, 0.25]))

    if not candidate_keys or number_secondary == 0:
        return []

    number_secondary = min(number_secondary, len(candidate_keys))

    return list(rng.choice(candidate_keys, size=number_secondary, replace=False))


def build_diagnosis_record(
    *,
    diagnosis_id: str,
    encounter_row: pd.Series,
    diagnosis_type: str,
    diagnosis_key: str,
    present_on_admission: str,
) -> dict[str, str]:
    """Build one diagnosis record."""
    reference = get_reference_record(diagnosis_key)

    return {
        "diagnosis_id": diagnosis_id,
        "encounter_id": str(encounter_row["encounter_id"]),
        "patient_id": str(encounter_row["patient_id"]),
        "mrn": str(encounter_row["mrn"]),
        "diagnosis_type": diagnosis_type,
        "icd10_code": reference["code"],
        "diagnosis_name": reference["name"],
        "diagnosis_category": reference["category"],
        "present_on_admission": present_on_admission,
        "diagnosis_date": str(encounter_row["encounter_date"]),
    }


def validate_inputs(patients: pd.DataFrame, encounters: pd.DataFrame) -> None:
    """Validate required input columns."""
    required_patient_columns = {
        "patient_id",
        "mrn",
        "hypertension",
        "diabetes",
        "ckd",
        "copd",
        "heart_failure",
        "sepsis",
        "cancer",
        "bmi",
    }

    required_encounter_columns = {
        "encounter_id",
        "patient_id",
        "mrn",
        "encounter_date",
        "sepsis",
        "mortality",
    }

    missing_patients = required_patient_columns - set(patients.columns)
    missing_encounters = required_encounter_columns - set(encounters.columns)

    if missing_patients:
        raise ValueError(f"Missing patient columns: {sorted(missing_patients)}")

    if missing_encounters:
        raise ValueError(f"Missing encounter columns: {sorted(missing_encounters)}")


def validate_output(diagnoses: pd.DataFrame, encounters: pd.DataFrame) -> None:
    """Validate generated diagnoses."""
    if diagnoses.empty:
        raise ValueError("Generated diagnoses dataset is empty.")

    if diagnoses["diagnosis_id"].duplicated().any():
        raise ValueError("Duplicate diagnosis_id values detected.")

    encounter_ids = set(encounters["encounter_id"])
    diagnosis_encounter_ids = set(diagnoses["encounter_id"])

    missing = diagnosis_encounter_ids - encounter_ids

    if missing:
        raise ValueError("Diagnoses contain encounter IDs not present in encounters.")

    primary_counts = diagnoses[diagnoses["diagnosis_type"] == "Primary"].groupby(
        "encounter_id"
    ).size()

    if not (primary_counts == 1).all():
        raise ValueError("Every encounter must have exactly one primary diagnosis.")


def generate_diagnoses(
    patients: pd.DataFrame,
    encounters: pd.DataFrame,
    seed: int = 42,
) -> pd.DataFrame:
    """Generate clinically coherent diagnosis records."""
    rng = np.random.default_rng(seed)

    validate_inputs(patients, encounters)

    patient_lookup = patients.set_index("patient_id")

    records: list[dict[str, str]] = []
    diagnosis_counter = 1

    for encounter_row in encounters.itertuples(index=False):
        encounter = pd.Series(encounter_row._asdict())

        patient = patient_lookup.loc[encounter["patient_id"]]

        condition_keys = get_patient_condition_keys(patient)

        primary_key = choose_primary_key(
            condition_keys=condition_keys,
            encounter_row=encounter,
            rng=rng,
        )

        records.append(
            build_diagnosis_record(
                diagnosis_id=f"DIAG-{diagnosis_counter:08d}",
                encounter_row=encounter,
                diagnosis_type="Primary",
                diagnosis_key=primary_key,
                present_on_admission="Yes",
            )
        )
        diagnosis_counter += 1

        secondary_keys = choose_secondary_keys(
            primary_key=primary_key,
            condition_keys=condition_keys,
            rng=rng,
        )

        for secondary_key in secondary_keys:
            records.append(
                build_diagnosis_record(
                    diagnosis_id=f"DIAG-{diagnosis_counter:08d}",
                    encounter_row=encounter,
                    diagnosis_type="Secondary",
                    diagnosis_key=secondary_key,
                    present_on_admission=str(rng.choice(["Yes", "No"], p=[0.82, 0.18])),
                )
            )
            diagnosis_counter += 1

    diagnoses = pd.DataFrame(records)

    validate_output(diagnoses, encounters)

    return diagnoses


def save_diagnoses(diagnoses: pd.DataFrame, output_path: Path = OUTPUT_PATH) -> None:
    """Save diagnoses dataset."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    diagnoses.to_csv(output_path, index=False)


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate ClariPulse synthetic diagnoses dataset."
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility.",
    )

    args = parser.parse_args()

    patients = load_csv(PATIENTS_PATH, "Patients")
    encounters = load_csv(ENCOUNTERS_PATH, "Encounters")

    diagnoses = generate_diagnoses(
        patients=patients,
        encounters=encounters,
        seed=args.seed,
    )

    save_diagnoses(diagnoses)

    print(f"Generated {len(diagnoses):,} diagnoses")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()