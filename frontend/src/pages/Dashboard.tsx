// The main dashboard - shows today's nutrition totals as a circular
// progress ring, macro breakdown bars, a weekly trend chart, recent
// meals, and AI-generated recommendations styled as a "coach" card.

import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { BarChart, Bar, XAxis, ResponsiveContainer } from 'recharts'
import apiClient from '../api/client'
import { useAuth } from '../context/AuthContext'

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

interface DailySummary {
  date: string
  total_calories: number
  total_protein: number
  total_carbs: number
  total_fat: number
}

interface DashboardData {
  today: DailySummary
  recent_meals: Meal[]
  weekly_calories: DailySummary[]
  recommendations: string[]
}

const TARGETS = { calories: 2650, protein: 190, carbs: 300, fat: 78 }

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const { user, logout } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    apiClient
      .get('/dashboard/summary')
      .then((response) => setData(response.data))
      .finally(() => setIsLoading(false))
  }, [])

  function handleLogout() {
    logout()
    navigate('/')
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#0a0f0d] text-white flex items-center justify-center">
        <p className="text-gray-500">Loading your dashboard…</p>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="min-h-screen bg-[#0a0f0d] text-white flex items-center justify-center">
        <p className="text-gray-500">Could not load dashboard.</p>
      </div>
    )
  }

  const caloriesLeft = Math.max(TARGETS.calories - data.today.total_calories, 0)
  const caloriePct = Math.min((data.today.total_calories / TARGETS.calories) * 100, 100)

  return (
    <div className="min-h-screen bg-[#0a0f0d] text-white">
      {/* Top bar */}
      <div className="flex justify-between items-center px-4 sm:px-8 py-4 sm:py-5 border-b border-white/5">
        <Link to="/" className="flex items-center gap-2">
          <span className="w-7 h-7 rounded-full bg-gradient-to-br from-emerald-400 to-teal-500 flex items-center justify-center text-xs font-bold text-black flex-shrink-0">
            N
          </span>
          <span className="font-semibold hidden md:inline">NutriVision AI</span>
        </Link>
        <div className="flex items-center gap-2 sm:gap-3">
          <span className="text-sm text-gray-500 hidden md:inline">
            {user?.full_name || user?.email}
          </span>
          <Link
            to="/history"
            className="text-sm text-gray-400 hover:text-white transition px-2 sm:px-3 py-1.5 hidden xs:inline"
          >
            History
          </Link>
          <Link
            to="/upload"
            className="flex items-center gap-1.5 bg-emerald-400 hover:bg-emerald-300 text-black text-xs sm:text-sm font-semibold px-2.5 sm:px-4 py-1.5 sm:py-2 rounded-full transition whitespace-nowrap"
          >
            Scan a meal
          </Link>
          <button
            onClick={handleLogout}
            className="text-sm text-gray-500 hover:text-white transition px-1 sm:px-2"
          >
            Log out
          </button>
        </div>
      </div>

      <div className="px-4 sm:px-8 py-8 max-w-6xl mx-auto">
        {/* Greeting */}
        <div className="flex flex-col sm:flex-row justify-between sm:items-end gap-3 mb-8">
          <div>
            <p className="text-sm text-gray-500 mb-1">
              {new Date().toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric' })}
            </p>
            <h1 className="text-2xl sm:text-3xl font-bold">
              Welcome back, <span className="text-emerald-400">{user?.full_name?.split(' ')[0] || 'there'}</span>
            </h1>
          </div>
          <div className="bg-emerald-400/10 border border-emerald-400/20 text-emerald-300 text-sm font-medium px-4 py-2 rounded-full self-start sm:self-auto">
            {Math.round(caloriesLeft)} kcal left today
          </div>
        </div>

        {/* Top row: calorie ring + macros */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 mb-6">
          <div className="bg-[#0f1613] border border-white/5 rounded-2xl p-6 flex flex-col items-center justify-center">
            <CalorieRing value={data.today.total_calories} target={TARGETS.calories} pct={caloriePct} />
            <p className="text-xs text-gray-500 mt-3">
              {Math.round(caloriePct)}% of daily goal reached
            </p>
          </div>

          <MacroCard label="Protein" icon="●" color="emerald" value={data.today.total_protein} target={TARGETS.protein} />
          <MacroCard label="Carbs" icon="●" color="sky" value={data.today.total_carbs} target={TARGETS.carbs} />
          <MacroCard label="Fat" icon="●" color="amber" value={data.today.total_fat} target={TARGETS.fat} />
        </div>

        {/* Weekly chart */}
        <div className="bg-[#0f1613] border border-white/5 rounded-2xl p-4 sm:p-6 mb-6">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h2 className="font-semibold">Weekly intake</h2>
              <p className="text-xs text-gray-500">Calories, last 7 days</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={160}>
            <BarChart data={data.weekly_calories}>
              <XAxis
                dataKey="date"
                tickFormatter={(d) => new Date(d).toLocaleDateString(undefined, { weekday: 'short' })}
                stroke="#4b5563"
                fontSize={12}
                tickLine={false}
                axisLine={false}
              />
              <Bar dataKey="total_calories" fill="#34d399" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Bottom row: recent meals + AI coach */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-[#0f1613] border border-white/5 rounded-2xl p-4 sm:p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="font-semibold">Recent meals</h2>
              <Link to="/upload" className="text-emerald-400 text-sm hover:underline">
                + Add meal
              </Link>
            </div>
            {data.recent_meals.length === 0 ? (
              <p className="text-gray-500 text-sm py-8 text-center">
                No meals logged yet. Scan your first meal to get started.
              </p>
            ) : (
              <div className="space-y-1">
                {data.recent_meals.map((meal) => {
                  const totalCal = meal.detected_foods.reduce((sum, f) => sum + (f.calories || 0), 0)
                  const foodNames = meal.detected_foods.map((f) => f.food_name).join(', ') || 'Unidentified food'
                  return (
                    <div
                      key={meal.id}
                      className="flex justify-between items-center gap-3 py-3 border-b border-white/5 last:border-0"
                    >
                      <div className="flex items-center gap-3 min-w-0">
                        <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-emerald-400/20 to-teal-500/20 flex items-center justify-center text-lg flex-shrink-0">
                          🍽️
                        </div>
                        <div className="min-w-0">
                          <p className="font-medium text-sm capitalize truncate">{foodNames}</p>
                          <p className="text-xs text-gray-500">
                            {new Date(meal.created_at).toLocaleString(undefined, {
                              month: 'short',
                              day: 'numeric',
                              hour: 'numeric',
                              minute: '2-digit',
                            })}
                          </p>
                        </div>
                      </div>
                      <span className="text-emerald-400 text-sm font-medium flex-shrink-0">{Math.round(totalCal)} kcal</span>
                    </div>
                  )
                })}
              </div>
            )}
          </div>

          <div className="bg-[#0f1613] border border-white/5 rounded-2xl p-4 sm:p-6">
            <div className="flex items-center gap-2 mb-3">
              <span className="text-emerald-400">✦</span>
              <h2 className="font-semibold">AI coach</h2>
            </div>
            <div className="space-y-3">
              {data.recommendations.map((tip, i) => (
                <p key={i} className="text-sm text-gray-400 leading-relaxed">
                  {tip}
                </p>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function CalorieRing({ value, target, pct }: { value: number; target: number; pct: number }) {
  const radius = 54
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (pct / 100) * circumference

  return (
    <div className="relative w-36 h-36">
      <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120">
        <circle cx="60" cy="60" r={radius} fill="none" stroke="#1a2420" strokeWidth="10" />
        <circle
          cx="60"
          cy="60"
          r={radius}
          fill="none"
          stroke="#34d399"
          strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{ transition: 'stroke-dashoffset 0.6s ease' }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-xs text-gray-500 uppercase tracking-wide">Calories</span>
        <span className="text-3xl font-bold text-emerald-400">{Math.round(value)}</span>
        <span className="text-xs text-gray-500">of {target} kcal</span>
      </div>
    </div>
  )
}

const colorMap: Record<string, { text: string; bar: string }> = {
  emerald: { text: 'text-emerald-400', bar: 'bg-emerald-400' },
  sky: { text: 'text-sky-400', bar: 'bg-sky-400' },
  amber: { text: 'text-amber-400', bar: 'bg-amber-400' },
}

function MacroCard({
  label,
  color,
  value,
  target,
}: {
  label: string
  icon: string
  color: string
  value: number
  target: number
}) {
  const pct = Math.min((value / target) * 100, 100)
  const c = colorMap[color]

  return (
    <div className="bg-[#0f1613] border border-white/5 rounded-2xl p-5">
      <p className="text-sm text-gray-500 mb-2">{label}</p>
      <p className="text-2xl font-bold mb-3">
        {Math.round(value)}
        <span className="text-sm text-gray-500">/{target}g</span>
      </p>
      <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden">
        <div className={`h-full ${c.bar} rounded-full transition-all`} style={{ width: `${pct}%` }} />
      </div>
      <p className="text-xs text-gray-500 mt-2">{Math.max(target - value, 0)}g remaining</p>
    </div>
  )
}