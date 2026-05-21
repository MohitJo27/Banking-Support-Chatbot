from langchain_openai import OpenAIEmbeddings
from backend.config import settings

def get_embeddings():
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=settings.OPENAI_API_KEY
    )