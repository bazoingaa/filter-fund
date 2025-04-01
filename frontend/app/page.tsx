'use client'

import React, { useState } from 'react'
import axios from 'axios'

type FilterParams = {
  pe_lt: string
  roe_gt: string
}

export default function Home() {
  const [results, setResults] = useState<any[]>([])
  const [filters, setFilters] = useState<FilterParams>({ pe_lt: '', roe_gt: '' })

  const fetchStocks = async () => {
    try {
      const params: any = {}
      if (filters.pe_lt.trim() !== '') params.pe_lt = parseFloat(filters.pe_lt)
      if (filters.roe_gt.trim() !== '') params.roe_gt = parseFloat(filters.roe_gt)
      const res = await axios.get(`http://localhost:8000/stocks`, { params })
      setResults([res.data])
    } catch (error) {
      console.error('Failed to fetch stocks:', error)
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">Stock Screener</h1>
      <div className="flex gap-4 mb-4">
        <input
          type="number"
          placeholder="P/E <"
          value={filters.pe_lt}
          onChange={e => setFilters({ ...filters, pe_lt: e.target.value })}
          className="border p-2"
        />
        <input
          type="number"
          placeholder="ROE >"
          value={filters.roe_gt}
          onChange={e => setFilters({ ...filters, roe_gt: e.target.value })}
          className="border p-2"
        />
        <button
          onClick={fetchStocks}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Search
        </button>
      </div>
      <ul>
        {results.map((res, idx) => (
          <li key={idx}>{JSON.stringify(res)}</li>
        ))}
      </ul>
    </div>
  )
}