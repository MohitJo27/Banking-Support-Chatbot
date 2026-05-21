from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from backend.config import settings

async def load_documents(directory: str = None):
    data_path = directory or settings.DATA_PATH
    
    loader = DirectoryLoader(
        data_path, 
        glob="*.pdf", 
        loader_cls=PyPDFLoader,
        show_progress=True
    )
    docs = await loader.aload()
    
    return docs