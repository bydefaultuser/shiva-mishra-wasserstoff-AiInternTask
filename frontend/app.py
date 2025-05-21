import os
import streamlit as st
import requests
import mimetypes
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_fixed

# Configuration - Safe for Hugging Face Spaces
os.environ['STREAMLIT_SERVER_ENABLE_XSRF_ONLY'] = 'true'
os.environ['STREAMLIT_METRICS_ENABLED'] = 'false'

# Backend URL - Use environment variable or default
BACKEND_URL = os.getenv("BACKEND_URL", "https://shiva-backend-zm9k.onrender.com").strip()

# Set page config
st.set_page_config(
    page_title="Wasserstoff Gen-AI Chatbot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS optimized for Spaces
# Add this CSS right after your st.markdown for page config (around line 20)

st.markdown("""
<style>
    body, .css-1d391kg, .css-1d391kg span {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #333;
    }
    .title {
        text-align: center;
        color: #0A4C6A;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .sidebar .block-container h2 {
        color: #0A4C6A;
        font-weight: 600;
    }
    div.stButton > button:first-child {
        background-color: #0A4C6A;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1.5rem;
        border-radius: 8px;
    }
    div.stButton > button:first-child:hover {
        background-color: #063545;
        color: #ddd;
    }
    .result-box {
        background-color: #ffffff;
        color: #000000;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 1px 1px 8px rgba(0,0,0,0.1);
        font-size: 1rem;
        line-height: 1.5;
        white-space: pre-wrap;
    }
    .detailed-summary {
        background-color: #f0f8ff;
        border-left: 4px solid #0A4C6A;
    }
    button[aria-expanded="true"] {
        color: #0A4C6A;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)
# Title
st.markdown("<h1 class='title'>📄 Wasserstoff Gen-AI Document Research</h1>", unsafe_allow_html=True)

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = []
if 'detailed_summary' not in st.session_state:
    st.session_state.detailed_summary = ""
if 'selected_docs' not in st.session_state:
    st.session_state.selected_docs = []
if 'query' not in st.session_state:
    st.session_state.query = ""

# Retry configuration for backend calls
@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def backend_request(method, endpoint, **kwargs):
    """Safe wrapper for backend requests with retry logic"""
    try:
        url = f"{BACKEND_URL}/{endpoint}"
        response = requests.request(method, url, timeout=30, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Backend request failed: {str(e)}")
        return None

# Document management
@st.cache_data(ttl=300, show_spinner="Fetching document list...")
def get_known_documents():
    """Get list of available documents with caching"""
    response = backend_request("GET", "files")
    return response.get("files", []) if response else []

# Sidebar - Document selection
with st.sidebar:
    st.header("Document Management")
    
    # File upload section
    st.subheader("Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF or Image files",
        type=["pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key="file_uploader"
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            mime_type = mimetypes.guess_type(uploaded_file.name)[0] or "application/octet-stream"
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), mime_type)}
            
            with st.spinner(f"Processing {uploaded_file.name}..."):
                response = backend_request("POST", "upload", files=files)
                if response:
                    st.success(f"Uploaded: {uploaded_file.name}")
    
    # Document selection
    st.markdown("---")
    known_docs = get_known_documents()
    st.session_state.selected_docs = st.multiselect(
        "Select documents to search",
        options=known_docs,
        default=st.session_state.selected_docs,
        key="doc_select"
    )

# Main content area
st.header("Document Query")

# Query input
st.session_state.query = st.text_input(
    "Enter your question:",
    value=st.session_state.query,
    key="query_input",
    placeholder="Ask about the selected documents..."
)

# Search button
if st.button("Search Documents", key="search_btn"):
    if not st.session_state.query.strip():
        st.warning("Please enter a question")
    elif not st.session_state.selected_docs:
        st.warning("Please select at least one document")
    else:
        with st.spinner("Searching documents..."):
            params = {
                "q": st.session_state.query,
                "docs": ",".join(st.session_state.selected_docs)
            }
            response = backend_request("GET", "query", params=params)
            
            if response:
                st.session_state.results = response.get("results", [])
                if not st.session_state.results:
                    st.info("No relevant information found")

# Display results
if st.session_state.results:
    st.subheader("Search Results")
    df = pd.DataFrame(st.session_state.results)
    st.dataframe(df[["filename", "content", "citation"]], use_container_width=True)

    # Summary generation
    st.markdown("---")
    st.subheader("Generate AI Summary")
    
    col1, col2 = st.columns(2)
    with col1:
        style_option = st.selectbox("Summary Style", ["detailed", "concise"])
    with col2:
        length_option = st.selectbox("Summary Length", ["long", "medium", "short"])
    
    include_sources = st.checkbox("Include citations", value=True)
    
    if st.button("Generate Summary", key="summary_btn"):
        with st.spinner("Generating summary..."):
            payload = {
                "question": st.session_state.query,
                "results": st.session_state.results,
                "style": style_option,
                "include_sources": include_sources,
                "length": length_option
            }
            response = backend_request("POST", "synthesize", json=payload)
            
            if response and (answer := response.get("answer")):
                st.session_state.detailed_summary = answer
                st.markdown("### Detailed Summary")
                st.markdown(
                    f"<div class='result-box detailed-summary'>{answer}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.error("Failed to generate summary")

# Clear session button
if st.sidebar.button("Clear Session", key="clear_btn"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()