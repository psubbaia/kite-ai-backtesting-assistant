from src.prompt_parser import parse_strategy_prompt
from src.config_validator import validate_strategy_config
from src.data_loader import load_historical_data
from src.data_loader import filter_data_by_date
from src.data_loader import prepare_sample_for_llm
from src.llm_backtester import run_llm_preliminary_backtest
from src.backtest_engine import run_python_backtest


def main():
    print("StrategyLab MVP — AI-Guided NIFTY Backtester")
    print("============================================")
    print("Supported strategies:")
    print("1. buy_open_sell_close")
    print("2. moving_average_crossover")
    print("3. breakout")
    print()

    user_prompt = input("Enter your strategy: ")

    print("\nStep 1: Parsing strategy with AI...")
    strategy_config = parse_strategy_prompt(user_prompt)

    print("\nAI Parsed Strategy Config")
    print("=========================")
    print(strategy_config)

    print("\nStep 2: Validating strategy config...")
    validation_result = validate_strategy_config(strategy_config)

    if not validation_result["is_valid"]:
        print("\nValidation Failed")
        print("=================")
        print(validation_result)
        return

    strategy_config = validation_result["config"]

    print("\nValidation Passed")
    print("=================")
    print(strategy_config)

    print("\nStep 3: Loading historical data...")
    df = load_historical_data("data/nifty_day.csv")

    filtered_df = filter_data_by_date(
        df,
        strategy_config["from_date"],
        strategy_config["to_date"]
    )

    print("Rows loaded for selected period:", len(filtered_df))
    print(
        "Selected period:",
        strategy_config["from_date"],
        "to",
        strategy_config["to_date"]
    )
    print("For Day 2 test, only first 10 rows will be used for both LLM and Python.")

    if len(filtered_df) == 0:
        print("No historical data found for selected date range.")
        return

    print("\nStep 4: Preparing same 10 rows for LLM and Python...")
    sample_df = filtered_df.head(10)

    historical_sample = prepare_sample_for_llm(sample_df, max_rows=10)

    print("Rows used for LLM backtest:", len(historical_sample))
    print("Rows used for Python backtest:", len(sample_df))

    print("\nStep 5: Running LLM preliminary backtest on 10 rows...")
    ai_preliminary_result = run_llm_preliminary_backtest(
        strategy_config,
        historical_sample
    )

    print("\nLLM Preliminary Backtest Result")
    print("===============================")
    print(ai_preliminary_result)

    print("\nStep 6: Running Python deterministic backtest on same 10 rows...")
    trades, python_summary = run_python_backtest(strategy_config, sample_df)

    print("\nPython Deterministic Backtest Summary")
    print("=====================================")
    print(python_summary)

    print("\nDay 2 run completed.")
    print("LLM and Python both used the same 10 rows.")
    print("Python result is the deterministic reference result for these 10 rows.")


if __name__ == "__main__":
    main()