# Use a Python base image
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose the port for Streamlit (frontend)
EXPOSE 8501

# Command to run the Streamlit frontend, specifying the path
CMD ["streamlit", "run", "frontend/app.py"]