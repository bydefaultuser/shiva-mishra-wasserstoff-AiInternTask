import os
import logging
from functools import lru_cache
from typing import Optional

# Lazy-import HuggingFace to avoid loading at startup
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    HuggingFaceEmbeddings = None

logger = logging.getLogger(__name__)

# Embedding model configuration
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-MiniLM-L3-v2")
EMBEDDING_DEVICE = os.getenv("EMBEDDING_DEVICE", "cpu")
EMBEDDING_BATCH_SIZE = int(os.getenv("EMBEDDING_BATCH_SIZE", 16))

@lru_cache(maxsize=1)
def get_embedder():
    """Lazy-load embeddings model only when needed"""
    if HuggingFaceEmbeddings is None:
        logger.error("❌ HuggingFaceEmbeddings not available — package not installed")
        raise ImportError("langchain-huggingface not installed")

    try:
        logger.info(f"🧠 Loading embedding model: {EMBEDDING_MODEL} on {EMBEDDING_DEVICE}")
        return HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": EMBEDDING_DEVICE},
            encode_kwargs={"device": EMBEDDING_DEVICE}
        )
    except Exception as e:
        logger.error(f"❌ Failed to load embeddings: {str(e)}", exc_info=True)
        raise RuntimeError(f"Failed to load embeddings even on CPU: {e}") from e