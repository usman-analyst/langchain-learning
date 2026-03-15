# 🔍 TechNova Research Assistant

> Ask questions across multiple business documents — 
> get accurate answers with source citations!

Built with **LangChain RAG** + **ChromaDB** + **OpenAI** + **Streamlit**

---

## 🎯 What This Project Does

A RAG (Retrieval Augmented Generation) system that allows
you to chat with multiple business documents simultaneously.

Instead of reading through 50+ pages manually:
- ❌ Read entire Annual Report to find revenue figures
- ✅ Ask: *"What is TechNova revenue growth in 2024?"*

---

## ✨ Features

- 📚 Multi-document support (4 business PDFs)
- 💬 Natural language questions
- 📄 Source citations with every answer
- 🧠 Semantic search across all documents
- 🔍 ChromaDB vector store for fast retrieval
- ❌ Honest "I don't know" when answer not found
- ⚡ Cached vector store — fast after first load

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| LangChain RAG | Retrieval pipeline |
| OpenAI Embeddings | text-embedding-3-small |
| ChromaDB | Vector database |
| GPT-4o-mini | Answer generation |
| PyPDF | PDF document loading |
| ReportLab | PDF generation |
| Streamlit | Web UI |
| Python 3.10+ | Core language |

---

## 📚 TechNova Documents

| Document | Pages | Contents |
|----------|-------|----------|
| Annual Report 2024 | 2 | Revenue, regional performance, products |
| HR Policy 2024 | 2 | Leave, WFH, increments, benefits |
| Market Research 2024 | 2 | Competitors, trends, risks |
| Product Catalog 2024 | 2 | Products, pricing, sales data |

---

## 🧠 How RAG Works
```
Your Question
      ↓
OpenAI converts question to numbers (embeddings)
      ↓
ChromaDB finds most similar document chunks
      ↓
Relevant chunks + question sent to GPT-4o-mini
      ↓
Answer generated from document context only
      ↓
Response with source document citations
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/usman-analyst/langchain-learning.git
cd langchain-learning/03-research-tool
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup environment variables
```bash
cp .env.example .env
# Add your OpenAI API key in .env
OPENAI_API_KEY=your_key_here
```

### 5. Generate TechNova documents
```bash
python generate_docs.py
```

### 6. Run the app
```bash
streamlit run app.py
```

Open browser at `http://localhost:8501`

---

## 📁 Project Structure
```
03-research-tool/
│
├── documents/                    # PDF documents
│   ├── 01_annual_report_2024.pdf
│   ├── 02_hr_policy_2024.pdf
│   ├── 03_market_research_2024.pdf
│   └── 04_product_catalog_2024.pdf
│
├── vector_store/                 # ChromaDB (auto-generated)
│
├── src/
│   ├── loader.py                 # PDF loading + chunking
│   ├── embeddings.py             # Vector store management
│   ├── chain.py                  # RAG chain
│   └── utils.py                  # Helper functions
│
├── app.py                        # Streamlit UI
├── generate_docs.py              # PDF generator
├── requirements.txt              # Dependencies
├── .env.example                  # Environment template
└── README.md                     # This file
```

---

## 💡 Sample Questions to Try
```
# Financial Questions
"What is TechNova total revenue in 2024?"
"Which region has highest revenue?"
"What is the revenue growth compared to last year?"

# HR Questions  
"What is the WFH policy?"
"How many days of annual leave do employees get?"
"What is the salary increment for exceptional performers?"

# Market Questions
"Who are TechNova main competitors?"
"What is TechNova market share?"
"What are the key market trends?"

# Product Questions
"Which product has highest revenue?"
"What is the pricing of TechNova laptops?"
"Which product is growing fastest?"

# Cross Document Questions
"What are the risks and how does HR policy address talent retention?"
"Compare TechNova revenue with competitors"
"What are the 2025 growth targets and which products will drive them?"
```

---

## 🧠 Key Concepts Learned

- **RAG Pipeline** — Retrieval Augmented Generation pattern
- **Embeddings** — Converting text to semantic vectors
- **ChromaDB** — Vector database for similarity search
- **Semantic Search** — Finding content by meaning not keywords
- **Chunk Strategy** — Size and overlap tuning for accuracy
- **Source Citations** — Grounding answers in documents
- **@st.cache_resource** — Caching expensive ML operations

---

## ⚠️ RAG Tuning Notes
```
chunk_size    : 1500 characters
chunk_overlap : 300 characters  
k (retrieval) : 6 chunks
embedding     : text-embedding-3-small
```

> These parameters affect answer quality.
> Larger chunks = more context but higher cost.
> k=6 retrieves more chunks for better coverage.

---

## 🚀 Part of My LangChain Learning Series

| Project | Description | Status |
|---------|-------------|--------|
| 01 - CSV Chatbot | Chat with CSV using AI Agent | ✅ Complete |
| 02 - SQL Generator | Natural language to SQL | ✅ Complete |
| 03 - Research Tool | Multi-document RAG system | ✅ Complete |
| 04 - Analysis Agent | Autonomous data analysis | 🔜 Coming Soon |

---

## 👨‍💻 Author

**Usman Sharif** — Data Analyst learning AI/LangChain development

[![GitHub](https://img.shields.io/badge/GitHub-usman--analyst-black?logo=github)](https://github.com/usman-analyst)

---

*Built with ❤️ as part of project-based LangChain learning*