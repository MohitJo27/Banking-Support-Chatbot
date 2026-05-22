from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from backend.rag.chain import get_chat_chain
from backend.rag.retriever import similarity_search

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class SourceDocument(BaseModel):
    content: str
    source: str
    doc_type: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceDocument]
    session_id: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    chain = get_chat_chain()
    if not chain:
        raise HTTPException(status_code=503, detail="Vector store not initialized")
    
    try:
        result = chain.invoke(
            {"question": request.message},
            config={"configurable": {"session_id": request.session_id}}
        )
        
        sources = []
        if "source_documents" in result:
            for doc in result["source_documents"]:
                sources.append(SourceDocument(
                    content=doc.page_content[:300] + "...",
                    source=doc.metadata.get("source", "unknown"),
                    doc_type=doc.metadata.get("doc_type", "unknown")
                ))
        
        return ChatResponse(
            answer=result["answer"],
            sources=sources,
            session_id=request.session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
async def search(query: str, k: Optional[int] = 3):
    results = similarity_search(query, k=k)
    return {
        "query": query,
        "results": [
            {
                "content": r.page_content[:200],
                "source": r.metadata.get("source"),
                "doc_type": r.metadata.get("doc_type")
            }
            for r in results
        ]
    }