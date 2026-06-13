"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: app.Home
Purpose:
    Enterprise landing page for ClariPulse™.
Author: Samuel Israel, MD
Project: ClariPulse™
License: MIT
===============================================================================
"""

from __future__ import annotations

import streamlit as st

import sys
from pathlib import Path

from app.services.data_service import get_product_status

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from config.settings import APP_NAME, APP_VERSION, FOOTER_TEXT, TECH_STACK
from components.executive_cards import render_card_grid
from components.hero import render_hero
from components.metric_cards import render_metric_cards


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
    """Render product positioning statement."""
    st.markdown(
        """
        <div class="claripulse-section-note">
            <strong>Enterprise Positioning:</strong> ClariPulse™ is a next-generation
            Clinical AI platform that unifies predictive analytics, explainable AI,
            executive intelligence, and responsible AI governance into a single,
            enterprise-grade decision support ecosystem for healthcare organizations.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_disclaimer() -> None:
    """Render clinical safety and demonstration disclaimer."""
    st.markdown(
        """
        <div class="claripulse-alert">
            <strong>ClariPulse™ demonstration notice:</strong>
            This product uses fully synthetic data for portfolio, education, and product
            demonstration purposes. It is not a medical device and must not be used for
            real clinical decision-making.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_capabilities() -> None:
    """Render product capability cards."""
    st.subheader("Enterprise Product Capabilities")

    cards = [
        {
            "badge": "Clinical AI",
            "title": "Predictive Clinical Intelligence",
            "description": (
                "Risk prediction for mortality, readmission, sepsis, ICU transfer, "
                "and length of stay using a governed multi-model pipeline."
            ),
        },
        {
            "badge": "XAI",
            "title": "Explainable AI",
            "description": (
                "SHAP-based local and global explanations with clinician-friendly "
                "interpretation and executive summaries."
            ),
        },
        {
            "badge": "Governance",
            "title": "Responsible AI Governance",
            "description": (
                "Model registry, bias monitoring, drift tracking, auditability, "
                "human oversight, and governance-ready evidence."
            ),
        },
    ]

    render_card_grid(cards, columns=3)


def render_foundation_status() -> None:
    """Render product foundation metrics."""
    st.divider()
    st.subheader("Product Foundation Status")

    render_metric_cards(
        [
            {"label": "Product Version", "value": APP_VERSION},
            {"label": "Data Status", "value": st.session_state.get("data_status", "Ready")},
            {"label": "Model Status", "value": st.session_state.get("model_status","Not Trained")},
            {"label": "Governance", "value": st.session_state.get("governance_status", "Ready")},
        ]
    )


def render_executive_kpis() -> None:
    """Render executive product KPI cards below the hero using live product status."""

    status = get_product_status()

    render_metric_cards(
        [
            {"label": "Patients Analysed", "value": "100,000"},
            {"label": "Champion AUC", "value": status["champion_auc"]},
            {"label": "Models Registered", "value": status["models_benchmarked"]},
            {"label": "SHAP Coverage", "value": "100%"},
        ]
    )

def render_technology_stack() -> None:
    """Render technology stack section."""
    st.divider()
    st.subheader("Technology Stack")
    st.write(" • ".join(TECH_STACK))


def render_next_steps() -> None:
    """Render recommended build sequence."""
    st.divider()
    st.subheader("Recommended Next Build Steps")

    st.markdown(
        """
        1. Generate the enterprise synthetic healthcare dataset.
        2. Build five-model benchmarking with Stratified 5-Fold Cross-Validation.
        3. Select the Champion model and register all candidate models.
        4. Generate SHAP explainability outputs.
        5. Populate executive, clinical, governance, and product intelligence dashboards.
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
    """Render the ClariPulse™ landing page."""
    inject_home_css()

    render_hero(
        title=APP_NAME,
        subtitle="Enterprise Clinical AI Product",
        description=(
            "Predictive Analytics • Explainable AI • Executive Intelligence • "
            "Responsible AI Governance"
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