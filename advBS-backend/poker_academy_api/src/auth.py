# src/auth.py
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from src.models import Users, db

class AuthService:
    @staticmethod
    def hash_password(password):
        """Hash a password using werkzeug"""
        return generate_password_hash(password, method='pbkdf2:sha256')

    @staticmethod
    def verify_password(password, hashed_password):
        """Verify a password against its hash"""
        return check_password_hash(hashed_password, password)
    
    @staticmethod
    def generate_token(user_id, user_type):
        """Generate JWT token for user"""
        payload = {
            'user_id': user_id,
            'user_type': user_type,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_token(token):
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def authenticate_user(email_or_username, password):
        """Authenticate user with email/username and password"""
        # Try to find user by email or username
        user = Users.query.filter(
            (Users.email == email_or_username) | (Users.username == email_or_username)
        ).first()

        if user and AuthService.verify_password(password, user.password_hash):
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()
            return user
        return None

def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Token format invalid'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            payload = AuthService.verify_token(token)
            if payload is None:
                return jsonify({'error': 'Token is invalid or expired'}), 401
            
            current_user = Users.query.get(payload['user_id'])
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
                
        except Exception as e:
            return jsonify({'error': 'Token verification failed'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Token format invalid'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            payload = AuthService.verify_token(token)
            if payload is None:
                return jsonify({'error': 'Token is invalid or expired'}), 401
            
            current_user = Users.query.get(payload['user_id'])
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
            
            if current_user.type.value != 'admin':
                return jsonify({'error': 'Admin access required'}), 403
                
        except Exception as e:
            return jsonify({'error': 'Token verification failed'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated
