"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Platform
Module: Reports & Exports
Purpose: Executive, clinical, AI, and governance reporting center.
Author: Samuel Israel, MD
License: MIT
===============================================================================
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from components.hero import render_hero
from components.metric_cards import render_metric_cards


def build_report_catalog() -> pd.DataFrame:
    """Create demonstration report catalog."""
    return pd.DataFrame(
        {
            "Report Name": [
                "Executive Performance Summary",
                "Clinical Risk Stratification Report",
                "Model Benchmark Report",
                "SHAP Explainability Report",
                "Responsible AI Governance Report",
                "Product Usage Summary",
            ],
            "Category": [
                "Executive",
                "Clinical",
                "AI",
                "Explainability",
                "Governance",
                "Product",
            ],
            "Format": ["PDF", "CSV", "PDF", "PDF", "PDF", "Excel"],
            "Status": [
                "Ready",
                "Ready",
                "Ready",
                "Ready",
                "Ready",
                "Ready",
            ],
        }
    )


def render_page() -> None:
    """Render Reports & Exports page."""

    render_hero(
        title="Reports & Exports",
        subtitle="Executive-Ready Reporting Center",
        description=(
            "Generate clinical, operational, AI, explainability, governance, "
            "and product intelligence reports."
        ),
    )

    render_metric_cards(
        [
            {"label": "Reports Available", "value": "6"},
            {"label": "Export Formats", "value": "4"},
            {"label": "Governance Reports", "value": "Ready"},
            {"label": "Executive Pack", "value": "Ready"},
        ]
    )

    st.divider()

    st.subheader("Report Catalog")

    reports = build_report_catalog()

    st.dataframe(
        reports,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Generate Report")

    selected_report = st.selectbox(
        "Select report",
        reports["Report Name"].tolist(),
    )

    export_format = st.selectbox(
        "Export format",
        ["PDF", "CSV", "Excel", "JSON"],
    )

    if st.button("Generate Report"):
        st.success(
            f"{selected_report} generated successfully as {export_format}. "
            "Full export automation will be connected in the reporting engine."
        )

    st.divider()

    st.info(
        """
        **Reporting Strategy:** ClariPulse™ is designed to support board-level
        executive reports, clinician-facing risk summaries, AI model cards,
        SHAP explainability outputs, and Responsible AI governance evidence packs.
        """
    )


render_page()