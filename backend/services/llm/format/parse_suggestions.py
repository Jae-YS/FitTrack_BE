from datetime import date, timedelta
import re
from typing import List, Tuple
from backend.db.models import PlannedWorkout


DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def extract_plan_metadata(lines: List[str]) -> Tuple[str, str, str, float]:
    focus = ""
    goal = ""
    intensity = ""
    distance = None

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

    return focus, goal, intensity, distance


def parse_suggestions(
    plan_text: str, training_plan_id: int, base_date: date
) -> List[PlannedWorkout]:
    suggestions = []
    lines = plan_text.strip().splitlines()
    today_idx = base_date.weekday()

    focus, goal, intensity, _ = extract_plan_metadata(lines)

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

        dist_match = re.search(r"(\d+(?:\.\d+)?)\s*km", desc.lower())
        distance_per_workout = float(dist_match.group(1)) if dist_match else None

        pace_match = re.search(
            r"(\d{1,2}:\d{2}(?:-\d{1,2}:\d{2})?)\s*/?\s*km", desc.lower()
        )

        suggested = PlannedWorkout(
            training_plan_id=training_plan_id,
            recommended_date=recommended_date,
            workout_type=workout_type,
            description=desc,
            duration_minutes=None,
            distance_km=distance_per_workout,
            pace=pace_match.group(1) if pace_match else None,
        )

        suggestions.append(suggested)

    return suggestions
