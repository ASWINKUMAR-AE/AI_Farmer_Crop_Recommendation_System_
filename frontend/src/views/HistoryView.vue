<template>
  <div class="history-container container">
    <div class="page-title-banner">
      <div class="title-text">
        <span class="badge-tag badge-blue"><i class="fa-solid fa-clock-rotate-left"></i> Farm Records</span>
        <h1>Prediction History & Bookmarks</h1>
        <p>Review your historical soil test evaluations and generate official advisory reports</p>
      </div>

      <!-- Tab Buttons -->
      <div class="tab-switcher">
        <button
          class="tab-btn"
          :class="{ 'tab-active': activeTab === 'history' }"
          @click="activeTab = 'history'"
          id="tab-history"
        >
          <i class="fa-solid fa-list-check"></i> Prediction History ({{ predictions.length }})
        </button>
        <button
          class="tab-btn"
          :class="{ 'tab-active': activeTab === 'saved' }"
          @click="activeTab = 'saved'"
          id="tab-saved"
        >
          <i class="fa-solid fa-bookmark"></i> Saved Recommendations ({{ savedCrops.length }})
        </button>
      </div>
    </div>

    <!-- History Tab -->
    <div v-if="activeTab === 'history'" class="history-tab-content animate-fade-in">
      <div class="table-card glass-panel">
        <div class="table-toolbar">
          <div class="search-input-box">
            <i class="fa-solid fa-magnifying-glass"></i>
            <input type="text" v-model="searchQuery" placeholder="Search by crop, district, or season..." id="input-search-history" />
          </div>
          <router-link to="/recommend" class="btn-primary btn-sm" id="btn-hist-new-pred">
            <i class="fa-solid fa-plus"></i> New Prediction
          </router-link>
        </div>

        <div class="table-responsive">
          <table class="premium-table" id="table-prediction-history">
            <thead>
              <tr>
                <th>#</th>
                <th>Date</th>
                <th>Recommended Crop</th>
                <th>Confidence</th>
                <th>Location</th>
                <th>Soil N-P-K</th>
                <th>Weather</th>
                <th class="text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, idx) in filteredPredictions" :key="item.id">
                <td class="text-muted">{{ idx + 1 }}</td>
                <td>{{ formatDate(item.created_at) }}</td>
                <td>
                  <div class="crop-td-flex">
                    <span class="crop-emoji-sm">{{ getCropEmoji(item.recommended_crop) }}</span>
                    <strong class="crop-td-name">{{ item.recommended_crop }}</strong>
                  </div>
                </td>
                <td>
                  <span class="badge-tag badge-green">{{ item.confidence }}%</span>
                </td>
                <td>{{ item.district || 'Madurai' }}</td>
                <td>
                  <span class="npk-chip">{{ item.nitrogen }}-{{ item.phosphorus }}-{{ item.potassium }}</span>
                </td>
                <td>{{ item.temperature }}°C | {{ item.rainfall }}mm</td>
                <td class="text-right actions-td">
                  <a :href="'/api/predictions/' + item.id + '/report'" target="_blank" class="btn-action-icon btn-pdf" title="Download PDF Report">
                    <i class="fa-solid fa-file-pdf"></i>
                  </a>
                  <button @click="showDetailModal(item)" class="btn-action-icon btn-info-view" title="View Full Breakdown">
                    <i class="fa-solid fa-eye"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="filteredPredictions.length === 0">
                <td colspan="8" class="text-center py-5 text-muted">
                  <i class="fa-solid fa-folder-open mb-2 font-lg"></i>
                  <p>No prediction records found.</p>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Saved Recommendations Tab -->
    <div v-if="activeTab === 'saved'" class="saved-tab-content animate-fade-in">
      <div class="grid-cols-3">
        <div v-for="item in savedCrops" :key="item.saved_id" class="saved-crop-card glass-panel">
          <div class="saved-card-header">
            <div class="saved-crop-badge">
              <span class="crop-emoji-lg">{{ getCropEmoji(item.crop_name) }}</span>
              <div>
                <h3>{{ item.crop_name }}</h3>
                <span class="saved-date">Saved on {{ formatDate(item.saved_at) }}</span>
              </div>
            </div>
            <button @click="removeSaved(item.saved_id)" class="btn-remove-bookmark" title="Remove Bookmark">
              <i class="fa-solid fa-trash"></i>
            </button>
          </div>

          <div class="saved-details">
            <div class="saved-row">
              <span>Confidence:</span>
              <strong class="text-green">{{ item.confidence }}%</strong>
            </div>
            <div class="saved-row">
              <span>Location:</span>
              <span>{{ item.district }} ({{ item.season }})</span>
            </div>
            <div class="saved-row">
              <span>Soil Chemistry:</span>
              <span>N:{{ item.nitrogen }}, P:{{ item.phosphorus }}, K:{{ item.potassium }}, pH:{{ item.ph }}</span>
            </div>
          </div>

          <div class="saved-card-actions">
            <a :href="'/api/predictions/' + item.prediction_id + '/report'" target="_blank" class="btn-primary btn-sm flex-1">
              <i class="fa-solid fa-file-pdf"></i> Download PDF
            </a>
          </div>
        </div>

        <div v-if="savedCrops.length === 0" class="col-span-3 text-center py-5 glass-panel">
          <i class="fa-regular fa-bookmark font-xl text-muted mb-2"></i>
          <h3>No Saved Bookmarks</h3>
          <p class="text-muted">Save recommendations from the prediction result page to review them here.</p>
        </div>
      </div>
    </div>

    <!-- Detail Breakdown Modal -->
    <div v-if="selectedPred" class="modal-backdrop" @click.self="selectedPred = null">
      <div class="modal-card glass-panel animate-fade-in">
        <div class="modal-header">
          <h3>Prediction Breakdown Details</h3>
          <button class="close-btn" @click="selectedPred = null"><i class="fa-solid fa-xmark"></i></button>
        </div>
        <div class="modal-body">
          <div class="rec-crop-banner mb-3">
            <span class="crop-emoji-lg">{{ getCropEmoji(selectedPred.recommended_crop) }}</span>
            <div class="flex-1 ml-3">
              <span class="rec-tag-sm">Recommended Crop</span>
              <h2>{{ selectedPred.recommended_crop }}</h2>
              <p>{{ selectedPred.district }} | {{ selectedPred.season }}</p>
            </div>
            <div class="conf-gauge-box">
              <span class="gauge-percent">{{ selectedPred.confidence }}%</span>
              <span class="gauge-label">Confidence</span>
            </div>
          </div>

          <div class="detail-grid mb-3">
            <div class="detail-item"><strong>Nitrogen:</strong> {{ selectedPred.nitrogen }} kg/ha</div>
            <div class="detail-item"><strong>Phosphorus:</strong> {{ selectedPred.phosphorus }} kg/ha</div>
            <div class="detail-item"><strong>Potassium:</strong> {{ selectedPred.potassium }} kg/ha</div>
            <div class="detail-item"><strong>Soil pH:</strong> {{ selectedPred.ph }}</div>
            <div class="detail-item"><strong>Temperature:</strong> {{ selectedPred.temperature }} °C</div>
            <div class="detail-item"><strong>Humidity:</strong> {{ selectedPred.humidity }} %</div>
            <div class="detail-item"><strong>Rainfall:</strong> {{ selectedPred.rainfall }} mm</div>
            <div class="detail-item"><strong>Date:</strong> {{ formatDate(selectedPred.created_at) }}</div>
          </div>

          <a :href="'/api/predictions/' + selectedPred.id + '/report'" target="_blank" class="btn-primary w-100">
            <i class="fa-solid fa-file-pdf"></i> Download Official PDF Report
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'HistoryView',
  data() {
    return {
      activeTab: 'history',
      predictions: [],
      savedCrops: [],
      searchQuery: '',
      selectedPred: null,
      loading: true
    }
  },
  computed: {
    filteredPredictions() {
      if (!this.searchQuery) return this.predictions
      const q = this.searchQuery.toLowerCase()
      return this.predictions.filter(p => 
        (p.recommended_crop && p.recommended_crop.toLowerCase().includes(q)) ||
        (p.district && p.district.toLowerCase().includes(q)) ||
        (p.season && p.season.toLowerCase().includes(q))
      )
    }
  },
  async mounted() {
    await this.fetchData()
  },
  methods: {
    async fetchData() {
      this.loading = true
      try {
        const [predResp, savedResp] = await Promise.all([
          api.getPredictions(),
          api.getSavedRecommendations()
        ])
        if (predResp.data.success) this.predictions = predResp.data.predictions || []
        if (savedResp.data.success) this.savedCrops = savedResp.data.saved_crops || []
      } catch (err) {
        console.error('History fetch error:', err)
      } finally {
        this.loading = false
      }
    },
    async removeSaved(savedId) {
      try {
        await api.removeSavedRecommendation(savedId)
        this.savedCrops = this.savedCrops.filter(s => s.saved_id !== savedId)
      } catch (e) {
        console.error('Remove saved error:', e)
      }
    },
    showDetailModal(item) {
      this.selectedPred = item
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
.history-container {
  padding: 2.5rem 1.5rem 4rem;
}

.page-title-banner {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 2rem;
}

.title-text h1 {
  font-size: 2rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0.35rem 0;
}

.title-text p {
  color: #64748b;
  font-size: 0.95rem;
}

.tab-switcher {
  display: flex;
  background: white;
  padding: 0.35rem;
  border-radius: var(--radius-md);
  border: 1px solid #e2e8f0;
  gap: 0.35rem;
}

.tab-btn {
  padding: 0.6rem 1.1rem;
  border: none;
  background: none;
  border-radius: 8px;
  font-size: 0.88rem;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s;
}

.tab-active {
  background: #10b981;
  color: white;
}

.table-card {
  background: white;
  padding: 1.5rem;
}

.table-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.search-input-box {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: var(--radius-sm);
  padding: 0.6rem 1rem;
  width: 340px;
}

.search-input-box input {
  border: none;
  background: none;
  outline: none;
  font-size: 0.9rem;
  width: 100%;
}

.premium-table {
  width: 100%;
  border-collapse: collapse;
}

.premium-table th {
  text-align: left;
  padding: 0.85rem 1rem;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  color: #475569;
  background: #f8fafc;
  border-bottom: 1.5px solid #e2e8f0;
}

.premium-table td {
  padding: 1rem;
  border-bottom: 1px solid #f1f5f9;
  font-size: 0.9rem;
  vertical-align: middle;
}

.crop-td-flex {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.crop-emoji-sm {
  font-size: 1.4rem;
}

.crop-td-name {
  color: #064e3b;
  font-size: 0.95rem;
}

.npk-chip {
  background: #ecfdf5;
  color: #064e3b;
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.8rem;
}

.actions-td {
  display: flex;
  gap: 0.4rem;
  justify-content: flex-end;
}

.btn-action-icon {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  background: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  transition: all 0.2s;
  text-decoration: none;
}

.btn-pdf { color: #dc2626; }
.btn-pdf:hover { background: #fee2e2; border-color: #dc2626; }
.btn-info-view { color: #0284c7; }
.btn-info-view:hover { background: #e0f2fe; border-color: #0284c7; }

/* Saved Crops */
.saved-crop-card {
  background: white;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.saved-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.saved-crop-badge {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.saved-crop-badge h3 {
  font-size: 1.2rem;
  font-weight: 800;
  color: #064e3b;
}

.saved-date {
  font-size: 0.75rem;
  color: #64748b;
}

.btn-remove-bookmark {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  font-size: 1rem;
  transition: color 0.2s;
}

.btn-remove-bookmark:hover {
  color: #ef4444;
}

.saved-details {
  background: #f8fafc;
  padding: 0.85rem;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-bottom: 1.25rem;
  font-size: 0.85rem;
}

.saved-row {
  display: flex;
  justify-content: space-between;
}

/* Modal */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(8px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.modal-card {
  width: 100%;
  max-width: 540px;
  background: white;
  border-radius: var(--radius-lg);
  padding: 2rem;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  background: #f8fafc;
  padding: 1rem;
  border-radius: 10px;
  font-size: 0.88rem;
}

@media (max-width: 900px) {
  .page-title-banner {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}
</style>
