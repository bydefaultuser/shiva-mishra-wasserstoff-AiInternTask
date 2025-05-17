from ..config import TESSERACT_PATH
from pdf2image import convert_from_path
import pytesseract, os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ocr_pdf(file_path: str, poppler_path: str = None) -> str:
    if not poppler_path:
        poppler_path = os.getenv("POPPLER_PATH")

    try:
        pages = convert_from_path(file_path, dpi=300, poppler_path=poppler_path)
    except Exception as e:
        raise RuntimeError(f"PDF to image conversion failed: {e}")

    text = ""
    for page in pages:
        try:
            page_text = pytesseract.image_to_string(page)
            text += page_text + "\n\n"
        except Exception as e:
            raise RuntimeError(f"Tesseract OCR failed: {e}")

    return text.strip()

