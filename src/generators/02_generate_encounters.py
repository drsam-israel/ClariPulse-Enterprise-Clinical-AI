"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Platform
Module: src.generators.02_generate_encounters
Purpose:
    Generate synthetic healthcare encounters linked to 01_patients.csv.

Author: Samuel Israel, MD
License: MIT
===============================================================================
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PATIENTS_PATH = PROJECT_ROOT / "data" / "synthetic" / "01_patients.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "synthetic" / "02_encounters.csv"


DEPARTMENTS = [
    "Emergency Department",
    "Internal Medicine",
    "Cardiology",
    "Endocrinology",
    "Nephrology",
    "Pulmonology",
    "General Surgery",
    "Intensive Care Unit",
]

FACILITIES = [
    "ClariPulse Central Hospital",
    "ClariPulse North Medical Center",
    "ClariPulse South Specialist Hospital",
    "ClariPulse Digital Health Hub",
]

ADMISSION_SOURCES = [
    "Self Referral",
    "Physician Referral",
    "Ambulance",
    "Transfer",
    "Outpatient Clinic",
]

DISCHARGE_DISPOSITIONS = [
    "Home",
    "Home with Follow-up",
    "Rehabilitation",
    "Transfer to Facility",
    "Deceased",
]


def load_patients(path: Path = PATIENTS_PATH) -> pd.DataFrame:
    """Load generated patients dataset."""
    if not path.exists():
        raise FileNotFoundError(
            f"Patients file not found: {path}. Run 01_generate_patients.py first."
        )

    return pd.read_csv(path)


def _select_department(admission_type: str, icu: int, sepsis: int) -> str:
    """Assign department using clinical logic."""
    if icu == 1:
        return "Intensive Care Unit"

    if sepsis == 1 or admission_type == "Emergency":
        return "Emergency Department"

    if admission_type == "Elective":
        return np.random.choice(["Cardiology", "General Surgery", "Endocrinology"])

    return np.random.choice(DEPARTMENTS)


def generate_encounters(
    patients: pd.DataFrame,
    seed: int = 42,
) -> pd.DataFrame:
    """Generate one encounter per patient for the current MVP."""
    rng = np.random.default_rng(seed)

    n = len(patients)

    encounter_dates = pd.to_datetime("2025-01-01") + pd.to_timedelta(
        rng.integers(0, 365, size=n),
        unit="D",
    )

    discharge_dates = encounter_dates + pd.to_timedelta(
        patients["length_of_stay_days"].round().astype(int).clip(lower=1),
        unit="D",
    )

    departments = [
        _select_department(row.admission_type, row.icu, row.sepsis)
        for row in patients.itertuples(index=False)
    ]

    facility = rng.choice(
        FACILITIES,
        size=n,
        p=[0.42, 0.24, 0.22, 0.12],
    )

    admission_source = rng.choice(
        ADMISSION_SOURCES,
        size=n,
        p=[0.24, 0.28, 0.22, 0.16, 0.10],
    )

    discharge_disposition = np.where(
        patients["mortality"] == 1,
        "Deceased",
        rng.choice(
            DISCHARGE_DISPOSITIONS[:-1],
            size=n,
            p=[0.50, 0.28, 0.12, 0.10],
        ),
    )

    base_cost = rng.normal(3200, 900, size=n)

    encounter_cost = (
        base_cost
        + patients["length_of_stay_days"] * 950
        + patients["icu"] * 8500
        + patients["sepsis"] * 5200
        + patients["heart_failure"] * 1800
        + patients["ckd"] * 1600
    )

    encounter_cost = np.clip(encounter_cost, 900, 95_000).round(2)

    encounters = pd.DataFrame(
        {
            "encounter_id": [f"ENC-{i:08d}" for i in range(1, n + 1)],
            "patient_id": patients["patient_id"],
            "mrn": patients["mrn"],
            "encounter_date": pd.Series(encounter_dates).dt.strftime("%Y-%m-%d"),
            "discharge_date": pd.Series(discharge_dates).dt.strftime("%Y-%m-%d"),
            "admission_type": patients["admission_type"],
            "department": departments,
            "facility": facility,
            "admission_source": admission_source,
            "discharge_disposition": discharge_disposition,
            "length_of_stay_days": patients["length_of_stay_days"],
            "icu": patients["icu"],
            "mortality": patients["mortality"],
            "readmission": patients["readmission"],
            "sepsis": patients["sepsis"],
            "encounter_cost_usd": encounter_cost,
            "encounter_status": np.where(
                patients["mortality"] == 1,
                "Closed",
                "Completed",
            ),
        }
    )

    return encounters


def save_encounters(
    encounters: pd.DataFrame,
    output_path: Path = OUTPUT_PATH,
) -> None:
    """Save encounters dataset."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    encounters.to_csv(output_path, index=False)


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate ClariPulse synthetic encounters dataset."
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility.",
    )

    args = parser.parse_args()

    patients = load_patients()
    encounters = generate_encounters(patients, seed=args.seed)
    save_encounters(encounters)

    print(f"Generated {len(encounters):,} encounters")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()