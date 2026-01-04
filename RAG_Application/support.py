# Text Splitters
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Document Loaders
from langchain_community.document_loaders import PyPDFLoader

# Embeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

# Vector Store
from langchain_community.vectorstores import FAISS

# Prompts
from langchain_core.prompts import ChatPromptTemplate

# Chains
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain


