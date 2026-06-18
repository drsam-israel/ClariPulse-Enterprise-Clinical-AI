"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product

Module:
    Dataset Governance

Purpose:
    Read-only enterprise dataset governance dashboard for staged, production,
    approved, rejected, and pending healthcare datasets.

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

from app.v2.services.dataset_governance_service import (
    build_governance_audit_timeline,
    build_governance_view,
    get_governance_summary,
)


def render_page() -> None:
    """Render Dataset Governance Center."""

    governance = build_governance_view()
    summary = get_governance_summary()
    timeline = build_governance_audit_timeline()

    render_hero(
        title="Dataset Governance",
        subtitle="Enterprise Dataset Review & Compliance Center",
        description=(
            "Governance visibility for production and staged datasets, including "
            "review status, compliance posture, audit readiness, and lifecycle tracking."
        ),
    )

    render_metric_cards(
        [
            {"label": "Total Datasets", "value": summary["total_datasets"]},
            {"label": "Approved", "value": summary["approved"]},
            {"label": "Pending Review", "value": summary["pending_review"]},
            {"label": "Rejected", "value": summary["rejected"]},
        ]
    )

    render_metric_cards(
        [
            {"label": "Compliance Rate", "value": f'{summary["compliance_rate"]}%'},
            {"label": "Governance Mode", "value": "Read-Only"},
            {"label": "Production Safety", "value": "Protected"},
            {"label": "Retraining", "value": "Disabled"},
        ]
    )

    st.divider()

    st.subheader("Dataset Governance View")

    if governance.empty:
        st.warning("No registered datasets found.")
        return

    display_columns = [
        "dataset_name",
        "source",
        "status",
        "governance_status",
        "reviewer",
        "decision_date",
        "quality_score",
        "schema_compatible",
        "comments",
    ]

    existing_columns = [
        column for column in display_columns if column in governance.columns
    ]

    st.dataframe(
        governance[existing_columns],
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Governance Status Distribution")

    status_counts = (
        governance["governance_status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = ["Governance Status", "Count"]

    fig = px.pie(
        status_counts,
        names="Governance Status",
        values="Count",
        hole=0.45,
        title="Dataset Governance Status",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Quality Score by Governance Status")

    chart_df = governance.copy()

    chart_df["quality_score"] = pd.to_numeric(
        chart_df["quality_score"],
        errors="coerce",
    )

    fig2 = px.bar(
        chart_df.sort_values("quality_score", ascending=True),
        x="quality_score",
        y="dataset_name",
        color="governance_status",
        orientation="h",
        text="quality_score",
        title="Dataset Quality Score and Governance Status",
        template="plotly_white",
    )

    fig2.update_layout(
        height=520,
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis_title="Quality Score",
        yaxis_title="Dataset",
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.subheader("Governance Audit Timeline")

    st.dataframe(
        timeline,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Governance Controls")

    controls = pd.DataFrame(
        {
            "Control": [
                "Production dataset overwrite",
                "Automatic retraining",
                "Champion model replacement",
                "Dataset staging visibility",
                "Governance review visibility",
                "Audit timeline",
            ],
            "Status": [
                "Disabled",
                "Disabled",
                "Disabled",
                "Enabled",
                "Enabled",
                "Enabled",
            ],
        }
    )

    st.dataframe(
        controls,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Executive Interpretation")

    st.success(
        f"""
### Dataset Governance Summary

ClariPulse™ currently tracks **{summary["total_datasets"]} dataset(s)**
within the enterprise governance layer.

Governance posture:

- **Approved datasets:** {summary["approved"]}
- **Pending review:** {summary["pending_review"]}
- **Rejected datasets:** {summary["rejected"]}
- **Compliance rate:** {summary["compliance_rate"]}%

This page is intentionally **read-only**. It provides governance visibility without
modifying production data, retraining models, changing the Champion Model, or altering
the active prediction pipeline.

This design supports safe enterprise AI lifecycle management and prepares ClariPulse™
for future controlled approval, retraining, and model promotion workflows.
"""
    )


render_page()