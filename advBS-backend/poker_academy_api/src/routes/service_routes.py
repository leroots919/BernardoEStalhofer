# src/routes/service_routes.py
import sys
import os

# Adiciona o diretório pai de 'src' (ou seja, 'poker_academy_api') ao sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request, current_app
from src.models import db, Services, ServiceCategory, Users, UserType
from src.auth import token_required, admin_required
from datetime import datetime
from sqlalchemy import desc

service_bp = Blueprint("service_bp", __name__)

# Rota de teste sem autenticação
@service_bp.route("/api/test", methods=["GET"])
def test_route():
    try:
        print("🧪 Rota de teste chamada!")

        # Testar conexão com banco
        all_services = Services.query.all()
        print(f"📊 Total de serviços: {len(all_services)}")

        return jsonify({
            "status": "OK",
            "message": "Backend funcionando",
            "total_services": len(all_services)
        }), 200
    except Exception as e:
        print(f"❌ Erro na rota de teste: {e}")
        return jsonify(error=str(e)), 500

# Rota para listar todos os serviços
@service_bp.route("/api/services", methods=["GET"])
@token_required
def get_all_services(current_user):
    try:
        print("🔍 Buscando serviços...")

        # Buscar todos os serviços ativos
        all_services = Services.query.filter_by(active=True).all()
        print(f"📊 Total de serviços: {len(all_services)}")

        result = [s.to_dict() for s in all_services]
        print(f"✅ Retornando {len(result)} serviços")

        return jsonify(result), 200
    except Exception as e:
        print(f"❌ Erro ao buscar serviços: {e}")
        current_app.logger.error(f"Erro ao buscar serviços: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar dados dos serviços."), 500

# Rota para buscar serviços por categoria
@service_bp.route("/api/services/category/<category>", methods=["GET"])
@token_required
def get_services_by_category(current_user, category):
    try:
        print(f"🔍 Buscando serviços da categoria: {category}")

        # Verificar se a categoria é válida
        valid_categories = [cat.value for cat in ServiceCategory]
        if category not in valid_categories:
            return jsonify(error="Categoria inválida"), 400

        services = Services.query.filter_by(category=category, active=True).all()
        result = [s.to_dict() for s in services]

        return jsonify(result), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar serviços por categoria: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar serviços por categoria"), 500

# Rota para criar um novo serviço (apenas admin)
@service_bp.route("/api/services", methods=["POST"])
@admin_required
def create_service(current_user):
    data = request.get_json()
    print(f"🔍 Dados recebidos para criar serviço: {data}")

    if not data:
        return jsonify(error="Dados não fornecidos"), 400

    # Campos obrigatórios básicos
    required_fields = ["name", "category"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify(error=f"Campo obrigatório ausente ou vazio: {field}"), 400

    try:
        new_service = Services(
            name=data["name"],
            description=data.get("description"),
            category=data["category"],
            price=data.get("price"),
            duration_days=data.get("duration_days"),
            active=data.get("active", True)
        )
        db.session.add(new_service)
        db.session.commit()
        return jsonify(new_service.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao criar serviço: {e}", exc_info=True)
        return jsonify(error=f"Erro ao criar novo serviço: {str(e)}"), 500

# Rota para atualizar um serviço (apenas admin)
@service_bp.route("/api/services/<int:service_id>", methods=["PUT"])
@admin_required
def update_service(current_user, service_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify(error="Dados não fornecidos"), 400

        service_to_update = Services.query.get(service_id)
        if not service_to_update:
            return jsonify(error="Serviço não encontrado"), 404

        # Campos que podem ser atualizados
        if "name" in data:
            service_to_update.name = data["name"]
        if "description" in data:
            service_to_update.description = data["description"]
        if "category" in data:
            service_to_update.category = data["category"]
        if "price" in data:
            service_to_update.price = data["price"]
        if "duration_days" in data:
            service_to_update.duration_days = data["duration_days"]
        if "active" in data:
            service_to_update.active = data["active"]

        db.session.commit()
        return jsonify(service_to_update.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao atualizar serviço: {e}", exc_info=True)
        return jsonify(error="Erro ao atualizar serviço"), 500

# Rota para deletar um serviço (apenas admin)
@service_bp.route("/api/services/<int:service_id>", methods=["DELETE"])
@admin_required
def delete_service(current_user, service_id):
    try:
        service_to_delete = Services.query.get(service_id)
        if not service_to_delete:
            return jsonify(error="Serviço não encontrado"), 404

        db.session.delete(service_to_delete)
        db.session.commit()
        return jsonify(message="Serviço deletado com sucesso"), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao deletar serviço: {e}", exc_info=True)
        return jsonify(error="Erro ao deletar serviço"), 500

# Rota para obter detalhes de um serviço específico
@service_bp.route("/api/services/<int:service_id>", methods=["GET"])
@token_required
def get_service_details(current_user, service_id):
    try:
        service = Services.query.get(service_id)
        if not service:
            return jsonify(error="Serviço não encontrado"), 404

        return jsonify(service.to_dict()), 200

    except Exception as e:
        current_app.logger.error(f"Erro ao buscar detalhes do serviço: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar detalhes do serviço"), 500

# Rota para listar categorias disponíveis
@service_bp.route("/api/services/categories", methods=["GET"])
def get_service_categories():
    try:
        categories = [{"value": cat.value, "name": cat.value.title()} for cat in ServiceCategory]
        return jsonify(categories), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar categorias: {e}", exc_info=True)
        return jsonify(error="Erro ao buscar categorias"), 500
