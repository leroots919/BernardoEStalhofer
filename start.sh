#!/bin/bash

# Script de inicialização para o Railway

echo "🚀 Iniciando aplicação FastAPI..."

# Navegar para o diretório do FastAPI
cd /app/poker_academy_api

# Verificar se os arquivos existem
echo "🔍 Verificando arquivos..."
ls -la

# Iniciar a aplicação
echo "🚀 Iniciando uvicorn..."
uvicorn fastapi_main:app --host 0.0.0.0 --port $PORT --log-level info