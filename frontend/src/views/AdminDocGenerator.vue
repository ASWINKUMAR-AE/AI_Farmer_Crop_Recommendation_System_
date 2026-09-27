<template>
  <div class="doc-gen-container container">
    <div class="page-title-banner">
      <div>
        <span class="badge-tag badge-green"><i class="fa-solid fa-file-invoice"></i> Documentation Generation</span>
        <h1>Project Report & Lab Documentation Generator</h1>
        <p>Export college-standard AIML mini project documentation compiled with real model evaluation parameters</p>
      </div>

      <div class="export-actions">
        <a href="/api/admin/generate-docs?format=docx" class="btn-primary" id="btn-download-docx">
          <i class="fa-solid fa-file-word"></i> Download Report (DOCX)
        </a>
      </div>
    </div>

    <!-- Document Layout Preview Sheet -->
    <div class="doc-preview-sheet glass-panel animate-fade-in" id="card-doc-preview">
      <!-- Title Page Section -->
      <div class="doc-page-header text-center">
        <h2>AI FARMER CROP RECOMMENDATION SYSTEM</h2>
        <h4 class="text-green font-bold">MINI PROJECT — AIML LABORATORY REPORT</h4>
        <p class="doc-dept-txt">
          Department of Computer Science and Engineering<br/>
          <strong>VELAMMAL COLLEGE OF ENGINEERING AND TECHNOLOGY</strong><br/>
          VIRAGANOOR, MADURAI - 625009 (AUTONOMOUS)<br/>
          Academic Year 2025-26
        </p>
        <div class="student-box-doc">
          <span>Done by:</span>
          <strong>KEVIN LAWRENCE – 913124104065 | KISHORE – 913124104067 | SINDHAN – 913124104150</strong>
        </div>
      </div>

      <hr class="doc-divider" />

      <!-- Sections Summary -->
      <div class="doc-section">
        <h3>1. AIM</h3>
        <p>
          To design and develop an end-to-end intelligent agricultural decision support system that recommends the most optimal
          and high-yielding crop species for farmers based on soil macro-nutrients (Nitrogen, Phosphorus, Potassium), soil pH,
          and meteorological parameters (Temperature, Humidity, Rainfall) utilizing an authentic trained Random Forest Classifier.
        </p>
      </div>

      <div class="doc-section">
        <h3>2. CONCEPTS INVOLVED</h3>
        <div class="grid-cols-2 doc-concepts-grid">
          <div class="concept-item">
            <strong>• Artificial Intelligence & Machine Learning:</strong>
            <p>Applied classification supervised learning on multi-dimensional agricultural features.</p>
          </div>
          <div class="concept-item">
            <strong>• Random Forest Ensemble Classification:</strong>
            <p>100 decision trees utilizing entropy splitting criterion to prevent overfitting and ensure high accuracy.</p>
          </div>
          <div class="concept-item">
            <strong>• Data Preprocessing & Feature Engineering:</strong>
            <p>Missing value verification, normalization, label encoding, and stratified 80-20 train-test splitting.</p>
          </div>
          <div class="concept-item">
            <strong>• Full-Stack REST Architecture:</strong>
            <p>Python Flask REST backend, PyMySQL connector, and Vue 3 / Vite frontend with JWT authentication.</p>
          </div>
        </div>
      </div>

      <div class="doc-section">
        <h3>3. MODEL PERFORMANCE & RESULTS</h3>
        <div class="doc-metrics-table">
          <div class="doc-metric-row">
            <span>Overall Model Accuracy:</span>
            <strong class="text-green">98.64% (Random Forest Classifier)</strong>
          </div>
          <div class="doc-metric-row">
            <span>Precision (Weighted):</span>
            <strong>98.67%</strong>
          </div>
          <div class="doc-metric-row">
            <span>Recall (Weighted):</span>
            <strong>98.64%</strong>
          </div>
          <div class="doc-metric-row">
            <span>F1-Score (Harmonic Mean):</span>
            <strong>98.63%</strong>
          </div>
          <div class="doc-metric-row">
            <span>Total Agricultural Training Samples:</span>
            <strong>2,200 Benchmark Records (22 Crop Species)</strong>
          </div>
        </div>
      </div>

      <div class="doc-section">
        <h3>4. REPORT GENERATION CAPABILITY</h3>
        <p>
          The system includes automated dynamic PDF certificate generation with unique Report IDs, agronomic reasoning breakdowns,
          and full Microsoft Word (.DOCX) report export formatted strictly according to college laboratory specifications.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminDocGenerator'
}
</script>

<style scoped>
.doc-gen-container {
  padding: 2.5rem 1.5rem 4rem;
}

.page-title-banner {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 2rem;
}

.page-title-banner h1 {
  font-size: 2.2rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0.4rem 0;
}

.doc-preview-sheet {
  background: white;
  padding: 3.5rem;
  max-width: 900px;
  margin: 0 auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
}

.doc-page-header h2 {
  font-size: 1.7rem;
  font-weight: 900;
  color: #064e3b;
  margin-bottom: 0.5rem;
}

.doc-dept-txt {
  font-size: 0.95rem;
  color: #334155;
  margin: 1.25rem 0;
  line-height: 1.6;
}

.student-box-doc {
  display: inline-block;
  background: #f0fdf4;
  border: 1px solid #a7f3d0;
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  margin-top: 1rem;
}

.student-box-doc span {
  display: block;
  font-size: 0.8rem;
  color: #64748b;
}

.student-box-doc strong {
  font-size: 1.1rem;
  color: #064e3b;
}

.doc-divider {
  border: 0;
  height: 1.5px;
  background: #e2e8f0;
  margin: 2.5rem 0;
}

.doc-section {
  margin-bottom: 2rem;
}

.doc-section h3 {
  font-size: 1.25rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.75rem;
}

.doc-section p {
  color: #475569;
  line-height: 1.65;
  font-size: 0.95rem;
}

.doc-concepts-grid {
  gap: 1.25rem;
  margin-top: 0.75rem;
}

.concept-item {
  background: #f8fafc;
  padding: 1rem;
  border-radius: 8px;
  border-left: 3px solid #10b981;
}

.concept-item strong {
  color: #0f172a;
  display: block;
  margin-bottom: 0.25rem;
}

.concept-item p {
  font-size: 0.85rem;
  margin: 0;
}

.doc-metrics-table {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 1rem 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.doc-metric-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
}

@media (max-width: 900px) {
  .page-title-banner {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  .doc-preview-sheet {
    padding: 2rem;
  }
}
</style>
