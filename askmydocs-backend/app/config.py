# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@askmydocs-postgres:5432/askmydocs"
    openai_api_key: str = "sk-dummy-key"
    ollama_api_url: str = "http://ollama:11434"

    # LLM Settings
    llm_provider: str = "ollama"        # default LLM provider
    ollama_host: str = "ollama"
    ollama_port: int = 11434
    ollama_model: str = "nomic-embed-text"
    
    # JWT Settings
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Azure Storage
    azure_storage_connection_string: str = ""
    
    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:5173"


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "forbid"  # keep strict checking

settings = Settings()

# Export individual settings for backward compatibility
JWT_SECRET_KEY = settings.jwt_secret_key
JWT_ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
AZURE_STORAGE_CONNECTION_STRING = settings.azure_storage_connection_string

