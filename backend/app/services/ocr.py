from config import TESSERACT_PATH
import pytesseract
from PIL import Image
import os
import logging
from typing import Union

logger = logging.getLogger(__name__)

# Configure Tesseract path from environment variables
tesseract_path = os.getenv("TESSERACT_PATH") or TESSERACT_PATH
if tesseract_path and os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
elif os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_PATH", "/usr/bin/tesseract")
else:   
    logger.warning("⚠️ Tesseract path not found. OCR may fail unless Tesseract is in PATH.")

def preprocess_image(img):
    """Enhance OCR accuracy"""
    try:
        img = img.convert('L')  # Grayscale
        return img.point(lambda x: 0 if x < 140 else 255)  # Basic threshold
    except Exception as e:
        logger.error(f"Image preprocessing failed: {e}")
        return img

def extract_text_from_image(file_path: str) -> Union[str, None]:
    """Robust OCR with preprocessing"""
    try:
        with Image.open(file_path) as img:
            processed = preprocess_image(img)
            text = pytesseract.image_to_string(processed, timeout=30)
            return text.strip() if text else None
    except Exception as e:
        logger.error(f"OCR failed for {file_path}: {str(e)}")
        return None