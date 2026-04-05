
/**
 * DripFit 2D Figure SVG
 * Props:
 *   topColour        — hex string for torso/top region
 *   bottomColour     — hex string for bottom/trousers region
 *   shoesColour      — hex string for shoes
 *   accessoryColour  — hex string for accessory indicator
 *   anchorImageUrl   — optional URL for cloth texture overlay on torso
 *   skinToneHex      — hex for head/neck/hands skin tone (defaults Monk 4)
 *   dupattaColour    — optional hex; if provided renders ethnic dupatta drape
 *   gender           — 'neutral' | 'masculine' | 'feminine' (shape variation)
 */
export default function FigureSVG({
  topColour = '#C9A96E',
  bottomColour = '#2D2114',
  shoesColour = '#1A1208',
  accessoryColour = '#C9A96E',
  anchorImageUrl = null,
  skinToneHex = '#C68642',
  dupattaColour = null,
  gender = 'neutral',
}) {
  // Shoulder width varies subtly by gender variant
  const sw = gender === 'masculine' ? 100 : gender === 'feminine' ? 86 : 92
  const torsoX = (200 - sw) / 2
  const torsoW = sw

  return (
    <svg
      className="figure-svg"
      viewBox="0 0 200 460"
      xmlns="http://www.w3.org/2000/svg"
      aria-label="2D outfit figure showing selected outfit colours"
      role="img"
    >
      <defs>
        {anchorImageUrl && (
          <clipPath id="torsoClip">
            <rect x={torsoX} y="84" width={torsoW} height="118" rx="10" />
          </clipPath>
        )}
        {dupattaColour && (
          <clipPath id="dupattaClip">
            <polygon points="108,80 172,90 90,320 30,308" />
          </clipPath>
        )}
      </defs>

      {/* ── Neck ── */}
      <rect
        x="91" y="72" width="18" height="18"
        fill={skinToneHex} opacity="0.95"
        role="img" aria-label="Neck"
      />

      {/* ── Head ── */}
      <ellipse
        cx="100" cy="44" rx="29" ry="33"
        fill={skinToneHex}
        role="img" aria-label="Head"
      />
      {/* Hair accent — subtle dark cap */}
      <ellipse cx="100" cy="20" rx="29" ry="12" fill={skinToneHex} style={{ filter: 'brightness(0.6)' }} />

      {/* ── Arms (behind torso) ── */}
      <rect
        x="18" y="90" width="30" height="98" rx="14"
        fill={topColour} opacity="0.82"
        role="img" aria-label="Left sleeve"
      />
      <rect
        x="152" y="90" width="30" height="98" rx="14"
        fill={topColour} opacity="0.82"
        role="img" aria-label="Right sleeve"
      />

      {/* ── Torso / Top slot ── */}
      {anchorImageUrl ? (
        <image
          href={anchorImageUrl}
          x={torsoX} y="84" width={torsoW} height="118"
          clipPath="url(#torsoClip)"
          preserveAspectRatio="xMidYMid slice"
          role="img" aria-label="Top garment (anchor item)"
        />
      ) : (
        <rect
          x={torsoX} y="84" width={torsoW} height="118" rx="10"
          fill={topColour} opacity="0.92"
          style={{ transition: 'fill 200ms ease-in-out' }}
          role="img" aria-label="Top garment"
        />
      )}

      {/* Dupatta drape (ethnic occasion) */}
      {dupattaColour && (
        <polygon
          points="108,80 172,90 90,320 30,308"
          fill={dupattaColour}
          opacity="0.72"
          clipPath="url(#dupattaClip)"
          role="img" aria-label="Dupatta"
          style={{ transition: 'fill 200ms ease-in-out' }}
        />
      )}

      {/* ── Bottom slot ── */}
      <rect
        x="60" y="202" width="80" height="138" rx="10"
        fill={bottomColour} opacity="0.92"
        style={{ transition: 'fill 200ms ease-in-out' }}
        role="img" aria-label="Bottom garment"
      />
      {/* Leg centre seam */}
      <line x1="100" y1="202" x2="100" y2="340" stroke={bottomColour} strokeWidth="3" style={{ filter: 'brightness(0.7)' }} />

      {/* ── Hands ── */}
      <ellipse cx="32" cy="195" rx="10" ry="7" fill={skinToneHex} opacity="0.9" aria-label="Left hand" />
      <ellipse cx="168" cy="195" rx="10" ry="7" fill={skinToneHex} opacity="0.9" aria-label="Right hand" />

      {/* ── Accessory (watch/bracelet dot on wrist) ── */}
      <circle
        cx="168" cy="188" r="5"
        fill={accessoryColour} opacity="0.9"
        stroke="rgba(26,18,8,0.1)" strokeWidth="1"
        role="img" aria-label="Accessory"
      />

      {/* ── Shoes ── */}
      <ellipse
        cx="76" cy="352" rx="20" ry="11"
        fill={shoesColour} opacity="0.95"
        style={{ transition: 'fill 200ms ease-in-out' }}
        role="img" aria-label="Left shoe"
      />
      <ellipse
        cx="124" cy="352" rx="20" ry="11"
        fill={shoesColour} opacity="0.95"
        style={{ transition: 'fill 200ms ease-in-out' }}
        role="img" aria-label="Right shoe"
      />

      {/* ── DripFit watermark ── */}
      <text
        x="100" y="435" textAnchor="middle"
        fill="rgba(26,18,8,0.18)" fontSize="8"
        fontFamily="'Cormorant Garamond', Georgia, serif"
        fontStyle="italic" letterSpacing="1"
      >DripFit</text>
    </svg>
  )
}
