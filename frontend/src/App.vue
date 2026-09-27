<template>
  <div id="ai-farmer-app" class="app-layout">
    <Navbar @open-assistant="showAssistant = true" />
    <main class="main-body">
      <router-view />
    </main>
    <Footer />
    <AIAssistantModal :isOpen="showAssistant" @close="showAssistant = false" />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
import AIAssistantModal from './components/AIAssistantModal.vue'

export default {
  name: 'App',
  components: {
    Navbar,
    Footer,
    AIAssistantModal
  },
  data() {
    return {
      showAssistant: false
    }
  }
}
</script>

<style>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-body {
  flex: 1;
}
</style>
