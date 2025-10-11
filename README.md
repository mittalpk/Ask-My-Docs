# AskMyDocs - AI-Powered Document Query System

AskMyDocs is a complete full-stack application that allows users to upload documents and ask questions about their content using Large Language Models. Built with React, FastAPI, and Ollama, it demonstrates modern full-stack development with AI integration.

## What it does

Upload PDF, TXT, or Markdown documents through a beautiful web interface and ask questions in plain English. The system extracts document content, creates semantic embeddings, and uses retrieval-augmented generation (RAG) to provide accurate answers based on your documents.

## Key Features

### 🎨 **Frontend (React)**
- **Modern UI/UX** - Professional, responsive design with gradient themes
- **User Authentication** - Secure JWT-based login/registration system
- **Document Upload** - Drag-and-drop file upload with progress indicators
- **Real-time Chat** - Interactive chat interface for document queries
- **Auto-logout** - 15-minute inactivity timeout for security
- **Password Management** - Secure password change functionality

### 🚀 **Backend (FastAPI)**
- **Document Processing** - Support for PDF, TXT, and Markdown files
- **Vector Search** - ChromaDB integration for semantic document retrieval
- **Multi-LLM Support** - Local Ollama models with automatic fallback
- **User Management** - Complete authentication and user session handling
- **RESTful API** - Auto-generated documentation with OpenAPI/Swagger

### 🤖 **AI Integration**
- **RAG Pipeline** - Retrieval-Augmented Generation for accurate answers
- **Local Models** - Ollama integration with llama3.2:1b and llama3 models
- **Semantic Embeddings** - nomic-embed-text for document vectorization
- **Smart Fallbacks** - Graceful degradation when AI models are unavailable

### 🐳 **Infrastructure**
- **Containerized** - Complete Docker setup with pre-loaded AI models
- **Production Ready** - PostgreSQL database with proper relationships
- **Scalable** - Async FastAPI backend with connection pooling
- **Persistent** - Models baked into Docker images for consistency

## Technology Stack

- **Frontend**: React 18, Vite, React Router, Axios
- **Backend**: FastAPI with async support, SQLAlchemy ORM
- **Database**: PostgreSQL 15 with user authentication
- **Vector Database**: ChromaDB for semantic embeddings
- **AI Models**: Ollama (llama3.2:1b, llama3, nomic-embed-text)
- **Authentication**: JWT tokens with bcrypt password hashing
- **Infrastructure**: Docker Compose with multi-service orchestration
- **Testing**: Pytest with comprehensive PDF processing tests

## Architecture

The system follows a standard web application pattern:

1. **API Layer**: FastAPI handles HTTP requests and responses
2. **Processing**: Documents are extracted and chunked for embedding
3. **Storage**: Text content stored in PostgreSQL, embeddings in ChromaDB
4. **Retrieval**: Vector similarity search finds relevant document chunks
5. **Generation**: LLM generates responses using retrieved context

## How it works

1. Upload a document through the `/add_document` endpoint
2. System extracts text content and creates embeddings
3. Ask questions via the `/query` endpoint
4. System finds relevant document sections using semantic search
5. LLM generates an answer based on the retrieved context

## Project Structure

```
AskMyDocs/
├── README.md
├── docker-compose.yml              # Full stack orchestration
├── askmydocs-frontend/            # React frontend
│   ├── Dockerfile
│   ├── package.json
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.jsx         # Authentication
│   │   │   ├── Register.jsx      # User registration  
│   │   │   ├── Dashboard.jsx     # Main UI
│   │   │   └── NavBar.jsx        # Navigation
│   │   ├── api.js               # Backend API client
│   │   └── App.jsx              # Main app component
│   └── public/
└── askmydocs-backend/
    ├── docker-compose.yml
    ├── Dockerfile
    ├── requirements.txt
    ├── app/
    │   ├── main.py                    # FastAPI application
    │   ├── config.py                  # Configuration
    │   ├── models.py                  # Database models
    │   ├── schemas.py                 # Pydantic schemas
    │   ├── api/
    │   │   ├── auth.py               # Auth endpoints
    │   │   └── chat.py               # Document endpoints
    │   └── services/
    │       ├── embeddings_service.py  # Embedding logic
    │       └── rag_service.py        # RAG pipeline
    ├── tests/                        # Test suite
    ├── test_documents/              # Sample documents
    └── test_pdf_documents/          # PDF test files
```

## Getting Started

### Prerequisites
- Docker and Docker Compose
- 8GB+ RAM for local LLM models

### Installation with Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/mittalpk/Ask-My-Docs.git
cd Ask-My-Docs
```

2. Start all services (backend + frontend + database):
```bash
docker-compose up --build
```

3. Wait for initialization (2-3 minutes for Ollama to download models)

4. Access the application:
   - **Frontend UI**: `http://localhost:3001` (main application)
   - **Backend API**: `http://localhost:8000/docs` (API documentation)

## Usage

### Web Interface (Recommended)

1. **Register/Login**: Create an account at `http://localhost:3001`
2. **Upload Documents**: Use the upload tab to add PDF, TXT, or MD files
3. **Add Text**: Directly paste text content for indexing
4. **Ask Questions**: Chat with your documents using natural language
5. **Manage Account**: Change password, auto-logout after 15 minutes

### API Usage (Advanced)

#### Authentication
```bash
# Register
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"name": "Your Name", "email": "email@example.com", "password": "password123"}'

# Login  
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "email@example.com", "password": "password123"}'
```

#### Document Management
```bash
# Upload document (with auth token)
curl -X POST "http://localhost:8000/upload/" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -F "file=@document.pdf"

# Query documents
curl -X POST "http://localhost:8000/chat/query" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"query": "What are the main topics in the document?"}'
```

### Test with PDFs
```bash
# Add PDF files to test directory
cp your_document.pdf test_pdf_documents/

# Run PDF processing tests
docker exec askmydocs-backend python test_pdf_processing_enhanced.py
```

## Testing

Run the test suite:
```bash
# Quick validation
docker exec askmydocs-backend python simple_test.py

# Full test suite
docker exec askmydocs-backend python run_tests.py
```

## Screenshots

### Login/Register
Professional authentication with password strength requirements and user-friendly design.

### Dashboard
Split-screen interface with document upload on the left and chat interface on the right.

### Document Upload
Drag-and-drop file upload with support for PDF, TXT, and Markdown files.

### AI Chat
Real-time conversation with your documents using retrieval-augmented generation.

## Configuration

The system uses local Ollama models by default (no API keys required). Environment variables:

- `LLM_PROVIDER`: "ollama" (default)
- `OLLAMA_HOST`: Ollama server host (default: ollama)
- `OLLAMA_PORT`: Ollama server port (default: 11434)
- `JWT_SECRET_KEY`: JWT signing secret (change in production)
- `DATABASE_URL`: PostgreSQL connection string

## Performance Optimizations

- **Model Caching**: AI models pre-loaded in Docker images
- **Smart Fallbacks**: Automatic fallback from large to small models
- **Optimized Parameters**: Reduced token counts for faster responses
- **Connection Pooling**: Async database connections
- **Auto-timeout**: User sessions expire after 15 minutes of inactivity

## License

This project is open source and available under the MIT License.
