<template>
  <header class="navbar-wrapper">
    <div class="container navbar-content">
      <!-- Logo -->
      <router-link to="/" class="brand-logo" id="nav-brand">
        <div class="brand-icon">
          <i class="fa-solid fa-wheat-awn"></i>
        </div>
        <div class="brand-text">
          <span class="brand-title">AI FARMER</span>
          <span class="brand-badge">ML ADVISORY</span>
        </div>
      </router-link>

      <!-- Navigation Links -->
      <nav class="nav-menu" :class="{ 'nav-open': isMobileMenuOpen }">
        <router-link to="/" class="nav-item" active-class="nav-active" id="nav-home" @click="closeMobile">
          <i class="fa-solid fa-house"></i> Home
        </router-link>
        
        <router-link to="/crops" class="nav-item" active-class="nav-active" id="nav-crops" @click="closeMobile">
          <i class="fa-solid fa-seedling"></i> Crops Guide
        </router-link>

        <template v-if="isAuthenticated && isFarmer">
          <router-link to="/dashboard" class="nav-item" active-class="nav-active" id="nav-dashboard" @click="closeMobile">
            <i class="fa-solid fa-table-columns"></i> Dashboard
          </router-link>
          <router-link to="/recommend" class="nav-item" active-class="nav-active" id="nav-recommend" @click="closeMobile">
            <i class="fa-solid fa-wand-magic-sparkles"></i> Predict Crop
          </router-link>
          <router-link to="/history" class="nav-item" active-class="nav-active" id="nav-history" @click="closeMobile">
            <i class="fa-solid fa-clock-rotate-left"></i> History
          </router-link>
        </template>

        <template v-if="isAuthenticated && isAdmin">
          <router-link to="/admin" class="nav-item" active-class="nav-active" id="nav-admin" @click="closeMobile">
            <i class="fa-solid fa-chart-line"></i> Admin Dashboard
          </router-link>
          <router-link to="/admin/model" class="nav-item" active-class="nav-active" id="nav-admin-model" @click="closeMobile">
            <i class="fa-solid fa-brain"></i> Model Metrics
          </router-link>
          <router-link to="/admin/documentation" class="nav-item" active-class="nav-active" id="nav-admin-docs" @click="closeMobile">
            <i class="fa-solid fa-file-lines"></i> Reports & Docs
          </router-link>
        </template>

        <!-- AI Assistant Trigger Button -->
        <button class="nav-assistant-btn" @click="$emit('open-assistant')" id="btn-open-assistant" title="Ask AI Farm Advisor">
          <i class="fa-solid fa-robot"></i> Ask AI Advisor
        </button>
      </nav>

      <!-- User Auth Section -->
      <div class="nav-auth">
        <template v-if="isAuthenticated">
          <div class="user-dropdown">
            <router-link to="/profile" class="user-pill" id="nav-profile">
              <div class="user-avatar">
                <i :class="isAdmin ? 'fa-solid fa-user-shield' : 'fa-solid fa-user-gear'"></i>
              </div>
              <div class="user-info-text">
                <span class="user-name">{{ currentUser?.full_name || currentUser?.username }}</span>
                <span class="user-role">{{ isAdmin ? 'Admin' : 'Farmer' }}</span>
              </div>
            </router-link>
            <button class="logout-btn" @click="handleLogout" id="btn-logout" title="Logout">
              <i class="fa-solid fa-arrow-right-from-bracket"></i>
            </button>
          </div>
        </template>
        <template v-else>
          <div class="auth-buttons">
            <router-link to="/login" class="btn-secondary btn-sm" id="nav-login">
              <i class="fa-solid fa-right-to-bracket"></i> Login
            </router-link>
            <router-link to="/register" class="btn-primary btn-sm" id="nav-register">
              <i class="fa-solid fa-user-plus"></i> Register
            </router-link>
          </div>
        </template>

        <!-- Mobile Toggle -->
        <button class="mobile-toggle" @click="isMobileMenuOpen = !isMobileMenuOpen" id="btn-mobile-toggle">
          <i :class="isMobileMenuOpen ? 'fa-solid fa-xmark' : 'fa-solid fa-bars'"></i>
        </button>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Navbar',
  emits: ['open-assistant'],
  data() {
    return {
      isMobileMenuOpen: false,
      currentUser: null
    }
  },
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('ai_farmer_token')
    },
    isAdmin() {
      return this.currentUser?.role === 'admin'
    },
    isFarmer() {
      return this.currentUser?.role === 'farmer'
    }
  },
  mounted() {
    this.loadUser()
    window.addEventListener('storage', this.loadUser)
  },
  beforeUnmount() {
    window.removeEventListener('storage', this.loadUser)
  },
  methods: {
    loadUser() {
      const userStr = localStorage.getItem('ai_farmer_user')
      if (userStr) {
        try {
          this.currentUser = JSON.parse(userStr)
        } catch (e) {
          this.currentUser = null
        }
      } else {
        this.currentUser = null
      }
    },
    closeMobile() {
      this.isMobileMenuOpen = false
    },
    handleLogout() {
      localStorage.removeItem('ai_farmer_token')
      localStorage.removeItem('ai_farmer_user')
      this.currentUser = null
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.navbar-wrapper {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(16, 185, 129, 0.15);
  box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05);
}

.navbar-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 72px;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
}

.brand-icon {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: #fff;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.35rem;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-title {
  font-size: 1.25rem;
  font-weight: 800;
  letter-spacing: -0.5px;
  background: linear-gradient(135deg, #064e3b 0%, #059669 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.brand-badge {
  font-size: 0.65rem;
  font-weight: 700;
  color: #059669;
  letter-spacing: 1px;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 0.9rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: #475569;
  text-decoration: none;
  border-radius: 10px;
  transition: all 0.2s ease;
}

.nav-item:hover {
  color: #059669;
  background: #ecfdf5;
}

.nav-active {
  color: #059669 !important;
  background: #ecfdf5 !important;
  font-weight: 700;
}

.nav-assistant-btn {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 0.9rem;
  font-size: 0.85rem;
  font-weight: 700;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
  border: 1px solid #fcd34d;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.25s ease;
}

.nav-assistant-btn:hover {
  transform: scale(1.04);
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.2);
}

.nav-auth {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.auth-buttons {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-sm {
  padding: 0.5rem 1rem !important;
  font-size: 0.85rem !important;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.user-pill {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.35rem 0.75rem 0.35rem 0.4rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 9999px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.user-pill:hover {
  border-color: #10b981;
  background: #ecfdf5;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #10b981;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
}

.user-info-text {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 0.82rem;
  font-weight: 700;
  color: #1e293b;
  max-width: 110px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 0.65rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
}

.logout-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  background: white;
  color: #ef4444;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: #fee2e2;
  border-color: #ef4444;
}

.mobile-toggle {
  display: none;
  background: none;
  border: none;
  font-size: 1.35rem;
  color: #334155;
  cursor: pointer;
}

@media (max-width: 992px) {
  .mobile-toggle {
    display: block;
  }
  .nav-menu {
    position: absolute;
    top: 72px;
    left: 0;
    width: 100%;
    background: white;
    flex-direction: column;
    padding: 1.5rem;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    display: none;
    border-bottom: 1px solid #e2e8f0;
  }
  .nav-open {
    display: flex;
  }
  .nav-item {
    width: 100%;
    padding: 0.75rem 1rem;
  }
}
</style>
