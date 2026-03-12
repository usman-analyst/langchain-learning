# 📊 CSV Analytics Chatbot

> Ask questions about your CSV data in plain English — no SQL, no coding needed!

Built with **LangChain** + **OpenAI** + **Streamlit** as part of my AI/LangChain learning journey.

---

## 🎯 What This Project Does

A Data Analyst's dream tool — upload any CSV file and chat with your data naturally.

Instead of writing pandas code or SQL queries:
- ❌ `df.groupby('region')['revenue'].sum().idxmax()`
- ✅ Just ask: *"Which region has the highest sales?"*

---

## ✨ Features

- 📁 Upload any CSV file or use built-in sample sales data
- 💬 Ask questions in plain English
- 🤖 AI automatically writes and executes pandas code
- 📋 See data preview and column info in sidebar
- 💡 Quick sample questions for instant insights
- 🧠 Powered by LangChain Pandas Agent + GPT-4o-mini

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| LangChain | AI Agent framework |
| OpenAI GPT-4o-mini | Language model |
| Streamlit | Web UI |
| Pandas | Data processing |
| Python 3.10+ | Core language |

---

## 📸 Demo

### Chat Interface
Ask natural language questions and get instant answers:

| Question | Answer |
|----------|--------|
| What is the total revenue? | $5,082,801 |
| Which region has highest sales? | West ($1,597,652) |
| Who is the top salesperson? | Arjun |
| What is the best selling product? | Tablet |
| What is the average discount? | 10.33% |

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/usman-analyst/langchain-learning.git
cd langchain-learning/01-csv-chatbot
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
# Copy example env file
cp .env.example .env

# Add your OpenAI API key in .env
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Generate sample data
```bash
python generate_data.py
```

### 6. Run the app
```bash
streamlit run app.py
```

Open browser at `http://localhost:8501`

---

## 📁 Project Structure
```
01-csv-chatbot/
│
├── data/
│   └── sample_sales.csv      # 500 rows synthetic sales data
│
├── src/
│   ├── data_loader.py        # CSV loading and validation
│   ├── chain.py              # LangChain Pandas Agent
│   └── utils.py              # Helper functions
│
├── tests/
│   └── test_chain.py         # Unit tests
│
├── app.py                    # Streamlit UI
├── generate_data.py          # Sample data generator
├── requirements.txt          # Dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

---

## 💡 Sample Questions to Try
```
# Revenue Analysis
"What is the total revenue?"
"Which month had the highest revenue?"
"Show monthly revenue trend"

# Regional Analysis  
"Which region has the highest sales?"
"Compare revenue across all regions"

# Product Analysis
"What is the best selling product?"
"Which product generates most revenue?"
"Show revenue breakdown by product"

# Salesperson Analysis
"Who is the top performing salesperson?"
"Compare all salesperson performance"

# General
"What is the average discount?"
"How many units were sold in total?"
```

---

## 🧠 Key Concepts Learned

- **LangChain Pandas Agent** — AI that writes and executes pandas code automatically
- **Streamlit Session State** — Persisting data between user interactions
- **LCEL Chains** — Connecting LangChain components with pipe operator
- **Prompt Engineering** — Getting accurate data answers from LLM
- **Professional Project Structure** — Modular, maintainable code

---

## 🚀 Part of My LangChain Learning Series

This is **Project 01** in my LangChain learning journey:

| Project | Description | Status |
|---------|-------------|--------|
| 01 - CSV Chatbot | Chat with CSV data using AI | ✅ Complete |
| 02 - SQL Generator | Natural language to SQL | 🔜 Coming Soon |
| 03 - Research Tool | Multi-document RAG | 🔜 Coming Soon |
| 04 - Analysis Agent | Autonomous data analysis | 🔜 Coming Soon |

---

## 👨‍💻 Author

**Usman Sharif** — Data Analyst learning AI/LangChain development

[![GitHub](https://img.shields.io/badge/GitHub-usman--analyst-black?logo=github)](https://github.com/usman-analyst)

---

*Built with ❤️ as part of project-based LangChain learning*