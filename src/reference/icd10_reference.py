
"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: src.reference.icd10_reference

Purpose:
    Master ICD-10 reference library used throughout the ClariPulse™
    synthetic data generation and Clinical AI pipelines.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations


ICD10_REFERENCE: dict[str, dict[str, str]] = {
    "hypertension": {
        "code": "I10",
        "name": "Essential (Primary) Hypertension",
        "category": "Cardiovascular",
    },
    "diabetes": {
        "code": "E11.9",
        "name": "Type 2 Diabetes Mellitus Without Complications",
        "category": "Endocrine",
    },
    "ckd": {
        "code": "N18.3",
        "name": "Chronic Kidney Disease Stage 3",
        "category": "Renal",
    },
    "copd": {
        "code": "J44.9",
        "name": "Chronic Obstructive Pulmonary Disease",
        "category": "Respiratory",
    },
    "heart_failure": {
        "code": "I50.9",
        "name": "Heart Failure",
        "category": "Cardiovascular",
    },
    "sepsis": {
        "code": "A41.9",
        "name": "Sepsis, Unspecified Organism",
        "category": "Infectious Disease",
    },
    "cancer": {
        "code": "C34.9",
        "name": "Malignant Neoplasm of Lung",
        "category": "Oncology",
    },
    "obesity": {
        "code": "E66.9",
        "name": "Obesity",
        "category": "Metabolic",
    },
    "pneumonia": {
        "code": "J18.9",
        "name": "Pneumonia",
        "category": "Respiratory",
    },
    "myocardial_infarction": {
        "code": "I21.9",
        "name": "Acute Myocardial Infarction",
        "category": "Cardiology",
    },
    "stroke": {
        "code": "I63.9",
        "name": "Cerebral Infarction",
        "category": "Neurology",
    },
    "uti": {
        "code": "N39.0",
        "name": "Urinary Tract Infection",
        "category": "Infectious Disease",
    },
    "gerd": {
        "code": "K21.9",
        "name": "Gastro-Oesophageal Reflux Disease",
        "category": "Gastroenterology",
    },
    "osteoarthritis": {
        "code": "M17.9",
        "name": "Osteoarthritis",
        "category": "Musculoskeletal",
    },
    "depression": {
        "code": "F32.9",
        "name": "Major Depressive Disorder",
        "category": "Mental Health",
    },
    "epilepsy": {
        "code": "G40.9",
        "name": "Epilepsy",
        "category": "Neurology",
    },
    "chest_pain": {
        "code": "R07.9",
        "name": "Chest Pain",
        "category": "Symptom",
    },
    "dyspnoea": {
        "code": "R06.0",
        "name": "Dyspnoea",
        "category": "Symptom",
    },
    "viral_infection": {
        "code": "B34.9",
        "name": "Viral Infection",
        "category": "Infectious Disease",
    },
    "long_term_insulin": {
        "code": "Z79.4",
        "name": "Long-Term Insulin Therapy",
        "category": "Medication History",
    },
}