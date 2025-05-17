from ..config import  TESSERACT_PATH
from langchain_huggingface import HuggingFaceEmbeddings
from functools import lru_cache
import os
import logging
import torch
torch.cuda.is_available()


logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def get_embedder():
    """Load HuggingFace embedder with safe fallback to CPU and better logging."""
    model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L12-v2")
    device = os.getenv("EMBEDDING_DEVICE", "cuda").strip()

    logger.info(f"🔍 Loading embedding model: {model_name} on device: {device}")

    try:
        return HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": device},
            encode_kwargs={"batch_size": 32}
        )
    except RuntimeError as e:
        logger.warning(f"⚠️ GPU unavailable or model failed on device='{device}': {e}")
        logger.info("🔁 Falling back to CPU embedding model.")
        return HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"batch_size": 16}  # Reduce batch size for CPU
        )
