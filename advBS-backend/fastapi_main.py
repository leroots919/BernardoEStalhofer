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
    description="API para sistema de advocacia de trânito",
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

# ============================ ROTAS DE AUTENTICAÇÃO ============================

@app.post("/api/auth/login")
async def login(user_data: UserLogin, db_session=Depends(get_db)):
    """Login de usuário"""
    try:
        print(f"🔐 Tuntativa de login: {user_data.email}")

        # Buscar usuário por email OU username (mais flexível)
        user = db_session.query(Users).filter(
            or_(Users.email == user_data.email, Users.username == user_data.email)
        ).first()
        print(f"🐍 Usuário encontrado: {user is not None}")

        if not user:
            print(f"❌ Usuário não encontrado: {user_data.email}")
            # Se for tentativa de login admin e não existir, criar usuário admin
            if user_data.email == "admin":
                print("💧 Criando usuário admin...")
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

if __name__ == "__main__":
    print("🚀 Iniciando FastAPI...")
    uvicorn.run(
        "fastapi_main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )