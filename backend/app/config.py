from pathlib import Path
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env (optional)
try:
    from dotenv import load_dotenv
    # Only try to load .env in dev mode
    if "GCP" not in os.getenv("DEPLOY_ENV", ""):
        env_path = Path(__file__).parent.parent / ".env"
        if env_path.exists():
            load_dotenv(env_path)
            logger.info(f"✅ Loaded .env from {env_path}")
        else:
            logger.warning("⚠️ No .env file found - using environment variables only")
except Exception as e:
    logger.error(f"❌ Failed to load .env: {str(e)}")

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Optional fallback

if not GROQ_API_KEY:
    logger.warning("⚠️ GROQ_API_KEY not set. AI synthesis will fail unless provided in platform secrets.")

# FAISS Configuration
FAISS_PATH = os.getenv("FAISS_PATH", "/tmp/faiss_index")

# Upload Directory
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/tmp/data"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Tesseract OCR Path (for image processing)
TESSERACT_PATH = os.getenv("TESSERACT_PATH", "/usr/bin/tesseract")

# Chunking defaults (smaller = better for memory-constrained environments)
DEFAULT_CHUNK_SIZE = int(os.getenv("DEFAULT_CHUNK_SIZE", 256))
DEFAULT_CHUNK_OVERLAP = int(os.getenv("DEFAULT_CHUNK_OVERLAP", 32))

# Embedding model configuration
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-MiniLM-L3-v2")
EMBEDDING_DEVICE = os.getenv("EMBEDDING_DEVICE", "cpu")
EMBEDDING_BATCH_SIZE = int(os.getenv("EMBEDDING_BATCH_SIZE", 16))

# PDF & OCR settings
PDF_DPI = int(os.getenv("PDF_DPI", 150))  # Reduced DPI for low-memory OCR
MAX_PAGES = int(os.getenv("MAX_PAGES", 3))  # Limit pages processed