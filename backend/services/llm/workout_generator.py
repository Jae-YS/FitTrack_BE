from backend.services.llm.openai_client import client
from backend.prompts.workout import runner_training_plan_prompt


async def generate_first_week_plan(
    race: str,
    level: str,
    today: str,
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

    prompt = runner_training_plan_prompt(
        race=race,
        initial_level=level,
        log_text=log_text,
        today=today,
    )

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
