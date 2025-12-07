from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from app.services.embeddings_service import get_chroma_client
from app.config import settings

# Define a custom prompt template that ensures the LLM uses the context
CUSTOM_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a helpful assistant that answers questions based ONLY on the provided documents.

Context from documents:
{context}

Question: {question}

Answer the question using ONLY the information from the documents above. If the answer is not in the documents, say "I cannot find this information in the provided documents." Be direct and concise."""
)

def get_qa_chain():
    # create LLM using Ollama
    llm = Ollama(
        base_url=settings.ollama_api_url,
        model="llama3",
        temperature=0
    )
    vectordb = get_chroma_client()
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})
    
    # Create QA chain with custom prompt
    qa = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        retriever=retriever,
        chain_type_kwargs={"prompt": CUSTOM_PROMPT},
        return_source_documents=False
    )
    return qa

def answer_question(question: str):
    qa = get_qa_chain()
    resp = qa.run(question)
    return resp
