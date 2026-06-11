import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def generate_ai_final_report(strategy_config, python_summary, evaluation_report):
    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("MODEL_NAME")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing in .env")

    if not model_name:
        raise ValueError("MODEL_NAME is missing in .env")

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are an AI backtesting risk analyst.

You must explain the verified Python deterministic backtest result.

Important rules:
- Use Python deterministic summary as the source of truth.
- Do not treat the LLM preliminary backtest as final.
- Do not give live trading advice.
- Do not say buy now or sell now.
- Do not guarantee profit.
- Do not claim the strategy will work in the future.
- Explain this as historical backtesting analysis only.
- Return ONLY valid JSON.

Strategy config:
{json.dumps(strategy_config, indent=2)}

Python deterministic summary:
{json.dumps(python_summary, indent=2)}

Evaluation report:
{json.dumps(evaluation_report, indent=2)}

Return JSON in this exact structure:
{{
  "strategy_summary": "...",
  "performance_observation": "...",
  "risk_level": "LOW / MEDIUM / HIGH",
  "main_risk": "...",
  "improvement_suggestions": [
    "...",
    "...",
    "..."
  ],
  "limitations": "...",
  "evaluation_observation": "...",
  "disclaimer": "Historical backtesting only. Not trading advice."
}}
"""

    response = client.responses.create(
        model=model_name,
        input=prompt
    )

    response_text = response.output_text.strip()

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        raise ValueError("AI final report was not valid JSON. Response was: " + response_text)