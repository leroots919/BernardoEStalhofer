# src/main.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_cors import CORS

project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(project_folder, ".env"))

from src.routes.user_routes import user_bp
from src.routes.auth_routes import auth_bp
from src.routes.favorites_routes import favorites_bp
from src.routes.upload_routes import upload_bp
from src.routes.admin_routes import admin_bp
print("✅ Admin blueprint importado com sucesso")
from src.routes.client_routes import client_bp
from src.models import db, Services
from src.routes.service_routes import service_bp

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:3001"], supports_credentials=True)

# Configuração do banco de dados MySQL
DB_USERNAME = os.getenv("DB_USERNAME", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "BS")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")

# Configuração do banco de dados MySQL (como estava antes)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024  # 500MB max file size
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")

db.init_app(app)

app.register_blueprint(service_bp)
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(favorites_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(admin_bp)
print("✅ Admin blueprint registrado com sucesso")
app.register_blueprint(client_bp)

@app.route("/")
def home():
    return jsonify(message="Bem-vindo à API da Poker Academy!")

@app.route("/api/health")
def health_check():
    return jsonify(status="ok", message="API está funcionando!")

@app.route("/debug/routes")
def list_routes():
    """Listar todas as rotas registradas"""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'rule': rule.rule
        })
    return jsonify(routes)

@app.route("/api/admin/test-direct")
def test_direct():
    """Rota de teste direta"""
    return jsonify({"message": "Rota direta funcionando!"})

@app.route("/api/admin/test-case-direct", methods=["POST"])
def test_case_direct():
    """Rota de teste direta para casos"""
    return jsonify({"message": "Rota direta de casos funcionando!"})

@app.route("/api/create-case-public", methods=["POST"])
def create_case_public():
    """Rota pública de criação de casos para teste"""
    try:
        from src.models import ClientCases, CaseStatus, Users
        from flask import request

        # Obter dados do request
        data = request.get_json() or {}

        # Extrair dados
        client_id = data.get('client_id')
        service_id = data.get('service_id', 1)
        title = data.get('title', 'Novo Processo')
        description = data.get('description', '')
        status = data.get('status', 'pendente')

        print(f"🔍 Criando caso: client_id={client_id}, service_id={service_id}, title={title}")

        # Validar cliente
        if not client_id:
            return jsonify({"error": "ID do cliente é obrigatório"}), 400

        client = Users.query.get(client_id)
        if not client:
            return jsonify({"error": "Cliente não encontrado"}), 404

        # Criar novo caso
        new_case = ClientCases(
            user_id=client_id,
            service_id=service_id,
            title=title,
            description=description,
            status=CaseStatus(status)
        )

        db.session.add(new_case)
        db.session.commit()

        print(f"✅ Caso criado com sucesso! ID: {new_case.id}")

        return jsonify({
            'id': new_case.id,
            'title': new_case.title,
            'description': new_case.description,
            'status': new_case.status.value,
            'created_at': new_case.created_at.isoformat(),
            'message': 'Caso criado com sucesso!'
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao criar caso: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/api/admin/create-case-main", methods=["POST"])
def create_case_main():
    """Rota de criação de casos diretamente no main.py"""
    try:
        from src.models import ClientCases, CaseStatus, Users
        from flask import request

        # Obter dados do request
        data = request.get_json() or {}

        # Extrair dados
        client_id = data.get('client_id')
        service_id = data.get('service_id', 1)
        title = data.get('title', 'Novo Processo')
        description = data.get('description', '')
        status = data.get('status', 'pendente')

        print(f"🔍 Criando caso: client_id={client_id}, service_id={service_id}, title={title}")

        # Validar cliente
        if not client_id:
            return jsonify({"error": "ID do cliente é obrigatório"}), 400

        client = Users.query.get(client_id)
        if not client:
            return jsonify({"error": "Cliente não encontrado"}), 404

        # Criar novo caso
        new_case = ClientCases(
            user_id=client_id,
            service_id=service_id,
            title=title,
            description=description,
            status=CaseStatus(status)
        )

        db.session.add(new_case)
        db.session.commit()

        print(f"✅ Caso criado com sucesso! ID: {new_case.id}")

        return jsonify({
            'id': new_case.id,
            'title': new_case.title,
            'description': new_case.description,
            'status': new_case.status.value,
            'created_at': new_case.created_at.isoformat(),
            'message': 'Caso criado com sucesso!'
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro ao criar caso: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)

