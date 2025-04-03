import os
import pandas as pd
import yfinance as yf
import json
from time import sleep

# Setup paths
csv_path = os.path.abspath(os.path.join("..", "backend", "data", "all_common_stocks.csv"))
output_folder = os.path.abspath(os.path.join("..", "backend", "data", "fundamentals"))

print(f"📂 Working from: {os.getcwd()}")
print(f"📄 CSV path: {csv_path}")
print(f"💾 Output folder: {output_folder}")

# Create output folder if missing
os.makedirs(output_folder, exist_ok=True)

# Load tickers
tickers = pd.read_csv(csv_path)["ticker"].dropna().unique().tolist()
print(f"✅ Loaded {len(tickers)} tickers")

# Start caching
for i, ticker in enumerate(tickers, 1):
    output_file = os.path.join(output_folder, f"{ticker}.json")

    if os.path.exists(output_file):
        continue  # Already cached

    print(f"⏳ Fetching: {ticker} ({i}/{len(tickers)})")

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Save to JSON
        with open(output_file, "w") as f:
            json.dump(info, f)

        print(f"✅ Saved: {ticker}")

        sleep(0.5)  # Be gentle with yfinance

    except Exception as e:
        print(f"❌ Error fetching {ticker}: {e}")
        continue
