"""Configuration utilities for ClariPulse™."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class AppConfig:
    """Application configuration resolved from environment variables."""

    environment: str = os.getenv("CLARIPULSE_ENV", "development")
    root_dir: Path = Path(__file__).resolve().parents[2]
    data_dir: Path = root_dir / "data"
    processed_data_dir: Path = root_dir / "data" / "processed"
    analytics_data_dir: Path = root_dir / "data" / "analytics"
    exports_dir: Path = root_dir / "data" / "exports"
    model_dir: Path = root_dir / "models"
    reports_dir: Path = root_dir / "reports"


def get_config() -> AppConfig:
    """Return immutable application configuration."""
    return AppConfig()
