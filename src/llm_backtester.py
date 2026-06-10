import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def run_llm_preliminary_backtest(strategy_config, historical_sample):
    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("MODEL_NAME")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing in .env")

    if not model_name:
        raise ValueError("MODEL_NAME is missing in .env")

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are a backtesting calculation assistant.

You must perform a preliminary backtest using ONLY the historical data rows provided.

Important:
- This is a preliminary LLM backtest.
- Use only the provided rows.
- Do not assume missing data.
- Do not give live trading advice.
- Do not say buy now or sell now.
- Do not guarantee profit.
- Return ONLY valid JSON.

Strategy config:
{json.dumps(strategy_config, indent=2)}

Historical data rows:
{json.dumps(historical_sample, indent=2)}

Supported strategy logic:

1. buy_open_sell_close:
For each row:
entry_price = open
exit_price = close
pnl = (exit_price - entry_price) * quantity

Return JSON in this format:
{{
  "calculation_type": "AI_PRELIMINARY_BACKTEST",
  "strategy_type": "...",
  "rows_used": 0,
  "total_trades": 0,
  "profit_trades": 0,
  "loss_trades": 0,
  "win_rate": 0,
  "total_pnl": 0,
  "average_pnl": 0,
  "best_trade": 0,
  "worst_trade": 0,
  "notes": "Preliminary LLM calculation only. Not final verified result."
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
        raise ValueError("LLM did not return valid JSON. Response was: " + response_text)