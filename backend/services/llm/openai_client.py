import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY not found in environment variables.")

client = AsyncOpenAI(api_key=api_key)
