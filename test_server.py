#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

# Criar aplicação FastAPI
app = FastAPI(
    title="TESTE - Bernardo & Stahlhöfer API",
    description="API de TESTE para diagnosticar problemas",
    version="3.0.0-TEST"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    """Health check de teste"""
    return {
        "message": "TESTE - FastAPI funcionando!",
        "status": "ok",
        "version": "3.0.0-TEST",
        "timestamp": "2024-12-21 - TESTE DEPLOY"
    }

@app.get("/api/admin/clients")
async def test_admin_clients():
    """Rota de teste para admin clients"""
    return {
        "message": "TESTE - Rota admin/clients funcionando!",
        "data": [
            {"id": 1, "name": "Cliente Teste", "email": "teste@teste.com"}
        ]
    }

@app.get("/api/admin/cases")
async def test_admin_cases():
    """Rota de teste para admin cases"""
    return {
        "message": "TESTE - Rota admin/cases funcionando!",
        "data": [
            {"id": 1, "title": "Caso Teste", "status": "pendente"}
        ]
    }

@app.get("/api/test/routes")
async def test_routes():
    """Listar todas as rotas de teste"""
    routes = []
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            routes.append({
                "path": route.path,
                "methods": list(route.methods)
            })
    
    return {
        "message": "TESTE - Rotas disponíveis",
        "total_routes": len(routes),
        "routes": routes
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print("🚀 TESTE - Iniciando servidor FastAPI...")
    print(f"📍 URL: http://localhost:{port}")
    
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)
