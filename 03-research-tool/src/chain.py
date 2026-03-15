import os
import sys
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from embeddings import get_or_build_vector_store, get_retriever


# ── RAG Prompt ────────────────────────────────────────
RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful business analyst
assistant for TechNova Solutions.

Answer questions using ONLY the context provided below.
If the answer is partially in the context, share what
you know and mention what is missing.
Only say "I don't have enough information" if the topic
is completely absent from the context.

Always mention which document your answer comes from.
Be specific with numbers, percentages and facts.

Context:
{context}
"""),
    ("human", "{question}")
])

# ── Format Documents ──────────────────────────────────
def format_docs(docs: List[Document]) -> str:
    """
    Format retrieved chunks into single string.
    Each chunk labeled with its source document.
    """
    formatted = []
    for i, doc in enumerate(docs):
        source = os.path.basename(
            doc.metadata.get("source", "unknown")
        )
        formatted.append(
            f"[Source {i+1}: {source}]\n{doc.page_content}"
        )
    return "\n\n".join(formatted)


# ── Get Sources ───────────────────────────────────────
def get_sources(docs: List[Document]) -> List[str]:
    """Extract unique source document names."""
    sources = list(set([
        os.path.basename(
            doc.metadata.get("source", "unknown")
        )
        for doc in docs
    ]))
    return sources


# ── Build RAG Chain ───────────────────────────────────
def build_rag_chain(retriever):
    """
    Build complete RAG chain using LCEL.

    Pipeline:
    question → retriever → format_docs → prompt → llm → parser

    RunnablePassthrough passes question through unchanged
    while retriever fetches relevant chunks simultaneously.
    """
    llm = ChatOpenAI(
        model      = "gpt-4o-mini",
        temperature= 0
    )

    # ── LCEL RAG Chain ────────────────────────────────
    rag_chain = (
        {
            # Retrieve relevant chunks + format them
            "context" : retriever | format_docs,
            # Pass question through unchanged
            "question": RunnablePassthrough()
        }
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )

    return rag_chain


# ── Ask Question ──────────────────────────────────────
def ask_question(
    rag_chain,
    retriever,
    question: str
) -> dict:
    try:
        answer  = rag_chain.invoke(question)
        docs    = retriever.invoke(question)
        sources = get_sources(docs)
        return {
            "question": question,
            "answer"  : answer,
            "sources" : sources,
            "status"  : "success"
        }
    except Exception as e:
        return {
            "question": question,
            "answer"  : f"❌ Error: {str(e)}",
            "sources" : [],
            "status"  : "error"
        }


# ── Quick Test ────────────────────────────────────────
if __name__ == "__main__":

    print("🔄 Loading vector store...")
    vectorstore = get_or_build_vector_store()
    retriever   = get_retriever(vectorstore)

    print("🤖 Building RAG chain...")
    rag_chain   = build_rag_chain(retriever)

    print("✅ RAG chain ready!\n")

    # Test questions — across all documents!
    questions = [
        "What is TechNova total revenue in 2024?",
        "What is the WFH policy at TechNova?",
        "Who are TechNova main competitors?",
        "Which product has highest revenue?",
        "What are the key risks for TechNova?",
        "What is the salary increment for exceptional performers?"
    ]

    print("=" * 60)
    for q in questions:
        result = ask_question(rag_chain, retriever, q)
        print(f"\n❓ Question: {result['question']}")
        print(f"\n💡 Answer  : {result['answer']}")
        print(f"\n📄 Sources : {', '.join(result['sources'])}")
        print("=" * 60)