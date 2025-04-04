'use client'

import React, { useState } from 'react'
import axios from 'axios'

type Stock = {
  symbol: string
  name: string
  pe_ratio: number | null
  roe: number | null
  market_cap: number | null
  dividend_yield: number | null
  beta: number | null
  sector: string
  country: string
  industry: string
}

export default function Home() {
  const [filters, setFilters] = useState({
    pe_min: '',
    pe_max: '',
    roe_min: '',
    roe_max: '',
    market_cap_min: '',
    market_cap_max: '',
    div_yield_min: '',
    div_yield_max: '',
    beta_min: '',
    beta_max: '',
    sector: '',
    country: '',
    industries: '' // comma-separated
  })

  const [results, setResults] = useState<Stock[]>([])
  const [offset, setOffset] = useState(0)
  const [hasMore, setHasMore] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFilters({ ...filters, [e.target.name]: e.target.value })
  }

  const buildParams = () => {
    const params: any = {}

    for (const key in filters) {
      const value = filters[key as keyof typeof filters]
      if (value.trim() !== '') {
        if (key === 'industries') {
          const industryList = value.split(',').map(ind => ind.trim())
          params['industries'] = industryList
        } else {
          params[key] = value
        }
      }
    }

    return params
  }

  const fetchStocks = async (newSearch = false) => {
    setLoading(true)
    const currentOffset = newSearch ? 0 : offset
    const params = { ...buildParams(), offset: currentOffset, limit: 20 }

    try {
      const res = await axios.get('http://localhost:8000/stocks', { params })
      const newData = res.data

      if (newSearch) {
        setResults(newData)
      } else {
        setResults(prev => [...prev, ...newData])
      }

      setOffset(currentOffset + 20)
      setHasMore(newData.length === 20)
    } catch (err: any) {
      console.error('Axios Error:', err)
      alert(`Error: ${err?.message || 'Something went wrong'}`)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = () => {
    setOffset(0)
    fetchStocks(true)
  }

  return (
    <main className="p-6 max-w-screen-lg mx-auto">
      <h1 className="text-2xl font-bold mb-6">Stock Screener</h1>

      <div className="grid grid-cols-2 gap-4 mb-4">
        {[
          ['pe_min', 'P/E Min'],
          ['pe_max', 'P/E Max'],
          ['roe_min', 'ROE Min (%)'],
          ['roe_max', 'ROE Max (%)'],
          ['market_cap_min', 'Market Cap Min'],
          ['market_cap_max', 'Market Cap Max'],
          ['div_yield_min', 'Dividend Yield Min (%)'],
          ['div_yield_max', 'Dividend Yield Max (%)'],
          ['beta_min', 'Beta Min'],
          ['beta_max', 'Beta Max']
        ].map(([key, label]) => (
          <input
            key={key}
            name={key}
            placeholder={label}
            value={filters[key as keyof typeof filters]}
            onChange={handleInput}
            type="number"
            className="border p-2 rounded"
          />
        ))}

        <input
          name="sector"
          placeholder="Sector (e.g. tech)"
          value={filters.sector}
          onChange={handleInput}
          className="border p-2 rounded"
        />
        <input
          name="country"
          placeholder="Country (e.g. usa)"
          value={filters.country}
          onChange={handleInput}
          className="border p-2 rounded"
        />
        <input
          name="industries"
          placeholder="Industries (comma separated)"
          value={filters.industries}
          onChange={handleInput}
          className="border p-2 rounded col-span-2"
        />
      </div>

      <button
        onClick={handleSearch}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        {loading ? 'Searching...' : 'Search'}
      </button>

      <div className="mt-6">
        {results.length > 0 && (
          <>
            <table className="w-full border mt-4 text-sm">
              <thead className="bg-gray-100">
                <tr>
                  <th className="p-2 border">Symbol</th>
                  <th className="p-2 border">Name</th>
                  <th className="p-2 border">P/E</th>
                  <th className="p-2 border">ROE</th>
                  <th className="p-2 border">Mkt Cap</th>
                  <th className="p-2 border">Div Yield</th>
                  <th className="p-2 border">Beta</th>
                  <th className="p-2 border">Sector</th>
                  <th className="p-2 border">Country</th>
                  <th className="p-2 border">Industry</th>
                </tr>
              </thead>
              <tbody>
                {results.map((stock, i) => (
                  <tr key={i} className="hover:bg-gray-50">
                    <td className="p-2 border">{stock.symbol}</td>
                    <td className="p-2 border">{stock.name}</td>
                    <td className="p-2 border">{stock.pe_ratio ?? '—'}</td>
                    <td className="p-2 border">{stock.roe ?? '—'}</td>
                    <td className="p-2 border">{stock.market_cap?.toLocaleString() ?? '—'}</td>
                    <td className="p-2 border">{stock.dividend_yield ?? '—'}</td>
                    <td className="p-2 border">{stock.beta ?? '—'}</td>
                    <td className="p-2 border">{stock.sector}</td>
                    <td className="p-2 border">{stock.country}</td>
                    <td className="p-2 border">{stock.industry}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            {hasMore && (
              <div className="mt-4 flex justify-center">
                <button
                  onClick={() => fetchStocks(false)}
                  className="bg-gray-700 text-white px-4 py-2 rounded hover:bg-gray-800"
                >
                  {loading ? 'Loading...' : 'Load More'}
                </button>
              </div>
            )}
          </>
        )}

        {results.length === 0 && !loading && (
          <p className="text-gray-500 mt-4">No results yet. Try adjusting your filters.</p>
        )}
      </div>
    </main>
  )
}
