import os
import json
from flask import Blueprint, request, jsonify, send_file
from backend.db import execute_query
from backend.utils.auth_middleware import token_required
from backend.ml_pipeline import predict_crop
from backend.utils.report_generator import generate_crop_pdf_report

farmer_bp = Blueprint('farmer_bp', __name__)


@farmer_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    user = request.current_user
    profile = execute_query(
        """SELECT u.id, u.username, u.email, u.role, u.created_at,
                  p.full_name, p.phone, p.district, p.state, p.farm_area, p.preferred_language
           FROM users u
           LEFT JOIN farmer_profiles p ON u.id = p.user_id
           WHERE u.id = %s;""",
        (user['id'],),
        fetchone=True
    )
    return jsonify({'success': True, 'profile': profile})


@farmer_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    user = request.current_user
    data = request.get_json() or {}
    full_name = data.get('full_name', '').strip()
    phone = data.get('phone', '').strip()
    district = data.get('district', 'Madurai').strip()
    state = data.get('state', 'Tamil Nadu').strip()
    farm_area = float(data.get('farm_area', 2.5) or 2.5)
    preferred_language = data.get('preferred_language', 'English').strip()

    execute_query(
        """UPDATE farmer_profiles
           SET full_name = %s, phone = %s, district = %s, state = %s, farm_area = %s, preferred_language = %s
           WHERE user_id = %s;""",
        (full_name, phone, district, state, farm_area, preferred_language, user['id'])
    )

    return jsonify({'success': True, 'message': 'Profile updated successfully!'})


@farmer_bp.route('/predict', methods=['POST'])
@token_required
def run_prediction():
    user = request.current_user
    data = request.get_json() or {}

    try:
        n = float(data.get('nitrogen', data.get('N', 0)))
        p = float(data.get('phosphorus', data.get('P', 0)))
        k = float(data.get('potassium', data.get('K', 0)))
        temperature = float(data.get('temperature', 25.0))
        humidity = float(data.get('humidity', 70.0))
        ph = float(data.get('ph', 6.5))
        rainfall = float(data.get('rainfall', 100.0))
        district = data.get('district', 'Madurai')
        state = data.get('state', 'Tamil Nadu')
        season = data.get('season', 'Kharif')
    except (ValueError, TypeError) as e:
        return jsonify({'success': False, 'message': f'Invalid numeric input: {str(e)}'}), 400

    # Range validations
    if not (0 <= n <= 300 and 0 <= p <= 300 and 0 <= k <= 300):
        return jsonify({'success': False, 'message': 'Soil N, P, K values must be between 0 and 300 kg/ha.'}), 400
    if not (0 <= ph <= 14):
        return jsonify({'success': False, 'message': 'Soil pH must be between 0 and 14.'}), 400
    if not (0 <= rainfall <= 1000):
        return jsonify({'success': False, 'message': 'Rainfall value out of realistic range (0-1000 mm).'}), 400

    # ML Model Prediction
    prediction_res = predict_crop(n, p, k, temperature, humidity, ph, rainfall)

    # Store in prediction_history database table
    pred_id = execute_query(
        """INSERT INTO prediction_history (
               farmer_id, nitrogen, phosphorus, potassium, temperature,
               humidity, ph, rainfall, district, state, season,
               recommended_crop, confidence, alternative_crops, explanation
           ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
        (
            user['id'], n, p, k, temperature, humidity, ph, rainfall,
            district, state, season,
            prediction_res['recommended_crop'],
            prediction_res['confidence'],
            json.dumps(prediction_res['alternative_crops']),
            json.dumps(prediction_res['explanation_points'])
        ),
        insert=True
    )

    # Fetch crop cultivation info if available
    crop_info = execute_query(
        "SELECT * FROM crop_information WHERE LOWER(crop_name) = LOWER(%s);",
        (prediction_res['recommended_crop'],),
        fetchone=True
    )

    return jsonify({
        'success': True,
        'prediction_id': pred_id,
        'recommended_crop': prediction_res['recommended_crop'],
        'crop_key': prediction_res['crop_key'],
        'confidence': prediction_res['confidence'],
        'top_recommendations': prediction_res['top_recommendations'],
        'alternative_crops': prediction_res['alternative_crops'],
        'explanation_points': prediction_res['explanation_points'],
        'inputs': {
            'nitrogen': n, 'phosphorus': p, 'potassium': k,
            'temperature': temperature, 'humidity': humidity,
            'ph': ph, 'rainfall': rainfall, 'district': district,
            'season': season
        },
        'crop_info': crop_info,
        'model_used': prediction_res['model_used'],
        'disclaimer': prediction_res['disclaimer']
    })


@farmer_bp.route('/predictions', methods=['GET'])
@token_required
def get_prediction_history():
    user = request.current_user
    rows = execute_query(
        """SELECT h.*, 
                  CASE WHEN s.id IS NOT NULL THEN 1 ELSE 0 END as is_saved
           FROM prediction_history h
           LEFT JOIN saved_recommendations s ON h.id = s.prediction_id AND s.farmer_id = %s
           WHERE h.farmer_id = %s
           ORDER BY h.created_at DESC;""",
        (user['id'], user['id']),
        fetchall=True
    ) or []

    # Parse JSON strings
    for r in rows:
        if isinstance(r.get('alternative_crops'), str):
            try:
                r['alternative_crops'] = json.loads(r['alternative_crops'])
            except:
                r['alternative_crops'] = [r['alternative_crops']]
        if isinstance(r.get('explanation'), str):
            try:
                r['explanation'] = json.loads(r['explanation'])
            except:
                r['explanation'] = [r['explanation']]

    return jsonify({'success': True, 'predictions': rows, 'total': len(rows)})


@farmer_bp.route('/predictions/<int:pred_id>', methods=['GET'])
@token_required
def get_prediction_detail(pred_id):
    user = request.current_user
    row = execute_query(
        "SELECT * FROM prediction_history WHERE id = %s AND (farmer_id = %s OR %s = 'admin');",
        (pred_id, user['id'], user['role']),
        fetchone=True
    )
    if not row:
        return jsonify({'success': False, 'message': 'Prediction not found'}), 404

    crop_info = execute_query(
        "SELECT * FROM crop_information WHERE LOWER(crop_name) = LOWER(%s);",
        (row['recommended_crop'],),
        fetchone=True
    )

    return jsonify({'success': True, 'prediction': row, 'crop_info': crop_info})


@farmer_bp.route('/recommendations/save', methods=['POST'])
@token_required
def save_recommendation():
    user = request.current_user
    data = request.get_json() or {}
    pred_id = data.get('prediction_id')
    notes = data.get('notes', 'Saved from prediction')

    if not pred_id:
        return jsonify({'success': False, 'message': 'Prediction ID required'}), 400

    # Verify prediction ownership
    pred = execute_query(
        "SELECT recommended_crop FROM prediction_history WHERE id = %s AND farmer_id = %s;",
        (pred_id, user['id']),
        fetchone=True
    )
    if not pred:
        return jsonify({'success': False, 'message': 'Prediction record not found'}), 404

    # Check already saved
    existing = execute_query(
        "SELECT id FROM saved_recommendations WHERE farmer_id = %s AND prediction_id = %s;",
        (user['id'], pred_id),
        fetchone=True
    )
    if existing:
        return jsonify({'success': True, 'message': 'Recommendation already saved in your bookmarks.'})

    execute_query(
        "INSERT INTO saved_recommendations (farmer_id, prediction_id, crop_name, notes) VALUES (%s, %s, %s, %s);",
        (user['id'], pred_id, pred['recommended_crop'], notes)
    )

    return jsonify({'success': True, 'message': f"Crop '{pred['recommended_crop']}' saved to your favorites!"})


@farmer_bp.route('/recommendations/saved', methods=['GET'])
@token_required
def get_saved_recommendations():
    user = request.current_user
    rows = execute_query(
        """SELECT s.id as saved_id, s.crop_name, s.notes, s.created_at as saved_at,
                  h.*
           FROM saved_recommendations s
           JOIN prediction_history h ON s.prediction_id = h.id
           WHERE s.farmer_id = %s
           ORDER BY s.created_at DESC;""",
        (user['id'],),
        fetchall=True
    ) or []

    return jsonify({'success': True, 'saved_crops': rows, 'total': len(rows)})


@farmer_bp.route('/recommendations/saved/<int:saved_id>', methods=['DELETE'])
@token_required
def remove_saved_recommendation(saved_id):
    user = request.current_user
    execute_query(
        "DELETE FROM saved_recommendations WHERE id = %s AND farmer_id = %s;",
        (saved_id, user['id'])
    )
    return jsonify({'success': True, 'message': 'Removed from saved recommendations.'})


@farmer_bp.route('/predictions/<int:pred_id>/report', methods=['GET'])
@token_required
def download_prediction_report(pred_id):
    user = request.current_user
    pred = execute_query(
        "SELECT * FROM prediction_history WHERE id = %s AND (farmer_id = %s OR %s = 'admin');",
        (pred_id, user['id'], user['role']),
        fetchone=True
    )
    if not pred:
        return jsonify({'success': False, 'message': 'Prediction record not found'}), 404

    profile = execute_query(
        "SELECT * FROM farmer_profiles WHERE user_id = %s;",
        (pred['farmer_id'],),
        fetchone=True
    ) or {}

    pdf_path = generate_crop_pdf_report(pred, profile)
    return send_file(pdf_path, as_attachment=True, download_name=f"crop_recommendation_report_{pred_id}.pdf")
