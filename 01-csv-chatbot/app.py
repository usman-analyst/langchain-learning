import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from src.data_loader import load_csv, get_column_info
from src.chain import build_csv_agent, ask_question

load_dotenv()

# ── Page Config ───────────────────────────────────────
st.set_page_config(
    page_title="CSV Analytics Chatbot",
    page_icon="📊",
    layout="wide"
)

# ── Session State ─────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "df" not in st.session_state:
    st.session_state.df = None

# ── Header ────────────────────────────────────────────
st.title("📊 CSV Analytics Chatbot")
st.markdown("Upload any CSV file and ask questions in plain English!")
st.divider()

# ── Sidebar ───────────────────────────────────────────
with st.sidebar:
    st.header("📁 Upload Data")

    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    st.markdown("**OR**")
    use_sample = st.button("📊 Use Sample Sales Data", width="stretch")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        st.session_state.agent = build_csv_agent(df)
        st.session_state.messages = []
        st.success(f"✅ Loaded {len(df)} rows!")

    if use_sample:
        if os.path.exists("data/sample_sales.csv"):
            df, _ = load_csv("data/sample_sales.csv")
            st.session_state.df = df
            st.session_state.agent = build_csv_agent(df)
            st.session_state.messages = []
            st.success(f"✅ Loaded {len(df)} rows!")
        else:
            st.error("Run generate_data.py first!")

    if st.session_state.df is not None:
        st.divider()
        st.header("📋 Data Info")
        df = st.session_state.df
        st.metric("Rows", len(df))
        st.metric("Columns", len(df.columns))
        col_info = get_column_info(df)
        st.markdown("**Columns:**")
        for col in col_info["all"]:
            st.markdown(f"- `{col}`")

        st.divider()
        st.header("💡 Sample Questions")
        sample_questions = [
            "What is the total revenue?",
            "Which region has highest sales?",
            "Who is the top salesperson?",
            "What is the best selling product?",
            "Show monthly revenue trend",
            "Compare revenue by region"
        ]
        for q in sample_questions:
            if st.button(q, key=f"btn_{q}", width="stretch"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": q
                })
                with st.spinner("🤔 Thinking..."):
                    answer = ask_question(st.session_state.agent, q)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

# ── Main Area ─────────────────────────────────────────
if st.session_state.df is None:
    st.info("👈 Upload a CSV file or use sample data to get started!")
    if os.path.exists("data/sample_sales.csv"):
        st.subheader("📊 Sample Data Preview")
        preview_df = pd.read_csv("data/sample_sales.csv")
        st.dataframe(preview_df.head(10), use_container_width=True)

else:
    # Data preview
    with st.expander("👀 Preview Data", expanded=False):
        st.dataframe(st.session_state.df.head(10), use_container_width=True)

    # Display all chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input at bottom
    question = st.chat_input("Ask anything about your data...")

    if question:
        # Add user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        # Display user message
        with st.chat_message("user"):
            st.markdown(question)

        # Get and display answer
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                answer = ask_question(st.session_state.agent, question)
            st.markdown(answer)

        # Save answer to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })