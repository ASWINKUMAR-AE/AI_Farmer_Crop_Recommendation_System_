import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import FarmerDashboard from '../views/FarmerDashboard.vue'
import RecommendView from '../views/RecommendView.vue'
import HistoryView from '../views/HistoryView.vue'
import CropInfoView from '../views/CropInfoView.vue'
import ProfileView from '../views/ProfileView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import AdminModelMetrics from '../views/AdminModelMetrics.vue'
import AdminDocGenerator from '../views/AdminDocGenerator.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView
  },
  {
    path: '/dashboard',
    name: 'FarmerDashboard',
    component: FarmerDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/recommend',
    name: 'Recommend',
    component: RecommendView,
    meta: { requiresAuth: true }
  },
  {
    path: '/history',
    name: 'History',
    component: HistoryView,
    meta: { requiresAuth: true }
  },
  {
    path: '/crops',
    name: 'CropInfo',
    component: CropInfoView
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileView,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/model',
    name: 'AdminModelMetrics',
    component: AdminModelMetrics,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/documentation',
    name: 'AdminDocGenerator',
    component: AdminDocGenerator,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

// Navigation Guards
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('ai_farmer_token')
  const userStr = localStorage.getItem('ai_farmer_user')
  let user = null
  try {
    user = userStr ? JSON.parse(userStr) : null
  } catch (e) {
    user = null
  }

  if (to.meta.requiresAuth && !token) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.meta.requiresAdmin && (!user || user.role !== 'admin')) {
    next({ name: 'FarmerDashboard' })
  } else {
    next()
  }
})

export default router
