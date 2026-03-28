# 🤖 TechNova AI Assistant — LlamaIndex + LangChain RAG

> An intelligent multi-document AI assistant built with LlamaIndex (data layer) and LangChain (conversation layer). Ask questions across 4 TechNova company documents and get accurate, grounded answers with conversation memory.

---

## 🎯 What This Project Does

TechNova AI Assistant lets you chat with 4 company documents simultaneously:

- Ask **financial questions** → answers from Annual Report
- Ask **HR questions** → answers from HR Policy
- Ask **market questions** → answers from Market Research Report
- Ask **product questions** → answers from Product Catalog
- Ask **cross-document questions** → SubQuestionQueryEngine routes and combines answers automatically

The assistant only answers from document context — it never hallucates or makes up answers.

---

## ✨ Features

- **Multi-document RAG** — query across 4 PDFs simultaneously
- **SubQuestion Engine** — complex questions auto-split into sub-questions, routed to correct document
- **Conversation Memory** — remembers previous messages within a session
- **Grounded Answers** — says "I don't have that information" for out-of-scope questions
- **Simple vs Sub-Question toggle** — switch engines based on question complexity
- **Source context viewer** — see exactly which document chunks were retrieved
- **Sample questions** — sidebar quick-launch buttons
- **Session memory clear** — start fresh conversation anytime

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| UI | Streamlit | Chat interface, session state |
| Conversation | LangChain LCEL | Memory, prompt template, LLM chain |
| Retrieval | LlamaIndex | PDF loading, chunking, embedding, vector search |
| Query Engine | SubQuestionQueryEngine | Multi-document question routing |
| Embeddings | OpenAI text-embedding-3-small | Semantic search (1536 dimensions) |
| LLM | GPT-4o-mini | Answer generation |
| Vector Store | LlamaIndex local storage | Persisted index on disk |
| PDF Parsing | pypdf via PDFReader | Text extraction from PDF files |

---

## 🏗️ Project Architecture

```
User Question
     │
     ▼
┌─────────────────────────────────┐
│  Streamlit UI  (app.py)         │  ← Chat interface, session state
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  LangChain Layer  (chain.py)    │  ← Memory + Prompt + LCEL Chain
│  - ChatMessageHistory           │
│  - PromptTemplate               │
│  - prompt | llm | StrOutputParser│
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  LlamaIndex Layer (retriever.py)│  ← Simple + SubQuestion engines
│  - SimpleQueryEngine            │
│  - SubQuestionQueryEngine       │
│  - QueryEngineTool × 4          │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  Ingestion Layer  (ingest.py)   │  ← PDF load + chunk + embed + store
│  - SimpleDirectoryReader        │
│  - PDFReader (pypdf)            │
│  - VectorStoreIndex             │
│  - StorageContext (disk)        │
└─────────────────────────────────┘
```

---

## 📁 Project Structure

```
04-llamaindex-langchain-rag/
├── documents/
│   ├── 01_annual_report_2024.pdf
│   ├── 02_hr_policy_2024.pdf
│   ├── 03_market_research_2024.pdf
│   └── 04_product_catalog_2024.pdf
├── storage/                      ← Auto-generated vector index (git ignored)
├── ingest.py                     ← LlamaIndex: PDF load + embed + store
├── retriever.py                  ← LlamaIndex: simple + sub-question engines
├── chain.py                      ← LangChain: memory + prompt + LCEL chain
├── app.py                        ← Streamlit: chat UI
├── requirements.txt
├── .env                          ← API key (never pushed to GitHub)
├── .env.example                  ← Placeholder (safe to push)
├── .gitignore
└── README.md
```

---

## 🚀 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/usman-analyst/langchain-learning.git
cd langchain-learning/04-llamaindex-langchain-rag
```

### 2. Create and activate virtual environment
```bash
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
# Copy the example file
copy .env.example .env   # Windows
cp .env.example .env     # Mac/Linux

# Add your OpenAI API key to .env
OPENAI_API_KEY=your_actual_api_key_here
```

### 5. Build the vector index (run once)
```bash
python ingest.py
```

### 6. Run the app
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 💬 Sample Questions to Try

### Single-document questions (Simple Engine):
- "What is TechNova's total revenue in 2024?"
- "What is the work from home policy?"
- "Who are the main competitors of TechNova?"
- "What laptop series does TechNova offer?"

### Cross-document questions (Sub-Question Engine):
- "What is TechNova's revenue and what are the main competitor risks?"
- "Compare TechNova's financial performance with market growth trends"
- "What is the net profit and how does TechNova's market share compare to competitors?"

### Memory test questions (ask these in sequence):
1. "What is TechNova's total revenue?"
2. "What is their net profit?" ← "their" resolved via memory
3. "How does that compare to EBITDA?" ← context maintained

---

## 🧠 Key Concepts Learned

### LlamaIndex vs LangChain
| | LangChain (Project 03) | LlamaIndex (Project 04) |
|---|---|---|
| Load 4 PDFs | ~15 lines | 3 lines |
| Chunk documents | ~10 lines | 0 (auto) |
| Create embeddings | ~12 lines | 0 (auto) |
| Build vector store | ~8 lines | 1 line |
| **Total** | **~80 lines** | **~6 lines** |

### SubQuestionQueryEngine
LlamaIndex's built-in multi-document router. Complex questions are automatically decomposed into sub-questions, each routed to the correct document tool, and answers combined into one final response. Equivalent functionality in LangChain requires custom routing chains.

### get_or_build Pattern
```python
def get_index():
    if os.path.exists(STORAGE_DIR):
        return load_index()   # free — no API call
    else:
        return build_index()  # first time only — calls OpenAI API
```
Saves embedding API costs on every restart.

### Grounded AI
The prompt explicitly instructs the LLM to answer ONLY from retrieved context. Out-of-scope questions return "I don't have that information in the documents" instead of hallucinated answers — critical for enterprise trust.

---

## 📚 Part of LangChain Learning Series

| Project | Concept | Stack |
|---|---|---|
| 01 - CSV Chatbot | LangChain Agent | Pandas Agent + Streamlit |
| 02 - SQL Generator | LCEL Chain | SQLite + LangChain + Streamlit |
| 03 - Research Tool | RAG Pipeline | LangChain + ChromaDB + Streamlit |
| **04 - TechNova AI Assistant** | **LlamaIndex + LangChain RAG** | **LlamaIndex + LangChain + Streamlit** |

---

## 👤 Author

**Usman Sharif** — Data Analyst transitioning to AI/LLM Engineer

[![GitHub](https://img.shields.io/badge/GitHub-usman--analyst-black?logo=github)](https://github.com/usman-analyst)