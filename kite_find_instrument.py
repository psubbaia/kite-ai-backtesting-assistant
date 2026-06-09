import os
from dotenv import load_dotenv
from kiteconnect import KiteConnect

load_dotenv()

api_key = os.getenv("KITE_API_KEY")
access_token = os.getenv("KITE_ACCESS_TOKEN")

kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

instruments = kite.instruments("NSE")

search_symbol = "NIFTY 50"

for instrument in instruments:
    if instrument["tradingsymbol"] == search_symbol:
        print(instrument)