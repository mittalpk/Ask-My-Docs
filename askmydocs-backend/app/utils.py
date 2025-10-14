import requests
from typing import List, Tuple
from app.config import settings
from app.schemas import SourceDoc
from app.services.embeddings_service import get_chroma_client
import logging

logger = logging.getLogger(__name__)

async def ask_hybrid_llm(query: str, model: str = 'llama3') -> Tuple[str, List[SourceDoc], str]:
    """
    Query documents using RAG approach with vector search.
    Args:
        query: User's question
        model: Selected model ('llama3' or 'openai')
    Returns: (answer, source_documents, llm_used)
    """
    try:
        # Step 1: Retrieve relevant documents from vector database
        vectordb = get_chroma_client()
        
        # Search for relevant documents
        try:
            search_results = vectordb.similarity_search_with_score(query, k=3)
            relevant_docs = []
            source_docs = []
            
            for doc, score in search_results:
                relevant_docs.append(doc.page_content)
                source_docs.append(SourceDoc(
                    doc_id=str(doc.metadata.get("doc_id", "unknown")),
                    filename=doc.metadata.get("filename", "unknown"),
                    content=doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    relevance_score=float(score)
                ))
            
            # Step 2: Create context from retrieved documents
            if relevant_docs:
                context = "\n\n".join([f"Document {i+1}: {doc}" for i, doc in enumerate(relevant_docs)])
                prompt = f"""Based on the following documents, answer the user's question. If the documents don't contain relevant information, say so.

Documents:
{context}

Question: {query}

Answer based on the documents provided:"""
            else:
                prompt = f"No relevant documents found for the question: {query}\n\nPlease let the user know that no documents are available or uploaded yet."
                
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            prompt = f"Unable to search documents due to an error. Question: {query}\n\nPlease let the user know there was an issue accessing their documents."
            source_docs = []
        
        # Step 3: Generate answer using selected model
        if model.lower() == "openai":
            return await generate_openai_response(prompt, source_docs)
        else:  # Default to llama3 (Ollama)
            return await generate_ollama_response(prompt, source_docs)
            
    except Exception as e:
        logger.error(f"Error in ask_hybrid_llm: {e}")
        return f"Error: {str(e)}", [], "error"


async def generate_ollama_response(prompt: str, source_docs: List[SourceDoc]) -> Tuple[str, List[SourceDoc], str]:
    """Generate response using Ollama models"""
    try:
        # Try smaller, faster model first
        models_to_try = ["llama3.2:1b", "llama3"]
        response = None
        
        for model_name in models_to_try:
            try:
                response = requests.post(
                    f"http://{settings.ollama_host}:{settings.ollama_port}/api/generate",
                    json={
                        "model": model_name,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "num_predict": 120,     # Shorter responses
                            "temperature": 0.1,     # Very focused answers
                            "top_p": 0.9,           # Limit token selection
                            "top_k": 20             # Further limit choices
                        }
                    },
                    timeout=45  # Shorter timeout
                )
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get("response", "No answer generated")
                    return answer.strip(), source_docs, f"ollama-{model_name}"
                    
            except Exception as e:
                logger.warning(f"Failed with model {model_name}: {e}")
                continue  # Try next model
        
        # If all Ollama models failed
        logger.error("All Ollama models failed")
        if source_docs:
            fallback_answer = f"Based on your documents: {source_docs[0].content[:200]}..."
            return fallback_answer, source_docs, "fallback"
        else:
            return "No documents found to answer your question. Please upload some documents first.", [], "error"
            
    except Exception as e:
        logger.error(f"Error with Ollama: {e}")
        if source_docs:
            fallback_answer = f"I found relevant content in your documents: {source_docs[0].content[:300]}..."
            return fallback_answer, source_docs, "fallback"
        else:
            return "Unable to generate response. Please try uploading documents first or try again later.", [], "error"


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