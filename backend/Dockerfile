# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        poppler-utils \
        tesseract-ocr \
        libgl1 \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app/ /app/

# Expose FastAPI port
EXPOSE 8000

# Set environment variables (override at runtime)
ENV BACKEND_URL=http://localhost:8000
ENV GROQ_API_KEY=your_groq_api_key_here
ENV ALLOWED_ORIGINS=http://localhost:8501
ENV TESSERACT_PATH=/usr/bin/tesseract

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]