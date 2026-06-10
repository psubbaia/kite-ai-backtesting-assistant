import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def parse_strategy_prompt(user_prompt):
    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("MODEL_NAME")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing in .env")

    if not model_name:
        raise ValueError("MODEL_NAME is missing in .env")

    client = OpenAI(api_key=api_key)

    system_prompt = """
You are a strategy parser for a NIFTY backtesting application.

Your job is to convert the user's natural language strategy into strict JSON.

Allowed strategy_type values:
1. buy_open_sell_close
2. moving_average_crossover
3. breakout

Return ONLY valid JSON. Do not include explanation.

Required JSON format:
{
  "symbol": "NIFTY",
  "strategy_type": "buy_open_sell_close",
  "from_date": "YYYY-MM-DD",
  "to_date": "YYYY-MM-DD",
  "quantity": 50,
  "timeframe": "day"
}

Rules:
- If the user says "2024", use from_date "2024-01-01" and to_date "2024-12-31".
- If quantity is missing, use 50.
- If timeframe is missing, use "day".
- If symbol is missing, use "NIFTY".
- If strategy is unsupported, set strategy_type to "unsupported".
"""

    response = client.responses.create(
        model=model_name,
        input=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    response_text = response.output_text.strip()

    try:
        strategy_config = json.loads(response_text)
        return strategy_config
    except json.JSONDecodeError:
        raise ValueError("AI did not return valid JSON. Response was: " + response_text)