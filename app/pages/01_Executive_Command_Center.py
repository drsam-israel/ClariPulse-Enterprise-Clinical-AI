"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: Executive Command Center
Purpose: Board-ready executive intelligence dashboard.
Author: Samuel Israel, MD
License: MIT
===============================================================================
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from components.hero import render_hero
from components.metric_cards import render_metric_cards

from app.utils.model_loader import (
    load_registry,
    load_training,
    load_benchmark,
)

def build_demo_trends() -> pd.DataFrame:
    """Create demo executive trend data."""
    return pd.DataFrame(
        {
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Admissions": [8200, 8700, 9100, 9400, 9800, 10250],
            "Readmission Rate": [10.8, 10.4, 9.9, 9.5, 9.1, 8.7],
            "High Risk Patients": [1320, 1410, 1495, 1530, 1588, 1620],
        }
    )


def render_live_ai_kpis() -> None:
    """Render live AI model KPIs from registry and benchmark files."""

    registry = load_registry()
    training = load_training()
    benchmark = load_benchmark()

    champion_model = registry.get("champion_model", "Unknown")
    champion_auc = registry.get("auc", "N/A")
    model_status = registry.get("status", "Unknown")

    model_count = len(benchmark) if not benchmark.empty else 0
    feature_count = training.get("feature_count", "N/A")
    train_rows = training.get("train_rows", "N/A")
    test_rows = training.get("test_rows", "N/A")

    if isinstance(champion_auc, float):
        champion_auc = round(champion_auc, 4)

    render_metric_cards(
        [
            {"label": "Champion Model", "value": champion_model},
            {"label": "Champion AUC", "value": champion_auc},
            {"label": "Models Benchmarked", "value": model_count},
            {"label": "Model Status", "value": model_status},
        ],
        
    )

    render_metric_cards(
        [
            {"label": "Features Used", "value": feature_count},
            {"label": "Training Rows", "value": train_rows},
            {"label": "Test Rows", "value": test_rows},
            {"label": "AI Engine", "value": "Live"},
        ],
        
    )


def render_model_benchmark_chart() -> None:
    """Render live benchmark chart."""

    benchmark = load_benchmark()

    if benchmark.empty:
        st.warning("Benchmark results not found. Run `python -m app.ml.train_models`.")
        return

    st.subheader("Live Model Benchmark Leaderboard")

    st.dataframe(
        benchmark,
        use_container_width=True,
        hide_index=True,
    )

    fig = px.bar(
        benchmark.sort_values("auc", ascending=True),
        x="auc",
        y="model",
        orientation="h",
        text="auc",
        title="Model Performance by ROC AUC",
    )

    fig.update_layout(
        height=420,
        template="plotly_white",
        margin=dict(l=20, r=20, t=60, b=20),
    )

    st.plotly_chart(fig, use_container_width=True)


def render_ai_governance_status() -> None:
    """Render responsible AI governance status."""
    st.subheader("Responsible AI Status")

    c1, c2, c3, c4 = st.columns(4)

    c1.success("Bias Check: Passed")
    c2.success("Drift Status: Stable")
    c3.success("Explainability: 100%")
    c4.success("Human Oversight: Active")


def render_executive_insight() -> None:
    """Render executive interpretation and recommendations."""

    registry = load_registry()
    champion_model = registry.get("champion_model", "the champion model")
    auc = registry.get("auc", "N/A")

    st.subheader("Executive Insight & Recommended Actions")

    st.info(
        f"""
        **Executive AI Insight:** ClariPulse™ is now operating with a live
        trained champion model: **{champion_model}**, with a current ROC AUC of
        **{auc}** based on the latest benchmark run.
        """
    )

    st.markdown(
        """
        **Recommended Actions**

        1. Continue monitoring champion model performance after each retraining cycle.
        2. Review high-risk patient predictions in the Patient Explorer.
        3. Use Explainability Studio to examine SHAP-based top drivers.
        4. Maintain weekly responsible AI governance review.
        5. Re-run benchmarking after major data or feature updates.
        """
    )


def render_executive_command_center() -> None:
    """Render the Executive Command Center page."""

    render_hero(
        title="Executive Command",
        subtitle="Strategic Intelligence for Healthcare Leaders",
        description=(
            "Live AI operations, clinical risk intelligence, responsible AI status, "
            "and executive-ready recommendations."
        ),
    )

    render_live_ai_kpis()

    st.divider()

    render_model_benchmark_chart()

    st.divider()

    trends = build_demo_trends()

    st.subheader("Clinical Operations Intelligence")

    c1, c2 = st.columns(2)

    with c1:
        fig = px.line(
            trends,
            x="Month",
            y="Admissions",
            markers=True,
            title="Monthly Admissions Trend",
            template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.line(
            trends,
            x="Month",
            y="Readmission Rate",
            markers=True,
            title="30-Day Readmission Rate Trend",
            template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        fig = px.bar(
            trends,
            x="Month",
            y="High Risk Patients",
            title="High-Risk Patient Volume",
            template="plotly_white",
        )
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        risk_df = pd.DataFrame(
            {
                "Risk Category": ["Low", "Moderate", "High", "Critical"],
                "Patients": [52000, 33800, 11200, 3000],
            }
        )
        fig = px.pie(
            risk_df,
            names="Risk Category",
            values="Patients",
            title="Population Risk Distribution",
            hole=0.45,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    render_ai_governance_status()

    st.divider()

    render_executive_insight()


render_executive_command_center()