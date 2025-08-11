# src/routes/admin_routes.py
from flask import Blueprint, request, jsonify, current_app
from src.models import db, Users, ClientCases, ProcessFiles, UserType, CaseStatus
from src.auth import AuthService
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

print("🔥 ADMIN_ROUTES.PY CARREGADO - VERSÃO NOVA!")

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator para verificar se o usuário é admin"""
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
            if not user or user.type != UserType.admin:
                return jsonify({'error': 'Admin access required'}), 403
            
            request.current_user = user
            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.error(f"Erro na verificação de admin: {e}", exc_info=True)
            return jsonify({"error": "Erro interno do servidor"}), 500
    
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route("/api/admin/clients", methods=["GET"])
@admin_required
def get_clients():
    """Listar todos os clientes"""
    try:
        print("🔍 Requisição GET /api/admin/clients recebida")
        clients = Users.query.filter_by(type=UserType.cliente).all()
        print(f"📊 Encontrados {len(clients)} clientes")
        return jsonify([client.to_dict() for client in clients]), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar clientes: {e}", exc_info=True)
        return jsonify({"error": "Erro interno do servidor"}), 500

@admin_bp.route("/api/admin/clients", methods=["POST"])
@admin_required
def create_client():
    """Criar novo cliente"""
    try:
        data = request.get_json()
        
        # Verificar se email já existe
        existing_user = Users.query.filter_by(email=data["email"]).first()
        if existing_user:
            return jsonify({"error": "Email já cadastrado"}), 409
        
        # Criar senha padrão se não fornecida
        password = data.get("password", "123456")
        hashed_password = generate_password_hash(password)
        
        # Criar novo cliente
        new_client = Users(
            name=data["name"],
            email=data["email"],
            password_hash=hashed_password,
            type=UserType.cliente,
            cpf=data.get("cpf"),
            phone=data.get("phone"),
            address=data.get("address"),
            city=data.get("city"),
            state=data.get("state"),
            zip_code=data.get("zip_code"),
            register_date=datetime.utcnow()
        )
        
        db.session.add(new_client)
        db.session.commit()
        
        return jsonify({
            "message": "Cliente criado com sucesso",
            "client": new_client.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao criar cliente: {e}", exc_info=True)
        return jsonify({"error": "Erro interno do servidor"}), 500

@admin_bp.route("/api/admin/clients/<int:client_id>", methods=["PUT"])
@admin_required
def update_client(client_id):
    """Atualizar cliente"""
    try:
        client = Users.query.get_or_404(client_id)
        data = request.get_json()
        
        # Verificar se email já existe em outro usuário
        if data.get("email") and data["email"] != client.email:
            existing_user = Users.query.filter_by(email=data["email"]).first()
            if existing_user:
                return jsonify({"error": "Email já cadastrado"}), 409
        
        # Atualizar campos
        if "name" in data:
            client.name = data["name"]
        if "email" in data:
            client.email = data["email"]
        if "cpf" in data:
            client.cpf = data["cpf"]
        if "phone" in data:
            client.phone = data["phone"]
        if "address" in data:
            client.address = data["address"]
        if "city" in data:
            client.city = data["city"]
        if "state" in data:
            client.state = data["state"]
        if "zip_code" in data:
            client.zip_code = data["zip_code"]
        
        db.session.commit()
        
        return jsonify({
            "message": "Cliente atualizado com sucesso",
            "client": client.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao atualizar cliente: {e}", exc_info=True)
        return jsonify({"error": "Erro interno do servidor"}), 500

@admin_bp.route("/api/admin/clients/<int:client_id>", methods=["DELETE"])
@admin_required
def delete_client(client_id):
    """Excluir cliente"""
    try:
        client = Users.query.get_or_404(client_id)
        
        if client.type != UserType.cliente:
            return jsonify({"error": "Usuário não é um cliente"}), 400
        
        db.session.delete(client)
        db.session.commit()
        
        return jsonify({"message": "Cliente excluído com sucesso"}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao excluir cliente: {e}", exc_info=True)
        return jsonify({"error": "Erro interno do servidor"}), 500

@admin_bp.route("/api/admin/cases", methods=["GET"])
@admin_required
def get_cases():
    """Listar todos os casos"""
    try:
        print("🔍 Requisição GET /api/admin/cases recebida")
        cases = ClientCases.query.all()
        print(f"📊 Encontrados {len(cases)} casos")
        return jsonify([{
            'id': case.id,
            'user_id': case.user_id,
            'title': case.title,
            'description': case.description,
            'status': case.status.value,
            'created_at': case.created_at.isoformat(),
            'updated_at': case.updated_at.isoformat()
        } for case in cases]), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar casos: {e}", exc_info=True)
        return jsonify({"error": "Erro interno do servidor"}), 500

@admin_bp.route("/api/admin/process-files", methods=["GET"])
@admin_required
def get_process_files():
    """Listar todos os arquivos de processo"""
    try:
        files = ProcessFiles.query.all()
        return jsonify([file.to_dict() for file in files]), 200
    except Exception as e:
        current_app.logger.error(f"Erro ao buscar arquivos: {e}", exc_info=True)
        return jsonify({"error": "Erro interno do servidor"}), 500

@admin_bp.route("/api/admin/process-files", methods=["POST"])
@admin_required
def upload_process_file():
    """Upload de arquivo de processo"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Nenhum arquivo enviado"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "Nenhum arquivo selecionado"}), 400
        
        client_id = request.form.get('client_id')
        case_id = request.form.get('case_id') or None
        description = request.form.get('description', '')
        
        if not client_id:
            return jsonify({"error": "ID do cliente é obrigatório"}), 400
        
        # Verificar se cliente existe
        client = Users.query.get(client_id)
        if not client or client.type != UserType.cliente:
            return jsonify({"error": "Cliente não encontrado"}), 404
        
        # Criar diretório se não existir
        upload_dir = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'uploads'), 'process_files')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Salvar arquivo
        filename = secure_filename(file.filename)
        unique_filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{filename}"
        file_path = os.path.join(upload_dir, unique_filename)
        file.save(file_path)
        
        # Salvar no banco
        process_file = ProcessFiles(
            user_id=client_id,
            case_id=case_id,
            filename=unique_filename,
            original_filename=filename,
            file_path=file_path,
            description=description,
            uploaded_by_admin=request.current_user.id,
            created_at=datetime.utcnow()
        )
        
        db.session.add(process_file)
        db.session.commit()
        
        return jsonify({
            "message": "Arquivo enviado com sucesso",
            "file": process_file.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao fazer upload: {e}", exc_info=True)
        return jsonify({"error": "Erro interno do servidor"}), 500

@admin_bp.route("/api/admin/process-files/<int:file_id>", methods=["DELETE"])
@admin_required
def delete_process_file(file_id):
    """Excluir arquivo de processo"""
    try:
        process_file = ProcessFiles.query.get_or_404(file_id)
        
        # Excluir arquivo físico
        if os.path.exists(process_file.file_path):
            os.remove(process_file.file_path)
        
        db.session.delete(process_file)
        db.session.commit()
        
        return jsonify({"message": "Arquivo excluído com sucesso"}), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao excluir arquivo: {e}", exc_info=True)
        return jsonify({"error": "Erro interno do servidor"}), 500

# Rotas específicas para casos de clientes
@admin_bp.route("/api/admin/clients/<int:client_id>/cases", methods=["GET"])
@admin_required
def get_client_cases(client_id):
    """Buscar casos de um cliente específico"""
    try:
        client = Users.query.get_or_404(client_id)

        if client.type != UserType.cliente:
            return jsonify({"error": "Usuário não é um cliente"}), 400

        cases = ClientCases.query.filter_by(user_id=client_id).all()

        return jsonify([{
            'id': case.id,
            'title': case.title,
            'description': case.description,
            'status': case.status.value,
            'created_at': case.created_at.isoformat(),
            'updated_at': case.updated_at.isoformat()
        } for case in cases]), 200

    except Exception as e:
        current_app.logger.error(f"Erro ao buscar casos do cliente: {e}", exc_info=True)
        return jsonify({"error": "Erro interno do servidor"}), 500

@admin_bp.route("/api/admin/clients/<int:client_id>/cases", methods=["POST"])
@admin_required
def create_client_case(client_id):
    """Criar novo caso para um cliente"""
    print(f"🔥 FUNÇÃO EXECUTADA! Cliente ID: {client_id}")

    try:
        print(f"🔍 Iniciando criação de caso para cliente {client_id}")

        # Verificar se cliente existe
        client = Users.query.get(client_id)
        if not client:
            print(f"❌ Cliente {client_id} não encontrado")
            return jsonify({"error": "Cliente não encontrado"}), 404

        print(f"✅ Cliente encontrado: {client.name}")

        data = request.get_json() or {}
        print(f"🔍 Dados recebidos: {data}")

        # Usar dados do request ou valores padrão
        title = data.get('title', 'Caso de Teste')
        description = data.get('description', 'Descrição de teste')
        service_id = data.get('service_id', 1)
        status = data.get('status', 'pendente')

        print(f"🔍 Dados processados: title={title}, service_id={service_id}, status={status}")

        # Verificar se serviço existe
        from src.models import Services
        service = Services.query.get(service_id)
        if not service:
            print(f"❌ Serviço {service_id} não encontrado")
            return jsonify({"error": "Serviço não encontrado"}), 404

        print(f"✅ Serviço encontrado: {service.name}")

        # Criar novo caso
        print("🔍 Criando objeto ClientCases...")
        new_case = ClientCases(
            user_id=client_id,
            service_id=service_id,
            title=title,
            description=description,
            status=CaseStatus(status)
        )
        print("✅ Objeto ClientCases criado")

        print("🔍 Salvando caso no banco...")
        db.session.add(new_case)
        db.session.commit()
        print("✅ Caso salvo com sucesso!")

        return jsonify({
            'id': new_case.id,
            'title': new_case.title,
            'description': new_case.description,
            'status': new_case.status.value,
            'created_at': new_case.created_at.isoformat(),
            'message': 'Caso criado com sucesso'
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro detalhado ao criar caso: {str(e)}")
        print(f"❌ Tipo do erro: {type(e)}")
        import traceback
        traceback.print_exc()
        current_app.logger.error(f"Erro ao criar caso: {e}", exc_info=True)
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

# Rota de teste sem autenticação
@admin_bp.route("/test", methods=["GET"])
def test_route():
    """Rota de teste"""
    print("🔍 Rota de teste acessada!")
    return jsonify({"message": "Rota de teste funcionando!"}), 200

@admin_bp.route("/api/admin/test-case", methods=["POST"])
@admin_required
def test_case_creation():
    """Rota de teste para criação de casos"""
    print("🔍 Rota de teste de criação de casos acessada!")
    return jsonify({"message": "Rota de teste de casos funcionando!"}), 200

@admin_bp.route("/api/admin/simple-test", methods=["POST"])
def simple_test():
    """Rota de teste simples sem autenticação"""
    print("🔍 Rota de teste simples acessada!")
    return jsonify({"message": "Rota simples funcionando!"}), 200

@admin_bp.route("/api/admin/create-case-simple", methods=["POST"])
@admin_required
def create_case_simple():
    """Rota simplificada para criar casos"""
    try:
        print("🔍 Iniciando criação de caso simples...")

        # Dados fixos para teste
        client_id = 2
        service_id = 1
        title = "Caso de Teste"
        description = "Descrição de teste"
        status = "pendente"

        print(f"🔍 Dados: client_id={client_id}, service_id={service_id}")

        # Criar novo caso
        new_case = ClientCases(
            user_id=client_id,
            service_id=service_id,
            title=title,
            description=description,
            status=CaseStatus.pendente
        )

        print("🔍 Objeto criado, salvando...")
        db.session.add(new_case)
        db.session.commit()
        print("🔍 Salvo com sucesso!")

        return jsonify({
            'id': new_case.id,
            'message': 'Caso criado com sucesso'
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro: {str(e)}")
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/api/admin/novo-caso", methods=["POST"])
@admin_required
def novo_caso():
    """Nova rota para criar casos"""
    print("🔥🔥🔥 NOVA ROTA EXECUTADA! 🔥🔥🔥")

    try:
        print("🔍 NOVA ROTA - Iniciando criação de caso...")

        data = request.get_json() or {}
        client_id = data.get('client_id', 2)

        # Usar dados do request ou valores padrão
        title = data.get('title', 'Novo Caso de Teste')
        description = data.get('description', 'Nova descrição de teste')
        service_id = data.get('service_id', 1)
        status = data.get('status', 'pendente')

        print(f"🔍 NOVA ROTA - Dados: client_id={client_id}, title={title}, service_id={service_id}")

        # Criar novo caso
        new_case = ClientCases(
            user_id=client_id,
            service_id=service_id,
            title=title,
            description=description,
            status=CaseStatus(status)
        )

        print("🔍 NOVA ROTA - Salvando caso...")
        db.session.add(new_case)
        db.session.commit()
        print("🔍 NOVA ROTA - Caso salvo com sucesso!")

        return jsonify({
            'id': new_case.id,
            'title': new_case.title,
            'description': new_case.description,
            'status': new_case.status.value,
            'created_at': new_case.created_at.isoformat(),
            'message': 'Caso criado com sucesso pela nova rota'
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"❌ NOVA ROTA - Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/api/admin/test-simple-case", methods=["POST"])
def test_simple_case():
    """Rota de teste super simples para casos"""
    print("🔥🔥🔥 TESTE SIMPLES EXECUTADO! 🔥🔥🔥")
    return jsonify({"message": "Teste simples funcionando!"}), 200
