from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain



EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.2:1b"


def create_vector_store(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    #embeddings
    embedding = OllamaEmbeddings(model=EMBEDDING_MODEL)

    #database
    vector_store = Chroma.from_documents(documents=splits,embedding=embedding)


    return vector_store



def create_rag_chain(vector_store):


    llm= Ollama(model=LLM_MODEL)

    prompt=ChatPromptTemplate.from_template("""
    Answer the following question based only on the provided context.
    Your goal is to provide a detailed and comprehensive answer.
    Extract all relevant information from the context to formulate your response.
    Think step by step and structure your answer logically.
    If the context does not contain the answer to the question, state that the information is not available in the provided document. Do not attempt to make up information.

    <context>
    {context}
    </context>

    Question: {input}
    """)


    # retrieve
    retriever= vector_store.as_retriever()

    #passing document to llm.
    document_chain = create_stuff_documents_chain(llm , prompt)

    # final step
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    return retrieval_chain

