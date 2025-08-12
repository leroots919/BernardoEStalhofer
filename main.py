#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import FastAPI, HTTPException, Depends, Header, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
from dotenv import load_dotenv
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
import logging

# Carregar variáveis de ambiente (opcional - Railway usa variáveis de ambiente)
try:
    load_dotenv()
except:
    pass  # Em produção (Railway) não há arquivo .env

# Criar aplicação FastAPI
app = FastAPI(
    title="Bernardo & Stahlhöfer - API",
    description="API para sistema de advocacia de trânsito",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Middleware para log de todas as requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"🔍 REQUEST: {request.method} {request.url}")
    logger.info(f"🔍 Headers: {dict(request.headers)}")

    response = await call_next(request)

    logger.info(f"🔍 RESPONSE: {response.status_code}")
    return response

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração do banco de dados
# Usar variáveis de ambiente para produção (Railway) ou localhost para desenvolvimento
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
# Forçar uso do banco railway em produção
if 'railway' in os.getenv('DB_HOST', ''):
    DB_NAME = 'railway'  # Forçar banco railway
    logger.info("🚀 PRODUÇÃO: Usando banco 'railway'")
else:
    DB_NAME = os.getenv("DB_NAME", "BS")  # Local usa BS
    logger.info("🏠 LOCAL: Usando banco 'BS'")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(f"🔗 Conectando ao banco: {DB_HOST}:{DB_PORT}/{DB_NAME}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Obter sessão do banco de dados"""
    try:
        logger.info(f"🔗 Criando sessão do banco: {DB_HOST}:{DB_PORT}/{DB_NAME}")
        db = SessionLocal()
        logger.info("✅ Sessão do banco criada com sucesso")
        yield db
    except Exception as e:
        logger.error(f"❌ Erro ao criar sessão do banco: {e}")
        raise
    finally:
        try:
            db.close()
            logger.info("🔒 Sessão do banco fechada")
        except:
            pass

# Modelos Pydantic
class UserLogin(BaseModel):
    email: str
    password: str

# ==================== ROTAS BÁSICAS ====================

@app.get("/api/health")
async def health_check():
    """Verificar se a API está funcionando"""
    return {"message": "FastAPI está funcionando!", "status": "ok", "version": "2.0.2", "timestamp": "2024-12-21 - DEPLOY NO PROJETO CORRETO BernardoEStalhofer"}

@app.get("/api/debug/routes")
async def debug_routes():
    """Listar todas as rotas disponíveis para debug"""
    routes = []
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            routes.append({
                "path": route.path,
                "methods": list(route.methods),
                "name": getattr(route, 'name', 'unknown')
            })

    logger.info(f"🔍 Total de rotas registradas: {len(routes)}")
    for route in routes:
        logger.info(f"   - {route['path']} [{', '.join(route['methods'])}]")

    return {
        "total_routes": len(routes),
        "routes": routes,
        "timestamp": "2024-12-21"
    }

@app.get("/api/debug/data")
async def debug_data(db_session=Depends(get_db)):
    """Debug - verificar dados no banco"""
    try:
        # Contar usuários
        users_result = db_session.execute(text("SELECT COUNT(*) as count FROM users"))
        users_count = users_result.fetchone().count

        # Contar clientes
        clients_result = db_session.execute(text("SELECT COUNT(*) as count FROM users WHERE type = 'cliente'"))
        clients_count = clients_result.fetchone().count

        # Contar casos
        cases_result = db_session.execute(text("SELECT COUNT(*) as count FROM client_cases"))
        cases_count = cases_result.fetchone().count

        # Listar alguns clientes
        clients_list_result = db_session.execute(text("SELECT id, name, email, type FROM users WHERE type = 'cliente' LIMIT 5"))
        clients_list = [{"id": row.id, "name": row.name, "email": row.email, "type": row.type} for row in clients_list_result.fetchall()]

        return {
            "database_info": {
                "total_users": users_count,
                "total_clients": clients_count,
                "total_cases": cases_count
            },
            "sample_clients": clients_list,
            "timestamp": "2024-12-21"
        }
    except Exception as e:
        return {"error": str(e), "timestamp": "2024-12-21"}

@app.post("/api/auth/login")
async def login(user_data: UserLogin, db_session=Depends(get_db)):
    """Login de usuário"""
    try:
        logger.info(f"🔐 Tentativa de login: {user_data.email}")
        logger.info(f"🔍 DB Session: {db_session}")
        logger.info(f"🔍 DB Config: {DB_HOST}:{DB_PORT}/{DB_NAME}")

        # Buscar usuário por email OU username usando SQL direto
        query = "SELECT id, name, email, password_hash, type FROM users WHERE email = :email OR username = :username"
        result = db_session.execute(text(query), {"email": user_data.email, "username": user_data.email})
        user = result.fetchone()

        if not user:
            print(f"❌ Usuário não encontrado: {user_data.email}")
            # Se for 'admin', criar usuário admin automaticamente
            if user_data.email == 'admin' and user_data.password == 'admin123':
                print("🔧 Criando usuário admin automaticamente...")
                from werkzeug.security import generate_password_hash
                admin_hash = generate_password_hash('admin123')

                insert_query = "INSERT INTO users (name, username, email, password_hash, type, register_date) VALUES (:name, :username, :email, :password_hash, :type, NOW())"
                db_session.execute(text(insert_query), {"name": "Administrador", "username": "admin", "email": "admin@advbs.com", "password_hash": admin_hash, "type": "admin"})
                db_session.commit()

                # Buscar o usuário recém-criado
                result = db_session.execute(text(query), {"email": user_data.email, "username": user_data.email})
                user = result.fetchone()
                print("✅ Usuário admin criado automaticamente!")

            if not user:
                raise HTTPException(status_code=401, detail="Credenciais inválidas")

        # Verificar senha hasheada
        from werkzeug.security import check_password_hash
        if not check_password_hash(user.password_hash, user_data.password):
            print(f"❌ Senha incorreta para: {user_data.email}")
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        print(f"✅ Login bem-sucedido: {user.name} ({user.type})")

        # Gerar token JWT
        import jwt
        from datetime import datetime, timedelta
        
        secret_key = os.getenv('JWT_SECRET_KEY', 'your-secret-key-here')
        
        # Payload do token
        payload = {
            'user_id': user.id,
            'email': user.email,
            'type': user.type,
            'exp': datetime.utcnow() + timedelta(hours=24),  # Expira em 24 horas
            'iat': datetime.utcnow()
        }
        
        # Gerar token JWT
        token = jwt.encode(payload, secret_key, algorithm='HS256')

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "type": user.type
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro no login: {str(e)}")
        logger.error(f"❌ Tipo do erro: {type(e)}")
        import traceback
        logger.error(f"❌ Stack trace: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

def verify_token(authorization: str = Header(None)):
    """Verificar token de autenticação JWT"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Token de acesso requerido")

    try:
        # Extrair token do header "Bearer token"
        if authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
            
            # Decodificar o token JWT
            import jwt
            
            secret_key = os.getenv('JWT_SECRET_KEY', 'your-secret-key-here')
            
            try:
                payload = jwt.decode(token, secret_key, algorithms=['HS256'])
                user_id = payload.get('user_id')
                email = payload.get('email')
                user_type = payload.get('type')
                
                if user_id:
                    return {
                        "user_id": user_id,
                        "email": email,
                        "type": user_type,
                        "id": user_id  # Para compatibilidade
                    }
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token expirado")
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        print(f"❌ Erro ao verificar token: {e}")
        pass

    raise HTTPException(status_code=401, detail="Token inválido")

@app.get("/api/auth/verify")
async def verify_token_route(current_user=Depends(verify_token)):
    """Verificar se o token é válido e retornar dados do usuário"""
    try:
        logger.info(f"🔍 Verificando token para usuário: {current_user}")
        return {
            "valid": True,
            "user": {
                "id": current_user.get('user_id'),
                "email": current_user.get('email'),
                "type": current_user.get('type')
            }
        }
    except Exception as e:
        logger.error(f"❌ Erro na verificação de token: {e}")
        raise HTTPException(status_code=401, detail="Token inválido")

# ==================== ROTAS DE PERFIL ====================
@app.get("/api/client/profile")
async def get_client_profile(db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Obter perfil do cliente logado"""
    try:
        print(f"🔍 Buscando perfil do cliente ID: {current_user.get('user_id')}")

        # Buscar dados completos do usuário usando SQL direto
        query = """
        SELECT id, name, email, cpf, phone, address, city, state, zip_code,
               register_date, last_login, type
        FROM users WHERE id = :user_id
        """
        result = db_session.execute(text(query), {"user_id": current_user.get('user_id')})
        user = result.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        # Retornar dados do perfil
        profile_data = {
            "id": user.id,
            "name": user.name or "",
            "email": user.email or "",
            "cpf": user.cpf or "",
            "phone": user.phone or "",
            "address": user.address or "",
            "city": user.city or "",
            "state": user.state or "",
            "zip_code": user.zip_code or "",
            "register_date": user.register_date.isoformat() if user.register_date else None,
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "type": user.type
        }

        print(f"✅ Perfil encontrado: {user.name} ({user.email})")
        return profile_data

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao buscar perfil: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/client/profile")
async def update_client_profile(profile_data: dict, db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Atualizar perfil do cliente logado"""
    try:
        print(f"🔄 Atualizando perfil do cliente ID: {current_user.get('user_id')}")

        # Verificar se email já existe em outro usuário
        if profile_data.get("email"):
            query = "SELECT id FROM users WHERE email = :email AND id != :user_id"
            result = db_session.execute(text(query), {"email": profile_data["email"], "user_id": current_user.get('user_id')})
            existing_user = result.fetchone()
            if existing_user:
                raise HTTPException(status_code=409, detail="Email já cadastrado")

        # Construir query de atualização dinamicamente
        update_fields = []
        update_values = []
        
        update_params = {}
        for field in ['name', 'email', 'cpf', 'phone', 'address', 'city', 'state', 'zip_code']:
            if field in profile_data:
                update_fields.append(f"{field} = :{field}")
                update_params[field] = profile_data[field]

        if update_fields:
            update_params['user_id'] = current_user.get('user_id')
            query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = :user_id"
            db_session.execute(text(query), update_params)
            db_session.commit()

        print(f"✅ Perfil atualizado com sucesso!")

        return {"message": "Perfil atualizado com sucesso"}

    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        print(f"❌ Erro ao atualizar perfil: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ROTAS ADMIN ====================

@app.get("/api/admin/clients")
async def get_admin_clients(db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Listar todos os clientes (admin)"""
    try:
        logger.info("🚀 ROTA /api/admin/clients CHAMADA!")
        logger.info(f"🔍 Current user: {current_user}")

        # Verificar se é admin
        if current_user.get('type') != 'admin':
            logger.error(f"❌ Acesso negado - usuário não é admin: {current_user}")
            raise HTTPException(status_code=403, detail="Acesso negado")

        logger.info("🔍 Buscando todos os clientes...")

        # Buscar todos os usuários do tipo cliente
        query = """
        SELECT id, name, username, email, cpf, phone, address, city, state,
               zip_code, register_date, last_login, type
        FROM users WHERE type = 'cliente'
        ORDER BY register_date DESC
        """
        logger.info(f"🔍 Executando query: {query}")
        result = db_session.execute(text(query))
        clients = result.fetchall()
        logger.info(f"🔍 Clientes encontrados na query: {len(clients)}")

        clients_list = []
        for client in clients:
            clients_list.append({
                'id': client.id,
                'name': client.name,
                'username': client.username,
                'email': client.email,
                'cpf': client.cpf,
                'phone': client.phone,
                'address': client.address,
                'city': client.city,
                'state': client.state,
                'zip_code': client.zip_code,
                'register_date': client.register_date.isoformat() if client.register_date else None,
                'last_login': client.last_login.isoformat() if client.last_login else None,
                'type': client.type
            })

        print(f"✅ {len(clients_list)} clientes encontrados")
        return {"data": clients_list}

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao buscar clientes: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@app.get("/api/admin/cases")
async def get_admin_cases(db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Listar todos os casos (admin)"""
    try:
        logger.info("🚀 ROTA /api/admin/cases CHAMADA!")
        logger.info(f"🔍 Current user: {current_user}")

        # Verificar se é admin
        if current_user.get('type') != 'admin':
            logger.error(f"❌ Acesso negado - usuário não é admin: {current_user}")
            raise HTTPException(status_code=403, detail="Acesso negado")

        logger.info("🔍 Buscando todos os casos...")

        # Primeiro, vamos verificar se as tabelas existem
        try:
            logger.info("🔍 Verificando se tabela client_cases existe...")
            check_table = "SHOW TABLES LIKE 'client_cases'"
            table_result = db_session.execute(text(check_table))
            table_exists = table_result.fetchone()
            logger.info(f"🔍 Tabela client_cases existe: {table_exists}")

            if not table_exists:
                logger.warning("⚠️ Tabela client_cases não existe - retornando lista vazia")
                return {"data": []}
        except Exception as table_error:
            logger.error(f"❌ Erro ao verificar tabela: {table_error}")

        # Buscar todos os casos com informações do cliente E serviço
        query = """
        SELECT cc.id, cc.user_id, cc.service_id, cc.title, cc.description,
               cc.status, cc.created_at, cc.updated_at,
               u.name as client_name, u.email as client_email,
               s.name as service_name
        FROM client_cases cc
        LEFT JOIN users u ON cc.user_id = u.id
        LEFT JOIN services s ON cc.service_id = s.id
        ORDER BY cc.created_at DESC
        """
        logger.info(f"🔍 Executando query: {query}")
        result = db_session.execute(text(query))
        cases = result.fetchall()

        cases_list = []
        for case in cases:
            cases_list.append({
                'id': case.id,
                'user_id': case.user_id,
                'service_id': case.service_id,
                'title': case.title,
                'description': case.description,
                'status': case.status,
                'created_at': case.created_at.isoformat() if case.created_at else None,
                'updated_at': case.updated_at.isoformat() if case.updated_at else None,
                'client_name': case.client_name,
                'client_email': case.client_email,
                'service_name': case.service_name  # ADICIONADO: nome do serviço
            })

        print(f"✅ {len(cases_list)} casos encontrados")
        return {"data": cases_list}

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao buscar casos: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@app.get("/api/services")
async def get_services(db_session=Depends(get_db)):
    """Listar todos os serviços"""
    try:
        print("🔍 Buscando todos os serviços...")

        # Buscar todos os serviços
        query = """
        SELECT id, name, description, price, created_at
        FROM services
        ORDER BY name
        """
        result = db_session.execute(text(query))
        services = result.fetchall()

        services_list = []
        for service in services:
            services_list.append({
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'price': float(service.price) if service.price else 0.0,
                'created_at': service.created_at.isoformat() if service.created_at else None
            })

        print(f"✅ {len(services_list)} serviços encontrados")
        return {"data": services_list}

    except Exception as e:
        print(f"❌ Erro ao buscar serviços: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

# ==================== ROTAS DE CLIENTE ====================
@app.get("/api/client/cases")
async def get_client_cases(db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Obter casos do cliente logado"""
    try:
        user_id = current_user.get('user_id')
        print(f"🔍 Buscando casos do cliente ID: {user_id}")

        query = """
        SELECT cc.id, cc.service_id, cc.title, cc.description, cc.status,
               cc.created_at, cc.updated_at,
               s.name as service_name
        FROM client_cases cc
        LEFT JOIN services s ON cc.service_id = s.id
        WHERE cc.user_id = :user_id
        ORDER BY cc.created_at DESC
        """
        result = db_session.execute(text(query), {"user_id": user_id})
        cases = result.fetchall()

        cases_list = []
        for case in cases:
            cases_list.append({
                'id': case.id,
                'service_id': case.service_id,
                'title': case.title,
                'description': case.description,
                'status': case.status,
                'created_at': case.created_at.isoformat() if case.created_at else None,
                'updated_at': case.updated_at.isoformat() if case.updated_at else None,
                'service_name': case.service_name
            })

        print(f"✅ {len(cases_list)} casos encontrados para o cliente")
        return {"data": cases_list}

    except Exception as e:
        print(f"❌ Erro ao buscar casos do cliente: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@app.get("/api/client/stats")
async def get_client_stats(db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Obter estatísticas do cliente logado"""
    try:
        user_id = current_user.get('user_id')
        print(f"🔍 Buscando estatísticas do cliente ID: {user_id}")

        # Contar casos por status
        query = """
        SELECT
            COUNT(*) as total_cases,
            SUM(CASE WHEN status = 'pendente' THEN 1 ELSE 0 END) as pending_cases,
            SUM(CASE WHEN status = 'em_andamento' THEN 1 ELSE 0 END) as active_cases,
            SUM(CASE WHEN status = 'concluido' THEN 1 ELSE 0 END) as completed_cases
        FROM client_cases
        WHERE user_id = :user_id
        """
        result = db_session.execute(text(query), {"user_id": user_id})
        stats = result.fetchone()

        # Contar arquivos
        files_query = "SELECT COUNT(*) as total_files FROM process_files WHERE user_id = :user_id"
        files_result = db_session.execute(text(files_query), {"user_id": user_id})
        files_count = files_result.fetchone()

        stats_data = {
            'total_cases': stats.total_cases or 0,
            'pending_cases': stats.pending_cases or 0,
            'active_cases': stats.active_cases or 0,
            'completed_cases': stats.completed_cases or 0,
            'total_files': files_count.total_files if files_count else 0
        }

        print(f"✅ Estatísticas calculadas: {stats_data}")
        return {"data": stats_data}

    except Exception as e:
        print(f"❌ Erro ao buscar estatísticas do cliente: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

# ==================== ROTAS ADMIN ADICIONAIS ====================
@app.get("/api/admin/clients/{client_id}/cases")
async def get_admin_client_cases(client_id: int, db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Obter casos de um cliente específico (admin)"""
    try:
        if current_user.get('type') != 'admin':
            raise HTTPException(status_code=403, detail="Acesso negado")

        print(f"🔍 Buscando casos do cliente ID: {client_id}")

        query = """
        SELECT cc.id, cc.service_id, cc.title, cc.description, cc.status,
               cc.created_at, cc.updated_at,
               s.name as service_name
        FROM client_cases cc
        LEFT JOIN services s ON cc.service_id = s.id
        WHERE cc.user_id = :client_id
        ORDER BY cc.created_at DESC
        """
        result = db_session.execute(text(query), {"client_id": client_id})
        cases = result.fetchall()

        cases_list = []
        for case in cases:
            cases_list.append({
                'id': case.id,
                'service_id': case.service_id,
                'title': case.title,
                'description': case.description,
                'status': case.status,
                'created_at': case.created_at.isoformat() if case.created_at else None,
                'updated_at': case.updated_at.isoformat() if case.updated_at else None,
                'service_name': case.service_name
            })

        print(f"✅ {len(cases_list)} casos encontrados para o cliente {client_id}")
        return {"data": cases_list}

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao buscar casos do cliente: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

# ==================== ROTAS DE ANALYTICS ====================
@app.get("/api/analytics/stats")
async def get_analytics_stats(db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Obter estatísticas gerais do sistema (admin)"""
    try:
        if current_user.get('type') != 'admin':
            raise HTTPException(status_code=403, detail="Acesso negado")

        print("🔍 Calculando estatísticas do sistema...")

        # Estatísticas gerais
        stats_query = """
        SELECT
            (SELECT COUNT(*) FROM users WHERE type = 'cliente') as total_clients,
            (SELECT COUNT(*) FROM client_cases) as total_cases,
            (SELECT COUNT(*) FROM client_cases WHERE status = 'pendente') as pending_cases,
            (SELECT COUNT(*) FROM client_cases WHERE status = 'em_andamento') as active_cases,
            (SELECT COUNT(*) FROM client_cases WHERE status = 'concluido') as completed_cases,
            (SELECT COUNT(*) FROM process_files) as total_files,
            (SELECT COUNT(*) FROM services) as total_services
        """
        result = db_session.execute(text(stats_query))
        stats = result.fetchone()

        analytics_data = {
            'total_clients': stats.total_clients or 0,
            'total_cases': stats.total_cases or 0,
            'pending_cases': stats.pending_cases or 0,
            'active_cases': stats.active_cases or 0,
            'completed_cases': stats.completed_cases or 0,
            'total_files': stats.total_files or 0,
            'total_services': stats.total_services or 0
        }

        print(f"✅ Estatísticas calculadas: {analytics_data}")
        return {"data": analytics_data}

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao calcular estatísticas: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

# ==================== ROTAS DE ARQUIVOS ====================

@app.get("/api/admin/process-files")
async def get_process_files(db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Listar todos os arquivos de processos (admin)"""
    try:
        logger.info("🚀 ROTA /api/admin/process-files CHAMADA!")

        # Verificar se é admin
        if current_user.get('type') != 'admin':
            raise HTTPException(status_code=403, detail="Acesso negado")

        # Primeiro, verificar se há arquivos
        count_query = "SELECT COUNT(*) as total FROM process_files"
        count_result = db_session.execute(text(count_query))
        total_files = count_result.fetchone().total

        logger.info(f"📁 Total de arquivos na base: {total_files}")

        if total_files == 0:
            logger.info("📁 Nenhum arquivo encontrado, retornando lista vazia")
            return {"data": []}

        # Buscar todos os arquivos com informações do cliente e caso
        query = """
        SELECT pf.id, pf.case_id, pf.file_name, pf.original_name, pf.file_size,
               pf.upload_date, pf.file_type, pf.user_id,
               COALESCE(u.name, 'Cliente não encontrado') as client_name,
               COALESCE(u.email, '') as client_email,
               COALESCE(cc.title, 'Caso não encontrado') as case_title,
               COALESCE(cc.status, '') as case_status
        FROM process_files pf
        LEFT JOIN users u ON pf.user_id = u.id
        LEFT JOIN client_cases cc ON pf.case_id = cc.id
        ORDER BY pf.upload_date DESC
        """
        result = db_session.execute(text(query))
        files = result.fetchall()

        files_list = []
        for file in files:
            files_list.append({
                'id': file.id,
                'case_id': file.case_id,
                'file_name': file.file_name,
                'original_name': file.original_name,
                'file_size': file.file_size,
                'upload_date': file.upload_date.isoformat() if file.upload_date else None,
                'file_type': file.file_type,
                'user_id': file.user_id,
                'client_name': file.client_name,
                'client_email': file.client_email,
                'case_title': file.case_title,
                'case_status': file.case_status
            })

        logger.info(f"✅ {len(files_list)} arquivos encontrados")
        return {"data": files_list}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao buscar arquivos: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@app.get("/api/admin/clients/search")
async def search_clients(q: str, limit: int = 10, db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Buscar clientes por nome ou email (admin)"""
    try:
        logger.info(f"🔍 Buscando clientes com termo: '{q}', limite: {limit}")

        # Verificar se é admin
        if current_user.get('type') != 'admin':
            raise HTTPException(status_code=403, detail="Acesso negado")

        # Buscar clientes que contenham o termo no nome ou email
        search_term = f"%{q}%"
        logger.info(f"🔍 Termo de busca: '{search_term}'")

        query = """
        SELECT id, name, email, phone, cpf, created_at, type
        FROM users
        WHERE type = 'cliente'
        AND (name LIKE :search_term OR email LIKE :search_term)
        ORDER BY name
        LIMIT :limit
        """
        result = db_session.execute(text(query), {"search_term": search_term, "limit": limit})
        clients = result.fetchall()

        clients_list = []
        for client in clients:
            clients_list.append({
                'id': client.id,
                'name': client.name,
                'email': client.email,
                'phone': client.phone,
                'cpf': client.cpf,
                'created_at': client.created_at.isoformat() if client.created_at else None,
                'type': client.type
            })

        logger.info(f"✅ {len(clients_list)} clientes encontrados")
        return {"data": clients_list}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao buscar clientes: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@app.put("/api/admin/clients/{client_id}")
async def update_client(client_id: int, request: Request, db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Atualizar dados de um cliente (admin) - Versão Ultra Simples"""
    try:
        print(f"🚀 UPDATE CLIENTE {client_id} - INICIADO")

        # Verificar se é admin
        if current_user.get('type') != 'admin':
            raise HTTPException(status_code=403, detail="Acesso negado")

        # Obter dados do request
        client_data = await request.json()
        print(f"📝 Dados recebidos: {client_data}")

        # Atualizar campos diretamente
        updates_made = []

        if 'name' in client_data:
            db_session.execute(text("UPDATE users SET name = :name WHERE id = :id"),
                             {"name": client_data['name'], "id": client_id})
            updates_made.append(f"name={client_data['name']}")

        if 'email' in client_data:
            db_session.execute(text("UPDATE users SET email = :email WHERE id = :id"),
                             {"email": client_data['email'], "id": client_id})
            updates_made.append(f"email={client_data['email']}")

        if 'phone' in client_data:
            db_session.execute(text("UPDATE users SET phone = :phone WHERE id = :id"),
                             {"phone": client_data['phone'], "id": client_id})
            updates_made.append(f"phone={client_data['phone']}")

        if 'cpf' in client_data:
            db_session.execute(text("UPDATE users SET cpf = :cpf WHERE id = :id"),
                             {"cpf": client_data['cpf'], "id": client_id})
            updates_made.append(f"cpf={client_data['cpf']}")

        # Commit
        db_session.commit()
        print(f"✅ UPDATES REALIZADOS: {', '.join(updates_made)}")

        # Retornar resposta simples
        return {
            "data": {
                "id": client_id,
                "name": client_data.get('name', ''),
                "email": client_data.get('email', ''),
                "phone": client_data.get('phone', ''),
                "cpf": client_data.get('cpf', ''),
                "type": "cliente",
                "updated": True
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ ERRO: {e}")
        try:
            db_session.rollback()
        except:
            pass
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/clients")
async def create_client(request: Request, db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Criar novo cliente (admin)"""
    try:
        print("🚀 CRIANDO NOVO CLIENTE")

        if current_user.get('type') != 'admin':
            raise HTTPException(status_code=403, detail="Acesso negado")

        data = await request.json()
        print(f"📝 Dados do cliente: {data}")

        # Insert simples
        query = "INSERT INTO users (name, email, phone, cpf, type, password, created_at) VALUES (:name, :email, :phone, :cpf, 'cliente', 'cliente123', NOW())"

        result = db_session.execute(text(query), {
            "name": data.get('name', ''),
            "email": data.get('email', ''),
            "phone": data.get('phone', ''),
            "cpf": data.get('cpf', '')
        })

        db_session.commit()
        client_id = result.lastrowid

        print(f"✅ Cliente {client_id} criado!")

        return {
            "data": {
                "id": client_id,
                "name": data.get('name', ''),
                "email": data.get('email', ''),
                "phone": data.get('phone', ''),
                "cpf": data.get('cpf', ''),
                "type": "cliente"
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ ERRO ao criar cliente: {e}")
        try:
            db_session.rollback()
        except:
            pass
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/clients/{client_id}")
async def delete_client(client_id: int, db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Deletar cliente (admin)"""
    try:
        print(f"🗑️ DELETANDO CLIENTE {client_id}")

        if current_user.get('type') != 'admin':
            raise HTTPException(status_code=403, detail="Acesso negado")

        # Deletar cliente
        query = "DELETE FROM users WHERE id = :client_id AND type = 'cliente'"
        result = db_session.execute(text(query), {"client_id": client_id})

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        db_session.commit()
        print(f"✅ Cliente {client_id} deletado!")

        return {"message": "Cliente deletado com sucesso"}

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ ERRO ao deletar cliente: {e}")
        try:
            db_session.rollback()
        except:
            pass
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/processes/{process_id}")
async def update_process(process_id: int, request: Request, db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Atualizar dados de um processo/caso (admin)"""
    try:
        logger.info(f"📝 Atualizando processo ID: {process_id}")

        # Verificar se é admin
        if current_user.get('type') != 'admin':
            raise HTTPException(status_code=403, detail="Acesso negado")

        # Obter dados do request
        process_data = await request.json()
        logger.info(f"📝 Dados do processo recebidos: {process_data}")

        # Verificar se processo existe
        check_query = "SELECT id FROM client_cases WHERE id = :process_id"
        check_result = db_session.execute(text(check_query), {"process_id": process_id})
        if not check_result.fetchone():
            raise HTTPException(status_code=404, detail="Processo não encontrado")

        # Preparar campos para atualização
        update_fields = []
        params = {"process_id": process_id}

        if 'title' in process_data:
            update_fields.append("title = :title")
            params['title'] = process_data['title']

        if 'description' in process_data:
            update_fields.append("description = :description")
            params['description'] = process_data['description']

        if 'status' in process_data:
            update_fields.append("status = :status")
            params['status'] = process_data['status']

        if 'service_id' in process_data:
            update_fields.append("service_id = :service_id")
            params['service_id'] = process_data['service_id']

        if not update_fields:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")

        # Executar atualização
        update_query = f"UPDATE client_cases SET {', '.join(update_fields)} WHERE id = :process_id"
        db_session.execute(text(update_query), params)
        db_session.commit()

        # Buscar processo atualizado
        select_query = """
        SELECT cc.id, cc.title, cc.description, cc.status, cc.created_at, cc.user_id as client_id, cc.service_id,
               u.name as client_name, u.email as client_email,
               s.name as service_name
        FROM client_cases cc
        LEFT JOIN users u ON cc.user_id = u.id
        LEFT JOIN services s ON cc.service_id = s.id
        WHERE cc.id = :process_id
        """
        result = db_session.execute(text(select_query), {"process_id": process_id})
        updated_process = result.fetchone()

        process_data = {
            'id': updated_process.id,
            'title': updated_process.title,
            'description': updated_process.description,
            'status': updated_process.status,
            'created_at': updated_process.created_at.isoformat() if updated_process.created_at else None,
            'client_id': updated_process.client_id,
            'service_id': updated_process.service_id,
            'client_name': updated_process.client_name,
            'client_email': updated_process.client_email,
            'service_name': updated_process.service_name
        }

        logger.info(f"✅ Processo {process_id} atualizado com sucesso")
        return {"data": process_data}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao atualizar processo: {e}")
        db_session.rollback()
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@app.post("/api/admin/clients/{client_id}/cases")
async def create_client_case(client_id: int, request: Request, db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Criar um novo caso para um cliente (admin) - Ultra Simples"""
    try:
        print(f"🚀 CRIANDO CASO PARA CLIENTE {client_id}")

        # Verificar se é admin
        if current_user.get('type') != 'admin':
            raise HTTPException(status_code=403, detail="Acesso negado")

        # Obter dados do request
        case_data = await request.json()
        print(f"📝 Dados recebidos: {case_data}")

        # Dados básicos
        title = case_data.get('title', 'Novo Caso')
        description = case_data.get('description', '')
        status = case_data.get('status', 'pendente')

        print(f"📝 Título: {title}, Descrição: {description}, Status: {status}")

        # Insert mais simples possível - CORRIGIDO: usar user_id em vez de client_id
        insert_query = "INSERT INTO client_cases (user_id, title, description, status, created_at) VALUES (:user_id, :title, :description, :status, NOW())"

        params = {
            "user_id": client_id,  # A tabela usa user_id, não client_id
            "title": title,
            "description": description,
            "status": status
        }

        print(f"📝 Executando insert com params: {params}")

        result = db_session.execute(text(insert_query), params)
        db_session.commit()

        case_id = result.lastrowid
        print(f"✅ Caso criado com ID: {case_id}")

        # Resposta ultra simples
        return {
            "data": {
                "id": case_id,
                "title": title,
                "description": description,
                "status": status,
                "client_id": client_id,
                "success": True
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ ERRO DETALHADO: {e}")
        print(f"❌ TIPO: {type(e)}")
        try:
            db_session.rollback()
        except:
            pass
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@app.post("/api/admin/create-case")
async def create_case_alternative(request: Request, db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Rota alternativa para criar caso - Ultra Simples"""
    try:
        print("🚀 ROTA ALTERNATIVA - CRIAR CASO")

        # Verificar se é admin
        if current_user.get('type') != 'admin':
            raise HTTPException(status_code=403, detail="Acesso negado")

        # Obter dados
        data = await request.json()
        print(f"📝 Dados: {data}")

        client_id = data.get('client_id')
        title = data.get('title', 'Novo Caso')
        description = data.get('description', '')
        status = data.get('status', 'pendente')

        if not client_id:
            raise HTTPException(status_code=400, detail="client_id obrigatório")

        # Insert direto - CORRIGIDO: usar user_id
        query = "INSERT INTO client_cases (user_id, title, description, status, created_at) VALUES (:user_id, :title, :description, :status, NOW())"

        result = db_session.execute(text(query), {
            "user_id": client_id,  # A tabela usa user_id
            "title": title,
            "description": description,
            "status": status
        })

        db_session.commit()
        case_id = result.lastrowid

        print(f"✅ Caso {case_id} criado!")

        return {
            "data": {
                "id": case_id,
                "title": title,
                "description": description,
                "status": status,
                "client_id": client_id
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ ERRO ALTERNATIVO: {e}")
        try:
            db_session.rollback()
        except:
            pass
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/create-case-public")
async def create_case_public(request: Request, db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Rota pública para criar caso - Versão que DEVE funcionar"""
    try:
        print("🚀 ROTA PÚBLICA - CRIAR CASO")

        # Verificar se é admin
        if current_user.get('type') != 'admin':
            raise HTTPException(status_code=403, detail="Acesso negado")

        # Obter dados
        data = await request.json()
        print(f"📝 Dados recebidos: {data}")

        client_id = data.get('client_id')
        title = data.get('title', 'Novo Caso')
        description = data.get('description', '')
        status = data.get('status', 'pendente')

        print(f"📝 client_id: {client_id}, title: {title}")

        if not client_id:
            raise HTTPException(status_code=400, detail="client_id obrigatório")

        # Usar a forma mais simples possível
        try:
            # Primeiro, verificar se a tabela existe
            check_table = db_session.execute(text("SHOW TABLES LIKE 'client_cases'"))
            if not check_table.fetchone():
                raise HTTPException(status_code=500, detail="Tabela client_cases não existe")

            # Insert com valores diretos - CORRIGIDO: usar user_id
            insert_sql = f"""
            INSERT INTO client_cases (user_id, title, description, status, created_at)
            VALUES ({client_id}, '{title}', '{description}', '{status}', NOW())
            """

            print(f"📝 SQL: {insert_sql}")

            result = db_session.execute(text(insert_sql))
            db_session.commit()

            case_id = result.lastrowid
            print(f"✅ Caso {case_id} criado com sucesso!")

            return {
                "data": {
                    "id": case_id,
                    "title": title,
                    "description": description,
                    "status": status,
                    "client_id": client_id,
                    "success": True
                }
            }

        except Exception as sql_error:
            print(f"❌ ERRO SQL: {sql_error}")
            raise HTTPException(status_code=500, detail=f"Erro SQL: {str(sql_error)}")

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ ERRO GERAL: {e}")
        try:
            db_session.rollback()
        except:
            pass
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Configurar porta para Railway (usa PORT do ambiente ou 5000 como fallback)
    port = int(os.getenv("PORT", 5000))

    print("🚀 Iniciando servidor FastAPI simples...")
    print(f"📍 URL: http://localhost:{port}")
    print(f"📖 Docs: http://localhost:{port}/docs")

    # Em produção (Railway), não usar reload
    is_production = os.getenv("RAILWAY_ENVIRONMENT") is not None
    uvicorn.run(app, host="0.0.0.0", port=port, reload=not is_production)
