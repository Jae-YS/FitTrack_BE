from backend.services.llm.format.format_history import format_workout_history
from backend.services.llm.openai_client import client
from backend.prompts.workout import (
    recurring_training_plan_prompt,
    runner_training_plan_prompt,
)


async def generate_first_week_plan(
    race_type: str,
    race_day: str,
    level: str,
    today_str: str,
    today_day: str,
    pr_5k: float | None,
    pr_10k: float | None,
    pr_half: float | None,
    pr_full: float | None,
) -> str:
    pr_lines = []
    if pr_5k:
        pr_lines.append(f"5K - {pr_5k} min")
    if pr_10k:
        pr_lines.append(f"10K - {pr_10k} min")
    if pr_half:
        pr_lines.append(f"Half Marathon - {pr_half} min")
    if pr_full:
        pr_lines.append(f"Full Marathon - {pr_full} min")

    log_text = "\n".join(pr_lines) if pr_lines else "No personal records provided."

    print(log_text)

    print(today_day, today_str)

    prompt = runner_training_plan_prompt(
        race_type=race_type,
        race_day=race_day,
        initial_level=level,
        records=log_text,
        today_str=today_str,
        today_day=today_day,
    )

    print(prompt)

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=300,
        top_p=0.9,
        frequency_penalty=0.2,
        presence_penalty=0.0,
    )

    return response.choices[0].message.content.strip()


async def generate_next_week_plan(
    race_type: str,
    race_day: str,
    level: str,
    week_number: int,
    recent_workouts: list,
) -> str:

    previous_plan = format_workout_history(recent_workouts)

    prompt = recurring_training_plan_prompt(
        initial_level=level,
        week_number=str(week_number),
        race_type=race_type,
        race_day=race_day,
        previous_plan=previous_plan,
    )

    print(prompt)

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_tokens=300,
        top_p=0.9,
        frequency_penalty=0.2,
        presence_penalty=0.0,
    )

    return response.choices[0].message.content.strip()
