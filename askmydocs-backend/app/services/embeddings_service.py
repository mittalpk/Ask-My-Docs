import os
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import settings

def get_chroma_client(persist_directory="./chroma_db"):
    # create embeddings object using Ollama
    embeddings = OllamaEmbeddings(
        base_url=f"http://{settings.ollama_host}:{settings.ollama_port}",
        model="nomic-embed-text"
    )
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return vectordb

async def embed_and_upsert_from_text(doc_id: int, text: str, metadata: dict):
    """
    Splits the text into chunks, creates embeddings and adds to Chroma.
    metadata is arbitrary dict stored with records (e.g. {"doc_id": doc_id, "filename": "..."})
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_text(text)
    vectordb = get_chroma_client()
    # prepare list of texts with metadata
    texts = []
    metadatas = []
    ids = []
    for i, chunk in enumerate(docs):
        texts.append(chunk)
        metadatas.append({**metadata, "chunk_index": i})
        ids.append(f"{metadata.get('doc_id')}_{i}")
    
    # Use add_texts instead of add_documents for string inputs
    vectordb.add_texts(texts=texts, metadatas=metadatas, ids=ids)
