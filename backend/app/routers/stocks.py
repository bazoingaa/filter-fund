from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter()

@router.get("/stocks")
def filter_stocks(
    pe_lt: Optional[float] = Query(None),
    roe_gt: Optional[float] = Query(None)
):
    return {
        "message": "Filters received",
        "pe_lt": pe_lt,
        "roe_gt": roe_gt
    }