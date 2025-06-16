import bcrypt
import os
from models.sql_models import User
from itsdangerous import URLSafeSerializer

SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")
if not SESSION_SECRET_KEY:
    raise ValueError("SESSION_SECRET_KEY environment variable is not set")

serializer = URLSafeSerializer(SESSION_SECRET_KEY)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_session_token(user: User) -> str:
    return serializer.dumps({"user_id": user.id})


def decode_session_token(token: str) -> dict:
    try:
        return serializer.loads(token)
    except Exception:
        return None
