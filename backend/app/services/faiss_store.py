import os
import pickle
from pathlib import Path
import logging
from typing import List, Optional, Dict

from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use /tmp for ephemeral storage
FAISS_PATH = os.getenv("FAISS_PATH", "/tmp/faiss_index")
VDB_PATH = Path(FAISS_PATH).with_suffix(".pkl")  # Save as .pkl file

def _save_index(vstore: FAISS):
    """Save FAISS index to disk"""
    try:
        # Ensure directory exists in /tmp
        VDB_PATH.parent.mkdir(parents=True, exist_ok=True)

        with open(VDB_PATH, "wb") as f:
            pickle.dump(vstore, f)

        logger.info(f"💾 FAISS index saved to {VDB_PATH}")
    except Exception as e:
        logger.error(f"❌ Failed to save FAISS index: {str(e)}")

def _load_index() -> Optional[FAISS]:
    """Load FAISS index from disk if available"""
    try:
        if not VDB_PATH.exists():
            logger.warning("⚠️ No existing FAISS index found")
            return None

        with open(VDB_PATH, "rb") as f:
            index = pickle.load(f)

        logger.info("🧠 Loaded existing FAISS index")
        return index
    except Exception as e:
        logger.error(f"❌ Failed to load FAISS index: {str(e)}")
        return None

def store_chunks(
    embedder: Embeddings,
    chunks: List[str],
    metadatas: List[dict],
):
    """
    Stores text chunks and metadata into a FAISS vector store.
    Creates new index or appends to existing one.
    """
    try:
        docs = [Document(page_content=c, metadata=m) for c, m in zip(chunks, metadatas)]

        index = _load_index()
        if index:
            logger.info("🔄 Appending to existing FAISS index")
            index.add_documents(docs)
        else:
            logger.info("🆕 Creating new FAISS index")
            index = FAISS.from_documents(docs, embedder)

        _save_index(index)
    except Exception as e:
        logger.error(f"❌ Failed to store chunks: {str(e)}")
        raise

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
    try:
        index = _load_index()
        if not index:
            raise RuntimeError("No FAISS index found. Upload documents first.")

        docs_and_scores = index.similarity_search_with_score(question, k=k)

        # Apply filename filter if provided
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
    except Exception as e:
        logger.error(f"❌ Query failed: {str(e)}")
        raise