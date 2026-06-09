import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from kiteconnect import KiteConnect

load_dotenv()

api_key = os.getenv("KITE_API_KEY")
access_token = os.getenv("KITE_ACCESS_TOKEN")

kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

instrument_token = 256265  # Example: replace with your instrument token

from_date = "2024-01-01"
to_date = "2026-06-09"
interval = "day"

data = kite.historical_data(
    instrument_token=instrument_token,
    from_date=from_date,
    to_date=to_date,
    interval=interval
)

df = pd.DataFrame(data)

print(df.head())

file_name = "historical_data.csv"
df.to_csv(file_name, index=False)

print("Historical data saved to:", file_name)