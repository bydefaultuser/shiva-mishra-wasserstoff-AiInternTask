from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv() 
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path) # Load once when this module is imported

# Optionally define settings as constants
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH")
TESSERACT_PATH = os.getenv("TESSERACT_PATH")