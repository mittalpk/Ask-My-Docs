from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
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
    title: str
    content: str

class QueryResponse(BaseModel):
    answer: str
    source_documents: List[SourceDoc]
    llm_used: str