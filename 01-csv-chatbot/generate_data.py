import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Reproducible results - same data every time you run
np.random.seed(42)
random.seed(42)

# ── Config ──────────────────────────────────────────
REGIONS = ["North", "South", "East", "West"]
PRODUCTS = ["Laptop", "Phone", "Tablet", "Headphones", "Smartwatch"]
SALESPERSONS = ["Raju", "Priya", "Arjun", "Sneha", "Vikram"]
PRODUCT_PRICES = {
    "Laptop": 999,
    "Phone": 499,
    "Tablet": 299,
    "Headphones": 149,
    "Smartwatch": 199
}

# ── Generate Data ────────────────────────────────────
def generate_sales_data(n_rows: int = 500) -> pd.DataFrame:
    """Generate synthetic sales data for testing."""

    start_date = datetime(2024, 1, 1)

    # Build raw data
    data = {
        "date": [
            (start_date + timedelta(days=random.randint(0, 364)))
            .strftime("%Y-%m-%d")
            for _ in range(n_rows)
        ],
        "region": [random.choice(REGIONS) for _ in range(n_rows)],
        "product": [random.choice(PRODUCTS) for _ in range(n_rows)],
        "salesperson": [random.choice(SALESPERSONS) for _ in range(n_rows)],
        "units_sold": [random.randint(1, 50) for _ in range(n_rows)],
        "discount_percent": [
            random.choice([0, 5, 10, 15, 20]) for _ in range(n_rows)
        ],
    }

    df = pd.DataFrame(data)

    # Add unit price based on product
    df["unit_price"] = df["product"].map(PRODUCT_PRICES)

    # Calculate final revenue
    df["revenue"] = (
        df["units_sold"]
        * df["unit_price"]
        * (1 - df["discount_percent"] / 100)
    )

    # Sort by date
    df = df.sort_values("date").reset_index(drop=True)

    return df


# ── Save Data ────────────────────────────────────────
def save_data(df: pd.DataFrame, path: str) -> None:
    """Save dataframe to CSV."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"✅ Saved {len(df)} rows to {path}")


# ── Main ─────────────────────────────────────────────
if __name__ == "__main__":
    print("🔄 Generating sales data...")

    df = generate_sales_data(n_rows=500)
    save_data(df, "data/sample_sales.csv")

    # Quick summary
    print("\n📊 Data Summary:")
    print(f"   Rows          : {len(df)}")
    print(f"   Date Range    : {df['date'].min()} → {df['date'].max()}")
    print(f"   Total Revenue : ${df['revenue'].sum():,.2f}")
    print(f"   Products      : {df['product'].unique().tolist()}")
    print(f"   Regions       : {df['region'].unique().tolist()}")

    print("\n📋 Sample Rows:")
    print(df.head())