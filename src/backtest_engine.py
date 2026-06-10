from src.strategies import buy_open_sell_close
from src.strategies import moving_average_crossover
from src.strategies import breakout


def calculate_summary(trades, strategy_config):
    total_trades = len(trades)

    profit_trades = 0
    loss_trades = 0
    total_pnl = 0

    pnl_values = []

    for trade in trades:
        pnl = trade["pnl"]
        pnl_values.append(pnl)
        total_pnl = total_pnl + pnl

        if pnl > 0:
            profit_trades = profit_trades + 1
        elif pnl < 0:
            loss_trades = loss_trades + 1

    if total_trades > 0:
        win_rate = (profit_trades / total_trades) * 100
        average_pnl = total_pnl / total_trades
        best_trade = max(pnl_values)
        worst_trade = min(pnl_values)
    else:
        win_rate = 0
        average_pnl = 0
        best_trade = 0
        worst_trade = 0

    summary = {
        "calculation_type": "PYTHON_DETERMINISTIC_BACKTEST",
        "strategy_type": strategy_config["strategy_type"],
        "symbol": strategy_config["symbol"],
        "from_date": strategy_config["from_date"],
        "to_date": strategy_config["to_date"],
        "quantity": strategy_config["quantity"],
        "total_trades": total_trades,
        "profit_trades": profit_trades,
        "loss_trades": loss_trades,
        "win_rate": round(win_rate, 2),
        "total_pnl": round(total_pnl, 2),
        "average_pnl": round(average_pnl, 2),
        "best_trade": round(best_trade, 2),
        "worst_trade": round(worst_trade, 2),
        "data_source": "Kite Connect historical data"
    }

    return summary


def run_python_backtest(strategy_config, df):
    strategy_type = strategy_config["strategy_type"]
    quantity = strategy_config["quantity"]

    if strategy_type == "buy_open_sell_close":
        trades = buy_open_sell_close(df, quantity)

    elif strategy_type == "moving_average_crossover":
        trades = moving_average_crossover(df, quantity)

    elif strategy_type == "breakout":
        trades = breakout(df, quantity)

    else:
        raise ValueError("Unsupported strategy type: " + strategy_type)

    summary = calculate_summary(trades, strategy_config)

    return trades, summary