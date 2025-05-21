from pathlib import Path
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
try:
    # Load .env file from project root
    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        logger.info(f"✅ Loaded .env from {env_path}")
    else:
        logger.warning("⚠️ .env file not found - using environment variables only")
except Exception as e:
    logger.error(f"❌ Failed to load .env file: {str(e)}")

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "fallback_key_for_local_dev")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Optional fallback

# FAISS Configuration
FAISS_PATH = os.getenv("FAISS_PATH", "/tmp/faiss_index")  # Use /tmp for GCP compatibility

# Upload Directory
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/tmp/data"))  # Use /tmp for GCP compatibility
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

# Optional: Tesseract OCR Path (for image processing)
TESSERACT_PATH = os.getenv("TESSERACT_PATH")
if TESSERACT_PATH:
    os.environ["TESSERACT_PATH"] = TESSERACT_PATH