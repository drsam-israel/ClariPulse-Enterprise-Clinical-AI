"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: app.py
Purpose: Main Streamlit navigation entry point.
===============================================================================
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Final

import streamlit as st

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parent
SRC_PATH: Final[Path] = PROJECT_ROOT / "src"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from config.settings import APP_NAME, DEFAULT_PAGE_LAYOUT, DEFAULT_SIDEBAR


st.set_page_config(
    page_title=f"{APP_NAME} | Enterprise Clinical AI Product",
    page_icon="🏥",
    layout=DEFAULT_PAGE_LAYOUT,
    initial_sidebar_state=DEFAULT_SIDEBAR,
)

pages = {
    "ClariPulse™": [
        st.Page(
            "app/Home.py",
            title="Home",
            icon="🏠",
        ),
        st.Page(
            "app/pages/01_Executive_Command_Center.py",
            title="Executive Command Center",
            icon="🏛️",
        ),
        st.Page(
            "app/pages/02_Clinical_Intelligence.py",
            title="Clinical Intelligence",
            icon="🩺",
        ),
        st.Page(
            "app/pages/03_Patient_Explorer.py",
            title="Patient Explorer",
            icon="👤",
        ),
        st.Page(
            "app/pages/04_Explainability_Studio.py",
            title="Explainability Studio",
            icon="🔍",
        ),
        st.Page(
            "app/pages/05_Model_Benchmark_Center.py",
            title="Model Benchmark Center",
            icon="🏆",
        ),
        st.Page(
           "app/pages/06_Responsible_AI_Center.py",
            title="Responsible AI Center",
            icon="🛡️",
        ),
        st.Page(
           "app/pages/07_Reports_Exports.py",
            title="Reports & Exports",
            icon="📄",
        ),
        st.Page(
           "app/pages/08_Product_Intelligence_Center.py",
            title="Product Intelligence Center",
            icon="📊",
        ),
        st.Page(
            "app/pages/09_Data_Source_Manager.py",
            title="Data Source Manager",
            icon="🔌",
        ),
        st.Page(
           "app/pages/10_Dataset_Registry.py",
            title="Dataset Registry",
            icon="📚",
        ),
        st.Page(
           "app/pages/11_Dataset_Governance.py",
            title="Dataset Governance",
            icon="🛡️",
        )
    ]
}

navigation = st.navigation(pages)
navigation.run()