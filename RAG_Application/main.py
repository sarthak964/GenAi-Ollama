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


# initilize the variables
if "Vector_store" not in st.session_state:
    st.session_state.vector_store= None
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain=None


if process_button and uploaded_file is not None:
    with st.spinner("Processing Document this might take few minutes"):
        #temp folder
        temp_dir="temp_docs"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)


        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path , "wb") as f:
            f.write(uploaded_file.getbuffer())

        #
        st.session_state.vector_store=create_vector_store(file_path)
        st.session_state.rag_chain=create_rag_chain(st.session_state.vector_store)
        st.success("Document  processed successfully, you can now ask the question.")


if st.session_state.rag_chain is not None:
    st.header("Ask your question.")
    question = st.text_input("Enter your question here", key="Question_input")
    if st.button("Get Answer"):
        if question:
            with st.spinner("Thinking...."):
                try:
                    response= st.session_state.rag_chain.invoke({"input":question})

                    st.write("Answer")
                    st.write(response["answer"])

                    # Optionally display the context used to generate the answer
                    with st.expander("Show Context"):
                        st.write("The following context was used to generate the answer:")
                        for doc in response["context"]:
                            st.info(f"**Content:** {doc.page_content}")
                except Exception as e:
                    st.error(f"An error occurred while getting the  answer {e}")

        else:
            st.warning("Please enter a question")
    else:
        st.info("Please upload a pdf file.")




