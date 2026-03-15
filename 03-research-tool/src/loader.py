import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


# ── Constants ─────────────────────────────────────────
DOCUMENTS_DIR = "documents"
# CHUNK_SIZE     = 1000
# CHUNK_OVERLAP  = 200

CHUNK_SIZE    = 1500
CHUNK_OVERLAP = 300
# ── Load Single PDF ───────────────────────────────────
def load_pdf(file_path: str) -> List[Document]:
    """Load a single PDF and return list of documents."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF not found: {file_path}")

    loader = PyPDFLoader(file_path)
    pages  = loader.load()

    print(f"   📄 {os.path.basename(file_path)}: {len(pages)} pages")
    return pages


# ── Load All PDFs ─────────────────────────────────────
def load_all_documents(docs_dir: str = DOCUMENTS_DIR) -> List[Document]:
    """
    Load all PDFs from documents folder.
    Returns list of all pages across all PDFs.
    """
    if not os.path.exists(docs_dir):
        raise FileNotFoundError(
            f"Documents folder not found: {docs_dir}"
        )

    # Get all PDF files
    pdf_files = [
        f for f in os.listdir(docs_dir)
        if f.endswith(".pdf")
    ]

    if not pdf_files:
        raise ValueError(f"No PDF files found in {docs_dir}")

    print(f"🔄 Loading {len(pdf_files)} documents...")

    all_pages = []
    for pdf_file in sorted(pdf_files):
        file_path = os.path.join(docs_dir, pdf_file)
        pages     = load_pdf(file_path)
        all_pages.extend(pages)

    print(f"✅ Total pages loaded: {len(all_pages)}")
    return all_pages


# ── Split into Chunks ─────────────────────────────────
def split_documents(
    documents : List[Document],
    chunk_size   : int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP
) -> List[Document]:
    """
    Split documents into smaller chunks.
    Smaller chunks = better retrieval accuracy!
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size    = chunk_size,
        chunk_overlap = chunk_overlap,
        length_function = len,
        separators = ["\n\n", "\n", ".", " "]
    )

    chunks = splitter.split_documents(documents)

    print(f"✅ Total chunks created: {len(chunks)}")
    print(f"   chunk_size   : {chunk_size} characters")
    print(f"   chunk_overlap: {chunk_overlap} characters")

    return chunks


# ── Load and Split Together ───────────────────────────
def load_and_split(
    docs_dir     : str = DOCUMENTS_DIR,
    chunk_size   : int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP
) -> List[Document]:
    """
    Complete pipeline:
    Load PDFs → Split into chunks → Return chunks
    """
    pages  = load_all_documents(docs_dir)
    chunks = split_documents(pages, chunk_size, chunk_overlap)
    return chunks


# ── Get Document Stats ────────────────────────────────
def get_document_stats(chunks: List[Document]) -> dict:
    """
    Analyze chunks and return statistics.
    Useful for understanding what got loaded!
    """
    # Get unique sources
    sources = list(set([
        os.path.basename(chunk.metadata.get("source", "unknown"))
        for chunk in chunks
    ]))

    # Chunks per document
    chunks_per_doc = {}
    for chunk in chunks:
        source = os.path.basename(
            chunk.metadata.get("source", "unknown")
        )
        chunks_per_doc[source] = chunks_per_doc.get(source, 0) + 1

    # Average chunk length
    avg_length = sum(
        len(chunk.page_content) for chunk in chunks
    ) / len(chunks)

    return {
        "total_chunks"   : len(chunks),
        "total_documents": len(sources),
        "sources"        : sources,
        "chunks_per_doc" : chunks_per_doc,
        "avg_chunk_length": round(avg_length, 0)
    }


# ── Quick Test ────────────────────────────────────────
if __name__ == "__main__":

    # Load and split
    chunks = load_and_split()

    print()

    # Show stats
    stats = get_document_stats(chunks)
    print("📊 Document Statistics:")
    print(f"   Total documents : {stats['total_documents']}")
    print(f"   Total chunks    : {stats['total_chunks']}")
    print(f"   Avg chunk length: {stats['avg_chunk_length']} chars")

    print("\n   Chunks per document:")
    for doc, count in stats["chunks_per_doc"].items():
        print(f"   → {doc}: {count} chunks")

    # Show sample chunk
    print("\n📋 Sample Chunk:")
    print(f"   Source : {chunks[0].metadata}")
    print(f"   Content: {chunks[0].page_content[:200]}...")