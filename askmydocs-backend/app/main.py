"""
AskMyDocs - AI-Powered Document Query System

Portfolio Project demonstrating:
- AI/ML Engineering: RAG architecture, vector embeddings, multi-LLM integration
- Backend Development: FastAPI, async programming, database design
- DevOps: Docker containerization, service orchestration
- Testing: Comprehensive automated test suite with PDF processing

Author: Praveen K Mittal
Purpose: Showcase advanced technical skills in modern AI application development
Tech Stack: Python, FastAPI, PostgreSQL, ChromaDB, Docker, Ollama, OpenAI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, chat
from app.routers import auth_router, upload_router, chat_router
from app.database import engine
from app.models import Base
import os

app = FastAPI(
    title="AskMyDocs - AI Document Query System",
    description="""
    **Portfolio Project**: Intelligent document processing and query system demonstrating 
    advanced AI/ML engineering and backend development skills.
    
    ## Features
    - **Document Processing**: Upload and process PDF/text documents
    - **AI-Powered Queries**: Ask natural language questions about your documents
    - **Multi-LLM Support**: OpenAI and local Ollama integration
    - **Vector Search**: Semantic document retrieval with ChromaDB
    - **Production Ready**: Containerized, tested, and documented
    
    ## Skills Demonstrated
    - RAG (Retrieval Augmented Generation) architecture
    - FastAPI async web framework
    - PostgreSQL database with SQLAlchemy
    - Vector embeddings and semantic search
    - Docker containerization and orchestration
    - Comprehensive testing and documentation
    """,
    version="1.0.0",
    contact={
        "name": "Praveen K Mittal",
        "email": "contact@example.com",  # Update with actual contact
    },
    license_info={
        "name": "Portfolio Project",
        "url": "https://github.com/mittalpk/Ask-My-Docs.git"
    }
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:3001", 
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Include routers
app.include_router(auth_router.router)
app.include_router(upload_router.router) 
app.include_router(chat.router, prefix="/chat")

# Create tables on startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
