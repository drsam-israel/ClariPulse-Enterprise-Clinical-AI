"""
===============================================================================
ClariPulse™ V2 - Unified Ingestion Service

Purpose:
    Central orchestration layer for importing healthcare data from
    CSV files, SQL databases, and future interoperability sources.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.v2.ingestion.csv_connector import (
    load_csv_file,
    summarize_csv,
    validate_csv_schema,
)

from app.v2.ingestion.sql_connector import (
    is_sql_supported,
    load_sql_query,
    sql_connector_status,
    summarize_sql_result,
    validate_sql_result,
)


class IngestionService:
    """Unified enterprise ingestion service."""

    @staticmethod
    def load_from_csv(
        file_path: str | Path,
        required_columns: list[str] | None = None,
    ) -> dict:
        """Load and optionally validate a CSV source."""

        df = load_csv_file(file_path)

        result = {
            "source": "CSV",
            "status": "Loaded",
            "dataframe": df,
            "summary": summarize_csv(df),
        }

        if required_columns is not None:
            result["validation"] = validate_csv_schema(
                df,
                required_columns,
            )

        return result

    @staticmethod
    def load_from_sql(
        connection_string: str,
        query: str,
        required_columns: list[str] | None = None,
    ) -> dict:
        """Load and optionally validate a SQL source."""

        if not is_sql_supported():
            return {
                "source": "SQL",
                "status": "Unavailable",
                "error": (
                    "SQLAlchemy is not installed. SQL ingestion is currently disabled."
                ),
                "install_command": "pip install SQLAlchemy",
                "dataframe": pd.DataFrame(),
                "summary": {},
                "validation": {},
            }

        df = load_sql_query(
            connection_string,
            query,
        )

        result = {
            "source": "SQL",
            "status": "Loaded",
            "dataframe": df,
            "summary": summarize_sql_result(df),
        }

        if required_columns is not None:
            result["validation"] = validate_sql_result(
                df,
                required_columns,
            )

        return result

    @staticmethod
    def supported_sources() -> pd.DataFrame:
        """Return enterprise ingestion roadmap."""

        sql_status = sql_connector_status()

        return pd.DataFrame(
            {
                "Source": [
                    "CSV",
                    "SQL Database",
                    "FHIR API",
                    "HL7 Feed",
                    "Epic",
                    "Cerner",
                    "OpenMRS",
                    "Azure Synapse",
                    "Snowflake",
                    "Databricks",
                ],
                "Status": [
                    "Supported",
                    sql_status["status"],
                    "Planned",
                    "Planned",
                    "Planned",
                    "Planned",
                    "Planned",
                    "Planned",
                    "Planned",
                    "Planned",
                ],
            }
        )

    @staticmethod
    def connector_health() -> pd.DataFrame:
        """Return connector-level health status."""

        sql_status = sql_connector_status()

        return pd.DataFrame(
            {
                "Connector": [
                    "CSV Connector",
                    "SQL Connector",
                    "FHIR Connector",
                    "HL7 Connector",
                ],
                "Readiness": [
                    "Ready",
                    "Ready" if sql_status["supported"] else "Dependency Missing",
                    "Roadmap",
                    "Roadmap",
                ],
                "Dependency": [
                    "pandas",
                    "SQLAlchemy",
                    "FHIR client / REST API",
                    "HL7 parser",
                ],
                "Action": [
                    "Available",
                    "Available" if sql_status["supported"] else "Install SQLAlchemy",
                    "Planned for V2/V3",
                    "Planned for V2/V3",
                ],
            }
        )


if __name__ == "__main__":
    print(IngestionService.supported_sources())
    print(IngestionService.connector_health())