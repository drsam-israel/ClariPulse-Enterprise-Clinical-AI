"""Navigation definitions for ClariPulse™."""
from __future__ import annotations

from src.utils.constants import NAV_ITEMS


def get_navigation_items() -> list[tuple[str, str, str]]:
    """Return product navigation items."""
    return NAV_ITEMS
