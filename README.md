# Banking Support Chatbot

A full-stack, RAG-powered banking chatbot application. This repository contains the AI-driven API backend for document indexing and conversational retrieval, alongside the client-facing frontend UI.

## 🏗️ Project Structure

* **`backend/`**: FastAPI application containing the API routes, LangChain RAG pipeline (`chain.py`, `loader.py`, `retriever.py`), and configuration.
* **`frontend/`**: The client-facing user interface for the chatbot.
* **`data/`**: Storage directory for source documents (e.g., banking PDFs and MITCs) used for vector indexing.

## 💻 Tech Stack

**Backend**
* **Framework:** FastAPI + Uvicorn
* **Package Manager:** uv
* **AI & Orchestration:** LangChain + OpenAI (GPT-3.5-turbo, text-embedding-3-small)
* **Vector Store:** ChromaDB 
* **Database:** SQLite (conversation memory)

**Frontend**
* *(Add your frontend tech stack here, e.g., React, Vue, Streamlit, vanilla JS)*

## 🔌 API Reference

The backend exposes the following endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/chat` | Chat with RAG |
| POST | `/api/upload` | Upload & index document |

## 🚀 Getting Started

### 1. Backend Setup

It is recommended to use a virtual environment. Install the required Python dependencies using `uv` and start the API server:

```bash
# Install dependencies using uv
uv pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# IMPORTANT: Open .env and add your OPENAI_API_KEY