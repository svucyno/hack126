import { createContext, useContext, useState, useEffect } from 'react'
import { getProfile } from './api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser]       = useState(null)
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getProfile()
      .then(({ data }) => {
        setUser(data.user)
        setProfile(data.profile)
      })
      .catch(() => {
        setUser(null)
        setProfile(null)
      })
      .finally(() => setLoading(false))
  }, [])

  const refreshProfile = () =>
    getProfile()
      .then(({ data }) => {
        setUser(data.user)
        setProfile(data.profile)
      })
      .catch(() => {
        // If refresh fails, clear stale auth state rather than leaving it inconsistent
        setUser(null)
        setProfile(null)
      })

  return (
    <AuthContext.Provider value={{ user, profile, loading, refreshProfile }}>
      {children}
    </AuthContext.Provider>
  )
}

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => useContext(AuthContext)
