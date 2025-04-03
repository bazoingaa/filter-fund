from fastapi import APIRouter, Query
from typing import Optional, List
import json
import os

router = APIRouter()
FUNDAMENTALS_DIR = os.path.join(os.path.dirname(__file__), "../../data/fundamentals")

def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

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
    if not os.path.exists(FUNDAMENTALS_DIR):
        return {"error": "Fundamentals directory not found."}

    results = []

    for file in os.listdir(FUNDAMENTALS_DIR):
        if not file.endswith(".json"):
            continue

        with open(os.path.join(FUNDAMENTALS_DIR, file), "r") as f:
            try:
                stock = json.load(f)
            except:
                continue

        pe = to_float(stock.get("trailingPE"))
        roe = to_float(stock.get("returnOnEquity"))
        market_cap = to_float(stock.get("marketCap"))
        div_yield = to_float(stock.get("dividendYield"))
        beta = to_float(stock.get("beta"))
        stock_sector = (stock.get("sector") or "").lower()
        stock_country = (stock.get("country") or "").lower()
        stock_industry = (stock.get("industry") or "").lower()

        if pe is not None:
            if pe_min is not None and pe < pe_min:
                continue
            if pe_max is not None and pe > pe_max:
                continue

        if roe is not None:
            if roe_min is not None and roe < roe_min:
                continue
            if roe_max is not None and roe > roe_max:
                continue

        if market_cap is not None:
            if market_cap_min is not None and market_cap < market_cap_min:
                continue
            if market_cap_max is not None and market_cap > market_cap_max:
                continue

        if div_yield is not None:
            if div_yield_min is not None and div_yield < div_yield_min:
                continue
            if div_yield_max is not None and div_yield > div_yield_max:
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
            "ticker": stock.get("symbol"),
            "name": stock.get("shortName"),
            "sector": stock.get("sector"),
            "industry": stock.get("industry"),
            "marketCap": market_cap,
            "pe_ratio": pe,
            "roe": roe,
            "dividendYield": div_yield,
            "beta": beta,
            "country": stock.get("country")
        })

    return results
