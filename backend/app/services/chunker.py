from config import TESSERACT_PATH
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Optional
import logging
import os

logger = logging.getLogger(__name__)

# Default chunking settings (optimized for memory)
DEFAULT_CHUNK_SIZE = int(os.getenv("DEFAULT_CHUNK_SIZE", 256))
DEFAULT_CHUNK_OVERLAP = int(os.getenv("DEFAULT_CHUNK_OVERLAP", 32))

def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    separators: Optional[List[str]] = None
) -> List[str]:
    """
    Improved chunking with fallbacks and validation.
    Uses smaller defaults for memory-constrained environments.
    """
    if not text or not isinstance(text, str):
        logger.warning("⚠️ Empty or invalid text provided")
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators or ["\n\n", "\n", ".", " ", ""]
    )

    try:
        chunks = splitter.split_text(text)
        logger.info(f"✂️ Chunked into {len(chunks)} chunks of ~{chunk_size} chars")
        return chunks
    except Exception as e:
        logger.error(f"❌ Chunking failed: {str(e)}")
        return []