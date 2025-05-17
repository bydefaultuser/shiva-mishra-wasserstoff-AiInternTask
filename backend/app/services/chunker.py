from ..config import CHROMA_DB_PATH, TESSERACT_PATH
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
    separators: Optional[List[str]] = None
) -> List[str]:
    """Improved chunking with validation"""
    if not text or not isinstance(text, str):
        logger.warning("Empty or invalid text provided")
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators or ["\n\n", "\n", ".", " ", ""]
    )
    
    try:
        return splitter.split_text(text)
    except Exception as e:
        logger.error(f"Chunking failed: {str(e)}")
        return []