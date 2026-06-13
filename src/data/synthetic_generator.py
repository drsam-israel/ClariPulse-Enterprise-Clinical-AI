"""Enterprise synthetic data generator placeholder for ClariPulse™.

Milestone 1 provides a safe foundation command that writes core starter files.
The full 18-domain generator will replace this module in Milestone 2.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from src.data.sample_data import patient_queue, model_leaderboard, governance_summary
from src.utils.logger import get_logger

logger = get_logger(__name__)


def generate_foundation_data(output_dir: Path, patients: int = 10000) -> None:
    """Generate starter synthetic assets for the foundation application."""
    output_dir.mkdir(parents=True, exist_ok=True)
    patient_queue(min(patients, 1000)).to_csv(output_dir / "patient_queue.csv", index=False)
    model_leaderboard().to_csv(output_dir / "model_leaderboard.csv", index=False)
    governance_summary().to_csv(output_dir / "governance_summary.csv", index=False)
    logger.info("Foundation data generated in %s", output_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate ClariPulse foundation synthetic data.")
    parser.add_argument("--patients", type=int, default=10000, help="Number of synthetic patients requested.")
    parser.add_argument("--output", type=str, default="data/processed", help="Output directory.")
    args = parser.parse_args()
    generate_foundation_data(Path(args.output), args.patients)


if __name__ == "__main__":
    main()
