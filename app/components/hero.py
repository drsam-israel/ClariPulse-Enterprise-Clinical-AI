"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product

Module:
    app.components.hero

Purpose:
    Reusable Hero Banner for all ClariPulse™ pages.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations

import streamlit as st


def render_hero(
    title: str,
    subtitle: str,
    description: str,
    version: str = "Enterprise v1.0",
) -> None:
    """Render enterprise hero banner."""

    html = (
        '<div style="background: linear-gradient(90deg,#0B2E4A,#0F6B7A); '
        'padding:36px; border-radius:18px; margin-bottom:28px;">'
        '<div style="display:flex; justify-content:space-between; '
        'align-items:flex-start; gap:24px;">'
        '<div>'
        '<div style="color:white; font-size:18px; font-weight:600; margin-bottom:10px;">'
        '🏥 ClariPulse™'
        '</div>'
        f'<div style="color:white; font-size:46px; font-weight:700; line-height:1.2;">{title}</div>'
        f'<div style="color:#D7F3F7; font-size:22px; margin-top:8px;">{subtitle}</div>'
        f'<div style="color:white; font-size:18px; margin-top:18px;">{description}</div>'
        '</div>'
        '<div style="background:white; color:#0B2E4A; padding:10px 20px; '
        'border-radius:999px; font-size:16px; font-weight:700; white-space:nowrap;">'
        f'{version}'
        '</div>'
        '</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)