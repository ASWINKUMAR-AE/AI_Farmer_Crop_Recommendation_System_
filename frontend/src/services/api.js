import axios from 'axios'

const API_BASE_URL = '/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Attach JWT token automatically
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('ai_farmer_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, (error) => {
  return Promise.reject(error)
})

// Handle 401 unauth
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Avoid redirect loop if already on login
      if (!window.location.pathname.includes('/login') && !window.location.pathname.includes('/register')) {
        localStorage.removeItem('ai_farmer_token')
        localStorage.removeItem('ai_farmer_user')
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default {
  // Auth
  register(userData) {
    return apiClient.post('/auth/register', userData)
  },
  login(credentials) {
    return apiClient.post('/auth/login', credentials)
  },
  getCurrentUser() {
    return apiClient.get('/auth/me')
  },
  logout() {
    localStorage.removeItem('ai_farmer_token')
    localStorage.removeItem('ai_farmer_user')
    return apiClient.post('/auth/logout')
  },

  // Farmer
  getProfile() {
    return apiClient.get('/profile')
  },
  updateProfile(data) {
    return apiClient.put('/profile', data)
  },
  predictCrop(inputs) {
    return apiClient.post('/predict', inputs)
  },
  getPredictions() {
    return apiClient.get('/predictions')
  },
  getPredictionDetail(id) {
    return apiClient.get(`/predictions/${id}`)
  },
  saveRecommendation(predictionId, notes = '') {
    return apiClient.post('/recommendations/save', { prediction_id: predictionId, notes })
  },
  getSavedRecommendations() {
    return apiClient.get('/recommendations/saved')
  },
  removeSavedRecommendation(savedId) {
    return apiClient.delete(`/recommendations/saved/${savedId}`)
  },
  getPredictionReportUrl(predId) {
    return `/api/predictions/${predId}/report`
  },

  // Crops & Knowledge base
  getCrops(search = '', category = '') {
    return apiClient.get('/crops', { params: { search, category } })
  },
  getCropDetail(idOrName) {
    return apiClient.get(`/crops/${idOrName}`)
  },
  getDistricts() {
    return apiClient.get('/districts')
  },
  getWeather(district) {
    return apiClient.get('/weather/current', { params: { district } })
  },

  // Admin
  getAdminDashboard() {
    return apiClient.get('/admin/dashboard')
  },
  getAdminFarmers() {
    return apiClient.get('/admin/farmers')
  },
  getAdminPredictions() {
    return apiClient.get('/admin/predictions')
  },
  getModelMetrics() {
    return apiClient.get('/admin/model-metrics')
  },
  retrainModel() {
    return apiClient.post('/admin/retrain')
  },
  getProjectDocsUrl(format = 'docx') {
    return `/api/admin/generate-docs?format=${format}`
  }
}
