#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import FastAPI, HTTPException, Depends, Header, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
from dotenv import load_dotenv
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker

# Carregar variáveis de ambiente
load_dotenv()

# Criar aplicação FastAPI
app = FastAPI(
    title="Bernardo & Stahlhöfer - API",
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

# Configuração do banco de dados
# Usar variáveis de ambiente para produção (Railway) ou localhost para desenvolvimento
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "BS")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(f"🔗 Conectando ao banco: {DB_HOST}:{DB_PORT}/{DB_NAME}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelos Pydantic
class UserLogin(BaseModel):
    email: str
    password: str

# ==================== ROTAS BÁSICAS ====================

@app.get("/api/health")
async def health_check():
    """Verificar se a API está funcionando"""
    return {"message": "FastAPI está funcionando!", "status": "ok", "version": "2.0.0"}

@app.post("/api/auth/login")
async def login(user_data: UserLogin, db_session=Depends(get_db)):
    """Login de usuário"""
    try:
        print(f"🔐 Tentativa de login: {user_data.email}")

        # Buscar usuário por email OU username usando SQL direto
        query = "SELECT id, name, email, password_hash, type FROM users WHERE email = %s OR username = %s"
        result = db_session.execute(text(query), (user_data.email, user_data.email))
        user = result.fetchone()

        if not user:
            print(f"❌ Usuário não encontrado: {user_data.email}")
            # Se for 'admin', criar usuário admin automaticamente
            if user_data.email == 'admin' and user_data.password == 'admin123':
                print("🔧 Criando usuário admin automaticamente...")
                from werkzeug.security import generate_password_hash
                admin_hash = generate_password_hash('admin123')

                insert_query = "INSERT INTO users (name, username, email, password_hash, type, register_date) VALUES (%s, %s, %s, %s, %s, NOW())"
                db_session.execute(text(insert_query), ("Administrador", "admin", "admin@advbs.com", admin_hash, "admin"))
                db_session.commit()

                # Buscar o usuário recém-criado
                result = db_session.execute(text(query), (user_data.email, user_data.email))
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
        print(f"❌ Erro no login: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

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

@app.get("/api/client/profile")
async def get_client_profile(db_session=Depends(get_db), current_user=Depends(verify_token)):
    """Obter perfil do cliente logado"""
    try:
        print(f"🔍 Buscando perfil do cliente ID: {current_user.get('user_id')}")

        # Buscar dados completos do usuário usando SQL direto
        query = """
        SELECT id, name, email, cpf, phone, address, city, state, zip_code, 
               register_date, last_login, type 
        FROM users WHERE id = %s
        """
        result = db_session.execute(text(query), (current_user.get('user_id'),))
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
            query = "SELECT id FROM users WHERE email = %s AND id != %s"
            result = db_session.execute(text(query), (profile_data["email"], current_user.get('user_id')))
            existing_user = result.fetchone()
            if existing_user:
                raise HTTPException(status_code=409, detail="Email já cadastrado")

        # Construir query de atualização dinamicamente
        update_fields = []
        update_values = []
        
        for field in ['name', 'email', 'cpf', 'phone', 'address', 'city', 'state', 'zip_code']:
            if field in profile_data:
                update_fields.append(f"{field} = %s")
                update_values.append(profile_data[field])
        
        if update_fields:
            update_values.append(current_user.get('user_id'))
            query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"
            db_session.execute(text(query), update_values)
            db_session.commit()

        print(f"✅ Perfil atualizado com sucesso!")

        return {"message": "Perfil atualizado com sucesso"}

    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        print(f"❌ Erro ao atualizar perfil: {str(e)}")
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
