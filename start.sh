#!/bin/bash

# Script de inicialização para o Railway

echo "🚀 Iniciando aplicação FastAPI..."

# Verificar se os arquivos existem
echo "🔍 Verificando arquivos..."
ls -la

# Navegar para o diretório src
cd /app/src

echo "🔍 Verificando arquivos em src..."
ls -la

# Iniciar a aplicação
echo "🚀 Iniciando uvicorn..."
uvicorn fastapi_main:app --host 0.0.0.0 --port $PORT --log-level info