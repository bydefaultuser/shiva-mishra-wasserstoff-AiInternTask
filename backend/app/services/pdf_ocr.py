from config import TESSERACT_PATH
from pdf2image import convert_from_path
import pytesseract
import os
import logging
from typing import Union

logger = logging.getLogger(__name__)

# Configure Tesseract path from environment variables
tesseract_path = os.getenv("TESSERACT_PATH") or TESSERACT_PATH
if tesseract_path and os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
elif os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_PATH", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
else:
    logger.warning("⚠️ Tesseract path not found. PDF OCR may fail unless Tesseract is in PATH.")

def ocr_pdf(file_path: str, poppler_path: str = None, max_pages: int = 3) -> Union[str, None]:
    """
    Convert PDF to images and perform OCR with optimized settings.
    
    Args:
        file_path (str): Path to the input PDF file
        poppler_path (str): Optional Poppler binary path (set via env var)
        max_pages (int): Limit number of pages processed to avoid OOM

    Returns:
        str: Extracted text or None if failed
    """
    try:
        # Get poppler path from environment if needed
        if not poppler_path:
            poppler_path = os.getenv("POPPLER_PATH")

        # Use low dpi and resize to keep memory use low
        pages = convert_from_path(
            file_path,
            dpi=150,              # Reduced from 300 to save memory
            first_page=0,
            last_page=max_pages   # Only process first few pages by default
        )
        
        if not pages:
            logger.error("No pages were extracted from the PDF.")
            return None

    except Exception as e:
        logger.error(f"PDF to image conversion failed: {e}")
        raise RuntimeError(f"PDF conversion error: {e}")

    full_text = ""
    for i, page in enumerate(pages):
        try:
            # Resize each page before OCR
            page.thumbnail((800, 800))  # Reduce image size

            # Perform OCR
            page_text = pytesseract.image_to_string(page)
            
            if page_text.strip():
                full_text += f"Page {i+1}:\n{page_text}\n\n"
            else:
                logger.info(f"📄 Page {i+1} has no extractable text")
                
        except Exception as e:
            logger.error(f"Tesseract OCR failed on page {i+1}: {e}")
            continue

    if not full_text.strip():
        logger.warning("⚠️ No text extracted from any page in the PDF")
        return None

    return full_text.strip()