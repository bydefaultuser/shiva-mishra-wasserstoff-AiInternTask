import streamlit as st
import requests
import mimetypes
import pandas as pd
import os

# Use environment variable for backend URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Wasserstoff Gen-AI Chatbot", layout="wide")

# Custom CSS
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

@st.cache_data(ttl=300)
def get_known_documents():
    try:
        resp = requests.get(f"{BACKEND_URL}/files", timeout=10)
        resp.raise_for_status()
        return resp.json().get("files", [])
    except requests.exceptions.ConnectionError:
        st.error("❌ Failed to connect to backend. Ensure backend is running and reachable.")
        return []
    except Exception as e:
        st.error(f"❌ Failed to fetch document list: {e}")
        return []

known_docs = get_known_documents()

# Sidebar layout
with st.sidebar:
    st.header("Upload Documents (75+)")
    uploaded_files = st.file_uploader("Upload multiple PDF or Image files", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            mime_type, _ = mimetypes.guess_type(uploaded_file.name)
            files = {
                "file": (uploaded_file.name, uploaded_file.getvalue(), mime_type or "application/octet-stream")
            }
            with st.spinner(f"Uploading and processing {uploaded_file.name}..."):
                try:
                    resp = requests.post(f"{BACKEND_URL}/upload", files=files, timeout=30)
                    resp.raise_for_status()
                    status = resp.json().get("status")
                    st.success(f"Uploaded: {uploaded_file.name} (Status: {status})")
                    known_docs = get_known_documents()  # Refresh list
                except requests.exceptions.RequestException as e:
                    st.error(f"Upload failed for {uploaded_file.name}: {str(e)}")
        if uploaded_files:
            st.info("All selected files uploaded and processing started.")

    st.markdown("---")
    st.session_state.selected_docs = st.multiselect(
        "Select documents to search",
        options=known_docs,
        default=known_docs
    )

# Main content
st.header("Ask a question about the documents")
st.session_state.query = st.text_input("Enter your question here:", value=st.session_state.query)

if st.button("Search") and st.session_state.query.strip():
    if not st.session_state.selected_docs:
        st.warning("Please select at least one document to search.")
    else:
        with st.spinner("Searching..."):
            try:
                params = {
                    "q": st.session_state.query,
                    "docs": ",".join(st.session_state.selected_docs)
                }
                resp = requests.get(f"{BACKEND_URL}/query", params=params, timeout=30)
                resp.raise_for_status()
                data = resp.json()

                # Update session state
                st.session_state.results = data.get("results", [])
                st.session_state.detailed_summary = ""  # Reset detailed summary

                if st.session_state.results:
                    st.markdown("### Individual Document Responses:")
                    df = pd.DataFrame(st.session_state.results)
                    st.dataframe(df[["filename", "content", "citation"]])
                else:
                    st.info("No relevant information found in the selected documents.")

            except requests.exceptions.RequestException as e:
                st.error(f"Search failed: {e}")

# Detailed summary section
if st.session_state.results:
    st.markdown("---")
    st.subheader("Generate Detailed Summary with AI")
    style_option = st.selectbox("Summary Style:", ["detailed", "concise"])
    include_sources_option = st.checkbox("Include Document Citations in Summary", value=True)
    length_option = st.selectbox("Summary Length:", ["long", "medium", "short"])

    if st.button("Generate Summary"):
        with st.spinner("Synthesizing detailed answer..."):
            try:
                synthesis_resp = requests.post(f"{BACKEND_URL}/synthesize", json={
                    "question": st.session_state.query,
                    "results": st.session_state.results,
                    "style": style_option,
                    "include_sources": include_sources_option,
                    "length": length_option
                }, timeout=60)
                synthesis_resp.raise_for_status()
                st.session_state.detailed_summary = synthesis_resp.json().get("answer", "")

                if not st.session_state.detailed_summary:
                    st.error("Received empty response from AI")
            except requests.exceptions.RequestException as e:
                st.error(f"LLM synthesis failed: {e}")

    # Display detailed summary if available
    if st.session_state.detailed_summary:
        st.markdown("## 🧠 Detailed AI Summary")
        st.markdown(
            f"<div class='result-box detailed-summary'>{st.session_state.detailed_summary}</div>",
            unsafe_allow_html=True
        )
elif not st.session_state.results and not st.session_state.detailed_summary and st.session_state.query:
    st.info("No results found for your query. Try a different question or select more documents.")
elif not st.session_state.selected_docs and known_docs:
    st.info("Please select documents from the sidebar to begin searching.")
elif not known_docs:
    st.info("Please upload documents to start.")

# Clear button to reset the session
if st.sidebar.button("Clear Session"):
    st.session_state.results = []
    st.session_state.detailed_summary = ""
    st.session_state.query = ""
    st.session_state.selected_docs = known_docs  # Reset selected docs to all
    st.rerun()