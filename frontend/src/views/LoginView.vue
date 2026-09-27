<template>
  <div class="auth-page-container">
    <div class="auth-card glass-panel animate-fade-in">
      <div class="auth-header text-center">
        <div class="auth-logo-badge">
          <i class="fa-solid fa-wheat-awn"></i>
        </div>
        <h2>Sign In to AI Farmer</h2>
        <p>Access your precision agricultural advisory and crop prediction history</p>
      </div>

      <!-- Quick Role Toggle Demo Buttons -->
      <div class="demo-accounts-box">
        <span class="demo-title"><i class="fa-solid fa-key"></i> Quick Demo Fill:</span>
        <div class="demo-buttons">
          <button type="button" @click="fillFarmer" class="btn-demo-pill" id="btn-demo-farmer">
            <i class="fa-solid fa-user-tag"></i> Farmer (aswin)
          </button>
          <button type="button" @click="fillAdmin" class="btn-demo-pill" id="btn-demo-admin">
            <i class="fa-solid fa-user-shield"></i> Admin (admin)
          </button>
        </div>
      </div>

      <div v-if="errorMessage" class="alert-banner alert-error animate-fade-in">
        <i class="fa-solid fa-triangle-exclamation"></i>
        <span>{{ errorMessage }}</span>
      </div>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label class="form-label" for="username">
            <span>Username or Email</span>
          </label>
          <input
            id="username"
            v-model="username"
            type="text"
            class="form-control"
            placeholder="Enter username (e.g., aswin)"
            required
          />
        </div>

        <div class="form-group">
          <label class="form-label" for="password">
            <span>Password</span>
          </label>
          <input
            id="password"
            v-model="password"
            type="password"
            class="form-control"
            placeholder="Enter password (e.g., farmer123)"
            required
          />
        </div>

        <button type="submit" class="btn-primary w-100" :disabled="loading" id="btn-submit-login">
          <span v-if="loading"><i class="fa-solid fa-spinner fa-spin"></i> Authenticating...</span>
          <span v-else><i class="fa-solid fa-right-to-bracket"></i> Login to Dashboard</span>
        </button>
      </form>

      <div class="auth-footer text-center">
        <p>Don't have a farmer account? <router-link to="/register" id="link-register">Register as Farmer</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'LoginView',
  data() {
    return {
      username: '',
      password: '',
      loading: false,
      errorMessage: ''
    }
  },
  methods: {
    fillFarmer() {
      this.username = 'aswin'
      this.password = 'farmer123'
      this.errorMessage = ''
    },
    fillAdmin() {
      this.username = 'admin'
      this.password = 'admin123'
      this.errorMessage = ''
    },
    async handleLogin() {
      this.loading = true
      this.errorMessage = ''
      try {
        const resp = await api.login({
          username: this.username,
          password: this.password
        })

        if (resp.data.success) {
          localStorage.setItem('ai_farmer_token', resp.data.token)
          localStorage.setItem('ai_farmer_user', JSON.stringify(resp.data.user))

          // Redirect based on role
          if (resp.data.user.role === 'admin') {
            this.$router.push('/admin')
          } else {
            this.$router.push('/dashboard')
          }
        }
      } catch (err) {
        this.errorMessage = err.response?.data?.message || 'Login failed. Please check credentials.'
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

.auth-card {
  width: 100%;
  max-width: 480px;
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
  margin-top: 0.25rem;
}

.demo-accounts-box {
  background: #f8fafc;
  border: 1px dashed #cbd5e1;
  border-radius: var(--radius-sm);
  padding: 0.75rem 1rem;
  margin: 1.5rem 0;
}

.demo-title {
  display: block;
  font-size: 0.75rem;
  font-weight: 700;
  color: #475569;
  margin-bottom: 0.4rem;
}

.demo-buttons {
  display: flex;
  gap: 0.5rem;
}

.btn-demo-pill {
  flex: 1;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 0.4rem 0.6rem;
  font-size: 0.78rem;
  font-weight: 600;
  color: #059669;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  transition: all 0.2s;
}

.btn-demo-pill:hover {
  border-color: #10b981;
  background: #ecfdf5;
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
  margin-top: 0.5rem;
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
