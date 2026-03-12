import pandas as pd
import os
from typing import Tuple


# ── Load CSV ─────────────────────────────────────────
def load_csv(file_path: str) -> Tuple[pd.DataFrame, str]:
    """
    Load and validate a CSV file.
    Returns dataframe and a summary string for the AI agent.
    """

    # Check file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    # Load CSV
    df = pd.read_csv(file_path)

    # Basic validation
    if df.empty:
        raise ValueError("CSV file is empty!")

    return df, build_data_summary(df)


# ── Build Summary ─────────────────────────────────────
def build_data_summary(df: pd.DataFrame) -> str:
    """
    Build a human readable summary of the dataframe.
    This is passed to AI so it understands the data structure.
    """

    summary = f"""
Dataset Overview:
-----------------
Total Rows      : {len(df)}
Total Columns   : {len(df.columns)}
Columns         : {', '.join(df.columns.tolist())}

Column Data Types:
{df.dtypes.to_string()}

Sample Data (first 3 rows):
{df.head(3).to_string()}

Numeric Columns Summary:
{df.describe().to_string()}
"""
    return summary


# ── Get Column Info ───────────────────────────────────
def get_column_info(df: pd.DataFrame) -> dict:
    """Return column names grouped by data type."""
    return {
        "numeric"  : df.select_dtypes(include="number").columns.tolist(),
        "text"     : df.select_dtypes(include="object").columns.tolist(),
        "all"      : df.columns.tolist()
    }


# ── Quick Test ────────────────────────────────────────
if __name__ == "__main__":
    df, summary = load_csv("data/sample_sales.csv")

    print("✅ CSV Loaded Successfully!")
    print(summary)

    print("\n📋 Column Info:")
    col_info = get_column_info(df)
    print(f"   Numeric columns : {col_info['numeric']}")
    print(f"   Text columns    : {col_info['text']}")