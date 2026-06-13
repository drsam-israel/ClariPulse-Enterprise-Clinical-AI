"""Model registry helpers for ClariPulse™."""
from __future__ import annotations

import pandas as pd
from src.data.sample_data import model_leaderboard


def get_model_registry() -> pd.DataFrame:
    """Return model registry view derived from current leaderboard."""
    registry = model_leaderboard().copy()
    registry["model_id"] = [f"MODEL-{i+1:03d}" for i in range(len(registry))]
    registry["approval_status"] = ["Approved" if s == "Champion" else "Under Review" for s in registry["status"]]
    registry["monitoring_status"] = "Active"
    return registry
