import os

from dotenv import load_dotenv
from langchain.schema.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

load_dotenv()
from langchain_community.document_loaders import UnstructuredURLLoader, PyMuPDFLoader


def add_to_vector_store(docs, file_path, embeddings):
    if not os.path.exists(file_path):
        return create_vector_store(docs, file_path, embeddings)

    vector_store = load_faiss_index(embeddings, file_path)
    vector_store.add_documents(docs)
    # Save the updated FAISS index
    vector_store.save_local(file_path)


def load_faiss_index(embeddings, filename='faiss_index_constitution'):
    # Load from local storage
    persisted_vectorstore = FAISS.load_local(filename, embeddings, allow_dangerous_deserialization=True)
    return persisted_vectorstore


# Function to fetch text from a URL
def fetch_documents_from_url(urls):
    loader = UnstructuredURLLoader(urls=urls)
    documents = loader.load()
    return documents


def get_documents_from_pdf(pdf_file_path):
    loader = PyMuPDFLoader(pdf_file_path)
    documents = loader.load()
    return documents


def get_text_chunks_langchain(text, chunk_size=1000, separators=["\n\n", "\n", "."]):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, separators=separators)
    docs = [Document(page_content=x, metadata={"source": "text"}) for x in text_splitter.split_text(text)]
    return docs


# Function to split text into chunks using RecursiveTextSplitter
def split_documents(documents, chunk_size=1000, separators=["\n\n", "\n", "."]):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, separators=separators)
    return splitter.split_documents(documents)


# Function to create FAISS index and save as PKL
def create_vector_store(docs, filepath, embeddings):
    vector_store = FAISS.from_documents(docs, embeddings)
    vector_store.save_local(filepath)


urls = [
    "https://www.livemint.com/market/stock-market-news/wall-street-today-us-stocks-rise-after-global-markets-rout-11722950046752.html"]
# Example URLs (replace with actual URLs)
if __name__ == '__main__':
    pass
