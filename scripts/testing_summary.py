import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
)

import asyncio
from services.llm.summary_generator import generate_summary_from_logs

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
    summary = await generate_summary_from_logs("user_123", sample_logs)
    print("Generated Summary:\n", summary)


if __name__ == "__main__":
    asyncio.run(main())
