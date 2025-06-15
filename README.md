# FitTrack AI – Backend

The backend service for FitTrack AI, a smart fitness tracker that uses LLMs to summarize workouts and generate weekly progress suggestions.

## Features

- User registration and workout logging
- AI-generated summaries for each workout
- Weekly suggestions generated from workout trends
- PostgreSQL with SQLAlchemy ORM
- FastAPI framework
- Async OpenAI integration
- Alembic migrations
- Docker support

## Tech Stack

- **FastAPI** (async API framework)
- **SQLAlchemy** (ORM)
- **PostgreSQL** (relational DB)
- **OpenAI GPT** (LLM-based summaries)
- **Alembic** (migrations)
- **Docker** (containerization)

## Project Structure

```
fittrack-ai-backend/
├── backend/
│   ├── api/            # Route definitions
│   ├── db/             # DB session and connection
│   ├── models/         # Pydantic and SQLAlchemy models
│   ├── services/       # Business logic and AI integration
│   └── tasks/          # Async background jobs
├── alembic/            # DB migration logic
├── scripts/            # CLI testing or utility scripts
├── tests/              # Pytest-based test suite
```

## Setup

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Set environment variables**

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key
DATABASE_URL=postgresql://user:password@localhost:5432/fittrack
```

3. **Run the API**

```bash
uvicorn backend.main:app --reload
```

4. **Initialize the database**

```bash
alembic upgrade head
```

## Docker

```bash
docker build -t fittrack-backend .
docker run -p 8000:8000 fittrack-backend
```
