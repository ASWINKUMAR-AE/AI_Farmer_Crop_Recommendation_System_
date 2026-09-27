import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS

# Add root directory to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.config import Config
from backend.routes.auth_routes import auth_bp
from backend.routes.farmer_routes import farmer_bp
from backend.routes.crop_routes import crop_bp
from backend.routes.admin_routes import admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for frontend Vite dev server (port 5173, 3000, 8080, etc.)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(farmer_bp, url_prefix='/api')
    app.register_blueprint(crop_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'AI Farmer Crop Recommendation API',
            'version': '1.0.0',
            'ml_model': 'Random Forest Classifier',
            'database': 'MySQL (ai_farmer_crop)'
        })

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'success': False, 'message': 'API endpoint not found'}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'success': False, 'message': f'Internal Server Error: {str(e)}'}), 500

    return app


app = create_app()

if __name__ == '__main__':
    print("==================================================")
    print("AI FARMER CROP RECOMMENDATION BACKEND SERVER")
    print("Starting Flask API on http://127.0.0.1:5000")
    print("==================================================")
    app.run(host='0.0.0.0', port=5000, debug=True)
