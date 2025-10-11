from fastapi import APIRouter, Depends, HTTPException
from app.schemas import ChatRequest
from app.services.rag_service import answer_question

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/")
async def chat_endpoint(req: ChatRequest):
    # Simple flow: ask RAG service the question
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    answer = answer_question(req.question)
    return {"answer": answer}
