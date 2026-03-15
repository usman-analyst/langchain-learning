import sqlite3
import pandas as pd
from typing import Tuple
import os

# ── DB Path ───────────────────────────────────────────
DB_PATH = "data/sales.db"


# ── Get Connection ────────────────────────────────────
def get_connection() -> sqlite3.Connection:
    """Create and return database connection."""
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            f"Database not found at {DB_PATH}. "
            f"Run data/setup_db.py first!"
        )
    return sqlite3.connect(DB_PATH)


# ── Execute Query ─────────────────────────────────────
def execute_query(sql: str) -> Tuple[pd.DataFrame, str]:
    """
    Execute SQL query and return results.
    Returns (dataframe, status_message)
    """
    try:
        conn = get_connection()
        df = pd.read_sql(sql, conn)
        conn.close()
        return df, "success"
    except Exception as e:
        return pd.DataFrame(), f"❌ Error: {str(e)}"


# ── Get Schema ────────────────────────────────────────
def get_schema() -> str:
    """
    Get database schema as string.
    This is passed to LLM so it knows what tables/columns exist.
    This is the KEY to accurate SQL generation!
    """
    conn = get_connection()
    cursor = conn.cursor()

    schema_parts = []

    # Get all table names
    cursor.execute("""
    SELECT name FROM sqlite_master 
    WHERE type='table' 
    AND name NOT LIKE 'sqlite_%'
""")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]

        # Get column info for each table
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        # Get sample rows
        sample_df = pd.read_sql(
            f"SELECT * FROM {table_name} LIMIT 3",
            conn
        )

        # Build schema string
        col_info = "\n".join([
            f"   - {col[1]} ({col[2]})"
            for col in columns
        ])

        schema_parts.append(f"""
Table: {table_name}
Columns:
{col_info}

Sample Data:
{sample_df.to_string()}
""")

    conn.close()
    return "\n".join(schema_parts)


# ── Get Table Names ───────────────────────────────────
def get_table_names() -> list:
    """Return list of all table names in database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT name FROM sqlite_master 
    WHERE type='table'
    AND name NOT LIKE 'sqlite_%'
""")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables


# ── Get Row Count ─────────────────────────────────────
def get_row_counts() -> dict:
    """Return row count for each table."""
    conn = get_connection()
    tables = get_table_names()
    counts = {}
    for table in tables:
        df = pd.read_sql(f"SELECT COUNT(*) as count FROM {table}", conn)
        counts[table] = df["count"][0]
    conn.close()
    return counts


# ── Quick Test ────────────────────────────────────────
if __name__ == "__main__":
    print("🔄 Testing database connection...")

    # Test connection
    conn = get_connection()
    print("✅ Connection successful!")
    conn.close()

    # Test schema
    print("\n📋 Database Schema:")
    print(get_schema())

    # Test row counts
    print("\n📊 Row Counts:")
    counts = get_row_counts()
    for table, count in counts.items():
        print(f"   {table}: {count} rows")

    # Test query execution
    print("\n🔍 Test Query:")
    df, status = execute_query("""
        SELECT region, SUM(revenue) as total_revenue
        FROM sales
        GROUP BY region
        ORDER BY total_revenue DESC
    """)
    print(f"   Status: {status}")
    print(df.to_string())