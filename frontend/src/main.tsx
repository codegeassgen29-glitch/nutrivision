// src/main.tsx
// ---------------------------------------------------------
// This is the JavaScript entry point referenced by index.html.
// Its ONE job: find the <div id="root"> in the HTML and tell
// React "render our whole app inside this div."
// ---------------------------------------------------------
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css' // global styles, including Tailwind

// createRoot + render is React 18's API for mounting an app.
// StrictMode is a development-only helper that warns us about
// deprecated patterns and potential bugs - it doesn't affect production.
ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
