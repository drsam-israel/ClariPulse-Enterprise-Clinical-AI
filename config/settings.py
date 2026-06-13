"""
===============================================================================
ClariPulse™ Enterprise Clinical AI Platform

Module: config.settings

Purpose:
    Central application configuration for the ClariPulse™ platform.

Author:
    Samuel Israel, MD

License:
    MIT

===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


# =============================================================================
# PROJECT ROOT
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

APP_DIR = PROJECT_ROOT / "app"
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
ANALYTICS_DATA_DIR = DATA_DIR / "analytics"

REPORTS_DIR = PROJECT_ROOT / "reports"
EXPORTS_DIR = PROJECT_ROOT / "exports"
MODELS_DIR = PROJECT_ROOT / "models"
LOGS_DIR = PROJECT_ROOT / "logs"
ASSETS_DIR = PROJECT_ROOT / "assets"
DOCS_DIR = PROJECT_ROOT / "docs"

CACHE_DIR = PROJECT_ROOT / "cache"
MLRUNS_DIR = PROJECT_ROOT / "mlruns"


# =============================================================================
# CREATE DIRECTORIES AUTOMATICALLY
# =============================================================================

DIRECTORIES = [

    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    ANALYTICS_DATA_DIR,

    REPORTS_DIR,
    EXPORTS_DIR,

    MODELS_DIR,

    LOGS_DIR,

    CACHE_DIR,

    MLRUNS_DIR,

]

for directory in DIRECTORIES:
    directory.mkdir(parents=True, exist_ok=True)


# =============================================================================
# APPLICATION METADATA
# =============================================================================

APP_NAME = "ClariPulse™"

APP_SHORT_NAME = "ClariPulse"

APP_VERSION = "1.0.0"

APP_STATUS = "Development"

ORGANIZATION = "Samuel Israel"

PRODUCT_TYPE = "Enterprise Clinical AI Platform"

ENVIRONMENT = "Local Development"

DEBUG_MODE = True


# =============================================================================
# SYNTHETIC DATA CONFIGURATION
# =============================================================================

DEFAULT_PATIENT_COUNT = 100_000

DEFAULT_RANDOM_SEED = 42

DEFAULT_POSITIVE_CLASS_RATE = 0.18


# =============================================================================
# MACHINE LEARNING CONFIGURATION
# =============================================================================

TARGET_COLUMN = "mortality"

TEST_SIZE = 0.20

NUMBER_OF_FOLDS = 5

RANDOM_STATE = 42

BENCHMARK_MODELS = [

    "Logistic Regression",

    "Decision Tree",

    "Random Forest",

    "XGBoost",

    "LightGBM",

]


# =============================================================================
# EXPORT SETTINGS
# =============================================================================

ENABLE_CSV_EXPORT = True

ENABLE_EXCEL_EXPORT = True

ENABLE_PDF_EXPORT = True


# =============================================================================
# RESPONSIBLE AI
# =============================================================================

ENABLE_SHAP = True

ENABLE_BIAS_MONITORING = True

ENABLE_DRIFT_MONITORING = True

ENABLE_MODEL_REGISTRY = True


# =============================================================================
# DASHBOARD SETTINGS
# =============================================================================

DEFAULT_PAGE_LAYOUT = "wide"

DEFAULT_SIDEBAR = "expanded"


# =============================================================================
# ENTERPRISE COLORS
# =============================================================================

@dataclass(frozen=True)
class EnterpriseColors:

    NAVY: str = "#0B2E4A"

    TEAL: str = "#0F6B7A"

    BLUE: str = "#2F80ED"

    GREEN: str = "#27AE60"

    ORANGE: str = "#F2994A"

    RED: str = "#EB5757"

    BACKGROUND: str = "#F8FAFC"

    CARD: str = "#FFFFFF"

    BORDER: str = "#E5E7EB"

    TEXT: str = "#1F2937"


COLORS = EnterpriseColors()


# =============================================================================
# KPI LABELS
# =============================================================================

KPI_LABELS = {

    "patients": "Patients",

    "mortality": "Mortality Risk",

    "readmission": "Readmission Risk",

    "los": "Length of Stay",

    "icu": "ICU Transfer Risk",

    "sepsis": "Sepsis Risk",

}


# =============================================================================
# TECHNOLOGY STACK
# =============================================================================

TECH_STACK = [

    "Python",

    "Streamlit",

    "Pandas",

    "NumPy",

    "Scikit-learn",

    "XGBoost",

    "LightGBM",

    "SHAP",

    "Plotly",

]


# =============================================================================
# FOOTER
# =============================================================================

FOOTER_TEXT = (

    "Developed by Samuel Israel, MD | "

    "Master of Information Technology (AI Specialization) | "

    "ClariPulse™ Enterprise Clinical AI Platform"

)