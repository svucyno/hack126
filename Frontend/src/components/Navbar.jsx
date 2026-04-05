import { useState } from 'react'
import { useAuth } from '../AuthContext'
import { NavLink, useLocation } from 'react-router-dom'

export default function Navbar() {
  const { user, profile } = useAuth()
  const [menuOpen, setMenuOpen] = useState(false)
  const location = useLocation()

  const navLinks = user ? [
    { to: '/wardrobe',  label: 'Wardrobe' },
    { to: '/outfit',    label: 'Outfit' },
    { to: '/style-me',  label: 'Style Me' },
    { to: '/analyser',  label: 'Analyser' },
    { to: '/looks',     label: 'Saved Looks' },
  ] : []

  const nextParam = `?next=${encodeURIComponent(location.pathname)}`

  return (
    <>
      <nav className="navbar">
        <div className="navbar-inner">
          <NavLink to="/" className="navbar-brand" onClick={() => setMenuOpen(false)}>
            DripFit<span> ✦</span>
          </NavLink>

          {/* Desktop tabs */}
          {user && (
            <div className="navbar-tabs">
              {navLinks.map(l => (
                <NavLink
                  key={l.to}
                  to={l.to}
                  className={({ isActive }) => `navbar-tab${isActive ? ' active' : ''}`}
                >
                  {l.label}
                </NavLink>
              ))}
            </div>
          )}

          <div className="navbar-auth">
            {user ? (
              <>
                <span className={`tier-badge${profile?.tier === 'premium' ? ' premium' : ''}`}>
                  {profile?.tier === 'premium' ? '✦ Premium' : 'Free'}
                </span>
                <span className="navbar-email">{user.email}</span>
                {/* Fixed: was /accounts/google/login/?process=logout (wrong — re-triggers login) */}
                <a href="/accounts/logout/" className="btn btn-secondary btn-sm">Sign Out</a>
              </>
            ) : (
              <a href={`/accounts/google/login/${nextParam}`} className="btn btn-gold btn-sm">
                Sign in with Google
              </a>
            )}

            {/* Mobile hamburger — only shown on small screens */}
            {user && (
              <button
                className="navbar-hamburger"
                aria-label={menuOpen ? 'Close menu' : 'Open menu'}
                aria-expanded={menuOpen}
                onClick={() => setMenuOpen(o => !o)}
              >
                <span className={`ham-line${menuOpen ? ' open' : ''}`} />
                <span className={`ham-line${menuOpen ? ' open' : ''}`} />
                <span className={`ham-line${menuOpen ? ' open' : ''}`} />
              </button>
            )}
          </div>
        </div>
      </nav>

      {/* Mobile drawer — only rendered if user is logged in */}
      {user && menuOpen && (
        <div className="mobile-menu" role="navigation" aria-label="Mobile navigation">
          {navLinks.map(l => (
            <NavLink
              key={l.to}
              to={l.to}
              className={({ isActive }) => `mobile-menu-link${isActive ? ' active' : ''}`}
              onClick={() => setMenuOpen(false)}
            >
              {l.label}
            </NavLink>
          ))}
        </div>
      )}
    </>
  )
}
