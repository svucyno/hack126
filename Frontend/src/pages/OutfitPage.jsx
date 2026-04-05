import { useState } from 'react'
import { generateOutfit, saveLook } from '../api'
import { useAuth } from '../AuthContext'
import { MonkSelector, OccasionPicker, OutfitResultCard } from '../components/OutfitComponents'
import SkeletonLoader from '../components/SkeletonLoader'
import Toast from '../components/Toast'

export default function OutfitPage() {
  const { profile }             = useAuth()
  const [skinTone, setSkinTone] = useState(profile?.monk_scale || 4)
  const [occasion, setOccasion] = useState('casual')
  const [loading, setLoading]   = useState(false)
  const [results, setResults]   = useState(null)
  const [activeIdx, setActiveIdx] = useState(0)
  const [toast, setToast]       = useState(null)

  const showToast = (m, t = 'success') => setToast({ message: m, type: t })

  const handleGenerate = async () => {
    setLoading(true)
    setResults(null)
    try {
      const { data } = await generateOutfit({ skin_tone: skinTone, occasion })
      setResults(data)
      setActiveIdx(0)
    } catch (e) {
      showToast(e.response?.data?.error || 'Failed to generate outfit', 'error')
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

  const allOutfits = results
    ? [results.best_outfit, ...(results.alternatives || [])].filter(Boolean)
    : []

  return (
    <div className="container page-wrap">
      <div style={{ marginBottom: 36 }}>
        <h1 className="section-title">Outfit Suggester</h1>
        <p className="section-sub">
          Module 1 — colour-theory engine builds complete looks from your wardrobe
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
            className="btn btn-primary"
            style={{ width: '100%', justifyContent: 'center', padding: '13px' }}
            onClick={handleGenerate}
            disabled={loading}
            id="btn-generate-outfit"
          >
            {loading
              ? <><span className="spinner" />&nbsp; Running engine…</>
              : '✦ Find My Outfit'}
          </button>
          <p style={{
            fontSize: '0.74rem', color: 'var(--ink-faint)',
            marginTop: 12, textAlign: 'center', fontStyle: 'italic',
          }}>
            6 colour-theory steps · skin palette · harmony filter · rank
          </p>
        </div>

        {/* Results */}
        <div>
          {/* Loading — warm skeleton */}
          {loading && (
            <div>
              <div style={{ marginBottom: 16 }}>
                <SkeletonLoader />
              </div>
              <p style={{
                fontSize: '0.82rem', color: 'var(--ink-muted)',
                fontStyle: 'italic', textAlign: 'center',
              }}>
                Running through your wardrobe…
              </p>
            </div>
          )}

          {/* Empty state */}
          {!loading && !results && (
            <div className="empty-state">
              <div className="icon" style={{ fontSize: '3rem' }}>👗</div>
              <h3>Ready to style you</h3>
              <p>
                Select your skin tone and the occasion, then hit{' '}
                <strong>Find My Outfit</strong> to see colour-scored combinations from your wardrobe.
              </p>
            </div>
          )}

          {/* Results with tab switcher */}
          {results && allOutfits.length > 0 && (
            <>
              <div className="tabs" role="tablist" aria-label="Outfit alternatives">
                {allOutfits.map((_, i) => (
                  <button
                    key={i}
                    role="tab"
                    aria-selected={activeIdx === i}
                    className={`tab${activeIdx === i ? ' active' : ''}`}
                    onClick={() => setActiveIdx(i)}
                  >
                    {i === 0 ? '⭐ Best Outfit' : `Alt ${i}`}
                  </button>
                ))}
              </div>

              <div className="outfit-results" role="tabpanel">
                <OutfitResultCard
                  outfit={allOutfits[activeIdx]}
                  rank={activeIdx}
                  onSave={handleSave}
                  skinTone={skinTone}
                />
              </div>

              {results.stats && (
                <p style={{
                  fontSize: '0.78rem', color: 'var(--ink-faint)', marginTop: 18,
                  fontFamily: 'var(--font-display)', fontStyle: 'italic', textAlign: 'right',
                }}>
                  {results.stats.combinations_built} combinations built ·{' '}
                  {results.stats.combinations_rejected} filtered ·{' '}
                  {results.stats.combinations_ranked} ranked
                </p>
              )}
            </>
          )}

          {results && allOutfits.length === 0 && (
            <div className="empty-state">
              <div className="icon">🤔</div>
              <h3>No outfits found</h3>
              <p>
                Try a different occasion or upload more items to your wardrobe.
                The engine needs at least one top and one bottom to build a complete look.
              </p>
            </div>
          )}
        </div>
      </div>

      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
    </div>
  )
}
