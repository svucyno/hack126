/* Warm cream shimmer skeleton — matches OutfitResultCard layout */
export default function SkeletonLoader() {
  return (
    <div className="skeleton-card">
      {/* Figure placeholder */}
      <div className="skeleton-figure">
        <div className="shimmer-warm skeleton-figure-body" />
        <div className="shimmer-warm skeleton-figure-label" />
      </div>
      {/* Details placeholder */}
      <div className="skeleton-details">
        <div className="shimmer-warm skeleton-badge" />
        <div className="skeleton-score-row">
          <div className="shimmer-warm skeleton-ring" />
          <div className="skeleton-bars">
            <div className="shimmer-warm skeleton-bar" style={{ width: '100%' }} />
            <div className="shimmer-warm skeleton-bar" style={{ width: '80%' }} />
            <div className="shimmer-warm skeleton-bar" style={{ width: '65%' }} />
          </div>
        </div>
        <div className="skeleton-chips">
          {[1,2,3,4].map(i => (
            <div key={i} className="shimmer-warm skeleton-chip" />
          ))}
        </div>
      </div>
    </div>
  )
}
