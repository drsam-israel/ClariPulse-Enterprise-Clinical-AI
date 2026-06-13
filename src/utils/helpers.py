"""General helper functions for ClariPulse™."""
from __future__ import annotations

from pathlib import Path
import pandas as pd


def safe_read_csv(path: Path) -> pd.DataFrame:
    """Read a CSV file safely and return an empty DataFrame if unavailable."""
    try:
        if path.exists():
            return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()
    return pd.DataFrame()


def format_percent(value: float) -> str:
    """Format a decimal or percentage-like number for executive display."""
    return f"{value:.1f}%"
