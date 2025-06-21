import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from backend.api.routes import users, logs, suggestions, route_planner
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()
app.include_router(users.router, prefix="/api/users")
app.include_router(logs.router, prefix="/api/logs")
app.include_router(suggestions.router, prefix="/api/suggestions")
app.include_router(route_planner.router, prefix="/api/routes")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://fit-track-fe.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY"),
)
