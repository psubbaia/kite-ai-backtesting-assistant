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

You must perform a preliminary backtest calculation using only the provided historical rows.

Important rules:
- Return ONLY valid JSON.
- Do not include markdown.
- Do not include explanation outside JSON.
- Use the exact same field names as the Python deterministic backtest summary.
- If a value cannot be calculated, use 0 or an empty string.
- Do not give trading advice.
- Do not say buy now or sell now.
- Do not guarantee profit.

Strategy configuration:
{json.dumps(strategy_config, indent=2)}

Historical sample rows:
{json.dumps(historical_sample, indent=2)}

For strategy_type = "buy_open_sell_close":
- entry_price = open
- exit_price = close
- pnl = (close - open) * quantity
- result = "PROFIT" if pnl > 0 else "LOSS" if pnl < 0 else "BREAKEVEN"

Return JSON in this exact structure:

{{
  "strategy_type": "{strategy_config.get("strategy_type", "")}",
  "symbol": "{strategy_config.get("symbol", "")}",
  "from_date": "{strategy_config.get("from_date", "")}",
  "to_date": "{strategy_config.get("to_date", "")}",
  "quantity": {strategy_config.get("quantity", 0)},
  "total_trades": 0,
  "profit_trades": 0,
  "loss_trades": 0,
  "win_rate": 0,
  "total_pnl": 0,
  "average_pnl": 0,
  "best_trade": 0,
  "worst_trade": 0,
  "data_source": "LLM preliminary calculation on sample rows",
  "calculation_type": "LLM_PRELIMINARY"
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
        raise ValueError(
            "LLM preliminary backtest did not return valid JSON. Response was: "
            + response_text
        )