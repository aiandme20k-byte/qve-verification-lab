import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration from environment variables."""
    
    DATABASE_URL: str = "sqlite:///./qve_verification.db"
    DATA_DIR: str = "./data"
    GEMINI_API_KEY: str = ""
    
    class Config:
        env_file = ".env"


settings = Settings()

# Ensure data directory exists
os.makedirs(settings.DATA_DIR, exist_ok=True)
