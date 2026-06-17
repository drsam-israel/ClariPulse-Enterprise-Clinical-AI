"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product

Module:
    Data Source Manager

Purpose:
    Enterprise ingestion readiness dashboard for CSV, SQL, FHIR, HL7, and EHR
    data sources.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from components.hero import render_hero
from components.metric_cards import render_metric_cards
from app.v2.ingestion.ingestion_service import IngestionService


def render_page() -> None:
    """Render Data Source Manager."""

    render_hero(
        title="Data Source Manager",
        subtitle="Enterprise Healthcare Data Ingestion Layer",
        description=(
            "Manage data source readiness across CSV, SQL databases, FHIR APIs, "
            "HL7 feeds, and enterprise EHR ecosystems."
        ),
    )

    sources = IngestionService.supported_sources()

    supported_count = int((sources["Status"] == "Supported").sum())
    planned_count = int((sources["Status"] == "Planned").sum())

    render_metric_cards(
        [
            {"label": "Supported Sources", "value": supported_count},
            {"label": "Planned Sources", "value": planned_count},
            {"label": "Current Ingestion Layer", "value": "CSV + SQL"},
            {"label": "FHIR / HL7", "value": "Planned"},
        ]
    )

    st.divider()

    st.subheader("Enterprise Data Source Readiness")

    display_df = sources.copy()

    display_df["Readiness"] = display_df["Status"].apply(
        lambda x: "✅ Ready" if x == "Supported" else "🟡 Roadmap"
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Ingestion Architecture")

    architecture = pd.DataFrame(
        {
            "Layer": [
                "Source Systems",
                "Connector Layer",
                "Validation Layer",
                "Feature Engineering",
                "AI Prediction Layer",
                "Governance Layer",
                "Executive Intelligence",
            ],
            "Description": [
                "CSV, SQL, FHIR, HL7, Epic, Cerner, OpenMRS",
                "Standardized connectors for structured healthcare data",
                "Schema checks, missingness review, quality validation",
                "Clinical feature transformation and target preparation",
                "Champion Model inference and risk scoring",
                "Bias, drift, explainability, audit readiness",
                "Dashboards, reports, and operational decision support",
            ],
        }
    )

    st.dataframe(
        architecture,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Connector Status")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### ✅ CSV Connector")
            st.write(
                "Supports hospital analytics exports, research datasets, "
                "registry extracts, and operational CSV files."
            )
            st.success("Status: Supported")

    with col2:
        with st.container(border=True):
            st.markdown("### ✅ SQL Connector")
            st.write(
                "Supports structured database ingestion through SQLAlchemy "
                "connection strings and query-based extraction."
            )
            st.success("Status: Supported")

    col3, col4 = st.columns(2)

    with col3:
        with st.container(border=True):
            st.markdown("### 🟡 FHIR API Connector")
            st.write(
                "Planned support for Patient, Encounter, Observation, Condition, "
                "MedicationRequest, and DiagnosticReport resources."
            )
            st.warning("Status: Planned")

    with col4:
        with st.container(border=True):
            st.markdown("### 🟡 HL7 / EHR Connector")
            st.write(
                "Planned support for HL7 feeds and enterprise EHR environments "
                "including Epic, Cerner, and OpenMRS."
            )
            st.warning("Status: Planned")

    st.divider()

    st.subheader("Executive Interpretation")

    st.info(
        """
ClariPulse™ V2 now includes the foundation of a pluggable enterprise ingestion
architecture.

Current supported connectors include:

- CSV ingestion for hospital analytics exports
- SQL ingestion for structured healthcare databases

Planned connectors include:

- FHIR APIs
- HL7 feeds
- Epic
- Cerner
- OpenMRS
- Snowflake
- Databricks

This positions ClariPulse™ for evolution from a real-world dataset-driven AI product
into a vendor-agnostic Clinical AI operating platform capable of integrating with
enterprise healthcare data ecosystems.
"""
    )


render_page()