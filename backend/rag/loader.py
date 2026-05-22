from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from backend.config import settings

def load_documents(directory: str = None):
    """Load PDF documents from directory (sync)."""
    data_path = directory or settings.DATA_PATH
    
    loader = DirectoryLoader(
        data_path, 
        glob="*.pdf", 
        loader_cls=PyPDFLoader,
        show_progress=True
    )
    docs = loader.load()
    
    return docs