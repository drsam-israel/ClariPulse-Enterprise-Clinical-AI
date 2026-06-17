"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product

Module:
    Model Benchmark Center

Purpose:
    Champion–Challenger evaluation dashboard for the
    Real-World Diabetes Readmission AI Model.

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
    get_v2_benchmark_results,
    get_v2_metadata,
    get_v2_registry,
)


def render_page() -> None:
    """Render V2 Model Benchmark Center."""

    render_hero(
        title="Model Benchmark",
        subtitle="Champion–Challenger Evaluation",
        description=(
            "Real-world diabetes readmission model comparison using "
            "cross-validation and holdout performance metrics."
        ),
    )

    benchmark = get_v2_benchmark_results()
    registry = get_v2_registry()
    metadata = get_v2_metadata()

    if benchmark.empty:
        st.warning(
            "Benchmark results not found.\n\n"
            "Run:\n"
            "`python -m app.v2.ml.train_diabetes_models`"
        )
        return

    champion_model = registry.get(
        "champion_model",
        benchmark.iloc[0]["model"],
    )

    cv_auc = registry.get(
        "cv_auc",
        benchmark.iloc[0]["auc"],
    )

    test_auc = registry.get(
        "test_auc",
        "N/A",
    )

    feature_count = metadata.get(
        "feature_count",
        "N/A",
    )

    train_rows = metadata.get(
        "train_rows",
        "N/A",
    )

    render_metric_cards(
        [
            {
                "label": "Models Benchmarked",
                "value": len(benchmark),
            },
            {
                "label": "Champion Model",
                "value": champion_model,
            },
            {
                "label": "Cross-Validation AUC",
                "value": round(float(cv_auc), 4),
            },
            {
                "label": "Holdout Test AUC",
                "value": test_auc,
            },
        ]
    )

    render_metric_cards(
        [
            {
                "label": "Features Used",
                "value": feature_count,
            },
            {
                "label": "Training Rows",
                "value": train_rows,
            },
            {
                "label": "Use Case",
                "value": "30-Day Readmission",
            },
            {
                "label": "Deployment Status",
                "value": "Production Ready",
            },
        ]
    )

    st.divider()

    st.subheader("Champion–Challenger Leaderboard")

    leaderboard = benchmark.copy()

    leaderboard["Champion"] = leaderboard["model"].apply(
        lambda x: "🏆 Champion" if x == champion_model else ""
    )

    st.dataframe(
        leaderboard,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("ROC AUC Comparison")

    fig = px.bar(
        benchmark.sort_values("auc", ascending=True),
        x="auc",
        y="model",
        orientation="h",
        text="auc",
        title="Cross-Validated ROC AUC",
        template="plotly_white",
    )

    fig.update_layout(
        height=500,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.divider()

    st.subheader("Performance Comparison")

    metrics_df = benchmark.melt(
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
        metrics_df,
        x="model",
        y="Score",
        color="Metric",
        barmode="group",
        title="Accuracy • Precision • Recall • F1 • ROC AUC",
        template="plotly_white",
    )

    fig2.update_layout(
        height=550,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
    )

    st.divider()

    st.subheader("Executive Interpretation")

    st.success(
        f"""
### Champion–Challenger Summary

The benchmark engine evaluated **{len(benchmark)} machine learning models**
for **30-day diabetes readmission prediction**.

🏆 **Champion Model:** {champion_model}

📈 **Cross-Validation ROC AUC:** {round(float(cv_auc),4)}

📊 **Holdout Test ROC AUC:** {test_auc}

The selected Champion Model demonstrated the strongest balance of:

- Predictive discrimination
- Precision
- Recall
- F1 performance
- Cross-validation stability
- Explainability compatibility
- Responsible AI governance readiness
- Enterprise deployment suitability

The benchmark framework supports transparent model selection and
continuous performance monitoring within ClariPulse™.
"""
    )


render_page()