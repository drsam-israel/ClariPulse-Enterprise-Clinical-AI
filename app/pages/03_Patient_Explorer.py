"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product

Patient Explorer

Author:
Samuel Israel, MD
===============================================================================
"""

from __future__ import annotations

import streamlit as st

from components.hero import render_hero
from app.ml.predict import predict_patient
from app.ml.explainability import explain_patient

render_hero(
    title="Patient Explorer",
    subtitle="Interactive Clinical Risk Prediction",
    description=(
        "Enter patient characteristics to generate AI-powered "
        "clinical risk predictions."
    ),
)

st.subheader("Patient Information")

col1, col2 = st.columns(2)

with col1:

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=65,
    )

    bmi = st.number_input(
        "BMI",
        value=28.0,
    )

    diabetes = st.selectbox(
        "Diabetes",
        [0, 1],
    )

    hypertension = st.selectbox(
        "Hypertension",
        [0, 1],
    )

    smoker = st.selectbox(
        "Smoker",
        [0, 1],
    )

with col2:

    ckd = st.selectbox(
        "CKD",
        [0, 1],
    )

    copd = st.selectbox(
        "COPD",
        [0, 1],
    )

    heart_failure = st.selectbox(
        "Heart Failure",
        [0, 1],
    )

    obesity = st.selectbox(
        "Obesity",
        [0, 1],
    )

    cancer = st.selectbox(
        "Cancer",
        [0, 1],
    )

if st.button("🔮 Predict Clinical Risk", use_container_width=True):

    patient = {
        "age": age,
        "bmi": bmi,
        "diabetes": diabetes,
        "hypertension": hypertension,
        "smoker": smoker,
        "ckd": ckd,
        "copd": copd,
        "heart_failure": heart_failure,
        "obesity": obesity,
        "cancer": cancer,
    }

    result = predict_patient(patient)

    probability = result["probability"]
    risk = result["risk_percent"]

    if risk < 25:
        category = "🟢 Low"

    elif risk < 50:
        category = "🟡 Moderate"

    elif risk < 75:
        category = "🟠 High"

    else:
        category = "🔴 Critical"

    st.success(f"Prediction: {result['prediction']}")

    st.metric(
        "Risk Probability",
        f"{risk:.1f}%",
    )

    st.metric(
        "Risk Category",
        category,
    )

    st.json(result)

      # -----------------------------
    # Top AI Risk Drivers
    # -----------------------------

    st.divider()

    st.subheader("Top AI Risk Drivers")

    explanation = explain_patient(patient)

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

The champion model primarily based this prediction on:

**{top5}**

These variables had the greatest influence on the patient's
predicted clinical risk and should be prioritized during
clinical assessment and management.
"""
    )