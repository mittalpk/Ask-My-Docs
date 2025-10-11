# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    openai_api_key: str
    ollama_api_url: str = "http://ollama:11434"

    # These were in your env but missing in Settings
    llm_provider: str = "ollama"        # default LLM provider
    ollama_host: str = "ollama"
    ollama_port: int = 11434
    ollama_model: str = "nomic-embed-text"


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "forbid"  # keep strict checking

settings = Settings()

