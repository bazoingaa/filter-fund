from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import stocks, tickers

app = FastAPI()

# ✅ This enables frontend on port 3000 to talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or use ["*"] temporarily
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stocks.router)
app.include_router(tickers.router)