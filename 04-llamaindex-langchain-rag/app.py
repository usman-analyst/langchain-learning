"""
app.py — Streamlit UI Layer
============================
Responsibility: Provide a clean chat interface that connects all layers:
    - ingest.py   → LlamaIndex PDF ingestion + vector storage
    - retriever.py → LlamaIndex query engines (simple + sub-question)
    - chain.py    → LangChain memory + prompt + LLM

UI Features:
    - Chat interface with message history
    - Toggle between Simple and Sub-Question query engines
    - Show/hide retrieved context (source chunks)
    - Clear conversation memory button
    - Sidebar with document info and sample questions
"""

import streamlit as st
from chain import ask, get_chat_history, clear_memory
from ingest import get_index

# -------------------------------------------------------------------
# Streamlit Page Configuration
# Must be the first Streamlit command in the file
# -------------------------------------------------------------------
st.set_page_config(
    page_title="TechNova AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------------------------------------------
# Cache the index loading — runs only once per session
# @st.cache_resource → for ML models, connections, heavy objects
# Without this, index reloads on every user interaction (slow + costly)
# -------------------------------------------------------------------
@st.cache_resource
def load_index_once():
    """Load LlamaIndex vector index once and cache it for the session."""
    return get_index()


# Load index at startup — triggers cache
load_index_once()

# -------------------------------------------------------------------
# Session State Initialization
# st.session_state persists data across Streamlit reruns
# Without this, chat history disappears on every interaction
# -------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []  # List of {"role": ..., "content": ...}

if "session_id" not in st.session_state:
    st.session_state.session_id = "default"

# -------------------------------------------------------------------
# Sidebar — Settings + Document Info + Sample Questions
# -------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Settings")

    # Engine selection toggle
    use_sub_questions = st.toggle(
        "Use Sub-Question Engine",
        value=False,
        help=(
            "OFF → Simple engine (faster, single-topic questions)\n"
            "ON  → Sub-Question engine (complex, multi-document questions)"
        )
    )

    # Show context toggle
    show_context = st.toggle(
        "Show Retrieved Context",
        value=False,
        help="Show the document chunks retrieved by LlamaIndex"
    )

    st.divider()

    # Clear memory button
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        clear_memory(st.session_state.session_id)
        st.success("Conversation cleared!")
        st.rerun()

    st.divider()

    # Document info
    st.subheader("📄 Available Documents")
    st.markdown("""
    - 📊 Annual Report 2024
    - 👥 HR Policy 2024
    - 📈 Market Research 2024
    - 🛍️ Product Catalog 2024
    """)

    st.divider()

    # Sample questions
    st.subheader("💡 Sample Questions")
    sample_questions = [
        "What is TechNova's total revenue?",
        "What is the work from home policy?",
        "Who are the main competitors?",
        "What products does TechNova sell?",
        "What is the net profit and market share?",
    ]
    for q in sample_questions:
        if st.button(q, use_container_width=True):
            st.session_state.pending_question = q

    st.divider()

    # Engine info
    st.subheader("🔧 Tech Stack")
    st.markdown("""
    - **LlamaIndex** — PDF ingestion + retrieval
    - **LangChain** — Memory + prompt + chain
    - **OpenAI** — GPT-4o-mini + embeddings
    - **Streamlit** — UI layer
    """)

# -------------------------------------------------------------------
# Main Chat Interface
# -------------------------------------------------------------------
st.title("🤖 TechNova AI Assistant")
st.caption("Ask questions about TechNova's Annual Report, HR Policy, Market Research, and Product Catalog.")

# Display engine status
if use_sub_questions:
    st.info("🔀 Sub-Question Engine active — best for complex, multi-document questions")
else:
    st.info("⚡ Simple Engine active — fast, best for single-topic questions")

st.divider()

# -------------------------------------------------------------------
# Display Chat History
# Loop through all messages and render them as chat bubbles
# -------------------------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Show context if enabled and this is an assistant message
        if (
            show_context
            and message["role"] == "assistant"
            and "context" in message
        ):
            with st.expander("📄 Retrieved Context"):
                st.text(message["context"])

# -------------------------------------------------------------------
# Handle Sample Question clicks from sidebar
# -------------------------------------------------------------------
if "pending_question" in st.session_state:
    pending = st.session_state.pop("pending_question")
    st.session_state.messages.append({"role": "user", "content": pending})

    with st.chat_message("assistant"):
        with st.spinner("Searching TechNova documents..."):
            result = ask(
                question=pending,
                use_sub_questions=use_sub_questions,
                session_id=st.session_state.session_id
            )

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "context": result["context"]
    })
    st.rerun()

# -------------------------------------------------------------------
# Chat Input — Main question box at the bottom
# -------------------------------------------------------------------
if user_input := st.chat_input("Ask a question about TechNova..."):

    # Display user message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Searching TechNova documents..."):
            result = ask(
                question=user_input,
                use_sub_questions=use_sub_questions,
                session_id=st.session_state.session_id
            )

        # Display answer first, then save to session state
        st.markdown(result["answer"])

        # Show context if enabled
        if show_context:
            with st.expander("📄 Retrieved Context"):
                st.text(result["context"])

    # Save assistant message to session state
    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "context": result["context"]
    })