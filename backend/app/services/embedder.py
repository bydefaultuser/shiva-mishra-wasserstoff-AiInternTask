from config import TESSERACT_PATH  # Unused here but kept for consistency
from langchain_huggingface import HuggingFaceEmbeddings
from functools import lru_cache
import os
import logging
import torch

logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def get_embedder():
    """
    Load HuggingFace embedder with safe fallback to CPU.
    Uses environment variables for model name and device.
    """
    # Get environment variables with defaults
    model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L12-v2")
    device = os.getenv("EMBEDDING_DEVICE", "cpu").strip().lower()  # Default to CPU for GCP compatibility

    logger.info(f"🔍 Loading embedding model: {model_name} on device: {device}")

    try:
        # Try loading with specified device
        return HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": device},
            encode_kwargs={"batch_size": int(os.getenv("EMBEDDING_BATCH_SIZE", 16))}
        )
    except Exception as e:
        logger.error(f"❌ Failed to load embeddings on {device}: {str(e)}", exc_info=True)
        
        # Fallback to CPU if device is not available
        if device != "cpu":
            logger.warning("⚠️ Device unavailable or model failed. Falling back to CPU.")
            return HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs={"device": "cpu"},
                encode_kwargs={"batch_size": int(os.getenv("EMBEDDING_BATCH_SIZE", 16))}
            )
        else:
            raise RuntimeError(f"Failed to load embeddings even on CPU: {str(e)}") from e