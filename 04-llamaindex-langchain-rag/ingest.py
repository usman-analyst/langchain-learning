"""
ingest.py — LlamaIndex Data Ingestion Layer
============================================
Responsibility: Load PDFs → Chunk → Embed → Store index to disk

This replaces ~50 lines of LangChain code (loader.py + embeddings.py)
with ~30 lines using LlamaIndex's built-in pipeline.

Run this file ONCE to build the index.
After that, get_index() loads from disk automatically (no API cost).
"""

import os
from dotenv import load_dotenv
from llama_index.core import (
    SimpleDirectoryReader,   # Reads all files in a directory automatically
    VectorStoreIndex,        # Chunks + embeds + stores in one step
    StorageContext,          # Manages where data is saved/loaded from
    load_index_from_storage, # Loads a previously saved index from disk
    Settings,                # Global config for LLM + embeddings + chunking
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.readers.file import PDFReader  # Explicit PDF reader using pypdf

# -------------------------------------------------------------------
# Load environment variables from .env file
# -------------------------------------------------------------------
load_dotenv()

# -------------------------------------------------------------------
# Global LlamaIndex Settings
# Set once here — automatically applies to all files that import this
# In LangChain we had to pass llm/embeddings to every function manually
# -------------------------------------------------------------------
Settings.llm = OpenAI(
    model="gpt-4o-mini",
    temperature=0  # temperature=0 → consistent, deterministic answers
)
Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-small"  # 1536 dimensions, cost-efficient
)
Settings.chunk_size = 512      # Smaller chunks → more precise retrieval
Settings.chunk_overlap = 50    # Overlap to preserve context at boundaries

# -------------------------------------------------------------------
# Directory Paths
# -------------------------------------------------------------------
DOCS_DIR = "./documents"   # Folder containing the 4 TechNova PDFs
STORAGE_DIR = "./storage"  # LlamaIndex saves the index here (like ChromaDB)


def build_index() -> VectorStoreIndex:
    """
    Build a fresh vector index from PDF documents.

    Steps:
        1. Load all PDFs from DOCS_DIR
        2. Chunk + embed all documents (VectorStoreIndex handles this)
        3. Save index to STORAGE_DIR for future reuse

    Returns:
        VectorStoreIndex: The built index ready for querying

    Note:
        This calls the OpenAI Embeddings API — costs a small amount.
        Run only once. Use load_index() or get_index() after that.
    """
    print("Loading PDFs from documents/ folder ...")
    # Explicitly pass PDFReader so LlamaIndex uses pypdf for text extraction
    # Without this, SimpleDirectoryReader reads raw PDF bytes instead of text
    documents = SimpleDirectoryReader(
        DOCS_DIR,
        file_extractor={".pdf": PDFReader()}
    ).load_data()
    print(f"Loaded {len(documents)} document pages from PDFs")

    print("Building VectorStoreIndex — chunking + embedding ...")
    # This single line does what took ~30 lines in LangChain:
    # RecursiveCharacterTextSplitter + OpenAIEmbeddings + Chroma.from_documents
    index = VectorStoreIndex.from_documents(
        documents,
        show_progress=True  # Shows a progress bar while embedding
    )

    print(f"Saving index to {STORAGE_DIR}/ ...")
    index.storage_context.persist(persist_dir=STORAGE_DIR)
    print("Index saved successfully! Use get_index() from now on.")

    return index


def load_index() -> VectorStoreIndex:
    """
    Load a previously saved index from disk.

    This does NOT call the OpenAI API — completely free to run.
    Use this after build_index() has been run at least once.

    Returns:
        VectorStoreIndex: The loaded index ready for querying
    """
    print(f"Loading existing index from {STORAGE_DIR}/ ...")
    storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
    index = load_index_from_storage(storage_context)
    print("Index loaded successfully!")

    return index


def get_index() -> VectorStoreIndex:
    """
    Smart index loader — automatically decides build vs load.

    Logic:
        - If storage/ folder exists → load from disk (fast, free)
        - If storage/ does not exist → build fresh index (first time only)

    This is the ONLY function other files should call.
    retriever.py, chain.py, and app.py all use get_index().

    Returns:
        VectorStoreIndex: Index ready for querying
    """
    if os.path.exists(STORAGE_DIR):
        return load_index()
    else:
        return build_index()


# -------------------------------------------------------------------
# Quick test — run this file directly to verify everything works
# Usage: python ingest.py
# -------------------------------------------------------------------
if __name__ == "__main__":
    index = get_index()

    print("\n--- Quick Test Query ---")
    query_engine = index.as_query_engine()
    response = query_engine.query("What are the main topics in these documents?")
    print(f"\nResponse: {response}")