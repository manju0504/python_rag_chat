from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    VECTOR_DB_PATH: str = "./vector_db"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    LLM_TYPE: str = "ollama"
    OLLAMA_BASE_URL: str = "http://localhost:11434"  # Default Ollama URL
    OLLAMA_MODEL: str = "llama3.1"  # Default Ollama model
    class Config:
        env_file = ".env"

settings = Settings()