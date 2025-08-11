# src/routes/client_routes.py
from flask import Blueprint, request, jsonify, current_app, send_file
from src.models import db, Users, ClientCases, ProcessFiles, UserType
from src.auth import AuthService
from datetime import datetime
import os

client_bp = Blueprint('client', __name__)

def client_required(f):
    """Decorator para verificar se o usuário é cliente"""
    def decorated_function(*args, **kwargs):
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
            if not user or user.type != UserType.cliente:
                return jsonify({'error': 'Client access required'}), 403
            
            request.current_user = user
            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"Erro na verificação de cliente: {e}", exc_info=True)
            return jsonify({"error": "Erro interno do servidor"}), 500
    
    decorated_function.__name__ = f.__name__
    return decorated_function

@client_bp.route("/api/client/profile", methods=["GET"])
@client_required
def get_profile():
    """Obter perfil do cliente"""
    try:
        return jsonify(request.current_user.to_dict()), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar perfil: {e}", exc_info=True)
        return jsonify({"error": "Erro interno do servidor"}), 500

@client_bp.route("/api/client/profile", methods=["PUT"])
@client_required
def update_profile():
    """Atualizar perfil do cliente"""
    try:
        data = request.get_json()
        user = request.current_user
        
        # Verificar se email já existe em outro usuário
        if data.get("email") and data["email"] != user.email:
            existing_user = Users.query.filter_by(email=data["email"]).first()
            if existing_user:
                return jsonify({"error": "Email já cadastrado"}), 409
        
        # Atualizar campos permitidos
        if "name" in data:
            user.name = data["name"]
        if "email" in data:
            user.email = data["email"]
        if "cpf" in data:
            user.cpf = data["cpf"]
        if "phone" in data:
            user.phone = data["phone"]
        if "address" in data:
            user.address = data["address"]
        if "city" in data:
            user.city = data["city"]
        if "state" in data:
            user.state = data["state"]
        if "zip_code" in data:
            user.zip_code = data["zip_code"]
        
        db.session.commit()
        
        return jsonify({
            "message": "Perfil atualizado com sucesso",
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao atualizar perfil: {e}", exc_info=True)
        return jsonify({"error": "Erro interno do servidor"}), 500

@client_bp.route("/api/client/cases", methods=["GET"])
@client_required
def get_my_cases():
    """Obter casos do cliente"""
    try:
        cases = ClientCases.query.filter_by(user_id=request.current_user.id).all()
        
        cases_data = []
        for case in cases:
            # Buscar arquivos relacionados ao caso
            case_files = ProcessFiles.query.filter_by(
                user_id=request.current_user.id,
                case_id=case.id
            ).all()
            
            case_data = {
                'id': case.id,
                'title': case.title,
                'description': case.description,
                'status': case.status.value,
                'created_at': case.created_at.isoformat(),
                'updated_at': case.updated_at.isoformat(),
                'files': [file.to_dict() for file in case_files]
            }
            cases_data.append(case_data)
        
        return jsonify(cases_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar casos: {e}", exc_info=True)
        return jsonify({"error": "Erro interno do servidor"}), 500

@client_bp.route("/api/client/files", methods=["GET"])
@client_required
def get_my_files():
    """Obter arquivos do cliente"""
    try:
        files = ProcessFiles.query.filter_by(user_id=request.current_user.id).all()
        
        files_data = []
        for file in files:
            file_data = file.to_dict()
            
            # Adicionar informações do caso se existir
            if file.case_id:
                case = ClientCases.query.get(file.case_id)
                if case:
                    file_data['case_title'] = case.title
                    file_data['case_status'] = case.status.value
            
            files_data.append(file_data)
        
        return jsonify(files_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar arquivos: {e}", exc_info=True)
        return jsonify({"error": "Erro interno do servidor"}), 500

@client_bp.route("/api/client/files/<int:file_id>/download", methods=["GET"])
@client_required
def download_file(file_id):
    """Download de arquivo do cliente"""
    try:
        file = ProcessFiles.query.filter_by(
            id=file_id,
            user_id=request.current_user.id
        ).first()
        
        if not file:
            return jsonify({"error": "Arquivo não encontrado"}), 404
        
        if not os.path.exists(file.file_path):
            return jsonify({"error": "Arquivo não encontrado no servidor"}), 404
        
        return send_file(
            file.file_path,
            as_attachment=True,
            download_name=file.original_filename
        )
        
    except Exception as e:
        current_app.logger.error(f"Erro ao fazer download: {e}", exc_info=True)
        return jsonify({"error": "Erro interno do servidor"}), 500

@client_bp.route("/api/client/stats", methods=["GET"])
@client_required
def get_stats():
    """Obter estatísticas do cliente"""
    try:
        user_id = request.current_user.id
        
        # Contar casos por status
        total_cases = ClientCases.query.filter_by(user_id=user_id).count()
        pending_cases = ClientCases.query.filter_by(user_id=user_id).filter(
            ClientCases.status == 'pendente'
        ).count()
        active_cases = ClientCases.query.filter_by(user_id=user_id).filter(
            ClientCases.status == 'em_andamento'
        ).count()
        completed_cases = ClientCases.query.filter_by(user_id=user_id).filter(
            ClientCases.status == 'concluido'
        ).count()
        
        # Contar arquivos
        total_files = ProcessFiles.query.filter_by(user_id=user_id).count()
        
        stats = {
            'total_cases': total_cases,
            'pending_cases': pending_cases,
            'active_cases': active_cases,
            'completed_cases': completed_cases,
            'total_files': total_files
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar estatísticas: {e}", exc_info=True)
        return jsonify({"error": "Erro interno do servidor"}), 500
