import requests
from typing import List, Tuple
from app.config import settings
from app.schemas import SourceDoc
import logging

logger = logging.getLogger(__name__)

async def ask_hybrid_llm(query: str) -> Tuple[str, List[SourceDoc], str]:
    """
    Query documents using hybrid LLM approach.
    Returns: (answer, source_documents, llm_used)
    """
    try:
        # For now, return a basic implementation
        # This can be enhanced later with actual RAG functionality
        
        if settings.llm_provider.lower() == "ollama":
            # Use Ollama for text generation
            try:
                response = requests.post(
                    f"http://{settings.ollama_host}:{settings.ollama_port}/api/generate",
                    json={
                        "model": "llama3",  # or another text generation model
                        "prompt": f"Answer the following question concisely: {query}",
                        "stream": False,
                        "options": {
                            "num_predict": 100  # Limit response length for faster generation
                        }
                    },
                    timeout=60  # Increased timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get("response", "No answer generated")
                    return answer.strip(), [], "ollama"
                else:
                    logger.error(f"Ollama API error: {response.status_code}")
                    return "Error generating response with Ollama", [], "error"
                    
            except Exception as e:
                logger.error(f"Error with Ollama: {e}")
                return f"Error: {str(e)}", [], "error"
        else:
            # Fallback response when OpenAI is configured but not implemented
            return "OpenAI integration not implemented yet", [], "openai"
            
    except Exception as e:
        logger.error(f"Error in ask_hybrid_llm: {e}")
        return f"Error: {str(e)}", [], "error"