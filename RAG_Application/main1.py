import streamlit as st
import os
from supporting_functions import create_vector_store, create_rag_chain


# Set up the title and a simple introduction for the Streamlit app
st.set_page_config(page_title="RAG with Ollama & ChromaDB", layout="wide")
st.title("📄 RAG Project with Ollama & ChromaDB")
st.write("""
Welcome! Upload a PDF and ask any question about its content.
The system uses a local Ollama model (LLaMA3.2) and ChromaDB for retrieval.
""")

# File uploader in the sidebar
with st.sidebar:
    st.header("Upload Your Document")
    uploaded_file = st.file_uploader("Upload a PDF file and click 'Process'", type=['pdf'])
    process_button = st.button("Process")