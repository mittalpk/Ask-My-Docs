from pydantic import BaseModel
from typing import List


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    class Config:
        orm_mode = True

class DocumentCreate(BaseModel):
    title: str
    content: str

class DocumentOut(DocumentCreate):
    id: str

class QueryRequest(BaseModel):
    query: str

class SourceDoc(BaseModel):
    doc_id: str
    filename: str
    content: str
    relevance_score: float = 0.0

class QueryResponse(BaseModel):
    answer: str
    source_documents: List[SourceDoc]
    llm_used: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ChatRequest(BaseModel):
    question: str

class UploadResponse(BaseModel):
    document_id: int
    filename: str
    blob_url: str