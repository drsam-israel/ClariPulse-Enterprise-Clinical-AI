"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Platform
Module: components.metric_cards
Purpose: Reusable executive KPI metric cards.
Author: Samuel Israel, MD
License: MIT
===============================================================================
"""

from __future__ import annotations

from html import escape

import streamlit as st


def _get_value_font_size(value: str) -> str:
    """Return font size based on metric value content."""
    value = value.strip()

    if value == "1.0.0":
        return "38px"

    if value in {"Not Generated", "Not Trained", "Foundation Ready"}:
        return "16px"

    if len(value) <= 6:
        return "32px"

    if len(value) <= 12:
        return "22px"

    return "18px"


def render_metric_cards(metrics: list[dict[str, str]]) -> None:
    """Render enterprise KPI metric cards."""

    if not metrics:
        return

    st.markdown(
        """
<style>
.claripulse-metric-card{
    background:#FFFFFF;
    border:1px solid #E5E7EB;
    border-radius:18px;
    padding:22px;
    min-height:140px;
    text-align:center;
    box-shadow:0 6px 18px rgba(15,23,42,.05);
    transition:all .2s ease;
    display:flex;
    flex-direction:column;
    justify-content:center;
}

.claripulse-metric-card:hover{
    transform:translateY(-2px);
    box-shadow:0 10px 28px rgba(15,23,42,.10);
}

.claripulse-metric-label{
    color:#6B7280;
    font-size:14px;
    font-weight:700;
    margin-bottom:12px;
}

.claripulse-metric-value{
    color:#0B2E4A;
    font-weight:800;
    line-height:1.15;
    white-space:normal;
    word-break:break-word;
    text-align:center;
}
</style>
""",
        unsafe_allow_html=True,
    )

    cols = st.columns(len(metrics))

    for col, metric in zip(cols, metrics):
        with col:
            label = escape(str(metric.get("label", "")))
            value = escape(str(metric.get("value", "")))
            font_size = _get_value_font_size(value)

            st.markdown(
                f"""
<div class="claripulse-metric-card">
    <div class="claripulse-metric-label">{label}</div>
    <div class="claripulse-metric-value" style="font-size:{font_size};">{value}</div>
</div>
""",
                unsafe_allow_html=True,
            )