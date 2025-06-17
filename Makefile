# Environment config
PYTHON=python
UVICORN=uvicorn
APP_MODULE=backend.main:app
ENV_FILE=backend/.env
PYTHONPATH=.

include $(ENV_FILE)
export

# Run FastAPI app
run:
	PYTHONPATH=$(PYTHONPATH) $(UVICORN) $(APP_MODULE) --reload

# Create new Alembic migration
migrate:
	PYTHONPATH=$(PYTHONPATH) alembic revision --autogenerate -m "$(m)"

# Apply latest migration
upgrade:
	PYTHONPATH=$(PYTHONPATH) alembic upgrade head

# Run the migration script
migrate-script:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/run_migrations.py

# Seed database with mock user and workout data
seed:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/reset_db.py

# Reset DB: drop all, recreate schema, seed data
reset:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) scripts/reset_db.py

# Format code
format:
	black backend scripts

# Run all: upgrade then seed
init: upgrade seed

# Run tests
test:
	PYTHONPATH=$(PYTHONPATH) pytest
