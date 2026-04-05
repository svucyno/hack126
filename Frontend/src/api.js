import axios from 'axios'

/** Read a cookie value by name */
function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^|;\\s*)' + name + '=([^;]*)'))
  return match ? decodeURIComponent(match[2]) : null
}

const api = axios.create({
  baseURL: '/',
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' },
})

// Attach Django's CSRF token from the csrftoken cookie for all mutating requests.
// DRF's SessionAuthentication enforces CSRF even on AllowAny endpoints when a
// session cookie is present, so we must send X-CSRFToken on every POST/PUT/PATCH/DELETE.
api.interceptors.request.use((config) => {
  const csrfToken = getCookie('csrftoken')
  if (csrfToken && ['post', 'put', 'patch', 'delete'].includes(config.method)) {
    config.headers['X-CSRFToken'] = csrfToken
  }
  return config
})

// ---------- Auth ----------
export const getProfile = () => api.get('/api/auth/profile/')

// ---------- Wardrobe ----------
export const getWardrobe = () => api.get('/api/wardrobe/')
export const uploadItem = (formData) =>
  api.post('/api/wardrobe/upload/', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
export const deleteItem = (id) => api.delete(`/api/wardrobe/${id}/`)

// ---------- Outfit Engine ----------
export const generateOutfit = (data) => api.post('/api/outfit/generate/', data)
export const styleMe = (data) => api.post('/api/outfit/style-me/', data)

// ---------- Saved Looks ----------
export const getSavedLooks = () => api.get('/api/outfit/looks/')
export const saveLook = (data) => api.post('/api/outfit/looks/', data)
export const deleteLook = (id) => api.delete(`/api/outfit/looks/${id}/`)

// ---------- Fashion Analyser ----------
export const analyseOutfit = (formData) =>
  api.post('/api/analyser/analyse/', formData, { headers: { 'Content-Type': 'multipart/form-data' } })

export default api
