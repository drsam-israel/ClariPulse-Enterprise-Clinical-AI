"""
===============================================================================
ClariPulse™
Clinical Intelligence Center
===============================================================================
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from components.hero import render_hero
from components.metric_cards import render_metric_cards


def render_page():

    render_hero(
        title="Clinical Intelligence",
        subtitle="AI-powered patient risk stratification",
        description=(
            "Mortality • Readmission • Sepsis • ICU Transfer • "
            "Length of Stay Prediction"
        ),
    )

    render_metric_cards(
        [
            {"label": "High-Risk Patients", "value": "14.2%"},
            {"label": "Mortality Risk", "value": "3.8%"},
            {"label": "Readmission Risk", "value": "11.1%"},
            {"label": "Sepsis Alerts", "value": "312"},
        ]
    )

    st.divider()

    st.subheader("Population Risk Distribution")

    df = pd.DataFrame(
        {
            "Risk": ["Low", "Moderate", "High", "Critical"],
            "Patients": [52000, 33800, 11200, 3000],
        }
    )

    fig = px.bar(
        df,
        x="Risk",
        y="Patients",
        text="Patients",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Clinical Summary")

    st.info(
        """
High-risk patients are concentrated among elderly populations with
multiple chronic diseases.

Primary drivers include:

• Advanced age

• Chronic kidney disease

• Diabetes

• Elevated lactate

• Emergency admission

Recommended intervention:
prioritize care coordination and early escalation.
"""
    )


render_page()