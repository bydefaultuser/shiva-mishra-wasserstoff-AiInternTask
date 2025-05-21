from dotenv import load_dotenv
import os
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi.responses import JSONResponse
from typing import Optional, Dict, List

# Load environment variables
load_dotenv()

# Import services
from services import ocr, pdf_ocr, chunker, embedder
from services.faiss_store import store_chunks as faiss_store_chunks, query_chunks
from services.embedder import get_embedder
from services.llm import generate_structured_answer

# Initialize FastAPI
app = FastAPI(title="Document Research Backend (FAISS Only)")

# Configure CORS (use environment variable for allowed origins)
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8501").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure upload directory
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/tmp/data"))  # Use /tmp for GCP compatibility
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Configure FAISS index path
FAISS_PATH = Path(os.getenv("FAISS_PATH", "/tmp/faiss_index"))
FAISS_PATH.parent.mkdir(parents=True, exist_ok=True)  # Ensure parent directory exists

@app.get("/files")
def list_uploaded_files():
    """Return list of uploaded document filenames"""
    try:
        files = [f.name for f in UPLOAD_DIR.glob("*") if f.is_file()]
        return {"files": files}
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")
        return JSONResponse(status_code=500, content={"error": "Failed to list files"})

@app.get("/query")
async def query_docs(
    q: str = Query(..., description="Your question to ask the documents"),
    k: int = 4,
    docs: Optional[str] = None
):
    try:
        embedder_instance = embedder.get_embedder()
        filters = {}
        if docs:
            doc_list = [d.strip() for d in docs.split(",")]
            filters["filename"] = {"$in": doc_list}

        retrieved_chunks = query_chunks(embedder_instance, q, k=k, filters=filters)

        # Extract relevant metadata for citation
        detailed_results = []
        for chunk in retrieved_chunks:
            detailed_results.append({
                "filename": chunk['metadata'].get('filename', 'N/A'),
                "content": chunk['content'],
                "citation": f"Page {chunk['metadata'].get('page_number', '?')}, Chunk {chunk['metadata'].get('chunk_num', '?')}"
            })

        return {
            "query": q,
            "results": detailed_results
        }
    except Exception as e:
        logger.error(f"Query failed: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": "Query failed", "details": str(e)}
        )

@app.post("/synthesize")
async def synthesize_answer(payload: dict):
    try:
        question = payload.get("question", "")
        results = payload.get("results", [])
        style = payload.get("style", "detailed")
        include_sources = payload.get("include_sources", True)
        length = payload.get("length", "long")

        if not question or not results:
            raise HTTPException(status_code=400, detail="Missing question or results")

        detailed_response = generate_structured_answer(
            question,
            results,
            style=style,
            include_sources=include_sources,
            length=length
        )

        return {
            "answer": detailed_response,
            "type": "detailed"
        }
    except Exception as e:
        logger.error(f"Synthesis failed: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": "Synthesis failed", "details": str(e)}
        )

@app.post("/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    chunk_size: int = 500,
    chunk_overlap: int = 100
):
    logger.info(f"Received upload: {file.filename} with content_type: {file.content_type}")
    allowed_types = ["application/pdf", "image/jpeg", "image/png", "image/tiff"]
    if file.content_type not in allowed_types:
        logger.warning(f"Unsupported file type: {file.content_type} for file {file.filename}")
        raise HTTPException(status_code=400, detail="Unsupported file type")

    try:
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as f:
            f.write(await file.read())

        background_tasks.add_task(
            process_document,
            file_path,
            file.content_type,
            file.filename,
            chunk_size,
            chunk_overlap
        )

        return {"status": "success", "filename": file.filename}
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(500, "Document processing failed") from e

def process_document(file_path: Path, content_type: str, filename: str, chunk_size: int, chunk_overlap: int):
    logger.info(f"🔄 Started processing {filename}")

    try:
        if content_type.startswith("image/"):
            logger.info("🧠 Running OCR on image...")
            text = ocr.extract_text_from_image(file_path)
        else:
            logger.info("🧠 Running OCR on PDF...")
            text = pdf_ocr.ocr_pdf(file_path)

        if not text.strip():
            logger.warning(f"⚠️ No text extracted from {filename}")
            return

        logger.info("✂️ Chunking text...")
        chunks = chunker.chunk_text(text, chunk_size, chunk_overlap)
        logger.info(f"📦 Chunked into {len(chunks)} chunks")

        logger.info("🧬 Embedding chunks...")
        embedder_instance = get_embedder()
        embeddings = embedder_instance.embed_documents(chunks)
        logger.info("✅ Embeddings created")

        logger.info("📚 Storing in FAISS vector store...")
        metadatas = [
            {
                "filename": filename,
                "chunk_num": i,
                "page_number": (i + 1)  # Assuming sequential page numbering per document
            }
            for i in range(len(chunks))
        ]

        faiss_store_chunks(embedder_instance, chunks, metadatas)
        logger.info(f"✅ Successfully processed and stored {filename} in FAISS")

    except Exception as e:
        logger.error(f"❌ Processing failed for {filename}: {str(e)}", exc_info=True)