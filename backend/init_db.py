"""
Database Initialization Script for AI Farmer Crop Recommendation System
Connects to MySQL (XAMPP), creates the database 'ai_farmer_crop', sets up tables,
indexes, initial admin user, and agricultural crop reference data.
"""

import sys
import os
import json
import pymysql
from werkzeug.security import generate_password_hash

# Add parent directory to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.config import Config


CROP_DATA_SEED = [
    {
        "crop_name": "Rice",
        "crop_category": "Cereal / Grain",
        "suitable_soil": "Clayey, Clay-Loam, Alluvial Soil with high water retention",
        "temp_min": 20.0, "temp_max": 35.0,
        "humidity_min": 75.0, "humidity_max": 95.0,
        "ph_min": 5.5, "ph_max": 7.0,
        "rainfall_min": 150.0, "rainfall_max": 300.0,
        "water_requirement": "Very High (Standing water required during vegetative phase)",
        "season": "Kharif / Samba / Kuruvai (June-Nov)",
        "growth_duration": "120 - 150 Days",
        "cultivation_guide": "Maintain puddle field conditions with 2-5 cm water layer. Apply balanced NPK with split nitrogen dosages during tillering and panicle initiation.",
        "market_value": "High demand staple cereal across India and global exports."
    },
    {
        "crop_name": "Maize",
        "crop_category": "Cereal / Coarse Grain",
        "suitable_soil": "Well-drained Fertile Sandy Loam to Clay Loam",
        "temp_min": 18.0, "temp_max": 32.0,
        "humidity_min": 55.0, "humidity_max": 75.0,
        "ph_min": 5.5, "ph_max": 7.5,
        "rainfall_min": 60.0, "rainfall_max": 110.0,
        "water_requirement": "Moderate (Critical at silking and grain filling)",
        "season": "Kharif & Rabi (All season adaptable)",
        "growth_duration": "90 - 110 Days",
        "cultivation_guide": "Ensure good drainage to avoid waterlogging. Plant on ridges with 60x20 cm spacing. Weed control in first 30 days is critical.",
        "market_value": "Excellent market for poultry feed, starch industry, and human consumption."
    },
    {
        "crop_name": "Chickpea",
        "crop_category": "Pulse / Legume",
        "suitable_soil": "Deep Black Soils, Sandy Loam with good drainage",
        "temp_min": 15.0, "temp_max": 25.0,
        "humidity_min": 14.0, "humidity_max": 30.0,
        "ph_min": 6.0, "ph_max": 8.0,
        "rainfall_min": 60.0, "rainfall_max": 95.0,
        "water_requirement": "Low to Moderate (Sensitive to excess moisture)",
        "season": "Rabi (October - March)",
        "growth_duration": "90 - 120 Days",
        "cultivation_guide": "Inoculate seeds with Rhizobium culture. Avoid excessive vegetative growth by managing irrigation at pre-flowering and pod development.",
        "market_value": "Premium pulse with strong domestic demand and high protein value."
    },
    {
        "crop_name": "Kidneybeans",
        "crop_category": "Pulse / Legume",
        "suitable_soil": "Rich Loamy Soil with organic humus",
        "temp_min": 15.0, "temp_max": 25.0,
        "humidity_min": 20.0, "humidity_max": 35.0,
        "ph_min": 5.5, "ph_max": 6.5,
        "rainfall_min": 60.0, "rainfall_max": 150.0,
        "water_requirement": "Moderate",
        "season": "Rabi in plains / Kharif in hills",
        "growth_duration": "100 - 130 Days",
        "cultivation_guide": "Prefers cool climate and sunny weather. Maintain moderate soil moisture during flowering and pod development.",
        "market_value": "High commercial value and gourmet culinary commodity."
    },
    {
        "crop_name": "Pigeonpeas",
        "crop_category": "Pulse / Red Gram",
        "suitable_soil": "Deep Well-drained Loam and Medium Black Soils",
        "temp_min": 20.0, "temp_max": 38.0,
        "humidity_min": 35.0, "humidity_max": 70.0,
        "ph_min": 5.0, "ph_max": 7.5,
        "rainfall_min": 90.0, "rainfall_max": 200.0,
        "water_requirement": "Moderate (Drought tolerant deep taproot)",
        "season": "Kharif (June - January)",
        "growth_duration": "150 - 180 Days",
        "cultivation_guide": "Intercropping with cotton or cereals improves soil nitrogen via symbiotic fixation. Regular monitoring for pod borer is advised.",
        "market_value": "Major staple dal in Indian cuisine with year-round steady market."
    },
    {
        "crop_name": "Mothbeans",
        "crop_category": "Pulse / Arid Legume",
        "suitable_soil": "Light Sandy to Sandy Loam Arid Soils",
        "temp_min": 24.0, "temp_max": 35.0,
        "humidity_min": 40.0, "humidity_max": 65.0,
        "ph_min": 4.0, "ph_max": 8.5,
        "rainfall_min": 30.0, "rainfall_max": 75.0,
        "water_requirement": "Very Low (Highly drought resistant)",
        "season": "Kharif (July - October)",
        "growth_duration": "75 - 90 Days",
        "cultivation_guide": "Ideal for semi-arid dryland farming. Requires minimal fertilizer and acts as soil erosion preventer.",
        "market_value": "Widely used in traditional snacks (Bhujia) and protein supplements."
    },
    {
        "crop_name": "Mungbean",
        "crop_category": "Pulse / Green Gram",
        "suitable_soil": "Well-drained Loam to Sandy Loam",
        "temp_min": 25.0, "temp_max": 35.0,
        "humidity_min": 75.0, "humidity_max": 90.0,
        "ph_min": 6.2, "ph_max": 7.2,
        "rainfall_min": 35.0, "rainfall_max": 60.0,
        "water_requirement": "Low to Moderate",
        "season": "Kharif, Rabi and Summer catch crop",
        "growth_duration": "60 - 75 Days",
        "cultivation_guide": "Short-duration crop ideal for crop rotation. Fixes atmospheric nitrogen and requires 1-2 protective irrigations.",
        "market_value": "High demand, fast cash realization for farmers."
    },
    {
        "crop_name": "Blackgram",
        "crop_category": "Pulse / Urad Dal",
        "suitable_soil": "Loamy to Heavy Clay and Black Cotton Soils",
        "temp_min": 25.0, "temp_max": 35.0,
        "humidity_min": 60.0, "humidity_max": 75.0,
        "ph_min": 6.5, "ph_max": 7.8,
        "rainfall_min": 60.0, "rainfall_max": 75.0,
        "water_requirement": "Moderate",
        "season": "Kharif and Rice-fallow Rabi",
        "growth_duration": "70 - 90 Days",
        "cultivation_guide": "Widely grown after rice harvesting in Tamil Nadu delta region. Seed treatment with Trichoderma viride enhances seedling vigor.",
        "market_value": "High commercial value for culinary uses (idli/dosa batter, papad)."
    },
    {
        "crop_name": "Lentil",
        "crop_category": "Pulse / Masoor",
        "suitable_soil": "Alluvial Loam, Clay Loam with good drainage",
        "temp_min": 18.0, "temp_max": 30.0,
        "humidity_min": 60.0, "humidity_max": 70.0,
        "ph_min": 6.0, "ph_max": 7.8,
        "rainfall_min": 35.0, "rainfall_max": 55.0,
        "water_requirement": "Low",
        "season": "Rabi (Winter)",
        "growth_duration": "100 - 130 Days",
        "cultivation_guide": "Requires cool growing season and warm ripening period. Sensitive to water logging and saline conditions.",
        "market_value": "High protein pulse with steady wholesale and retail pricing."
    },
    {
        "crop_name": "Pomegranate",
        "crop_category": "Horticultural Fruit",
        "suitable_soil": "Deep Well-drained Loam or Light Loam",
        "temp_min": 18.0, "temp_max": 35.0,
        "humidity_min": 80.0, "humidity_max": 95.0,
        "ph_min": 5.5, "ph_max": 7.5,
        "rainfall_min": 90.0, "rainfall_max": 120.0,
        "water_requirement": "Moderate (Drip irrigation recommended)",
        "season": "Perennial (Bahar treatment in Ambe/Mrig/Hasta)",
        "growth_duration": "Perennial (Bearing starts after 2-3 years)",
        "cultivation_guide": "Adopt drip irrigation and fertigation. Prune water shoots and manage bacterial blight with copper-based sprays.",
        "market_value": "High export potential and premium domestic market fruit."
    },
    {
        "crop_name": "Banana",
        "crop_category": "Horticultural Fruit",
        "suitable_soil": "Rich Loamy Soil with excellent drainage and organic matter",
        "temp_min": 20.0, "temp_max": 35.0,
        "humidity_min": 75.0, "humidity_max": 90.0,
        "ph_min": 5.5, "ph_max": 7.5,
        "rainfall_min": 90.0, "rainfall_max": 130.0,
        "water_requirement": "High (Regular, uniform soil moisture required)",
        "season": "Year-round planting in tropics",
        "growth_duration": "11 - 14 Months",
        "cultivation_guide": "Plant tissue culture suckers with 1.8x1.8m spacing. Apply high potassium at bunch emergence and provide propping support.",
        "market_value": "Tremendous cash flow crop with massive daily market consumption."
    },
    {
        "crop_name": "Mango",
        "crop_category": "Horticultural Fruit Tree",
        "suitable_soil": "Deep, Well-drained Alluvial or Red Loamy Soil",
        "temp_min": 24.0, "temp_max": 38.0,
        "humidity_min": 45.0, "humidity_max": 65.0,
        "ph_min": 5.5, "ph_max": 7.5,
        "rainfall_min": 85.0, "rainfall_max": 110.0,
        "water_requirement": "Moderate (Dry period required before flowering)",
        "season": "Summer Harvest (March - July)",
        "growth_duration": "Perennial Orchard",
        "cultivation_guide": "Maintain dry spell during winter to induce heavy floral blooming. Control powdery mildew and hopper during flowering.",
        "market_value": "King of Fruits with lucrative seasonal domestic and export earnings."
    },
    {
        "crop_name": "Grapes",
        "crop_category": "Horticultural Cash Fruit",
        "suitable_soil": "Sandy Loam to Clay Loam with pH 6.0 - 7.5",
        "temp_min": 15.0, "temp_max": 40.0,
        "humidity_min": 75.0, "humidity_max": 88.0,
        "ph_min": 5.5, "ph_max": 6.8,
        "rainfall_min": 60.0, "rainfall_max": 80.0,
        "water_requirement": "Moderate (Precision drip irrigation)",
        "season": "Pruning in April and October; Harvest Jan-April",
        "growth_duration": "Perennial Vineyard",
        "cultivation_guide": "Requires bower (pandal) trellising system. Timely pruning, gibberellic acid (GA3) dipping for berry elongation.",
        "market_value": "Highly profitable for table grape market, raisin processing, and wine industry."
    },
    {
        "crop_name": "Watermelon",
        "crop_category": "Cucurbit / Summer Fruit",
        "suitable_soil": "Sandy Loam and Riverbed Alluvial Soils",
        "temp_min": 24.0, "temp_max": 35.0,
        "humidity_min": 80.0, "humidity_max": 90.0,
        "ph_min": 6.0, "ph_max": 7.0,
        "rainfall_min": 40.0, "rainfall_max": 60.0,
        "water_requirement": "Moderate (Irrigate regularly till fruit ripening)",
        "season": "Zaid / Summer (Jan - May)",
        "growth_duration": "80 - 100 Days",
        "cultivation_guide": "Silver-black plastic mulching and drip irrigation enhance fruit sweetness and yield. Reduce water 10 days before harvest.",
        "market_value": "High seasonal demand during warm summer months."
    },
    {
        "crop_name": "Muskmelon",
        "crop_category": "Cucurbit / Summer Fruit",
        "suitable_soil": "Well-drained Fertile Sandy Loam",
        "temp_min": 25.0, "temp_max": 35.0,
        "humidity_min": 85.0, "humidity_max": 95.0,
        "ph_min": 6.0, "ph_max": 7.0,
        "rainfall_min": 20.0, "rainfall_max": 35.0,
        "water_requirement": "Low to Moderate (Avoid moisture on leaves)",
        "season": "Summer (February - May)",
        "growth_duration": "70 - 90 Days",
        "cultivation_guide": "Warm and dry weather during fruit ripening enhances TSS (sugar percentage). Avoid water stagnation.",
        "market_value": "Rapid cash crop with high consumer preference in urban markets."
    },
    {
        "crop_name": "Apple",
        "crop_category": "Temperate Fruit",
        "suitable_soil": "Deep Well-drained Loamy Soil rich in organic matter",
        "temp_min": 15.0, "temp_max": 25.0,
        "humidity_min": 85.0, "humidity_max": 95.0,
        "ph_min": 5.5, "ph_max": 6.5,
        "rainfall_min": 100.0, "rainfall_max": 130.0,
        "water_requirement": "Moderate to High",
        "season": "Harvest July - October",
        "growth_duration": "Perennial",
        "cultivation_guide": "Requires chilling hours (<7°C) during dormancy. Training and pruning on central leader system maximizes fruit color.",
        "market_value": "Premium high-value fruit with year-round cold storage marketing."
    },
    {
        "crop_name": "Orange",
        "crop_category": "Citrus Fruit",
        "suitable_soil": "Well-drained Light Loam or Alluvial Soils",
        "temp_min": 15.0, "temp_max": 35.0,
        "humidity_min": 85.0, "humidity_max": 95.0,
        "ph_min": 6.0, "ph_max": 8.0,
        "rainfall_min": 95.0, "rainfall_max": 125.0,
        "water_requirement": "Moderate (Avoid waterlogging at root zone)",
        "season": "Ambe Bahar & Mrig Bahar harvests",
        "growth_duration": "Perennial Citrus Orchard",
        "cultivation_guide": "Budded plants on Rangpur lime rootstock resist phytophthora root rot. Zinc and micronutrient foliar spray is essential.",
        "market_value": "High demand for fresh fruit and fruit juice beverage processing."
    },
    {
        "crop_name": "Papaya",
        "crop_category": "Tropical Fruit",
        "suitable_soil": "Well-drained Rich Loamy Soil",
        "temp_min": 22.0, "temp_max": 38.0,
        "humidity_min": 85.0, "humidity_max": 95.0,
        "ph_min": 6.0, "ph_max": 7.0,
        "rainfall_min": 120.0, "rainfall_max": 250.0,
        "water_requirement": "Moderate to High (Extremely sensitive to water logging)",
        "season": "Year-round planting",
        "growth_duration": "9 - 12 Months",
        "cultivation_guide": "Ensure perfect soil drainage on raised beds. Cultivate gynodioecious varieties (e.g. Red Lady) for 100% productive trees.",
        "market_value": "Fast-yielding commercial crop with high domestic consumption and papain extraction."
    },
    {
        "crop_name": "Coconut",
        "crop_category": "Plantation / Cash Crop",
        "suitable_soil": "Coastal Sandy Loam, Alluvial, Red Sandy Loam",
        "temp_min": 24.0, "temp_max": 35.0,
        "humidity_min": 85.0, "humidity_max": 99.0,
        "ph_min": 5.2, "ph_max": 7.5,
        "rainfall_min": 130.0, "rainfall_max": 250.0,
        "water_requirement": "High (Drip irrigation / basin irrigation)",
        "season": "Perennial (Continuous monthly nut harvest)",
        "growth_duration": "Perennial (60+ years productive lifespan)",
        "cultivation_guide": "Apply 1 kg urea, 2 kg superphosphate, and 2 kg muriate of potash per palm per year with regular organic green manuring.",
        "market_value": "Evergreen economic return from tender water, copra, coconut oil, and coir."
    },
    {
        "crop_name": "Cotton",
        "crop_category": "Commercial Fiber Crop",
        "suitable_soil": "Deep Black Cotton Soils (Vertisols) and Heavy Loams",
        "temp_min": 20.0, "temp_max": 32.0,
        "humidity_min": 70.0, "humidity_max": 85.0,
        "ph_min": 6.0, "ph_max": 8.0,
        "rainfall_min": 60.0, "rainfall_max": 100.0,
        "water_requirement": "Moderate (Critical at square formation and boll development)",
        "season": "Kharif (May - December)",
        "growth_duration": "150 - 180 Days",
        "cultivation_guide": "Deep summer plowing destroys overwintering pupae. Provide optimum potassium for boll retention and lint strength.",
        "market_value": "White Gold of agriculture, backbone of textile and ginning mills."
    },
    {
        "crop_name": "Jute",
        "crop_category": "Commercial Fiber Crop",
        "suitable_soil": "Alluvial Loam to Clayey Loam",
        "temp_min": 24.0, "temp_max": 35.0,
        "humidity_min": 70.0, "humidity_max": 90.0,
        "ph_min": 6.0, "ph_max": 7.5,
        "rainfall_min": 150.0, "rainfall_max": 220.0,
        "water_requirement": "High (Requires abundant water for growth and retting)",
        "season": "Kharif (March - August)",
        "growth_duration": "120 - 140 Days",
        "cultivation_guide": "Requires high humidity and warm temperatures. Harvest at 50% flowering stage for finest quality fiber extraction.",
        "market_value": "Eco-friendly golden fiber with massive packaging and geotextile usage."
    },
    {
        "crop_name": "Coffee",
        "crop_category": "Plantation Beverage Crop",
        "suitable_soil": "Rich Friable Humus-rich Loamy Forest Soils",
        "temp_min": 18.0, "temp_max": 28.0,
        "humidity_min": 50.0, "humidity_max": 75.0,
        "ph_min": 6.0, "ph_max": 7.0,
        "rainfall_min": 120.0, "rainfall_max": 220.0,
        "water_requirement": "Moderate to High (Blossom showers are essential in March)",
        "season": "Harvest Nov - Feb (Arabica) & Jan - April (Robusta)",
        "growth_duration": "Perennial Plantation",
        "cultivation_guide": "Grown under two-tier shade trees (silver oak, dadap). Regular desuckering and shade regulation enhance coffee cherry quality.",
        "market_value": "High-value export beverage commodity traded globally."
    }
]


def init_database():
    print("=" * 60)
    print("AI FARMER CROP RECOMMENDATION SYSTEM - DATABASE INITIALIZATION")
    print("=" * 60)

    # 1. Connect to MySQL server (without specifying DB name first)
    try:
        conn = pymysql.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            autocommit=True
        )
        print("[OK] Successfully connected to MySQL Server.")
    except pymysql.MySQLError as e:
        print("\n" + "!" * 60)
        print(f"[ERROR] Could not connect to MySQL at {Config.DB_HOST}:{Config.DB_PORT}")
        print(f"Details: {e}")
        print("Please ensure that XAMPP / MySQL service is running on your system!")
        print("!" * 60 + "\n")
        sys.exit(1)

    with conn.cursor() as cursor:
        # 2. Create Database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print(f"[OK] Database `{Config.DB_NAME}` verified/created.")

        cursor.execute(f"USE `{Config.DB_NAME}`;")

        # 3. Create Tables
        print("[...] Creating tables with foreign keys and indexes...")

        # Users Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `users` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `username` VARCHAR(80) NOT NULL UNIQUE,
            `email` VARCHAR(120) NOT NULL UNIQUE,
            `password_hash` VARCHAR(255) NOT NULL,
            `role` ENUM('farmer', 'admin') NOT NULL DEFAULT 'farmer',
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # Farmer Profiles Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `farmer_profiles` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `user_id` INT NOT NULL UNIQUE,
            `full_name` VARCHAR(150) NOT NULL,
            `phone` VARCHAR(20) DEFAULT '',
            `district` VARCHAR(100) DEFAULT 'Madurai',
            `state` VARCHAR(100) DEFAULT 'Tamil Nadu',
            `farm_area` FLOAT DEFAULT 2.5,
            `preferred_language` VARCHAR(50) DEFAULT 'English',
            `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # Crop Information Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `crop_information` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `crop_name` VARCHAR(80) NOT NULL UNIQUE,
            `crop_category` VARCHAR(60) NOT NULL,
            `suitable_soil` VARCHAR(200) NOT NULL,
            `temp_min` FLOAT NOT NULL,
            `temp_max` FLOAT NOT NULL,
            `humidity_min` FLOAT NOT NULL,
            `humidity_max` FLOAT NOT NULL,
            `ph_min` FLOAT NOT NULL,
            `ph_max` FLOAT NOT NULL,
            `rainfall_min` FLOAT NOT NULL,
            `rainfall_max` FLOAT NOT NULL,
            `water_requirement` VARCHAR(150) NOT NULL,
            `season` VARCHAR(100) NOT NULL,
            `growth_duration` VARCHAR(100) NOT NULL,
            `cultivation_guide` TEXT NOT NULL,
            `market_value` VARCHAR(200) NOT NULL,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # Prediction History Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `prediction_history` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `farmer_id` INT NOT NULL,
            `nitrogen` FLOAT NOT NULL,
            `phosphorus` FLOAT NOT NULL,
            `potassium` FLOAT NOT NULL,
            `temperature` FLOAT NOT NULL,
            `humidity` FLOAT NOT NULL,
            `ph` FLOAT NOT NULL,
            `rainfall` FLOAT NOT NULL,
            `district` VARCHAR(100) DEFAULT 'Madurai',
            `state` VARCHAR(100) DEFAULT 'Tamil Nadu',
            `season` VARCHAR(50) DEFAULT 'Kharif',
            `recommended_crop` VARCHAR(80) NOT NULL,
            `confidence` FLOAT NOT NULL,
            `alternative_crops` TEXT,
            `explanation` TEXT,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_farmer_id (`farmer_id`),
            INDEX idx_recommended_crop (`recommended_crop`),
            FOREIGN KEY (`farmer_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # Saved Recommendations Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `saved_recommendations` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `farmer_id` INT NOT NULL,
            `prediction_id` INT NOT NULL,
            `crop_name` VARCHAR(80) NOT NULL,
            `notes` TEXT,
            `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_saved_farmer (`farmer_id`),
            FOREIGN KEY (`farmer_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`prediction_id`) REFERENCES `prediction_history`(`id`) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        # Model Metrics Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS `model_metrics` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            `model_name` VARCHAR(100) NOT NULL,
            `algorithm` VARCHAR(100) NOT NULL,
            `accuracy` FLOAT NOT NULL,
            `precision_val` FLOAT NOT NULL,
            `recall_val` FLOAT NOT NULL,
            `f1_score` FLOAT NOT NULL,
            `total_samples` INT NOT NULL,
            `metrics_json` JSON,
            `trained_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)

        print("[OK] Tables created successfully.")

        # 4. Insert / Seed Admin User
        admin_pass_hash = generate_password_hash("admin123")
        cursor.execute("SELECT id FROM users WHERE username = %s;", ("admin",))
        admin_row = cursor.fetchone()
        if not admin_row:
            cursor.execute("""
            INSERT INTO users (username, email, password_hash, role)
            VALUES (%s, %s, %s, %s);
            """, ("admin", "admin@aifarmer.org", admin_pass_hash, "admin"))
            admin_id = cursor.lastrowid
            cursor.execute("""
            INSERT INTO farmer_profiles (user_id, full_name, phone, district, state, farm_area)
            VALUES (%s, %s, %s, %s, %s, %s);
            """, (admin_id, "System Administrator", "+91 9876543210", "Madurai", "Tamil Nadu", 10.0))
            print("[OK] Default Admin created (Username: admin | Password: admin123).")
        else:
            print("[INFO] Admin user already exists.")

        # 5. Insert / Seed Demo Farmer (Aswin Kumar)
        farmer_pass_hash = generate_password_hash("farmer123")
        cursor.execute("SELECT id FROM users WHERE username = %s;", ("aswin",))
        farmer_row = cursor.fetchone()
        if not farmer_row:
            cursor.execute("""
            INSERT INTO users (username, email, password_hash, role)
            VALUES (%s, %s, %s, %s);
            """, ("aswin", "aswin@example.com", farmer_pass_hash, "farmer"))
            farmer_id = cursor.lastrowid
            cursor.execute("""
            INSERT INTO farmer_profiles (user_id, full_name, phone, district, state, farm_area, preferred_language)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (farmer_id, "Aswin Kumar T A", "+91 9131241043", "Madurai", "Tamil Nadu", 4.5, "English"))
            print("[OK] Demo Farmer created (Username: aswin | Password: farmer123).")
        else:
            print("[INFO] Farmer 'aswin' already exists.")

        # 6. Seed Crop Information Data
        for crop in CROP_DATA_SEED:
            cursor.execute("SELECT id FROM crop_information WHERE crop_name = %s;", (crop['crop_name'],))
            if not cursor.fetchone():
                cursor.execute("""
                INSERT INTO crop_information (
                    crop_name, crop_category, suitable_soil, temp_min, temp_max,
                    humidity_min, humidity_max, ph_min, ph_max, rainfall_min, rainfall_max,
                    water_requirement, season, growth_duration, cultivation_guide, market_value
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    crop['crop_name'], crop['crop_category'], crop['suitable_soil'],
                    crop['temp_min'], crop['temp_max'], crop['humidity_min'], crop['humidity_max'],
                    crop['ph_min'], crop['ph_max'], crop['rainfall_min'], crop['rainfall_max'],
                    crop['water_requirement'], crop['season'], crop['growth_duration'],
                    crop['cultivation_guide'], crop['market_value']
                ))
        print(f"[OK] Seeded {len(CROP_DATA_SEED)} agricultural crop reference profiles.")

        # 7. Seed initial Model Metrics from JSON if available
        metrics_file = os.path.join(Config.BASE_DIR, 'models', 'model_metrics.json')
        if os.path.exists(metrics_file):
            with open(metrics_file, 'r') as mf:
                m_data = json.load(mf)
            cursor.execute("SELECT id FROM model_metrics ORDER BY id DESC LIMIT 1;")
            if not cursor.fetchone():
                cursor.execute("""
                INSERT INTO model_metrics (
                    model_name, algorithm, accuracy, precision_val, recall_val, f1_score, total_samples, metrics_json
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    "Crop Recommendation Model v1.0",
                    m_data.get('algorithm', 'Random Forest Classifier'),
                    m_data.get('accuracy', 0.9864),
                    m_data.get('precision_weighted', 0.9867),
                    m_data.get('recall_weighted', 0.9864),
                    m_data.get('f1_score_weighted', 0.9863),
                    m_data.get('total_dataset_records', 2200),
                    json.dumps(m_data)
                ))
                print("[OK] Synchronized model metrics into database.")

    conn.close()
    print("=" * 60)
    print("DATABASE INITIALIZATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == '__main__':
    init_database()
