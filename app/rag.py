from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from app.db import get_vectorstore
import os

YOUR_API_KEY = os.environ.get("GEMINI_API_KEY")

_rag_chain = None

def get_rag_chain():
    global _rag_chain
    if _rag_chain is not None:
        return _rag_chain

    vectordb = get_vectorstore()
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    llm = ChatGoogleGenerativeAI(
        model="models/gemini-2.5-flash",
        api_key=YOUR_API_KEY
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use the retrieved context to answer.\n\nContext: {context}"),
        ("human", "{input}")
    ])

    document_chain = create_stuff_documents_chain(llm, prompt)
    _rag_chain = create_retrieval_chain(retriever, document_chain)

    return _rag_chain

def query_rag(question: str):
    chain = get_rag_chain()
    result = chain.invoke({"input": question})
    return result["answer"]  # chain returns dict with "answer" and "context" keys