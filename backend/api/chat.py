from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, AsyncGenerator
import json
from backend.rag.chain import get_chat_chain, get_streaming_chain
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


# /chat
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


# /chat/stream
async def stream_generator(message: str, session_id: str) -> AsyncGenerator[str, None]:
    chain = get_streaming_chain()
    if not chain:
        yield f"data: {json.dumps({'error': 'Vector store not initialized'})}\n\n"
        return
    
    try:
        async for chunk in chain.astream(
            {"question": message},
            config={"configurable": {"session_id": session_id}}
        ):
            token = chunk.get("answer", "")
            if token:
                yield f"data: {json.dumps({'token': token})}\n\n"
        
        # Fetch sources after streaming
        results = similarity_search(message, k=3)
        sources = [
            {
                "content": r.page_content[:300] + "...",
                "source": r.metadata.get("source", "unknown"),
                "doc_type": r.metadata.get("doc_type", "unknown")
            }
            for r in results
        ]
        yield f"data: {json.dumps({'sources': sources, 'done': True})}\n\n"
        
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    return StreamingResponse(
        stream_generator(request.message, request.session_id),
        media_type="text/event-stream"
    )


# Debug search
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