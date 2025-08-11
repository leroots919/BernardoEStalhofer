# src/routes/upload_routes.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, request, current_app, send_from_directory
from src.models import db, ClientCases
from src.auth import token_required
from datetime import datetime
from werkzeug.utils import secure_filename
import uuid

upload_bp = Blueprint("upload_bp", __name__)

# Configurações de upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads', 'documents')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'txt', 'zip', 'rar'}

# Criar pasta de upload se não existir
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
print(f"Pasta de upload de documentos: {UPLOAD_FOLDER}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rota para upload de documentos do cliente
@upload_bp.route("/api/upload/document", methods=["POST"])
@token_required
def upload_document(current_user):
    try:
        if 'document' not in request.files:
            return jsonify(error="Nenhum arquivo enviado"), 400

        file = request.files['document']
        case_id = request.form.get('case_id')
        description = request.form.get('description', '')

        if file.filename == '':
            return jsonify(error="Nenhum arquivo selecionado"), 400

        if not allowed_file(file.filename):
            return jsonify(error="Tipo de arquivo não permitido"), 400

        # Verificar se o caso pertence ao usuário (se case_id fornecido)
        if case_id:
            case = ClientCases.query.filter_by(id=case_id, user_id=current_user.id).first()
            if not case:
                return jsonify(error="Caso não encontrado"), 404

        # Gerar nome único para o arquivo
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

        # Salvar arquivo
        file.save(file_path)

        # Criar registro no banco (você pode criar uma tabela Documents se quiser)
        # Por enquanto, vou retornar as informações do upload
        
        return jsonify({
            "message": "Arquivo enviado com sucesso",
            "filename": filename,
            "unique_filename": unique_filename,
            "file_size": os.path.getsize(file_path),
            "upload_date": datetime.utcnow().isoformat(),
            "description": description,
            "case_id": case_id
        }), 200

    except Exception as e:
        current_app.logger.error(f"Erro no upload: {e}", exc_info=True)
        return jsonify(error="Erro ao fazer upload do arquivo"), 500

# Rota para listar documentos do cliente
@upload_bp.route("/api/upload/documents", methods=["GET"])
@token_required
def list_user_documents(current_user):
    try:
        # Por enquanto, retornar lista vazia
        # Você pode implementar uma tabela Documents para armazenar metadados
        return jsonify([]), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao listar documentos: {e}", exc_info=True)
        return jsonify(error="Erro ao listar documentos"), 500

# Rota para download de documento
@upload_bp.route("/api/upload/download/<filename>", methods=["GET"])
@token_required
def download_document(current_user, filename):
    try:
        # Verificar se o arquivo existe e pertence ao usuário
        # Por segurança, você deve implementar verificação de propriedade
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    except Exception as e:
        current_app.logger.error(f"Erro no download: {e}", exc_info=True)
        return jsonify(error="Arquivo não encontrado"), 404

# Rota para deletar documento
@upload_bp.route("/api/upload/document/<filename>", methods=["DELETE"])
@token_required
def delete_document(current_user, filename):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify(message="Arquivo deletado com sucesso"), 200
        else:
            return jsonify(error="Arquivo não encontrado"), 404
            
    except Exception as e:
        current_app.logger.error(f"Erro ao deletar arquivo: {e}", exc_info=True)
        return jsonify(error="Erro ao deletar arquivo"), 500
