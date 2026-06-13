"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Product
Module: src.reference.governance_config

Purpose:
    Central configuration for AI governance logging.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations


# =============================================================================
# DEFAULT REVIEWER
# =============================================================================

DEFAULT_REVIEWER = "Clinical AI Governance Committee"


# =============================================================================
# DEFAULT GOVERNANCE STATUS
# =============================================================================

BIAS_CHECK_STATUS = "Passed"

DRIFT_CHECK_STATUS = "Stable"

EXPLAINABILITY_STATUS = "Available"

MODEL_APPROVAL_STATUS = "Approved"


# =============================================================================
# REVIEW THRESHOLDS
# =============================================================================

HIGH_RISK_THRESHOLD = 0.75

CRITICAL_RISK_THRESHOLD = 0.90


# =============================================================================
# HUMAN REVIEW POLICY
# =============================================================================

REQUIRE_HUMAN_REVIEW_FOR_CRITICAL = True