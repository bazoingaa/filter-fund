# FilterFund - Scalable, Open Stock Screener

**FilterFund** is an advanced, open-source stock screener designed to help investors and analysts find fundamentally strong stocks using deep filters across 20,000+ global tickers.

This project uses a fast, modern stack:
- FastAPI backend with cached fundamentals via `yfinance`
- Next.js frontend with TypeScript and TailwindCSS
- Data-ingestion pipeline for updating financials in batches

---

## Features
- Filter by P/E ratio, ROE, market cap, beta, dividend yield, industry, sector, and more
- Multi-select with partial matching (e.g. type "prop" to match "Property")
- Supports thousands of tickers with smart API call batching and local caching
- Modular architecture (data ingestion, backend API, frontend UI)
- Ready for SQLite or JSON storage
- Built for scalability: targeting 50,000+ stocks over time

---

## Folder Structure
```
filter-fund/
├── backend/             # FastAPI app
│   └── app/
│       └── routers/     # Stocks API
│   └── data/            # Cached fundamentals
├── frontend/            # Next.js app (UI)
├── data-ingestion/      # Batch fetcher scripts
└── README.md            # You're here!
```

---

## Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/bazoingaa/filter-fund.git
cd filter-fund
```

### 2. Install Frontend
```bash
cd frontend
npm install
npm run dev
```

### 3. Install Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 4. Load Sample Data
```bash
cd data-ingestion
python3 fetch_data.py 0   # run in batches
python3 merge_batches.py  # combine into one JSON
```

---

## Credits
Built by [@bazoingaa](https://github.com/bazoingaa) to democratise access to fundamental stock screening.

Pull requests welcome.
