"""
tools/rag_tool.py — RAG Document Search Tool
==============================================
Responsibility: Answer questions about TechNova company documents
                using LlamaIndex vector search.

Reuses the ingestion + retrieval logic from Project 04
(LlamaIndex + LangChain RAG) but wrapped as a LangGraph tool.

When to use this tool:
    - Questions about TechNova company information
    - Annual report, HR policy, market research, product catalog
    - Examples: "TechNova revenue", "WFH policy", "main competitors"
"""

import os
from dotenv import load_dotenv
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    Settings,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.readers.file import PDFReader

load_dotenv()

# -------------------------------------------------------------------
# LlamaIndex Global Settings — same as Project 04
# -------------------------------------------------------------------
Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.chunk_size = 512
Settings.chunk_overlap = 50

# -------------------------------------------------------------------
# Paths — documents and persisted index storage
# -------------------------------------------------------------------
DOCS_DIR    = "./data/documents"
STORAGE_DIR = "./data/storage"

# -------------------------------------------------------------------
# Global index cache — loaded once, reused across all tool calls
# Avoids reloading the index on every question (saves time + API cost)
# -------------------------------------------------------------------
_index_cache = None


def get_index() -> VectorStoreIndex:
    """
    Get the LlamaIndex vector index (cached after first load).

    Uses the same get_or_build pattern from Project 04:
        - storage exists → load from disk (free)
        - storage missing → build fresh (calls OpenAI API once)

    Returns:
        VectorStoreIndex ready for querying
    """
    global _index_cache

    # Return cached index if already loaded
    if _index_cache is not None:
        return _index_cache

    if os.path.exists(STORAGE_DIR):
        # Load from disk — no API cost
        print("Loading RAG index from storage...")
        storage_context = StorageContext.from_defaults(
            persist_dir=STORAGE_DIR
        )
        _index_cache = load_index_from_storage(storage_context)
    else:
        # Build fresh — calls OpenAI Embeddings API
        print("Building RAG index from documents...")
        if not os.path.exists(DOCS_DIR):
            raise FileNotFoundError(
                f"Documents folder not found: {DOCS_DIR}\n"
                "Please copy TechNova PDFs to data/documents/"
            )

        documents = SimpleDirectoryReader(
            DOCS_DIR,
            file_extractor={".pdf": PDFReader()}
        ).load_data()

        _index_cache = VectorStoreIndex.from_documents(documents)
        _index_cache.storage_context.persist(persist_dir=STORAGE_DIR)
        print(f"RAG index built and saved to {STORAGE_DIR}")

    return _index_cache


def run_rag_tool(question: str) -> str:
    """
    Answer a question about TechNova documents using RAG.

    Flow:
        1. Load vector index (from cache or disk)
        2. Embed the question → find similar chunks
        3. LLM generates answer from retrieved chunks

    Args:
        question: Natural language question about TechNova

    Returns:
        str: Answer grounded in TechNova document content
    """
    try:
        index = get_index()
        query_engine = index.as_query_engine(similarity_top_k=6)
        response = query_engine.query(question)
        return str(response)

    except FileNotFoundError as e:
        return f"RAG Tool Setup Error: {str(e)}"
    except Exception as e:
        return f"RAG Tool Error: {str(e)}"


# -------------------------------------------------------------------
# Quick test
# Usage: python -m tools.rag_tool
# -------------------------------------------------------------------
if __name__ == "__main__":
    questions = [
        "What is TechNova's total revenue in 2024?",
        "What is the work from home policy?",
        "Who are the main competitors?"
    ]

    for q in questions:
        print(f"Q: {q}")
        print(f"A: {run_rag_tool(q)}")
        print()