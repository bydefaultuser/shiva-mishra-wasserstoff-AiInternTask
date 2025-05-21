

---

## `README.md` 

# 🚀 Wasserstoff AI Document Research Assistant

A document research assistant that lets users upload PDFs or images and ask questions about their content. The system uses OCR, semantic embeddings, and a local FAISS vector store for fast and accurate retrieval.

---

## 🔍 Overview

This project enables semantic search and Q&A over documents using a combination of:

- 🧠 **FastAPI** backend for OCR, embeddings, and vector search
- 🎛️ **Streamlit** frontend for uploading documents and asking questions
- 📦 **FAISS** for fast, local vector similarity search
- 🤖 **Groq API** for natural language answers

---

## 🧱 Folder Structure

```

project-root/
├── backend/
│   └── app/
│       ├── main.py           # FastAPI entry point
│       ├── config.py         # Configurations and environment variables
│       ├── services/         # Core logic: OCR, embedding, FAISS store
│       └── requirements.txt  # Backend dependencies
│
├── frontend/
│   ├── app.py                # Streamlit frontend
│   └── requirements.txt      # Frontend dependencies
│
└── README.md                 # Project instructions

````

---

## 🛠️ Features

- Upload and process PDFs or images
- Extract text with OCR (`pytesseract`)
- Generate embeddings with `sentence-transformers`
- Perform fast semantic search with `faiss-cpu`
- Synthesize answers using LLMs via Groq API
- Easy-to-use Streamlit interface

---

## ⚙️ Backend API Endpoints

| Endpoint     | Description                             |
|--------------|-----------------------------------------|
| `/upload`    | Accepts and processes files             |
| `/query`     | Searches vector store for top matches   |
| `/synthesize`| Generates an answer from retrieved text |
| `/health`    | Health check endpoint                   |

> **Tech stack**: FastAPI, FAISS, pytesseract, HuggingFace Transformers, Groq API

---

## 💻 Frontend Functionality

- Upload PDFs/images
- Select documents for search
- Ask questions
- Get answers from backend

> Deployed using Streamlit and Hugging Face Spaces.

---

## 🚀 Deployment Instructions

### 1. Deploy Backend on Render

Use Render with a Docker build or directly run `uvicorn`. Set the following environment variables:

| Variable         | Value                                      |
|------------------|--------------------------------------------|
| `GROQ_API_KEY`   | Your Groq API key                          |
| `TESSERACT_PATH` | `/usr/bin/tesseract`                       |
| `FAISS_PATH`     | `/tmp/faiss_index`                         |
| `ALLOWED_ORIGINS`| `https://your-frontend-url`                |

### 2. Deploy Frontend on Hugging Face / Streamlit

In your environment config:

| Variable       | Value                                      |
|----------------|--------------------------------------------|
| `BACKEND_URL`  | `https://your-backend-url.onrender.com`   |
| `GROQ_API_KEY` | Your Groq API key                          |

---

## 🧪 Local Development

Run backend:

```bash
cd backend/app
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
````

Run frontend:

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py --server.headless true
```

Go to: [http://localhost:8501](http://localhost:8501)

---

## 🌿 Branch Strategy

We use one primary branch for deployable code:

* `render-deploy`: Active production-ready branch

To rename it locally to `main` or `master`:

```bash
git checkout render-deploy
git branch -M main
git push -u origin main --force-with-lease
```

---

## 👤 Author

**Shiva Mishra**
Wasserstoff AI Intern | [GitHub](https://github.com/bydefaultuser)

> ✨ Powered by FastAPI, Streamlit, FAISS, HuggingFace, and Groq API

```

---
```
### ✅ Summary of What I Did

| Section | Action |
|--------|--------|
| Folder Structure | Included, trimmed and accurate |
| Backend/Frontend Details | Simplified, no long dependency lists |
| Deployment Steps | Clean and structured |
| API Endpoints | Summarized with descriptions |
| Local Dev | Clear commands to test locally |
| Branch Strategy | Included for clarity |


```
