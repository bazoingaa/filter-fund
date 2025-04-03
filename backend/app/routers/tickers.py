from fastapi import APIRouter
import pandas as pd
import os

router = APIRouter()

# Adjust if you're not in app/routers/
DATA_PATH = os.path.join(os.path.dirname(__file__), "../../data/all_common_stocks.csv")

@router.get("/tickers")
def get_all_tickers():
    try:
        df = pd.read_csv(DATA_PATH)
        tickers = df.to_dict(orient="records")
        return {"tickers": tickers}
    except Exception as e:
        return {"error": str(e)}
