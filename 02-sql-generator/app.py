import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from src.database import get_schema, get_table_names, get_row_counts
from src.chain import ask_question

load_dotenv()

# ── Page Config ───────────────────────────────────────
st.set_page_config(
    page_title="SQL Generator Bot",
    page_icon="🔍",
    layout="wide"
)

# ── Session State ─────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ── Header ────────────────────────────────────────────
st.title("🔍 SQL Generator Bot")
st.markdown("Ask questions in plain English — get SQL + results instantly!")
st.divider()

# ── Sidebar ───────────────────────────────────────────
with st.sidebar:
    st.header("🗄️ Database Info")

    # Show table info
    try:
        counts = get_row_counts()
        for table, count in counts.items():
            st.metric(f"{table} table", f"{count} rows")

        st.divider()

        # Show schema in expander
        with st.expander("📋 View Schema"):
            schema = get_schema()
            st.code(schema)

    except Exception as e:
        st.error(f"Database error: {e}")
        st.info("Run data/setup_db.py first!")

    st.divider()

    # ── Sample Questions ──────────────────────────────
    st.header("💡 Sample Questions")

    sample_questions = [
        "What is the total revenue?",
        "Show top 5 regions by revenue",
        "Which product sells the most?",
        "Who is the top salesperson?",
        "Show customers from Technology industry",
        "What is revenue by product?",
        "Show monthly revenue trend",
        "Which customer has highest purchases?",
        "Compare discount impact on revenue",
        "Show sales by region and product"
    ]

    for q in sample_questions:
        if st.button(q, key=f"btn_{q}", width="stretch"):
            st.session_state.pending_question = q

    st.divider()

    # Clear history button
    if st.button("🗑️ Clear History", width="stretch"):
        st.session_state.history = []
        st.rerun()

# ── Main Area ─────────────────────────────────────────

# Check DB exists
if not os.path.exists("data/sales.db"):
    st.error("❌ Database not found!")
    st.info("Run this command first: `python data/setup_db.py`")
    st.stop()

# ── Query Input ───────────────────────────────────────
col1, col2 = st.columns([4, 1])

with col1:
    question = st.text_input(
        "Ask a question about your data:",
        placeholder="e.g. Show top 5 customers by revenue",
        key="question_input"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    ask_btn = st.button("🚀 Generate SQL", width="stretch")

# ── Handle Sidebar Button Questions ──────────────────
if "pending_question" in st.session_state:
    question = st.session_state.pending_question
    del st.session_state.pending_question
    ask_btn = True

# ── Process Question ──────────────────────────────────
if ask_btn and question:
    with st.spinner("🤔 Generating SQL..."):
        result = ask_question(question)

    # Store in history
    st.session_state.history.insert(0, result)

# ── Display History ───────────────────────────────────
if st.session_state.history:
    for i, result in enumerate(st.session_state.history):

        # Question header
        st.subheader(f"❓ {result['question']}")

        # Two columns — SQL + Results
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("**🔍 Generated SQL:**")
            st.code(result["sql"], language="sql")

        with col2:
            st.markdown("**📊 Results:**")
            if result["status"] == "success":
                if result["data"] is not None and not result["data"].empty:
                    st.dataframe(
                        result["data"],
                        use_container_width=True
                    )
                    st.caption(f"✅ {result['rows']} rows returned")
                else:
                    st.info("No results found")
            else:
                st.error(result["status"])

        st.divider()

else:
    # No history yet — show welcome
    st.info("👆 Type a question above or click a sample question!")

    # Show sample data preview
    st.subheader("📋 Database Preview")
    tab1, tab2 = st.tabs(["Sales Table", "Customers Table"])

    with tab1:
        df, _ = __import__('src.database', fromlist=['execute_query']).execute_query(
            "SELECT * FROM sales LIMIT 10"
        )
        st.dataframe(df, use_container_width=True)

    with tab2:
        df, _ = __import__('src.database', fromlist=['execute_query']).execute_query(
            "SELECT * FROM customers"
        )
        st.dataframe(df, use_container_width=True)