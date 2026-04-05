import { useState } from 'react'
import { styleMe, saveLook } from '../api'
import { useAuth } from '../AuthContext'
import { MonkSelector, OccasionPicker, OutfitResultCard } from '../components/OutfitComponents'
import SkeletonLoader from '../components/SkeletonLoader'
import Toast from '../components/Toast'

export default function StyleMePage() {
  const { profile }               = useAuth()
  const [skinTone, setSkinTone]   = useState(profile?.monk_scale || 4)
  const [occasion, setOccasion]   = useState('casual')
  const [loading, setLoading]     = useState(false)
  const [results, setResults]     = useState(null)
  const [activeIdx, setActiveIdx] = useState(0)
  const [toast, setToast]         = useState(null)

  const showToast = (m, t = 'success') => setToast({ message: m, type: t })

  const handle = async () => {
    setLoading(true)
    setResults(null)
    try {
      const { data } = await styleMe({ skin_tone: skinTone, occasion })
      setResults(data)
      setActiveIdx(0)
    } catch (e) {
      showToast(e.response?.data?.error || 'Failed to get style suggestions', 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async (outfit) => {
    try {
      await saveLook({ outfit_data: outfit, occasion, note: '' })
      showToast('Look saved to your collection')
    } catch (e) {
      showToast(e.response?.data?.error || 'Could not save look', 'error')
    }
  }

  const allOutfits = results ? [results.best_outfit, ...(results.alternatives || [])].filter(Boolean) : []

  return (
    <div className="container page-wrap">
      {/* Header */}
      <div style={{ marginBottom: 36 }}>
        <h1 className="section-title">Style Me</h1>
        <p className="section-sub">
          <em style={{ fontFamily: 'var(--font-display)', fontStyle: 'italic' }}>
            Let's see what works for you today
          </em>
          &nbsp;· No wardrobe upload needed
        </p>
      </div>

      <div className="page-split-grid">
        {/* Controls */}
        <div className="card" style={{ position: 'sticky', top: 88 }}>
          <MonkSelector value={skinTone} onChange={setSkinTone} />
          <hr className="divider" />
          <OccasionPicker value={occasion} onChange={setOccasion} />
          <hr className="divider" />
          <button
            id="btn-style-me"
            className="btn btn-primary"
            style={{ width: '100%', justifyContent: 'center', padding: '13px' }}
            onClick={handle}
            disabled={loading}
          >
            {loading ? <><span className="spinner" />&nbsp; Curating…</> : '✦ Style Me'}
          </button>
          <p style={{
            fontSize: '0.74rem', color: 'var(--ink-faint)',
            marginTop: 12, textAlign: 'center', fontStyle: 'italic',
          }}>
            Pulls from a curated sample dataset · No account needed
          </p>
        </div>

        {/* Results */}
        <div>
          {loading && (
            <div>
              <SkeletonLoader />
              <p style={{ textAlign: 'center', marginTop: 16, color: 'var(--ink-muted)', fontStyle: 'italic', fontSize: '0.85rem' }}>
                Curating your look…
              </p>
            </div>
          )}

          {!loading && !results && (
            <div className="empty-state">
              <div className="icon">🌅</div>
              <h3>Get instant style inspiration</h3>
              <p>
                Pick your skin tone and the occasion, then hit{' '}
                <strong>Style Me</strong> for ready-to-wear outfit ideas — no uploads required.
              </p>
            </div>
          )}

          {results && allOutfits.length > 0 && (
            <>
              {/* Desktop: arrow nav + tabs */}
              <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 24 }}>
                <button
                  className="btn btn-secondary btn-sm"
                  onClick={() => setActiveIdx(i => Math.max(0, i - 1))}
                  disabled={activeIdx === 0}
                  aria-label="Previous outfit alternative"
                >
                  ←
                </button>
                <div className="tabs" style={{ flex: 1, marginBottom: 0 }} role="tablist">
                  {allOutfits.map((_, i) => (
                    <button
                      key={i}
                      role="tab"
                      aria-selected={activeIdx === i}
                      className={`tab${activeIdx === i ? ' active' : ''}`}
                      onClick={() => setActiveIdx(i)}
                    >
                      {i === 0 ? '⭐ Best Look' : `Alt ${i}`}
                    </button>
                  ))}
                </div>
                <button
                  className="btn btn-secondary btn-sm"
                  onClick={() => setActiveIdx(i => Math.min(allOutfits.length - 1, i + 1))}
                  disabled={activeIdx === allOutfits.length - 1}
                  aria-label="Next outfit alternative"
                >
                  →
                </button>
              </div>

              <div className="outfit-results" role="tabpanel">
                <OutfitResultCard
                  outfit={allOutfits[activeIdx]}
                  rank={activeIdx}
                  onSave={handleSave}
                  skinTone={skinTone}
                />
              </div>

              <p style={{
                textAlign: 'center', marginTop: 20, fontSize: '0.78rem',
                color: 'var(--ink-faint)', fontStyle: 'italic',
              }}>
                Swipe or use arrows to browse alternatives
              </p>
            </>
          )}
        </div>
      </div>

      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
    </div>
  )
}
