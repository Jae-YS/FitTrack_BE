from backend.services.llm.openai_client import client
from backend.prompts.summary import weekly_summary_prompt


async def generate_summary_from_logs(user_id: str, logs: list[dict]) -> str:
    if not logs:
        return "No activity data available."

    log_text = "\n".join(
        f"Date: {log['date']} | Workout: {log.get('workout')} | Sleep: {log.get('sleep_hours')}h | Mood: {log.get('mood')}"
        for log in logs
    )

    prompt = weekly_summary_prompt(log_text)

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300,
    )
    print(response)
    return response.choices[0].message.content.strip()
