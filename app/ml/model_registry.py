"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product

Module:
    app.ml.model_registry

Purpose:
    Register benchmark results and champion model metadata.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pandas as pd


# -----------------------------------------------------------------------------
# Project paths
# -----------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

REPORT_PATH = PROJECT_ROOT / "reports" / "model_benchmark_results.csv"
REGISTRY_PATH = PROJECT_ROOT / "models" / "model_registry.json"


# -----------------------------------------------------------------------------
# Model Registry Builder
# -----------------------------------------------------------------------------

def create_registry() -> None:
    """Create the enterprise model registry."""

    if not REPORT_PATH.exists():
        raise FileNotFoundError(
            f"Benchmark results not found:\n{REPORT_PATH}"
        )

    df = pd.read_csv(REPORT_PATH)

    # Select champion model by highest AUC
    champion = df.sort_values(by="auc", ascending=False).iloc[0]

    registry = {
        "created_at": datetime.now().isoformat(),
        "product": "ClariPulse™",
        "version": "1.0.0",
        "status": "Approved",
        "champion_model": champion["model"],
        "accuracy": float(champion["accuracy"]),
        "precision": float(champion["precision"]),
        "recall": float(champion["recall"]),
        "f1": float(champion["f1"]),
        "auc": float(champion["auc"]),
    }

    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=4)

    print("\n✅ Enterprise Model Registry Created Successfully")
    print(f"📄 Saved to: {REGISTRY_PATH}")


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    create_registry()