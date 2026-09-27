# AI Farmer Crop Recommendation System
**Full A–Z Artificial Intelligence & Machine Learning Project with Automated Document Generation**

---

## 🌾 Project Overview
The **AI Farmer Crop Recommendation System** is an end-to-end intelligent agricultural decision support platform. By analyzing 7 crucial agronomic parameters (**Soil Nitrogen, Phosphorus, Potassium, Soil pH, Ambient Temperature, Relative Humidity, and Rainfall**), the system utilizes an authentic trained **Random Forest Classifier (100 Decision Trees)** to recommend the highest yielding crop species with confidence probability distributions, top alternative crops, and explainable agronomic reasoning.

---

## 🚀 Key Features

1. **Farmer Module:**
   - Secure Registration & JWT Authentication
   - Profile & Land Size Management (Acres)
   - Analytical Soil Chemistry & Meteorological Telemetry Input
   - Live District Meteorological Fetching (Tamil Nadu districts & Pan-India)
   - Instant AI Crop Prediction with Confidence Score & Top-3 Alternatives
   - Explainable AI (XAI) Agronomic Reasoning Breakdown
   - Bookmark & Saved Recommendations Manager
   - Downloadable PDF Crop Advisory Certificates

2. **Crop Knowledge Base:**
   - 22 Supported Agricultural Crop Species
   - Empirical Soil, Climate, and Cultivation Guides
   - Dynamic Category Filtering (Cereals, Pulses, Fruits, Fibers, Plantation)

3. **Admin Control Center:**
   - High-Level KPI Metric Counters
   - Visual Analytics powered by Chart.js (Crop Popularity & Regional Adoption)
   - Global Prediction Audit Logs & Registered Farmer Management
   - Real ML Evaluation Metrics Viewer (Accuracy, Precision, Recall, F1-Score, Confusion Matrix, Feature Importance)
   - One-Click Model Retraining Engine
   - One-Click Project Documentation & Lab Report Generator (.DOCX / .PDF)

4. **AI Agricultural Advisor:**
   - Built-in interactive assistant for farmer queries on soil fertilizers, pH balancing, and climate suitability.

---

## 🛠️ Technology Stack

- **Frontend:** Vue 3, Vite, JavaScript, Vue Router, Axios, Chart.js, Vanilla Modern CSS (Glassmorphism & Emerald Theme)
- **Backend:** Python 3.12, Flask, Flask-CORS, PyJWT, ReportLab, python-docx, docx2pdf
- **Machine Learning:** Scikit-Learn, Pandas, NumPy, Joblib, Random Forest Classifier (100 Estimators)
- **Database:** MySQL (XAMPP default port 3306), PyMySQL Connector
- **Automated Testing & Captures:** Playwright Browser Automation

---

## 📊 Machine Learning Model Performance

| Metric | Measured Value | Description |
| :--- | :--- | :--- |
| **Model Algorithm** | **Random Forest Classifier** | 100 Decision Trees, Entropy Criterion |
| **Dataset Records** | **2,200 Benchmark Samples** | 22 Unique Crop Classes (100 each) |
| **Overall Accuracy** | **98.64%** | Stratified 80:20 Train-Test Split |
| **Precision (Weighted)** | **98.67%** | True positive classification ratio |
| **Recall (Weighted)** | **98.64%** | Sensitivity index |
| **F1-Score (Weighted)**| **98.63%** | Harmonic mean of precision and recall |

### Feature Importance Gini Breakdown:
- **Relative Humidity:** 21.51%
- **Seasonal Rainfall:** 18.97%
- **Potassium (K):** 18.31%
- **Nitrogen (N):** 17.18%
- **Phosphorus (P):** 15.06%
- **Air Temperature:** 5.93%
- **Soil pH Level:** 3.03%

---

## 📂 Project Directory Structure

```
AI_FARMER_CROP_RECOMMENDATION_SYSTEM/
├── dataset/
│   ├── Crop_recommendation.csv           # 2,200 Agricultural Records
│   ├── generate_dataset.py               # Dataset Generator & Benchmark Validator
│   └── dataset_metadata.json             # Dataset Profile & Feature Definitions
├── models/
│   ├── crop_recommendation_model.pkl     # Trained Random Forest Model Artifact
│   └── model_metrics.json                # Statistical Evaluations & Confusion Matrix
├── backend/
│   ├── app.py                            # Flask API Application Server (Port 5000)
│   ├── config.py                         # Environment & MySQL Database Settings
│   ├── db.py                             # PyMySQL Connector & Query Helpers
│   ├── init_db.py                        # Automated Database Schema Creation & Seeder
│   ├── ml_pipeline.py                    # Model Training, Evaluation & Prediction API
│   ├── routes/
│   │   ├── auth_routes.py                # Register, Login, JWT Token Issuance
│   │   ├── farmer_routes.py              # Prediction, History, Bookmarks, PDF Reports
│   │   ├── crop_routes.py                # Crop Catalog, Districts & Weather Feeds
│   │   └── admin_routes.py               # Analytics, Retraining & Documentation Generator
│   ├── utils/
│   │   ├── auth_middleware.py            # JWT Route Decorators
│   │   ├── weather_service.py            # Meteorological Weather Integration
│   │   ├── report_generator.py           # ReportLab PDF Advisory Generator
│   │   └── doc_generator.py              # Project Documentation Generator (.DOCX)
│   └── requirements.txt                  # Python Dependencies
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── main.js
│       ├── App.vue
│       ├── router/index.js               # Route Guards & Role Authorization
│       ├── services/api.js               # Axios API Client with JWT Interceptors
│       ├── assets/style.css              # Custom Glassmorphic Agricultural Theme
│       ├── components/
│       │   ├── Navbar.vue
│       │   ├── Footer.vue
│       │   └── AIAssistantModal.vue      # AI Agri-Advisor Chatbot
│       └── views/
│           ├── HomeView.vue
│           ├── LoginView.vue
│           ├── RegisterView.vue
│           ├── FarmerDashboard.vue
│           ├── RecommendView.vue
│           ├── HistoryView.vue
│           ├── CropInfoView.vue
│           ├── ProfileView.vue
│           ├── AdminDashboard.vue
│           ├── AdminModelMetrics.vue
│           └── AdminDocGenerator.vue
├── screenshots/                          # 14 Full-Resolution Live Captured Screenshots
├── reports/                              # Generated PDF Crop Reports
├── capture_all_screens.py                # Playwright E2E Automation Script
├── generate_report_docx.py               # College Lab Report Word Document Compiler
├── AI_Farmer_Crop_Recommendation_System_Report.docx # Official Word Document
├── AI_Farmer_Crop_Recommendation_System_Report.pdf  # Official PDF Document
└── README.md
```

---

## ⚡ Setup & Execution Instructions

### 1. Database Setup (XAMPP MySQL)
1. Start **Apache** and **MySQL** in XAMPP Control Panel.
2. Initialize the database and seed reference tables:
   ```bash
   py -3.12 backend/init_db.py
   ```

### 2. Backend Server
```bash
py -3.12 backend/app.py
```
*Flask API will start on: `http://127.0.0.1:5000`*

### 3. Frontend Application
```bash
cd frontend
npm install
npm run dev
```
*Frontend interface will start on: `http://localhost:5173`*

---

## 🔑 Default Credentials
- **Farmer Account:** `aswin` / `farmer123`
- **Admin Account:** `admin` / `admin123`

---

## 📄 Academic Project Details
- **Institution:** Velammal College of Engineering and Technology (Autonomous), Madurai - 625009
- **Department:** Department of Computer Science and Engineering
- **Team Members:**
  - **Kevin Lawrence** (Register No: `913124104065`, Roll No: `24CSEA47`)
  - **Kishore** (Register No: `913124104067`, Roll No: `24CSEA48`)
  - **Sindhan** (Register No: `913124104150`, Roll No: `24CSEA61`)
- **Academic Year:** 2025–26
- **Course:** 21CS410-Artificial Intelligence & Machine Learning Laboratory
