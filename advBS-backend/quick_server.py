from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import mysql.connector
import jwt
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos
class UserLogin(BaseModel):
    email: str
    password: str

# Conexão com banco
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='BS'
    )

# Verificar token
def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token requerido")
    
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, 'your-secret-key-here', algorithms=['HS256'])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

@app.get("/api/health")
async def health():
    return {"message": "FastAPI funcionando!", "status": "ok"}

@app.post("/api/auth/login")
async def login(user_data: UserLogin):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users WHERE email = %s", (user_data.email,))
        user = cursor.fetchone()
        
        if not user or not check_password_hash(user['password_hash'], user_data.password):
            raise HTTPException(status_code=401, detail="Credenciais inválidas")
        
        # Gerar token
        payload = {
            'user_id': user['id'],
            'email': user['email'],
            'type': user['type'],
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        token = jwt.encode(payload, 'your-secret-key-here', algorithm='HS256')
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user['id'],
                "name": user['name'],
                "email": user['email'],
                "type": user['type']
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if 'conn' in locals():
            conn.close()

@app.get("/api/client/profile")
async def get_profile(current_user=Depends(verify_token)):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users WHERE id = %s", (current_user['user_id'],))
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        return {
            "id": user['id'],
            "name": user['name'] or "",
            "email": user['email'] or "",
            "cpf": user['cpf'] or "",
            "phone": user['phone'] or "",
            "address": user['address'] or "",
            "city": user['city'] or "",
            "state": user['state'] or "",
            "zip_code": user['zip_code'] or ""
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if 'conn' in locals():
            conn.close()

@app.put("/api/client/profile")
async def update_profile(profile_data: dict, current_user=Depends(verify_token)):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar email duplicado
        if 'email' in profile_data:
            cursor.execute("SELECT id FROM users WHERE email = %s AND id != %s", 
                         (profile_data['email'], current_user['user_id']))
            if cursor.fetchone():
                raise HTTPException(status_code=409, detail="Email já cadastrado")
        
        # Atualizar campos
        fields = []
        values = []
        for field in ['name', 'email', 'cpf', 'phone', 'address', 'city', 'state', 'zip_code']:
            if field in profile_data:
                fields.append(f"{field} = %s")
                values.append(profile_data[field])
        
        if fields:
            values.append(current_user['user_id'])
            query = f"UPDATE users SET {', '.join(fields)} WHERE id = %s"
            cursor.execute(query, values)
            conn.commit()
        
        return {"message": "Perfil atualizado com sucesso"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("🚀 Servidor FastAPI iniciando...")
    uvicorn.run(app, host="0.0.0.0", port=5000)
