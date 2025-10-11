from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from app.services.embeddings_service import get_chroma_client
from app.config import settings
import openai

openai.api_key = settings.openai_api_key

def get_qa_chain():
    # create LLM
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key=settings.openai_api_key)
    vectordb = get_chroma_client()
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    return qa

def answer_question(question: str):
    qa = get_qa_chain()
    resp = qa.run(question)
    return resp
