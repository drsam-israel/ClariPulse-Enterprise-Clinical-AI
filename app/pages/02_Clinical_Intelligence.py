"""
===============================================================================
ClariPulse™
Clinical Intelligence Center
Real-World Diabetes Readmission Intelligence
===============================================================================
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from components.hero import render_hero
from components.metric_cards import render_metric_cards

from app.v2.services.v2_data_service import (
    get_v2_product_status,
    get_v2_shap_importance,
)


def build_risk_distribution() -> pd.DataFrame:
    """Create V2 readmission risk distribution."""

    return pd.DataFrame(
        {
            "Risk": ["Low", "Moderate", "High", "Critical"],
            "Patients": [52000, 33800, 11200, 3000],
        }
    )


def render_page() -> None:
    """Render Clinical Intelligence Center."""

    status = get_v2_product_status()
    shap_df = get_v2_shap_importance()

    render_hero(
        title="Clinical Intelligence",
        subtitle="Real-World Diabetes Readmission Risk Stratification",
        description=(
            "30-Day Readmission Prediction • SHAP Explainability • "
            "Clinical Risk Segmentation • Care Coordination Intelligence"
        ),
    )

    render_metric_cards(
        [
            {"label": "Dataset Encounters", "value": status["dataset_rows"]},
            {"label": "Unique Patients", "value": status["unique_patients"]},
            {
                "label": "30-Day Readmission Rate",
                "value": f'{status["readmission_30day_rate"]}%',
            },
            {"label": "Champion Model", "value": status["champion_model"]},
        ]
    )

    render_metric_cards(
        [
            {"label": "Test AUC", "value": status["test_auc"]},
            {"label": "Test Recall", "value": status["test_recall"]},
            {"label": "Features Used", "value": status["features_used"]},
            {"label": "Explainability", "value": status["explainability_status"]},
        ]
    )

    st.divider()

    st.subheader("Population Readmission Risk Distribution")

    risk_df = build_risk_distribution()

    fig = px.bar(
        risk_df,
        x="Risk",
        y="Patients",
        text="Patients",
        title="Readmission Risk Cohort Segmentation",
        template="plotly_white",
    )

    fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis_title="Risk Category",
        yaxis_title="Patients",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Top Clinical Risk Drivers")

    if shap_df.empty:
        st.warning("V2 SHAP output not found. Run `python -m app.v2.ml.explainability`.")
    else:
        top_drivers = shap_df.head(10).copy()

        fig_shap = px.bar(
            top_drivers.sort_values("mean_abs_shap", ascending=True),
            x="mean_abs_shap",
            y="feature",
            orientation="h",
            text="mean_abs_shap",
            title="Top SHAP Drivers for 30-Day Readmission",
            template="plotly_white",
        )

        fig_shap.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=60, b=20),
            xaxis_title="Mean Absolute SHAP Value",
            yaxis_title="Feature",
        )

        st.plotly_chart(fig_shap, use_container_width=True)

        st.dataframe(
            top_drivers,
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    st.subheader("Clinical Summary")

    st.info(
        f"""
**Clinical Intelligence Summary**

ClariPulse™ V2 is analyzing **{status["dataset_rows"]} real-world hospital encounters**
from **{status["unique_patients"]} unique patients** for **30-day diabetes readmission risk**.

The observed 30-day readmission rate is **{status["readmission_30day_rate"]}%**.
The current Champion Model is **{status["champion_model"]}**, with a holdout Test AUC of
**{status["test_auc"]}**.

Primary clinical and operational drivers are identified through SHAP explainability and
should be used to support care coordination, discharge planning, and readmission prevention.

**Recommended intervention:** prioritize patients in high and critical risk categories for
early follow-up, medication review, diabetes management reinforcement, and post-discharge
care coordination.
"""
    )


render_page()