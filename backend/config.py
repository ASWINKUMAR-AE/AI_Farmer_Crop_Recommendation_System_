import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ai-farmer-crop-recommendation-secret-key-2026')
    JWT_SECRET = os.environ.get('JWT_SECRET', 'jwt-super-secret-key-agri-ai-2026')
    JWT_EXPIRATION_HOURS = int(os.environ.get('JWT_EXPIRATION_HOURS', 24))

    # MySQL / XAMPP Database Configuration
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('DB_PORT', 3306))
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'ai_farmer_crop')

    # Weather API (Optional OpenWeather key)
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', '')

    # Base directories
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
    SCREENSHOTS_DIR = os.path.join(BASE_DIR, 'screenshots')
    DOCS_DIR = os.path.join(BASE_DIR, 'docs')
