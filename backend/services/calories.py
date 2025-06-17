MET_VALUES = {
    "running": 9.8,
    "walking": 4.3,
    "lifting": 6.0,
    "yoga": 2.5,
    "cycling": 7.5,
    "tempo": 10.0,
    "easy": 7.0,
    "long": 8.5,
    "recovery": 4.5,
    "cross-training": 4.0,
    "strength": 6.0,
}


def calculate_calories(workout_type: str, duration_min: int, weight_kg: float) -> float:
    met = MET_VALUES.get(workout_type.lower(), 5.0)
    return met * weight_kg * (duration_min / 60)
