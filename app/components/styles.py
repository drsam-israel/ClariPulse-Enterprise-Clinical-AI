"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product

Module:
    app.components.styles

Purpose:
    Global CSS styling utilities used across all pages.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

import streamlit as st


def load_global_styles() -> None:
    """
    Load global ClariPulse™ CSS styles.
    """

    st.markdown(
        """
        <style>

        .main {
            background-color: #F6F8FA;
        }

        .claripulse-title {
            font-size: 48px;
            font-weight: 700;
            color: #0B2E4A;
            margin-bottom: 0;
        }

        .claripulse-subtitle {
            font-size: 20px;
            color: #64748B;
            margin-top: 0;
        }

        .section-title {
            font-size: 28px;
            font-weight: 700;
            color: #0B2E4A;
            margin-top: 30px;
            margin-bottom: 15px;
        }

        .executive-card {

            background: white;

            border-radius: 16px;

            padding: 1.25rem;

            border: 1px solid #E2E8F0;

            box-shadow: 0 2px 8px rgba(0,0,0,0.05);

        }

        .footer-text {

            text-align: center;

            color: gray;

            font-size: 14px;

            margin-top: 40px;

        }

        </style>
        """,
        unsafe_allow_html=True,
    )