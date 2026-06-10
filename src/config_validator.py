ALLOWED_STRATEGIES = [
    "buy_open_sell_close",
    "moving_average_crossover",
    "breakout"
]


def validate_strategy_config(config):
    required_fields = [
        "symbol",
        "strategy_type",
        "from_date",
        "to_date",
        "quantity",
        "timeframe"
    ]

    missing_fields = []

    for field in required_fields:
        if field not in config or config[field] in [None, ""]:
            missing_fields.append(field)

    if len(missing_fields) > 0:
        return {
            "is_valid": False,
            "message": "Missing required fields",
            "missing_fields": missing_fields
        }

    if config["strategy_type"] not in ALLOWED_STRATEGIES:
        return {
            "is_valid": False,
            "message": "Unsupported strategy for MVP",
            "supported_strategies": ALLOWED_STRATEGIES
        }

    if config["symbol"] != "NIFTY":
        return {
            "is_valid": False,
            "message": "Only NIFTY is supported in MVP"
        }

    if config["timeframe"] != "day":
        return {
            "is_valid": False,
            "message": "Only day timeframe is supported in MVP"
        }

    try:
        config["quantity"] = int(config["quantity"])
    except ValueError:
        return {
            "is_valid": False,
            "message": "Quantity must be a number"
        }

    return {
        "is_valid": True,
        "message": "Strategy config is valid",
        "config": config
    }