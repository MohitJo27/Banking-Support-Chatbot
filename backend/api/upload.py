import os
import shutil
import traceback
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.config import settings
from backend.rag.loader import load_documents
from backend.rag.chunker import split_documents
from backend.rag.vectorstore import get_vectorstore, create_vectorstore, add_documents

router = APIRouter()

@router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    allowed_extensions = {".pdf", ".txt"}
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(400, f"Only {allowed_extensions} files allowed")
    
    file_path = os.path.join(settings.DATA_PATH, file.filename)
    os.makedirs(settings.DATA_PATH, exist_ok=True)
    
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    try:
        docs = load_documents(settings.DATA_PATH)
        if not docs:
            raise Exception("No documents loaded - check if PDF is readable")
        
        chunks = split_documents(docs)
        
        vectorstore = get_vectorstore()
        if vectorstore:
            add_documents(vectorstore, chunks)
            msg = f"Added {len(chunks)} chunks from {file.filename}"
        else:
            create_vectorstore(chunks)
            msg = f"Created new vector store with {len(chunks)} chunks"
        
        return {
            "filename": file.filename,
            "chunks_indexed": len(chunks),
            "message": msg
        }
    except Exception as e:
        error_detail = f"{str(e)}\n\n{traceback.format_exc()}"
        print(error_detail)
        raise HTTPException(500, detail=error_detail)