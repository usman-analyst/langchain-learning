# 🔍 SQL Generator Bot

> Type a question in plain English — get SQL query + results instantly!

Built with **LangChain LCEL Chains** + **OpenAI** + **Streamlit** + **SQLite**

---

## 🎯 What This Project Does

Converts natural language questions into SQL queries and executes them automatically.

Instead of writing SQL manually:
- ❌ `SELECT region, SUM(revenue) FROM sales GROUP BY region ORDER BY SUM(revenue) DESC`
- ✅ Just ask: *"Which region has the highest revenue?"*

---

## ✨ Features

- 💬 Natural language to SQL conversion
- 🔍 SQL syntax highlighted display
- 📊 Results shown as interactive table
- 🗄️ Multi-table database with JOIN support
- 📋 Schema viewer in sidebar
- 💡 Sample questions for quick start
- 🕐 Query history — see all previous questions
- ⚡ Powered by LangChain LCEL Chain + GPT-4o-mini

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| LangChain LCEL | Chain pipeline framework |
| OpenAI GPT-4o-mini | SQL generation |
| Streamlit | Web UI |
| SQLite | Local database |
| Pandas | Results processing |
| Python 3.10+ | Core language |

---

## 📸 Demo

### Natural Language → SQL → Results

| Question | Generated SQL |
|----------|--------------|
| Total revenue? | `SELECT SUM(revenue) FROM sales` |
| Top region? | `SELECT region, SUM(revenue)... GROUP BY region ORDER BY...` |
| Best salesperson per region? | Nested subquery with HAVING clause |
| Revenue by industry? | JOIN between sales and customers tables |

---

## 🗄️ Database Schema
```
sales table (500 rows)
├── date          TEXT
├── customer      TEXT
├── region        TEXT
├── product       TEXT
├── salesperson   TEXT
├── units_sold    INTEGER
├── discount_pct  REAL
├── unit_price    REAL
└── revenue       REAL

customers table (10 rows)
├── customer_name TEXT
├── industry      TEXT
├── city          TEXT
└── since_year    INTEGER
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/usman-analyst/langchain-learning.git
cd langchain-learning/02-sql-generator
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
```

### 5. Create database
```bash
python data/setup_db.py
```

### 6. Run the app
```bash
streamlit run app.py
```

Open browser at `http://localhost:8501`

---

## 📁 Project Structure
```
02-sql-generator/
│
├── data/
│   ├── setup_db.py       # Database creation script
│   └── sales.db          # SQLite database (auto-generated)
│
├── src/
│   ├── database.py       # DB connection, schema reader, query executor
│   ├── chain.py          # LangChain LCEL Chain for SQL generation
│   └── utils.py          # Helper functions
│
├── tests/
│   └── test_chain.py     # Unit tests
│
├── app.py                # Streamlit UI
├── requirements.txt      # Dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

---

## 💡 Sample Questions to Try
```
# Basic Queries
"What is the total revenue?"
"Show all regions and their revenue"
"How many units were sold in total?"

# Aggregations
"Which product sells the most units?"
"What is the average discount percentage?"
"Show revenue by product"

# Advanced Queries
"Which salesperson performs best in each region?"
"Show monthly revenue trend for Laptop only"
"Which month had the highest revenue?"

# JOIN Queries
"Show total revenue by industry"
"Which industry generates most revenue?"
"Show customers with their total purchases"

# Complex Analysis
"Show top 3 products for each region"
"Compare salesperson performance across regions"
"Show month wise regional revenue breakdown"
```

---

## 🧠 Key Concepts Learned

- **LCEL Chain** — Pipe operator `|` connecting Prompt → LLM → Parser
- **Prompt Engineering** — Schema injection for accurate SQL generation
- **SQLite** — Lightweight local database with Python
- **Multi-table JOIN** — AI handles relationships between tables
- **Output Parsing** — Cleaning LLM output to pure SQL
- **Schema as Context** — Giving AI database map for better results

---

## ⚠️ Important Notes

- Always validate AI generated SQL before using in production
- Complex window functions may need manual review
- Schema quality directly affects SQL accuracy
- Temperature=0 ensures consistent SQL generation

---

## 🔄 How It Works
```
Your Question
     ↓
ChatPromptTemplate
(fills schema + question)
     ↓
ChatOpenAI GPT-4o-mini
(generates SQL)
     ↓
StrOutputParser
(extracts clean SQL)
     ↓
SQLite Executor
(runs query)
     ↓
Streamlit Table
(displays results)
```

---

## 🚀 Part of My LangChain Learning Series

| Project | Description | Status |
|---------|-------------|--------|
| 01 - CSV Chatbot | Chat with CSV using AI Agent | ✅ Complete |
| 02 - SQL Generator | Natural language to SQL with LCEL Chain | ✅ Complete |
| 03 - Research Tool | Multi-document RAG | 🔜 Coming Soon |
| 04 - Analysis Agent | Autonomous data analysis | 🔜 Coming Soon |

---

## 👨‍💻 Author

**Usman Sharif** — Data Analyst learning AI/LangChain development

[![GitHub](https://img.shields.io/badge/GitHub-usman--analyst-black?logo=github)](https://github.com/usman-analyst)

---

*Built with ❤️ as part of project-based LangChain learning*