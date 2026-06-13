"""Logging utilities for ClariPulse™."""
from __future__ import annotations

import logging
from pathlib import Path


def get_logger(name: str) -> logging.Logger:
    """Create a configured logger for application modules."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(log_dir / "claripulse.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
