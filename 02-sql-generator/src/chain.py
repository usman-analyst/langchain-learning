from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import get_schema, execute_query

load_dotenv()


# ── SQL Generation Prompt ─────────────────────────────
SQL_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert SQL analyst.
Your job is to convert natural language questions to SQLite SQL queries.

Database Schema:
{schema}

Rules:
- Generate ONLY the SQL query, nothing else
- No markdown, no backticks, no explanation
- Use correct table and column names from schema
- For revenue calculations use SUM(revenue)
- Always use proper SQLite syntax
- If question needs JOIN, use customer_name = customer
"""),
    ("human", "Question: {question}\n\nSQL Query:")
])


# ── Clean SQL Output ──────────────────────────────────
def clean_sql(sql: str) -> str:
    """
    Clean LLM output to get pure SQL.
    LLM sometimes adds extra text — we strip it.
    """
    # Remove markdown code blocks if present
    sql = sql.strip()
    sql = sql.replace("```sql", "").replace("```", "")
    sql = sql.strip()
    return sql


# ── Build Chain ───────────────────────────────────────
def build_sql_chain():
    """
    Build LCEL Chain for SQL generation.

    Pipeline:
    question → prompt → llm → output_parser → clean_sql
    """

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0  # 0 = consistent SQL, no creativity needed
    )

    # ── This is the LCEL Chain! ───────────────────────
    # | pipe operator connects each step
    # output of one step = input of next step
    sql_generation_chain = (
        SQL_PROMPT
        | llm
        | StrOutputParser()
    )

    return sql_generation_chain


# ── Ask Question ──────────────────────────────────────
def ask_question(question: str) -> dict:
    """
    Full pipeline:
    1. Get schema from database
    2. Generate SQL using chain
    3. Execute SQL on database
    4. Return results

    Returns dict with sql, dataframe, status
    """
    try:
        # Step 1 — Get schema
        schema = get_schema()

        # Step 2 — Build chain and generate SQL
        chain = build_sql_chain()

        # Step 3 — Invoke chain
        # This flows through: prompt → llm → parser
        raw_sql = chain.invoke({
            "schema": schema,
            "question": question
        })

        # Step 4 — Clean SQL
        sql = clean_sql(raw_sql)

        # Step 5 — Execute SQL
        df, status = execute_query(sql)

        return {
            "question": question,
            "sql"     : sql,
            "data"    : df,
            "status"  : status,
            "rows"    : len(df)
        }

    except Exception as e:
        return {
            "question": question,
            "sql"     : "",
            "data"    : None,
            "status"  : f"❌ Error: {str(e)}",
            "rows"    : 0
        }


# ── Quick Test ────────────────────────────────────────
if __name__ == "__main__":

    print("🔄 Building SQL chain...")
    print("✅ Chain ready!\n")

    # Test questions
    questions = [
        "What is the total revenue?",
        "Show top 3 regions by revenue",
        "Which product sells the most units?",
        "Show me all customers from Technology industry",
    ]

    for q in questions:
        print(f"❓ Question : {q}")
        result = ask_question(q)
        print(f"🔍 SQL      : {result['sql']}")
        print(f"📊 Status   : {result['status']}")
        if result["data"] is not None and not result["data"].empty:
            print(f"📋 Results  :")
            print(result["data"].to_string())
        print("-" * 60)