# 🚀 AskMyDocs Backend - AI Document Query System

> **Portfolio Project**: Demonstrating advanced AI/ML engineering, backend development, and DevOps skills through a production-ready intelligent document processing system.

## 📋 Backend Overview

The AskMyDocs backend is a sophisticated AI-powered application that showcases modern software engineering practices through:

- **RAG Architecture**: Complete retrieval-augmented generation pipeline
- **Multi-LLM Support**: OpenAI and Ollama integration with intelligent fallback
- **Vector Database**: ChromaDB for semantic document search and retrieval
- **Async FastAPI**: High-performance web framework with automatic documentation
- **Containerized Deployment**: Docker-based development and deployment
- **Comprehensive Testing**: Automated test suite with PDF processing validation

## 🎯 Skills Demonstrated

### **AI/ML Engineering**
- ✅ RAG (Retrieval Augmented Generation) implementation
- ✅ Vector embeddings and semantic search
- ✅ Multi-provider LLM integration (OpenAI + Ollama)
- ✅ Document processing and intelligent chunking
- ✅ Prompt engineering for accurate responses

### **Backend Development**
- ✅ FastAPI framework with async programming
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ RESTful API design with automatic documentation
- ✅ Pydantic models for data validation
- ✅ Comprehensive error handling and logging

### **DevOps & Infrastructure**
- ✅ Multi-container Docker architecture
- ✅ Docker Compose service orchestration
- ✅ Environment-based configuration management
- ✅ Volume and network management
- ✅ Service dependency coordination

### **Testing & Quality Assurance**
- ✅ Automated test suite with pytest
- ✅ PDF processing test automation
- ✅ API endpoint validation
- ✅ Error scenario coverage
- ✅ Integration testing

## 🏗️ Architecture

```
┌─────────────────────┐
│     Client API      │
│   (REST/JSON)       │
└──────────┬──────────┘
           │
┌──────────▼──────────┐    ┌─────────────────────┐
│    FastAPI App      │    │    AI Services      │
│  ┌─────────────────┐│    │  ┌─────────────────┐│
│  │ Chat Router     ││◄──►│  │ Ollama LLM      ││
│  │ • add_document  ││    │  │ • llama3        ││
│  │ • query         ││    │  │ • nomic-embed   ││
│  └─────────────────┘│    │  └─────────────────┘│
│  ┌─────────────────┐│    │  ┌─────────────────┐│
│  │ Auth Router     ││    │  │ OpenAI API      ││
│  │ • login         ││    │  │ • GPT models    ││
│  │ • register      ││    │  │ • Embeddings    ││
│  └─────────────────┘│    │  └─────────────────┘│
└──────────┬──────────┘    └─────────────────────┘
           │
┌──────────▼──────────┐    ┌─────────────────────┐
│   PostgreSQL DB     │    │    ChromaDB         │
│  ┌─────────────────┐│    │  ┌─────────────────┐│
│  │ Users           ││    │  │ Documents       ││
│  │ Documents       ││◄──►│  │ Embeddings      ││
│  │ Metadata        ││    │  │ Collections     ││
│  └─────────────────┘│    │  └─────────────────┘│
└─────────────────────┘    └─────────────────────┘
```

## 🚀 Quick Start

### **Prerequisites**
```bash
# Required software
- Docker & Docker Compose
- 8GB+ RAM (for Ollama models)
- Git

# Optional for development
- Python 3.12+
- VS Code or PyCharm
```

### **1. Environment Setup**
```bash
# Clone the repository
git clone https://github.com/mittalpk/AskMyDocs.git
cd AskMyDocs/askmydocs-backend

# Configure environment (review .env file)
# Update API keys if using OpenAI
```

### **2. Launch Services**
```bash
# Start all services
docker-compose up --build

# Services will be available at:
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - PostgreSQL: localhost:5432
# - Ollama: localhost:11434
```

### **3. Verify Installation**
```bash
# Check API health
curl http://localhost:8000/docs

# Run quick tests
docker exec askmydocs-backend python simple_test.py

# Test PDF processing
docker exec askmydocs-backend python demo_pdf_testing.py
```

## 📚 API Usage

### **Document Management**
```bash
# Add a document
curl -X POST "http://localhost:8000/chat/add_document" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "sample_doc",
       "content": "Your document content here..."
     }'

# Response
{
  "id": "sample_doc",
  "title": "sample_doc", 
  "content": "Your document content here..."
}
```

### **Query Documents**
```bash
# Ask questions about your documents
curl -X POST "http://localhost:8000/chat/query" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What are the main topics discussed?"
     }'

# Response
{
  "answer": "Based on your documents, the main topics include...",
  "source_documents": [...],
  "llm_used": "ollama"
}
```

## 🧪 Testing Infrastructure

### **Automated Test Suite**
```bash
# Quick API validation
docker exec askmydocs-backend python simple_test.py

# Comprehensive tests
docker exec askmydocs-backend python run_tests.py

# PDF processing tests
docker exec askmydocs-backend python test_pdf_processing_enhanced.py
```

### **PDF Testing Demo**
The system includes advanced PDF testing capabilities:

```bash
# Add your own PDFs
cp your_document.pdf test_pdf_documents/

# Process automatically
docker exec askmydocs-backend python test_pdf_processing_enhanced.py

# Results: Automatic discovery, processing, and validation
```

**Sample Test Output:**
```
🔍 Discovered 4 PDF files in /app/test_pdf_documents
   📄 sample_document.pdf (2,270 bytes)
   📄 technology_overview.pdf (2,300 bytes)
   📄 business_strategy.pdf (2,278 bytes)
   📄 research_methodology.pdf (2,332 bytes)

📊 Processing Summary:
   Total PDFs found: 4
   Successfully processed: 4
   Documents added to API: 4

✅ End-to-end PDF workflow validated
```

## 🔧 Development Features

### **Code Quality**
- **Type Safety**: Full type hints throughout
- **Error Handling**: Comprehensive exception management
- **Logging**: Structured logging for debugging
- **Documentation**: Inline code documentation

### **Configuration Management**
```python
# Flexible, secure configuration
class Settings(BaseSettings):
    database_url: str
    openai_api_key: str
    llm_provider: str = "ollama"
    ollama_host: str = "ollama"
    ollama_model: str = "nomic-embed-text"
    
    class Config:
        env_file = ".env"
        extra = "forbid"
```

### **Professional API Design**
```python
@router.post("/add_document", response_model=DocumentOut)
async def add_document(doc: DocumentCreate):
    """Add a document to the knowledge base with automatic embedding generation."""
    try:
        if embedding_fn is None:
            raise RuntimeError("No embedding function available")
        
        # Process document with ChromaDB
        collection.add(
            documents=[doc.content],
            metadatas=[{"title": doc.title}],
            ids=[str(doc.title)]
        )
        
        return DocumentOut(
            id=str(doc.title), 
            title=doc.title, 
            content=doc.content
        )
    except Exception as e:
        logger.error(f"Document processing failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
```

## 📊 Performance & Scalability

### **Optimization Features**
- **Async Operations**: Non-blocking I/O for better concurrency
- **Connection Pooling**: Efficient database connections
- **Vector Caching**: Fast similarity search with ChromaDB
- **Error Recovery**: Graceful fallback mechanisms

### **Monitoring & Observability**
- **Structured Logging**: JSON-formatted logs for analysis
- **Error Tracking**: Comprehensive exception logging
- **Performance Metrics**: Request timing and success rates
- **Health Checks**: Service availability monitoring

## 🔄 Services Architecture

### **PostgreSQL Database**
- **User Management**: Authentication and authorization
- **Document Metadata**: File information and processing status
- **Async Operations**: SQLAlchemy async support
- **Migration Support**: Alembic for schema changes

### **ChromaDB Vector Store**
- **Embedding Storage**: Document vector representations
- **Similarity Search**: Semantic document retrieval
- **Collection Management**: Organized document groups
- **Persistent Storage**: Data persistence across restarts

### **Ollama AI Service**
- **Local LLM**: Privacy-focused local AI processing
- **Model Management**: Automatic model downloading
- **Embedding Generation**: Document vectorization
- **Text Generation**: Query response generation

## 🎯 Portfolio Highlights

This backend demonstrates professional-level skills in:

### **Modern Python Development**
- FastAPI framework mastery
- Async programming patterns
- Type-safe development practices
- Professional error handling

### **AI/ML Engineering**
- RAG architecture implementation
- Vector database integration
- Multi-model LLM support
- Production AI deployment

### **DevOps Practices**
- Container orchestration
- Service dependency management
- Environment configuration
- Automated testing strategies

### **API Design Excellence**
- RESTful endpoint design
- Automatic documentation
- Request/response validation
- Professional error responses

---

**Project Status**: Production-ready portfolio demonstration  
**Author**: Praveen K Mittal  
**Purpose**: Showcase advanced backend, AI/ML, and DevOps skills  
**Tech Stack**: Python, FastAPI, PostgreSQL, ChromaDB, Docker, Ollama