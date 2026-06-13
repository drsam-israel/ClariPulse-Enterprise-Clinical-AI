"""Session state helpers for ClariPulse™."""
from __future__ import annotations

import streamlit as st


def init_session() -> None:
    """Initialize application session defaults."""
    st.session_state.setdefault("product_version", "1.0.0-foundation")
