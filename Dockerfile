# Dockerfile para Backend FastAPI
FROM python:3.9-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de teste
COPY test_server.py .

# Criar diretório para uploads
RUN mkdir -p uploads/documents

# Expor porta
EXPOSE 8000

# Comando para iniciar a aplicação de teste
CMD ["python", "test_server.py"]