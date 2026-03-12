import pandas as pd
from typing import Optional


# ── Format Currency ───────────────────────────────────
def format_currency(value: float) -> str:
    """Format number as currency string."""
    return f"${value:,.2f}"


# ── Format Percentage ─────────────────────────────────
def format_percentage(value: float) -> str:
    """Format number as percentage string."""
    return f"{value:.1f}%"


# ── Validate CSV Columns ──────────────────────────────
def validate_columns(df: pd.DataFrame, required_cols: list) -> tuple[bool, list]:
    """
    Check if required columns exist in dataframe.
    Returns (is_valid, missing_columns)
    """
    missing = [col for col in required_cols if col not in df.columns]
    return len(missing) == 0, missing


# ── Get Quick Stats ───────────────────────────────────
def get_quick_stats(df: pd.DataFrame) -> dict:
    """
    Generate quick stats summary for any dataframe.
    Useful for sidebar metrics display.
    """
    stats = {
        "total_rows"   : len(df),
        "total_columns": len(df.columns),
        "numeric_cols" : df.select_dtypes(include="number").columns.tolist(),
        "text_cols"    : df.select_dtypes(include="object").columns.tolist(),
        "missing_values": df.isnull().sum().sum()
    }

    # Add numeric summaries if available
    numeric_df = df.select_dtypes(include="number")
    if not numeric_df.empty:
        stats["numeric_summary"] = numeric_df.describe().to_dict()

    return stats


# ── Clean Column Names ────────────────────────────────
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names:
    - lowercase
    - replace spaces with underscores
    - remove special characters
    """
    df.columns = (
        df.columns
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^a-z0-9_]", "", regex=True)
    )
    return df


# ── Quick Test ────────────────────────────────────────
if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from data_loader import load_csv

    df, _ = load_csv("data/sample_sales.csv")

    print("✅ Testing utils functions:")
    print(f"   format_currency  : {format_currency(5082801.0)}")
    print(f"   format_percentage: {format_percentage(10.33)}")

    is_valid, missing = validate_columns(df, ["region", "revenue", "fake_col"])
    print(f"   validate_columns : valid={is_valid}, missing={missing}")

    stats = get_quick_stats(df)
    print(f"   get_quick_stats  : rows={stats['total_rows']}, missing={stats['missing_values']}")

    df_cleaned = clean_column_names(df.copy())
    print(f"   clean_col_names  : {df_cleaned.columns.tolist()}")