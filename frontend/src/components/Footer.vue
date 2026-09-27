<template>
  <footer class="app-footer">
    <div class="container footer-content">
      <div class="footer-top">
        <div class="footer-brand">
          <div class="footer-logo">
            <i class="fa-solid fa-wheat-awn"></i>
            <span>AI FARMER</span>
          </div>
          <p class="footer-desc">
            Precision Agricultural Decision Support System powered by Ensemble Machine Learning. 
            Empowering modern farmers with scientific soil, weather, and crop intelligence.
          </p>
        </div>

        <div class="footer-links-group">
          <h4>Quick Navigation</h4>
          <ul>
            <li><router-link to="/">Home Platform</router-link></li>
            <li><router-link to="/crops">Crop Knowledge Base</router-link></li>
            <li><router-link to="/recommend">AI Crop Predictor</router-link></li>
            <li><router-link to="/history">Prediction Records</router-link></li>
          </ul>
        </div>

        <div class="footer-academic">
          <h4>Academic Mini Project</h4>
          <p class="academic-inst">
            <strong>Velammal College of Engineering and Technology</strong><br/>
            (Autonomous) — Madurai - 625009
          </p>
          <p class="academic-dept">Department of Computer Science and Engineering</p>
          <div class="student-tag">
            <i class="fa-solid fa-users"></i>
            <span>Team: <strong>KEVIN LAWRENCE (913124104065), KISHORE (913124104067), SINDHAN (913124104150)</strong></span>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <p>© 2025-2026 AI Farmer Crop Recommendation System. All rights reserved.</p>
        <p class="model-badge-foot">
          <i class="fa-solid fa-microchip"></i> Random Forest Classifier (98.64% Accuracy)
        </p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
.app-footer {
  background: #0f172a;
  color: #94a3b8;
  padding: 3.5rem 0 1.5rem;
  margin-top: 5rem;
  border-top: 1px solid #1e293b;
}

.footer-top {
  display: grid;
  grid-template-columns: 1.5fr 1fr 1.5fr;
  gap: 3rem;
  padding-bottom: 2.5rem;
  border-bottom: 1px solid #1e293b;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 1.35rem;
  font-weight: 800;
  color: #10b981;
  margin-bottom: 0.8rem;
}

.footer-desc {
  font-size: 0.88rem;
  line-height: 1.6;
  color: #64748b;
}

.footer-links-group h4,
.footer-academic h4 {
  color: #f8fafc;
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.footer-links-group ul {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.footer-links-group a {
  color: #94a3b8;
  text-decoration: none;
  font-size: 0.88rem;
  transition: all 0.2s ease;
}

.footer-links-group a:hover {
  color: #10b981;
  padding-left: 4px;
}

.academic-inst {
  font-size: 0.88rem;
  color: #cbd5e1;
  margin-bottom: 0.4rem;
}

.academic-dept {
  font-size: 0.8rem;
  color: #94a3b8;
  margin-bottom: 0.8rem;
}

.student-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.8rem;
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: 8px;
  font-size: 0.82rem;
  color: #34d399;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1.5rem;
  font-size: 0.82rem;
  color: #64748b;
}

.model-badge-foot {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  color: #10b981;
  font-weight: 600;
}

@media (max-width: 850px) {
  .footer-top {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  .footer-bottom {
    flex-direction: column;
    gap: 0.75rem;
    text-align: center;
  }
}
</style>
