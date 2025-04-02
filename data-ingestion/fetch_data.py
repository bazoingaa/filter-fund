import yfinance as yf
import json
import time
import os
import csv
import sys

print("🚀 Running fetch_data.py")

# === CONFIG ===
BATCH_SIZE = 500
OFFSET = 0
if len(sys.argv) > 1:
    try:
        OFFSET = int(sys.argv[1])
    except ValueError:
        print("Invalid offset provided. Using 0.")

# === Load tickers from CSV ===
ticker_file = "../data-ingestion/tickers_5000.csv"
with open(ticker_file, "r") as f:
    reader = csv.reader(f)
    tickers = [row[0].strip() for row in reader if row]

# Slice based on offset
tickers = tickers[OFFSET:OFFSET + BATCH_SIZE]

results = []
output_dir = "../backend/data"
os.makedirs(output_dir, exist_ok=True)

print(f"📈 Fetching {len(tickers)} tickers (offset {OFFSET})\n")

for i, symbol in enumerate(tickers):
    print(f"[{i + 1}/{len(tickers)}] Fetching {symbol}")
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        results.append({
            "symbol": symbol,
            "name": info.get("shortName"),
            "pe_ratio": info.get("trailingPE"),
            "roe": info.get("returnOnEquity") * 100 if info.get("returnOnEquity") is not None else None,
            "market_cap": info.get("marketCap"),
            "dividend_yield": info.get("dividendYield") * 100 if info.get("dividendYield") is not None else None,
            "beta": info.get("beta"),
            "sector": info.get("sector"),
            "country": info.get("country"),
            "industry": info.get("industry")
        })

        time.sleep(1.0)  # avoid rate-limiting

    except Exception as e:
        print(f"⚠️  Failed to fetch {symbol}: {e}")

# Save partial output
output_path = f"{output_dir}/stock_cache_batch_{OFFSET}.json"
with open(output_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"\n✅ Done. Saved batch to {output_path}")
