"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product

Module:
    Explainability Studio

Purpose:
    Enterprise Explainable AI dashboard powered by SHAP for V2 real-world
    diabetes readmission prediction.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from components.hero import render_hero
from components.metric_cards import render_metric_cards

from app.v2.services.v2_data_service import (
    get_v2_product_status,
    get_v2_shap_importance,
)


def render_page() -> None:
    """Render V2 Explainability Studio."""

    status = get_v2_product_status()
    shap_df = get_v2_shap_importance()

    render_hero(
        title="Explainability Studio",
        subtitle="Real-World Readmission Explainability",
        description=(
            "Interpret the V2 diabetes readmission Champion Model using "
            "SHAP feature importance to improve clinician trust, governance, "
            "and care coordination."
        ),
    )

    if shap_df.empty:
        st.warning(
            "V2 SHAP results not found. Run:\n\n"
            "`python -m app.v2.ml.explainability`"
        )
        return

    top10 = shap_df.head(10)

    render_metric_cards(
        [
            {"label": "Features Analysed", "value": str(len(shap_df))},
            {"label": "Top Drivers", "value": "10"},
            {"label": "Champion Model", "value": status["champion_model"]},
            {"label": "SHAP Status", "value": status["explainability_status"]},
        ]
    )

    render_metric_cards(
        [
            {"label": "Dataset Encounters", "value": status["dataset_rows"]},
            {
                "label": "30-Day Readmission Rate",
                "value": f'{status["readmission_30day_rate"]}%',
            },
            {"label": "Test AUC", "value": status["test_auc"]},
            {"label": "Use Case", "value": "30-Day Readmission"},
        ]
    )

    st.divider()

    st.subheader("Top 10 SHAP Feature Importance")

    fig = px.bar(
        top10.sort_values("mean_abs_shap", ascending=True),
        x="mean_abs_shap",
        y="feature",
        orientation="h",
        text="mean_abs_shap",
        title="Global SHAP Feature Importance for Readmission Risk",
    )

    fig.update_layout(
        height=550,
        showlegend=False,
        template="plotly_white",
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis_title="Mean Absolute SHAP Value",
        yaxis_title="Feature",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Feature Importance Table")

    st.dataframe(
        top10,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Executive Interpretation")

    top_features = ", ".join(top10["feature"].head(5).tolist())

    st.success(
        f"""
### Executive AI Insight

The V2 Champion Model for **30-day diabetes readmission prediction**
primarily relies on:

**{top_features}**

These variables contribute the greatest influence on readmission risk and should
receive priority attention during discharge planning, medication review,
diabetes care management, and post-discharge follow-up.

The Explainability Studio provides transparent AI reasoning to improve clinician
trust, governance compliance, and Responsible AI adoption.
"""
    )


render_page()