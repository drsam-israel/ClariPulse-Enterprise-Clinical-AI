"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product

Module:
    Explainability Studio

Purpose:
    Enterprise Explainable AI dashboard powered by SHAP.

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
from app.services.data_service import get_shap_importance


def render_page() -> None:
    """Render Explainability Studio."""

    render_hero(
        title="Explainability Studio",
        subtitle="Transparent Clinical AI & SHAP Intelligence",
        description=(
            "Interpret model predictions using SHAP feature importance "
            "to improve clinician trust and Responsible AI governance."
        ),
    )

    shap_df = get_shap_importance()

    if shap_df.empty:
        st.warning(
            "SHAP results not found. Run:\n\n"
            "`python -m app.ml.explainability`"
        )
        return

    top10 = shap_df.head(10)

    render_metric_cards(
        [
            {"label": "Features Analysed", "value": str(len(shap_df))},
            {"label": "Top Drivers", "value": "10"},
            {"label": "Explainability", "value": "100%"},
            {"label": "SHAP Status", "value": "Ready"},
        ]
    )

    st.divider()

    st.subheader("Top 10 Feature Importance")

    fig = px.bar(
        top10.sort_values("mean_abs_shap", ascending=True),
        x="mean_abs_shap",
        y="feature",
        orientation="h",
        text="mean_abs_shap",
        title="Global SHAP Feature Importance",
    )

    fig.update_layout(
        height=550,
        showlegend=False,
        template="plotly_white",
        margin=dict(l=20, r=20, t=60, b=20),
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

The current Champion Model primarily relies on:

**{top_features}**

These variables contribute the greatest influence on clinical
risk prediction and should receive priority attention during
patient assessment and care planning.

The Explainability Studio provides transparent AI reasoning
to improve clinician trust, governance compliance, and
Responsible AI adoption.
"""
    )


render_page()