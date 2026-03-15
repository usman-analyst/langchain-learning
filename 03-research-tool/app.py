import streamlit as st
import os
from dotenv import load_dotenv
from src.embeddings import (
    get_or_build_vector_store,
    get_retriever,
    build_vector_store
)
from src.chain import build_rag_chain, ask_question
from src.loader import load_and_split, get_document_stats

load_dotenv()

# ── Page Config ───────────────────────────────────────
st.set_page_config(
    page_title="TechNova Research Assistant",
    page_icon="🔍",
    layout="wide"
)

# ── Session State ─────────────────────────────────────
if "messages"   not in st.session_state:
    st.session_state.messages   = []
if "rag_chain"  not in st.session_state:
    st.session_state.rag_chain  = None
if "retriever"  not in st.session_state:
    st.session_state.retriever  = None
if "docs_loaded" not in st.session_state:
    st.session_state.docs_loaded = False


# ── Load Default Docs ─────────────────────────────────
@st.cache_resource
def load_default_rag():
    """
    Load default TechNova documents.
    @st.cache_resource = runs once, cached for session!
    """
    vectorstore = get_or_build_vector_store()
    retriever   = get_retriever(vectorstore, k=6)
    rag_chain   = build_rag_chain(retriever)
    return rag_chain, retriever


# ── Header ────────────────────────────────────────────
st.title("🔍 TechNova Research Assistant")
st.markdown("Ask questions across all TechNova documents!")
st.divider()

# ── Sidebar ───────────────────────────────────────────
with st.sidebar:
    st.header("📁 Documents")

    # Load default docs button
    if st.button(
        "📚 Load TechNova Documents",
        width="stretch"
    ):
        with st.spinner("Loading documents..."):
            rag_chain, retriever = load_default_rag()
            st.session_state.rag_chain  = rag_chain
            st.session_state.retriever  = retriever
            st.session_state.docs_loaded = True
            st.session_state.messages   = []
        st.success("✅ Documents loaded!")

    st.divider()

    # Show available documents
    st.header("📄 Available Documents")
    docs_dir = "documents"
    if os.path.exists(docs_dir):
        pdf_files = [
            f for f in os.listdir(docs_dir)
            if f.endswith(".pdf")
        ]
        for pdf in sorted(pdf_files):
            st.markdown(f"📄 {pdf}")
    else:
        st.warning("No documents folder found!")

    st.divider()

    # Sample questions
    st.header("💡 Sample Questions")
    sample_questions = [
        "What is TechNova total revenue?",
        "What is the WFH policy?",
        "Who are the main competitors?",
        "Which product has highest revenue?",
        "What is salary increment policy?",
        "What are growth targets for 2025?",
        "What is TechNova market share?",
        "Which region performs best?",
        "What benefits do employees get?",
        "What is the laptop pricing strategy?"
    ]

    for q in sample_questions:
        if st.button(q, key=f"btn_{q}", width="stretch"):
            if st.session_state.rag_chain:
                st.session_state.pending_q = q
            else:
                st.warning("Load documents first!")

    st.divider()

    # Clear chat
    if st.button("🗑️ Clear Chat", width="stretch"):
        st.session_state.messages = []
        st.rerun()

# ── Main Chat Area ────────────────────────────────────
if not st.session_state.docs_loaded:
    # Welcome screen
    st.info("👈 Click 'Load TechNova Documents' to start!")

    st.subheader("📚 Available Documents")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
**📊 Annual Report 2024**
- Revenue: Rs. 508 Crores
- Regional performance
- Product line analysis
- Future outlook 2025

**👥 HR Policy 2024**
- Leave policy
- WFH guidelines
- Performance review
- Salary increments
        """)

    with col2:
        st.markdown("""
**🔬 Market Research 2024**
- Market size analysis
- Competitor landscape
- Growth trends
- Key risks

**📦 Product Catalog 2024**
- Full product lineup
- Pricing details
- Sales performance
- Target segments
        """)

    st.divider()
    st.subheader("💡 What You Can Ask")
    st.markdown("""
    - *"What is TechNova's revenue growth compared to last year?"*
    - *"What are the WFH rules and leave policies?"*
    - *"Who are the competitors and what is our market share?"*
    - *"Which products are growing fastest?"*
    - *"What are the key risks and challenges?"*
    """)

else:
    # ── Chat Interface ────────────────────────────────
    with st.expander("📄 Documents Loaded", expanded=False):
        docs_dir = "documents"
        if os.path.exists(docs_dir):
            pdf_files = [
                f for f in os.listdir(docs_dir)
                if f.endswith(".pdf")
            ]
            for pdf in sorted(pdf_files):
                st.markdown(f"✅ {pdf}")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "sources" in msg and msg["sources"]:
                st.caption(
                    f"📄 Sources: {', '.join(msg['sources'])}"
                )

    # Handle sidebar button questions
    if "pending_q" in st.session_state:
        question = st.session_state.pending_q
        del st.session_state.pending_q

        # Add user message
        st.session_state.messages.append({
            "role"   : "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        # Get answer
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching documents..."):
                result = ask_question(
                    st.session_state.rag_chain,
                    st.session_state.retriever,
                    question
                )
            st.markdown(result["answer"])
            if result["sources"]:
                st.caption(
                    f"📄 Sources: {', '.join(result['sources'])}"
                )

        # Save to history
        st.session_state.messages.append({
            "role"   : "assistant",
            "content": result["answer"],
            "sources": result["sources"]
        })

    # Chat input
    question = st.chat_input(
        "Ask anything about TechNova documents..."
    )

    if question:
        # Add user message
        st.session_state.messages.append({
            "role"   : "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        # Get answer
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching documents..."):
                result = ask_question(
                    st.session_state.rag_chain,
                    st.session_state.retriever,
                    question
                )
            st.markdown(result["answer"])
            if result["sources"]:
                st.caption(
                    f"📄 Sources: {', '.join(result['sources'])}"
                )

        # Save to history
        st.session_state.messages.append({
            "role"   : "assistant",
            "content": result["answer"],
            "sources": result["sources"]
        })