"""Sample/demo data utilities for the ClariPulse™ foundation build.

This module intentionally provides lightweight synthetic data so the foundation
application is useful immediately before the full 18-domain generator is added.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def executive_kpis() -> dict[str, float | int]:
    """Return deterministic executive KPI examples for foundation dashboards."""
    return {
        "patients_monitored": 10000,
        "active_encounters": 1284,
        "high_risk_patients": 312,
        "avg_los": 5.2,
        "readmission_rate": 9.8,
        "governance_compliance": 100.0,
    }


def patient_queue(n: int = 25) -> pd.DataFrame:
    """Create a deterministic synthetic high-risk patient queue."""
    rng = np.random.default_rng(42)
    data = {
        "patient_id": [f"PAT-{100000+i}" for i in range(n)],
        "age": rng.integers(28, 92, n),
        "department": rng.choice(["ICU", "Emergency", "Cardiology", "Internal Medicine"], n),
        "prediction_type": rng.choice(["Mortality", "Sepsis", "Readmission", "ICU Transfer"], n),
        "risk_score": np.round(rng.uniform(35, 96, n), 1),
        "risk_category": [],
    }
    for score in data["risk_score"]:
        if score >= 75:
            data["risk_category"].append("Critical")
        elif score >= 50:
            data["risk_category"].append("High")
        else:
            data["risk_category"].append("Moderate")
    return pd.DataFrame(data).sort_values("risk_score", ascending=False)


def model_leaderboard() -> pd.DataFrame:
    """Return benchmark leaderboard for foundation display."""
    return pd.DataFrame(
        [
            ["XGBoost", 0.931, 0.902, 0.895, 0.043, 142, "Champion"],
            ["LightGBM", 0.926, 0.894, 0.889, 0.046, 118, "Challenger"],
            ["Random Forest", 0.911, 0.876, 0.871, 0.052, 220, "Challenger"],
            ["Decision Tree", 0.842, 0.801, 0.792, 0.071, 38, "Baseline"],
            ["Logistic Regression", 0.881, 0.852, 0.846, 0.059, 35, "Clinical Baseline"],
        ],
        columns=["model", "roc_auc", "recall", "f1_score", "brier_score", "latency_ms", "status"],
    )


def governance_summary() -> pd.DataFrame:
    """Return responsible AI governance sample metrics."""
    return pd.DataFrame(
        {
            "governance_dimension": ["Bias Review", "Explainability", "Drift Monitoring", "Model Cards", "Human Review"],
            "completion_rate": [100, 100, 96, 100, 92],
            "status": ["Complete", "Complete", "Monitoring", "Complete", "Active"],
        }
    )
