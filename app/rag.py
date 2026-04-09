from langchain_google_genai import ChatGoogleGenerativeAI
from app.db import get_vectorstore
from dotenv import load_dotenv
from app.logger import logger
import os 
load_dotenv()  # Load environment variables from .env file

YOUR_API_KEY = os.environ.get("GEMINI_API_KEY")  # Ensure you have this in your .env file

def get_rag_chain():
    logger.info("Setting up RAG chain with Google Generative AI and Chroma vector store")
    vectordb = get_vectorstore()
    
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    logger.info("Retriever created from vector store with top-k=3")

    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", api_key=YOUR_API_KEY)
    logger.info("Google Generative AI model initialized")

    qa_chain = llm | retriever
    logger.info("RAG chain created by combining LLM and retriever")
    
    return qa_chain


def query_rag(question: str):
    chain = get_rag_chain()
    logger.info(f"Querying RAG chain with question: {question}")
    result = chain.invoke(question)
    logger.info(f"RAG chain response: {result}")
    return result