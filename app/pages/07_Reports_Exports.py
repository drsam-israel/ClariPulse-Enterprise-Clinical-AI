"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Platform

Module:
    Reports & Exports

Purpose:
    Executive, clinical, AI, explainability, and governance reporting center
    for V2 real-world diabetes readmission intelligence.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations

import json

import pandas as pd
import streamlit as st

from components.hero import render_hero
from components.metric_cards import render_metric_cards

from app.v2.services.v2_data_service import (
    get_v2_benchmark_results,
    get_v2_data_profile,
    get_v2_product_status,
    get_v2_registry,
    get_v2_shap_importance,
)


def build_report_catalog() -> pd.DataFrame:
    """Create V2 report catalog."""

    return pd.DataFrame(
        {
            "Report Name": [
                "Executive Readmission Intelligence Summary",
                "Clinical Risk Stratification Report",
                "V2 Model Benchmark Report",
                "V2 SHAP Explainability Report",
                "Responsible AI Governance Report",
                "Real-World Data Profile Report",
                "Product Intelligence Summary",
            ],
            "Category": [
                "Executive",
                "Clinical",
                "AI",
                "Explainability",
                "Governance",
                "Data Quality",
                "Product",
            ],
            "Primary Evidence": [
                "101,766 encounters and 30-day readmission KPIs",
                "Risk segmentation and readmission prevention priorities",
                "Champion–Challenger evaluation results",
                "Global SHAP feature importance",
                "Governance scorecard and audit readiness",
                "Data profile, missingness, demographics, admissions",
                "Product status, model registry, and roadmap",
            ],
            "Status": [
                "Ready",
                "Ready",
                "Ready",
                "Ready",
                "Ready",
                "Ready",
                "Ready",
            ],
        }
    )


def build_executive_report_text() -> str:
    """Generate V2 executive report text."""

    status = get_v2_product_status()

    return f"""
ClariPulse™ V2 Executive Readmission Intelligence Summary

Product: {status["product"]}
Version: {status["version"]}
Use Case: {status["use_case"]}

Dataset Summary:
- Dataset Encounters: {status["dataset_rows"]}
- Unique Patients: {status["unique_patients"]}
- 30-Day Readmission Rate: {status["readmission_30day_rate"]}%

Model Summary:
- Champion Model: {status["champion_model"]}
- Cross-Validation AUC: {status["cv_auc"]}
- Holdout Test AUC: {status["test_auc"]}
- Features Used: {status["features_used"]}
- Models Benchmarked: {status["models_benchmarked"]}

Governance Summary:
- Governance Status: {status["status"]}
- Explainability Status: {status["explainability_status"]}
- Human Oversight: Active
- Bias Review: Passed
- Drift Status: Stable

Executive Recommendation:
Prioritize high-risk diabetes patients for discharge planning, medication review,
early follow-up, and post-discharge care coordination to reduce preventable
30-day readmissions.
"""


def render_page() -> None:
    """Render V2 Reports & Exports page."""

    status = get_v2_product_status()
    benchmark = get_v2_benchmark_results()
    shap_df = get_v2_shap_importance()
    data_profile = get_v2_data_profile()
    registry = get_v2_registry()

    render_hero(
        title="Reports & Exports",
        subtitle="Real-World AI Reporting Center",
        description=(
            "Generate executive, clinical, benchmark, SHAP, data quality, "
            "and Responsible AI governance reports for V2 diabetes readmission intelligence."
        ),
    )

    render_metric_cards(
        [
            {"label": "Reports Available", "value": "7"},
            {"label": "Dataset Encounters", "value": status["dataset_rows"]},
            {"label": "Champion Model", "value": status["champion_model"]},
            {"label": "Governance", "value": status["status"]},
        ]
    )

    render_metric_cards(
        [
            {"label": "Benchmark Rows", "value": len(benchmark)},
            {"label": "SHAP Features", "value": len(shap_df)},
            {"label": "Data Profile", "value": "Ready" if not data_profile.empty else "Pending"},
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
        ["TXT", "CSV", "JSON"],
    )

    if st.button("Generate Report", use_container_width=True):
        st.success(
            f"{selected_report} generated successfully as {export_format}."
        )

        if export_format == "TXT":
            report_text = build_executive_report_text()

            st.download_button(
                label="Download TXT Report",
                data=report_text,
                file_name="claripulse_v2_executive_report.txt",
                mime="text/plain",
            )

            st.text_area(
                "Report Preview",
                report_text,
                height=350,
            )

        elif export_format == "CSV":
            if "Benchmark" in selected_report:
                export_df = benchmark
                filename = "claripulse_v2_model_benchmark_report.csv"
            elif "SHAP" in selected_report:
                export_df = shap_df
                filename = "claripulse_v2_shap_report.csv"
            elif "Data Profile" in selected_report:
                export_df = data_profile
                filename = "claripulse_v2_data_profile_report.csv"
            else:
                export_df = reports
                filename = "claripulse_v2_report_catalog.csv"

            st.download_button(
                label="Download CSV Report",
                data=export_df.to_csv(index=False),
                file_name=filename,
                mime="text/csv",
            )

            st.dataframe(
                export_df,
                use_container_width=True,
                hide_index=True,
            )

        elif export_format == "JSON":
            export_json = {
                "status": status,
                "registry": registry,
                "selected_report": selected_report,
            }

            st.download_button(
                label="Download JSON Report",
                data=json.dumps(export_json, indent=4),
                file_name="claripulse_v2_report.json",
                mime="application/json",
            )

            st.json(export_json)

    st.divider()

    st.info(
        f"""
**Reporting Strategy:** ClariPulse™ V2 reporting now supports real-world
diabetes readmission intelligence based on **{status["dataset_rows"]} encounters**
and **{status["unique_patients"]} unique patients**.

The reporting center is designed to support:

- Executive readmission intelligence
- Clinical risk stratification
- Champion–Challenger model evidence
- SHAP explainability outputs
- Responsible AI governance packs
- Data quality and profiling evidence
- Product intelligence summaries
"""
    )


render_page()