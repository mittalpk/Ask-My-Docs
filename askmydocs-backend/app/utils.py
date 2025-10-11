import requests
from typing import List, Tuple
from app.config import settings
from app.schemas import SourceDoc
from app.services.embeddings_service import get_chroma_client
import logging

logger = logging.getLogger(__name__)

async def ask_hybrid_llm(query: str) -> Tuple[str, List[SourceDoc], str]:
    """
    Query documents using RAG approach with vector search.
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
        
        # Step 3: Generate answer using Ollama
        if settings.llm_provider.lower() == "ollama":
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
                            break  # Success, use this response
                        
                    except Exception as e:
                        logger.warning(f"Failed with model {model_name}: {e}")
                        continue  # Try next model
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get("response", "No answer generated")
                    return answer.strip(), source_docs, "ollama"
                else:
                    logger.error(f"Ollama API error: {response.status_code}")
                    # Fallback: provide a basic response using retrieved documents
                    if relevant_docs:
                        fallback_answer = f"Based on your documents: {relevant_docs[0][:200]}..."
                        return fallback_answer, source_docs, "fallback"
                    else:
                        return "No documents found to answer your question. Please upload some documents first.", [], "error"
                    
            except Exception as e:
                logger.error(f"Error with Ollama: {e}")
                # Fallback response with document content if available
                if relevant_docs:
                    fallback_answer = f"I found relevant content in your documents: {relevant_docs[0][:300]}..."
                    return fallback_answer, source_docs, "fallback"
                else:
                    return "Unable to generate response. Please try uploading documents first or try again later.", [], "error"
        else:
            # Fallback response when OpenAI is configured but not implemented
            return "OpenAI integration not implemented yet", [], "openai"
            
    except Exception as e:
        logger.error(f"Error in ask_hybrid_llm: {e}")
        return f"Error: {str(e)}", [], "error"