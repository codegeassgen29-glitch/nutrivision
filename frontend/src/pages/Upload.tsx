// The meal upload page - lets the user pick or drag a food photo,
// uploads it to our backend, and shows the AI detection results
// (foods identified + nutrition) once processing completes.

import { useState, useRef } from 'react'
import { Link, useNavigate } from 'react-router-dom'
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

interface MealResult {
  id: number
  image_path: string
  created_at: string
  detected_foods: DetectedFood[]
}

type Status = 'idle' | 'ready' | 'uploading' | 'done' | 'error'

export default function Upload() {
  const [file, setFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [status, setStatus] = useState<Status>('idle')
  const [result, setResult] = useState<MealResult | null>(null)
  const [errorMsg, setErrorMsg] = useState('')
  const [isDragging, setIsDragging] = useState(false)

  const fileInputRef = useRef<HTMLInputElement>(null)
  const navigate = useNavigate()

  function handleFileSelected(selected: File) {
    setFile(selected)
    setPreviewUrl(URL.createObjectURL(selected))
    setStatus('ready')
    setResult(null)
    setErrorMsg('')
  }

  function handleInputChange(e: React.ChangeEvent<HTMLInputElement>) {
    const selected = e.target.files?.[0]
    if (selected) handleFileSelected(selected)
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault()
    setIsDragging(false)
    const dropped = e.dataTransfer.files?.[0]
    if (dropped) handleFileSelected(dropped)
  }

  async function handleUpload() {
    if (!file) return
    setStatus('uploading')
    setErrorMsg('')

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await apiClient.post<MealResult>('/meals/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setResult(response.data)
      setStatus('done')
    } catch (err: any) {
      const detail = err.response?.data?.detail
      setErrorMsg(typeof detail === 'string' ? detail : 'Upload failed. Please try again.')
      setStatus('error')
    }
  }

  function reset() {
    setFile(null)
    setPreviewUrl(null)
    setStatus('idle')
    setResult(null)
    setErrorMsg('')
  }

  const totalCalories = result?.detected_foods.reduce((sum, f) => sum + (f.calories || 0), 0) ?? 0

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
        <Link to="/dashboard" className="text-sm text-gray-400 hover:text-white transition">
          ← Back to dashboard
        </Link>
      </div>

      <div className="max-w-2xl mx-auto px-8 py-12">
        <h1 className="text-3xl font-bold mb-2">Scan a meal</h1>
        <p className="text-gray-500 mb-8">
          Upload a photo of your food and our AI will identify it and estimate its nutrition.
        </p>

        {/* Upload zone / preview */}
        {status === 'idle' ? (
          <div
            onDragOver={(e) => {
              e.preventDefault()
              setIsDragging(true)
            }}
            onDragLeave={() => setIsDragging(false)}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`aspect-video rounded-2xl border-2 border-dashed flex flex-col items-center justify-center cursor-pointer transition ${
              isDragging
                ? 'border-emerald-400 bg-emerald-400/5'
                : 'border-white/10 hover:border-white/20 bg-[#0f1613]'
            }`}
          >
            <div className="text-4xl mb-3">📸</div>
            <p className="font-medium mb-1">Drag a photo here, or click to browse</p>
            <p className="text-sm text-gray-500">JPG, PNG, or WEBP</p>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/jpeg,image/png,image/webp"
              className="hidden"
              onChange={handleInputChange}
            />
          </div>
        ) : (
          <div className="rounded-2xl overflow-hidden bg-[#0f1613] border border-white/5">
            <div className="relative aspect-video">
              {previewUrl && (
                <img src={previewUrl} alt="Selected meal" className="w-full h-full object-cover" />
              )}
              {status === 'uploading' && (
                <div className="absolute inset-0 bg-black/60 flex flex-col items-center justify-center">
                  <div className="w-8 h-8 border-2 border-emerald-400 border-t-transparent rounded-full animate-spin mb-3" />
                  <p className="text-sm text-emerald-300">Analyzing your meal…</p>
                </div>
              )}
            </div>

            <div className="p-5">
              {status === 'ready' && (
                <div className="flex gap-3">
                  <button
                    onClick={handleUpload}
                    className="flex-1 bg-emerald-400 hover:bg-emerald-300 text-black font-semibold py-2.5 rounded-full transition"
                  >
                    Analyze meal
                  </button>
                  <button
                    onClick={reset}
                    className="px-5 border border-white/10 hover:border-white/30 rounded-full transition text-sm"
                  >
                    Cancel
                  </button>
                </div>
              )}

              {status === 'error' && (
                <div>
                  <p className="text-red-400 text-sm mb-3">{errorMsg}</p>
                  <button
                    onClick={reset}
                    className="w-full border border-white/10 hover:border-white/30 rounded-full py-2.5 transition text-sm"
                  >
                    Try again
                  </button>
                </div>
              )}

              {status === 'done' && result && (
                <div>
                  <div className="flex justify-between items-center mb-4">
                    <p className="font-semibold">Detected</p>
                    <p className="text-emerald-400 font-semibold">{Math.round(totalCalories)} kcal</p>
                  </div>

                  {result.detected_foods.length === 0 ? (
                    <p className="text-gray-500 text-sm mb-4">
                      No foods recognized in this image. Our AI is still learning — try a
                      clearer photo, or this dish may not be in our library yet.
                    </p>
                  ) : (
                    <div className="space-y-2 mb-5">
                      {result.detected_foods.map((f) => (
                        <div
                          key={f.id}
                          className="flex justify-between items-center bg-white/5 rounded-lg px-4 py-2.5"
                        >
                          <div>
                            <p className="text-sm font-medium capitalize">{f.food_name}</p>
                            <p className="text-xs text-gray-500">
                              {Math.round(f.confidence * 100)}% confidence
                            </p>
                          </div>
                          <p className="text-sm text-gray-400">
                            {f.calories != null ? `${Math.round(f.calories)} kcal` : '—'}
                          </p>
                        </div>
                      ))}
                    </div>
                  )}

                  <div className="flex gap-3">
                    <button
                      onClick={() => navigate('/dashboard')}
                      className="flex-1 bg-emerald-400 hover:bg-emerald-300 text-black font-semibold py-2.5 rounded-full transition"
                    >
                      Done
                    </button>
                    <button
                      onClick={reset}
                      className="px-5 border border-white/10 hover:border-white/30 rounded-full transition text-sm"
                    >
                      Scan another
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}