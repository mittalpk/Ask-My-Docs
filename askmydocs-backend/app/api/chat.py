from fastapi import APIRouter, HTTPException
from app.config import settings
from chromadb.utils import embedding_functions
from chromadb import Client
from app.schemas import DocumentCreate, DocumentOut
import logging
from app.schemas import QueryRequest, QueryResponse
from app.utils import ask_hybrid_llm  # a helper to query OpenAI/Ollama

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

# Initialize ChromaDB client
client = Client()

# Choose embedding function based on settings
if settings.llm_provider.lower() == "ollama":
    try:
        embedding_fn = embedding_functions.OllamaEmbeddingFunction(
            url=f"http://{settings.ollama_host}:{settings.ollama_port}",
            model_name=settings.ollama_model,
        )
        print("Using Ollama embeddings")
    except Exception as e:
        logger.error(f"Failed to initialize Ollama embedding: {e}")
        embedding_fn = None
else:
    # Default to OpenAI
    try:
        embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
            api_key=settings.openai_api_key,
            model_name="text-embedding-3-small"
        )
        print("Using OpenAI embeddings")
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI embedding: {e}")
        embedding_fn = None

# Create or get collection
collection = client.get_or_create_collection(
    name="documents", embedding_function=embedding_fn
)

@router.post("/add_document", response_model=DocumentOut)
async def add_document(doc: DocumentCreate):
    try:
        if embedding_fn is None:
            raise RuntimeError(
                "No embedding function available. Check your LLM settings."
            )

        collection.add(
            documents=[doc.content],
            metadatas=[{"title": doc.title}],
            ids=[str(doc.title)]
        )

        logger.info(f"Document added: {doc.title}")
        return {"id": str(doc.title), "title": doc.title, "content": doc.content}

    except Exception as e:
        logger.error(f"Failed to add document '{doc.title}': {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add document '{doc.title}': {str(e)}"
        )


@router.post("/query", response_model=QueryResponse)
async def query_docs(request: QueryRequest):
    """
    Ask a question about uploaded documents using selected LLM (Ollama or OpenAI).
    """
    answer, sources, llm_used = await ask_hybrid_llm(request.query, request.model)
    return {"answer": answer, "source_documents": sources, "llm_used": llm_used}
