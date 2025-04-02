from fastapi import APIRouter, Query
from typing import Optional, List
import yfinance as yf

router = APIRouter()

@router.get("/stocks")
def filter_stocks(
    pe_min: Optional[float] = Query(None),
    pe_max: Optional[float] = Query(None),
    roe_min: Optional[float] = Query(None),
    roe_max: Optional[float] = Query(None),
    market_cap_min: Optional[float] = Query(None),
    market_cap_max: Optional[float] = Query(None),
    div_yield_min: Optional[float] = Query(None),
    div_yield_max: Optional[float] = Query(None),
    beta_min: Optional[float] = Query(None),
    beta_max: Optional[float] = Query(None),
    sector: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    industries: Optional[List[str]] = Query(None)
):
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NFLX", "NVDA", "JPM", "BHP"]
    results = []

    for symbol in symbols:
        stock = yf.Ticker(symbol)
        info = stock.info

        try:
            pe_ratio = info.get("trailingPE")
            roe = info.get("returnOnEquity")
            market_cap = info.get("marketCap")
            div_yield = info.get("dividendYield")
            beta = info.get("beta")
            stock_sector = info.get("sector", "").lower()
            stock_country = info.get("country", "").lower()
            stock_industry = info.get("industry", "").lower()

            if pe_ratio is not None:
                if pe_min is not None and pe_ratio < pe_min:
                    continue
                if pe_max is not None and pe_ratio > pe_max:
                    continue

            if roe is not None:
                roe_percent = roe * 100
                if roe_min is not None and roe_percent < roe_min:
                    continue
                if roe_max is not None and roe_percent > roe_max:
                    continue

            if market_cap is not None:
                if market_cap_min is not None and market_cap < market_cap_min:
                    continue
                if market_cap_max is not None and market_cap > market_cap_max:
                    continue

            if div_yield is not None:
                dy_percent = div_yield * 100
                if div_yield_min is not None and dy_percent < div_yield_min:
                    continue
                if div_yield_max is not None and dy_percent > div_yield_max:
                    continue

            if beta is not None:
                if beta_min is not None and beta < beta_min:
                    continue
                if beta_max is not None and beta > beta_max:
                    continue

            if sector and sector.lower() not in stock_sector:
                continue

            if country and country.lower() not in stock_country:
                continue

            if industries:
                if not any(ind.lower() in stock_industry for ind in industries):
                    continue

            results.append({
                "symbol": symbol,
                "name": info.get("shortName"),
                "pe_ratio": pe_ratio,
                "roe": round(roe_percent, 2) if roe is not None else None,
                "market_cap": market_cap,
                "dividend_yield": round(dy_percent, 2) if div_yield is not None else None,
                "beta": beta,
                "sector": info.get("sector"),
                "country": info.get("country"),
                "industry": info.get("industry")
            })

        except Exception:
            continue

    return results
