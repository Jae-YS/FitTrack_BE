def weekly_summary_prompt(log_text: str) -> str:
    return f"""You're a virtual fitness coach. Here's a summary of a user's week:

{log_text}

Generate a concise, friendly weekly summary and one personalized suggestion for improvement.
"""
