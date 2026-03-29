"""
tools/csv_tool.py — CSV Analysis Tool
=======================================
Responsibility: Answer questions about sales data using pandas.

Reuses the core logic from Project 01 (CSV Chatbot) but wrapped
as a LangGraph-compatible tool function instead of a Streamlit agent.

When to use this tool:
    - Questions about sales, orders, revenue from CSV data
    - Aggregations: total, average, count, max, min
    - Filtering: by region, product, date, salesperson
    - Examples: "total sales by region", "top 5 products by revenue"
"""

import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

load_dotenv()

# -------------------------------------------------------------------
# Path to CSV file
# -------------------------------------------------------------------
CSV_PATH = "./data/sales_data.csv"

# -------------------------------------------------------------------
# LLM for pandas agent — same as Project 01
# -------------------------------------------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


def run_csv_tool(question: str) -> str:
    """
    Answer a question about sales data using a pandas dataframe agent.

    The agent automatically writes and executes pandas code to answer
    the question — no manual query writing needed.

    Args:
        question: Natural language question about sales data

    Returns:
        str: Answer derived from the CSV data
    """
    try:
        # Load CSV into dataframe
        if not os.path.exists(CSV_PATH):
            return f"Error: CSV file not found at {CSV_PATH}"

        df = pd.read_csv(CSV_PATH)

        # Create pandas agent — same as Project 01
        agent = create_pandas_dataframe_agent(
            llm=llm,
            df=df,
            agent_type="tool-calling",
            verbose=False,
            allow_dangerous_code=True  # Required for pandas agent execution
        )

        # Run the question
        result = agent.invoke({"input": question})
        return str(result.get("output", "No answer found"))

    except Exception as e:
        return f"CSV Tool Error: {str(e)}"


# -------------------------------------------------------------------
# Quick test
# Usage: python -m tools.csv_tool
# -------------------------------------------------------------------
if __name__ == "__main__":
    questions = [
        "What is the total sales revenue?",
        "Which region has the highest sales?",
        "What are the top 3 products by revenue?"
    ]

    for q in questions:
        print(f"Q: {q}")
        print(f"A: {run_csv_tool(q)}")
        print()