"""Reusable Streamlit UI components for ClariPulse™."""
from __future__ import annotations

import streamlit as st
from src.utils.constants import PRODUCT_NAME, PRODUCT_CATEGORY, TAGLINE, DEVELOPER_FOOTER


def apply_page_config(title: str = PRODUCT_NAME) -> None:
    """Apply consistent Streamlit page configuration and theme styling."""
    st.set_page_config(page_title=f"{title} | ClariPulse", page_icon="🩺", layout="wide")
    st.markdown(
        """
        <style>
        .block-container {padding-top: 2rem; padding-bottom: 2rem; max-width: 1280px;}
        .cp-hero {background: linear-gradient(135deg, #0B2F4A 0%, #0F5D75 100%); padding: 3rem 2.5rem; border-radius: 1.25rem; color: white; margin-bottom: 1.5rem;}
        .cp-hero h1 {font-size: 3.2rem; margin-bottom: 0.5rem; font-weight: 800;}
        .cp-hero p {font-size: 1.2rem; opacity: .95;}
        .cp-card {background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 1rem; padding: 1.35rem; box-shadow: 0 6px 22px rgba(15, 93, 117, 0.07); min-height: 155px;}
        .cp-card h3 {margin-top:0; color:#0B2F4A;}
        .cp-info {background:#E8F3FF; color:#0057A8; border-radius:.75rem; padding:1rem 1.25rem; margin: 1rem 0;}
        .cp-warning {background:#FFF8D6; color:#8A6500; border-radius:.75rem; padding:1rem 1.25rem; margin: 1rem 0;}
        .cp-footer {font-size:.9rem; color:#6B7280; border-top:1px solid #E5E7EB; padding-top:1rem; margin-top:2rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str) -> None:
    """Render a consistent enterprise hero banner."""
    st.markdown(
        f"""
        <div class="cp-hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def product_disclaimer() -> None:
    """Render product safety and demonstration disclaimer."""
    st.markdown(
        """
        <div class="cp-info">
        <strong>ClariPulse™ demonstration notice:</strong> This product uses fully synthetic data for portfolio, education, and product demonstration purposes. It is not a medical device and must not be used for real clinical decision-making.
        </div>
        """,
        unsafe_allow_html=True,
    )


def capability_card(title: str, body: str) -> None:
    """Render a reusable capability card."""
    st.markdown(f"<div class='cp-card'><h3>{title}</h3><p>{body}</p></div>", unsafe_allow_html=True)


def metric_row(metrics: list[tuple[str, str, str]]) -> None:
    """Render a row of Streamlit metric cards."""
    cols = st.columns(len(metrics))
    for col, (label, value, delta) in zip(cols, metrics):
        col.metric(label, value, delta)


def footer() -> None:
    """Render a consistent product footer."""
    st.markdown(f"<div class='cp-footer'>{DEVELOPER_FOOTER}</div>", unsafe_allow_html=True)
