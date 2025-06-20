# ---- Run Test ----
import asyncio
from datetime import date, timedelta
from backend.models.sql_models import Workout
from backend.services.llm.workout_generator import generate_next_week_plan


if __name__ == "__main__":
    # Create some mock workouts
    mock_workouts = [
        Workout(
            user_id=1,
            log_date=date.today() - timedelta(days=14),
            type="easy",
            distance_km=4,
            pace_min_per_km=7.2,
        ),
        Workout(
            user_id=1,
            log_date=date.today() - timedelta(days=13),
            type="tempo",
            distance_km=5,
            pace_min_per_km=6.1,
        ),
        Workout(
            user_id=1,
            log_date=date.today() - timedelta(days=7),
            type="long",
            distance_km=7,
            pace_min_per_km=6.8,
        ),
        Workout(
            user_id=1,
            log_date=date.today() - timedelta(days=1),
            type="recovery",
            distance_km=3,
            pace_min_per_km=7.5,
        ),
    ]

    async def test():
        plan = await generate_next_week_plan(
            race_type="Half Marathon",
            race_day="2025-09-15",
            level="beginner",
            week_number=4,
            recent_workouts=mock_workouts,
        )
        print("\nGenerated Plan:\n", plan)

    asyncio.run(test())
