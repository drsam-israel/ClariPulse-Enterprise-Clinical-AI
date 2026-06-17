"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: app.Home
Purpose:
    Enterprise landing page for ClariPulse™ V2 Real-World Clinical AI Product.
Author: Samuel Israel, MD
Project: ClariPulse™
License: MIT
===============================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

from app.v2.services.v2_data_service import get_v2_product_status
from components.hero import render_hero
from components.metric_cards import render_metric_cards
from config.settings import APP_NAME, FOOTER_TEXT, TECH_STACK


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def inject_home_css() -> None:
    """Inject page-specific enterprise styling."""

    st.markdown(
        """
        <style>
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 3rem;
                max-width: 1500px;
            }

            h1, h2, h3 {
                letter-spacing: -0.02em;
            }

            .claripulse-alert {
                background: #E8F3FF;
                color: #004F9E;
                border-radius: 16px;
                padding: 22px 26px;
                margin: 28px 0 34px 0;
                font-size: 18px;
                line-height: 1.8;
            }

            .claripulse-footer {
                margin-top: 4rem;
                padding-top: 1.5rem;
                border-top: 1px solid #E5E7EB;
                color: #6B7280;
                font-size: 0.95rem;
            }

            .claripulse-section-note {
                color: #4B5563;
                font-size: 18px;
                line-height: 1.75;
                margin: 30px 0 24px 0;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_positioning() -> None:
    """Render V2 product positioning statement."""

    st.markdown(
        """
        <div class="claripulse-section-note">
            <strong>Enterprise Positioning:</strong> ClariPulse™ V2 is a real-world
            Clinical AI product for 30-day diabetes readmission intelligence,
            integrating predictive analytics, SHAP explainability, executive
            intelligence, model benchmarking, and Responsible AI governance into
            a unified enterprise decision support ecosystem.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_disclaimer() -> None:
    """Render clinical safety and demonstration disclaimer."""

    st.markdown(
        """
        <div class="claripulse-alert">
            <strong>Clinical AI demonstration notice:</strong>
            ClariPulse™ V2 uses a real-world de-identified diabetes readmission
            research dataset for portfolio, education, and product demonstration
            purposes. It is not a medical device and must not be used for real
            clinical decision-making.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_capabilities() -> None:
    """Render product capability cards without custom HTML dependency."""

    st.divider()
    st.subheader("Enterprise Product Capabilities")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("### Clinical AI")
            st.markdown("#### Real-World Readmission Intelligence")
            st.write(
                "Predicts 30-day diabetes readmission risk using real-world "
                "hospital encounter data and a governed ML pipeline."
            )

    with col2:
        with st.container(border=True):
            st.markdown("### Explainable AI")
            st.markdown("#### SHAP Transparency")
            st.write(
                "Provides global SHAP feature importance to support model "
                "interpretability, clinician trust, and governance review."
            )

    with col3:
        with st.container(border=True):
            st.markdown("### Responsible AI")
            st.markdown("#### Governance & Oversight")
            st.write(
                "Tracks model status, explainability readiness, governance evidence, "
                "auditability, and human oversight controls."
            )


def render_foundation_status() -> None:
    """Render V2 product foundation metrics."""

    status = get_v2_product_status()

    st.divider()
    st.subheader("Product Foundation Status")

    render_metric_cards(
        [
            {"label": "Product Version", "value": status["version"]},
            {"label": "Data Status", "value": "Real-World Dataset"},
            {"label": "Model Status", "value": status["status"]},
            {"label": "Governance", "value": "Ready"},
        ]
    )


def render_executive_kpis() -> None:
    """Render V2 executive product KPI cards below the hero."""

    status = get_v2_product_status()

    render_metric_cards(
        [
            {"label": "Dataset Encounters", "value": status["dataset_rows"]},
            {"label": "Unique Patients", "value": status["unique_patients"]},
            {
                "label": "30-Day Readmission Rate",
                "value": f'{status["readmission_30day_rate"]}%',
            },
            {"label": "Champion Model", "value": status["champion_model"]},
        ]
    )

    render_metric_cards(
        [
            {"label": "Cross-Val AUC", "value": status["cv_auc"]},
            {"label": "Test AUC", "value": status["test_auc"]},
            {"label": "Models Benchmarked", "value": status["models_benchmarked"]},
            {"label": "SHAP Features", "value": status["shap_features"]},
        ]
    )


def render_technology_stack() -> None:
    """Render technology stack section."""

    st.divider()
    st.subheader("Technology Stack")
    st.write(" • ".join(TECH_STACK))


def render_next_steps() -> None:
    """Render V2 strategic roadmap."""

    st.divider()
    st.subheader("Strategic V2 Roadmap")

    st.markdown(
        """
        1. Expand real-world readmission intelligence across additional clinical cohorts.
        2. Add CSV and SQL ingestion connectors for hospital analytics teams.
        3. Design HL7/FHIR interoperability layer for EHR-ready integration.
        4. Implement advanced model monitoring for drift, calibration, and fairness.
        5. Prepare enterprise deployment pathway for Epic, Cerner, and OpenMRS ecosystems.
        """
    )


def render_footer() -> None:
    """Render footer."""

    st.markdown(
        f"""
        <div class="claripulse-footer">
            {FOOTER_TEXT}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_home() -> None:
    """Render the ClariPulse™ V2 landing page."""

    inject_home_css()

    render_hero(
        title=APP_NAME,
        subtitle="Enterprise Clinical AI Product V2",
        description=(
            "Real-World Diabetes Readmission Intelligence • SHAP Explainability • "
            "Responsible AI Governance • Executive Decision Support"
        ),
    )

    render_executive_kpis()
    render_positioning()
    render_capabilities()
    render_disclaimer()
    render_foundation_status()
    render_technology_stack()
    render_next_steps()
    render_footer()


render_home()