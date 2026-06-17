"""
===============================================================================
ClariPulse™ V2 - SQL Ingestion Connector

Purpose:
    Optional SQL ingestion connector for hospital analytics databases.
    Designed to fail gracefully if SQLAlchemy is not installed.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations

import pandas as pd


try:
    from sqlalchemy import create_engine

    SQLALCHEMY_AVAILABLE = True

except ImportError:
    create_engine = None
    SQLALCHEMY_AVAILABLE = False


def is_sql_supported() -> bool:
    """Return whether SQL ingestion is available in the current environment."""

    return SQLALCHEMY_AVAILABLE


def load_sql_query(
    connection_string: str,
    query: str,
) -> pd.DataFrame:
    """Load data from SQL database if SQLAlchemy is available."""

    if not SQLALCHEMY_AVAILABLE:
        raise ImportError(
            "SQL ingestion requires SQLAlchemy. Install it with: pip install SQLAlchemy"
        )

    engine = create_engine(connection_string)

    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    df = df.replace("?", pd.NA)

    return df


def validate_sql_result(
    df: pd.DataFrame,
    required_columns: list[str],
) -> dict:
    """Validate required columns in SQL query result."""

    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]

    return {
        "valid": len(missing_columns) == 0,
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_columns": missing_columns,
    }


def summarize_sql_result(df: pd.DataFrame) -> dict:
    """Return summary of SQL-ingested data."""

    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }


def sql_connector_status() -> dict:
    """Return SQL connector readiness status."""

    return {
        "source": "SQL Database",
        "supported": SQLALCHEMY_AVAILABLE,
        "status": "Supported" if SQLALCHEMY_AVAILABLE else "Dependency Missing",
        "dependency": "SQLAlchemy",
        "install_command": "pip install SQLAlchemy",
    }