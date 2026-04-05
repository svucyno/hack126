import { useEffect, useRef } from 'react'

export default function Toast({ message, type = 'success', onClose }) {
  // Use a ref so that a new onClose reference from parent re-renders
  // doesn't fire a fresh 4-second timer (which was causing early dismissal).
  const onCloseRef = useRef(onClose)
  useEffect(() => { onCloseRef.current = onClose }, [onClose])

  useEffect(() => {
    const t = setTimeout(() => onCloseRef.current(), 4000)
    return () => clearTimeout(t)
  }, []) // intentionally empty — timer only starts once per mount

  const icon = type === 'success' ? '✦' : '!'

  return (
    <div className={`toast ${type}`} role="alert" aria-live="polite">
      <span className="toast-icon" style={{ color: type === 'error' ? 'var(--terracotta)' : 'var(--gold-deep)' }}>
        {icon}
      </span>
      <span className="toast-message">{message}</span>
      <button
        onClick={onClose}
        style={{
          marginLeft: 'auto', background: 'none', border: 'none',
          color: 'var(--ink-muted)', cursor: 'pointer', fontSize: '1rem',
          padding: '2px 4px',
        }}
        aria-label="Dismiss notification"
      >×</button>
    </div>
  )
}
