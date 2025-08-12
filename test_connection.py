#!/usr/bin/env python3
"""
Script para testar a conexão e verificar qual banco estamos usando
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Carregar variáveis de ambiente
try:
    load_dotenv()
except:
    pass

# Mostrar variáveis de ambiente
print("🔍 VARIÁVEIS DE AMBIENTE:")
print(f"DB_HOST: {os.getenv('DB_HOST', 'NÃO DEFINIDO')}")
print(f"DB_PORT: {os.getenv('DB_PORT', 'NÃO DEFINIDO')}")
print(f"DB_USER: {os.getenv('DB_USER', 'NÃO DEFINIDO')}")
print(f"DB_PASSWORD: {'*' * len(os.getenv('DB_PASSWORD', '')) if os.getenv('DB_PASSWORD') else 'NÃO DEFINIDO'}")
print(f"DB_NAME: {os.getenv('DB_NAME', 'NÃO DEFINIDO')}")

# Configurações do banco
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'BS')

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"\n🔗 Conectando em: {DB_HOST}:{DB_PORT}/{DB_NAME}")

try:
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        print("✅ Conexão estabelecida!")
        
        # Verificar qual banco estamos usando
        db_result = connection.execute(text("SELECT DATABASE() as current_db"))
        current_db = db_result.fetchone().current_db
        print(f"📍 Banco atual: {current_db}")
        
        # Verificar tabelas
        tables_result = connection.execute(text("SHOW TABLES"))
        tables = [row[0] for row in tables_result.fetchall()]
        print(f"📋 Tabelas: {tables}")
        
        # Contar dados
        if 'users' in tables:
            users_count = connection.execute(text("SELECT COUNT(*) as count FROM users")).fetchone().count
            clients_count = connection.execute(text("SELECT COUNT(*) as count FROM users WHERE type = 'cliente'")).fetchone().count
            print(f"👥 Total usuários: {users_count}")
            print(f"👥 Total clientes: {clients_count}")
        
        if 'client_cases' in tables:
            cases_count = connection.execute(text("SELECT COUNT(*) as count FROM client_cases")).fetchone().count
            print(f"📋 Total casos: {cases_count}")
        
        if 'services' in tables:
            services_count = connection.execute(text("SELECT COUNT(*) as count FROM services")).fetchone().count
            print(f"🛠️ Total serviços: {services_count}")

except Exception as e:
    print(f"❌ Erro: {e}")
