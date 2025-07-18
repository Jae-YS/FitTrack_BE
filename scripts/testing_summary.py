import asyncio
from backend.services.llm.workout_generator import generate_first_week_plan

sample_logs = [
    {
        "date": "2025-06-10",
        "workout": "Chest & Back",
        "sleep_hours": 6.5,
        "mood": "Energized",
    },
    {
        "date": "2025-06-11",
        "workout": "Cardio",
        "sleep_hours": 7,
        "mood": "Tired but motivated",
    },
]


async def main():
    # summary = await generate_summary_from_logs("user_123", sample_logs)
    # print("Generated Summary:\n", summary)
    plan = await generate_first_week_plan("user_123", sample_logs)
    print("\ Generated Training Plan:\n")
    print(plan)


if __name__ == "__main__":
    asyncio.run(main())
