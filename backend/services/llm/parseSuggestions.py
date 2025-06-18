from datetime import timedelta, date
import re
from typing import List
from backend.models.sql_models import SuggestedWorkout

DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def parse_suggestions(
    plan_text: str, user_id: int, week: int, base_date: date
) -> List[SuggestedWorkout]:
    print(f"[DEBUG] Parsing suggestions for user_id={user_id}, week={week}")
    suggestions = []
    lines = plan_text.strip().splitlines()
    today_idx = base_date.weekday()

    focus = ""
    goal = ""
    intensity = ""
    distance = ""

    for line in lines:
        line_lower = line.lower().strip()
        if line_lower.startswith("focus:"):
            focus = line.split(":", 1)[-1].strip()
        elif line_lower.startswith("goal:"):
            goal = line.split(":", 1)[-1].strip()
        elif line_lower.startswith("intensity:"):
            intensity = line.split(":", 1)[-1].strip()
        elif line_lower.startswith("distance:"):
            distance_str = line.split(":", 1)[-1].strip()
            match = re.search(r"\d+(?:\.\d+)?", distance_str)
            distance = float(match.group()) if match else None

    print("[DEBUG] Parsed Plan Metadata:")
    print(f"  ↳ Focus: {focus}")
    print(f"  ↳ Goal: {goal}")
    print(f"  ↳ Intensity: {intensity}")
    print(f"  ↳ Distance: {distance}")
    print("-" * 40)

    for line in lines:
        if not line.strip() or ":" not in line or not line.startswith("- "):
            continue

        try:
            day_str, desc = line[2:].split(":", 1)
            day_str = day_str.strip().lower()
            desc = desc.strip()
        except ValueError:
            continue

        if day_str not in DAYS:
            continue

        day_idx = DAYS.index(day_str)
        if day_idx < today_idx:
            continue

        recommended_date = base_date + timedelta(days=(day_idx - today_idx))
        workout_type = desc.split(",")[0].strip().lower()
        pace_match = re.search(
            r"(\d{1,2}:\d{2}(?:-\d{1,2}:\d{2})?)\s*/?\s*km", desc.lower()
        )

        suggested = SuggestedWorkout(
            user_id=user_id,
            week=week,
            recommended_date=recommended_date,
            workout_type=workout_type,
            description=desc,
            duration_minutes=None,
            distance_km=distance,
            pace=pace_match.group(1) if pace_match else None,
            goal=goal,
            focus=focus,
            intensity=intensity,
        )

        suggestions.append(suggested)

    return suggestions
