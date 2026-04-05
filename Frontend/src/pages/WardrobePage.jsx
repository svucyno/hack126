import { useState, useEffect, useCallback } from 'react'
import { getWardrobe, uploadItem, deleteItem } from '../api'
import { useAuth } from '../AuthContext'
import Toast from '../components/Toast'

export default function WardrobePage() {
  const { profile } = useAuth()
  const [items, setItems]       = useState([])
  const [loading, setLoading]   = useState(true)
  const [uploading, setUploading] = useState(false)
  const [toast, setToast]       = useState(null)
  const [drag, setDrag]         = useState(false)

  const showToast = (message, type = 'success') => setToast({ message, type })

  const load = useCallback(() => {
    setLoading(true)
    getWardrobe()
      .then(({ data }) => setItems(data.items || []))
      .catch(() => showToast('Failed to load wardrobe', 'error'))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    load()
  }, [load])

  const handleFiles = async (files) => {
    if (!files?.length) return
    setUploading(true)
    let successCount = 0
    for (const file of Array.from(files)) {
      if (!file.type.startsWith('image/')) continue
      const fd = new FormData()
      fd.append('image', file)
      try {
        await uploadItem(fd)
        successCount++
      } catch (e) {
        showToast(e.response?.data?.error || 'Upload failed', 'error')
        break
      }
    }
    if (successCount) {
      showToast(`${successCount} item${successCount > 1 ? 's' : ''} uploaded & analysed`)
      load()
    }
    setUploading(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDrag(false)
    handleFiles(e.dataTransfer.files)
  }

  const handleDelete = async (id) => {
    try {
      await deleteItem(id)
      setItems(prev => prev.filter(i => i.id !== id))
      showToast('Item removed from wardrobe')
    } catch {
      showToast('Could not remove item', 'error')
    }
  }

  const canUpload = profile?.can_upload_more !== false
  const limit = profile?.tier === 'premium' ? '∞' : '10'

  return (
    <div className="container page-wrap">
      {/* Header */}
      <div style={{ marginBottom: 32 }}>
        <h1 className="section-title">My Wardrobe</h1>
        <p className="section-sub">
          {items.length} / {limit} items
          &nbsp;·&nbsp;
          <span style={{ fontStyle: 'italic' }}>Claude Vision analyses each upload automatically</span>
        </p>
      </div>

      {/* Upload Zone */}
      <div
        className={`upload-zone${drag ? ' drag-over' : ''}`}
        style={{
          minHeight: 160, opacity: canUpload ? 1 : 0.5,
          transition: 'var(--trans-fast)',
        }}
        onDragOver={(e) => { e.preventDefault(); setDrag(true) }}
        onDragLeave={() => setDrag(false)}
        onDrop={handleDrop}
      >
        <input
          type="file"
          multiple accept="image/*"
          disabled={!canUpload || uploading}
          onChange={(e) => handleFiles(e.target.files)}
          id="wardrobe-upload"
        />

        <div className="upload-icon">{uploading ? '⏳' : '✦'}</div>

        {uploading ? (
          <>
            <p><strong>Analysing with Claude Vision AI…</strong></p>
            <p style={{ fontSize: '0.82rem', marginTop: 6, color: 'var(--ink-faint)' }}>
              Detecting item type, pattern & formality
            </p>
            <div style={{ marginTop: 16 }}>
              <span className="spinner" />
            </div>
          </>
        ) : canUpload ? (
          <>
            <p><strong>Drop a garment on the styling table</strong></p>
            <p style={{ marginTop: 6, color: 'var(--ink-faint)', fontSize: '0.82rem' }}>
              or click to browse · JPEG / PNG · Multiple files OK
            </p>
          </>
        ) : (
          <p>
            Free tier limit reached ({limit} items).{' '}
            <strong>Upgrade to Premium</strong> for unlimited uploads.
          </p>
        )}
      </div>

      {/* Wardrobe note */}
      <p style={{
        marginTop: 12, fontSize: '0.78rem',
        color: 'var(--ink-faint)', fontStyle: 'italic', textAlign: 'center',
      }}>
        Item type, colour palette, and formality are automatically extracted by AI
      </p>

      {/* Grid */}
      {loading ? (
        <div className="loading-wrap">
          <span className="spinner" style={{ width: 32, height: 32, borderWidth: 3 }} />
          <p>Loading your wardrobe…</p>
        </div>
      ) : items.length === 0 ? (
        <div className="empty-state">
          <div className="icon">👗</div>
          <h3>Your wardrobe is empty</h3>
          <p>Upload your first clothing item above to get started. Each piece will be automatically categorised.</p>
        </div>
      ) : (
        <div className="wardrobe-grid">
          {items.map(item => (
            <div className="wardrobe-item fade-up" key={item.id}>
              <img src={item.image} alt={`${item.item_type} — ${item.colour_hex}`} loading="lazy" />
              <div className="wardrobe-item-info">
                <span className="category-badge">{item.item_subtype || item.item_type}</span>
              </div>
              <button
                className="wardrobe-item-delete"
                onClick={() => handleDelete(item.id)}
                title="Remove from wardrobe"
                aria-label={`Remove ${item.item_type} from wardrobe`}
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      )}

      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
    </div>
  )
}
