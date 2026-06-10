def buy_open_sell_close(df, quantity):
    trades = []

    for _, row in df.iterrows():
        entry_price = float(row["open"])
        exit_price = float(row["close"])
        pnl = (exit_price - entry_price) * quantity

        if pnl > 0:
            result = "PROFIT"
        elif pnl < 0:
            result = "LOSS"
        else:
            result = "BREAKEVEN"

        trade = {
            "date": str(row["date"].date()),
            "strategy": "buy_open_sell_close",
            "entry_price": entry_price,
            "exit_price": exit_price,
            "quantity": quantity,
            "pnl": round(pnl, 2),
            "result": result
        }

        trades.append(trade)

    return trades


def moving_average_crossover(df, quantity):
    df = df.copy()

    df["sma_20"] = df["close"].rolling(window=20).mean()
    df["sma_50"] = df["close"].rolling(window=50).mean()

    trades = []
    in_position = False
    entry_price = None
    entry_date = None

    for _, row in df.iterrows():
        if row["sma_20"] != row["sma_20"] or row["sma_50"] != row["sma_50"]:
            continue

        if not in_position and row["sma_20"] > row["sma_50"]:
            in_position = True
            entry_price = float(row["close"])
            entry_date = row["date"]

        elif in_position and row["sma_20"] < row["sma_50"]:
            exit_price = float(row["close"])
            pnl = (exit_price - entry_price) * quantity

            trade = {
                "date": str(row["date"].date()),
                "strategy": "moving_average_crossover",
                "entry_date": str(entry_date.date()),
                "entry_price": round(entry_price, 2),
                "exit_price": round(exit_price, 2),
                "quantity": quantity,
                "pnl": round(pnl, 2),
                "result": "PROFIT" if pnl > 0 else "LOSS"
            }

            trades.append(trade)
            in_position = False

    return trades


def breakout(df, quantity):
    df = df.copy()
    df["previous_high"] = df["high"].shift(1)

    trades = []

    for index in range(1, len(df) - 1):
        current_row = df.iloc[index]
        next_row = df.iloc[index + 1]

        if current_row["close"] > current_row["previous_high"]:
            entry_price = float(current_row["close"])
            exit_price = float(next_row["close"])
            pnl = (exit_price - entry_price) * quantity

            trade = {
                "date": str(current_row["date"].date()),
                "strategy": "breakout",
                "entry_price": round(entry_price, 2),
                "exit_price": round(exit_price, 2),
                "quantity": quantity,
                "pnl": round(pnl, 2),
                "result": "PROFIT" if pnl > 0 else "LOSS"
            }

            trades.append(trade)

    return trades