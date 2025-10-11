from sqlalchemy.future import select

from app.models import User, Document
from sqlalchemy.ext.asyncio import AsyncSession
import bcrypt

def hash_password(password: str) -> str:
    # Use bcrypt directly to avoid passlib initialization issues
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

async def create_user(db: AsyncSession, name: str, email: str, password: str):
    hashed_pw = hash_password(password)
    user = User(name=name, email=email, password=hashed_pw)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()
