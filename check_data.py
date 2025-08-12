#!/usr/bin/env python3
"""
Script para verificar os dados no banco Railway
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Carregar variáveis de ambiente
try:
    load_dotenv()
except:
    pass

# Configurações do banco RAILWAY
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME', 'railway')

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"🔗 Conectando ao banco Railway: {DB_HOST}:{DB_PORT}/{DB_NAME}")

try:
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as connection:
        print("✅ Conexão estabelecida!")
        
        # Verificar usuários
        print("\n👥 USUÁRIOS:")
        users_result = connection.execute(text("SELECT id, name, email, type FROM users"))
        users = users_result.fetchall()
        for user in users:
            print(f"  - ID: {user.id}, Nome: {user.name}, Email: {user.email}, Tipo: {user.type}")
        
        # Verificar casos
        print(f"\n📋 CASOS DE CLIENTES:")
        cases_result = connection.execute(text("SELECT id, user_id, title, status FROM client_cases"))
        cases = cases_result.fetchall()
        for case in cases:
            print(f"  - ID: {case.id}, User ID: {case.user_id}, Título: {case.title}, Status: {case.status}")
        
        # Verificar serviços
        print(f"\n🛠️ SERVIÇOS:")
        services_result = connection.execute(text("SELECT id, name, price FROM services LIMIT 10"))
        services = services_result.fetchall()
        for service in services:
            print(f"  - ID: {service.id}, Nome: {service.name}, Preço: {service.price}")
        
        # Contar totais
        print(f"\n📊 TOTAIS:")
        total_users = connection.execute(text("SELECT COUNT(*) as count FROM users")).fetchone().count
        total_clients = connection.execute(text("SELECT COUNT(*) as count FROM users WHERE type = 'cliente'")).fetchone().count
        total_cases = connection.execute(text("SELECT COUNT(*) as count FROM client_cases")).fetchone().count
        total_services = connection.execute(text("SELECT COUNT(*) as count FROM services")).fetchone().count
        
        print(f"  - Total usuários: {total_users}")
        print(f"  - Total clientes: {total_clients}")
        print(f"  - Total casos: {total_cases}")
        print(f"  - Total serviços: {total_services}")

except Exception as e:
    print(f"❌ Erro: {e}")
