import { useState, useEffect, useCallback } from 'react'
import { getSavedLooks, deleteLook } from '../api'
import { useAuth } from '../AuthContext'
import Toast from '../components/Toast'

const OCCASION_LABELS = {
  casual:         '☀️ Casual',
  formal:         '👔 Formal',
  party:          '✨ Party',
  sport:          '🏃 Sport',
  ethnic_festive: '🪔 Ethnic & Festive',
}

export default function SavedLooksPage() {
  const { profile }       = useAuth()
  const [looks, setLooks]     = useState([])
  const [loading, setLoading] = useState(true)
  const [toast, setToast]     = useState(null)

  const showToast = (m, t = 'success') => setToast({ message: m, type: t })

  const load = useCallback(() => {
    setLoading(true)
    getSavedLooks()
      .then(({ data }) => setLooks(data.looks || []))
      .catch(() => showToast('Failed to load saved looks', 'error'))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    load()
  }, [load])

  const handleDelete = async (id) => {
    try {
      await deleteLook(id)
      setLooks(prev => prev.filter(l => l.id !== id))
      showToast('Look removed')
    } catch {
      showToast('Could not remove look', 'error')
    }
  }

  return (
    <div className="container page-wrap">
      <div style={{ marginBottom: 32 }}>
        <h1 className="section-title">Saved Looks</h1>
        <p className="section-sub">
          {looks.length} saved look{looks.length !== 1 ? 's' : ''}
          &nbsp;·&nbsp;
          <span style={{ fontStyle: 'italic' }}>
            {profile?.tier === 'premium' ? 'Unlimited saves' : 'Free tier: up to 3'}
          </span>
        </p>
      </div>

      {loading ? (
        <div className="loading-wrap">
          <span className="spinner" />
          <p>Loading your looks…</p>
        </div>
      ) : looks.length === 0 ? (
        <div className="empty-state">
          <div className="icon">📚</div>
          <h3>No saved looks yet</h3>
          <p>
            Generate or explore an outfit and hit{' '}
            <strong>Save this Look</strong> to build your style archive.
          </p>
        </div>
      ) : (
        <div className="looks-grid">
          {looks.map(look => {
            const items = look.outfit_data?.items || []
            return (
              <div className="look-card fade-up" key={look.id}>
                {/* Card header — score + persona */}
                <div className="look-card-header">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <div>
                      <div className="look-score">
                        {look.total_score}
                        <span className="look-score-sub"> /100</span>
                      </div>
                      <div className="look-persona">
                        {look.persona || 'Style Persona'}
                      </div>
                    </div>
                    <span style={{
                      fontSize: '0.75rem', color: 'var(--ink-muted)',
                      padding: '4px 10px', background: 'var(--surface-2)',
                      borderRadius: '99px', fontWeight: 500,
                    }}>
                      {OCCASION_LABELS[look.occasion] || look.occasion}
                    </span>
                  </div>
                </div>

                {/* Card body */}
                <div className="look-card-body">
                  {/* Colour palette */}
                  <div className="look-colour-dots">
                    {items.map((item, i) => (
                      <div
                        key={i}
                        className="look-dot"
                        title={`${item.item_type}: ${item.colour_hex}`}
                        style={{ background: item.colour_hex }}
                        role="img"
                        aria-label={`${item.item_type} in ${item.colour_hex}`}
                      />
                    ))}
                  </div>

                  {look.note && (
                    <div className="look-note">"{look.note}"</div>
                  )}

                  {/* Score rationale if available */}
                  {look.outfit_data?.score?.rationale && (
                    <p className="score-rationale" style={{ marginTop: 10, fontSize: '0.82rem' }}>
                      "{look.outfit_data.score.rationale}"
                    </p>
                  )}

                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 16 }}>
                    <span style={{ fontSize: '0.74rem', color: 'var(--ink-faint)', fontStyle: 'italic' }}>
                      {new Date(look.created_at).toLocaleDateString('en-GB', {
                        day: 'numeric', month: 'short', year: 'numeric',
                      })}
                    </span>
                    <button
                      className="btn btn-danger btn-sm"
                      onClick={() => handleDelete(look.id)}
                      aria-label={`Delete look from ${new Date(look.created_at).toLocaleDateString()}`}
                    >
                      Remove
                    </button>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}

      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
    </div>
  )
}
