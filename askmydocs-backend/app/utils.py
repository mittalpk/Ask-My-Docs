import logging
from typing import List, Tuple

from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama

from app.config import settings
from app.schemas import SourceDoc
from app.services.embeddings_service import get_chroma_client

logger = logging.getLogger(__name__)


# Keep the prompt in sync with rag_service to force document-grounded answers.
CUSTOM_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a helpful assistant that answers questions based ONLY on the provided documents.

Context from documents:
{context}

Question: {question}

Answer the question using ONLY the information from the documents above. If the answer is not in the documents, say \"I cannot find this information in the provided documents.\" Be direct and concise."""
)


async def ask_hybrid_llm(query: str, model: str = "ollama") -> Tuple[str, List[SourceDoc], str]:
    """
    Query the persisted Chroma vector store and answer with Ollama using the same embeddings used on upload.
    Returns: (answer, source_documents, llm_used)
    """
    try:
        vectordb = get_chroma_client()
        retriever = vectordb.as_retriever(search_kwargs={"k": 5})
        docs = retriever.get_relevant_documents(query)

        if docs:
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Deduplicate source documents by filename
            seen_filenames = set()
            source_docs = []
            for i, doc in enumerate(docs):
                filename = doc.metadata.get("filename", f"document_{i}")
                if filename not in seen_filenames:
                    seen_filenames.add(filename)
                    source_docs.append(SourceDoc(
                        doc_id=str(doc.metadata.get("doc_id", i)),
                        filename=filename,
                        content=doc.page_content,
                        relevance_score=0.0,
                    ))
        else:
            context = ""
            source_docs = []

        prompt = CUSTOM_PROMPT.format(context=context or "No documents found.", question=query)

        # Use Ollama locally (aligned with embeddings + rag_service)
        llm = Ollama(base_url=settings.ollama_api_url, model="llama3", temperature=0)
        answer = llm.invoke(prompt).strip()

        if not docs:
            return "I cannot find this information in the provided documents.", source_docs, "ollama-llama3"

        return answer, source_docs, "ollama-llama3"

    except Exception as e:
        logger.error(f"Error in ask_hybrid_llm: {e}")
        return f"Error: {str(e)}", [], "error"


async def generate_openai_response(prompt: str, source_docs: List[SourceDoc]) -> Tuple[str, List[SourceDoc], str]:
    """Generate response using OpenAI API"""
    try:
        from openai import OpenAI
        
        if not settings.openai_api_key or settings.openai_api_key == "sk-dummy-key":
            return "OpenAI API key not configured. Please set a valid OPENAI_API_KEY environment variable.", [], "error"
        
        # Initialize OpenAI client
        client = OpenAI(api_key=settings.openai_api_key)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on provided documents. Keep your answers concise and accurate."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.1
        )
        
        answer = response.choices[0].message.content.strip()
        return answer, source_docs, "openai-gpt-3.5-turbo"
        
    except ImportError:
        return "OpenAI library not installed. Please install: pip install openai", [], "error"
    except Exception as e:
        logger.error(f"Error with OpenAI: {e}")
        return f"OpenAI API error: {str(e)}", [], "error"