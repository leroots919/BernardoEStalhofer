# app.py - Aplicação FastAPI ultra-simples
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Criar aplicação
app = FastAPI(
    title="Bernardo & Stahlöfer API",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota principal
@app.get("/")
async def root():
    return {
        "message": "Bernardo & Stahlöfer Advocacia de Trânsito - API Funcionando!",
        "status": "okay",
        "version": "1.0.0",
        "environment": "Railway Production"
    }

# Rota de healthcheck (essencial para Railway)
@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "message": "Serviço funcionando perfeitamente!",
        "timestamp": import datetime; datetime.datetime.now().isoformat()
    }

# Rota de teste de conectividade
@app.get("/api/test")
async def test_api():
    return {
        "message": "API funcionando perfeitamente!",
        "data": {
            "empresa": "Bernardo & Stahlöfer Advocacia",
            "especialidade": "Direito de Trânsito",
            "contato": "(51) 99357-7272",
            "email": "bernardostahlhofer@gmail.com"
        }
    }

# Iniciar aplicação (se executado diretamente)
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Iniciando FastAPI na porta {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")