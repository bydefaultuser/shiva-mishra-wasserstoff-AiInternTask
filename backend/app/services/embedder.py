from config import TESSERACT_PATH  # Unused here but kept for consistency
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from functools import lru_cache
import os
import logging
import torch

logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def get_embedder():
    """
    Load HuggingFace embedder with safe fallback to CPU and meta tensor handling.
    Uses environment variables for model name and device.
    """
    # Get environment variables with defaults
    model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L12-v2")
    device = os.getenv("EMBEDDING_DEVICE", "cpu").strip().lower()
    
    logger.info(f"🔍 Loading embedding model: {model_name} on device: {device}")

    try:
        # First try standard loading
        return HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"device": device},
            encode_kwargs={"batch_size": int(os.getenv("EMBEDDING_BATCH_SIZE", 16))}
        )
    except Exception as e:
        logger.error(f"❌ Initial load failed on {device}: {str(e)}", exc_info=True)
        
        try:
            # Fallback with manual model loading
            logger.warning("⚠️ Attempting manual model loading with meta tensor handling")
            
            # Initialize SentenceTransformer directly
            model = SentenceTransformer(model_name)
            
            # Handle meta tensors if present
            if any(p.is_meta for p in model.parameters()):
                logger.info("🔄 Found meta tensors - initializing with to_empty()")
                model.to_empty(device=device)
                model.load_state_dict(
                    torch.load(
                        os.path.join(model._model_path, "pytorch_model.bin"),
                        map_location=device
                    ),
                    strict=True
                )
            else:
                model.to(device)
            
            # Create LangChain compatible wrapper
            return HuggingFaceEmbeddings(
                client=model,
                model_name=model_name,
                encode_kwargs={"batch_size": int(os.getenv("EMBEDDING_BATCH_SIZE", 16))}
            )
            
        except Exception as fallback_error:
            logger.error(f"❌ Fallback load failed: {str(fallback_error)}", exc_info=True)
            
            # Final fallback to CPU if not already trying
            if device != "cpu":
                logger.warning("⚠️ Falling back to CPU as last resort")
                try:
                    return HuggingFaceEmbeddings(
                        model_name=model_name,
                        model_kwargs={"device": "cpu"},
                        encode_kwargs={"batch_size": int(os.getenv("EMBEDDING_BATCH_SIZE", 16))}
                    )
                except Exception as cpu_error:
                    raise RuntimeError(f"Failed to load embeddings even on CPU: {str(cpu_error)}") from cpu_error
            else:
                raise RuntimeError(f"Failed to load embeddings: {str(fallback_error)}") from fallback_error