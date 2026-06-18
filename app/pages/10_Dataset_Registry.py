"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product

Module:
    Dataset Registry

Purpose:
    Enterprise read-only registry for all production and staged datasets.

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

from app.v2.services.dataset_registry_service import (
    load_dataset_registry,
    get_registry_summary,
    ensure_default_production_dataset,
)


def render_page() -> None:
    """Render Dataset Registry."""

    ensure_default_production_dataset()

    registry = load_dataset_registry()
    summary = get_registry_summary()

    render_hero(
        title="Dataset Registry",
        subtitle="Enterprise Dataset Inventory & Governance",
        description=(
            "Persistent registry of production and staged datasets with "
            "quality scoring, governance visibility, and audit readiness."
        ),
    )

    # =====================================================
    # KPI Cards
    # =====================================================

    render_metric_cards(
        [
            {
                "label": "Registered Datasets",
                "value": summary["total_datasets"],
            },
            {
                "label": "Production",
                "value": summary["production_datasets"],
            },
            {
                "label": "Staged",
                "value": summary["staged_datasets"],
            },
            {
                "label": "Average Quality",
                "value": f'{summary["average_quality_score"]}%',
            },
        ]
    )

    st.divider()

    # =====================================================
    # Registry Table
    # =====================================================

    st.subheader("Dataset Inventory")

    st.dataframe(
        registry,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # =====================================================
    # Quality Score Chart
    # =====================================================

    st.subheader("Dataset Quality Scores")

    chart_df = registry.copy()

    chart_df["quality_score"] = pd.to_numeric(
        chart_df["quality_score"],
        errors="coerce",
    )

    fig = px.bar(
        chart_df.sort_values(
            "quality_score",
            ascending=True,
        ),
        x="quality_score",
        y="dataset_name",
        orientation="h",
        text="quality_score",
        title="Registered Dataset Quality Scores",
    )

    fig.update_layout(
        template="plotly_white",
        height=500,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.divider()

    # =====================================================
    # Status Distribution
    # =====================================================

    st.subheader("Dataset Status Distribution")

    status_counts = (
        registry["status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = [
        "Status",
        "Count",
    ]

    fig2 = px.pie(
        status_counts,
        names="Status",
        values="Count",
        hole=0.45,
        title="Production vs Staged vs Approved vs Rejected",
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
    )

    st.divider()

    # =====================================================
    # Upload Timeline
    # =====================================================

    st.subheader("Dataset Registration Timeline")

    timeline = registry[
        [
            "dataset_name",
            "upload_timestamp",
            "status",
        ]
    ]

    st.dataframe(
        timeline,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # =====================================================
    # Executive Interpretation
    # =====================================================

    st.subheader("Executive Interpretation")

    st.success(
        f"""
### Enterprise Dataset Registry Summary

The ClariPulse™ Dataset Registry currently tracks
**{summary["total_datasets"]} registered dataset(s)**.

Current composition includes:

- **Production datasets:** {summary["production_datasets"]}
- **Staged datasets:** {summary["staged_datasets"]}
- **Approved datasets:** {summary["approved_datasets"]}
- **Rejected datasets:** {summary["rejected_datasets"]}

The current average dataset quality score is
**{summary["average_quality_score"]}%**.

This registry provides an immutable inventory of enterprise data
assets while ensuring that staging, governance, and future model
retraining workflows remain isolated from the production prediction
pipeline.
"""
    )


render_page()