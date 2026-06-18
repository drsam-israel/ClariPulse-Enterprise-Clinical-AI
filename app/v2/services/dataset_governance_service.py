"""
===============================================================================
ClariPulse™ V2 - Dataset Governance Service

Purpose:
    Read-only dataset governance service for registry-driven governance KPIs,
    compliance posture, pending review tracking, and audit readiness.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.v2.services.dataset_registry_service import load_dataset_registry


PROJECT_ROOT = Path(__file__).resolve().parents[3]

REPORT_DIR = PROJECT_ROOT / "reports" / "v2"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

GOVERNANCE_LOG_PATH = REPORT_DIR / "governance_log.csv"

GOVERNANCE_COLUMNS = [
    "dataset_name",
    "governance_status",
    "reviewer",
    "decision_date",
    "comments",
]


def initialize_governance_log() -> None:
    """Create governance log if it does not exist."""

    if not GOVERNANCE_LOG_PATH.exists():
        pd.DataFrame(columns=GOVERNANCE_COLUMNS).to_csv(
            GOVERNANCE_LOG_PATH,
            index=False,
        )


def load_governance_log() -> pd.DataFrame:
    """Load governance log safely."""

    initialize_governance_log()

    log = pd.read_csv(GOVERNANCE_LOG_PATH)

    for column in GOVERNANCE_COLUMNS:
        if column not in log.columns:
            log[column] = pd.NA

    return log[GOVERNANCE_COLUMNS]


def build_governance_view() -> pd.DataFrame:
    """Build read-only governance view from dataset registry and governance log."""

    registry = load_dataset_registry()
    log = load_governance_log()

    if registry.empty:
        return pd.DataFrame()

    governance = registry.copy()

    if not log.empty:
        latest_log = (
            log.sort_values("decision_date")
            .drop_duplicates(subset=["dataset_name"], keep="last")
        )

        governance = governance.merge(
            latest_log,
            on="dataset_name",
            how="left",
        )
    else:
        governance["governance_status"] = pd.NA
        governance["reviewer"] = pd.NA
        governance["decision_date"] = pd.NA
        governance["comments"] = pd.NA

    governance["governance_status"] = governance["governance_status"].fillna(
        governance["status"].apply(
            lambda status: "Approved"
            if status == "Production"
            else "Pending Review"
        )
    )

    governance["reviewer"] = governance["reviewer"].fillna(
        governance["status"].apply(
            lambda status: "System"
            if status == "Production"
            else "Pending"
        )
    )

    governance["decision_date"] = governance["decision_date"].fillna("Pending")
    governance["comments"] = governance["comments"].fillna(
        governance["status"].apply(
            lambda status: "Default production dataset"
            if status == "Production"
            else "Awaiting governance review"
        )
    )

    return governance


def get_governance_summary() -> dict:
    """Return governance KPIs."""

    governance = build_governance_view()

    if governance.empty:
        return {
            "total_datasets": 0,
            "approved": 0,
            "pending_review": 0,
            "rejected": 0,
            "compliance_rate": "N/A",
        }

    approved = int((governance["governance_status"] == "Approved").sum())
    pending = int((governance["governance_status"] == "Pending Review").sum())
    rejected = int((governance["governance_status"] == "Rejected").sum())
    total = int(len(governance))

    compliance_rate = round((approved / total) * 100, 2) if total else 0

    return {
        "total_datasets": total,
        "approved": approved,
        "pending_review": pending,
        "rejected": rejected,
        "compliance_rate": compliance_rate,
    }


def build_governance_audit_timeline() -> pd.DataFrame:
    """Build governance lifecycle timeline from registry data."""

    governance = build_governance_view()

    if governance.empty:
        return pd.DataFrame(
            columns=[
                "dataset_name",
                "event",
                "timestamp",
                "status",
            ]
        )

    rows = []

    for _, row in governance.iterrows():
        dataset_name = row.get("dataset_name", "Unknown")
        upload_timestamp = row.get("upload_timestamp", "N/A")
        status = row.get("status", "Unknown")
        governance_status = row.get("governance_status", "Pending Review")

        rows.append(
            {
                "dataset_name": dataset_name,
                "event": "Registered",
                "timestamp": upload_timestamp,
                "status": status,
            }
        )

        rows.append(
            {
                "dataset_name": dataset_name,
                "event": "Governance Review",
                "timestamp": row.get("decision_date", "Pending"),
                "status": governance_status,
            }
        )

    return pd.DataFrame(rows)


if __name__ == "__main__":
    print(build_governance_view())
    print(get_governance_summary())
    print(build_governance_audit_timeline())