from collections import defaultdict
from datetime import timedelta


def format_workout_history(workouts):
    weeks = defaultdict(list)

    for workout in workouts:
        week_start = workout.log_date - timedelta(days=workout.log_date.weekday() + 1)
        weeks[week_start].append(workout)

    sorted_weeks = sorted(weeks.items(), reverse=True)[:3]

    summary_lines = []

    for i, (week_start, weekly_workouts) in enumerate(reversed(sorted_weeks), 1):
        day_summary = []
        for w in sorted(weekly_workouts, key=lambda x: x.log_date):
            if w.distance_km:
                pace = (
                    f" ({round(w.pace_min_per_km, 1)} min/km)"
                    if w.pace_min_per_km
                    else ""
                )
                entry = f"{int(w.distance_km)}km {w.type}{pace}"
            elif w.duration_minutes:
                entry = f"{w.duration_minutes} min {w.type}"
            else:
                entry = w.type

            day_summary.append(entry)

        summary_line = f"Week {i}: " + ", ".join(day_summary)
        summary_lines.append(summary_line)

    return "\n".join(summary_lines)
