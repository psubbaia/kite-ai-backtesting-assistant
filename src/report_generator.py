import os
import json
import pandas as pd


def ensure_results_folder():
    os.makedirs("results", exist_ok=True)


def save_trade_report(trades, file_path="results/trade_report.csv"):
    ensure_results_folder()

    df = pd.DataFrame(trades)
    df.to_csv(file_path, index=False)

    return file_path


def save_json_report(data, file_path):
    ensure_results_folder()

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return file_path