// This component wraps pages that require login.
// If the user isn't authenticated, it redirects them to /login
// instead of showing the protected content.

import { ReactNode } from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function ProtectedRoute({ children }: { children: ReactNode }) {
  const { user, isLoading } = useAuth()

  // While we're checking if there's a saved login token, show nothing
  // (or a spinner) instead of flashing the login page then redirecting.
  if (isLoading) {
    return <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white">Loading...</div>
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}