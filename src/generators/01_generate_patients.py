"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Platform
Module: src.generators.01_generate_patients
Purpose:
    Generate a clinically plausible synthetic patient cohort for ClariPulse™.

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
OUTPUT_PATH = PROJECT_ROOT / "data" / "synthetic" / "01_patients.csv"


ETHNICITIES = [
    "Middle Eastern",
    "African",
    "South Asian",
    "European",
    "East Asian",
    "Other",
]

ADMISSION_TYPES = [
    "Emergency",
    "Elective",
    "Urgent",
    "Observation",
]


def sigmoid(x: np.ndarray) -> np.ndarray:
    """Convert linear risk score into probability."""
    return 1 / (1 + np.exp(-x))


def assign_risk_category(probability: float) -> str:
    """Convert probability into business-friendly risk category."""
    if probability < 0.25:
        return "Low"
    if probability < 0.50:
        return "Moderate"
    if probability < 0.75:
        return "High"
    return "Critical"


def generate_patients(
    n_patients: int = 100_000,
    seed: int = 42,
) -> pd.DataFrame:
    """Generate synthetic patient-level clinical data."""

    rng = np.random.default_rng(seed)

    patient_number = np.arange(1, n_patients + 1)

    age = np.clip(rng.normal(56, 19, n_patients).round(), 18, 95).astype(int)

    sex = rng.choice(
        ["Male", "Female"],
        size=n_patients,
        p=[0.49, 0.51],
    )

    ethnicity = rng.choice(
        ETHNICITIES,
        size=n_patients,
        p=[0.30, 0.20, 0.18, 0.16, 0.10, 0.06],
    )

    height_cm = np.where(
        sex == "Male",
        rng.normal(173, 8, n_patients),
        rng.normal(161, 7, n_patients),
    )

    bmi = np.clip(rng.normal(28.5, 6.2, n_patients), 16, 55)

    weight_kg = bmi * ((height_cm / 100) ** 2)

    smoker = rng.binomial(1, 0.22, n_patients)

    diabetes_prob = sigmoid(-3.0 + 0.035 * age + 0.055 * (bmi - 25))
    diabetes = rng.binomial(1, diabetes_prob)

    hypertension_prob = sigmoid(-4.2 + 0.055 * age + 0.045 * (bmi - 25))
    hypertension = rng.binomial(1, hypertension_prob)

    ckd_prob = sigmoid(-5.0 + 0.045 * age + 0.7 * diabetes + 0.5 * hypertension)
    ckd = rng.binomial(1, ckd_prob)

    copd_prob = sigmoid(-4.6 + 0.035 * age + 1.1 * smoker)
    copd = rng.binomial(1, copd_prob)

    heart_failure_prob = sigmoid(
        -5.2 + 0.045 * age + 0.55 * hypertension + 0.7 * ckd
    )
    heart_failure = rng.binomial(1, heart_failure_prob)

    cancer_prob = sigmoid(-5.0 + 0.035 * age)
    cancer = rng.binomial(1, cancer_prob)

    admission_type = rng.choice(
        ADMISSION_TYPES,
        size=n_patients,
        p=[0.46, 0.23, 0.21, 0.10],
    )

    emergency_flag = (admission_type == "Emergency").astype(int)

    sepsis_linear = (
        -4.1
        + 0.025 * age
        + 0.75 * ckd
        + 0.50 * diabetes
        + 0.55 * copd
        + 0.80 * emergency_flag
    )
    sepsis_probability = sigmoid(sepsis_linear)
    sepsis = rng.binomial(1, sepsis_probability)

    icu_linear = (
        -4.3
        + 0.028 * age
        + 0.70 * heart_failure
        + 0.65 * ckd
        + 1.10 * sepsis
        + 0.75 * emergency_flag
    )
    icu_probability = sigmoid(icu_linear)
    icu = rng.binomial(1, icu_probability)

    los = np.clip(
        rng.normal(3.5, 1.8, n_patients)
        + 2.4 * icu
        + 2.1 * sepsis
        + 1.2 * heart_failure
        + 0.8 * ckd,
        1,
        45,
    ).round(1)

    mortality_linear = (
        -5.5
        + 0.045 * age
        + 0.90 * icu
        + 1.15 * sepsis
        + 0.65 * ckd
        + 0.60 * heart_failure
        + 0.40 * cancer
    )
    mortality_probability = sigmoid(mortality_linear)
    mortality = rng.binomial(1, mortality_probability)

    readmission_linear = (
        -3.4
        + 0.018 * age
        + 0.55 * diabetes
        + 0.65 * ckd
        + 0.80 * heart_failure
        + 0.35 * copd
        + 0.025 * los
    )
    readmission_probability = sigmoid(readmission_linear)
    readmission = rng.binomial(1, readmission_probability)

    composite_risk_probability = (
        0.45 * mortality_probability
        + 0.30 * readmission_probability
        + 0.25 * sepsis_probability
    )

    risk_category = [
        assign_risk_category(prob) for prob in composite_risk_probability
    ]

    patients = pd.DataFrame(
        {
            "patient_id": [f"PAT-{i:06d}" for i in patient_number],
            "mrn": [f"MRN-{i:08d}" for i in patient_number],
            "age": age,
            "sex": sex,
            "ethnicity": ethnicity,
            "height_cm": np.round(height_cm, 1),
            "weight_kg": np.round(weight_kg, 1),
            "bmi": np.round(bmi, 1),
            "smoker": smoker,
            "diabetes": diabetes,
            "hypertension": hypertension,
            "ckd": ckd,
            "copd": copd,
            "heart_failure": heart_failure,
            "cancer": cancer,
            "admission_type": admission_type,
            "icu": icu,
            "length_of_stay_days": los,
            "mortality": mortality,
            "readmission": readmission,
            "sepsis": sepsis,
            "mortality_probability": np.round(mortality_probability, 4),
            "readmission_probability": np.round(readmission_probability, 4),
            "sepsis_probability": np.round(sepsis_probability, 4),
            "composite_risk_probability": np.round(composite_risk_probability, 4),
            "risk_category": risk_category,
        }
    )

    return patients


def save_patients(patients: pd.DataFrame, output_path: Path = OUTPUT_PATH) -> None:
    """Save patient dataset to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    patients.to_csv(output_path, index=False)


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate synthetic ClariPulse patient dataset."
    )

    parser.add_argument(
        "--patients",
        type=int,
        default=100_000,
        help="Number of synthetic patients to generate.",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility.",
    )

    args = parser.parse_args()

    patients = generate_patients(
        n_patients=args.patients,
        seed=args.seed,
    )

    save_patients(patients)

    print(f"Generated {len(patients):,} patients")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()