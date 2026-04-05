import { useState } from 'react'
import { analyseOutfit } from '../api'
import Toast from '../components/Toast'

const GRADE_COLOURS = {
  A: 'var(--teal-grade)',
  B: 'var(--gold-deep)',
  C: 'var(--terracotta)',
  D: 'var(--dusty-rose)',
}

export default function AnalyserPage() {
  const [file, setFile]       = useState(null)
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult]   = useState(null)
  const [toast, setToast]     = useState(null)
  const [drag, setDrag]       = useState(false)

  const showToast = (m, t = 'success') => setToast({ message: m, type: t })

  const handleFile = (f) => {
    if (!f || !f.type.startsWith('image/')) return
    setFile(f)
    setPreview(URL.createObjectURL(f))
    setResult(null)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDrag(false)
    handleFile(e.dataTransfer.files[0])
  }

  const handleAnalyse = async () => {
    if (!file) return
    setLoading(true)
    setResult(null)
    try {
      const fd = new FormData()
      fd.append('image', file)
      const { data } = await analyseOutfit(fd)
      setResult(data)
    } catch (e) {
      showToast(e.response?.data?.error || 'Analysis failed', 'error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container page-wrap">
      {/* Header */}
      <div style={{ marginBottom: 36 }}>
        <h1 className="section-title">Fashion Analyser</h1>
        <p className="section-sub">
          Module 3 — upload an outfit photo for an AI letter grade powered by Claude Vision
        </p>
      </div>

      <div className="analyser-split-grid">
        {/* Upload — fitting room mirror */}
        <div>
          <div
            className={drag ? 'drag-over' : ''}
            style={{ position: 'relative' }}
            onDragOver={(e) => { e.preventDefault(); setDrag(true) }}
            onDragLeave={() => setDrag(false)}
            onDrop={handleDrop}
          >
            {/* Mirror frame */}
            <div
              className="analyser-mirror"
              style={{
                minHeight: preview ? 0 : 380,
                display: 'flex', flexDirection: 'column',
                alignItems: 'center', justifyContent: 'center',
                cursor: 'pointer', overflow: 'hidden',
                border: drag ? '1.5px solid var(--gold)' : undefined,
              }}
            >
              <div className="analyser-mirror-frame" />
              <input
                type="file"
                accept="image/*"
                id="analyser-upload"
                onChange={(e) => handleFile(e.target.files[0])}
                style={{ position: 'absolute', inset: 0, opacity: 0, cursor: 'pointer', width: '100%', height: '100%' }}
              />

              {preview ? (
                <img
                  src={preview}
                  alt="Outfit to analyse"
                  style={{ width: '100%', maxHeight: 480, objectFit: 'contain' }}
                />
              ) : (
                <div style={{ padding: '48px 32px', textAlign: 'center' }}>
                  <div style={{ fontSize: '2.5rem', marginBottom: 18 }}>🪞</div>
                  <p style={{
                    fontFamily: 'var(--font-display)', fontSize: '1.2rem',
                    fontStyle: 'italic', color: 'var(--ink-soft)',
                    marginBottom: 10, letterSpacing: '0.03em',
                  }}>
                    Bring your outfit to the mirror
                  </p>
                  <p style={{ fontSize: '0.84rem', color: 'var(--ink-muted)', lineHeight: 1.7 }}>
                    Drop a full-body or torso-up outfit photo,<br />or click to browse
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Analyse CTA */}
          {file && (
            <button
              id="btn-analyse"
              className="btn btn-primary"
              style={{ width: '100%', justifyContent: 'center', padding: '13px', marginTop: 16 }}
              onClick={handleAnalyse}
              disabled={loading}
            >
              {loading
                ? <><span className="spinner" />&nbsp; Claude Vision is analysing…</>
                : '✦ Analyse My Outfit'}
            </button>
          )}

          {/* What we evaluate */}
          <div className="card" style={{ marginTop: 20, background: 'transparent' }}>
            <p style={{ fontSize: '0.83rem', color: 'var(--ink-muted)', lineHeight: 1.8 }}>
              Claude Vision evaluates:{' '}
              <strong style={{ color: 'var(--ink)' }}>colour harmony</strong>,{' '}
              <strong style={{ color: 'var(--ink)' }}>visual balance</strong>,{' '}
              <strong style={{ color: 'var(--ink)' }}>formality consistency</strong>, and{' '}
              <strong style={{ color: 'var(--ink)' }}>occasion suitability</strong>.
            </p>
            <p style={{ fontSize: '0.75rem', color: 'var(--ink-faint)', marginTop: 10, fontStyle: 'italic' }}>
              Free tier: 3 analyses / month
            </p>
          </div>
        </div>

        {/* Result */}
        <div>
          {loading && (
            <div className="loading-wrap">
              <span className="spinner" style={{ width: 44, height: 44, borderWidth: 3 }} />
              <p>Claude Vision is reading your outfit…</p>
              <small>Usually 3–8 seconds</small>
            </div>
          )}

          {!loading && !result && (
            <div className="empty-state">
              <div className="icon">👁️</div>
              <h3>Your critique appears here</h3>
              <p>
                Upload a photo and hit Analyse. You'll receive a letter grade with an honest,
                constructive breakdown — no harsh verdicts, just clear guidance.
              </p>
            </div>
          )}

          {result && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
              {/* Grade card */}
              <div className="grade-display">
                <span className="grade-label">Outfit Grade</span>
                <div
                  className="grade-letter"
                  style={{ color: GRADE_COLOURS[result.grade] || 'var(--gold-deep)' }}
                  aria-label={`Grade: ${result.grade}`}
                >
                  {result.grade}
                </div>
                <p style={{
                  fontSize: '0.92rem', color: 'var(--ink-muted)', maxWidth: 340,
                  lineHeight: 1.75, marginTop: 4,
                }}>
                  {result.works_well}
                </p>
                {result.analyser_uses_remaining !== 'unlimited' && (
                  <span style={{
                    fontSize: '0.72rem', color: 'var(--ink-faint)',
                    fontStyle: 'italic', marginTop: 8,
                  }}>
                    {result.analyser_uses_remaining} free{' '}
                    {result.analyser_uses_remaining === 1 ? 'analysis' : 'analyses'} remaining this month
                  </span>
                )}
              </div>

              {/* Tips */}
              <div>
                <h3 style={{
                  fontFamily: 'var(--font-display)', fontSize: '1.1rem',
                  fontWeight: 600, letterSpacing: '0.03em', marginBottom: 16,
                }}>
                  Three Ways to Elevate This
                </h3>
                <ul className="tips-list">
                  {(result.tips || []).map((tip, i) => (
                    <li className="tip-item" key={i}>
                      <span className="tip-num">{i + 1}</span>
                      <span className="tip-text">{tip}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Premium nudge — after result, non-disruptive */}
              <p style={{
                fontFamily: 'var(--font-display)', fontStyle: 'italic',
                fontSize: '0.88rem', color: 'var(--ink-faint)', textAlign: 'center', marginTop: 8,
              }}>
                Upgrade to Premium for unlimited analyses and priority AI processing
              </p>
            </div>
          )}
        </div>
      </div>

      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
    </div>
  )
}
