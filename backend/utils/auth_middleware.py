import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from backend.config import Config
from backend.db import execute_query


def generate_jwt_token(user_id, username, role):
    payload = {
        'user_id': user_id,
        'username': username,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, Config.JWT_SECRET, algorithm='HS256')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return jsonify({'success': False, 'message': 'Authorization header is missing'}), 401

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'success': False, 'message': 'Invalid token format. Expected Bearer <token>'}), 401

        token = parts[1]
        try:
            payload = jwt.decode(token, Config.JWT_SECRET, algorithms=['HS256'])
            user_id = payload['user_id']
            # Fetch user from DB
            user = execute_query("SELECT id, username, email, role FROM users WHERE id = %s;", (user_id,), fetchone=True)
            if not user:
                return jsonify({'success': False, 'message': 'User not found or account deactivated'}), 401

            request.current_user = user
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'message': 'Session expired. Please login again.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'message': 'Invalid authentication token.'}), 401
        except Exception as e:
            return jsonify({'success': False, 'message': f'Auth Error: {str(e)}'}), 401

        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(request, 'current_user') or request.current_user['role'] != 'admin':
            return jsonify({'success': False, 'message': 'Admin privileges required for this action'}), 403
        return f(*args, **kwargs)
    return decorated
