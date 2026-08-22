// Meal history page - shows all past meals for the logged-in user,
// with optional date filtering. Reuses the GET /meals and
// DELETE /meals/{id} endpoints built earlier.

import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import apiClient from '../api/client'

interface DetectedFood {
  id: number
  food_name: string
  confidence: number
  calories: number | null
  protein: number | null
  carbs: number | null
  fat: number | null
}

interface Meal {
  id: number
  image_path: string
  created_at: string
  detected_foods: DetectedFood[]
}

export default function History() {
  const [meals, setMeals] = useState<Meal[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [deletingId, setDeletingId] = useState<number | null>(null)

  async function fetchMeals() {
    setIsLoading(true)
    const params: Record<string, string> = {}
    if (startDate) params.start_date = startDate
    if (endDate) params.end_date = endDate

    try {
      const response = await apiClient.get<Meal[]>('/meals', { params })
      setMeals(response.data)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchMeals()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  async function handleDelete(mealId: number) {
    setDeletingId(mealId)
    try {
      await apiClient.delete(`/meals/${mealId}`)
      setMeals((prev) => prev.filter((m) => m.id !== mealId))
    } finally {
      setDeletingId(null)
    }
  }

  function handleFilter(e: React.FormEvent) {
    e.preventDefault()
    fetchMeals()
  }

  function clearFilter() {
    setStartDate('')
    setEndDate('')
    // fetchMeals uses current state, so fetch after clearing via a microtask
    setTimeout(fetchMeals, 0)
  }

  return (
    <div className="min-h-screen bg-[#0a0f0d] text-white">
      {/* Top bar */}
      <div className="flex justify-between items-center px-8 py-5 border-b border-white/5">
        <Link to="/dashboard" className="flex items-center gap-2">
          <span className="w-7 h-7 rounded-full bg-gradient-to-br from-emerald-400 to-teal-500 flex items-center justify-center text-xs font-bold text-black">
            N
          </span>
          <span className="font-semibold">NutriVision AI</span>
        </Link>
        <div className="flex items-center gap-4">
          <Link to="/upload" className="bg-emerald-400 hover:bg-emerald-300 text-black text-sm font-semibold px-4 py-2 rounded-full transition">
            + Log meal
          </Link>
          <Link to="/dashboard" className="text-sm text-gray-400 hover:text-white transition">
            Dashboard
          </Link>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-8 py-10">
        <h1 className="text-3xl font-bold mb-6">Meal history</h1>

        {/* Filter bar */}
        <form onSubmit={handleFilter} className="flex flex-wrap items-end gap-3 mb-8 bg-[#0f1613] border border-white/5 rounded-2xl p-4">
          <div>
            <label className="block text-xs text-gray-500 mb-1">From</label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="bg-[#0a0f0d] border border-white/10 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:border-emerald-400"
            />
          </div>
          <div>
            <label className="block text-xs text-gray-500 mb-1">To</label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="bg-[#0a0f0d] border border-white/10 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:border-emerald-400"
            />
          </div>
          <button
            type="submit"
            className="bg-emerald-400 hover:bg-emerald-300 text-black text-sm font-semibold px-4 py-1.5 rounded-lg transition"
          >
            Filter
          </button>
          {(startDate || endDate) && (
            <button
              type="button"
              onClick={clearFilter}
              className="text-sm text-gray-500 hover:text-white transition px-2 py-1.5"
            >
              Clear
            </button>
          )}
        </form>

        {/* Meal list */}
        {isLoading ? (
          <p className="text-gray-500 text-sm">Loading…</p>
        ) : meals.length === 0 ? (
          <div className="text-center py-16 bg-[#0f1613] border border-white/5 rounded-2xl">
            <p className="text-gray-500 mb-4">No meals found for this range.</p>
            <Link
              to="/upload"
              className="inline-block bg-emerald-400 hover:bg-emerald-300 text-black font-semibold px-5 py-2 rounded-full transition text-sm"
            >
              Log your first meal
            </Link>
          </div>
        ) : (
          <div className="space-y-3">
            {meals.map((meal) => {
              const totalCal = meal.detected_foods.reduce((sum, f) => sum + (f.calories || 0), 0)
              const foodNames = meal.detected_foods.map((f) => f.food_name).join(', ') || 'Unidentified food'

              return (
                <div
                  key={meal.id}
                  className="flex items-center gap-4 bg-[#0f1613] border border-white/5 rounded-2xl p-4"
                >
                  <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-emerald-400/20 to-teal-500/20 flex items-center justify-center text-2xl flex-shrink-0">
                    🍽️
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-medium capitalize truncate">{foodNames}</p>
                    <p className="text-xs text-gray-500">
                      {new Date(meal.created_at).toLocaleString(undefined, {
                        month: 'short',
                        day: 'numeric',
                        year: 'numeric',
                        hour: 'numeric',
                        minute: '2-digit',
                      })}
                    </p>
                  </div>
                  <p className="text-emerald-400 font-medium text-sm flex-shrink-0">
                    {Math.round(totalCal)} kcal
                  </p>
                  <button
                    onClick={() => handleDelete(meal.id)}
                    disabled={deletingId === meal.id}
                    className="text-gray-600 hover:text-red-400 transition text-sm flex-shrink-0 disabled:opacity-50"
                  >
                    {deletingId === meal.id ? '…' : 'Delete'}
                  </button>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}