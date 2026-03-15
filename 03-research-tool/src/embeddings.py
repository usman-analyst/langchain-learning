import os
import sys
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from loader import load_and_split, get_document_stats

# ── Constants ─────────────────────────────────────────
VECTOR_STORE_DIR = "vector_store"
COLLECTION_NAME  = "technova_docs"


# ── Get Embeddings Model ──────────────────────────────
def get_embeddings():
    """
    OpenAI Embeddings model.
    Converts text → 1536 dimensional vector.
    """
    return OpenAIEmbeddings(
        model="text-embedding-3-small"  # cheap + accurate
    )


# ── Build Vector Store ────────────────────────────────
def build_vector_store(
    chunks    : List[Document],
    persist_dir: str = VECTOR_STORE_DIR
) -> Chroma:
    """
    Convert chunks to embeddings and store in ChromaDB.
    This is a ONE TIME operation — saves to disk!
    """
    print(f"🔄 Creating embeddings for {len(chunks)} chunks...")
    print(f"   This may take 30-60 seconds...")

    embeddings = get_embeddings()

    # Create ChromaDB vector store
    vectorstore = Chroma.from_documents(
        documents       = chunks,
        embedding       = embeddings,
        persist_directory = persist_dir,
        collection_name = COLLECTION_NAME
    )

    print(f"✅ Vector store created at: {persist_dir}/")
    print(f"   Total vectors stored: {vectorstore._collection.count()}")

    return vectorstore


# ── Load Existing Vector Store ────────────────────────
def load_vector_store(
    persist_dir: str = VECTOR_STORE_DIR
) -> Chroma:
    """
    Load existing ChromaDB from disk.
    Use this after first build — no need to rebuild every time!
    """
    if not os.path.exists(persist_dir):
        raise FileNotFoundError(
            f"Vector store not found at {persist_dir}. "
            f"Run build_vector_store() first!"
        )

    embeddings  = get_embeddings()
    vectorstore = Chroma(
        persist_directory = persist_dir,
        embedding_function = embeddings,
        collection_name   = COLLECTION_NAME
    )

    count = vectorstore._collection.count()
    print(f"✅ Vector store loaded: {count} vectors")

    return vectorstore


# ── Get or Build Vector Store ─────────────────────────
def get_or_build_vector_store(
    docs_dir   : str = "documents",
    persist_dir: str = VECTOR_STORE_DIR
) -> Chroma:
    """
    Smart function:
    - If vector store exists → load it (fast!)
    - If not → build it (slow, one time)
    """
    if os.path.exists(persist_dir) and \
       os.listdir(persist_dir):
        print("📂 Found existing vector store — loading...")
        return load_vector_store(persist_dir)
    else:
        print("🔨 Building new vector store...")
        chunks = load_and_split(docs_dir)
        return build_vector_store(chunks, persist_dir)


# ── Get Retriever ─────────────────────────────────────
def get_retriever(
    vectorstore: Chroma,
    k          : int = 4
):
    """
    Convert vectorstore to retriever.
    k = number of relevant chunks to retrieve per question.
    """
    return vectorstore.as_retriever(
        search_type   = "similarity",
        search_kwargs = {"k": k}
    )


# ── Test Retrieval ────────────────────────────────────
def test_retrieval(
    retriever,
    query: str
) -> None:
    """Test what chunks get retrieved for a query."""
    print(f"\n🔍 Query: {query}")
    docs = retriever.invoke(query)
    print(f"   Retrieved {len(docs)} chunks:")
    for i, doc in enumerate(docs):
        source = os.path.basename(
            doc.metadata.get("source", "unknown")
        )
        print(f"\n   Chunk {i+1} — {source}")
        print(f"   {doc.page_content[:150]}...")


# ── Quick Test ────────────────────────────────────────
if __name__ == "__main__":

    # Build or load vector store
    vectorstore = get_or_build_vector_store()
    retriever   = get_retriever(vectorstore)

    print()

    # Test retrieval with sample queries
    test_queries = [
        "What is TechNova total revenue?",
        "What is the leave policy?",
        "Who are the competitors?",
        "Which product has highest sales?"
    ]

    for query in test_queries:
        test_retrieval(retriever, query)
        print("-" * 50)