"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: src.reference.vital_reference

Purpose:
    Master vital signs reference ranges used throughout the
    ClariPulse™ synthetic data generation pipeline.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations


VITAL_REFERENCE: dict[str, dict[str, str | float]] = {

    "Heart Rate": {
        "unit": "bpm",
        "low": 60,
        "high": 100,
        "category": "Cardiovascular",
    },

    "Respiratory Rate": {
        "unit": "breaths/min",
        "low": 12,
        "high": 20,
        "category": "Respiratory",
    },

    "Temperature": {
        "unit": "°C",
        "low": 36.1,
        "high": 37.5,
        "category": "General",
    },

    "SpO2": {
        "unit": "%",
        "low": 95,
        "high": 100,
        "category": "Respiratory",
    },

    "Systolic Blood Pressure": {
        "unit": "mmHg",
        "low": 90,
        "high": 120,
        "category": "Cardiovascular",
    },

    "Diastolic Blood Pressure": {
        "unit": "mmHg",
        "low": 60,
        "high": 80,
        "category": "Cardiovascular",
    },

    "Mean Arterial Pressure": {
        "unit": "mmHg",
        "low": 70,
        "high": 100,
        "category": "Cardiovascular",
    },

    "BMI": {
        "unit": "kg/m²",
        "low": 18.5,
        "high": 24.9,
        "category": "Anthropometric",
    },

}