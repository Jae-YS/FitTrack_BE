from backend.services.llm.openai_client import client
from backend.prompts.workout import runner_training_plan_prompt


async def generate_first_week_plan(user_id: str, logs: list[dict]) -> str:
    if not logs:
        return "No activity data available."

    prompt = runner_training_plan_prompt(
        race="Half Marathon",
        initial_level="Intermediate",
        log_text="""
        5K 26:45 (April 2025)
        10K 55:30 (June 202)
        Half Marathon 2:05:12 (October 2025)
        Full Marathon N/A
        """,
        today="2025-06-17",
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
    print(response)
    return response.choices[0].message.content.strip()
