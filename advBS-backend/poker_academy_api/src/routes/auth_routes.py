# src/routes/auth_routes.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request, current_app
from src.models import db, Users, UserType
from src.auth import AuthService
from datetime import datetime

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    """Login endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"error": "Email e senha são obrigatórios"}), 400
        
        # Authenticate user
        user = AuthService.authenticate_user(email, password)
        if not user:
            return jsonify({"error": "Email ou senha inválidos"}), 401
        
        # Generate token
        token = AuthService.generate_token(user.id, user.type.value)
        
        return jsonify({
            "message": "Login realizado com sucesso",
            "token": token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "type": user.type.value,
                "last_login": user.last_login.isoformat() if user.last_login else None
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro no login: {e}", exc_info=True)
        return jsonify({"error": "Erro interno do servidor"}), 500

@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    """Register new user endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        required_fields = ["name", "email", "password"]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Campo obrigatório: {field}"}), 400
        
        # Check if user already exists
        if Users.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email já cadastrado"}), 409
        
        if Users.query.filter_by(name=data["name"]).first():
            return jsonify({"error": "Nome de usuário já cadastrado"}), 409
        
        # Hash password
        hashed_password = AuthService.hash_password(data["password"])
        
        # Create new user
        new_user = Users(
            name=data["name"],
            email=data["email"],
            password_hash=hashed_password,
            type=UserType.cliente,  # Default to cliente
            register_date=datetime.utcnow()
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Generate token for immediate login
        token = AuthService.generate_token(new_user.id, new_user.type.value)
        
        return jsonify({
            "message": "Usuário criado com sucesso",
            "token": token,
            "user": {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email,
                "type": new_user.type.value,
                "register_date": new_user.register_date.isoformat()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro no registro: {e}", exc_info=True)
        return jsonify({"error": "Erro interno do servidor"}), 500

@auth_bp.route("/api/auth/verify", methods=["GET"])
def verify_token():
    """Verify token endpoint"""
    try:
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Token format invalid'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        payload = AuthService.verify_token(token)
        if payload is None:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        user = Users.query.get(payload['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 401
        
        return jsonify({
            "valid": True,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "type": user.type.value,
                "last_login": user.last_login.isoformat() if user.last_login else None
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro na verificação do token: {e}", exc_info=True)
        return jsonify({"error": "Erro interno do servidor"}), 500

@auth_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    """Logout endpoint (client-side token removal)"""
    return jsonify({"message": "Logout realizado com sucesso"}), 200
