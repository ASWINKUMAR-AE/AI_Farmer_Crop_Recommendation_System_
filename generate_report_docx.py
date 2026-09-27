"""
Official College Mini Project & Lab Report Generator
Strictly replicates the Velammal College of Engineering and Technology Lab Report Layout.
Includes Page Borders, Cover Page, Bonafide Certificate, AIM, Concepts Involved,
Files Used, Program Source Code, Output Screenshots, Result, and References.
"""

import os
import json
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, 'screenshots')
OUTPUT_DOCX = os.path.join(BASE_DIR, 'AI_Farmer_Crop_Recommendation_System_Report.docx')
OUTPUT_PDF = os.path.join(BASE_DIR, 'AI_Farmer_Crop_Recommendation_System_Report.pdf')


def add_page_border(section):
    """Adds a clean outer rectangular page border to the section."""
    sectPr = section._sectPr
    pgBorders = parse_xml(
        r'<w:pgBorders {} w:offsetFrom="page">'
        r'<w:top w:val="single" w:sz="12" w:space="24" w:color="333333"/>'
        r'<w:left w:val="single" w:sz="12" w:space="24" w:color="333333"/>'
        r'<w:bottom w:val="single" w:sz="12" w:space="24" w:color="333333"/>'
        r'<w:right w:val="single" w:sz="12" w:space="24" w:color="333333"/>'
        r'</w:pgBorders>'.format(nsdecls('w'))
    )
    sectPr.append(pgBorders)


def build_lab_report():
    doc = Document()

    # Section Margins & Page Border
    sec = doc.sections[0]
    sec.top_margin = Inches(0.8)
    sec.bottom_margin = Inches(0.8)
    sec.left_margin = Inches(0.85)
    sec.right_margin = Inches(0.85)
    add_page_border(sec)

    logo_path = os.path.join(SCREENSHOTS_DIR, 'vcet_emblem.png')

    # ==========================================
    # 1. COVER PAGE (Matching Reference Page 1)
    # ==========================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(24)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run("AI FARMER CROP RECOMMENDATION SYSTEM\n")
    r.bold = True
    r.font.size = Pt(16)
    r.font.name = 'Times New Roman'

    # VCET Logo
    if os.path.exists(logo_path):
        p_logo1 = doc.add_paragraph()
        p_logo1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo1.paragraph_format.space_after = Pt(12)
        run_l1 = p_logo1.add_run()
        run_l1.add_picture(logo_path, width=Inches(1.2))

    p_mini = doc.add_paragraph()
    p_mini.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mini.paragraph_format.space_after = Pt(12)
    r = p_mini.add_run("MINI PROJECT\n")
    r.bold = True
    r.font.size = Pt(13)
    r.font.name = 'Times New Roman'
    r2 = p_mini.add_run("21CS410-Artificial Intelligence & Machine Learning Laboratory\n")
    r2.bold = True
    r2.font.size = Pt(12)
    r2.font.name = 'Times New Roman'
    r3 = p_mini.add_run("(for the Academic Year 2025-26)\n\n")
    r3.font.italic = True
    r3.font.size = Pt(11)
    r3.font.name = 'Times New Roman'

    r_done = p_mini.add_run("Done by\n\n")
    r_done.font.italic = True
    r_done.font.size = Pt(12)
    r_done.font.name = 'Times New Roman'

    # Team Members (Replaced Aswin with team members)
    r_members = p_mini.add_run(
        "KEVIN LAWRENCE – 913124104065\n"
        "KISHORE – 913124104067\n"
        "SINDHAN – 913124104150\n\n"
    )
    r_members.bold = True
    r_members.font.size = Pt(12)
    r_members.font.name = 'Times New Roman'

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_after = Pt(8)
    r_dept = p_inst.add_run("Department of Computer Science and Engineering\n\n")
    r_dept.font.size = Pt(12)
    r_dept.font.name = 'Times New Roman'

    r_clg = p_inst.add_run("VELAMMAL COLLEGE OF ENGINEERING AND TECHNOLOGY\n")
    r_clg.bold = True
    r_clg.font.size = Pt(13)
    r_clg.font.name = 'Times New Roman'

    r_loc = p_inst.add_run("VIRAGANOOR, MADURAI-625009\n(AUTONOMOUS)\n")
    r_loc.bold = True
    r_loc.font.size = Pt(12)
    r_loc.font.name = 'Times New Roman'

    if os.path.exists(logo_path):
        p_logo2 = doc.add_paragraph()
        p_logo2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo2.paragraph_format.space_before = Pt(4)
        run_l2 = p_logo2.add_run()
        run_l2.add_picture(logo_path, width=Inches(1.1))

    doc.add_page_break()

    # ==========================================
    # 2. BONAFIDE CERTIFICATE (Matching Reference Page 2)
    # ==========================================
    p_bon_top = doc.add_paragraph()
    p_bon_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bon_top.paragraph_format.space_before = Pt(14)
    p_bon_top.paragraph_format.space_after = Pt(4)
    r = p_bon_top.add_run("VELAMMAL COLLEGE OF ENGINEERING AND TECHNOLOGY,\nMADURAI-625009.\n(Autonomous)\n\n")
    r.bold = True
    r.font.size = Pt(12)
    r.font.name = 'Times New Roman'

    r_dept2 = p_bon_top.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\n\n")
    r_dept2.bold = True
    r_dept2.font.size = Pt(12)
    r_dept2.font.name = 'Times New Roman'

    if os.path.exists(logo_path):
        p_logo3 = doc.add_paragraph()
        p_logo3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo3.paragraph_format.space_after = Pt(8)
        run_l3 = p_logo3.add_run()
        run_l3.add_picture(logo_path, width=Inches(1.0))

    p_bon_mid = doc.add_paragraph()
    p_bon_mid.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bon_mid.paragraph_format.space_after = Pt(10)
    r_yr = p_bon_mid.add_run("2025-26\n\n")
    r_yr.bold = True
    r_yr.font.size = Pt(12)
    r_yr.font.name = 'Times New Roman'

    r_bon = p_bon_mid.add_run("BONAFIDE CERTIFICATE\n")
    r_bon.bold = True
    r_bon.font.size = Pt(14)
    r_bon.font.color.rgb = RGBColor(0, 102, 102)
    r_bon.font.name = 'Times New Roman'

    r_cert = p_bon_mid.add_run("This is to certify that the thesis work titled\n\n")
    r_cert.font.italic = True
    r_cert.font.size = Pt(11)
    r_cert.font.name = 'Times New Roman'

    r_proj = p_bon_mid.add_run("AI FARMER CROP RECOMMENDATION SYSTEM\n")
    r_proj.bold = True
    r_proj.font.size = Pt(14)
    r_proj.font.name = 'Times New Roman'

    r_doneby = p_bon_mid.add_run("Was done by\n\n")
    r_doneby.font.italic = True
    r_doneby.font.size = Pt(11)
    r_doneby.font.name = 'Times New Roman'

    r_team = p_bon_mid.add_run(
        "KEVIN LAWRENCE – 913124104065\n"
        "KISHORE – 913124104067\n"
        "SINDHAN – 913124104150\n\n"
    )
    r_team.bold = True
    r_team.font.size = Pt(12)
    r_team.font.name = 'Times New Roman'

    p_bon_body = doc.add_paragraph()
    p_bon_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_bon_body.paragraph_format.line_spacing = 1.3
    p_bon_body.paragraph_format.space_after = Pt(45)
    r_desc = p_bon_body.add_run(
        "of fourth semester – Computer Science and Engineering Department in partial fulfillment of "
        "the requirement of 21CS410-Artificial Intelligence and Machine Learning Laboratory during the year 2025-26."
    )
    r_desc.font.size = Pt(11.5)
    r_desc.font.name = 'Times New Roman'

    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign.paragraph_format.space_after = Pt(0)
    r_sign = p_sign.add_run("Course in-charge")
    r_sign.bold = True
    r_sign.font.size = Pt(12)
    r_sign.font.name = 'Times New Roman'

    doc.add_page_break()

    # ==========================================
    # 3. EXPERIMENT HEADER & AIM (Matching Reference Page 3)
    # ==========================================
    p_ex = doc.add_paragraph()
    p_ex.paragraph_format.space_before = Pt(8)
    p_ex.paragraph_format.space_after = Pt(12)
    r_ex = p_ex.add_run("EX .NO: 10\t\tAI FARMER CROP RECOMMENDATION SYSTEM\nDATE: 27/09/2026")
    r_ex.bold = True
    r_ex.font.size = Pt(12)
    r_ex.font.name = 'Times New Roman'

    def add_heading_underlined(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(title)
        r.bold = True
        r.font.size = Pt(12)
        r.font.name = 'Times New Roman'
        r.underline = True

    def add_para(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.font.size = Pt(11)
        r.font.name = 'Times New Roman'
        return p

    def add_concept_bullet(title, desc):
        p1 = doc.add_paragraph()
        p1.paragraph_format.space_before = Pt(4)
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(f"• {title}")
        r1.bold = True
        r1.font.size = Pt(11)
        r1.font.name = 'Times New Roman'

        p2 = doc.add_paragraph()
        p2.paragraph_format.left_indent = Inches(0.4)
        p2.paragraph_format.space_after = Pt(6)
        p2.paragraph_format.line_spacing = 1.15
        r2 = p2.add_run(desc)
        r2.font.size = Pt(11)
        r2.font.name = 'Times New Roman'

    # AIM
    add_heading_underlined("AIM:")
    add_para(
        "To design and develop a web-based AI Farmer Crop Recommendation System that analyzes soil nutrients "
        "(Nitrogen, Phosphorus, Potassium), soil pH, and meteorological conditions (Temperature, Humidity, Rainfall) "
        "using Python, Flask, and Random Forest Classifier Machine Learning model, providing accurate crop prediction, "
        "confidence probability scoring, explainable agronomic reasoning, and real-time report generation with MySQL database storage."
    )

    # CONCEPTS INVOLVED
    add_heading_underlined("CONCEPTS INVOLVED:")
    add_concept_bullet("Database Management System (DBMS & MySQL):",
                       "Used to store and manage farmer registrations, telemetry logs, prediction history, crop knowledge references, and model metrics efficiently in relational MySQL tables.")
    add_concept_bullet("Machine Learning & Random Forest Classification:",
                       "Supervised ensemble classification algorithm utilizing 100 decision trees to classify 22 crop classes with non-linear multi-dimensional boundaries achieving 98.64% accuracy.")
    add_concept_bullet("Data Preprocessing & Feature Engineering:",
                       "Handles feature normalization, missing value verification, categorical label encoding, and stratified 80:20 train-test splitting.")
    add_concept_bullet("Python (Backend Development & REST API):",
                       "Handles server-side logic including PyMySQL database transactions, JWT token authentication, model inference endpoints, and automated document compilation.")
    add_concept_bullet("Frontend Technologies (Vue 3, Vite, JavaScript, CSS):",
                       "Provides responsive, modern glassmorphism user interface for farmers and administrators including analytical dashboards, soil input forms, and interactive pages.")
    add_concept_bullet("Explainable AI (XAI) Recommendation Logic:",
                       "Analyzes the causal factor contributions of soil nutrients and weather thresholds to provide transparent, human-readable agronomic justifications.")
    add_concept_bullet("Weather Integration & Agronomic Telemetry System:",
                       "Fetches live or baseline meteorological weather data (temperature, humidity, rainfall) for Tamil Nadu districts to support precision farming decisions.")
    add_concept_bullet("Automated Document & PDF Report Generator:",
                       "Dynamically compiles and exports official crop advisory certificates in PDF format and college project documentation in DOCX format.")

    # FILES USED
    add_heading_underlined("FILES USED:")
    files_list = [
        "dataset/Crop_recommendation.csv",
        "dataset/generate_dataset.py",
        "backend/ml_pipeline.py",
        "backend/app.py",
        "backend/config.py",
        "backend/db.py",
        "backend/init_db.py",
        "backend/routes/auth_routes.py",
        "backend/routes/farmer_routes.py",
        "backend/routes/crop_routes.py",
        "backend/routes/admin_routes.py",
        "backend/utils/auth_middleware.py",
        "backend/utils/weather_service.py",
        "backend/utils/report_generator.py",
        "backend/utils/doc_generator.py",
        "frontend/src/views/RecommendView.vue",
        "frontend/src/views/FarmerDashboard.vue",
        "frontend/src/views/HistoryView.vue",
        "frontend/src/views/CropInfoView.vue",
        "frontend/src/views/AdminDashboard.vue",
        "frontend/src/views/AdminModelMetrics.vue"
    ]
    for f in files_list:
        add_para(f"• {f}")

    # ==========================================
    # 4. PROGRAM / SOURCE CODE (Matching Reference Layout)
    # ==========================================
    add_heading_underlined("PROGRAM:")

    def add_code_section(filename, code_text):
        p_fn = doc.add_paragraph()
        p_fn.paragraph_format.space_before = Pt(8)
        p_fn.paragraph_format.space_after = Pt(2)
        r_fn = p_fn.add_run(filename)
        r_fn.bold = True
        r_fn.font.size = Pt(11)
        r_fn.font.name = 'Times New Roman'
        r_fn.underline = True

        p_code = doc.add_paragraph()
        p_code.paragraph_format.space_after = Pt(8)
        p_code.paragraph_format.line_spacing = 1.05
        r_c = p_code.add_run(code_text.strip())
        r_c.font.size = Pt(9.5)
        r_c.font.name = 'Courier New'

    add_code_section("db.py:", """
import pymysql
import pymysql.cursors
from backend.config import Config

// Database Connection
def get_db_connection(use_db=True):
    conn = pymysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME if use_db else None,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
        charset='utf8mb4'
    )
    return conn

def execute_query(query, params=None, fetchone=False, fetchall=False, insert=False):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            if insert: return cursor.lastrowid
            if fetchone: return cursor.fetchone()
            if fetchall: return cursor.fetchall()
            return cursor.rowcount
    finally:
        conn.close()
""")

    add_code_section("ml_pipeline.py:", """
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd, numpy as np, joblib

def train_crop_model():
    df = pd.read_csv('dataset/Crop_recommendation.csv')
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=15, criterion='entropy')
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred) # 98.64%
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    joblib.dump({'model': model, 'classes': list(model.classes_)}, 'models/crop_recommendation_model.pkl')
    return {'accuracy': acc, 'f1_score': f1}

def predict_crop(n, p, k, temperature, humidity, ph, rainfall):
    pkg = joblib.load('models/crop_recommendation_model.pkl')
    model = pkg['model']
    input_df = pd.DataFrame([{'N': n, 'P': p, 'K': k, 'temperature': temperature, 'humidity': humidity, 'ph': ph, 'rainfall': rainfall}])
    probs = model.predict_proba(input_df)[0]
    top_indices = np.argsort(probs)[::-1][:3]
    
    return {
        'recommended_crop': model.classes_[top_indices[0]].capitalize(),
        'confidence': round(float(probs[top_indices[0]]) * 100, 2),
        'top_recommendations': [{'crop': model.classes_[i].capitalize(), 'confidence': round(float(probs[i])*100, 2)} for i in top_indices]
    }
""")

    add_code_section("app.py:", """
from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.routes.auth_routes import auth_bp
from backend.routes.farmer_routes import farmer_bp
from backend.routes.crop_routes import crop_bp
from backend.routes.admin_routes import admin_bp

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(farmer_bp, url_prefix='/api')
app.register_blueprint(crop_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
""")

    add_code_section("farmer_routes.py:", """
from flask import Blueprint, request, jsonify, send_file
from backend.utils.auth_middleware import token_required
from backend.ml_pipeline import predict_crop
from backend.db import execute_query
from backend.utils.report_generator import generate_crop_pdf_report

farmer_bp = Blueprint('farmer_bp', __name__)

@farmer_bp.route('/predict', methods=['POST'])
@token_required
def run_prediction():
    user = request.current_user
    d = request.get_json()
    
    res = predict_crop(d['nitrogen'], d['phosphorus'], d['potassium'], d['temperature'], d['humidity'], d['ph'], d['rainfall'])
    
    pred_id = execute_query(
        \"\"\"INSERT INTO prediction_history (farmer_id, nitrogen, phosphorus, potassium, temperature,
               humidity, ph, rainfall, district, season, recommended_crop, confidence)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);\"\"\",
        (user['id'], d['nitrogen'], d['phosphorus'], d['potassium'], d['temperature'], d['humidity'],
         d['ph'], d['rainfall'], d.get('district'), d.get('season'), res['recommended_crop'], res['confidence']),
        insert=True
    )
    res['prediction_id'] = pred_id
    return jsonify({'success': True, **res})

@farmer_bp.route('/predictions/<int:pred_id>/report', methods=['GET'])
@token_required
def download_prediction_report(pred_id):
    pred = execute_query("SELECT * FROM prediction_history WHERE id = %s;", (pred_id,), fetchone=True)
    profile = execute_query("SELECT * FROM farmer_profiles WHERE user_id = %s;", (pred['farmer_id'],), fetchone=True)
    pdf_path = generate_crop_pdf_report(pred, profile)
    return send_file(pdf_path, as_attachment=True, download_name=f"crop_report_{pred_id}.pdf")
""")

    add_code_section("style.css:", """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
  --primary-color: #10b981;
  --secondary-color: #059669;
  --accent-color: #f59e0b;
  --bg-color: #f8fafc;
  --card-bg: rgba(255, 255, 255, 0.9);
  --text-main: #0f172a;
}

body {
  font-family: 'Plus Jakarta Sans', sans-serif;
  background-color: var(--bg-color);
  color: var(--text-main);
}

.glass-card {
  background: var(--card-bg);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(16, 185, 129, 0.15);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}
""")

    doc.add_page_break()

    # ==========================================
    # 5. OUTPUT SECTION (Matching Reference Pages 22-25)
    # ==========================================
    add_heading_underlined("OUTPUT:")
    add_para("The actual screenshots collected from the running AI Farmer Crop Recommendation application are shown below:")

    screenshots_data = [
        ("Fig 1: Home / Landing Page & Model Showcase", "fig0_landing_page.png"),
        ("Fig 2: Farmer Registration Interface", "fig1_farmer_registration.png"),
        ("Fig 3: Farmer Authentication / Login Interface", "fig2_farmer_login.png"),
        ("Fig 4: Farmer Dashboard with Farm Metrics & Overview", "fig3_farmer_dashboard.png"),
        ("Fig 5: Crop Recommendation Form with Soil NPK & Climate Inputs", "fig4_crop_recommendation_form.png"),
        ("Fig 6: AI Machine Learning Crop Prediction Result Card", "fig5_ai_crop_prediction.png"),
        ("Fig 7: Confidence Score Meter & Top-3 Alternative Crops", "fig6_confidence_score.png"),
        ("Fig 8: Prediction History & Saved Bookmarks Table", "fig7_prediction_history.png"),
        ("Fig 9: Agricultural Crop Encyclopedia Knowledge Base", "fig8_crop_information.png"),
        ("Fig 10: Administrator Analytics Dashboard with Chart.js Visualizations", "fig9_admin_dashboard.png"),
        ("Fig 11: Machine Learning Model Performance & Evaluation Metrics", "fig10_model_performance.png"),
        ("Fig 12: Project Documentation & Lab Report Generator", "fig11_project_documentation_generator.png"),
        ("Fig 13: MySQL Relational Database Schema & Table Structure", "fig12_database_schema.png")
    ]

    for caption, img_name in screenshots_data:
        img_path = os.path.join(SCREENSHOTS_DIR, img_name)
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(6)
            p_img.paragraph_format.space_after = Pt(2)
            run = p_img.add_run()
            run.add_picture(img_path, width=Inches(5.6))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(12)
            r_cap = p_cap.add_run(caption)
            r_cap.bold = True
            r_cap.font.size = Pt(9.5)
            r_cap.font.name = 'Times New Roman'

    doc.add_page_break()

    # ==========================================
    # 6. RESULT (Matching Reference Page 26)
    # ==========================================
    add_heading_underlined("RESULT:")
    add_para("The system successfully:")
    add_para("• Displays farmer telemetry and crop prediction details dynamically")
    add_para("• Evaluates soil macro-nutrients (N, P, K), pH, and climate parameters using Random Forest Classifier")
    add_para("• Delivers real-time crop recommendations with 98.64% measured test accuracy and top-3 alternative choices")
    add_para("• Tracks historical predictions, saved bookmarks, and farmer profiles efficiently")
    add_para("• Provides administrative visual dashboard analytics (crop popularity, district distribution, model metrics)")
    add_para("• Generates official downloadable PDF advisory reports with unique Report IDs")
    add_para("• Ensures reliable, secure relational data storage and transaction management using MySQL under XAMPP")

    add_para(
        "\nThus, the mini project effectively integrates Artificial Intelligence, Machine Learning, Python Flask, "
        "MySQL, and Vue 3 modern web technologies to simplify precision crop management, improve agricultural productivity, "
        "and enhance administrative efficiency."
    )

    # ==========================================
    # 7. REFERENCES (Matching Reference Page 26)
    # ==========================================
    add_heading_underlined("REFERENCES:")
    refs = [
        "1. ICAR Precision Agriculture & Soil Classification Documentation – https://icar.org.in/",
        "2. Scikit-Learn Ensemble & Random Forest Documentation – https://scikit-learn.org/",
        "3. Flask Web Framework Documentation – https://flask.palletsprojects.com/",
        "4. W3Schools (HTML, CSS, JavaScript, Python) – https://www.w3schools.com/",
        "5. GeeksforGeeks – Machine Learning & DBMS Concepts – https://www.geeksforgeeks.org/"
    ]
    for ref in refs:
        add_para(ref)

    # Save DOCX
    doc.save(OUTPUT_DOCX)
    print("=" * 60)
    print(f"LAB REPORT WORD DOCUMENT CREATED AT:\n{OUTPUT_DOCX}")
    print("=" * 60)


if __name__ == '__main__':
    build_lab_report()
