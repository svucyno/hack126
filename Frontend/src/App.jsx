import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { AuthProvider, useAuth } from './AuthContext'
import Navbar from './components/Navbar'
import HomePage from './pages/HomePage'
import WardrobePage from './pages/WardrobePage'
import OutfitPage from './pages/OutfitPage'
import StyleMePage from './pages/StyleMePage'
import AnalyserPage from './pages/AnalyserPage'
import SavedLooksPage from './pages/SavedLooksPage'

function RequireAuth({ children }) {
  const { user, loading } = useAuth()
  const location = useLocation()

  if (loading) return (
    <div className="loading-wrap" style={{ minHeight: '60vh' }}>
      <span className="spinner" style={{ width: 40, height: 40, borderWidth: 3 }} />
      <p>Loading DripFit…</p>
    </div>
  )

  if (!user) {
    // Pass ?next= so that after Google OAuth the user lands back on the page they wanted
    const next = encodeURIComponent(location.pathname + location.search)
    return (
      <div className="container page-wrap" style={{ textAlign: 'center' }}>
        <div style={{ fontSize: '3rem', marginBottom: 20 }}>🔒</div>
        <h2 style={{ fontFamily: 'var(--font-display)', fontSize: '1.8rem', fontWeight: 600, marginBottom: 10 }}>Sign in to continue</h2>
        <p style={{ color: 'var(--ink-muted)', marginBottom: 28, fontSize: '0.95rem' }}>This page requires a DripFit account.</p>
        <a href={`/accounts/google/login/?next=${next}`} className="btn btn-primary">Sign in with Google</a>
      </div>
    )
  }

  return children
}

function AppRoutes() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/"           element={<HomePage />} />
        <Route path="/style-me"   element={<StyleMePage />} />
        <Route path="/wardrobe"   element={<RequireAuth><WardrobePage /></RequireAuth>} />
        <Route path="/outfit"     element={<RequireAuth><OutfitPage /></RequireAuth>} />
        <Route path="/analyser"   element={<RequireAuth><AnalyserPage /></RequireAuth>} />
        <Route path="/looks"      element={<RequireAuth><SavedLooksPage /></RequireAuth>} />
        <Route path="*"           element={<Navigate to="/" replace />} />
      </Routes>
    </>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  )
}
