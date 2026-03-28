"""
chain.py — LangChain Conversation Layer
========================================
Responsibility: Add conversation memory + prompt formatting on top of
                LlamaIndex retrieval.

Architecture:
    User question
        → LangChain formats prompt (question + chat history + context)
        → LlamaIndex retrieves relevant chunks (via retriever.py)
        → LangChain sends formatted prompt + context to GPT-4o-mini
        → Answer returned with memory updated

This is the LangChain + LlamaIndex integration layer.
LlamaIndex handles DATA retrieval, LangChain handles CONVERSATION logic.

Note on imports:
    langchain.chains  → deprecated, use langchain_core LCEL pipe (|) instead
    langchain.memory  → deprecated, use ChatMessageHistory instead
    langchain.prompts → deprecated, use langchain_core.prompts instead
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory

from retriever import build_simple_engine, build_sub_question_engine
from ingest import get_index

# -------------------------------------------------------------------
# Load environment variables
# -------------------------------------------------------------------
load_dotenv()

# -------------------------------------------------------------------
# LLM Configuration
# -------------------------------------------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0  # temperature=0 → consistent, factual answers
)

# -------------------------------------------------------------------
# Prompt Template
# {history}  → filled by ChatMessageHistory (conversation memory)
# {context}  → filled by LlamaIndex retrieval results
# {question} → filled by user's current question
# -------------------------------------------------------------------
PROMPT_TEMPLATE = """You are a helpful AI assistant for TechNova Solutions.
You answer questions based ONLY on the provided context from TechNova documents.
If the answer is not in the context, say "I don't have that information in the documents."
Do not make up answers.

Conversation History:
{history}

Context from TechNova Documents:
{context}

Current Question: {question}

Answer:"""

prompt = PromptTemplate(
    input_variables=["history", "context", "question"],
    template=PROMPT_TEMPLATE
)

# -------------------------------------------------------------------
# LCEL Chain — Modern LangChain pipe syntax (replaces LLMChain)
# prompt | llm | StrOutputParser()
# This is the same pattern we used in Project 02 SQL Generator!
# -------------------------------------------------------------------
chain = prompt | llm | StrOutputParser()

# -------------------------------------------------------------------
# Conversation Memory Store
# Dict of session_id → ChatMessageHistory
# Supports multiple users / sessions simultaneously
# -------------------------------------------------------------------
store = {}  # { "session_id": ChatMessageHistory }


def get_session_history(session_id: str) -> ChatMessageHistory:
    """
    Get or create a ChatMessageHistory for the given session.

    Args:
        session_id: Unique identifier for the conversation session

    Returns:
        ChatMessageHistory for that session
    """
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def ask(
    question: str,
    use_sub_questions: bool = False,
    session_id: str = "default"
) -> dict:
    """
    Ask a question using LangChain memory + LlamaIndex retrieval.

    Flow:
        1. LlamaIndex retrieves relevant context chunks
        2. ChatMessageHistory builds conversation history string
        3. LCEL chain formats prompt → calls LLM → parses output
        4. Q&A saved to memory for next turn

    Args:
        question:          Natural language question from the user
        use_sub_questions: True  → SubQuestionQueryEngine (complex questions)
                           False → Simple engine (faster, single-topic)
        session_id:        Unique session ID for memory isolation

    Returns:
        dict:
            "answer"  → generated answer string
            "context" → retrieved chunks used as context
    """
    # Step 1: Load index and select query engine
    index = get_index()
    if use_sub_questions:
        query_engine = build_sub_question_engine(index)
    else:
        query_engine = build_simple_engine(index)

    # Step 2: Retrieve relevant context from LlamaIndex
    retrieval_response = query_engine.query(question)
    context = str(retrieval_response)

    # Step 3: Build history string from memory
    history = get_session_history(session_id)
    history_str = "\n".join(
        [f"{m.type}: {m.content}" for m in history.messages]
    )

    # Step 4: Run LCEL chain — prompt | llm | StrOutputParser
    answer = chain.invoke({
        "question": question,
        "context":  context,
        "history":  history_str
    })

    # Step 5: Save this Q&A to memory for next turn
    history.add_user_message(question)
    history.add_ai_message(answer.strip())

    return {
        "answer":  answer.strip(),
        "context": context
    }


def get_chat_history(session_id: str = "default") -> str:
    """
    Return full conversation history as a formatted string.
    Used by Streamlit UI to display previous messages.

    Returns:
        str: Formatted conversation history
    """
    history = get_session_history(session_id)
    return "\n".join(
        [f"{m.type}: {m.content}" for m in history.messages]
    )


def clear_memory(session_id: str = "default") -> None:
    """
    Clear conversation history for a session.
    Called when user clicks 'New Chat' button in Streamlit UI.
    """
    if session_id in store:
        store[session_id].clear()
    print("Conversation memory cleared.")


# -------------------------------------------------------------------
# Quick test — run this file directly to verify memory works
# Usage: python chain.py
# -------------------------------------------------------------------
if __name__ == "__main__":

    print("=" * 60)
    print("TEST: Conversation Memory")
    print("=" * 60)

    # Question 1 — direct fact
    print("\nQuestion 1:")
    r1 = ask("What is TechNova's total revenue in 2024?")
    print(f"Answer: {r1['answer']}")

    # Question 2 — memory test ("their" should refer to TechNova)
    print("\nQuestion 2 (memory test):")
    r2 = ask("What is their net profit?")
    print(f"Answer: {r2['answer']}")

    # Question 3 — different document
    print("\nQuestion 3 (cross-document):")
    r3 = ask("What is the work from home policy?")
    print(f"Answer: {r3['answer']}")

    # Show memory
    print("\n" + "=" * 60)
    print("Full Conversation History in Memory:")
    print("=" * 60)
    print(get_chat_history())