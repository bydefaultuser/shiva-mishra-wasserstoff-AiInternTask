from config import TESSERACT_PATH
import pytesseract
from PIL import Image, ImageFile
import os
import logging
from typing import Union

logger = logging.getLogger(__name__)
ImageFile.LOAD_TRUNCATED_IMAGES = True
logging.getLogger('PIL').setLevel(logging.ERROR)

# Configure Tesseract path from environment variables
tesseract_path = os.getenv("TESSERACT_PATH", TESSERACT_PATH)
if tesseract_path and os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
elif os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_PATH", "C:/Program Files/Tesseract-OCR/tesseract.exe")
else:
    logger.warning("⚠️ Tesseract path not found. OCR may fail unless Tesseract is in PATH.")

def resize_image(img, max_size=800):
    """Resize image to reduce memory usage"""
    try:
        img.thumbnail((max_size, max_size))
        return img
    except Exception as e:
        logger.error(f"Image resize failed: {e}")
        return img

def preprocess_image(img):
    """Enhance OCR accuracy with minimal memory overhead"""
    try:
        # Resize first to reduce memory footprint
        img = resize_image(img)
        
        # Convert to grayscale
        img = img.convert('L')  # Grayscale
        return img.point(lambda x: 0 if x < 140 else 255)  # Basic threshold
    except Exception as e:
        logger.error(f"Image preprocessing failed: {e}")
        return img

def extract_text_from_image(file_path: str) -> Union[str, None]:
    """Robust OCR with preprocessing and fallbacks"""
    try:
        if not os.path.isfile(file_path):
            logger.warning(f"❌ Invalid file path: {file_path}")
            return None
            
        if not os.path.getsize(file_path) > 0:
            logger.warning(f"⚠️ File is empty or invalid: {file_path}")
            return None

        with Image.open(file_path) as img:
            # Resize before processing
            img = resize_image(img)
            
            # Preprocess image
            processed = preprocess_image(img)
            
            # Extract text with timeout
            text = pytesseract.image_to_string(processed, timeout=10)  # Reduced timeout
            return text.strip() if text else None
            
    except Exception as e:
        logger.error(f"OCR failed for {file_path}: {str(e)}")
        return None