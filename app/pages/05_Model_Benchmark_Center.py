"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product

Module:
    Model Benchmark

Purpose:
    Champion–Challenger model evaluation dashboard.

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
from app.services.data_service import (
    get_benchmark_results,
    get_model_registry,
    get_training_metadata,
)

def render_page() -> None:
    """Render Model Benchmark Center."""

    render_hero(
        title="Model Benchmark",
        subtitle="Champion–Challenger AI Model Evaluation",
        description=(
            "Live model benchmarking, champion selection, cross-validation evidence, "
            "and enterprise AI performance governance."
        ),
    )

    benchmark = get_benchmark_results()
    registry = get_model_registry()
    training = get_training_metadata()

    if benchmark.empty:
        st.warning(
            "Benchmark results not found. Run: `python -m app.ml.train_models`"
        )
        return

    champion_model = registry.get("champion_model", benchmark.iloc[0]["model"])
    champion_auc = registry.get("auc", benchmark.iloc[0]["auc"])
    feature_count = training.get("feature_count", "N/A")

    render_metric_cards(
        [
            {"label": "Models Compared", "value": len(benchmark)},
            {"label": "Champion Model", "value": champion_model},
            {"label": "Champion AUC", "value": round(float(champion_auc), 4)},
            {"label": "Features Used", "value": feature_count},
        ],
    
    )

    st.divider()

    st.subheader("Live Model Leaderboard")

    display_df = benchmark.copy()

    display_df["champion"] = display_df["model"].apply(
        lambda model: "🏆 Champion" if model == champion_model else ""
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Champion–Challenger Performance")

    chart_df = benchmark.sort_values("auc", ascending=True)

    fig = px.bar(
        chart_df,
        x="auc",
        y="model",
        orientation="h",
        text="auc",
        title="Model Performance Ranked by ROC AUC",
    )

    fig.update_layout(
        template="plotly_white",
        height=480,
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis_title="ROC AUC",
        yaxis_title="Model",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Metric Comparison")

    metric_view = benchmark.melt(
        id_vars=["model"],
        value_vars=[
            "accuracy",
            "precision",
            "recall",
            "f1",
            "auc",
        ],
        var_name="Metric",
        value_name="Score",
    )

    fig2 = px.bar(
        metric_view,
        x="model",
        y="Score",
        color="Metric",
        barmode="group",
        title="Accuracy, Precision, Recall, F1 and AUC Comparison",
    )

    fig2.update_layout(
        template="plotly_white",
        height=520,
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis_title="Model",
        yaxis_title="Score",
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.subheader("Executive Summary")

    st.success(
        f"""
The benchmark engine evaluated **{len(benchmark)} candidate models** using
cross-validated performance metrics.

The selected Champion model is **{champion_model}**, achieving a ROC AUC of
**{round(float(champion_auc), 4)}**.

Selection criteria include:

• Predictive discrimination  
• Recall and F1 balance  
• Cross-validation stability  
• Explainability compatibility  
• Responsible AI governance readiness  
• Operational deployment suitability
"""
    )


render_page()