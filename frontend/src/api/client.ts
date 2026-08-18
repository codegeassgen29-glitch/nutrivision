// This file creates a single, shared axios instance for talking to
// our FastAPI backend. Instead of writing the full URL and headers
// in every component, we configure it once here and reuse it.

import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
})

// This runs before EVERY request made with apiClient.
// If we have a saved JWT token (from login), attach it automatically
// as "Authorization: Bearer <token>" - so we never have to
// remember to do this manually in each component.
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default apiClient