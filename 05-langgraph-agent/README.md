# 🤖 Multi-Tool AI Agent — LangGraph + LangChain

> An intelligent multi-tool AI agent built with LangGraph that automatically routes questions to the correct data source — CSV sales data, SQL database, TechNova documents, or LLM knowledge — without any manual routing logic.

---

## 🎯 What This Project Does

Ask any question in natural language. The agent automatically decides:

| Your Question | Agent Routes To |
|---|---|
| "What is total sales revenue?" | 🟢 CSV Tool — pandas analysis |
| "How many customers from Hyderabad?" | 🔵 SQL Tool — SQLite query |
| "What is TechNova's WFH policy?" | 🟣 RAG Tool — LlamaIndex document search |
| "What is artificial intelligence?" | 🟡 LLM — general knowledge |

Zero manual routing — LangGraph + LLM decides automatically!

---

## ✨ Features

- **Automatic tool routing** — LLM classifies question and routes to correct tool
- **4 data sources** — CSV, SQL, RAG documents, LLM knowledge
- **LangGraph state machine** — clean node-based architecture with conditional edges
- **Conversation memory** — chat history maintained across turns
- **Tool badge display** — shows which tool answered each question
- **Debug mode** — toggle raw tool output visibility
- **Sample questions** — sidebar quick-launch per tool category
- **Grounded responses** — out-of-scope questions handled by LLM honestly

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Agent Framework | LangGraph | State machine, node routing, conditional edges |
| LLM | GPT-4o-mini | Router decisions + final answer generation |
| CSV Analysis | LangChain Pandas Agent | Natural language → pandas code |
| SQL Queries | LangChain LCEL Chain | Natural language → SQLite queries |
| Document RAG | LlamaIndex | PDF ingestion, vector search, retrieval |
| Embeddings | OpenAI text-embedding-3-small | Semantic search for RAG |
| UI | Streamlit | Chat interface, session state |
| Database | SQLite | Structured sales + customer data |

---

## 🏗️ Architecture

```
User Question
      │
      ▼
┌─────────────────────┐
│   router_node       │  ← LLM classifies question → decides tool
│   (nodes.py)        │
└────────┬────────────┘
         │ decide_tool() — conditional edge
    ┌────┴─────────────────────┐
    │                          │
    ▼                          ▼
┌──────────┐            ┌────────────┐
│tool_node │            │  llm_node  │  ← llm_only questions skip tool
│(nodes.py)│            │ (nodes.py) │
└──────┬───┘            └─────┬──────┘
       │                      │
       └──────────┬───────────┘
                  ▼
           ┌────────────┐
           │  llm_node  │  ← polishes tool result into final answer
           └─────┬──────┘
                 ▼
                END
```

---

## 📁 Project Structure

```
05-langgraph-agent/
├── agent/
│   ├── __init__.py
│   ├── state.py          ← AgentState TypedDict (shared whiteboard)
│   ├── nodes.py          ← router_node, tool_node, llm_node, decide_tool
│   └── graph.py          ← StateGraph assembly + run_agent()
├── tools/
│   ├── __init__.py
│   ├── csv_tool.py       ← Pandas agent for CSV sales data
│   ├── sql_tool.py       ← LCEL chain for SQLite queries
│   └── rag_tool.py       ← LlamaIndex RAG for TechNova documents
├── data/
│   ├── sales_data.csv    ← 500 rows synthetic sales data
│   ├── setup_db.py       ← Creates SQLite DB with sales + customers
│   ├── documents/        ← TechNova PDFs (git ignored)
│   └── storage/          ← LlamaIndex vector index (git ignored)
├── app.py                ← Streamlit chat UI
├── requirements.txt
├── .env                  ← API key (never pushed)
├── .env.example          ← Placeholder (safe to push)
├── .gitignore
└── README.md
```

---

## 🚀 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/usman-analyst/langchain-learning.git
cd langchain-learning/05-langgraph-agent
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
.\venv\Scripts\pip.exe install -r requirements.txt
```

### 4. Set up environment variables
```bash
# Create .env with UTF-8 encoding
python -c "open('.env', 'w', encoding='utf-8').write('OPENAI_API_KEY=your_key_here\n')"
```

### 5. Set up data sources
```bash
# Create SQLite database
python data/setup_db.py

# Copy TechNova PDFs to data/documents/
# (PDFs available in 04-llamaindex-langchain-rag/documents/)
```

### 6. Run the app
```bash
.\venv\Scripts\python.exe -m streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 💬 Sample Questions to Try

### CSV Tool (sales data):
- "What is the total sales revenue?"
- "Which region has the highest sales?"
- "Top 3 products by revenue?"
- "What is the average order value?"

### SQL Tool (customer database):
- "How many customers are from Hyderabad?"
- "Top 5 customers by total spend?"
- "How many total orders are there?"
- "Which industry has the most customers?"

### RAG Tool (TechNova documents):
- "What is TechNova's total revenue in 2024?"
- "What is the work from home policy?"
- "Who are the main competitors?"
- "What products does TechNova sell?"

### LLM Only (general knowledge):
- "What is artificial intelligence?"
- "Explain LangGraph vs LangChain"
- "What is 2 + 2?"

---

## 🧠 Key Concepts Learned

### LangGraph Core Concepts
| Concept | Description |
|---|---|
| `StateGraph` | Graph that carries state between nodes |
| `AgentState` | TypedDict — shared whiteboard for all nodes |
| `add_node()` | Register a processing function as a node |
| `add_edge()` | Fixed connection A → B always |
| `add_conditional_edges()` | Dynamic routing — A → B or C based on condition |
| `set_entry_point()` | First node to execute |
| `compile()` | Validate + build runnable graph |
| `operator.add` | Append to list fields instead of overwrite |

### LangGraph vs LangChain Chain

| Feature | LangChain Chain | LangGraph |
|---|---|---|
| Flow | Linear A→B→C | Graph with loops + branches |
| Routing | Manual, hardcoded | Conditional edges, LLM decides |
| State | Per-chain inputs/outputs | Shared state across all nodes |
| Memory | Manual injection | Built into state |
| Use case | Fixed pipelines | Dynamic multi-step agents |

### Router Pattern
```python
# LLM classifies question into tool category
ROUTER_PROMPT = "Classify into: csv_tool, sql_tool, rag_tool, llm_only"
tool = router_chain.invoke({"question": question})

# Conditional edge routes to correct node
graph.add_conditional_edges("router_node", decide_tool, {
    "tool_node": "tool_node",
    "llm_node":  "llm_node"
})
```

---

## 📚 Part of LangChain Learning Series

| Project | Concept | Stack |
|---|---|---|
| 01 - CSV Chatbot | LangChain Agent | Pandas Agent + Streamlit |
| 02 - SQL Generator | LCEL Chain | SQLite + LangChain + Streamlit |
| 03 - Research Tool | RAG Pipeline | LangChain + ChromaDB + Streamlit |
| 04 - TechNova AI Assistant | LlamaIndex + LangChain RAG | LlamaIndex + LangChain + Streamlit |
| **05 - Multi-Tool AI Agent** | **LangGraph Agent** | **LangGraph + LangChain + LlamaIndex + Streamlit** |

---

## 👤 Author

**Usman Sharif** — Data Analyst transitioning to AI/LLM Engineer

[![GitHub](https://img.shields.io/badge/GitHub-usman--analyst-black?logo=github)](https://github.com/usman-analyst)