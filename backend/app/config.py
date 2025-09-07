import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    CORS_ORIGINS: list = ["http://localhost:3000"]

settings = Settings()
