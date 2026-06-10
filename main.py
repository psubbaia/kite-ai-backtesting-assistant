from src.prompt_parser import parse_strategy_prompt
from src.config_validator import validate_strategy_config


def main():
    print("StrategyLab MVP — AI-Guided NIFTY Backtester")
    print("============================================")
    print("Supported strategies:")
    print("1. buy_open_sell_close")
    print("2. moving_average_crossover")
    print("3. breakout")
    print()

    user_prompt = input("Enter your strategy: ")

    print("\nParsing strategy with AI...")
    strategy_config = parse_strategy_prompt(user_prompt)

    print("\nAI Parsed Strategy Config")
    print("=========================")
    print(strategy_config)

    print("\nValidating strategy config...")
    validation_result = validate_strategy_config(strategy_config)

    if not validation_result["is_valid"]:
        print("\nValidation Failed")
        print("=================")
        print(validation_result)
        return

    print("\nValidation Passed")
    print("=================")
    print(validation_result["config"])


if __name__ == "__main__":
    main()