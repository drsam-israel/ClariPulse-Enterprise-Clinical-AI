"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product

Module:
    Product Intelligence Center

Purpose:
    Executive product health, adoption, maturity, roadmap, and AI product status.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from components.hero import render_hero
from components.metric_cards import render_metric_cards
from app.services.data_service import (
    get_product_status,
    get_benchmark_results,
    get_shap_importance,
)


def render_page() -> None:
    """Render Product Intelligence Center."""

    render_hero(
        title="Product Intelligence",
        subtitle="AI Product Health, Adoption & Value Intelligence",
        description=(
            "Monitor product maturity, AI engine status, adoption readiness, "
            "governance alignment, and strategic roadmap progress."
        ),
    )

    status = get_product_status()
    benchmark = get_benchmark_results()
    shap_df = get_shap_importance()

    render_metric_cards(
        [
            {"label": "Product Version", "value": "v1.0"},
            {"label": "AI Engine", "value": "Live"},
            {"label": "Champion Model", "value": status["champion_model"]},
            {"label": "Champion AUC", "value": status["champion_auc"]},
        ]
    )

    render_metric_cards(
        [
            {"label": "Models Benchmarked", "value": status["models_benchmarked"]},
            {"label": "Features Used", "value": status["features_used"]},
            {"label": "SHAP Features", "value": status["shap_features"]},
            {"label": "Product Status", "value": "Operational"},
        ]
    )

    st.divider()

    st.subheader("AI Product Health Overview")

    health_df = pd.DataFrame(
        {
            "Capability": [
                "Prediction Engine",
                "Model Registry",
                "Benchmarking",
                "Explainability",
                "Responsible AI",
                "Reports & Exports",
                "Executive Intelligence",
            ],
            "Status": [
                "Live",
                "Synced",
                "Complete",
                status["explainability_status"],
                "Active",
                "Ready",
                "Operational",
            ],
            "Score": [95, 94, 93, 96, 92, 90, 95],
        }
    )

    fig = px.bar(
        health_df,
        x="Capability",
        y="Score",
        text="Score",
        title="Product Capability Health Score",
    )

    fig.update_layout(
        template="plotly_white",
        height=480,
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis_title="Capability",
        yaxis_title="Health Score",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        health_df,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Model & Explainability Intelligence")

    c1, c2 = st.columns(2)

    with c1:
        if not benchmark.empty:
            fig_model = px.bar(
                benchmark.sort_values("auc", ascending=True),
                x="auc",
                y="model",
                orientation="h",
                text="auc",
                title="Model Performance Snapshot",
            )
            fig_model.update_layout(template="plotly_white", height=420)
            st.plotly_chart(fig_model, use_container_width=True)
        else:
            st.warning("Benchmark results not available.")

    with c2:
        if not shap_df.empty:
            top_shap = shap_df.head(8).sort_values("mean_abs_shap", ascending=True)

            fig_shap = px.bar(
                top_shap,
                x="mean_abs_shap",
                y="feature",
                orientation="h",
                text="mean_abs_shap",
                title="Top Explainability Drivers",
            )
            fig_shap.update_layout(template="plotly_white", height=420)
            st.plotly_chart(fig_shap, use_container_width=True)
        else:
            st.warning("SHAP explainability results not available.")

    st.divider()

    st.subheader("Product Maturity Roadmap")

    roadmap_df = pd.DataFrame(
        {
            "Phase": [
                "Foundation",
                "AI Engine",
                "Explainability",
                "Governance",
                "Executive Intelligence",
                "Operationalization",
            ],
            "Status": [
                "Complete",
                "Complete",
                "Complete",
                "Complete",
                "Complete",
                "V2 Planned",
            ],
            "Progress": [100, 100, 100, 100, 100, 35],
        }
    )

    fig_roadmap = px.line(
        roadmap_df,
        x="Phase",
        y="Progress",
        markers=True,
        text="Progress",
        title="ClariPulse™ Product Maturity Progression",
    )

    fig_roadmap.update_layout(
        template="plotly_white",
        height=430,
        yaxis_range=[0, 110],
    )

    st.plotly_chart(fig_roadmap, use_container_width=True)

    st.dataframe(
        roadmap_df,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Executive Product Interpretation")

    st.success(
        f"""
### Product Intelligence Summary

ClariPulse™ v1.0 is operating as a functional enterprise Clinical AI product.

The current AI engine is live with **{status["models_benchmarked"]} benchmarked models**,
a registered Champion Model (**{status["champion_model"]}**), and a current Champion AUC of
**{status["champion_auc"]}**.

The product includes predictive analytics, SHAP explainability, responsible AI governance,
executive intelligence, patient-level risk prediction, and report generation.

### V2 Direction

The next maturity step is operationalization through a pluggable ingestion layer for:

• CSV datasets  
• SQL databases  
• FHIR APIs  
• EHR systems such as Epic, Cerner, and OpenMRS  

This will evolve ClariPulse™ from a portfolio-ready Clinical AI product into a real-world,
data-source-agnostic Clinical AI operating platform.
"""
    )


render_page()