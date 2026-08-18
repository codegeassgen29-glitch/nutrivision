// This file provides authentication state (is the user logged in?
// what's their info?) to the entire app via React Context.
// Any component can access this with the useAuth() hook below,
// instead of passing login state down through every component manually.

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import apiClient from '../api/client'

interface User {
  id: number
  email: string
  full_name: string | null
}

interface AuthContextType {
  user: User | null
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

// Context needs a default value for TypeScript, but it's never
// actually used - the real value comes from AuthProvider below.
const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // On app load, check if we already have a saved token and
  // try to fetch the user's profile with it - this keeps users
  // logged in across page refreshes.
  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (!token) {
      setIsLoading(false)
      return
    }

    apiClient
      .get('/users/me')
      .then((response) => setUser(response.data))
      .catch(() => {
        // Token invalid/expired - clear it
        localStorage.removeItem('access_token')
      })
      .finally(() => setIsLoading(false))
  }, [])

  async function login(email: string, password: string) {
    // Our backend's /auth/login expects OAuth2 form data
    // (username + password), not JSON - so we build a form here.
    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)

    const response = await apiClient.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })

    const token = response.data.access_token
    localStorage.setItem('access_token', token)

    // Fetch and store the user's profile right after login
    const profileResponse = await apiClient.get('/users/me')
    setUser(profileResponse.data)
  }

  function logout() {
    localStorage.removeItem('access_token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

// Custom hook - lets any component do `const { user, login } = useAuth()`
// instead of importing useContext and AuthContext every time.
export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}