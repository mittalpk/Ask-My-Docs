from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # This will now store a hashed password
    
    # Relationship to documents
    documents = relationship("Document", back_populates="user")

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    blob_url = Column(String, nullable=False)
    # Optionally keep title/content for future use
    title = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    
    # Relationship to user
    user = relationship("User", back_populates="documents")
