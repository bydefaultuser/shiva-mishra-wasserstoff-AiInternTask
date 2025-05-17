from typing import List, Optional, Dict
import os
import pickle
from pathlib import Path
import logging

from langchain_community.vectorstores import FAISS   # LangChain’s FAISS wrapper
from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings

logger = logging.getLogger(__name__)

# Path to store the FAISS index
VDB_PATH = Path(os.getenv("FAISS_PATH", "vector_store/faiss_index")).with_suffix(".pkl")

def _save_index(vstore: FAISS):
    """Save FAISS index to disk."""
    VDB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(VDB_PATH, "wb") as f:
        pickle.dump(vstore, f)
    logger.info(f"💾  FAISS index saved → {VDB_PATH}")

def _load_index() -> Optional[FAISS]:
    """Load FAISS index from disk, if available."""
    if VDB_PATH.exists():
        with open(VDB_PATH, "rb") as f:
            return pickle.load(f)
    return None

def store_chunks(
    embedder: Embeddings,
    chunks: List[str],
    metadatas: List[dict],
):
    """
    Stores text chunks and metadata into a local FAISS vector store.
    Appends if an index already exists.
    """
    docs = [Document(page_content=c, metadata=m) for c, m in zip(chunks, metadatas)]

    index = _load_index()
    if index:
        logger.info("🔄  Appending to existing FAISS index")
        index.add_documents(docs)
    else:
        logger.info("🆕  Creating new FAISS index")
        index = FAISS.from_documents(docs, embedder)

    _save_index(index)

def query_chunks(
    embedder: Embeddings,
    question: str,
    k: int = 4,
    filters: Optional[Dict] = None
):
    """
    Queries the FAISS index and optionally filters results by metadata.
    Returns top-k most similar chunks.
    """
    index = _load_index()
    if not index:
        raise RuntimeError("No FAISS index found. Upload documents first.")

    docs_and_scores = index.similarity_search_with_score(question, k=k)

    if filters and "filename" in filters:
        allowed = set(filters["filename"]["$in"])
        original_count = len(docs_and_scores)
        docs_and_scores = [
            (doc, score)
            for doc, score in docs_and_scores
            if doc.metadata.get("filename") in allowed
        ]
        logger.info(f"📎 Filtered results by filename: {len(docs_and_scores)} / {original_count} retained")

    return [
        {
            "content": doc.page_content,
            "metadata": doc.metadata,
            "score": float(score)  # Ensure JSON serialization
        }
        for doc, score in docs_and_scores
    ]
