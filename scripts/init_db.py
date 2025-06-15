import sys
import os
import psycopg2

print(psycopg2.__version__)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from backend.db.session import engine
from backend.models.sql_models import DailyLog

from backend.models.sql_models import Workout
from backend.models.sql_models import User

DailyLog.metadata.create_all(bind=engine)
Workout.metadata.create_all(bind=engine)
User.metadata.create_all(bind=engine)
print(engine.connect())
