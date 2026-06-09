import os
from dotenv import load_dotenv
from kiteconnect import KiteConnect

load_dotenv()

api_key = os.getenv("KITE_API_KEY")

kite = KiteConnect(api_key=api_key)

print("Open this URL in browser and login:")
print(kite.login_url())