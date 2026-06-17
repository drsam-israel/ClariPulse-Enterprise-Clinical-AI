"""
===============================================================================
ClariPulse™ V2 - Diabetes Readmission Preprocessor

Purpose:
    Convert the real-world diabetes readmission dataset into an ML-ready
    feature matrix for 30-day readmission prediction.

Author:
    Samuel Israel, MD

License:
    MIT
===============================================================================
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split

from app.v2.data.diabetes_loader import load_diabetes_data


PROJECT_ROOT = Path(__file__).resolve().parents[3]

REPORT_DIR = PROJECT_ROOT / "reports" / "v2"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed" / "v2"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

FEATURE_MATRIX_PATH = PROCESSED_DIR / "diabetes_feature_matrix.csv"
FEATURE_COLUMNS_PATH = REPORT_DIR / "diabetes_feature_columns.csv"

TARGET_COLUMN = "target_readmitted_30day"


def create_target(df: pd.DataFrame) -> pd.DataFrame:
    """Create binary target: <30 readmission = 1, otherwise 0."""

    df = df.copy()

    if "readmitted" not in df.columns:
        raise KeyError("Required target column 'readmitted' not found.")

    df[TARGET_COLUMN] = (df["readmitted"] == "<30").astype(int)

    return df


def clean_invalid_categories(df: pd.DataFrame) -> pd.DataFrame:
    """Clean invalid categories and uncommon values."""

    df = df.copy()

    if "gender" in df.columns:
        df = df[df["gender"] != "Unknown/Invalid"]

    return df


def simplify_diagnosis_codes(df: pd.DataFrame) -> pd.DataFrame:
    """Convert diagnosis codes into broad clinical groups."""

    df = df.copy()

    diagnosis_columns = ["diag_1", "diag_2", "diag_3"]

    def map_diagnosis(value: object) -> str:
        if pd.isna(value):
            return "Missing"

        value_str = str(value)

        if value_str.startswith("V") or value_str.startswith("E"):
            return "External_or_Supplementary"

        try:
            code = float(value_str)
        except ValueError:
            return "Other"

        if 390 <= code <= 459 or code == 785:
            return "Circulatory"

        if 460 <= code <= 519 or code == 786:
            return "Respiratory"

        if 520 <= code <= 579 or code == 787:
            return "Digestive"

        if 250 <= code < 251:
            return "Diabetes"

        if 800 <= code <= 999:
            return "Injury"

        if 710 <= code <= 739:
            return "Musculoskeletal"

        if 580 <= code <= 629 or code == 788:
            return "Genitourinary"

        if 140 <= code <= 239:
            return "Neoplasms"

        return "Other"

    for column in diagnosis_columns:
        if column in df.columns:
            df[column] = df[column].apply(map_diagnosis)

    return df


def drop_leakage_and_id_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove ID, target leakage, and non-model columns."""

    columns_to_drop = [
        "encounter_id",
        "patient_nbr",
        "readmitted",
        "weight",
        "payer_code",
        "medical_specialty",
    ]

    existing_columns = [column for column in columns_to_drop if column in df.columns]

    return df.drop(columns=existing_columns)


def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    """Encode categorical features using one-hot encoding."""

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    df_encoded = pd.get_dummies(
        df,
        columns=categorical_columns,
        drop_first=True,
        dummy_na=True,
    )

    return df_encoded


def sanitize_feature_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Make feature names safe for XGBoost, LightGBM, CatBoost, ONNX, and future APIs.

    This removes or replaces special characters such as:
    [, ], <, >, (, ), /, \\ , spaces, commas, and other non-alphanumeric symbols.
    """

    df = df.copy()

    cleaned_columns = []

    for column in df.columns.astype(str):
        clean_name = column

        clean_name = clean_name.replace("<", "lt_")
        clean_name = clean_name.replace(">", "gt_")

        clean_name = re.sub(r"[^A-Za-z0-9_]+", "_", clean_name)
        clean_name = re.sub(r"_+", "_", clean_name)
        clean_name = clean_name.strip("_")

        cleaned_columns.append(clean_name)

    # Ensure no duplicate column names after sanitization
    seen = {}
    final_columns = []

    for column in cleaned_columns:
        if column not in seen:
            seen[column] = 0
            final_columns.append(column)
        else:
            seen[column] += 1
            final_columns.append(f"{column}_{seen[column]}")

    df.columns = final_columns

    return df


def build_feature_matrix() -> pd.DataFrame:
    """Build and save the final ML-ready feature matrix."""

    df = load_diabetes_data()

    df = create_target(df)
    df = clean_invalid_categories(df)
    df = simplify_diagnosis_codes(df)
    df = drop_leakage_and_id_columns(df)
    df = encode_features(df)
    df = sanitize_feature_names(df)

    if TARGET_COLUMN not in df.columns:
        raise KeyError(f"Target column '{TARGET_COLUMN}' was lost during preprocessing.")

    df[TARGET_COLUMN] = df[TARGET_COLUMN].astype(int)

    feature_columns = [column for column in df.columns if column != TARGET_COLUMN]

    df.to_csv(FEATURE_MATRIX_PATH, index=False)

    pd.DataFrame({"feature": feature_columns}).to_csv(
        FEATURE_COLUMNS_PATH,
        index=False,
    )

    return df


def split_features_target(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    """Split feature matrix into X and y."""

    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    return X, y


def train_test_split_v2(
    X: pd.DataFrame,
    y: pd.Series,
):
    """Create stratified train/test split."""

    return train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42,
    )


if __name__ == "__main__":
    feature_matrix = build_feature_matrix()

    X, y = split_features_target(feature_matrix)

    X_train, X_test, y_train, y_test = train_test_split_v2(X, y)

    print("\nClariPulse™ V2 Feature Matrix Created Successfully\n")
    print(f"Feature matrix shape: {feature_matrix.shape}")
    print(f"X shape: {X.shape}")
    print(f"Target distribution:\n{y.value_counts(normalize=True)}")
    print(f"Train shape: {X_train.shape}")
    print(f"Test shape: {X_test.shape}")
    print(f"Saved feature matrix to: {FEATURE_MATRIX_PATH}")