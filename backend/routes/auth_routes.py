from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from backend.db import execute_query
from backend.utils.auth_middleware import generate_jwt_token, token_required

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    full_name = data.get('full_name', '').strip()
    username = data.get('username', '').strip().lower()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    phone = data.get('phone', '').strip()
    district = data.get('district', 'Madurai').strip()
    state = data.get('state', 'Tamil Nadu').strip()
    farm_area = float(data.get('farm_area', 2.0) or 2.0)
    preferred_language = data.get('preferred_language', 'English').strip()

    if not username or not email or not password or not full_name:
        return jsonify({'success': False, 'message': 'Full name, username, email, and password are required.'}), 400

    if len(password) < 6:
        return jsonify({'success': False, 'message': 'Password must be at least 6 characters.'}), 400

    # Check for duplicate username or email
    existing = execute_query(
        "SELECT id, username, email FROM users WHERE username = %s OR email = %s;",
        (username, email),
        fetchone=True
    )
    if existing:
        if existing['username'] == username:
            return jsonify({'success': False, 'message': 'Username is already taken. Please choose another.'}), 409
        return jsonify({'success': False, 'message': 'Email address is already registered.'}), 409

    # Create user & profile
    pwd_hash = generate_password_hash(password)
    user_id = execute_query(
        "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, 'farmer');",
        (username, email, pwd_hash),
        insert=True
    )

    execute_query(
        """INSERT INTO farmer_profiles (user_id, full_name, phone, district, state, farm_area, preferred_language)
           VALUES (%s, %s, %s, %s, %s, %s, %s);""",
        (user_id, full_name, phone, district, state, farm_area, preferred_language)
    )

    token = generate_jwt_token(user_id, username, 'farmer')

    return jsonify({
        'success': True,
        'message': 'Farmer registered successfully! Welcome to AI Farmer.',
        'token': token,
        'user': {
            'id': user_id,
            'username': username,
            'email': email,
            'role': 'farmer',
            'full_name': full_name,
            'district': district,
            'state': state,
            'farm_area': farm_area,
            'preferred_language': preferred_language
        }
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    identifier = data.get('username', '').strip().lower() # can be username or email
    password = data.get('password', '')

    if not identifier or not password:
        return jsonify({'success': False, 'message': 'Please provide username/email and password.'}), 400

    user = execute_query(
        "SELECT id, username, email, password_hash, role FROM users WHERE username = %s OR email = %s;",
        (identifier, identifier),
        fetchone=True
    )

    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'success': False, 'message': 'Invalid username or password.'}), 401

    profile = execute_query(
        "SELECT full_name, phone, district, state, farm_area, preferred_language FROM farmer_profiles WHERE user_id = %s;",
        (user['id'],),
        fetchone=True
    ) or {}

    token = generate_jwt_token(user['id'], user['username'], user['role'])

    return jsonify({
        'success': True,
        'message': f"Welcome back, {profile.get('full_name', user['username'])}!",
        'token': token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role'],
            'full_name': profile.get('full_name', user['username']),
            'phone': profile.get('phone', ''),
            'district': profile.get('district', 'Madurai'),
            'state': profile.get('state', 'Tamil Nadu'),
            'farm_area': profile.get('farm_area', 2.5),
            'preferred_language': profile.get('preferred_language', 'English')
        }
    })


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user():
    user = request.current_user
    profile = execute_query(
        "SELECT full_name, phone, district, state, farm_area, preferred_language FROM farmer_profiles WHERE user_id = %s;",
        (user['id'],),
        fetchone=True
    ) or {}

    return jsonify({
        'success': True,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role'],
            'full_name': profile.get('full_name', user['username']),
            'phone': profile.get('phone', ''),
            'district': profile.get('district', 'Madurai'),
            'state': profile.get('state', 'Tamil Nadu'),
            'farm_area': profile.get('farm_area', 2.5),
            'preferred_language': profile.get('preferred_language', 'English')
        }
    })


@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'success': True, 'message': 'Logged out successfully.'})
