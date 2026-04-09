from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os 
from app.logger import logger
from dotenv import load_dotenv 
load_dotenv()  # Load environment variables from .env file

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Ensure you have this in your .env file
def get_vectorstore():
    logger.info("Initializing vector store with Google Generative AI embeddings")

    embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",  # or "gemini-embedding-2-preview"
    api_key=GEMINI_API_KEY
    )

    logger.info("Creating Chroma vector store with embeddings")
    
    vectordb = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    logger.info("Vector store initialized successfully")
    
    return vectordb