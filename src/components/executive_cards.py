"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Platform
Module: components.executive_cards
Purpose:
    Reusable executive card components for ClariPulse™ pages.
Author: Samuel Israel, MD
License: MIT
===============================================================================
"""

from __future__ import annotations

from html import escape

import streamlit as st


def render_card_grid(cards: list[dict[str, str]], columns: int = 3) -> None:
    """Render a responsive grid of enterprise cards."""
    if not cards:
        return

    cols = st.columns(columns)

    for index, card in enumerate(cards):
        with cols[index % columns]:
            render_executive_card(
                title=card.get("title", ""),
                description=card.get("description", ""),
                badge=card.get("badge"),
            )


def render_executive_card(
    *,
    title: str,
    description: str,
    badge: str | None = None,
) -> None:
    """Render a single reusable executive card."""
    safe_title = escape(title)
    safe_description = escape(description)
    safe_badge = escape(badge or "")

    badge_html = (
        f'<div class="claripulse-card-badge">{safe_badge}</div>'
        if safe_badge
        else ""
    )

    st.markdown(
        f"""
        <style>
            .claripulse-card {{
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 18px;
                padding: 28px;
                min-height: 210px;
                box-shadow: 0 8px 26px rgba(15, 23, 42, 0.06);
                margin-bottom: 22px;
            }}

            .claripulse-card:hover {{
                box-shadow: 0 14px 34px rgba(15, 23, 42, 0.10);
                transform: translateY(-2px);
                transition: all 0.2s ease-in-out;
            }}

            .claripulse-card-badge {{
                display: inline-block;
                background: #E8F3FF;
                color: #0057A8;
                border-radius: 999px;
                padding: 6px 12px;
                font-size: 13px;
                font-weight: 700;
                margin-bottom: 16px;
            }}

            .claripulse-card-title {{
                font-size: 28px;
                font-weight: 800;
                color: #1F2937;
                margin-bottom: 14px;
                line-height: 1.25;
            }}

            .claripulse-card-description {{
                font-size: 17px;
                color: #4B5563;
                line-height: 1.7;
            }}
        </style>

        <div class="claripulse-card">
            {badge_html}
            <div class="claripulse-card-title">{safe_title}</div>
            <div class="claripulse-card-description">{safe_description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )