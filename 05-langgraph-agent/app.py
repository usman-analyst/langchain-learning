"""
app.py — Streamlit UI Layer
============================
Responsibility: Provide a clean chat interface for the LangGraph agent.

Features:
    - Chat interface with message history
    - Shows which tool was used for each answer
    - Show/hide raw tool result (debug mode)
    - Clear conversation button
    - Sidebar with sample questions per tool
"""

import streamlit as st
from agent.graph import run_agent

# -------------------------------------------------------------------
# Page configuration — must be first Streamlit command
# -------------------------------------------------------------------
st.set_page_config(
    page_title="Multi-Tool AI Agent",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------------------------------------------
# Session state initialization
# -------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------------------------------------------
# Tool badge colors — visual indicator of which tool was used
# -------------------------------------------------------------------
TOOL_COLORS = {
    "csv_tool":  ("🟢", "CSV Data"),
    "sql_tool":  ("🔵", "SQL Database"),
    "rag_tool":  ("🟣", "TechNova Docs"),
    "llm_only":  ("🟡", "LLM Knowledge"),
    "unknown":   ("⚪", "Unknown"),
}

# -------------------------------------------------------------------
# Sidebar
# -------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Settings")

    show_tool_result = st.toggle(
        "Show raw tool output",
        value=False,
        help="Show the raw data retrieved before LLM processing"
    )

    show_tool_badge = st.toggle(
        "Show tool used",
        value=True,
        help="Show which tool was used to answer each question"
    )

    st.divider()

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.success("Conversation cleared!")
        st.rerun()

    st.divider()

    # Sample questions grouped by tool
    st.subheader("💡 Sample Questions")

    st.markdown("**🟢 CSV Data**")
    csv_questions = [
        "What is the total sales revenue?",
        "Which region has the highest sales?",
        "Top 3 products by revenue?",
    ]
    for q in csv_questions:
        if st.button(q, key=f"csv_{q}", use_container_width=True):
            st.session_state.pending_question = q

    st.markdown("**🔵 SQL Database**")
    sql_questions = [
        "How many customers from Hyderabad?",
        "Top 5 customers by total spend?",
        "How many total orders?",
    ]
    for q in sql_questions:
        if st.button(q, key=f"sql_{q}", use_container_width=True):
            st.session_state.pending_question = q

    st.markdown("**🟣 TechNova Docs**")
    rag_questions = [
        "What is TechNova's total revenue?",
        "What is the work from home policy?",
        "Who are the main competitors?",
    ]
    for q in rag_questions:
        if st.button(q, key=f"rag_{q}", use_container_width=True):
            st.session_state.pending_question = q

    st.divider()

    st.subheader("🔧 Tech Stack")
    st.markdown("""
    - **LangGraph** — Agent routing + graph
    - **LangChain** — LLM + prompts
    - **LlamaIndex** — Document RAG
    - **SQLite** — Structured queries
    - **Pandas** — CSV analysis
    - **OpenAI** — GPT-4o-mini
    """)

# -------------------------------------------------------------------
# Main UI
# -------------------------------------------------------------------
st.title("🤖 Multi-Tool AI Agent")
st.caption(
    "Powered by LangGraph — automatically routes questions to "
    "CSV, SQL, RAG, or LLM based on your question."
)

# Tool legend
col1, col2, col3, col4 = st.columns(4)
col1.markdown("🟢 **CSV** — Sales data")
col2.markdown("🔵 **SQL** — Customer DB")
col3.markdown("🟣 **RAG** — TechNova docs")
col4.markdown("🟡 **LLM** — General questions")

st.divider()

# -------------------------------------------------------------------
# Display chat history
# -------------------------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Show tool badge for assistant messages
        if message["role"] == "assistant" and show_tool_badge:
            tool = message.get("tool_used", "unknown")
            emoji, label = TOOL_COLORS.get(tool, ("⚪", "Unknown"))
            st.caption(f"{emoji} Tool used: **{label}**")

        # Show raw tool result if debug mode on
        if (
            message["role"] == "assistant"
            and show_tool_result
            and message.get("tool_result")
        ):
            with st.expander("🔍 Raw tool output"):
                st.text(message["tool_result"])

# -------------------------------------------------------------------
# Handle sidebar sample question clicks
# -------------------------------------------------------------------
if "pending_question" in st.session_state:
    pending = st.session_state.pop("pending_question")

    st.session_state.messages.append({
        "role": "user",
        "content": pending
    })

    with st.chat_message("assistant"):
        with st.spinner("Agent thinking..."):
            result = run_agent(pending)

        st.markdown(result["answer"])

        if show_tool_badge:
            tool = result["tool_used"]
            emoji, label = TOOL_COLORS.get(tool, ("⚪", "Unknown"))
            st.caption(f"{emoji} Tool used: **{label}**")

        if show_tool_result and result["tool_result"]:
            with st.expander("🔍 Raw tool output"):
                st.text(result["tool_result"])

    st.session_state.messages.append({
        "role":        "assistant",
        "content":     result["answer"],
        "tool_used":   result["tool_used"],
        "tool_result": result["tool_result"]
    })
    st.rerun()

# -------------------------------------------------------------------
# Chat input
# -------------------------------------------------------------------
if user_input := st.chat_input("Ask anything — sales, customers, TechNova docs..."):

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    with st.chat_message("user"):
        st.markdown(user_input)

    # Run agent + display answer
    with st.chat_message("assistant"):
        with st.spinner("Agent thinking..."):
            result = run_agent(user_input)

        # Display answer first
        st.markdown(result["answer"])

        if show_tool_badge:
            tool = result["tool_used"]
            emoji, label = TOOL_COLORS.get(tool, ("⚪", "Unknown"))
            st.caption(f"{emoji} Tool used: **{label}**")

        if show_tool_result and result["tool_result"]:
            with st.expander("🔍 Raw tool output"):
                st.text(result["tool_result"])

    # Save to session state
    st.session_state.messages.append({
        "role":        "assistant",
        "content":     result["answer"],
        "tool_used":   result["tool_used"],
        "tool_result": result["tool_result"]
    })