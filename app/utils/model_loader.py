"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product

Module:
    app.utils.model_loader

Purpose:
    Load enterprise model metadata.

Author:
    Samuel Israel, MD
===============================================================================
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_REGISTRY = PROJECT_ROOT / "models" / "model_registry.json"
TRAINING_METADATA = PROJECT_ROOT / "models" / "training_metadata.json"
BENCHMARK_RESULTS = PROJECT_ROOT / "reports" / "model_benchmark_results.csv"


def load_registry():

    if MODEL_REGISTRY.exists():

        with open(MODEL_REGISTRY) as f:
            return json.load(f)

    return {}


def load_training():

    if TRAINING_METADATA.exists():

        with open(TRAINING_METADATA) as f:
            return json.load(f)

    return {}


def load_benchmark():

    if BENCHMARK_RESULTS.exists():
        return pd.read_csv(BENCHMARK_RESULTS)

    return pd.DataFrame()