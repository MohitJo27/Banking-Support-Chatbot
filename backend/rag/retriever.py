from backend.config import settings
from backend.rag.vectorstore import get_vectorstore

def get_retriever():
    """Get retriever for semantic search."""
    vectorstore = get_vectorstore()
    if not vectorstore:
        return None
    
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": settings.TOP_K}
    )

def similarity_search(query: str, k: int = None, filter_dict: dict = None):
    """Perform similarity search on vector store."""
    vectorstore = get_vectorstore()
    if not vectorstore:
        return []
    
    k = settings.TOP_K
    return vectorstore.similarity_search(query, k=k, filter=filter_dict)