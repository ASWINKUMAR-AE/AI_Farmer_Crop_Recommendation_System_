<template>
  <div class="dashboard-container container">
    <!-- Welcome Header Banner -->
    <div class="welcome-banner glass-panel animate-fade-in">
      <div class="welcome-content">
        <div class="farmer-avatar-badge">
          <i class="fa-solid fa-wheat-awn"></i>
        </div>
        <div class="welcome-text">
          <div class="greeting-row">
            <h1>Welcome, {{ profile.full_name || user.username }}!</h1>
            <span class="badge-tag badge-green"><i class="fa-solid fa-circle-check"></i> Active Farmer</span>
          </div>
          <p class="welcome-sub">
            <i class="fa-solid fa-location-dot"></i> {{ profile.district || 'Madurai' }}, {{ profile.state || 'Tamil Nadu' }} &nbsp;|&nbsp; 
            <i class="fa-solid fa-vector-square"></i> Farm Area: {{ profile.farm_area || 2.5 }} Acres &nbsp;|&nbsp;
            <i class="fa-solid fa-language"></i> Advisory: {{ profile.preferred_language || 'English' }}
          </p>
        </div>
      </div>
      <div class="banner-action">
        <router-link to="/recommend" class="btn-primary" id="btn-dash-predict">
          <i class="fa-solid fa-wand-magic-sparkles"></i> New Crop Prediction
        </router-link>
      </div>
    </div>

    <!-- Quick Stats Grid -->
    <div class="grid-cols-4 stats-cards-grid">
      <div class="glass-card stat-metric-box">
        <div class="stat-icon-wrapper bg-green-light">
          <i class="fa-solid fa-seedling text-green"></i>
        </div>
        <div>
          <span class="stat-count">{{ totalPredictions }}</span>
          <span class="stat-meta">Total Predictions</span>
        </div>
      </div>

      <div class="glass-card stat-metric-box">
        <div class="stat-icon-wrapper bg-amber-light">
          <i class="fa-solid fa-bookmark text-amber"></i>
        </div>
        <div>
          <span class="stat-count">{{ totalSaved }}</span>
          <span class="stat-meta">Saved Bookmarks</span>
        </div>
      </div>

      <div class="glass-card stat-metric-box">
        <div class="stat-icon-wrapper bg-blue-light">
          <i class="fa-solid fa-brain text-blue"></i>
        </div>
        <div>
          <span class="stat-count">98.64%</span>
          <span class="stat-meta">Random Forest ML</span>
        </div>
      </div>

      <div class="glass-card stat-metric-box">
        <div class="stat-icon-wrapper bg-purple-light">
          <i class="fa-solid fa-cloud-sun text-purple"></i>
        </div>
        <div>
          <span class="stat-count">Samba / Rabi</span>
          <span class="stat-meta">Current Agri Season</span>
        </div>
      </div>
    </div>

    <!-- Main Dashboard Two-Column Layout -->
    <div class="dashboard-main-grid">
      <!-- Latest Recommendation Card -->
      <div class="latest-rec-card glass-panel" v-if="latestPrediction">
        <div class="card-head">
          <div>
            <span class="badge-tag badge-green">Latest AI Analysis</span>
            <h3 class="mt-1">Recent Recommendation</h3>
          </div>
          <span class="rec-date"><i class="fa-regular fa-clock"></i> {{ formatDate(latestPrediction.created_at) }}</span>
        </div>

        <div class="latest-rec-body">
          <div class="rec-crop-banner">
            <div class="crop-big-badge">
              <span class="crop-emoji-lg">{{ getCropEmoji(latestPrediction.recommended_crop) }}</span>
            </div>
            <div>
              <span class="rec-tag-sm">Recommended Crop</span>
              <h2 class="crop-name-highlight">{{ latestPrediction.recommended_crop }}</h2>
              <p class="rec-location-tag"><i class="fa-solid fa-location-dot"></i> {{ latestPrediction.district || profile.district }} ({{ latestPrediction.season }})</p>
            </div>
            <div class="conf-gauge-box">
              <span class="gauge-percent">{{ latestPrediction.confidence }}%</span>
              <span class="gauge-label">Confidence</span>
            </div>
          </div>

          <div class="soil-weather-summary-grid">
            <div class="param-badge">
              <span class="p-label">Nitrogen (N)</span>
              <strong>{{ latestPrediction.nitrogen }} kg/ha</strong>
            </div>
            <div class="param-badge">
              <span class="p-label">Phosphorus (P)</span>
              <strong>{{ latestPrediction.phosphorus }} kg/ha</strong>
            </div>
            <div class="param-badge">
              <span class="p-label">Potassium (K)</span>
              <strong>{{ latestPrediction.potassium }} kg/ha</strong>
            </div>
            <div class="param-badge">
              <span class="p-label">Rainfall</span>
              <strong>{{ latestPrediction.rainfall }} mm</strong>
            </div>
          </div>

          <div class="rec-card-actions">
            <a :href="'/api/predictions/' + latestPrediction.id + '/report'" target="_blank" class="btn-primary btn-sm" id="btn-dash-download-pdf">
              <i class="fa-solid fa-file-pdf"></i> Download PDF Report
            </a>
            <router-link to="/history" class="btn-secondary btn-sm" id="btn-dash-view-history">
              <i class="fa-solid fa-clock-rotate-left"></i> View All History
            </router-link>
          </div>
        </div>
      </div>

      <!-- No Prediction State -->
      <div v-else class="empty-state-panel glass-panel text-center">
        <div class="empty-icon"><i class="fa-solid fa-seedling"></i></div>
        <h3>No Crop Predictions Yet</h3>
        <p>Enter your soil test parameters and meteorological conditions to generate your first AI crop recommendation.</p>
        <router-link to="/recommend" class="btn-primary mt-3" id="btn-empty-predict">
          <i class="fa-solid fa-wand-magic-sparkles"></i> Predict Crop
        </router-link>
      </div>

      <!-- Quick Action Navigation Hub -->
      <div class="quick-nav-panel glass-panel">
        <h3 class="mb-3">Farmer Control Center</h3>
        <div class="nav-links-list">
          <router-link to="/recommend" class="quick-link-item" id="nav-hub-predict">
            <div class="q-icon bg-green-light text-green"><i class="fa-solid fa-wand-magic-sparkles"></i></div>
            <div class="q-text">
              <strong>Crop Recommendation Form</strong>
              <span>Enter NPK and get instant AI predictions</span>
            </div>
            <i class="fa-solid fa-chevron-right q-arrow"></i>
          </router-link>

          <router-link to="/history" class="quick-link-item" id="nav-hub-history">
            <div class="q-icon bg-blue-light text-blue"><i class="fa-solid fa-clock-rotate-left"></i></div>
            <div class="q-text">
              <strong>Prediction History & Reports</strong>
              <span>Review past soil tests and download reports</span>
            </div>
            <i class="fa-solid fa-chevron-right q-arrow"></i>
          </router-link>

          <router-link to="/crops" class="quick-link-item" id="nav-hub-crops">
            <div class="q-icon bg-amber-light text-amber"><i class="fa-solid fa-book-open"></i></div>
            <div class="q-text">
              <strong>Crop Encyclopedia</strong>
              <span>22 crop cultivation guides and market insights</span>
            </div>
            <i class="fa-solid fa-chevron-right q-arrow"></i>
          </router-link>

          <router-link to="/profile" class="quick-link-item" id="nav-hub-profile">
            <div class="q-icon bg-purple-light text-purple"><i class="fa-solid fa-user-gear"></i></div>
            <div class="q-text">
              <strong>Farmer Profile Settings</strong>
              <span>Manage land size, phone, and district</span>
            </div>
            <i class="fa-solid fa-chevron-right q-arrow"></i>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'FarmerDashboard',
  data() {
    return {
      user: {},
      profile: {},
      predictions: [],
      savedCrops: [],
      loading: true
    }
  },
  computed: {
    totalPredictions() {
      return this.predictions.length
    },
    totalSaved() {
      return this.savedCrops.length
    },
    latestPrediction() {
      return this.predictions.length > 0 ? this.predictions[0] : null
    }
  },
  async mounted() {
    await this.fetchDashboardData()
  },
  methods: {
    async fetchDashboardData() {
      this.loading = true
      try {
        const userStr = localStorage.getItem('ai_farmer_user')
        if (userStr) this.user = JSON.parse(userStr)

        const [profResp, predResp, savedResp] = await Promise.all([
          api.getProfile(),
          api.getPredictions(),
          api.getSavedRecommendations()
        ])

        if (profResp.data.success) this.profile = profResp.data.profile || {}
        if (predResp.data.success) this.predictions = predResp.data.predictions || []
        if (savedResp.data.success) this.savedCrops = savedResp.data.saved_crops || []
      } catch (err) {
        console.error('Error fetching dashboard:', err)
      } finally {
        this.loading = false
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return ''
      const d = new Date(dateStr)
      return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
    },
    getCropEmoji(name) {
      if (!name) return '🌱'
      const n = name.toLowerCase()
      const emojis = {
        rice: '🌾', maize: '🌽', chickpea: '🥜', kidneybeans: '🫘',
        pigeonpeas: '🌱', mothbeans: '🌱', mungbean: '🫘', blackgram: '🫘',
        lentil: '🥣', pomegranate: '🍎', banana: '🍌', mango: '🥭',
        grapes: '🍇', watermelon: '🍉', muskmelon: '🍈', apple: '🍏',
        orange: '🍊', papaya: '🥭', coconut: '🥥', cotton: '🌿',
        jute: '🌾', coffee: '☕'
      }
      return emojis[n] || '🌱'
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  padding: 2.5rem 1.5rem;
}

.welcome-banner {
  padding: 2rem;
  background: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  border: 1px solid #c8e6c9;
}

.welcome-content {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.farmer-avatar-badge {
  width: 64px;
  height: 64px;
  border-radius: 18px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.3);
}

.greeting-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.greeting-row h1 {
  font-size: 1.8rem;
  font-weight: 800;
  color: #0f172a;
}

.welcome-sub {
  font-size: 0.88rem;
  color: #64748b;
  margin-top: 0.35rem;
}

.stats-cards-grid {
  margin-bottom: 2.5rem;
}

.stat-metric-box {
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1.2rem;
  background: white;
}

.stat-icon-wrapper {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.35rem;
}

.bg-green-light { background: #ecfdf5; }
.bg-amber-light { background: #fef3c7; }
.bg-blue-light { background: #e0f2fe; }
.bg-purple-light { background: #f3e8ff; }

.text-green { color: #059669; }
.text-amber { color: #d97706; }
.text-blue { color: #0284c7; }
.text-purple { color: #9333ea; }

.stat-count {
  display: block;
  font-size: 1.45rem;
  font-weight: 800;
  color: #0f172a;
}

.stat-meta {
  font-size: 0.78rem;
  color: #64748b;
  font-weight: 600;
}

/* Two Column Layout */
.dashboard-main-grid {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 2rem;
}

.latest-rec-card {
  padding: 2rem;
  background: white;
}

.card-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.card-head h3 {
  font-size: 1.3rem;
  font-weight: 800;
  color: #0f172a;
}

.rec-date {
  font-size: 0.82rem;
  color: #64748b;
}

.rec-crop-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f0fdf4;
  border: 1.5px solid #a7f3d0;
  padding: 1.25rem 1.5rem;
  border-radius: var(--radius-md);
  margin-bottom: 1.5rem;
}

.crop-big-badge {
  font-size: 2.5rem;
  width: 60px;
  height: 60px;
  background: white;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
}

.rec-tag-sm {
  font-size: 0.72rem;
  text-transform: uppercase;
  font-weight: 700;
  color: #059669;
}

.crop-name-highlight {
  font-size: 1.7rem;
  font-weight: 800;
  color: #064e3b;
}

.rec-location-tag {
  font-size: 0.8rem;
  color: #64748b;
}

.conf-gauge-box {
  text-align: right;
}

.gauge-percent {
  display: block;
  font-size: 1.6rem;
  font-weight: 800;
  color: #059669;
}

.gauge-label {
  font-size: 0.72rem;
  color: #64748b;
  font-weight: 600;
}

.soil-weather-summary-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.param-badge {
  background: #f8fafc;
  padding: 0.6rem 0.8rem;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
}

.p-label {
  font-size: 0.7rem;
  color: #64748b;
}

.rec-card-actions {
  display: flex;
  gap: 0.75rem;
}

.empty-state-panel {
  padding: 3rem 2rem;
  background: white;
}

.empty-icon {
  font-size: 3rem;
  color: #10b981;
  margin-bottom: 1rem;
}

/* Quick Nav */
.quick-nav-panel {
  padding: 2rem;
  background: white;
}

.quick-nav-panel h3 {
  font-size: 1.2rem;
  font-weight: 800;
  color: #0f172a;
}

.nav-links-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.quick-link-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.9rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.quick-link-item:hover {
  background: #ecfdf5;
  border-color: #10b981;
  transform: translateX(4px);
}

.q-icon {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.15rem;
}

.q-text {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.q-text strong {
  font-size: 0.9rem;
  color: #0f172a;
}

.q-text span {
  font-size: 0.75rem;
  color: #64748b;
}

.q-arrow {
  color: #94a3b8;
  font-size: 0.85rem;
}

@media (max-width: 992px) {
  .welcome-banner {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.25rem;
  }
  .dashboard-main-grid {
    grid-template-columns: 1fr;
  }
}
</style>
