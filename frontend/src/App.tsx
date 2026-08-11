// src/App.tsx
// ---------------------------------------------------------
// This is the ROOT component of our entire React app.
// Right now it's a simple placeholder that proves:
//   1. React is rendering correctly
//   2. Tailwind CSS classes are working
//   3. It can successfully call our FastAPI backend
//
// In Milestone 10 this will become the real landing page.
// In Milestone 3 we'll add React Router here to handle
// multiple pages (Login, Dashboard, etc.)
// ---------------------------------------------------------
import { useEffect, useState } from 'react'
import axios from 'axios'

function App() {
  // React state: a variable that, when changed, tells React
  // "re-render this component with the new value."
  // `message` starts as an empty string until the backend responds.
  const [message, setMessage] = useState<string>('Connecting to backend...')

  // useEffect runs code AFTER the component first renders.
  // The empty array [] at the end means "only run this once,
  // when the component first mounts" - not on every re-render.
  useEffect(() => {
    axios
      .get('http://localhost:8000/')
      .then((response) => {
        // response.data is the JSON our FastAPI /  route returned:
        // { "message": "Welcome to NutriVision AI API" }
        setMessage(response.data.message)
      })
      .catch(() => {
        setMessage('Could not reach backend. Is it running?')
      })
  }, [])

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white">
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold">🥗 NutriVision AI</h1>
        <p className="text-lg text-gray-300">{message}</p>
      </div>
    </div>
  )
}

export default App
