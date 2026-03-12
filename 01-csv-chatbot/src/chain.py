from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd

load_dotenv()


# ── Build Agent ───────────────────────────────────────
def build_csv_agent(df: pd.DataFrame):
    """Create a LangChain Pandas Agent."""

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        verbose=True,
        allow_dangerous_code=True,
        agent_type="tool-calling",  # ← key fix!
        # handle_parsing_errors=True  #  ←# removed handle_parsing_errors - not supported in this version
    )

    return agent


# ── Ask Question ──────────────────────────────────────
def ask_question(agent, question: str) -> str:
    """Send a question to agent and get answer."""
    try:
        response = agent.invoke({"input": question})
        # Debug - print to terminal to see what's coming back
        print(f"DEBUG response: {response}")
        output = response.get("output", "")
        return str(output)
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ── Quick Test ────────────────────────────────────────
if __name__ == "__main__":
    import sys
    import os

    # Fix import path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from data_loader import load_csv

    print("🔄 Loading data...")
    df, summary = load_csv("data/sample_sales.csv")

    print("🤖 Building agent...")
    agent = build_csv_agent(df)

    questions = [
        "What is the total revenue?",
        "Which region has the highest sales?",
        "Who is the top performing salesperson?",
        "What is the best selling product?"
    ]

    print("\n--- Testing Agent ---\n")
    for q in questions:
        print(f"❓ {q}")
        answer = ask_question(agent, q)
        print(f"✅ {answer}")
        print("-" * 50)