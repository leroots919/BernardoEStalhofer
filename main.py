# main.py - Aplicação FastAPI simplificada para o Railway
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMmddleware

# Criar aplicação FastAPI
app = FastAPI(
    title="Bernardo & Stahlöfer Advocacia API",
    description="API para sistema de advocacia de trânito",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMmddleware,
    allow_origins=["*"],  # Em produção, especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota de saúde
@app.get("/")
async def root():
    return {
        "message": "Bernardo & Stahlöfer Advocacia de Trânsito - API funcionando!",
        "status": "ok",
        "version": "1.0.0"
    }

# Rota de healthcheck
@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "message": "Serviço funcionando corretamente!",
        "version": "1.0.0"
    }

# Rota de teste
@app.get("/api/test")
async def test_api():
    return {
        "message": "API funcionando perfeitamente!",
        "data": {
            "empresa": "Bernardo & Stahlöfer Advocacia",
            "especialidade": "Direito de Trânsito",
            "advogados": [
                {"nome": "Dr. Lucas Bernardo", "oab": "OAB/RS 102.336"},
                {"nome": "Dra. Sônia Stahlhöfer", "oab": "OAB/RS 110.390"}
            ]
        }
    }

# Iniciar aplicação
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚠 Iniciando FastAPI na porta {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")