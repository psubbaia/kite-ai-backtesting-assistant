import pandas as pd


def load_historical_data(file_path):
    df = pd.read_csv(file_path)

    # Convert Kite date column to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Remove timezone info if present
    # Kite data may contain +05:30 timezone
    if df["date"].dt.tz is not None:
        df["date"] = df["date"].dt.tz_localize(None)

    return df


def filter_data_by_date(df, from_date, to_date):
    from_date = pd.to_datetime(from_date)
    to_date = pd.to_datetime(to_date)

    filtered_df = df[
        (df["date"] >= from_date) &
        (df["date"] <= to_date)
    ]

    return filtered_df


def prepare_sample_for_llm(df, max_rows=10):
    sample_df = df.head(max_rows)

    records = []

    for _, row in sample_df.iterrows():
        records.append({
            "date": str(row["date"].date()),
            "open": float(row["open"]),
            "high": float(row["high"]),
            "low": float(row["low"]),
            "close": float(row["close"]),
            "volume": int(row["volume"]) if "volume" in row else 0
        })

    return records