"""Foundation model benchmarking command for ClariPulse™.

Milestone 1 writes a governance-ready sample leaderboard. Milestone 3 will
replace this with real five-model training and stratified cross-validation.
"""
from __future__ import annotations

from pathlib import Path
from src.data.sample_data import model_leaderboard
from src.utils.logger import get_logger

logger = get_logger(__name__)


def main() -> None:
    output_dir = Path("data/analytics")
    output_dir.mkdir(parents=True, exist_ok=True)
    leaderboard = model_leaderboard()
    leaderboard.to_csv(output_dir / "model_leaderboard.csv", index=False)
    logger.info("Model benchmark leaderboard generated: %s", output_dir / "model_leaderboard.csv")


if __name__ == "__main__":
    main()
