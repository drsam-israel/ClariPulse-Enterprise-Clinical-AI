"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Platform
Module: components.hero
Purpose: Reusable enterprise hero/banner component.
Author: Samuel Israel, MD
License: MIT
===============================================================================
"""

from __future__ import annotations

from html import escape
import streamlit as st


def render_hero(
    *,
    title: str,
    subtitle: str,
    description: str | None = None,
    height: str = "250px",
) -> None:
    """Render a reusable enterprise hero banner."""

    safe_title = escape(title)
    safe_subtitle = escape(subtitle)
    safe_description = escape(description or "")

    html = f"""
<style>
.claripulse-hero {{
    position: relative;
    background: linear-gradient(135deg, #0B2E4A 0%, #0F6B7A 100%);
    border-radius: 24px;
    padding: 40px 48px;
    min-height: {height};
    margin-bottom: 36px;
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 10px 30px rgba(0,0,0,.10);
}}

.claripulse-version-badge {{
    position: absolute;
    top: 24px;
    right: 28px;
    background: rgba(255,255,255,.18);
    border: 1px solid rgba(255,255,255,.28);
    padding: 7px 15px;
    border-radius: 999px;
    font-size: 14px;
    font-weight: 700;
    color: white;
}}

.claripulse-title {{
    font-size: 72px;
    font-weight: 800;
    letter-spacing: -2px;
    line-height: 1.0;
    margin-bottom: 18px;
    color: white;
}}

.claripulse-subtitle {{
    font-size: 26px;
    font-weight: 600;
    margin-bottom: 22px;
    color: rgba(255,255,255,.96);
}}

.claripulse-description {{
    font-size: 20px;
    line-height: 1.8;
    max-width: 1200px;
    color: rgba(255,255,255,.90);
}}
</style>

<div class="claripulse-hero">
    <div class="claripulse-version-badge">🏥 Enterprise Edition | v1.0</div>
    <div class="claripulse-title">{safe_title}</div>
    <div class="claripulse-subtitle">{safe_subtitle}</div>
    <div class="claripulse-description">{safe_description}</div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)