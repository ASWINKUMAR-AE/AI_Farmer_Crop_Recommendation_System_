<template>
  <div v-if="isOpen" class="modal-backdrop" @click.self="$emit('close')">
    <div class="assistant-card glass-panel animate-fade-in">
      <div class="assistant-header">
        <div class="assistant-title">
          <div class="bot-icon">
            <i class="fa-solid fa-robot"></i>
          </div>
          <div>
            <h3>AI Agri-Advisor</h3>
            <p>Real-Time Agricultural Intelligence Assistant</p>
          </div>
        </div>
        <button class="close-btn" @click="$emit('close')" id="btn-close-assistant">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

      <!-- Chat Stream -->
      <div class="chat-body" ref="chatBody">
        <div class="chat-bubble bot-msg">
          <div class="bubble-icon"><i class="fa-solid fa-seedling"></i></div>
          <div class="bubble-content">
            <p><strong>Vanakkam & Welcome!</strong> I am your AI Crop Advisor. You can ask me:</p>
            <div class="quick-chips">
              <button @click="askPrompt('What crop is best for high rainfall and clay soil?')">🌧️ High rainfall & clay soil?</button>
              <button @click="askPrompt('Why does rice need high nitrogen?')">🌿 Why rice needs high Nitrogen?</button>
              <button @click="askPrompt('What soil pH is best for cultivation?')">🧪 Best soil pH range?</button>
              <button @click="askPrompt('What are top crops for Tamil Nadu districts?')">📍 Tamil Nadu district crops?</button>
            </div>
          </div>
        </div>

        <div v-for="(msg, index) in messages" :key="index" :class="['chat-bubble', msg.sender === 'user' ? 'user-msg' : 'bot-msg']">
          <div class="bubble-icon">
            <i :class="msg.sender === 'user' ? 'fa-solid fa-user' : 'fa-solid fa-robot'"></i>
          </div>
          <div class="bubble-content">
            <p v-html="formatMessage(msg.text)"></p>
            <span class="msg-time">{{ msg.time }}</span>
          </div>
        </div>

        <div v-if="isTyping" class="chat-bubble bot-msg">
          <div class="bubble-icon"><i class="fa-solid fa-robot"></i></div>
          <div class="bubble-content typing-indicator">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>

      <!-- Input Bar -->
      <form class="chat-footer" @submit.prevent="sendMessage">
        <input
          type="text"
          v-model="inputQuery"
          class="chat-input"
          placeholder="Ask anything about soil NPK, weather, or crop recommendations..."
          id="input-assistant-query"
        />
        <button type="submit" class="send-btn" :disabled="!inputQuery.trim()" id="btn-send-assistant">
          <i class="fa-solid fa-paper-plane"></i>
        </button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AIAssistantModal',
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close'],
  data() {
    return {
      inputQuery: '',
      isTyping: false,
      messages: []
    }
  },
  methods: {
    askPrompt(query) {
      this.inputQuery = query
      this.sendMessage()
    },
    sendMessage() {
      const q = this.inputQuery.trim()
      if (!q) return

      const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      this.messages.push({ sender: 'user', text: q, time })
      this.inputQuery = ''
      this.scrollToBottom()

      this.isTyping = true

      setTimeout(() => {
        const reply = this.generateResponse(q)
        this.messages.push({
          sender: 'bot',
          text: reply,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        })
        this.isTyping = false
        this.scrollToBottom()
      }, 600)
    },
    generateResponse(query) {
      const q = query.toLowerCase()

      if (q.includes('rice') || (q.includes('rainfall') && q.includes('high'))) {
        return "<strong>Rice Cultivation Insights:</strong><br/>• Rice thrives with heavy rainfall (200-300 mm), high relative humidity (>80%), and temperature between 22-32°C.<br/>• It requires high Nitrogen (80-100 kg/ha) and moderate Phosphorus and Potassium.<br/>• Ideal Soil: Clayey loam with high water holding capacity."
      } else if (q.includes('ph') || q.includes('soil ph') || q.includes('acid')) {
        return "<strong>Soil pH Guide:</strong><br/>• <strong>Optimal Range:</strong> 6.0 to 7.5 (Slightly acidic to neutral).<br/>• At pH 6.0-7.0, primary nutrients (Nitrogen, Phosphorus, Potassium) have maximum bioavailability.<br/>• <em>pH < 5.5:</em> Apply agricultural lime (CaCO3) to reduce acidity.<br/>• <em>pH > 8.0:</em> Apply gypsum (CaSO4) or organic compost to lower alkalinity."
      } else if (q.includes('tamil nadu') || q.includes('district') || q.includes('madurai')) {
        return "<strong>Tamil Nadu Agricultural Highlights:</strong><br/>• <strong>Thanjavur & Delta:</strong> Rice, Blackgram, Banana, Coconut (Samba & Kuruvai seasons).<br/>• <strong>Madurai & Virudhunagar:</strong> Cotton, Maize, Blackgram, Pomegranate, Groundnut.<br/>• <strong>Coimbatore & Erode:</strong> Maize, Cotton, Banana, Sugarcane.<br/>• <strong>Nilgiris:</strong> Tea, Coffee, Apple, Potato."
      } else if (q.includes('nitrogen') || q.includes('phosphorus') || q.includes('potassium') || q.includes('npk')) {
        return "<strong>NPK Nutrient Role in Crop Biology:</strong><br/>• <strong>Nitrogen (N):</strong> Stimulates chlorophyll production and vegetative leaf growth.<br/>• <strong>Phosphorus (P):</strong> Accelerates root establishment, blooming, and energy transfer (ATP).<br/>• <strong>Potassium (K):</strong> Enhances disease resistance, water regulation, and fruit starch quality."
      } else if (q.includes('cotton') || q.includes('black soil')) {
        return "<strong>Cotton Growing Guide:</strong><br/>• Prefers deep Black Cotton Soil (Vertisols) with temperature 22-30°C and rainfall 60-100 mm.<br/>• High Nitrogen (100-130 kg/ha) and balanced Potassium prevent boll shedding."
      } else if (q.includes('coffee') || q.includes('plantation')) {
        return "<strong>Coffee Cultivation Parameters:</strong><br/>• Requires altitude, shade trees, temperature 18-28°C, and rainfall 150-220 mm.<br/>• Thrives in rich friable forest loam rich in organic humus."
      } else {
        return "Based on agronomic principles, our <strong>Random Forest Classifier</strong> analyzes your 7 vital input parameters (N, P, K, Temperature, Humidity, pH, Rainfall) simultaneously to predict the crop with the highest yield probability. You can enter your soil values in the <em>Predict Crop</em> tab to get a real-time recommendation!"
      }
    },
    formatMessage(text) {
      return text.replace(/\n/g, '<br/>')
    },
    scrollToBottom() {
      this.$nextTick(() => {
        if (this.$refs.chatBody) {
          this.$refs.chatBody.scrollTop = this.$refs.chatBody.scrollHeight
        }
      })
    }
  }
}
</script>

<style scoped>
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

.assistant-card {
  width: 100%;
  max-width: 580px;
  height: 600px;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.assistant-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, #064e3b 0%, #059669 100%);
  color: white;
}

.assistant-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.bot-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.assistant-title h3 {
  font-size: 1.15rem;
  font-weight: 700;
}

.assistant-title p {
  font-size: 0.75rem;
  opacity: 0.9;
}

.close-btn {
  background: rgba(255, 255, 255, 0.15);
  border: none;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.chat-body {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background: #f8fafc;
}

.chat-bubble {
  display: flex;
  gap: 0.6rem;
  max-width: 85%;
}

.bot-msg {
  align-self: flex-start;
}

.user-msg {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.bubble-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  flex-shrink: 0;
}

.bot-msg .bubble-icon {
  background: #ecfdf5;
  color: #059669;
  border: 1px solid #a7f3d0;
}

.user-msg .bubble-icon {
  background: #0284c7;
  color: white;
}

.bubble-content {
  padding: 0.85rem 1.1rem;
  border-radius: 14px;
  font-size: 0.88rem;
  line-height: 1.5;
}

.bot-msg .bubble-content {
  background: white;
  color: #1e293b;
  border: 1px solid #e2e8f0;
  border-top-left-radius: 4px;
}

.user-msg .bubble-content {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border-top-right-radius: 4px;
}

.msg-time {
  display: block;
  font-size: 0.65rem;
  margin-top: 0.3rem;
  opacity: 0.7;
}

.quick-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-top: 0.75rem;
}

.quick-chips button {
  background: #ecfdf5;
  color: #064e3b;
  border: 1px solid #a7f3d0;
  border-radius: 9999px;
  padding: 0.3rem 0.65rem;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.quick-chips button:hover {
  background: #10b981;
  color: white;
}

.chat-footer {
  display: flex;
  gap: 0.6rem;
  padding: 1rem 1.25rem;
  background: white;
  border-top: 1px solid #e2e8f0;
}

.chat-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1.5px solid #cbd5e1;
  border-radius: 9999px;
  font-size: 0.9rem;
  outline: none;
}

.chat-input:focus {
  border-color: #10b981;
}

.send-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.typing-indicator span {
  display: inline-block;
  width: 6px;
  height: 6px;
  background: #94a3b8;
  border-radius: 50%;
  margin-right: 3px;
  animation: typing 1s infinite alternate;
}

@keyframes typing {
  from { opacity: 0.2; transform: translateY(0); }
  to { opacity: 1; transform: translateY(-4px); }
}
</style>
