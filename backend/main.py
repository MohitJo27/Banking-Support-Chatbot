from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import chat, upload

app = FastAPI(
    title="Banking Support Chatbot",
    description="RAG-powered banking chatbot",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# /health
@app.get("/health")
async def health():
    from backend.rag.vectorstore import get_vectorstore
    vs = get_vectorstore()
    return {
        "status": "healthy",
        "vectorstore_ready": vs is not None
    }

@app.get("/")
async def root():
    return {"message": "Banking Chatbot API", "docs": "/docs"}

app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(upload.router, prefix="/api", tags=["upload"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)