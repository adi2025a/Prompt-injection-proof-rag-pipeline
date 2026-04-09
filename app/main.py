from fastapi import FastAPI , File , UploadFile
import shutil
from pydantic import BaseModel
from app.rag import query_rag
from app.ingest import ingest
from dotenv import load_dotenv
from app.logger import logger

import os

load_dotenv()  # Load environment variables from .env file

app = FastAPI()
logger.info("FastAPI application has started")

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def query(request: QueryRequest):
    logger.info(f"Received query: {request.question}")
    answer = query_rag(request.question)
    return {"answer": answer}



UPLOAD_DIR = "uploads"

# Make sure the folder exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    logger.info(f"Received file upload: {file.filename}")
    if file.content_type != "application/pdf":
        logger.warning(f"Rejected file upload: {file.filename} - Invalid content type: {file.content_type}")
        return {"error": "Only PDF files are allowed"}
    
    file_path = os.path.join(UPLOAD_DIR, "mypdf.pdf")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        logger.info(f"Saved file: {file.filename} to {file_path}")

    ingest()
    
    return {"filename": file.filename, "saved_to": file_path, "message": "PDF uploaded successfully"}