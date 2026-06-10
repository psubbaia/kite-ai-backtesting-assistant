import os
import json
from datetime import datetime
import pandas as pd


def ensure_results_folder():
    os.makedirs("results", exist_ok=True)


def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_trade_report(trades, file_path=None):
    ensure_results_folder()

    if file_path is None:
        file_path = f"results/trade_report_{get_timestamp()}.csv"

    df = pd.DataFrame(trades)
    df.to_csv(file_path, index=False)

    return file_path


def save_json_report(data, file_path=None, report_name="report"):
    ensure_results_folder()

    if file_path is None:
        file_path = f"results/{report_name}_{get_timestamp()}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return file_path