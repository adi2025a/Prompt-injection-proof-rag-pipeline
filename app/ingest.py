from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.db import get_vectorstore
from app.logger import logger

def load_documents():
    logger.info("Starting document loading process")
    documents = []
    # Load PDF
    loader = PyPDFLoader("uploads/mypdf.pdf")
    logger.info("Loaded PDF document: uploads/mypdf.pdf")
    documents.extend(loader.load())

    # Load text
    # loader = TextLoader("data/sample.txt")
    # documents.extend(loader.load())

    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=10
    )
    return splitter.split_documents(documents)


def ingest():
    docs = load_documents()
    chunks = split_documents(docs)

    vectordb = get_vectorstore()
    vectordb.add_documents(chunks)

    print("✅ Ingestion complete")