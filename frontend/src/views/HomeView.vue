<template>
  <div class="home-container">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container hero-content">
        <div class="hero-text-col">
          <div class="hero-badge">
            <i class="fa-solid fa-seedling"></i>
            <span>AI Precision Agriculture Platform</span>
          </div>
          <h1 class="hero-title">
            Smart Crop Advisory Powered by <span class="gradient-text">Machine Learning</span>
          </h1>
          <p class="hero-desc">
            Make confident agronomic decisions. Our trained Random Forest AI model analyzes soil nutrients (N, P, K), pH, and regional meteorological conditions to recommend the highest yielding crop for your land.
          </p>
          <div class="hero-stats-row">
            <div class="stat-pill">
              <span class="stat-num">98.64%</span>
              <span class="stat-label">Model Accuracy</span>
            </div>
            <div class="stat-pill">
              <span class="stat-num">22</span>
              <span class="stat-label">Crop Species</span>
            </div>
            <div class="stat-pill">
              <span class="stat-num">100%</span>
              <span class="stat-label">Free & Offline ML</span>
            </div>
          </div>
          <div class="hero-actions">
            <router-link to="/recommend" class="btn-primary btn-lg" id="btn-hero-predict">
              <i class="fa-solid fa-wand-magic-sparkles"></i> Predict Crop Now
            </router-link>
            <router-link to="/crops" class="btn-secondary btn-lg" id="btn-hero-crops">
              <i class="fa-solid fa-book-open"></i> Browse Crop Guide
            </router-link>
          </div>
        </div>

        <div class="hero-visual-col">
          <div class="hero-card-preview glass-panel pulse-glow">
            <div class="preview-header">
              <div class="crop-icon-large">🌾</div>
              <div>
                <span class="badge-tag badge-green"><i class="fa-solid fa-check"></i> High Confidence</span>
                <h3 class="preview-crop-title">Rice (Paddy)</h3>
                <p class="preview-sub">Optimal for High Rainfall & Clay Loam</p>
              </div>
            </div>
            <div class="preview-metric-grid">
              <div class="metric-item">
                <span class="m-label">Nitrogen (N)</span>
                <span class="m-val text-green">90 kg/ha</span>
              </div>
              <div class="metric-item">
                <span class="m-label">Phosphorus (P)</span>
                <span class="m-val">42 kg/ha</span>
              </div>
              <div class="metric-item">
                <span class="m-label">Potassium (K)</span>
                <span class="m-val">43 kg/ha</span>
              </div>
              <div class="metric-item">
                <span class="m-label">Rainfall</span>
                <span class="m-val text-blue">202 mm</span>
              </div>
            </div>
            <div class="preview-conf-bar">
              <div class="conf-head">
                <span>AI Confidence Score</span>
                <strong>92.0%</strong>
              </div>
              <div class="progress-track">
                <div class="progress-fill" style="width: 92%;"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works -->
    <section class="section-how">
      <div class="container">
        <div class="section-header text-center">
          <span class="badge-tag badge-blue">Workflow</span>
          <h2>How AI Farmer Recommends Crops</h2>
          <p>Scientific four-step machine learning pipeline for precision agriculture</p>
        </div>

        <div class="grid-cols-4 steps-grid">
          <div class="step-card glass-card">
            <div class="step-num">1</div>
            <div class="step-icon"><i class="fa-solid fa-flask"></i></div>
            <h4>Soil Nutrient Input</h4>
            <p>Input your soil test Nitrogen (N), Phosphorus (P), Potassium (K) & pH values.</p>
          </div>
          <div class="step-card glass-card">
            <div class="step-num">2</div>
            <div class="step-icon"><i class="fa-solid fa-cloud-sun-rain"></i></div>
            <h4>Meteorological Data</h4>
            <p>Fetch live weather for your district or enter temperature, humidity and rainfall.</p>
          </div>
          <div class="step-card glass-card">
            <div class="step-num">3</div>
            <div class="step-icon"><i class="fa-solid fa-brain"></i></div>
            <h4>Random Forest ML</h4>
            <p>Ensemble decision trees evaluate 22 crop classes with stratified precision.</p>
          </div>
          <div class="step-card glass-card">
            <div class="step-num">4</div>
            <div class="step-icon"><i class="fa-solid fa-file-pdf"></i></div>
            <h4>Report & Advisory</h4>
            <p>Receive top-3 predictions, confidence score, cultivation guide & PDF report.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Supported Crops Showcase -->
    <section class="section-crops-showcase">
      <div class="container">
        <div class="section-header">
          <div>
            <span class="badge-tag badge-green">Crop Diversity</span>
            <h2>22 Supported Agricultural Crops</h2>
          </div>
          <router-link to="/crops" class="btn-secondary">View All Details <i class="fa-solid fa-arrow-right"></i></router-link>
        </div>

        <div class="crops-chips-grid">
          <div v-for="crop in sampleCrops" :key="crop.name" class="crop-chip glass-card">
            <span class="crop-emoji">{{ crop.emoji }}</span>
            <div class="crop-info">
              <span class="c-name">{{ crop.name }}</span>
              <span class="c-cat">{{ crop.category }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      sampleCrops: [
        { name: 'Rice', category: 'Cereal', emoji: '🌾' },
        { name: 'Maize', category: 'Cereal', emoji: '🌽' },
        { name: 'Cotton', category: 'Fiber', emoji: '🌱' },
        { name: 'Coffee', category: 'Plantation', emoji: '☕' },
        { name: 'Banana', category: 'Fruit', emoji: '🍌' },
        { name: 'Pomegranate', category: 'Fruit', emoji: '🍎' },
        { name: 'Mango', category: 'Fruit', emoji: '🥭' },
        { name: 'Grapes', category: 'Fruit', emoji: '🍇' },
        { name: 'Blackgram', category: 'Pulse', emoji: '🫘' },
        { name: 'Chickpea', category: 'Pulse', emoji: '🥜' },
        { name: 'Coconut', category: 'Plantation', emoji: '🥥' },
        { name: 'Watermelon', category: 'Cucurbit', emoji: '🍉' }
      ]
    }
  }
}
</script>

<style scoped>
.hero-section {
  padding: 4.5rem 0 3.5rem;
}

.hero-content {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 3.5rem;
  align-items: center;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.9rem;
  background: var(--primary-light);
  color: var(--primary-dark);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 9999px;
  font-size: 0.85rem;
  font-weight: 700;
  margin-bottom: 1.25rem;
}

.hero-title {
  font-size: 2.85rem;
  font-weight: 800;
  line-height: 1.2;
  color: #0f172a;
  margin-bottom: 1.25rem;
  letter-spacing: -1px;
}

.gradient-text {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-desc {
  font-size: 1.08rem;
  color: #475569;
  line-height: 1.65;
  margin-bottom: 2rem;
}

.hero-stats-row {
  display: flex;
  gap: 1.25rem;
  margin-bottom: 2.25rem;
}

.stat-pill {
  display: flex;
  flex-direction: column;
  padding: 0.75rem 1.25rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: var(--radius-md);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}

.stat-num {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--primary-dark);
}

.stat-label {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 600;
}

.hero-actions {
  display: flex;
  gap: 1rem;
}

.btn-lg {
  padding: 0.9rem 2rem !important;
  font-size: 1.02rem !important;
}

/* Hero Preview Card */
.hero-card-preview {
  padding: 2rem;
  background: rgba(255, 255, 255, 0.95);
  border: 1.5px solid #10b981;
}

.preview-header {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  margin-bottom: 1.5rem;
}

.crop-icon-large {
  font-size: 3.2rem;
  background: #ecfdf5;
  width: 76px;
  height: 76px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 18px;
  border: 1px solid #a7f3d0;
}

.preview-crop-title {
  font-size: 1.6rem;
  font-weight: 800;
  color: #064e3b;
  margin: 0.2rem 0;
}

.preview-sub {
  font-size: 0.82rem;
  color: #64748b;
}

.preview-metric-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.9rem;
  margin-bottom: 1.5rem;
}

.metric-item {
  background: #f8fafc;
  padding: 0.75rem;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
}

.m-label {
  font-size: 0.72rem;
  color: #64748b;
  font-weight: 600;
}

.m-val {
  font-size: 1.05rem;
  font-weight: 700;
  color: #0f172a;
}

.text-green { color: #059669; }
.text-blue { color: #0284c7; }

.preview-conf-bar {
  background: #f8fafc;
  padding: 1rem;
  border-radius: 12px;
}

.conf-head {
  display: flex;
  justify-content: space-between;
  font-size: 0.88rem;
  margin-bottom: 0.5rem;
}

.progress-track {
  height: 10px;
  background: #e2e8f0;
  border-radius: 9999px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #10b981 0%, #059669 100%);
  border-radius: 9999px;
}

/* Sections */
.section-how {
  padding: 4.5rem 0;
  background: rgba(255, 255, 255, 0.7);
  border-top: 1px solid #e2e8f0;
  border-bottom: 1px solid #e2e8f0;
}

.section-header {
  margin-bottom: 3rem;
}

.text-center {
  text-align: center;
}

.section-header h2 {
  font-size: 2.1rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0.5rem 0;
}

.section-header p {
  color: #64748b;
  font-size: 1.02rem;
}

.step-card {
  padding: 1.75rem;
  position: relative;
}

.step-num {
  position: absolute;
  top: 1rem;
  right: 1.25rem;
  font-size: 1.8rem;
  font-weight: 900;
  color: #e2e8f0;
}

.step-icon {
  width: 48px;
  height: 48px;
  background: #ecfdf5;
  color: #059669;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  margin-bottom: 1.25rem;
}

.step-card h4 {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.step-card p {
  font-size: 0.85rem;
  color: #64748b;
  line-height: 1.5;
}

/* Crops Showcase */
.section-crops-showcase {
  padding: 4.5rem 0;
}

.section-crops-showcase .section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.crops-chips-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
}

.crop-chip {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.1rem;
}

.crop-emoji {
  font-size: 2.2rem;
}

.crop-info {
  display: flex;
  flex-direction: column;
}

.c-name {
  font-size: 1.05rem;
  font-weight: 700;
  color: #1e293b;
}

.c-cat {
  font-size: 0.75rem;
  color: #64748b;
  text-transform: uppercase;
  font-weight: 600;
}

@media (max-width: 992px) {
  .hero-content {
    grid-template-columns: 1fr;
  }
  .crops-chips-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
