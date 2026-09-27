<template>
  <div class="profile-container container">
    <div class="profile-card glass-panel animate-fade-in">
      <div class="profile-header">
        <div class="profile-avatar-large">
          <i class="fa-solid fa-user-gear"></i>
        </div>
        <div>
          <h2>Farmer Profile Settings</h2>
          <p>Manage your agricultural land holdings, regional location, and contact parameters</p>
        </div>
      </div>

      <div v-if="successMsg" class="alert-banner alert-success animate-fade-in">
        <i class="fa-solid fa-circle-check"></i>
        <span>{{ successMsg }}</span>
      </div>

      <form @submit.prevent="saveProfile" class="profile-form">
        <div class="grid-cols-2">
          <div class="form-group">
            <label class="form-label">Full Name</label>
            <input type="text" v-model="profile.full_name" class="form-control" required />
          </div>

          <div class="form-group">
            <label class="form-label">Username (Read Only)</label>
            <input type="text" :value="profile.username" class="form-control" disabled />
          </div>

          <div class="form-group">
            <label class="form-label">Email Address (Read Only)</label>
            <input type="email" :value="profile.email" class="form-control" disabled />
          </div>

          <div class="form-group">
            <label class="form-label">Contact Phone</label>
            <input type="tel" v-model="profile.phone" class="form-control" placeholder="+91 9876543210" />
          </div>

          <div class="form-group">
            <label class="form-label">District (Tamil Nadu)</label>
            <select v-model="profile.district" class="form-control" required>
              <option v-for="d in districts" :key="d" :value="d">{{ d }}</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">State</label>
            <input type="text" v-model="profile.state" class="form-control" required />
          </div>

          <div class="form-group">
            <label class="form-label">Farm Area (Acres)</label>
            <input type="number" step="0.5" min="0.1" v-model.number="profile.farm_area" class="form-control" required />
          </div>

          <div class="form-group">
            <label class="form-label">Preferred Advisory Language</label>
            <select v-model="profile.preferred_language" class="form-control">
              <option value="English">English</option>
              <option value="Tamil">Tamil (தமிழ்)</option>
            </select>
          </div>
        </div>

        <div class="profile-actions mt-3">
          <button type="submit" class="btn-primary" :disabled="saving" id="btn-save-profile">
            <span v-if="saving"><i class="fa-solid fa-spinner fa-spin"></i> Saving...</span>
            <span v-else><i class="fa-solid fa-floppy-disk"></i> Update Profile</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../services/api'

export default {
  name: 'ProfileView',
  data() {
    return {
      profile: {},
      districts: [
        'Madurai', 'Coimbatore', 'Thanjavur', 'Tiruchirappalli', 'Salem',
        'Chennai', 'Tirunelveli', 'Erode', 'Dindigul', 'Vellore',
        'Cuddalore', 'Kanchipuram', 'Kanyakumari', 'Namakkal', 'Nilgiris',
        'Perambalur', 'Pudukkottai', 'Ramanathapuram', 'Sivaganga', 'Tenkasi',
        'Theni', 'Thoothukudi', 'Tiruppur', 'Tiruvarur', 'Viluppuram', 'Virudhunagar'
      ],
      saving: false,
      successMsg: ''
    }
  },
  async mounted() {
    try {
      const resp = await api.getProfile()
      if (resp.data.success) {
        this.profile = resp.data.profile || {}
      }
    } catch (e) {
      console.error('Profile fetch error:', e)
    }
  },
  methods: {
    async saveProfile() {
      this.saving = true
      this.successMsg = ''
      try {
        const resp = await api.updateProfile(this.profile)
        if (resp.data.success) {
          this.successMsg = 'Profile updated successfully!'
          // Update localstorage user
          const uStr = localStorage.getItem('ai_farmer_user')
          if (uStr) {
            const u = JSON.parse(uStr)
            u.full_name = this.profile.full_name
            u.district = this.profile.district
            u.farm_area = this.profile.farm_area
            localStorage.setItem('ai_farmer_user', JSON.stringify(u))
          }
        }
      } catch (e) {
        console.error('Profile save error:', e)
      } finally {
        this.saving = false
      }
    }
  }
}
</script>

<style scoped>
.profile-container {
  padding: 3rem 1.5rem;
  max-width: 800px;
}

.profile-card {
  padding: 2.5rem;
  background: white;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.profile-avatar-large {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
}

.profile-header h2 {
  font-size: 1.6rem;
  font-weight: 800;
  color: #0f172a;
}

.profile-header p {
  font-size: 0.88rem;
  color: #64748b;
}

.alert-success {
  background: #ecfdf5;
  color: #064e3b;
  border: 1px solid #a7f3d0;
  padding: 0.75rem 1rem;
  border-radius: var(--radius-sm);
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
</style>
