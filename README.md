# AskMyDocs

AskMyDocs is an AI-powered document query system that allows users to upload documents and ask questions about their content using Large Language Models. Built with Python and FastAPI, it demonstrates modern backend development practices and AI integration.

## What it does

Upload PDF or text documents and ask questions in plain English. The system extracts document content, creates semantic embeddings, and uses retrieval-augmented generation (RAG) to provide accurate answers based on your documents.

## Key features

- Document processing for PDF and text files
- Semantic search using vector embeddings
- Support for both OpenAI and local Ollama models
- RESTful API with automatic documentation
- Comprehensive test suite
- Docker containerization for easy deployment

## Technology stack

- **Backend**: FastAPI with async support
- **Database**: PostgreSQL with SQLAlchemy ORM  
- **Vector DB**: ChromaDB for embeddings
- **AI Models**: OpenAI GPT and local Ollama
- **Testing**: Pytest with custom PDF processing tests
- **Infrastructure**: Docker and Docker Compose

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

### Installation

1. Clone the repository:
```bash
git clone https://github.com/mittalpk/AskMyDocs.git
cd AskMyDocs/askmydocs-backend
```

2. Start the services:
```bash
docker-compose up --build
```

3. Wait for initialization (2-3 minutes for Ollama to download models)

4. Access the API documentation at `http://localhost:8000/docs`

## Usage

### Add a document
```bash
curl -X POST "http://localhost:8000/chat/add_document" \
     -H "Content-Type: application/json" \
     -d '{"title": "sample", "content": "Your document content here"}'
```

### Query documents
```bash
curl -X POST "http://localhost:8000/chat/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "What does the document say about...?"}'
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

## Configuration

The system supports both OpenAI and local Ollama models. Configure via environment variables in `.env`:

- `LLM_PROVIDER`: "openai" or "ollama"
- `OPENAI_API_KEY`: Your OpenAI API key (if using OpenAI)
- `OLLAMA_HOST`: Ollama server host (default: localhost)

## License

This project is open source and available under the MIT License.
