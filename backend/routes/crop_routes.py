from flask import Blueprint, request, jsonify
from backend.db import execute_query
from backend.utils.weather_service import get_weather_for_district, DISTRICT_CLIMATE_DEFAULTS

crop_bp = Blueprint('crop_bp', __name__)


@crop_bp.route('/crops', methods=['GET'])
def list_crops():
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()

    query = "SELECT * FROM crop_information WHERE 1=1"
    params = []

    if search:
        query += " AND (crop_name LIKE %s OR crop_category LIKE %s OR suitable_soil LIKE %s)"
        like_term = f"%{search}%"
        params.extend([like_term, like_term, like_term])

    if category and category.lower() != 'all':
        query += " AND crop_category LIKE %s"
        params.append(f"%{category}%")

    query += " ORDER BY crop_name ASC;"
    crops = execute_query(query, params, fetchall=True) or []

    # Get distinct categories
    categories_raw = execute_query("SELECT DISTINCT crop_category FROM crop_information ORDER BY crop_category ASC;", fetchall=True) or []
    categories = [c['crop_category'] for c in categories_raw]

    return jsonify({
        'success': True,
        'crops': crops,
        'total': len(crops),
        'categories': categories
    })


@crop_bp.route('/crops/<identifier>', methods=['GET'])
def get_crop(identifier):
    if identifier.isdigit():
        crop = execute_query("SELECT * FROM crop_information WHERE id = %s;", (int(identifier),), fetchone=True)
    else:
        crop = execute_query("SELECT * FROM crop_information WHERE LOWER(crop_name) = LOWER(%s);", (identifier,), fetchone=True)

    if not crop:
        return jsonify({'success': False, 'message': 'Crop details not found'}), 404

    return jsonify({'success': True, 'crop': crop})


@crop_bp.route('/districts', methods=['GET'])
def get_districts():
    district_list = []
    for d, info in DISTRICT_CLIMATE_DEFAULTS.items():
        district_list.append({
            'name': d,
            'state': info['state'],
            'default_temperature': info['temperature'],
            'default_humidity': info['humidity'],
            'default_rainfall': info['rainfall']
        })
    district_list.sort(key=lambda x: x['name'])
    return jsonify({'success': True, 'districts': district_list})


@crop_bp.route('/weather/current', methods=['GET'])
def get_current_weather():
    district = request.args.get('district', 'Madurai').strip()
    weather_info = get_weather_for_district(district)
    return jsonify({'success': True, 'weather': weather_info})
