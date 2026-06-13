"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: src.reference.executive_config

Purpose:
    Executive dashboard configuration and KPI thresholds.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations


# =============================================================================
# EXECUTIVE THRESHOLDS
# =============================================================================

CRITICAL_RISK_ALERT_THRESHOLD = 0.05

HUMAN_REVIEW_ALERT_THRESHOLD = 500


# =============================================================================
# DEFAULT GOVERNANCE STATUS
# =============================================================================

DEFAULT_GOVERNANCE_STATUS = "Operational"


# =============================================================================
# EXECUTIVE RECOMMENDATIONS
# =============================================================================

NORMAL_RECOMMENDATION = (
    "Clinical AI system operating within acceptable governance thresholds. "
    "Continue routine monitoring."
)

ALERT_RECOMMENDATION = (
    "Immediate executive review recommended. Increase clinical oversight, "
    "prioritize critical-risk patients, and review AI governance metrics."
)