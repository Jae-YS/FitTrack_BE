from datetime import datetime
from backend.services.llm.parseSuggestions import parse_suggestions

sample_plan = """
Focus: This week emphasizes building endurance with a mix of easy runs and a long run. Incorporating cross-training will aid recovery.

Weekly Plan:
- Monday: Easy run, 8 km at a comfortable pace (6:00-6:30/km) - recovery.
- Tuesday: Cross-training, 45 min cycling or swimming - low impact.
- Wednesday: Tempo run, 6 km with 3 km at 5:00/km pace - speed development.
- Thursday: Rest day - recovery.
- Friday: Easy run, 10 km at a relaxed pace (6:00-6:30/km) - endurance.
- Saturday: Long run, 12 km at a steady pace (6:30/km) - endurance building.
- Sunday: Yoga session, 30 min - flexibility and relaxation.

Intensity: Moderate  
Distance: 36 km  
Goal: Build endurance with varied paces, targeting 36 km this week.
"""

today = datetime(2025, 6, 17).date()
week = today.isocalendar().week
user_id = 1

suggestions = parse_suggestions(
    sample_plan, user_id=user_id, week=week, base_date=today
)
