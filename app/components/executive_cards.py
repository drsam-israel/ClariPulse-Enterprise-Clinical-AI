"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product

Module:
    app.components.executive_cards

Purpose:
    Reusable executive capability card grid component.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

import streamlit as st


def render_card_grid(cards: list[dict], columns: int = 3) -> None:
    """Render a grid of executive capability cards."""

    cols = st.columns(columns)

    for index, card in enumerate(cards):
        with cols[index % columns]:
            html = (
                '<div style="background:white; border-radius:16px; padding:1.25rem; '
                'border:1px solid #E2E8F0; box-shadow:0 2px 8px rgba(0,0,0,0.05); '
                'min-height:230px;">'
                '<div style="display:inline-block; background:#E0F2FE; color:#0B2E4A; '
                'padding:6px 12px; border-radius:999px; font-size:13px; '
                'font-weight:700; margin-bottom:12px;">'
                f'{card.get("badge", "Capability")}</div>'
                f'<h3 style="color:#0B2E4A; margin-bottom:10px;">{card.get("title", "")}</h3>'
                f'<p style="color:#64748B; font-size:16px; line-height:1.6;">{card.get("description", "")}</p>'
                '</div>'
            )

            st.markdown(html, unsafe_allow_html=True)