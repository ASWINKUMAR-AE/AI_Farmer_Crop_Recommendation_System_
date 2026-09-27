<template>
  <div class="auth-page-container">
    <div class="auth-card register-card glass-panel animate-fade-in">
      <div class="auth-header text-center">
        <div class="auth-logo-badge">
          <i class="fa-solid fa-user-plus"></i>
        </div>
        <h2>Farmer Registration</h2>
        <p>Join the AI-driven precision agriculture ecosystem</p>
      </div>

      <div v-if="errorMessage" class="alert-banner alert-error animate-fade-in">
        <i class="fa-solid fa-triangle-exclamation"></i>
        <span>{{ errorMessage }}</span>
      </div>

      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="grid-cols-2 form-grid">
          <div class="form-group">
            <label class="form-label" for="reg-fullname">Full Name *</label>
            <input
              id="reg-fullname"
              v-model="form.full_name"
              type="text"
              class="form-control"
              placeholder="e.g. Aswin Kumar"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="reg-username">Username *</label>
            <input
              id="reg-username"
              v-model="form.username"
              type="text"
              class="form-control"
              placeholder="e.g. aswin_farmer"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="reg-email">Email Address *</label>
            <input
              id="reg-email"
              v-model="form.email"
              type="email"
              class="form-control"
              placeholder="aswin@example.com"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="reg-phone">Phone Number</label>
            <input
              id="reg-phone"
              v-model="form.phone"
              type="tel"
              class="form-control"
              placeholder="+91 9876543210"
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="reg-password">Password (Min 6 chars) *</label>
            <input
              id="reg-password"
              v-model="form.password"
              type="password"
              class="form-control"
              placeholder="Create a strong password"
              minlength="6"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="reg-district">Farm District (Tamil Nadu) *</label>
            <select id="reg-district" v-model="form.district" class="form-control" required>
              <option v-for="d in districts" :key="d" :value="d">{{ d }}</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label" for="reg-farmarea">Farm Area (Acres) *</label>
            <input
              id="reg-farmarea"
              v-model.number="form.farm_area"
              type="number"
              step="0.5"
              min="0.1"
              class="form-control"
              placeholder="e.g. 4.5"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="reg-lang">Preferred Advisory Language</label>
            <select id="reg-lang" v-model="form.preferred_language" class="form-control">
              <option value="English">English</option>
              <option value="Tamil">Tamil (தமிழ்)</option>
            </select>
          </div>
        </div>

        <button type="submit" class="btn-primary w-100" :disabled="loading" id="btn-submit-register">
          <span v-if="loading"><i class="fa-solid fa-spinner fa-spin"></i> Creating Account...</span>
          <span v-else><i class="fa-solid fa-user-check"></i> Complete Farmer Registration</span>
        </button>
      </form>

      <div class="auth-footer text-center">
        <p>Already have an account? <router-link to="/login" id="link-login">Sign In</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'RegisterView',
  data() {
    return {
      form: {
        full_name: '',
        username: '',
        email: '',
        password: '',
        phone: '',
        district: 'Madurai',
        state: 'Tamil Nadu',
        farm_area: 3.5,
        preferred_language: 'English'
      },
      districts: [
        'Madurai', 'Coimbatore', 'Thanjavur', 'Tiruchirappalli', 'Salem',
        'Chennai', 'Tirunelveli', 'Erode', 'Dindigul', 'Vellore',
        'Cuddalore', 'Kanchipuram', 'Kanyakumari', 'Namakkal', 'Nilgiris',
        'Perambalur', 'Pudukkottai', 'Ramanathapuram', 'Sivaganga', 'Tenkasi',
        'Theni', 'Thoothukudi', 'Tiruppur', 'Tiruvarur', 'Viluppuram', 'Virudhunagar'
      ],
      loading: false,
      errorMessage: ''
    }
  },
  methods: {
    async handleRegister() {
      this.loading = true
      this.errorMessage = ''
      try {
        const resp = await api.register(this.form)
        if (resp.data.success) {
          localStorage.setItem('ai_farmer_token', resp.data.token)
          localStorage.setItem('ai_farmer_user', JSON.stringify(resp.data.user))
          this.$router.push('/dashboard')
        }
      } catch (err) {
        this.errorMessage = err.response?.data?.message || 'Registration failed.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.auth-page-container {
  min-height: calc(100vh - 150px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem 1.5rem;
}

.register-card {
  width: 100%;
  max-width: 680px;
  padding: 2.5rem;
  background: white;
}

.auth-logo-badge {
  width: 56px;
  height: 56px;
  background: #ecfdf5;
  color: #059669;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.6rem;
  margin: 0 auto 1rem;
  border: 1px solid #a7f3d0;
}

.auth-header h2 {
  font-size: 1.65rem;
  font-weight: 800;
  color: #0f172a;
}

.auth-header p {
  font-size: 0.88rem;
  color: #64748b;
  margin: 0.25rem 0 1.5rem;
}

.form-grid {
  gap: 1rem 1.25rem;
}

.alert-banner {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.75rem 1rem;
  border-radius: var(--radius-sm);
  font-size: 0.88rem;
  margin-bottom: 1.25rem;
}

.alert-error {
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

.w-100 {
  width: 100%;
  margin-top: 1rem;
}

.auth-footer {
  margin-top: 1.75rem;
  font-size: 0.88rem;
  color: #64748b;
}

.auth-footer a {
  color: #059669;
  font-weight: 700;
  text-decoration: none;
}
</style>
