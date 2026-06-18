"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product

Module:
    Data Source Manager

Purpose:
    Enterprise ingestion readiness dashboard for CSV, SQL, FHIR, HL7, and EHR
    data sources with safe CSV upload, validation, governed staging, and
    persistent Dataset Registry logging.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations

from datetime import datetime

import pandas as pd
import streamlit as st

from components.hero import render_hero
from components.metric_cards import render_metric_cards
from app.v2.ingestion.ingestion_service import IngestionService
from app.v2.services.dataset_registry_service import (
    register_staged_dataset_from_summary,
)


DIABETES_REQUIRED_COLUMNS = [
    "time_in_hospital",
    "num_lab_procedures",
    "num_procedures",
    "num_medications",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "number_diagnoses",
    "readmitted",
]


def summarize_uploaded_csv(df: pd.DataFrame) -> dict:
    """Summarize uploaded CSV data safely."""

    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }


def validate_uploaded_schema(
    df: pd.DataFrame,
    required_columns: list[str],
) -> dict:
    """Validate uploaded CSV against expected schema."""

    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]

    return {
        "valid": len(missing_columns) == 0,
        "missing_columns": missing_columns,
        "required_columns": required_columns,
    }


def render_staged_dataset_status() -> None:
    """Render currently staged dataset status."""

    if "staged_dataset_summary" not in st.session_state:
        return

    st.divider()

    st.subheader("Currently Staged Dataset")

    staged_summary = st.session_state.get("staged_dataset_summary", {})
    staged_validation = st.session_state.get("staged_dataset_validation", {})
    staged_name = st.session_state.get("staged_dataset_name", "Uploaded CSV")
    staged_time = st.session_state.get("staged_dataset_timestamp", "N/A")
    registry_status = st.session_state.get("staged_dataset_registry_status", "Recorded")

    st.success(
        f"""
Dataset staged successfully for governance review.

**Dataset:** {staged_name}  
**Staged At:** {staged_time}  
**Registry Status:** {registry_status}  
**Activation Status:** Not activated  
**Model Retraining:** Disabled  
**Production Dataset Overwrite:** Disabled
"""
    )

    render_metric_cards(
        [
            {"label": "Staged Rows", "value": staged_summary.get("rows", "N/A")},
            {"label": "Staged Columns", "value": staged_summary.get("columns", "N/A")},
            {
                "label": "Missing Values",
                "value": staged_summary.get("missing_values", "N/A"),
            },
            {
                "label": "Schema Compatible",
                "value": "Yes" if staged_validation.get("valid") else "No",
            },
        ]
    )

    if st.button("🧹 Clear Staged Dataset", use_container_width=True):
        st.session_state.pop("staged_dataset", None)
        st.session_state.pop("staged_dataset_summary", None)
        st.session_state.pop("staged_dataset_validation", None)
        st.session_state.pop("staged_dataset_name", None)
        st.session_state.pop("staged_dataset_timestamp", None)
        st.session_state.pop("staged_dataset_registry_status", None)
        st.success("Staged dataset cleared. Default V2 dataset remains unchanged.")


def render_csv_upload_console() -> None:
    """Render safe CSV upload, validation, staging, and registry logging console."""

    st.divider()

    st.subheader("CSV Upload, Validation & Staging Console")

    st.info(
        """
This console is governed and safe.

Uploaded CSV files are previewed and validated in memory. When staged, the dataset is
stored only in the current Streamlit session for review and recorded in the persistent
Dataset Registry. It does **not** overwrite the current diabetes dataset, does **not**
retrain the model, and does **not** change the active ClariPulse™ V2 prediction pipeline.
"""
    )

    uploaded_file = st.file_uploader(
        "Upload a hospital analytics CSV file",
        type=["csv"],
    )

    render_staged_dataset_status()

    if uploaded_file is None:
        st.caption("Upload a CSV file to preview schema, quality, and compatibility.")
        return

    try:
        uploaded_df = pd.read_csv(uploaded_file)
        uploaded_df = uploaded_df.replace("?", pd.NA)

    except Exception as error:
        st.error(f"Unable to read uploaded CSV file: {error}")
        return

    summary = summarize_uploaded_csv(uploaded_df)
    validation = validate_uploaded_schema(
        uploaded_df,
        DIABETES_REQUIRED_COLUMNS,
    )

    render_metric_cards(
        [
            {"label": "Uploaded Rows", "value": summary["rows"]},
            {"label": "Uploaded Columns", "value": summary["columns"]},
            {"label": "Missing Values", "value": summary["missing_values"]},
            {"label": "Duplicate Rows", "value": summary["duplicate_rows"]},
        ]
    )

    schema_status = "Compatible" if validation["valid"] else "Review Required"

    render_metric_cards(
        [
            {"label": "Schema Status", "value": schema_status},
            {"label": "Required Columns", "value": len(DIABETES_REQUIRED_COLUMNS)},
            {
                "label": "Missing Required Columns",
                "value": len(validation["missing_columns"]),
            },
            {"label": "Mode", "value": "Staging Only"},
        ]
    )

    st.divider()

    st.subheader("Uploaded Data Preview")

    st.dataframe(
        uploaded_df.head(100),
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Column Profile")

    column_profile = pd.DataFrame(
        {
            "column": uploaded_df.columns,
            "dtype": [str(dtype) for dtype in uploaded_df.dtypes],
            "missing_count": uploaded_df.isna().sum().values,
            "missing_percent": (
                uploaded_df.isna().mean().values * 100
            ).round(2),
            "unique_values": uploaded_df.nunique(dropna=True).values,
        }
    )

    st.dataframe(
        column_profile,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Schema Compatibility Check")

    if validation["valid"]:
        st.success(
            """
The uploaded CSV contains the required columns for the current diabetes readmission
use case.

This confirms schema compatibility for exploration and staging. Production activation
and model retraining remain disabled.
"""
        )
    else:
        st.warning(
            "The uploaded CSV is missing one or more required columns. It may still be "
            "staged for governance review, but it is not compatible with the current "
            "diabetes readmission prediction schema."
        )

        missing_df = pd.DataFrame(
            {
                "missing_required_column": validation["missing_columns"],
            }
        )

        st.dataframe(
            missing_df,
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    st.subheader("Governed Dataset Staging")

    st.warning(
        """
Staging is not activation. A staged dataset is held only in the current session for
data review, governance assessment, and schema validation. It is also recorded in the
persistent Dataset Registry for audit visibility. It does not change the active model
or production dataset.
"""
    )

    if st.button("📥 Stage Uploaded Dataset for Governance Review", use_container_width=True):
        staged_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        st.session_state["staged_dataset"] = uploaded_df
        st.session_state["staged_dataset_summary"] = summary
        st.session_state["staged_dataset_validation"] = validation
        st.session_state["staged_dataset_name"] = uploaded_file.name
        st.session_state["staged_dataset_timestamp"] = staged_timestamp

        try:
            registry_record = register_staged_dataset_from_summary(
                dataset_name=uploaded_file.name,
                summary=summary,
                validation=validation,
            )

            st.session_state["staged_dataset_registry_status"] = "Recorded"

            st.success(
                "Uploaded dataset staged successfully and recorded in the Dataset Registry. "
                "Production dataset remains unchanged."
            )

            with st.expander("View Registry Record"):
                st.json(registry_record)

        except Exception as error:
            st.session_state["staged_dataset_registry_status"] = "Registry Error"

            st.warning(
                "Dataset was staged in the current session, but registry logging failed."
            )

            st.error(str(error))

    st.divider()

    st.subheader("Staging Safety Controls")

    safety_df = pd.DataFrame(
        {
            "Safety Control": [
                "Overwrite production dataset",
                "Retrain model automatically",
                "Change active Champion Model",
                "Change live prediction pipeline",
                "Store uploaded file permanently",
                "Record dataset in registry",
                "Allow governance staging",
            ],
            "Status": [
                "Disabled",
                "Disabled",
                "Disabled",
                "Disabled",
                "Disabled",
                "Enabled",
                "Enabled",
            ],
        }
    )

    st.dataframe(
        safety_df,
        use_container_width=True,
        hide_index=True,
    )


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

    render_csv_upload_console()

    st.divider()

    st.subheader("Ingestion Architecture")

    architecture = pd.DataFrame(
        {
            "Layer": [
                "Source Systems",
                "Connector Layer",
                "Validation Layer",
                "Staging Layer",
                "Registry Layer",
                "Feature Engineering",
                "AI Prediction Layer",
                "Governance Layer",
                "Executive Intelligence",
            ],
            "Description": [
                "CSV, SQL, FHIR, HL7, Epic, Cerner, OpenMRS",
                "Standardized connectors for structured healthcare data",
                "Schema checks, missingness review, quality validation",
                "Session-based governed staging for uploaded datasets",
                "Persistent dataset registry with audit-ready metadata",
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
architecture with governed dataset staging and persistent registry logging.

Current supported connectors include:

- CSV ingestion for hospital analytics exports
- SQL ingestion for structured healthcare databases
- Safe CSV upload, validation, preview, session-based staging, and registry recording

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