#!/usr/bin/env python3
"""
Script de teste simples para verificar se o servidor está funcionando
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
from werkzeug.security import check_password_hash

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"], methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
app.config['SECRET_KEY'] = 'poker-academy-secret-key-2024'

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({
        "message": "Backend funcionando",
        "status": "OK"
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Dados não fornecidos"}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"error": "Email e senha são obrigatórios"}), 400
        
        # Conectar ao banco
        db_path = "poker_academy.db"
        if not os.path.exists(db_path):
            return jsonify({"error": "Banco de dados não encontrado"}), 500
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Buscar usuário
        cursor.execute("SELECT id, name, email, password_hash, type FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return jsonify({"error": "Email ou senha inválidos"}), 401
        
        user_id, name, user_email, password_hash, user_type = user
        
        # Verificar senha
        if not check_password_hash(password_hash, password):
            conn.close()
            return jsonify({"error": "Email ou senha inválidos"}), 401
        
        conn.close()
        
        # Simular token (simplificado para teste)
        token = f"test-token-{user_id}"
        
        return jsonify({
            "message": "Login realizado com sucesso",
            "token": token,
            "user": {
                "id": user_id,
                "name": name,
                "email": user_email,
                "type": user_type
            }
        }), 200
        
    except Exception as e:
        print(f"Erro no login: {e}")
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    """Rota para buscar usuários (para área admin)"""
    try:
        # Conectar ao banco
        db_path = "poker_academy.db"
        if not os.path.exists(db_path):
            return jsonify({"error": "Banco de dados não encontrado"}), 500

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Buscar apenas estudantes
        cursor.execute("SELECT id, name, email, type, register_date FROM users WHERE type = 'student'")
        users = cursor.fetchall()

        conn.close()

        users_list = []
        for user in users:
            user_id, name, email, user_type, register_date = user
            users_list.append({
                "id": user_id,
                "name": name,
                "email": email,
                "type": user_type,
                "register_date": register_date
            })

        return jsonify(users_list), 200

    except Exception as e:
        print(f"Erro ao buscar usuários: {e}")
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/classes', methods=['GET'])
def get_classes():
    """Rota para buscar aulas"""
    try:
        # Conectar ao banco
        db_path = "poker_academy.db"
        if not os.path.exists(db_path):
            return jsonify({"error": "Banco de dados não encontrado"}), 500

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Buscar aulas
        cursor.execute("SELECT id, name, description, instructor, video_path, created_at FROM classes")
        classes = cursor.fetchall()

        conn.close()

        classes_list = []
        for class_data in classes:
            class_id, name, description, instructor, video_path, created_at = class_data
            classes_list.append({
                "id": class_id,
                "name": name,
                "description": description,
                "instructor": instructor,
                "video_path": video_path,
                "created_at": created_at
            })

        return jsonify(classes_list), 200

    except Exception as e:
        print(f"Erro ao buscar aulas: {e}")
        return jsonify({"error": f"Erro interno: {str(e)}"}), 500

@app.route('/api/auth/verify', methods=['GET'])
def verify_token():
    """Verificar token (simplificado)"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token is missing'}), 401

        token = auth_header.split(' ')[1]

        # Verificação simplificada do token
        if token.startswith('test-token-'):
            user_id = token.replace('test-token-', '')

            # Buscar usuário
            db_path = "poker_academy.db"
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT id, name, email, type FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()

            if user:
                user_id, name, email, user_type = user
                return jsonify({
                    "valid": True,
                    "user": {
                        "id": user_id,
                        "name": name,
                        "email": email,
                        "type": user_type
                    }
                }), 200

        return jsonify({'error': 'Token is invalid'}), 401

    except Exception as e:
        print(f"Erro na verificação do token: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

if __name__ == '__main__':
    print("🚀 Iniciando servidor de teste...")
    print("📍 Backend: http://localhost:5000")
    print("🧪 Teste: http://localhost:5000/api/test")
    print()
    print("📋 Credenciais:")
    print("   Admin: admin@pokeracademy.com / admin123")
    print("   Student: student@pokeracademy.com / student123")
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
