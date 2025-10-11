from fastapi import APIRouter, Depends, HTTPException
from app.schemas import UserCreate, UserOut
from app.database import get_db
from app.crud import create_user, get_user_by_email
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await create_user(db, user.name, user.email, user.password)
    return new_user
