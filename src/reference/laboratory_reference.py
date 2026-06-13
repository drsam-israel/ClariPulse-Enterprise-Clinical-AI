"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: src.reference.laboratory_reference

Purpose:
    Master laboratory test reference ranges used across the ClariPulse™
    synthetic data generation pipeline.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations


LABORATORY_REFERENCE: dict[str, dict[str, str | float]] = {
    "Hemoglobin": {
        "unit": "g/dL",
        "low": 12.0,
        "high": 17.5,
        "category": "Hematology",
    },
    "WBC": {
        "unit": "10^9/L",
        "low": 4.0,
        "high": 11.0,
        "category": "Hematology",
    },
    "Platelets": {
        "unit": "10^9/L",
        "low": 150,
        "high": 450,
        "category": "Hematology",
    },
    "Creatinine": {
        "unit": "mg/dL",
        "low": 0.6,
        "high": 1.3,
        "category": "Renal",
    },
    "Sodium": {
        "unit": "mmol/L",
        "low": 135,
        "high": 145,
        "category": "Chemistry",
    },
    "Potassium": {
        "unit": "mmol/L",
        "low": 3.5,
        "high": 5.1,
        "category": "Chemistry",
    },
    "Glucose": {
        "unit": "mg/dL",
        "low": 70,
        "high": 140,
        "category": "Metabolic",
    },
    "HbA1c": {
        "unit": "%",
        "low": 4.0,
        "high": 5.6,
        "category": "Endocrine",
    },
    "Lactate": {
        "unit": "mmol/L",
        "low": 0.5,
        "high": 2.2,
        "category": "Critical Care",
    },
    "CRP": {
        "unit": "mg/L",
        "low": 0,
        "high": 10,
        "category": "Inflammation",
    },
}