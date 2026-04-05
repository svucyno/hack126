import { useEffect, useState } from 'react'
import FigureSVG from './FigureSVG'

/* ─── Monk Scale — actual skin-tone hex values ─── */
const MONK_SWATCHES = [
  { hex: '#f6ede4', label: 'Monk 1 — porcelain warm' },
  { hex: '#f0d5b6', label: 'Monk 2 — light warm beige' },
  { hex: '#daa679', label: 'Monk 3 — light medium warm' },
  { hex: '#c68642', label: 'Monk 4 — medium warm brown' },
  { hex: '#9a6132', label: 'Monk 5 — medium brown' },
  { hex: '#6b3a1f', label: 'Monk 6 — deep warm brown' },
  { hex: '#3a1a0a', label: 'Monk 7 — very deep brown' },
]

const OCCASIONS = [
  { id: 'casual',         label: 'Casual',          emoji: '☀️' },
  { id: 'formal',         label: 'Formal',          emoji: '👔' },
  { id: 'party',          label: 'Party',            emoji: '✨' },
  { id: 'sport',          label: 'Sport',            emoji: '🏃' },
  { id: 'ethnic_festive', label: 'Ethnic & Festive', emoji: '🪔', ethnic: true },
]

/* ─── Animated SVG Score Ring ─── */
function ScoreRing({ score }) {
  const [animated, setAnimated] = useState(0)
  useEffect(() => {
    const t = setTimeout(() => setAnimated(score), 120)
    return () => clearTimeout(t)
  }, [score])

  const r = 36
  const circumference = 2 * Math.PI * r
  const offset = circumference - (animated / 100) * circumference

  return (
    <div className="score-ring-wrap" aria-label={`Score: ${score} out of 100`}>
      <svg width="90" height="90" viewBox="0 0 90 90" aria-hidden="true">
        <circle cx="45" cy="45" r={r} fill="none" stroke="var(--surface-3)" strokeWidth="6" />
        <circle
          cx="45" cy="45" r={r} fill="none"
          stroke="var(--gold-deep)" strokeWidth="6"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform="rotate(-90 45 45)"
          style={{ transition: 'stroke-dashoffset 600ms var(--ease-calm)' }}
        />
      </svg>
      <span className="score-value">{score}</span>
    </div>
  )
}

/* ─── Score Breakdown Bars ─── */
function ScoreBreakdown({ score }) {
  const rows = [
    { label: 'Colour Harmony', value: score?.colour_harmony ?? 0, max: 40 },
    { label: 'Skin Tone Match', value: score?.skin_tone_match ?? 0, max: 30 },
    { label: 'Occasion Fit',   value: score?.occasion_fit   ?? 0, max: 30 },
  ]
  return (
    <div className="score-breakdown">
      {rows.map(r => (
        <div className="score-row" key={r.label}>
          <span className="score-label">{r.label}</span>
          <div className="score-bar-wrap">
            <div
              className="score-bar"
              style={{ width: `${(r.value / r.max) * 100}%` }}
            />
          </div>
          <span className="score-num">{r.value}/{r.max}</span>
        </div>
      ))}
    </div>
  )
}

/* ─── Outfit Result Card ─── */
export function OutfitResultCard({ outfit, rank = 0, onSave, skinTone = 4 }) {
  const [gender, setGender] = useState('neutral')
  if (!outfit) return null

  // Engine returns items as a dict: { top:{}, bottom:{}, shoes:{}, accessory:{} }
  const itemsDict = outfit.items || {}
  const top  = itemsDict.top       || {}
  const bot  = itemsDict.bottom    || {}
  const shoe = itemsDict.shoes     || {}
  const acc  = itemsDict.accessory || {}

  // All items as array for rendering the chip list
  const itemsList = [
    Object.keys(top).length  ? { ...top,  item_type: 'top' }       : null,
    Object.keys(bot).length  ? { ...bot,  item_type: 'bottom' }    : null,
    Object.keys(shoe).length ? { ...shoe, item_type: 'shoes' }     : null,
    Object.keys(acc).length  ? { ...acc,  item_type: 'accessory' } : null,
  ].filter(Boolean)

  const skinHex = MONK_SWATCHES[(skinTone || 4) - 1]?.hex || '#c68642'
  // Show dupatta drape if accessory is a dupatta subtype
  const dupattaColour = (acc.item_subtype === 'dupatta') ? acc.colour_hex : null

  return (
    <div className="outfit-card-wrap">
      {/* Left — 2D Figure */}
      <div className="figure-wrap">
        {rank === 0
          ? <span className="outfit-best-badge">✦ Best Outfit</span>
          : <span className="outfit-alt-badge">Alt {rank}</span>
        }

        {/* Gender toggle */}
        <div className="figure-gender-toggle" role="group" aria-label="Figure gender">
          {['neutral','feminine','masculine'].map(g => (
            <button
              key={g}
              className={`gender-btn${gender === g ? ' active' : ''}`}
              onClick={() => setGender(g)}
              type="button"
            >
              {g.charAt(0).toUpperCase() + g.slice(1)}
            </button>
          ))}
        </div>

        <FigureSVG
          topColour={top?.colour_hex || '#C9A96E'}
          bottomColour={bot?.colour_hex || '#2D2114'}
          shoesColour={shoe?.colour_hex || '#1A1208'}
          accessoryColour={acc?.colour_hex || '#C9A96E'}
          anchorImageUrl={top?.cutout_image_url || null}
          skinToneHex={skinHex}
          dupattaColour={dupattaColour}
          gender={gender}
        />
        <span className="figure-label">{outfit.persona || 'Style Persona'}</span>
      </div>

      {/* Right — Details */}
      <div>
        <div className="persona-badge">✦ {outfit.persona || 'Your Style Persona'}</div>

        <div className="outfit-score-ring">
          <ScoreRing score={outfit.score?.total ?? 0} />
          <div style={{ flex: 1 }}>
            <div style={{
              fontSize: '0.72rem', color: 'var(--ink-muted)', letterSpacing: '0.07em',
              textTransform: 'uppercase', fontWeight: 600, marginBottom: 10,
            }}>
              Score out of 100
            </div>
            <ScoreBreakdown score={outfit.score} />
          </div>
        </div>

        {/* Outfit items */}
        <div className="outfit-items-grid">
          {itemsList.map(item => (
            <div className="outfit-item-chip" key={item.id || item.item_type}>
              <div className="colour-dot" style={{ background: item.colour_hex }} />
              <div className="outfit-item-text">
                <div className="type">{item.item_type}</div>
                <div className="name">{item.item_subtype || item.colour_name || item.colour_hex}</div>
              </div>
            </div>
          ))}
        </div>

        {/* Score rationale */}
        {outfit.score?.rationale && (
          <p className="score-rationale">"{outfit.score.rationale}"</p>
        )}

        {onSave && (
          <button
            className="btn btn-secondary btn-sm"
            style={{ marginTop: 20 }}
            onClick={() => onSave(outfit)}
          >
            Save this Look
          </button>
        )}
      </div>
    </div>
  )
}

/* ─── Monk Selector ─── */
export function MonkSelector({ value, onChange }) {
  return (
    <div className="form-group">
      <label className="form-label">Skin Tone — Monk Scale</label>
      <div className="monk-grid" role="radiogroup" aria-label="Monk skin tone scale">
        {MONK_SWATCHES.map((swatch, i) => (
          <button
            key={i}
            className={`monk-swatch${value === i + 1 ? ' selected' : ''}`}
            style={{ background: swatch.hex }}
            title={swatch.label}
            onClick={() => onChange(i + 1)}
            type="button"
            role="radio"
            aria-checked={value === i + 1}
            aria-label={swatch.label}
          />
        ))}
      </div>
      {value && (
        <p style={{ marginTop: 8, fontSize: '0.75rem', color: 'var(--ink-muted)', fontStyle: 'italic' }}>
          {MONK_SWATCHES[value - 1]?.label}
        </p>
      )}
    </div>
  )
}

/* ─── Occasion Picker ─── */
export function OccasionPicker({ value, onChange }) {
  return (
    <div className="form-group">
      <label className="form-label">Occasion</label>
      <div className="occasion-chips" role="radiogroup" aria-label="Occasion selector">
        {OCCASIONS.map(o => (
          <button
            key={o.id}
            className={`occasion-chip${value === o.id ? ' selected' : ''}${o.ethnic ? ' ethnic' : ''}`}
            onClick={() => onChange(o.id)}
            type="button"
            role="radio"
            aria-checked={value === o.id}
          >
            {o.ethnic && <span className="jewel-dot" aria-hidden="true" />}
            <span>{o.emoji}</span>
            <span>{o.label}</span>
          </button>
        ))}
      </div>
    </div>
  )
}
