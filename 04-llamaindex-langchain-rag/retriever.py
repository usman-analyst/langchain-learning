"""
retriever.py — LlamaIndex Query Engine Layer
=============================================
Responsibility: Take a question → retrieve relevant chunks → return answer + sources

Two query engines are provided:
    1. simple_query_engine  — single-document style retrieval (fast)
    2. sub_question_engine  — splits complex questions into sub-questions,
                              routes each to the right document, combines answers

This is the key advantage of LlamaIndex over LangChain:
SubQuestionQueryEngine is built-in — no custom routing logic needed.
"""

from llama_index.core import VectorStoreIndex
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.response.pprint_utils import pprint_response

from ingest import get_index  # Reuse smart loader from ingest.py


def build_simple_engine(index: VectorStoreIndex):
    """
    Build a basic query engine from the vector index.

    Best for: single-topic questions like
    "What is TechNova's revenue?" or "What is the WFH policy?"

    Args:
        index: VectorStoreIndex loaded from ingest.get_index()

    Returns:
        QueryEngine ready to accept .query() calls
    """
    query_engine = index.as_query_engine(
        similarity_top_k=6,   # Retrieve top 6 most relevant chunks
        streaming=False        # Return full response at once (not streamed)
    )
    return query_engine


def build_sub_question_engine(index: VectorStoreIndex):
    """
    Build a SubQuestionQueryEngine for complex multi-document questions.

    How it works:
        1. User asks: "Compare TechNova revenue vs competitor market share"
        2. Engine splits into sub-questions:
           - "What is TechNova's revenue?" → routes to annual_report tool
           - "What is competitor market share?" → routes to market_research tool
        3. Each sub-question is answered separately
        4. All answers are combined into one final response

    This replaces complex custom routing chains in LangChain.

    Args:
        index: VectorStoreIndex loaded from ingest.get_index()

    Returns:
        SubQuestionQueryEngine ready to accept .query() calls
    """

    # Step 1: Create individual query engines for each document topic
    # Each tool represents one document / domain area
    # The description tells the LLM WHEN to use each tool
    individual_query_engine = index.as_query_engine(similarity_top_k=4)

    tools = [
        QueryEngineTool(
            query_engine=individual_query_engine,
            metadata=ToolMetadata(
                name="annual_report",
                description=(
                    "Contains TechNova's 2024 annual report. "
                    "Use this for questions about revenue, financial performance, "
                    "regional sales, product performance, and business outlook."
                ),
            ),
        ),
        QueryEngineTool(
            query_engine=individual_query_engine,
            metadata=ToolMetadata(
                name="hr_policy",
                description=(
                    "Contains TechNova's 2024 HR policy document. "
                    "Use this for questions about leave policy, work from home, "
                    "performance reviews, salary, and employee benefits."
                ),
            ),
        ),
        QueryEngineTool(
            query_engine=individual_query_engine,
            metadata=ToolMetadata(
                name="market_research",
                description=(
                    "Contains TechNova's 2024 market research report. "
                    "Use this for questions about market trends, competitors, "
                    "industry risks, and market opportunities."
                ),
            ),
        ),
        QueryEngineTool(
            query_engine=individual_query_engine,
            metadata=ToolMetadata(
                name="product_catalog",
                description=(
                    "Contains TechNova's 2024 product catalog. "
                    "Use this for questions about products, pricing, "
                    "product features, and sales data."
                ),
            ),
        ),
    ]

    # Step 2: Wrap all tools into a SubQuestionQueryEngine
    # This engine automatically breaks complex questions into sub-questions
    sub_question_engine = SubQuestionQueryEngine.from_defaults(
        query_engine_tools=tools,
        verbose=True,   # Shows sub-questions in terminal — great for learning!
        use_async=False # Synchronous mode (simpler, works everywhere)
    )

    return sub_question_engine


def query_simple(question: str) -> str:
    """
    Answer a simple single-topic question.

    Args:
        question: Natural language question string

    Returns:
        Answer string with source information
    """
    index = get_index()
    engine = build_simple_engine(index)
    response = engine.query(question)
    return str(response)


def query_sub_question(question: str) -> str:
    """
    Answer a complex multi-document question using sub-question decomposition.

    Args:
        question: Natural language question string (can be complex/multi-part)

    Returns:
        Combined answer string from multiple sub-question responses
    """
    index = get_index()
    engine = build_sub_question_engine(index)
    response = engine.query(question)
    return str(response)


# -------------------------------------------------------------------
# Quick test — run this file directly to verify both engines work
# Usage: python retriever.py
# -------------------------------------------------------------------
if __name__ == "__main__":

    print("=" * 60)
    print("TEST 1: Simple Query Engine")
    print("=" * 60)
    answer1 = query_simple("What is TechNova's total revenue in 2024?")
    print(f"Answer: {answer1}")

    print("\n" + "=" * 60)
    print("TEST 2: Sub-Question Query Engine")
    print("=" * 60)
    answer2 = query_sub_question(
        "What is TechNova's revenue and what are the main competitor risks?"
    )
    print(f"\nFinal Answer: {answer2}")