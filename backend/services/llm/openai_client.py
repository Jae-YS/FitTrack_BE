from openai import AsyncOpenAI
from backend.core.config import settings


if not settings.OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not found in environment variables.")

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
