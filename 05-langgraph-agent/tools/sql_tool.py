"""
tools/sql_tool.py — SQL Query Tool
=====================================
Responsibility: Answer questions about structured data using SQLite.

Reuses the core logic from Project 02 (SQL Generator) but wrapped
as a LangGraph-compatible tool function.

When to use this tool:
    - Questions requiring precise structured queries
    - JOIN operations across multiple tables
    - Questions about customers, orders, transactions
    - Examples: "how many orders from Hyderabad", "top customers by spend"
"""

import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# -------------------------------------------------------------------
# Database path — created by data/setup_db.py
# -------------------------------------------------------------------
DB_PATH = "./data/sales.db"

# -------------------------------------------------------------------
# LLM for SQL generation — same as Project 02
# -------------------------------------------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# -------------------------------------------------------------------
# SQL generation prompt — same pattern as Project 02
# -------------------------------------------------------------------
SQL_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert SQL developer.
Generate a valid SQLite SQL query to answer the user's question.
Return ONLY the SQL query — no explanations, no markdown, no backticks.

Database Schema:
{schema}"""),
    ("human", "{question}")
])

# LCEL chain — same pipe pattern as Project 02
sql_chain = SQL_PROMPT | llm | StrOutputParser()


def get_db_schema() -> str:
    """
    Get the schema of all tables in the SQLite database.

    Returns:
        str: Schema description with table names and columns
    """
    if not os.path.exists(DB_PATH):
        return ""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    schema_parts = []
    for (table_name,) in tables:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        col_desc = ", ".join([f"{col[1]} {col[2]}" for col in columns])
        schema_parts.append(f"Table: {table_name}\nColumns: {col_desc}")

    conn.close()
    return "\n\n".join(schema_parts)


def clean_sql(sql: str) -> str:
    """
    Clean LLM output to extract pure SQL.
    Removes markdown fences, extra whitespace, and unwanted prefixes.

    Args:
        sql: Raw SQL string from LLM output

    Returns:
        str: Clean SQL query ready for execution
    """
    sql = sql.strip()
    sql = sql.replace("```sql", "").replace("```", "")
    sql = sql.replace("SQL:", "").replace("sql:", "")
    return sql.strip()


def run_sql_tool(question: str) -> str:
    """
    Answer a question by generating and executing a SQL query.

    Flow:
        1. Get database schema
        2. LLM generates SQL from question + schema
        3. Execute SQL against SQLite database
        4. Return results as formatted string

    Args:
        question: Natural language question about the database

    Returns:
        str: Query results as formatted string
    """
    try:
        # Check if database exists — if not, create it
        if not os.path.exists(DB_PATH):
            return (
                "Database not found. "
                "Please run: python data/setup_db.py"
            )

        # Step 1: Get schema
        schema = get_db_schema()
        if not schema:
            return "Error: Could not retrieve database schema"

        # Step 2: Generate SQL using LCEL chain
        raw_sql = sql_chain.invoke({
            "schema": schema,
            "question": question
        })
        sql = clean_sql(raw_sql)

        # Step 3: Execute SQL
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(sql, conn)
        conn.close()

        # Step 4: Format results
        if df.empty:
            return "Query returned no results."

        # Return as readable string (max 20 rows to avoid token overflow)
        return df.head(20).to_string(index=False)

    except Exception as e:
        return f"SQL Tool Error: {str(e)}"


# -------------------------------------------------------------------
# Quick test
# Usage: python -m tools.sql_tool
# -------------------------------------------------------------------
if __name__ == "__main__":
    print("Schema:")
    print(get_db_schema())
    print()

    questions = [
        "How many total orders are there?",
        "What are the top 5 customers by total spend?",
    ]

    for q in questions:
        print(f"Q: {q}")
        print(f"A: {run_sql_tool(q)}")
        print()