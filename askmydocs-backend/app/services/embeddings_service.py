import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config import CHROMA_PERSIST_DIR, OPENAI_API_KEY
import openai

# Ensure OpenAI key is set for the langchain components
openai.api_key = OPENAI_API_KEY

def get_chroma_client(persist_directory=CHROMA_PERSIST_DIR):
    # create embeddings object
    embeddings = OpenAIEmbeddings()
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
    # prepare list of documents with metadata
    documents = []
    metadatas = []
    ids = []
    for i, chunk in enumerate(docs):
        documents.append(chunk)
        metadatas.append({**metadata, "chunk_index": i})
        ids.append(f"{metadata.get('doc_id')}_{i}")
    vectordb.add_documents(documents=documents, metadatas=metadatas, ids=ids)
