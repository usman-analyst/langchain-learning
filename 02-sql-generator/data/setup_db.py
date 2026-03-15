import sqlite3
import pandas as pd
import numpy as np
import random
import os

# Reproducible
np.random.seed(42)
random.seed(42)

# ── Config ────────────────────────────────────────────
DB_PATH = "data/sales.db"

REGIONS = ["North", "South", "East", "West"]
PRODUCTS = ["Laptop", "Phone", "Tablet", "Headphones", "Smartwatch"]
SALESPERSONS = ["Raju", "Priya", "Arjun", "Sneha", "Vikram"]
CUSTOMERS = [
    "TechCorp", "DataSystems", "CloudBase", "InfoTech",
    "SmartSolutions", "DigiWorld", "ByteForce", "NetPulse",
    "CoreLogic", "AlphaWave"
]
PRODUCT_PRICES = {
    "Laptop": 999,
    "Phone": 499,
    "Tablet": 299,
    "Headphones": 149,
    "Smartwatch": 199
}


# ── Generate Sales Data ───────────────────────────────
def generate_sales_data(n: int = 500) -> pd.DataFrame:
    from datetime import datetime, timedelta

    start_date = datetime(2024, 1, 1)

    data = {
        "date": [
            (start_date + timedelta(days=random.randint(0, 364)))
            .strftime("%Y-%m-%d")
            for _ in range(n)
        ],
        "customer"    : [random.choice(CUSTOMERS) for _ in range(n)],
        "region"      : [random.choice(REGIONS) for _ in range(n)],
        "product"     : [random.choice(PRODUCTS) for _ in range(n)],
        "salesperson" : [random.choice(SALESPERSONS) for _ in range(n)],
        "units_sold"  : [random.randint(1, 50) for _ in range(n)],
        "discount_pct": [random.choice([0, 5, 10, 15, 20]) for _ in range(n)],
    }

    df = pd.DataFrame(data)
    df["unit_price"] = df["product"].map(PRODUCT_PRICES)
    df["revenue"] = (
        df["units_sold"]
        * df["unit_price"]
        * (1 - df["discount_pct"] / 100)
    )
    df = df.sort_values("date").reset_index(drop=True)
    return df


# ── Generate Customer Data ────────────────────────────
def generate_customer_data() -> pd.DataFrame:
    data = {
        "customer_name" : CUSTOMERS,
        "industry"      : [
            "Technology", "Finance", "Healthcare",
            "Retail", "Education", "Manufacturing",
            "Consulting", "Media", "Logistics", "Banking"
        ],
        "city"          : [
            "Hyderabad", "Mumbai", "Bangalore",
            "Chennai", "Delhi", "Pune",
            "Kolkata", "Ahmedabad", "Jaipur", "Surat"
        ],
        "since_year"    : [
            random.randint(2018, 2023) for _ in range(len(CUSTOMERS))
        ]
    }
    return pd.DataFrame(data)


# ── Create Database ───────────────────────────────────
def create_database():
    # Create data folder if not exists
    os.makedirs("data", exist_ok=True)

    # Connect to SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("🔄 Generating data...")
    sales_df    = generate_sales_data(500)
    customer_df = generate_customer_data()

    # ── Create Tables ─────────────────────────────────
    cursor.execute("DROP TABLE IF EXISTS sales")
    cursor.execute("DROP TABLE IF EXISTS customers")

    cursor.execute("""
        CREATE TABLE sales (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            date         TEXT,
            customer     TEXT,
            region       TEXT,
            product      TEXT,
            salesperson  TEXT,
            units_sold   INTEGER,
            discount_pct REAL,
            unit_price   REAL,
            revenue      REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE customers (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            industry      TEXT,
            city          TEXT,
            since_year    INTEGER
        )
    """)

    # ── Insert Data ───────────────────────────────────
    sales_df.to_sql(
        "sales", conn,
        if_exists="replace",
        index=False
    )
    customer_df.to_sql(
        "customers", conn,
        if_exists="replace",
        index=False
    )

    conn.commit()

    # ── Verify ────────────────────────────────────────
    sales_count    = pd.read_sql("SELECT COUNT(*) as count FROM sales", conn)
    customer_count = pd.read_sql("SELECT COUNT(*) as count FROM customers", conn)

    print(f"✅ Database created: {DB_PATH}")
    print(f"   sales table    : {sales_count['count'][0]} rows")
    print(f"   customers table: {customer_count['count'][0]} rows")

    # Show sample
    print("\n📋 Sample Sales Data:")
    print(pd.read_sql("SELECT * FROM sales LIMIT 3", conn).to_string())

    print("\n📋 Sample Customer Data:")
    print(pd.read_sql("SELECT * FROM customers LIMIT 3", conn).to_string())

    # Show table schemas
    print("\n🗄️ Table Schemas:")
    print("\nsales columns:")
    for row in cursor.execute("PRAGMA table_info(sales)"):
        print(f"   {row[1]:15} {row[2]}")

    print("\ncustomers columns:")
    for row in cursor.execute("PRAGMA table_info(customers)"):
        print(f"   {row[1]:15} {row[2]}")
    conn.close()
    print("\n✅ Database setup complete!")


# ── Main ──────────────────────────────────────────────
if __name__ == "__main__":
    create_database()