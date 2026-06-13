"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: src.reference.prediction_config

Purpose:
    Central configuration for the Explainable Clinical Rules Engine.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations


# =============================================================================
# MODEL METADATA
# =============================================================================

CHAMPION_MODEL = "XGBoost_v1.0"

MODEL_VERSION = "1.0.0"

MODEL_TYPE = "Rules-Based Clinical Engine"


# =============================================================================
# RISK CATEGORY THRESHOLDS
# =============================================================================

LOW_THRESHOLD = 0.25

MODERATE_THRESHOLD = 0.50

HIGH_THRESHOLD = 0.75


# =============================================================================
# HUMAN REVIEW THRESHOLD
# =============================================================================

HUMAN_REVIEW_THRESHOLD = 0.80


# =============================================================================
# PREDICTION STATUS
# =============================================================================

DEFAULT_STATUS = "Success"