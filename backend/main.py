import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from backend.api.routes import users, logs
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()
app.include_router(users.router, prefix="/api")
app.include_router(logs.router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # adjust to match your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY"),
)
