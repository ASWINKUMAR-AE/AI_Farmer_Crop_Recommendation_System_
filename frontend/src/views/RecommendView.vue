<template>
  <div class="recommend-container container">
    <div class="page-title-banner text-center">
      <span class="badge-tag badge-green"><i class="fa-solid fa-microchip"></i> Machine Learning Model</span>
      <h1>AI Crop Recommendation Engine</h1>
      <p>Provide your soil chemistry and meteorological conditions to generate a scientific crop advisory.</p>
    </div>

    <!-- Preset Test Chips -->
    <div class="presets-row">
      <span class="preset-label"><i class="fa-solid fa-wand-magic"></i> Quick Test Presets:</span>
      <button type="button" @click="applyPreset('rice')" class="btn-preset" id="btn-preset-rice">🌾 Rice (Paddy)</button>
      <button type="button" @click="applyPreset('cotton')" class="btn-preset" id="btn-preset-cotton">🌿 Cotton</button>
      <button type="button" @click="applyPreset('maize')" class="btn-preset" id="btn-preset-maize">🌽 Maize</button>
      <button type="button" @click="applyPreset('banana')" class="btn-preset" id="btn-preset-banana">🍌 Banana</button>
      <button type="button" @click="applyPreset('coffee')" class="btn-preset" id="btn-preset-coffee">☕ Coffee</button>
    </div>

    <div class="form-result-layout">
      <!-- Input Form Card -->
      <div class="form-card glass-panel">
        <div class="form-section-head">
          <div class="sec-icon"><i class="fa-solid fa-flask-vial"></i></div>
          <div>
            <h3>Soil & Climate Parameters</h3>
            <p>Enter analytical values obtained from soil tests & local meteorology</p>
          </div>
        </div>

        <form @submit.prevent="submitPrediction" class="prediction-form">
          <!-- District & Season Row -->
          <div class="grid-cols-3">
            <div class="form-group">
              <label class="form-label" for="input-district">
                <span>District</span>
                <button type="button" @click="fetchDistrictWeather" class="btn-fetch-weather" id="btn-fetch-weather" title="Fetch live weather">
                  <i class="fa-solid fa-cloud-arrow-down"></i> Live Weather
                </button>
              </label>
              <select id="input-district" v-model="form.district" @change="fetchDistrictWeather" class="form-control" required>
                <option v-for="d in districts" :key="d" :value="d">{{ d }}</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label" for="input-season">Season</label>
              <select id="input-season" v-model="form.season" class="form-control" required>
                <option value="Kharif (Monsoon)">Kharif (Monsoon)</option>
                <option value="Rabi / Samba (Winter)">Rabi / Samba (Winter)</option>
                <option value="Zaid / Summer">Zaid / Summer</option>
                <option value="Kuruvai (Short Term)">Kuruvai (Short Term)</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label" for="input-area">
                <span>Farm Area</span>
                <span class="form-unit">Acres</span>
              </label>
              <input id="input-area" v-model.number="form.farm_area" type="number" step="0.5" min="0.1" class="form-control" required />
            </div>
          </div>

          <!-- Soil Nutrients (NPK) -->
          <h4 class="sub-heading mt-2"><i class="fa-solid fa-seedling"></i> Soil Macro-Nutrients</h4>
          <div class="grid-cols-3">
            <div class="form-group">
              <label class="form-label" for="input-n">
                <span>Nitrogen (N)</span>
                <span class="form-unit">kg/ha</span>
              </label>
              <input id="input-n" v-model.number="form.nitrogen" type="number" step="1" min="0" max="300" class="form-control" placeholder="0 - 200" required />
            </div>

            <div class="form-group">
              <label class="form-label" for="input-p">
                <span>Phosphorus (P)</span>
                <span class="form-unit">kg/ha</span>
              </label>
              <input id="input-p" v-model.number="form.phosphorus" type="number" step="1" min="0" max="300" class="form-control" placeholder="0 - 200" required />
            </div>

            <div class="form-group">
              <label class="form-label" for="input-k">
                <span>Potassium (K)</span>
                <span class="form-unit">kg/ha</span>
              </label>
              <input id="input-k" v-model.number="form.potassium" type="number" step="1" min="0" max="300" class="form-control" placeholder="0 - 250" required />
            </div>
          </div>

          <!-- Environmental & pH -->
          <h4 class="sub-heading mt-2"><i class="fa-solid fa-cloud-sun-rain"></i> Environmental & Soil Chemistry</h4>
          <div class="grid-cols-4">
            <div class="form-group">
              <label class="form-label" for="input-temp">
                <span>Temperature</span>
                <span class="form-unit">°C</span>
              </label>
              <input id="input-temp" v-model.number="form.temperature" type="number" step="0.1" min="5" max="55" class="form-control" placeholder="e.g. 26.5" required />
            </div>

            <div class="form-group">
              <label class="form-label" for="input-hum">
                <span>Humidity</span>
                <span class="form-unit">%</span>
              </label>
              <input id="input-hum" v-model.number="form.humidity" type="number" step="0.1" min="10" max="100" class="form-control" placeholder="e.g. 75" required />
            </div>

            <div class="form-group">
              <label class="form-label" for="input-ph">
                <span>Soil pH</span>
                <span class="form-unit">0 - 14</span>
              </label>
              <input id="input-ph" v-model.number="form.ph" type="number" step="0.1" min="3.0" max="10.0" class="form-control" placeholder="e.g. 6.5" required />
            </div>

            <div class="form-group">
              <label class="form-label" for="input-rain">
                <span>Rainfall</span>
                <span class="form-unit">mm</span>
              </label>
              <input id="input-rain" v-model.number="form.rainfall" type="number" step="1" min="5" max="1000" class="form-control" placeholder="e.g. 180" required />
            </div>
          </div>

          <div v-if="weatherSourceNotice" class="weather-notice animate-fade-in">
            <i class="fa-solid fa-circle-info"></i> {{ weatherSourceNotice }}
          </div>

          <button type="submit" class="btn-primary w-100 btn-submit-pred" :disabled="loading" id="btn-predict-submit">
            <span v-if="loading"><i class="fa-solid fa-spinner fa-spin"></i> Processing ML Random Forest Model...</span>
            <span v-else><i class="fa-solid fa-wand-magic-sparkles"></i> Predict Recommended Crop</span>
          </button>
        </form>
      </div>

      <!-- Live Prediction Result Card -->
      <div v-if="predictionResult" class="result-card-col animate-fade-in" id="section-prediction-result">
        <div class="prediction-result-card glass-panel pulse-glow">
          <div class="result-header">
            <span class="badge-tag badge-green"><i class="fa-solid fa-check"></i> ML Model Recommendation</span>
            <span class="model-tag">Random Forest (100 Trees)</span>
          </div>

          <div class="result-hero-crop">
            <div class="crop-avatar-circle">
              <span class="crop-big-emoji">{{ getCropEmoji(predictionResult.recommended_crop) }}</span>
            </div>
            <div class="crop-hero-info">
              <span class="rec-label-tiny">Optimal Crop Selection</span>
              <h2 class="rec-crop-name" id="text-recommended-crop">{{ predictionResult.recommended_crop }}</h2>
              <p class="rec-sub-info">Suited for {{ form.district }} in {{ form.season }} season</p>
            </div>
            <div class="confidence-circle" id="badge-confidence-score">
              <span class="conf-digit">{{ predictionResult.confidence }}%</span>
              <span class="conf-lbl">Confidence</span>
            </div>
          </div>

          <!-- Top-3 Alternative Predictions -->
          <div class="alternatives-box">
            <h4><i class="fa-solid fa-chart-simple"></i> Top Crop Probabilities</h4>
            <div class="alt-list">
              <div v-for="rec in predictionResult.top_recommendations" :key="rec.crop" class="alt-item">
                <div class="alt-crop-name">
                  <span>{{ getCropEmoji(rec.crop) }} {{ rec.crop }}</span>
                  <strong>{{ rec.confidence }}%</strong>
                </div>
                <div class="progress-track-alt">
                  <div class="progress-fill-alt" :style="{ width: rec.confidence + '%' }"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Explainable AI Section -->
          <div class="explanation-box">
            <h4><i class="fa-solid fa-lightbulb"></i> Explainable AI Agronomic Reasoning</h4>
            <ul class="reasoning-list">
              <li v-for="(point, idx) in predictionResult.explanation_points" :key="idx">
                <i class="fa-solid fa-circle-check text-green"></i>
                <span>{{ point }}</span>
              </li>
            </ul>
          </div>

          <!-- Action Buttons (Save & PDF Report) -->
          <div class="result-actions-footer">
            <button @click="savePrediction" class="btn-secondary flex-1" :disabled="isSaved" id="btn-save-recommendation">
              <i class="fa-solid fa-bookmark"></i> {{ isSaved ? 'Saved to Bookmarks' : 'Save Recommendation' }}
            </button>
            <a :href="'/api/predictions/' + predictionResult.prediction_id + '/report'" target="_blank" class="btn-primary flex-1" id="btn-generate-report">
              <i class="fa-solid fa-file-pdf"></i> Generate PDF Report
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'RecommendView',
  data() {
    return {
      form: {
        district: 'Madurai',
        state: 'Tamil Nadu',
        season: 'Kharif (Monsoon)',
        farm_area: 2.5,
        nitrogen: 80,
        phosphorus: 45,
        potassium: 40,
        temperature: 24.5,
        humidity: 82.0,
        ph: 6.5,
        rainfall: 210.0
      },
      districts: [
        'Madurai', 'Coimbatore', 'Thanjavur', 'Tiruchirappalli', 'Salem',
        'Chennai', 'Tirunelveli', 'Erode', 'Dindigul', 'Vellore',
        'Cuddalore', 'Kanchipuram', 'Kanyakumari', 'Namakkal', 'Nilgiris',
        'Perambalur', 'Pudukkottai', 'Ramanathapuram', 'Sivaganga', 'Tenkasi',
        'Theni', 'Thoothukudi', 'Tiruppur', 'Tiruvarur', 'Viluppuram', 'Virudhunagar'
      ],
      loading: false,
      predictionResult: null,
      isSaved: false,
      weatherSourceNotice: ''
    }
  },
  mounted() {
    const userStr = localStorage.getItem('ai_farmer_user')
    if (userStr) {
      const u = JSON.parse(userStr)
      if (u.district) this.form.district = u.district
      if (u.farm_area) this.form.farm_area = u.farm_area
    }
  },
  methods: {
    applyPreset(type) {
      if (type === 'rice') {
        this.form.nitrogen = 90
        this.form.phosphorus = 42
        this.form.potassium = 43
        this.form.temperature = 23.5
        this.form.humidity = 82.0
        this.form.ph = 6.5
        this.form.rainfall = 220.0
        this.form.district = 'Thanjavur'
      } else if (type === 'cotton') {
        this.form.nitrogen = 120
        this.form.phosphorus = 45
        this.form.potassium = 20
        this.form.temperature = 24.0
        this.form.humidity = 80.0
        this.form.ph = 6.9
        this.form.rainfall = 80.0
        this.form.district = 'Madurai'
      } else if (type === 'maize') {
        this.form.nitrogen = 78
        this.form.phosphorus = 48
        this.form.potassium = 20
        this.form.temperature = 22.5
        this.form.humidity = 65.0
        this.form.ph = 6.3
        this.form.rainfall = 85.0
        this.form.district = 'Coimbatore'
      } else if (type === 'banana') {
        this.form.nitrogen = 100
        this.form.phosphorus = 82
        this.form.potassium = 50
        this.form.temperature = 27.5
        this.form.humidity = 80.0
        this.form.ph = 6.0
        this.form.rainfall = 105.0
        this.form.district = 'Tiruchirappalli'
      } else if (type === 'coffee') {
        this.form.nitrogen = 101
        this.form.phosphorus = 29
        this.form.potassium = 30
        this.form.temperature = 25.5
        this.form.humidity = 59.0
        this.form.ph = 6.8
        this.form.rainfall = 160.0
        this.form.district = 'Nilgiris'
      }
    },
    async fetchDistrictWeather() {
      try {
        const resp = await api.getWeather(this.form.district)
        if (resp.data.success && resp.data.weather) {
          const w = resp.data.weather
          this.form.temperature = w.temperature
          this.form.humidity = w.humidity
          this.form.rainfall = w.rainfall
          this.weatherSourceNotice = `Weather updated for ${w.district} (${w.source}): ${w.temperature}°C, ${w.humidity}% Hum, ${w.rainfall}mm Rain`
        }
      } catch (e) {
        console.error('Weather fetch error:', e)
      }
    },
    async submitPrediction() {
      this.loading = true
      this.isSaved = false
      try {
        const resp = await api.predictCrop(this.form)
        if (resp.data.success) {
          this.predictionResult = resp.data
          this.$nextTick(() => {
            const el = document.getElementById('section-prediction-result')
            if (el) el.scrollIntoView({ behavior: 'smooth' })
          })
        }
      } catch (err) {
        alert(err.response?.data?.message || 'Prediction failed')
      } finally {
        this.loading = false
      }
    },
    async savePrediction() {
      if (!this.predictionResult?.prediction_id) return
      try {
        await api.saveRecommendation(this.predictionResult.prediction_id)
        this.isSaved = true
      } catch (e) {
        console.error('Save error:', e)
      }
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
.recommend-container {
  padding: 2.5rem 1.5rem 4rem;
}

.page-title-banner {
  margin-bottom: 2rem;
}

.page-title-banner h1 {
  font-size: 2.2rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0.5rem 0;
}

.page-title-banner p {
  color: #64748b;
  font-size: 1rem;
}

.presets-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-wrap: wrap;
  margin-bottom: 2rem;
  background: white;
  padding: 0.75rem 1.25rem;
  border-radius: var(--radius-md);
  border: 1px solid #e2e8f0;
}

.preset-label {
  font-size: 0.82rem;
  font-weight: 700;
  color: #475569;
}

.btn-preset {
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: 9999px;
  padding: 0.35rem 0.8rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: #0f172a;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-preset:hover {
  background: #ecfdf5;
  border-color: #10b981;
  color: #059669;
}

.form-result-layout {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.form-card {
  padding: 2.25rem;
  background: white;
}

.form-section-head {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.75rem;
}

.sec-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: #ecfdf5;
  color: #059669;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
}

.form-section-head h3 {
  font-size: 1.35rem;
  font-weight: 800;
  color: #0f172a;
}

.form-section-head p {
  font-size: 0.85rem;
  color: #64748b;
}

.btn-fetch-weather {
  background: none;
  border: none;
  color: #0284c7;
  font-size: 0.75rem;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.btn-fetch-weather:hover {
  text-decoration: underline;
}

.sub-heading {
  font-size: 1.05rem;
  font-weight: 700;
  color: #1e293b;
  margin: 1.25rem 0 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.weather-notice {
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  color: #0369a1;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  font-size: 0.82rem;
  margin-bottom: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-submit-pred {
  padding: 1rem 2rem !important;
  font-size: 1.1rem !important;
  margin-top: 1.5rem;
}

/* Prediction Result Card */
.prediction-result-card {
  padding: 2.5rem;
  background: white;
  border: 2px solid #10b981;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.75rem;
}

.model-tag {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 600;
}

.result-hero-crop {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f0fdf4;
  border: 1.5px solid #a7f3d0;
  padding: 1.5rem 2rem;
  border-radius: var(--radius-md);
  margin-bottom: 2rem;
}

.crop-avatar-circle {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
}

.crop-big-emoji {
  font-size: 3.5rem;
}

.crop-hero-info {
  flex: 1;
  margin-left: 1.5rem;
}

.rec-label-tiny {
  font-size: 0.75rem;
  text-transform: uppercase;
  font-weight: 800;
  color: #059669;
  letter-spacing: 0.5px;
}

.rec-crop-name {
  font-size: 2.2rem;
  font-weight: 900;
  color: #064e3b;
  line-height: 1.1;
  margin: 0.2rem 0;
}

.rec-sub-info {
  font-size: 0.88rem;
  color: #64748b;
}

.confidence-circle {
  text-align: right;
}

.conf-digit {
  display: block;
  font-size: 2.4rem;
  font-weight: 900;
  color: #059669;
  line-height: 1;
}

.conf-lbl {
  font-size: 0.78rem;
  color: #64748b;
  font-weight: 600;
}

.alternatives-box {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: var(--radius-md);
  margin-bottom: 1.75rem;
}

.alternatives-box h4,
.explanation-box h4 {
  font-size: 1.05rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.alt-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.alt-crop-name {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  margin-bottom: 0.35rem;
}

.progress-track-alt {
  height: 8px;
  background: #e2e8f0;
  border-radius: 9999px;
  overflow: hidden;
}

.progress-fill-alt {
  height: 100%;
  background: linear-gradient(90deg, #10b981 0%, #0284c7 100%);
  border-radius: 9999px;
}

.explanation-box {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  padding: 1.5rem;
  border-radius: var(--radius-md);
  margin-bottom: 2rem;
}

.reasoning-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.reasoning-list li {
  display: flex;
  align-items: flex-start;
  gap: 0.65rem;
  font-size: 0.9rem;
  color: #334155;
  line-height: 1.5;
}

.reasoning-list i {
  margin-top: 3px;
}

.result-actions-footer {
  display: flex;
  gap: 1rem;
}

.flex-1 {
  flex: 1;
}

@media (max-width: 800px) {
  .result-hero-crop {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  .crop-hero-info {
    margin-left: 0;
  }
  .confidence-circle {
    text-align: center;
  }
  .result-actions-footer {
    flex-direction: column;
  }
}
</style>
