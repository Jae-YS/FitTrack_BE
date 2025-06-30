import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from backend.api.routes import (
    users,
    daily_entries,
    dashboard,
    route_planner,
    training_plans,
    completed_workouts,
)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://fit-track-fe.vercel.app",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY"),
)


API_PREFIX = "/api"

app.include_router(users.router, prefix=API_PREFIX)
app.include_router(daily_entries.router, prefix=API_PREFIX)
app.include_router(route_planner.router, prefix=API_PREFIX)
app.include_router(training_plans.router, prefix=API_PREFIX)
app.include_router(completed_workouts.router, prefix=API_PREFIX)
app.include_router(dashboard.router, prefix=API_PREFIX)
