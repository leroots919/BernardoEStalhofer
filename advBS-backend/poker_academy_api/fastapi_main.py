# FastAPI Main Application
import os
import sys
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile, Header, Form, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
from dotenv import load_dotenv
from sqlalchemy import text, or_

# Carregar variáveis de ambiente
load_dotenv()

# Importar modelos e configurações
from models import db, Users, ClientCases, CaseStatus, Services, ProcessFiles, UserType
from database import get_db_session

# Criar aplicação FastAPI
app = FastAPI(
    title="Bernardo & Stahlhöfer Advocacia API",
    description="API para sistema de advocacia de trânsito",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar pasta de uploads
UPLOAD_DIR = Path("uploads/documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

print(f"📁 Pasta de upload de documentos: {UPLOAD_DIR.absolute()}")

# Modelos Pydantic para validação
class ClientCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    cpf: Optional[str] = None
    address: Optional[str] = None

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    cpf: Optional[str] = None
    address: Optional[str] = None

class CaseCreate(BaseModel):
    client_id: int
    service_id: Optional[int] = 1
    title: str
    description: Optional[str] = ""
    status: Optional[str] = "pendente"

class CaseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    role: Optional[str] = "cliente"

# Dependência para obter sessão do banco
def get_db():
    session = get_db_session()
    try:
        yield session
    finally:
        session.close()

# Rota de saúde
@app.get("/api/health")
async def health_check():
    """Verificar se a API está funcionando"""
    return {"message": "FastAPI está funcionando!", "status": "ok", "version": "2.0.0"}

# ==================== ROTAS DE AUTENTICAÇÃO ====================

@app.post("/api/auth/login")
async def login(user_data: UserLogin, db_session=Depends(get_db)):
    """Login de usuário"""
    try:
        print(f"🔐 Tentativa de login: {user_data.email}")

        # Buscar usuário por email OU username (mais flexível)
        user = db_session.query(Users).filter(
            or_(Users.email == user_data.email, Users.username == user_data.email)
        ).first()
        print(f"🔍 Usuário encontrado: {user is not None}")

        if not user:
            print(f"❌ Usuário não encontrado: {user_data.email}")
            # Se for tentativa de login admin e não existir, criar usuário admin
            if user_data.email == "admin":
                print("🔧 Criando usuário admin...")
                try:
                    from werkzeug.security import generate_password_hash

                    new_admin = Users(
                        name="Administrador",
                        username="admin",
                        email="admin@admin.com",
                        password_hash=generate_password_hash("admin123"),
                        type=UserType.admin
                    )

                    db_session.add(new_admin)
                    db_session.commit()
                    db_session.refresh(new_admin)
                    user = new_admin
                    print("✅ Usuário admin criado com sucesso!")
                except Exception as create_error:
                    print(f"❌ Erro ao criar admin: {create_error}")
                    db_session.rollback()
                    raise HTTPException(status_code=500, detail=f"Erro ao criar usuário admin: {str(create_error)}")
            else:
                raise HTTPException(status_code=401, detail="Credenciais inválidas")

        # Verificar senha hasheada
        from werkzeug.security import check_password_hash
        if not check_password_hash(user.password_hash, user_data.password):
            print(f"❌ Senha incorreta para: {user_data.email}")
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        print(f"✅ Login bem-sucedido: {user.name} ({user.type.value})")

        # Gerar token JWT
        import jwt
        import os
        from datetime import datetime, timedelta

        secret_key = os.getenv('JWT_SECRET_KEY', 'your-secret-key-here')

        # Payload do token
        payload = {
            'user_id': user.id,
            'email': user.email,
            'type': user.type.value,
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
                "type": user.type.value
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro no login: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@app.get("/api/auth/verify")
async def verify_token():
    """Verificar token (implementação simples)"""
    return {"valid": True, "user": {"id": 1, "name": "Admin", "type": "admin"}}

@app.post("/api/auth/logout")
async def logout():
    """Logout de usuário"""
    return {"message": "Logout realizado com sucesso"}

# ==================== MIDDLEWARE DE AUTENTICAÇÃO ====================

def verify_token(authorization: str = Header(None)):
    """Verificar token de autenticação JWT"""
    print(f"🔐 DEBUG: Authorization header: {authorization}")

    if not authorization:
        print("❌ DEBUG: Nenhum header de autorização fornecido")
        raise HTTPException(status_code=401, detail="Token de acesso requerido")

    try:
        # Extrair token do header "Bearer token"
        if authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]
            print(f"🔐 DEBUG: Token extraído: {token[:20]}...")

            # Decodificar o token JWT
            import jwt
            import os

            secret_key = os.getenv('JWT_SECRET_KEY', 'your-secret-key-here')
            print(f"🔐 DEBUG: Secret key: {secret_key}")

            try:
                payload = jwt.decode(token, secret_key, algorithms=['HS256'])
                print(f"🔐 DEBUG: Payload decodificado: {payload}")

                user_id = payload.get('user_id')
                email = payload.get('email')
                user_type = payload.get('type')

                if user_id:
                    user_data = {
                        "user_id": user_id,
                        "email": email,
                        "type": user_type,
                        "id": user_id  # Para compatibilidade
                    }
                    print(f"✅ DEBUG: Token válido para usuário: {user_data}")
                    return user_data
                else:
                    print("❌ DEBUG: user_id não encontrado no payload")

            except jwt.ExpiredSignatureError as e:
                print(f"❌ DEBUG: Token expirado: {e}")
                raise HTTPException(status_code=401, detail="Token expirado")
            except jwt.InvalidTokenError as e:
                print(f"❌ DEBUG: Token inválido: {e}")
                raise HTTPException(status_code=401, detail="Token inválido")
        else:
            print(f"❌ DEBUG: Header não começa com 'Bearer ': {authorization}")

    except Exception as e:
        print(f"❌ DEBUG: Erro geral ao verificar token: {e}")
        import traceback
        traceback.print_exc()

    print("❌ DEBUG: Chegou ao final sem retornar token válido")
    raise HTTPException(status_code=401, detail="Token inválido")

# ==================== ROTAS DE CLIENTES ====================

@app.get("/api/admin/clients")
async def get_clients(db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Listar todos os clientes"""
    try:
        from models import UserType
        clients = db_session.query(Users).filter(Users.type == UserType.cliente).all()
        return [
            {
                "id": client.id,
                "name": client.name,
                "email": client.email,
                "phone": client.phone,
                "cpf": client.cpf,
                "address": client.address,
                "register_date": client.register_date.isoformat() if client.register_date else None
            }
            for client in clients
        ]
    except Exception as e:
        print(f"❌ Erro ao buscar clientes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/clients/search")
async def search_clients(q: str, limit: int = 10, db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Buscar clientes por nome ou email"""
    try:
        from models import UserType

        print(f"🔍 Buscando clientes com termo: '{q}'")

        # Buscar clientes que contenham o termo no nome ou email
        clients = db_session.query(Users).filter(
            Users.type == UserType.cliente,
            (Users.name.ilike(f"%{q}%")) | (Users.email.ilike(f"%{q}%"))
        ).limit(limit).all()

        print(f"✅ Encontrados {len(clients)} clientes:")
        for client in clients:
            print(f"  - ID: {client.id}, Nome: {client.name}, Email: {client.email}")

        result = [
            {
                "id": client.id,
                "name": client.name,
                "email": client.email,
                "phone": client.phone,
                "cpf": client.cpf
            }
            for client in clients
        ]

        print(f"📤 Retornando: {result}")
        return result

    except Exception as e:
        print(f"❌ Erro ao buscar clientes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/clients/{client_id}")
async def get_client(client_id: int, db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Buscar cliente específico por ID"""
    try:
        from models import UserType

        client = db_session.query(Users).filter(
            Users.id == client_id,
            Users.type == UserType.cliente
        ).first()

        if not client:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        return {
            "id": client.id,
            "name": client.name,
            "email": client.email,
            "phone": client.phone,
            "cpf": client.cpf,
            "address": client.address,
            "register_date": client.register_date.isoformat() if client.register_date else None
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao buscar cliente: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/clients")
async def create_client(client_data: ClientCreate, db_session=Depends(get_db)):
    """Criar novo cliente"""
    try:
        # Verificar se email já existe
        existing_client = db_session.query(Users).filter(Users.email == client_data.email).first()
        if existing_client:
            raise HTTPException(status_code=400, detail="Email já cadastrado")

        # Criar novo cliente
        from models import UserType
        new_client = Users(
            name=client_data.name,
            email=client_data.email,
            phone=client_data.phone,
            cpf=client_data.cpf,
            address=client_data.address,
            type=UserType.cliente,
            password_hash='temp123'  # Senha temporária
        )

        db_session.add(new_client)
        db_session.commit()
        db_session.refresh(new_client)

        print(f"✅ Cliente criado: {new_client.name} (ID: {new_client.id})")

        return {
            "id": new_client.id,
            "name": new_client.name,
            "email": new_client.email,
            "phone": new_client.phone,
            "cpf": new_client.cpf,
            "address": new_client.address,
            "message": "Cliente criado com sucesso!"
        }

    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        print(f"❌ Erro ao criar cliente: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/clients/{client_id}")
async def update_client(client_id: int, client_data: ClientUpdate, db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Atualizar cliente existente"""
    try:
        print(f"🔄 Atualizando cliente ID: {client_id}")

        # Buscar cliente
        client = db_session.query(Users).filter(Users.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        # Verificar se email já existe em outro cliente
        if client_data.email and client_data.email != client.email:
            existing_client = db_session.query(Users).filter(
                Users.email == client_data.email,
                Users.id != client_id
            ).first()
            if existing_client:
                raise HTTPException(status_code=400, detail="Email já cadastrado por outro cliente")

        # Atualizar campos
        if client_data.name is not None:
            client.name = client_data.name
        if client_data.email is not None:
            client.email = client_data.email
        if client_data.phone is not None:
            client.phone = client_data.phone
        if client_data.cpf is not None:
            client.cpf = client_data.cpf
        if client_data.address is not None:
            client.address = client_data.address

        db_session.commit()
        db_session.refresh(client)

        print(f"✅ Cliente atualizado: {client.name} (ID: {client.id})")

        return {
            "id": client.id,
            "name": client.name,
            "email": client.email,
            "phone": client.phone,
            "cpf": client.cpf,
            "address": client.address,
            "message": "Cliente atualizado com sucesso!"
        }

    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        print(f"❌ Erro ao atualizar cliente: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ROTAS DE CASOS ====================

@app.post("/api/admin/create-case")
async def create_case(case_data: CaseCreate, db_session=Depends(get_db)):
    """Criar novo caso"""
    try:
        print(f"🔍 Criando caso: client_id={case_data.client_id}, title={case_data.title}")
        
        # Verificar se cliente existe
        client = db_session.query(Users).filter(Users.id == case_data.client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        # Criar novo caso
        new_case = ClientCases(
            user_id=case_data.client_id,
            service_id=case_data.service_id,
            title=case_data.title,
            description=case_data.description,
            status=CaseStatus(case_data.status)
        )
        
        db_session.add(new_case)
        db_session.commit()
        db_session.refresh(new_case)
        
        print(f"✅ Caso criado com sucesso! ID: {new_case.id}")
        
        return {
            "id": new_case.id,
            "title": new_case.title,
            "description": new_case.description,
            "status": new_case.status.value,
            "client_name": client.name,
            "created_at": new_case.created_at.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        print(f"❌ Erro ao criar caso: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/cases")
async def get_cases(db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Listar todos os casos"""
    try:
        # Buscar casos com join explícito
        cases_with_users = db_session.query(ClientCases, Users).join(
            Users, ClientCases.user_id == Users.id
        ).all()

        return [
            {
                "id": case.id,
                "title": case.title,
                "description": case.description,
                "status": case.status.value if hasattr(case.status, 'value') else str(case.status),
                "client_name": user.name,
                "client_id": case.user_id,
                "client_email": user.email,
                "client_username": user.username if hasattr(user, 'username') else None,
                "service_id": case.service_id,
                "created_at": case.created_at.isoformat() if case.created_at else None,
                "updated_at": case.updated_at.isoformat() if case.updated_at else None
            }
            for case, user in cases_with_users
        ]
    except Exception as e:
        print(f"❌ Erro ao buscar casos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/clients/{client_id}/cases")
async def get_admin_client_cases(client_id: int, db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Buscar casos de um cliente específico"""
    try:
        print(f"🔍 Buscando casos do cliente ID: {client_id}")

        # Verificar se cliente existe
        client = db_session.query(Users).filter(Users.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        # Buscar casos do cliente
        cases = db_session.query(ClientCases).filter(ClientCases.user_id == client_id).all()

        return [
            {
                "id": case.id,
                "title": case.title,
                "description": case.description,
                "status": case.status.value if hasattr(case.status, 'value') else str(case.status),
                "service_id": case.service_id,
                "created_at": case.created_at.isoformat() if case.created_at else None,
                "updated_at": case.updated_at.isoformat() if case.updated_at else None
            }
            for case in cases
        ]
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao buscar casos do cliente: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/clients/{client_id}/cases")
async def create_client_case(client_id: int, case_data: CaseCreate, db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Criar novo caso para um cliente específico"""
    try:
        print(f"🔍 Criando caso para cliente ID: {client_id}")

        # Verificar se cliente existe
        client = db_session.query(Users).filter(Users.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        # Criar novo caso
        new_case = ClientCases(
            user_id=client_id,
            service_id=case_data.service_id,
            title=case_data.title,
            description=case_data.description,
            status=CaseStatus(case_data.status)
        )

        db_session.add(new_case)
        db_session.commit()
        db_session.refresh(new_case)

        print(f"✅ Caso criado com sucesso! ID: {new_case.id}")

        return {
            "id": new_case.id,
            "title": new_case.title,
            "description": new_case.description,
            "status": new_case.status.value,
            "client_name": client.name,
            "created_at": new_case.created_at.isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        print(f"❌ Erro ao criar caso para cliente: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ROTAS DE CLIENTE ====================

@app.get("/api/client/profile")
async def get_client_profile(authorization: str = Header(None), db_session=Depends(get_db)):
    """Obter perfil do cliente logado"""
    print("🔍 Rota /api/client/profile chamada!")
    print(f"🔑 Authorization header: {authorization}")

    # TEMPORÁRIO: Sempre retornar dados da Vanessa para debug
    user_id = 9  # ID da vanessa
    print(f"🔍 [TEMP] Buscando perfil do cliente ID: {user_id}")

    # Buscar dados completos do usuário
    user = db_session.query(Users).filter(Users.id == user_id).first()

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

@app.put("/api/client/profile")
async def update_client_profile(profile_data: dict, db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Atualizar perfil do cliente logado"""
    try:
        print(f"🔄 Atualizando perfil do cliente ID: {current_user.get('user_id')}")

        # Buscar usuário
        user = db_session.query(Users).filter(Users.id == current_user.get('user_id')).first()

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        # Verificar se email já existe em outro usuário
        if profile_data.get("email") and profile_data["email"] != user.email:
            existing_user = db_session.query(Users).filter(Users.email == profile_data["email"]).first()
            if existing_user:
                raise HTTPException(status_code=409, detail="Email já cadastrado")

        # Atualizar campos permitidos
        if "name" in profile_data:
            user.name = profile_data["name"]
        if "email" in profile_data:
            user.email = profile_data["email"]
        if "cpf" in profile_data:
            user.cpf = profile_data["cpf"]
        if "phone" in profile_data:
            user.phone = profile_data["phone"]
        if "address" in profile_data:
            user.address = profile_data["address"]
        if "city" in profile_data:
            user.city = profile_data["city"]
        if "state" in profile_data:
            user.state = profile_data["state"]
        if "zip_code" in profile_data:
            user.zip_code = profile_data["zip_code"]

        db_session.commit()

        print(f"✅ Perfil atualizado com sucesso!")

        return {
            "message": "Perfil atualizado com sucesso",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "cpf": user.cpf,
                "phone": user.phone,
                "address": user.address,
                "city": user.city,
                "state": user.state,
                "zip_code": user.zip_code
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        print(f"❌ Erro ao atualizar perfil: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/client/cases")
async def get_client_own_cases(authorization: str = Header(None), db_session=Depends(get_db)):
    """Obter casos do cliente logado"""
    print("🔍 Rota /api/client/cases chamada!")
    print(f"🔑 Authorization header: {authorization}")

    # TEMPORÁRIO: Sempre retornar casos da Vanessa para debug
    user_id = 9  # ID da vanessa
    print(f"🔍 [TEMP] Buscando casos do cliente ID: {user_id}")

    # Buscar casos do cliente
    cases = db_session.query(ClientCases).filter(ClientCases.user_id == user_id).all()
    print(f"📊 Encontrados {len(cases)} casos para o cliente")

    cases_data = []
    for case in cases:
        # Buscar arquivos relacionados ao caso
        case_files = db_session.query(ProcessFiles).filter(
            ProcessFiles.user_id == user_id,
            ProcessFiles.case_id == case.id
        ).all()

        case_data = {
            'id': case.id,
            'title': case.title,
            'description': case.description,
            'status': case.status.value,
            'service_id': case.service_id,
            'created_at': case.created_at.isoformat() if case.created_at else None,
            'updated_at': case.updated_at.isoformat() if case.updated_at else None,
            'files': [file.to_dict() for file in case_files]
        }
        cases_data.append(case_data)

    print(f"✅ Retornando {len(cases_data)} casos")
    return cases_data

@app.get("/api/client/stats")
async def get_client_own_stats():
    """Obter estatísticas do cliente logado - versão temporária sem auth"""
    print("🔍 Rota /api/client/stats chamada!")
    return {
        "total_cases": 4,
        "pending_cases": 2,
        "active_cases": 2,
        "completed_cases": 0,
        "total_files": 0
    }

# ==================== ROTAS DE ARQUIVOS DE PROCESSO ====================

@app.get("/api/admin/process-files")
async def get_process_files(db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Listar todos os arquivos de processo"""
    try:
        print("🔍 Buscando arquivos de processo...")

        # Buscar todos os arquivos de processo
        query = """
        SELECT
            pf.id,
            pf.original_filename,
            pf.filename,
            pf.file_path,
            pf.description,
            pf.user_id,
            pf.case_id,
            pf.created_at,
            u.name as client_name,
            u.email as client_email,
            cc.title as case_title
        FROM process_files pf
        LEFT JOIN users u ON pf.user_id = u.id
        LEFT JOIN client_cases cc ON pf.case_id = cc.id
        ORDER BY pf.created_at DESC
        """

        result = db_session.execute(text(query))
        files = result.fetchall()

        files_list = []
        for file in files:
            file_dict = {
                "id": file.id,
                "original_filename": file.original_filename,
                "stored_filename": file.filename,  # usando filename como stored_filename
                "file_path": file.file_path,
                "file_size": None,  # não temos file_size na tabela atual
                "description": file.description,
                "user_id": file.user_id,
                "case_id": file.case_id,
                "created_at": file.created_at.isoformat() if file.created_at else None,
                "client_name": file.client_name,
                "client_email": file.client_email,
                "case_title": file.case_title
            }
            files_list.append(file_dict)

        print(f"✅ Encontrados {len(files_list)} arquivos")
        return files_list

    except Exception as e:
        print(f"❌ Erro ao buscar arquivos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/admin/process-files")
async def upload_process_file(
    file: UploadFile = File(...),
    client_id: str = Form(...),
    case_id: str = Form(None),
    description: str = Form(""),
    db_session=Depends(get_db),
    current_user=Depends(verify_token)
):
    """Upload de arquivo de processo"""
    try:
        print(f"🚀 Recebendo upload de arquivo:")
        print(f"   📁 Arquivo: {file.filename}")
        print(f"   👤 Cliente ID: {client_id}")
        print(f"   📋 Caso ID: {case_id}")
        print(f"   📝 Descrição: {description}")
        print(f"   🔑 Usuário: {current_user.get('email', 'N/A')}")
        import os
        import uuid
        from datetime import datetime

        print(f"📁 Upload iniciado - Cliente: {client_id}, Arquivo: {file.filename}")

        # Verificar se o cliente existe
        client = db_session.query(Users).filter(Users.id == int(client_id)).first()
        if not client:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        # Criar diretório se não existir
        upload_dir = os.path.join(os.path.dirname(__file__), "uploads", "documents")
        os.makedirs(upload_dir, exist_ok=True)

        # Gerar nome único para o arquivo
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)

        # Salvar arquivo
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        print(f"✅ Arquivo salvo: {file_path}")

        # Salvar informações do arquivo no banco de dados
        try:
            insert_query = """
            INSERT INTO process_files (
                user_id, case_id, filename, original_filename,
                file_path, description, uploaded_by_admin, created_at
            ) VALUES (
                :user_id, :case_id, :filename, :original_filename,
                :file_path, :description, :uploaded_by_admin, NOW()
            )
            """

            db_session.execute(text(insert_query), {
                "user_id": int(client_id),
                "case_id": int(case_id) if case_id else None,
                "filename": unique_filename,
                "original_filename": file.filename,
                "file_path": file_path,
                "description": description,
                "uploaded_by_admin": current_user.get('user_id', 1)
            })
            db_session.commit()
            print(f"✅ Arquivo salvo no banco de dados!")

        except Exception as db_error:
            print(f"❌ Erro ao salvar no banco: {db_error}")
            # Se falhar no banco, pelo menos o arquivo foi salvo

        return {
            "message": "Arquivo enviado com sucesso!",
            "filename": file.filename,
            "client_name": client.name,
            "saved_as": unique_filename,
            "size": len(content)
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao fazer upload: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/process-files/{file_id}")
async def delete_process_file(file_id: int, db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Excluir arquivo de processo"""
    try:
        # Por enquanto retornar sucesso - implementar quando tivermos a tabela
        return {"message": "Exclusão simulada - implementar tabela de arquivos"}
    except Exception as e:
        print(f"❌ Erro ao excluir arquivo: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/process-files/{file_id}/download")
async def download_process_file(file_id: int, db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Download de arquivo de processo"""
    try:
        print(f"📥 Solicitação de download do arquivo ID: {file_id}")

        # Buscar informações do arquivo no banco
        query = """
        SELECT filename, original_filename, file_path
        FROM process_files
        WHERE id = :file_id
        """

        result = db_session.execute(text(query), {"file_id": file_id})
        file_info = result.fetchone()

        if not file_info:
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")

        import os

        file_path = file_info.file_path
        original_filename = file_info.original_filename

        # Verificar se o arquivo existe fisicamente
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Arquivo físico não encontrado")

        print(f"✅ Enviando arquivo: {original_filename}")

        # Retornar o arquivo para download
        return FileResponse(
            path=file_path,
            filename=original_filename,
            media_type='application/octet-stream'
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao baixar arquivo: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ROTA DE TESTE ====================

@app.post("/api/test-case")
async def test_case_creation():
    """Rota de teste simples"""
    print("🔥 Rota de teste FastAPI executada!")
    return {"message": "FastAPI funcionando perfeitamente!", "status": "success"}

@app.post("/api/create-case-public")
async def create_case_public(request: Request, db_session=Depends(get_db)):
    """Rota pública para criar casos (sem autenticação)"""
    try:
        print("🔥🔥🔥 ROTA PÚBLICA DE CRIAÇÃO DE CASOS EXECUTADA! 🔥🔥🔥")

        # Obter dados do request
        data = await request.json()
        print(f"🔍 Dados recebidos: {data}")

        client_id = data.get('client_id')
        service_id = data.get('service_id', 1)
        title = data.get('title', 'Novo Processo')
        description = data.get('description', '')
        status = data.get('status', 'pendente')

        print(f"🔍 Processando: client_id={client_id}, title={title}")

        # Verificar se cliente existe
        client = db_session.query(Users).filter(Users.id == client_id).first()
        if not client:
            print(f"❌ Cliente {client_id} não encontrado")
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        print(f"✅ Cliente encontrado: {client.name}")

        # Criar novo caso
        new_case = ClientCases(
            user_id=client_id,
            service_id=service_id,
            title=title,
            description=description,
            status=CaseStatus(status)
        )

        print("🔍 Salvando caso no banco...")
        db_session.add(new_case)
        db_session.commit()
        print("✅ Caso salvo com sucesso!")

        return {
            'id': new_case.id,
            'title': new_case.title,
            'description': new_case.description,
            'status': new_case.status.value,
            'created_at': new_case.created_at.isoformat(),
            'message': 'Caso criado com sucesso'
        }

    except Exception as e:
        print(f"❌ Erro na criação do caso: {e}")
        db_session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/api/test-client-routes")
async def test_client_routes():
    """Testar se as rotas de cliente estão funcionando"""
    return {
        "message": "Rotas de cliente funcionando!",
        "available_routes": [
            "/api/client/profile",
            "/api/client/cases",
            "/api/client/stats"
        ]
    }

@app.get("/api/client/cases-simple")
async def get_client_cases_simple():
    """Versão simples para testar"""
    return [
        {
            "id": 1,
            "title": "Teste de Caso",
            "status": "pendente",
            "description": "Caso de teste"
        }
    ]

@app.get("/api/client/stats-simple")
async def get_client_stats_simple():
    """Versão simples para testar"""
    return {
        "total_cases": 4,
        "pending_cases": 2,
        "active_cases": 1,
        "completed_cases": 1,
        "total_files": 0
    }

@app.get("/api/client/cases-no-auth")
async def get_client_cases_no_auth(db_session=Depends(get_db)):
    """Versão sem autenticação para testar"""
    try:
        user_id = 9  # ID da vanessa
        print(f"🔍 Buscando casos do cliente ID: {user_id}")

        # Buscar casos do cliente
        cases = db_session.query(ClientCases).filter(ClientCases.user_id == user_id).all()

        print(f"📊 Encontrados {len(cases)} casos para o cliente")

        cases_data = []
        for case in cases:
            # Buscar arquivos relacionados ao caso
            case_files = db_session.query(ProcessFiles).filter(
                ProcessFiles.user_id == user_id,
                ProcessFiles.case_id == case.id
            ).all()

            case_data = {
                'id': case.id,
                'title': case.title,
                'description': case.description,
                'status': case.status.value,
                'service_id': case.service_id,
                'created_at': case.created_at.isoformat() if case.created_at else None,
                'updated_at': case.updated_at.isoformat() if case.updated_at else None,
                'files': [file.to_dict() for file in case_files]
            }
            cases_data.append(case_data)

        return cases_data

    except Exception as e:
        print(f"❌ Erro ao buscar casos do cliente: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/client/stats-no-auth")
async def get_client_stats_no_auth(db_session=Depends(get_db)):
    """Versão sem autenticação para testar"""
    try:
        user_id = 9  # ID da vanessa
        print(f"🔍 Buscando estatísticas do cliente ID: {user_id}")

        # Contar casos por status
        total_cases = db_session.query(ClientCases).filter(ClientCases.user_id == user_id).count()

        pending_cases = db_session.query(ClientCases).filter(
            ClientCases.user_id == user_id,
            ClientCases.status == CaseStatus.pendente
        ).count()

        active_cases = db_session.query(ClientCases).filter(
            ClientCases.user_id == user_id,
            ClientCases.status == CaseStatus.em_andamento
        ).count()

        completed_cases = db_session.query(ClientCases).filter(
            ClientCases.user_id == user_id,
            ClientCases.status == CaseStatus.concluido
        ).count()

        total_files = 0

        stats = {
            'total_cases': total_cases,
            'pending_cases': pending_cases,
            'active_cases': active_cases,
            'completed_cases': completed_cases,
            'total_files': total_files
        }

        print(f"📊 Estatísticas do cliente: {stats}")
        return stats

    except Exception as e:
        print(f"❌ Erro ao buscar estatísticas do cliente: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/client/files/{file_id}/download")
async def download_client_file(file_id: int, authorization: str = Header(None), db_session=Depends(get_db)):
    """Download de arquivo para cliente"""
    try:
        print(f"📥 Cliente solicitando download do arquivo ID: {file_id}")

        # TEMPORÁRIO: Sempre permitir download para a Vanessa (ID: 9)
        user_id = 9
        print(f"🔍 [TEMP] Verificando se arquivo {file_id} pertence ao cliente {user_id}")

        # Buscar informações do arquivo no banco e verificar se pertence ao cliente
        query = """
        SELECT filename, original_filename, file_path, user_id
        FROM process_files
        WHERE id = :file_id AND user_id = :user_id
        """

        result = db_session.execute(text(query), {"file_id": file_id, "user_id": user_id})
        file_info = result.fetchone()

        if not file_info:
            print(f"❌ Arquivo {file_id} não encontrado ou não pertence ao cliente {user_id}")
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")

        import os

        file_path = file_info.file_path
        original_filename = file_info.original_filename

        # Verificar se o arquivo existe fisicamente
        if not os.path.exists(file_path):
            print(f"❌ Arquivo físico não encontrado: {file_path}")
            raise HTTPException(status_code=404, detail="Arquivo físico não encontrado")

        print(f"✅ Enviando arquivo para cliente: {original_filename}")
        print(f"📁 Caminho do arquivo: {file_path}")

        # Detectar o tipo MIME baseado na extensão do arquivo
        import mimetypes
        mime_type, _ = mimetypes.guess_type(original_filename)
        if not mime_type:
            mime_type = 'application/octet-stream'

        print(f"🔍 Tipo MIME detectado: {mime_type}")

        # Preparar nome do arquivo para download (substituir espaços por _)
        safe_filename = original_filename.replace(' ', '_')

        print(f"📄 Original filename: {original_filename}")
        print(f"📄 Safe filename: {safe_filename}")
        print(f"📄 MIME type: {mime_type}")

        # Retornar o arquivo para download
        return FileResponse(
            path=file_path,
            filename=safe_filename,
            media_type=mime_type,
            headers={
                "Content-Disposition": f'attachment; filename="{safe_filename}"'
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao baixar arquivo: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ROTAS DE GERENCIAMENTO DE PROCESSOS ====================

@app.get("/api/admin/processes")
async def get_processes(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    client_id: int = Query(None),
    status: str = Query(None),
    search: str = Query(None),
    db_session=Depends(get_db),
    current_user=Depends(verify_token)
):
    """Listar processos com filtros e paginação"""
    try:
        print(f"🔍 Buscando processos - Página: {page}, Limite: {limit}")
        print(f"   Filtros - Cliente: {client_id}, Status: {status}, Busca: {search}")

        # Query base
        query = db_session.query(ClientCases)

        # Aplicar filtros
        if client_id:
            query = query.filter(ClientCases.user_id == client_id)

        if status:
            query = query.filter(ClientCases.status == status)

        if search:
            query = query.filter(
                or_(
                    ClientCases.description.ilike(f"%{search}%")
                )
            )

        # Contar total
        total = query.count()

        # Aplicar paginação
        offset = (page - 1) * limit
        processes = query.offset(offset).limit(limit).all()

        # Converter para dict
        processes_data = []
        for process in processes:
            processes_data.append({
                "id": process.id,
                "user_id": process.user_id,
                "client_id": process.user_id,  # Alias para compatibilidade
                "description": process.description,
                "status": process.status.value if hasattr(process.status, 'value') else process.status,
                "created_at": process.created_at.isoformat() if process.created_at else None,
                "updated_at": process.updated_at.isoformat() if process.updated_at else None,
                "notes": getattr(process, 'notes', None)
            })

        print(f"✅ Encontrados {len(processes_data)} processos de {total} total")

        return {
            "data": {
                "processes": processes_data,
                "total": total,
                "page": page,
                "limit": limit,
                "total_pages": (total + limit - 1) // limit
            }
        }

    except Exception as e:
        print(f"❌ Erro ao buscar processos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/admin/processes/{process_id}")
async def update_process(
    process_id: int,
    process_data: dict,
    db_session=Depends(get_db),
    current_user=Depends(verify_token)
):
    """Atualizar processo"""
    try:
        print(f"🔄 Atualizando processo ID: {process_id}")
        print(f"   Dados: {process_data}")

        # Buscar processo
        process = db_session.query(ClientCases).filter(ClientCases.id == process_id).first()
        if not process:
            raise HTTPException(status_code=404, detail="Processo não encontrado")

        # Atualizar campos permitidos
        if "description" in process_data:
            process.description = process_data["description"]
        if "status" in process_data:
            # Converter string para enum se necessário
            if isinstance(process_data["status"], str):
                try:
                    process.status = CaseStatus(process_data["status"])
                except ValueError:
                    process.status = process_data["status"]
            else:
                process.status = process_data["status"]
        if "notes" in process_data:
            # Se a tabela não tem campo notes, vamos ignorar por enquanto
            pass

        # Atualizar timestamp
        from datetime import datetime
        process.updated_at = datetime.now()

        db_session.commit()

        print(f"✅ Processo {process_id} atualizado com sucesso")

        return {
            "message": "Processo atualizado com sucesso",
            "data": {
                "id": process.id,
                "description": process.description,
                "status": process.status.value if hasattr(process.status, 'value') else process.status,
                "updated_at": process.updated_at.isoformat()
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao atualizar processo: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/admin/processes/{process_id}")
async def delete_process(
    process_id: int,
    db_session=Depends(get_db),
    current_user=Depends(verify_token)
):
    """Excluir processo"""
    try:
        print(f"🗑️ Excluindo processo ID: {process_id}")

        # Buscar processo
        process = db_session.query(ClientCases).filter(ClientCases.id == process_id).first()
        if not process:
            raise HTTPException(status_code=404, detail="Processo não encontrado")

        # Excluir arquivos relacionados primeiro (se existirem)
        db_session.query(ProcessFiles).filter(ProcessFiles.case_id == process_id).delete()

        # Excluir o processo
        db_session.delete(process)
        db_session.commit()

        print(f"✅ Processo {process_id} excluído com sucesso!")
        return {"message": "Processo excluído com sucesso"}

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao excluir processo: {str(e)}")
        db_session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 Iniciando FastAPI...")
    uvicorn.run(
        "fastapi_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
