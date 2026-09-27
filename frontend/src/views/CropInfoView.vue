<template>
  <div class="crop-info-container container">
    <div class="page-title-banner text-center">
      <span class="badge-tag badge-green"><i class="fa-solid fa-book-open"></i> Knowledge Base</span>
      <h1>Agricultural Crop Encyclopedia</h1>
      <p>Explore empirical soil suitability, climate requirements, and agronomic practices for 22 supported crops</p>
    </div>

    <!-- Search & Filters -->
    <div class="filter-controls-bar glass-panel">
      <div class="search-box">
        <i class="fa-solid fa-magnifying-glass"></i>
        <input
          type="text"
          v-model="searchQuery"
          @input="filterCrops"
          placeholder="Search crop by name, category, or soil type (e.g. Rice, Loam, Fruit)..."
          id="input-search-crops"
        />
      </div>

      <div class="category-pills">
        <button
          v-for="cat in ['All', 'Cereal', 'Pulse', 'Fruit', 'Fiber', 'Plantation']"
          :key="cat"
          :class="['cat-btn', selectedCategory === cat ? 'cat-active' : '']"
          @click="selectCategory(cat)"
        >
          {{ cat }}
        </button>
      </div>
    </div>

    <!-- Crops Grid -->
    <div class="grid-cols-3 crops-grid">
      <div v-for="crop in filteredCrops" :key="crop.id" class="crop-detail-card glass-panel animate-fade-in">
        <div class="crop-card-top">
          <div class="crop-emoji-box">
            <span>{{ getCropEmoji(crop.crop_name) }}</span>
          </div>
          <div class="crop-title-group">
            <span class="crop-cat-badge">{{ crop.crop_category }}</span>
            <h3 class="crop-name">{{ crop.crop_name }}</h3>
          </div>
        </div>

        <div class="crop-specs-list">
          <div class="spec-row">
            <span class="spec-label"><i class="fa-solid fa-layer-group text-green"></i> Suitable Soil:</span>
            <span class="spec-val">{{ crop.suitable_soil }}</span>
          </div>
          <div class="spec-row">
            <span class="spec-label"><i class="fa-solid fa-temperature-three-quarters text-amber"></i> Temp Range:</span>
            <span class="spec-val">{{ crop.temp_min }}°C – {{ crop.temp_max }}°C</span>
          </div>
          <div class="spec-row">
            <span class="spec-label"><i class="fa-solid fa-cloud-rain text-blue"></i> Rainfall:</span>
            <span class="spec-val">{{ crop.rainfall_min }} – {{ crop.rainfall_max }} mm</span>
          </div>
          <div class="spec-row">
            <span class="spec-label"><i class="fa-solid fa-droplet text-blue"></i> Water Need:</span>
            <span class="spec-val">{{ crop.water_requirement }}</span>
          </div>
          <div class="spec-row">
            <span class="spec-label"><i class="fa-solid fa-calendar text-purple"></i> Season:</span>
            <span class="spec-val">{{ crop.season }}</span>
          </div>
        </div>

        <div class="guide-box">
          <p class="guide-text">{{ crop.cultivation_guide }}</p>
        </div>

        <div class="crop-card-footer">
          <span class="market-tag"><i class="fa-solid fa-tag"></i> {{ crop.market_value }}</span>
        </div>
      </div>
    </div>

    <div v-if="filteredCrops.length === 0" class="text-center py-5 glass-panel">
      <i class="fa-solid fa-seedling font-xl text-muted mb-2"></i>
      <h3>No Crops Found</h3>
      <p class="text-muted">Try adjusting your search query or category filter.</p>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'CropInfoView',
  data() {
    return {
      crops: [],
      filteredCrops: [],
      searchQuery: '',
      selectedCategory: 'All',
      loading: true
    }
  },
  async mounted() {
    await this.fetchCrops()
  },
  methods: {
    async fetchCrops() {
      this.loading = true
      try {
        const resp = await api.getCrops()
        if (resp.data.success) {
          this.crops = resp.data.crops || []
          this.filteredCrops = this.crops
        }
      } catch (e) {
        console.error('Error fetching crops:', e)
      } finally {
        this.loading = false
      }
    },
    selectCategory(cat) {
      this.selectedCategory = cat
      this.filterCrops()
    },
    filterCrops() {
      let list = this.crops
      if (this.selectedCategory !== 'All') {
        list = list.filter(c => c.crop_category.toLowerCase().includes(this.selectedCategory.toLowerCase()))
      }
      if (this.searchQuery.trim()) {
        const q = this.searchQuery.toLowerCase()
        list = list.filter(c => 
          c.crop_name.toLowerCase().includes(q) ||
          c.crop_category.toLowerCase().includes(q) ||
          c.suitable_soil.toLowerCase().includes(q)
        )
      }
      this.filteredCrops = list
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
.crop-info-container {
  padding: 2.5rem 1.5rem 4rem;
}

.page-title-banner {
  margin-bottom: 2rem;
}

.page-title-banner h1 {
  font-size: 2.2rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0.4rem 0;
}

.page-title-banner p {
  color: #64748b;
  font-size: 1rem;
}

.filter-controls-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  background: white;
  margin-bottom: 2.5rem;
  gap: 1.5rem;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: #f8fafc;
  border: 1.5px solid #cbd5e1;
  border-radius: var(--radius-sm);
  padding: 0.65rem 1rem;
  flex: 1;
}

.search-box input {
  border: none;
  background: none;
  outline: none;
  font-size: 0.95rem;
  width: 100%;
}

.category-pills {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.cat-btn {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 9999px;
  padding: 0.4rem 0.9rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s;
}

.cat-btn:hover {
  border-color: #10b981;
  color: #059669;
}

.cat-active {
  background: #10b981;
  border-color: #10b981;
  color: white;
}

.crops-grid {
  gap: 1.5rem;
}

.crop-detail-card {
  background: white;
  padding: 1.75rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.crop-card-top {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.crop-emoji-box {
  width: 56px;
  height: 56px;
  background: #ecfdf5;
  border: 1px solid #a7f3d0;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.2rem;
}

.crop-cat-badge {
  font-size: 0.72rem;
  font-weight: 700;
  color: #059669;
  text-transform: uppercase;
}

.crop-name {
  font-size: 1.35rem;
  font-weight: 800;
  color: #064e3b;
}

.crop-specs-list {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  margin-bottom: 1.25rem;
  font-size: 0.85rem;
}

.spec-row {
  display: flex;
  justify-content: space-between;
  gap: 0.5rem;
}

.spec-label {
  color: #64748b;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  white-space: nowrap;
}

.spec-val {
  font-weight: 600;
  color: #1e293b;
  text-align: right;
}

.guide-box {
  background: #f8fafc;
  padding: 0.85rem 1rem;
  border-radius: 10px;
  border-left: 3px solid #10b981;
  margin-bottom: 1.25rem;
}

.guide-text {
  font-size: 0.82rem;
  color: #475569;
  line-height: 1.5;
}

.crop-card-footer {
  padding-top: 0.85rem;
  border-top: 1px solid #f1f5f9;
}

.market-tag {
  font-size: 0.78rem;
  color: #0284c7;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

@media (max-width: 992px) {
  .filter-controls-bar {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
