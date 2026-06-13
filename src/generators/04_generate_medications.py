
"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: src.generators.04_generate_medications

Purpose:
    Generate clinically coherent medication records linked to
    diagnoses, encounters, and patients.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd


# =============================================================================
# PROJECT PATHS
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.reference.medication_reference import (  # noqa: E402
    DIAGNOSIS_TO_MEDICATION,
    MEDICATION_REFERENCE,
)


PATIENTS_PATH = (
    PROJECT_ROOT
    / "data"
    / "synthetic"
    / "01_patients.csv"
)

ENCOUNTERS_PATH = (
    PROJECT_ROOT
    / "data"
    / "synthetic"
    / "02_encounters.csv"
)

DIAGNOSES_PATH = (
    PROJECT_ROOT
    / "data"
    / "synthetic"
    / "03_diagnoses.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "synthetic"
    / "04_medications.csv"
)


# =============================================================================
# DATA LOADERS
# =============================================================================


def load_csv(path: Path, label: str) -> pd.DataFrame:
    """
    Load required CSV dataset.
    """

    if not path.exists():
        raise FileNotFoundError(
            f"{label} file not found:\n{path}"
        )

    return pd.read_csv(path)


def load_patients() -> pd.DataFrame:
    """
    Load patients dataset.
    """

    return load_csv(
        PATIENTS_PATH,
        "Patients",
    )


def load_encounters() -> pd.DataFrame:
    """
    Load encounters dataset.
    """

    return load_csv(
        ENCOUNTERS_PATH,
        "Encounters",
    )


def load_diagnoses() -> pd.DataFrame:
    """
    Load diagnoses dataset.
    """

    return load_csv(
        DIAGNOSES_PATH,
        "Diagnoses",
    )


# =============================================================================
# LOOKUP HELPERS
# =============================================================================


def get_medications_for_icd(
    icd10_code: str,
) -> list[str]:
    """
    Return medication names mapped
    to an ICD-10 diagnosis.
    """

    return DIAGNOSIS_TO_MEDICATION.get(
        icd10_code,
        [],
    )


def get_medication_metadata(
    medication_name: str,
) -> dict:
    """
    Return metadata for a medication.
    """

    if medication_name not in MEDICATION_REFERENCE:

        raise KeyError(
            f"Medication not found: {medication_name}"
        )

    return MEDICATION_REFERENCE[
        medication_name
    ]


# =============================================================================
# DATE HELPERS
# =============================================================================


def calculate_duration(
    rng: np.random.Generator,
) -> int:
    """
    Random realistic medication duration.
    """

    return int(

        rng.choice(

            [5, 7, 10, 14, 30, 60, 90],

            p=[
                0.12,
                0.18,
                0.10,
                0.15,
                0.25,
                0.10,
                0.10,
            ],

        )

    )

# =============================================================================
# MEDICATION RECORD BUILDER
# =============================================================================


def build_medication_record(
    *,
    medication_id: str,
    diagnosis_row: pd.Series,
    medication_name: str,
    start_date: str,
    duration_days: int,
    active: str,
) -> dict[str, str | int]:
    """
    Build one medication record.
    """

    metadata = get_medication_metadata(
        medication_name
    )

    start_timestamp = pd.to_datetime(
        start_date
    )

    end_date = (
        start_timestamp
        + pd.to_timedelta(duration_days, unit="D")
    ).strftime("%Y-%m-%d")

    return {
        "medication_id": medication_id,
        "encounter_id": str(diagnosis_row["encounter_id"]),
        "patient_id": str(diagnosis_row["patient_id"]),
        "mrn": str(diagnosis_row["mrn"]),
        "medication_name": medication_name,
        "drug_class": metadata["drug_class"],
        "dose": metadata.get("default_dose", "Standard Dose"),
        "route": metadata["route"],
        "frequency": metadata["frequency"],
        "start_date": start_date,
        "end_date": end_date,
        "duration_days": duration_days,
        "active": active,
    }


def choose_medications(
    medication_names: list[str],
    rng: np.random.Generator,
) -> list[str]:
    """
    Choose one or more medications from a mapped list.
    """

    if not medication_names:
        return []

    if len(medication_names) == 1:
        return medication_names

    if len(medication_names) == 2:
        use_both = rng.random() < 0.45

        if use_both:
            return medication_names

        return [str(rng.choice(medication_names))]

    max_count = min(3, len(medication_names))

    count = int(
        rng.integers(
            1,
            max_count + 1,
        )
    )

    return list(
        rng.choice(
            medication_names,
            size=count,
            replace=False,
        )
    )
# =============================================================================
# GENERATION ENGINE
# =============================================================================


def generate_medications(
    diagnoses: pd.DataFrame,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate clinically coherent medications from diagnoses.
    """

    rng = np.random.default_rng(seed)

    records: list[dict[str, str | int]] = []
    medication_counter = 1

    for diagnosis_row in diagnoses.itertuples(index=False):

        diagnosis = pd.Series(
            diagnosis_row._asdict()
        )

        icd10_code = str(
            diagnosis["icd10_code"]
        )

        mapped_medications = get_medications_for_icd(
            icd10_code
        )

        selected_medications = choose_medications(
            mapped_medications,
            rng,
        )

        if not selected_medications:
            continue

        for medication_name in selected_medications:

            duration_days = calculate_duration(
                rng
            )

            active = str(
                rng.choice(
                    ["Yes", "No"],
                    p=[0.72, 0.28],
                )
            )

            record = build_medication_record(
                medication_id=f"MED-{medication_counter:08d}",
                diagnosis_row=diagnosis,
                medication_name=medication_name,
                start_date=str(diagnosis["diagnosis_date"]),
                duration_days=duration_days,
                active=active,
            )

            records.append(record)

            medication_counter += 1

    medications = pd.DataFrame(records)

    return medications


# =============================================================================
# VALIDATION
# =============================================================================


def validate_inputs(
    diagnoses: pd.DataFrame,
) -> None:
    """
    Validate required diagnosis columns.
    """

    required_columns = {
        "diagnosis_id",
        "encounter_id",
        "patient_id",
        "mrn",
        "icd10_code",
        "diagnosis_date",
    }

    missing_columns = required_columns - set(
        diagnoses.columns
    )

    if missing_columns:
        raise ValueError(
            f"Missing diagnosis columns: {sorted(missing_columns)}"
        )


def validate_output(
    medications: pd.DataFrame,
    diagnoses: pd.DataFrame,
) -> None:
    """
    Validate generated medication output.
    """

    if medications.empty:
        raise ValueError(
            "Generated medications dataset is empty."
        )

    if medications["medication_id"].duplicated().any():
        raise ValueError(
            "Duplicate medication_id values detected."
        )

    diagnosis_patient_ids = set(
        diagnoses["patient_id"]
    )

    medication_patient_ids = set(
        medications["patient_id"]
    )

    missing_patients = (
        medication_patient_ids
        - diagnosis_patient_ids
    )

    if missing_patients:
        raise ValueError(
            "Medication records contain unknown patient_id values."
        )

    valid_medications = set(
        MEDICATION_REFERENCE.keys()
    )

    generated_medications = set(
        medications["medication_name"]
    )

    invalid_medications = (
        generated_medications
        - valid_medications
    )

    if invalid_medications:
        raise ValueError(
            f"Invalid medication names detected: {sorted(invalid_medications)}"
        )
    
    # =============================================================================
# SAVE OUTPUT
# =============================================================================


def save_medications(
    medications: pd.DataFrame,
    output_path: Path = OUTPUT_PATH,
) -> None:
    """
    Save generated medications dataset.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    medications.to_csv(
        output_path,
        index=False,
    )


# =============================================================================
# MAIN
# =============================================================================


def main() -> None:
    """
    CLI entry point.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Generate ClariPulse synthetic medications dataset."
        )
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility.",
    )

    args = parser.parse_args()

    print("\nLoading datasets...")

    # These are loaded to ensure referential integrity and future extensibility.
    _patients = load_patients()
    _encounters = load_encounters()
    diagnoses = load_diagnoses()

    print(
        f"Loaded {len(_patients):,} patients"
    )

    print(
        f"Loaded {len(_encounters):,} encounters"
    )

    print(
        f"Loaded {len(diagnoses):,} diagnoses"
    )

    validate_inputs(
        diagnoses,
    )

    print("\nGenerating medications...")

    medications = generate_medications(
        diagnoses=diagnoses,
        seed=args.seed,
    )

    validate_output(
        medications=medications,
        diagnoses=diagnoses,
    )

    save_medications(
        medications,
    )

    print(
        f"\nGenerated {len(medications):,} medications"
    )

    print(
        f"Saved to:\n{OUTPUT_PATH}"
    )


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
