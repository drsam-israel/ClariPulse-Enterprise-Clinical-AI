"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product

Patient Explorer - V2 Real-World Diabetes Readmission Prediction

Author:
Samuel Israel, MD
===============================================================================
"""

from __future__ import annotations

import streamlit as st

from components.hero import render_hero

from app.v2.services.diabetes_prediction_service import (
    predict_diabetes_readmission,
)
from app.v2.ml.explainability import explain_v2_patient


render_hero(
    title="Patient Explorer",
    subtitle="Real-World Diabetes Readmission Risk Prediction",
    description=(
        "Enter patient characteristics to generate AI-powered "
        "30-day hospital readmission risk predictions."
    ),
)

st.subheader("Patient Information")

col1, col2 = st.columns(2)

with col1:
    time_in_hospital = st.number_input(
        "Time in Hospital",
        min_value=1,
        max_value=14,
        value=5,
    )

    num_lab_procedures = st.number_input(
        "Number of Lab Procedures",
        min_value=0,
        max_value=150,
        value=45,
    )

    num_procedures = st.number_input(
        "Number of Procedures",
        min_value=0,
        max_value=10,
        value=1,
    )

    num_medications = st.number_input(
        "Number of Medications",
        min_value=1,
        max_value=100,
        value=18,
    )

    number_outpatient = st.number_input(
        "Prior Outpatient Visits",
        min_value=0,
        max_value=50,
        value=0,
    )

with col2:
    number_emergency = st.number_input(
        "Prior Emergency Visits",
        min_value=0,
        max_value=50,
        value=1,
    )

    number_inpatient = st.number_input(
        "Prior Inpatient Visits",
        min_value=0,
        max_value=50,
        value=1,
    )

    number_diagnoses = st.number_input(
        "Number of Diagnoses",
        min_value=1,
        max_value=20,
        value=8,
    )

    diabetesMed_Yes = st.selectbox(
        "Diabetes Medication Prescribed",
        [0, 1],
        index=1,
    )

    change_Ch = st.selectbox(
        "Medication Changed During Encounter",
        [0, 1],
        index=1,
    )


if st.button("🔮 Predict 30-Day Readmission Risk", use_container_width=True):
    patient = {
        "time_in_hospital": time_in_hospital,
        "num_lab_procedures": num_lab_procedures,
        "num_procedures": num_procedures,
        "num_medications": num_medications,
        "number_outpatient": number_outpatient,
        "number_emergency": number_emergency,
        "number_inpatient": number_inpatient,
        "number_diagnoses": number_diagnoses,
        "diabetesMed_Yes": diabetesMed_Yes,
        "change_Ch": change_Ch,
    }

    result = predict_diabetes_readmission(patient)

    risk = result["risk_percent"]

    if risk < 10:
        category = "🟢 Low"
    elif risk < 20:
        category = "🟡 Moderate"
    elif risk < 35:
        category = "🟠 High"
    else:
        category = "🔴 Critical"

    st.success("Prediction completed successfully.")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "30-Day Readmission Probability",
        f"{risk:.1f}%",
    )

    c2.metric(
        "Risk Category",
        category,
    )

    c3.metric(
        "Use Case",
        "30-Day Readmission",
    )

    with st.expander("View Raw Prediction Output"):
        st.json(result)

    st.divider()

    st.subheader("Top AI Risk Drivers")

    explanation = explain_v2_patient(patient)

    if explanation.empty:
        st.warning(
            "V2 SHAP explainability output not found. "
            "Run `python -m app.v2.ml.explainability`."
        )
    else:
        st.dataframe(
            explanation.head(10),
            use_container_width=True,
            hide_index=True,
        )

        top5 = ", ".join(
            explanation.head(5)["feature"].tolist()
        )

        st.info(
            f"""
### AI Clinical Interpretation

The V2 real-world readmission model highlights the following top risk drivers:

**{top5}**

These variables are associated with the patient's predicted 30-day readmission risk
and should be considered during discharge planning, medication review, follow-up
coordination, and diabetes care management.

This explanation uses deployment-safe global SHAP feature importance generated from
the real-world diabetes readmission dataset.
"""
        )