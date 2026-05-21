import os
import uuid
from langchain_chroma import Chroma
from backend.config import settings
from backend.rag.embedding import get_embeddings

def get_vectorstore():
    """Get or create ChromaDB vector store."""
    embedding = get_embeddings()
    persist_dir = settings.CHROMA_PERSIST_DIR
    
    if os.path.exists(persist_dir) and os.listdir(persist_dir):
        return Chroma(
            persist_directory=persist_dir,
            embedding_function=embedding,
            collection_name=settings.COLLECTION_NAME
        )
    return None

def create_vectorstore(documents):
    """Create new vector store from documents."""
    embedding = get_embeddings()
    os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
    
    ids = [str(uuid.uuid4()) for _ in documents]
    
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embedding,
        persist_directory=settings.CHROMA_PERSIST_DIR,
        collection_name=settings.COLLECTION_NAME,
        ids=ids
    )
    return vectorstore

def add_documents(vectorstore, documents):
    """Add new documents to existing vector store."""
    ids = [str(uuid.uuid4()) for _ in documents]
    vectorstore.add_documents(documents=documents, ids=ids)
    return vectorstore