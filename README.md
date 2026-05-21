# Banking Support Chatbot (Backend)

RAG-powered banking chatbot API.

## Tech Stack
- FastAPI + Uvicorn
- LangChain + OpenAI (GPT-3.5-turbo, text-embedding-3-small)
- ChromaDB (vector store)
- SQLite (conversation memory)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/chat` | Chat with RAG |
| POST | `/api/upload` | Upload & index document |

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Add OPENAI_API_KEY to .env
uvicorn backend.main:app --reload