import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DATA_PATH = os.getenv("DATA_PATH", "./data")
    CHROMA_PERSIST_DIR = "./chroma_db"
    COLLECTION_NAME = "banking_docs"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 100
    TOP_K = 3

settings = Settings()