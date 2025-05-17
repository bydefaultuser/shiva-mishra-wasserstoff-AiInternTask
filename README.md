
# Wasserstoff Gen-AI Document Research Chatbot

## Overview

This project is an interactive chatbot designed to perform research across a large set of documents, identify common themes, and provide detailed, cited responses to user queries. It fulfills the requirements of the AI Software Intern - Internship Task Document provided by Wasserstoff.

The chatbot allows users to upload multiple documents (PDF and scanned images), processes them using OCR (if necessary), and utilizes a vector store (FAISS) for efficient semantic search. It then employs a Generative AI model (via the Groq API) to synthesize answers and identify overarching themes, with clear citations back to the original documents.

## Key Features

* **Document Upload:** Users can upload 75+ documents in PDF and image formats (PNG, JPG, JPEG).
* **OCR Processing:** Scanned images are processed using Optical Character Recognition (OCR) to extract text content.
* **Knowledge Base:** Uploaded documents are chunked, embedded, and stored in a FAISS vector store for semantic search.
* **Document Search:** Users can ask questions, and the chatbot retrieves relevant information from the uploaded documents based on semantic similarity.
* **Cited Responses:** The chatbot provides answers with citations indicating the source documents (based on filename, page, and chunk number).
* **Theme Identification:** The chatbot analyzes the retrieved information to identify common themes across the documents.
* **Synthesized Output:** The final response is presented in a chat format, clearly marking citations with document IDs and grouping information under identified themes.
* **Hugging Face Spaces Deployment:** The application is designed to be deployable on Hugging Face Spaces for easy access and demonstration.

## Folder Structure
```
chatbot_theme_identifier/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   └── database.py  (Optional: If you explored database integration)
│   │   ├── models/
│   │   ├── services/
│   │   │   ├── chunker.py
│   │   │   ├── embedder.py
│   │   │   ├── faiss_store.py
│   │   │   ├── llm.py
│   │   │   ├── ocr.py
│   │   │   └── pdf_ocr.py
│   │   ├── main.py
│   │   └── config.py
│   └── data/             (Directory for uploaded documents and FAISS index)
├── requirements.txt
├── Dockerfile          (Optional: If you created a Dockerfile)
├── README.md

```
## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd chatbot_theme_identifier
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    .\venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables:**
    * Create a `.env` file in the `backend` directory.
    * Add your Groq API key (or OpenAI API key if you used that) to the `.env` file:
        ```
        GROQ_API_KEY=YOUR_GROQ_API_KEY
        # Or
        # OPENAI_API_KEY=YOUR_OPENAI_API_KEY
        ```
    * Optionally, you can set the FAISS index path:
        ```
        FAISS_PATH=vector_store/faiss_index
        ```
    * Optionally, configure allowed origins for CORS:
        ```
        ALLOWED_ORIGINS=http://localhost:3000,[http://your-deployed-frontend.com](http://your-deployed-frontend.com)
        ```

## Running the Backend (FastAPI)

Navigate to the `backend/app` directory and run the FastAPI application using Uvicorn:

```bash
cd backend/app
uvicorn main:app --reload
The backend will be accessible at http://localhost:8000.

Running the Frontend (Streamlit)
Navigate to the root of the chatbot_theme_identifier directory and run the Streamlit application:

Bash

streamlit run app.py
The frontend will typically be accessible at http://localhost:8501.

Deployment on Hugging Face Spaces
Create a Hugging Face Space: Go to https://huggingface.co/spaces and create a new Space.
```
## Deployment on Hugging Face Spaces

* **Choose Streamlit SDK:** When creating a new Space on Hugging Face, select the Streamlit SDK as the application type.
* **Link Git Repository:** Connect your Hugging Face Space to the Git repository where you have pushed your `chatbot_theme_identifier` project code.
* **Automatic `app.py` Execution:** Hugging Face Spaces will automatically attempt to run the `app.py` file located in the root of your repository.
* **Backend Configuration:**
    * **Separate Backend (Recommended for Production):** Ensure your `app.py` is configured to communicate with your deployed FastAPI backend (if you choose to deploy it separately on platforms like Render or Railway) via its accessible URL.
    * **Running Backend in Space (Less Recommended):** If you attempt to run the FastAPI backend within the same Hugging Face Space, you'll need to manage the concurrent execution of both Streamlit and FastAPI within the Space's constraints.
* **Environment Variables:** Configure any necessary environment variables, such as your Groq or OpenAI API key, as Secrets within the "Settings" tab of your Hugging Face Space.
* **Git LFS Support:** Hugging Face Spaces provides built-in support for Git Large File Storage (LFS), which is helpful if you have large files (though your FAISS index should ideally be rebuilt on the Space).

## Usage

1.  **Upload Documents:** Once the Streamlit application is running on Hugging Face Spaces, use the file uploader typically located in the sidebar to upload your collection of PDF and image documents (a minimum of 75 documents is recommended for effective theme identification).
2.  **Select Documents for Query:** In the sidebar, you'll likely have options (e.g., checkboxes or a multi-select) to choose which of the uploaded documents you want to include in your current search query.
3.  **Ask a Question:** Enter your research question or query into the text input field provided in the main area of the application.
4.  **Initiate Search:** Click the "Search" button (or a similar interactive element) to start the process of retrieving relevant information from the selected documents based on your question. The individual responses extracted from the most relevant documents will then be displayed.
5.  **Generate Synthesized Response:** Look for an option (e.g., a button or a section) to generate a synthesized response. You might have options to adjust the style and length of the summary. Clicking this will trigger the LLM to identify common themes across the retrieved information and present a final answer in a chat-like format with citations.

## Notes and Considerations

* **OCR Quality:** The accuracy of the Optical Character Recognition (OCR) for scanned images can vary depending on the image quality. Ensure your scanned documents are as clear as possible.
* **LLM Performance:** The quality of the synthesized answers and the identified themes is heavily reliant on the capabilities of the Generative AI model you are using (e.g., Groq's Llama 3).
* **Dataset Size for Themes:** For the chatbot to effectively identify meaningful themes, it is recommended to provide a diverse set of at least 75 semantically related documents.
* **Resource Limitations on Free Platforms:** Be aware that free hosting platforms like Hugging Face Spaces may have limitations on computing resources and can experience "cold starts" if the application hasn't been accessed recently.
* **Potential Improvements:** For a more robust and user-friendly application, consider implementing more comprehensive error handling, improving the user interface and user experience, and potentially adding features for document management and visualization.

## Contact

**Shiva Mishra**
Email: 21shiva12mishra@gmail.com
=======
# Wasserstoff Gen-AI Document Research Chatbot

## Overview

This project is an interactive chatbot designed to perform research across a large set of documents, identify common themes, and provide detailed, cited responses to user queries. It fulfills the requirements of the AI Software Intern - Internship Task Document provided by Wasserstoff.

The chatbot allows users to upload multiple documents (PDF and scanned images), processes them using OCR (if necessary), and utilizes a vector store (FAISS) for efficient semantic search. It then employs a Generative AI model (via the Groq API) to synthesize answers and identify overarching themes, with clear citations back to the original documents.

## Key Features

* **Document Upload:** Users can upload 75+ documents in PDF and image formats (PNG, JPG, JPEG).
* **OCR Processing:** Scanned images are processed using Optical Character Recognition (OCR) to extract text content.
* **Knowledge Base:** Uploaded documents are chunked, embedded, and stored in a FAISS vector store for semantic search.
* **Document Search:** Users can ask questions, and the chatbot retrieves relevant information from the uploaded documents based on semantic similarity.
* **Cited Responses:** The chatbot provides answers with citations indicating the source documents (based on filename, page, and chunk number).
* **Theme Identification:** The chatbot analyzes the retrieved information to identify common themes across the documents.
* **Synthesized Output:** The final response is presented in a chat format, clearly marking citations with document IDs and grouping information under identified themes.
* **Hugging Face Spaces Deployment:** The application is designed to be deployable on Hugging Face Spaces for easy access and demonstration.

## Folder Structure
```
chatbot_theme_identifier/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   └── database.py  (Optional: If you explored database integration)
│   │   ├── models/
│   │   ├── services/
│   │   │   ├── chunker.py
│   │   │   ├── embedder.py
│   │   │   ├── faiss_store.py
│   │   │   ├── llm.py
│   │   │   ├── ocr.py
│   │   │   └── pdf_ocr.py
│   │   ├── main.py
│   │   └── config.py
│   └── data/             (Directory for uploaded documents and FAISS index)
├── requirements.txt
├── Dockerfile          (Optional: If you created a Dockerfile)
├── README.md

```
## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd chatbot_theme_identifier
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    .\venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Variables:**
    * Create a `.env` file in the `backend` directory.
    * Add your Groq API key (or OpenAI API key if you used that) to the `.env` file:
        ```
        GROQ_API_KEY=YOUR_GROQ_API_KEY
        # Or
        # OPENAI_API_KEY=YOUR_OPENAI_API_KEY
        ```
    * Optionally, you can set the FAISS index path:
        ```
        FAISS_PATH=vector_store/faiss_index
        ```
    * Optionally, configure allowed origins for CORS:
        ```
        ALLOWED_ORIGINS=http://localhost:3000,[http://your-deployed-frontend.com](http://your-deployed-frontend.com)
        ```

## Running the Backend (FastAPI)

Navigate to the `backend/app` directory and run the FastAPI application using Uvicorn:

```bash
cd backend/app
uvicorn main:app --reload
The backend will be accessible at http://localhost:8000.

Running the Frontend (Streamlit)
Navigate to the root of the chatbot_theme_identifier directory and run the Streamlit application:

Bash

streamlit run app.py
The frontend will typically be accessible at http://localhost:8501.

Deployment on Hugging Face Spaces
Create a Hugging Face Space: Go to https://huggingface.co/spaces and create a new Space.
```
## Deployment on Hugging Face Spaces

* **Choose Streamlit SDK:** When creating a new Space on Hugging Face, select the Streamlit SDK as the application type.
* **Link Git Repository:** Connect your Hugging Face Space to the Git repository where you have pushed your `chatbot_theme_identifier` project code.
* **Automatic `app.py` Execution:** Hugging Face Spaces will automatically attempt to run the `app.py` file located in the root of your repository.
* **Backend Configuration:**
    * **Separate Backend (Recommended for Production):** Ensure your `app.py` is configured to communicate with your deployed FastAPI backend (if you choose to deploy it separately on platforms like Render or Railway) via its accessible URL.
    * **Running Backend in Space (Less Recommended):** If you attempt to run the FastAPI backend within the same Hugging Face Space, you'll need to manage the concurrent execution of both Streamlit and FastAPI within the Space's constraints.
* **Environment Variables:** Configure any necessary environment variables, such as your Groq or OpenAI API key, as Secrets within the "Settings" tab of your Hugging Face Space.
* **Git LFS Support:** Hugging Face Spaces provides built-in support for Git Large File Storage (LFS), which is helpful if you have large files (though your FAISS index should ideally be rebuilt on the Space).

## Usage

1.  **Upload Documents:** Once the Streamlit application is running on Hugging Face Spaces, use the file uploader typically located in the sidebar to upload your collection of PDF and image documents (a minimum of 75 documents is recommended for effective theme identification).
2.  **Select Documents for Query:** In the sidebar, you'll likely have options (e.g., checkboxes or a multi-select) to choose which of the uploaded documents you want to include in your current search query.
3.  **Ask a Question:** Enter your research question or query into the text input field provided in the main area of the application.
4.  **Initiate Search:** Click the "Search" button (or a similar interactive element) to start the process of retrieving relevant information from the selected documents based on your question. The individual responses extracted from the most relevant documents will then be displayed.
5.  **Generate Synthesized Response:** Look for an option (e.g., a button or a section) to generate a synthesized response. You might have options to adjust the style and length of the summary. Clicking this will trigger the LLM to identify common themes across the retrieved information and present a final answer in a chat-like format with citations.

## Notes and Considerations

* **OCR Quality:** The accuracy of the Optical Character Recognition (OCR) for scanned images can vary depending on the image quality. Ensure your scanned documents are as clear as possible.
* **LLM Performance:** The quality of the synthesized answers and the identified themes is heavily reliant on the capabilities of the Generative AI model you are using (e.g., Groq's Llama 3).
* **Dataset Size for Themes:** For the chatbot to effectively identify meaningful themes, it is recommended to provide a diverse set of at least 75 semantically related documents.
* **Resource Limitations on Free Platforms:** Be aware that free hosting platforms like Hugging Face Spaces may have limitations on computing resources and can experience "cold starts" if the application hasn't been accessed recently.
* **Potential Improvements:** For a more robust and user-friendly application, consider implementing more comprehensive error handling, improving the user interface and user experience, and potentially adding features for document management and visualization.

## Contact

**Shiva Mishra**
Email: 21shiva12mishra@gmail.com
>>>>>>> b9cd768b6cee49c1cd796f9b0603db2f42a76c81
