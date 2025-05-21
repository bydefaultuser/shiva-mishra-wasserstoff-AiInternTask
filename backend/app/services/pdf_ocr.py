from config import TESSERACT_PATH
from pdf2image import convert_from_path
import pytesseract
import os
import logging

logger = logging.getLogger(__name__)


# Configure Tesseract path
tesseract_path = os.getenv("TESSERACT_PATH") or TESSERACT_PATH
if tesseract_path and os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
elif os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_PATH", "/usr/bin/tesseract")
else:
    logger.warning("⚠️ Tesseract path not found. PDF OCR may fail unless Tesseract is in PATH.")

def ocr_pdf(file_path: str, poppler_path: str = None) -> str:
    """
    Convert PDF to images and perform OCR on each page.
    """
    try:
        # Use poppler_path from environment if not provided
        if not poppler_path:
            poppler_path = os.getenv("POPPLER_PATH")

        # Convert PDF to images
        pages = convert_from_path(file_path, dpi=300, poppler_path=poppler_path)
    except Exception as e:
        logger.error(f"PDF to image conversion failed: {e}")
        raise RuntimeError(f"PDF to image conversion failed: {e}")

    text = ""
    for i, page in enumerate(pages):
        try:
            page_text = pytesseract.image_to_string(page)
            text += f"Page {i+1}:\n{page_text}\n\n"
        except Exception as e:
            logger.error(f"Tesseract OCR failed on page {i+1}: {e}")
            continue

    return text.strip()