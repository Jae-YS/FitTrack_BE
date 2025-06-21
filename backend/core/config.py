from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    OPENAI_API_KEY: str
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]
    ORS_API_KEY: str

    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env"


settings = Settings()
