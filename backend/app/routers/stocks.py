from fastapi import APIRouter, Query
from typing import Optional
import yfinance as yf

router = APIRouter()

@router.get("/stocks")
def filter_stocks(
    pe_lt: Optional[float] = Query(None),
    roe_gt: Optional[float] = Query(None)
):
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NFLX", "NVDA", "JPM", "BHP"]  # Sample tickers

    results = []

    for symbol in symbols:
        stock = yf.Ticker(symbol)
        info = stock.info

        try:
            pe_ratio = info.get("trailingPE")
            roe = info.get("returnOnEquity")

            if pe_ratio is None or roe is None:
                continue

            roe_percent = roe * 100

            if (pe_lt is None or pe_ratio < pe_lt) and (roe_gt is None or roe_percent > roe_gt):
                results.append({
                    "symbol": symbol,
                    "name": info.get("shortName"),
                    "pe_ratio": pe_ratio,
                    "roe": round(roe_percent, 2)
                })

        except Exception:
            continue

    return results
