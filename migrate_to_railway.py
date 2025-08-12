#!/usr/bin/env python3
"""
Script para migrar dados do banco local para o Railway
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Carregar variáveis de ambiente
try:
    load_dotenv()
except:
    pass

# Configurações do banco LOCAL
LOCAL_DB_HOST = 'localhost'
LOCAL_DB_PORT = '3306'
LOCAL_DB_USER = 'root'
LOCAL_DB_PASSWORD = ''  # Coloque sua senha local aqui se necessário
LOCAL_DB_NAME = 'BS'

print("🔧 CONFIGURAÇÃO:")
print(f"📍 Banco LOCAL: {LOCAL_DB_HOST}:{LOCAL_DB_PORT}/{LOCAL_DB_NAME}")
print("📍 Banco RAILWAY: Carregando do .env...")

# Configurações do banco RAILWAY (do .env)
RAILWAY_DB_HOST = os.getenv('DB_HOST')
RAILWAY_DB_PORT = os.getenv('DB_PORT', '3306')
RAILWAY_DB_USER = os.getenv('DB_USER')
RAILWAY_DB_PASSWORD = os.getenv('DB_PASSWORD')
RAILWAY_DB_NAME = os.getenv('DB_NAME', 'railway')

# Strings de conexão
LOCAL_URL = f"mysql+pymysql://{LOCAL_DB_USER}:{LOCAL_DB_PASSWORD}@{LOCAL_DB_HOST}:{LOCAL_DB_PORT}/{LOCAL_DB_NAME}"
RAILWAY_URL = f"mysql+pymysql://{RAILWAY_DB_USER}:{RAILWAY_DB_PASSWORD}@{RAILWAY_DB_HOST}:{RAILWAY_DB_PORT}/{RAILWAY_DB_NAME}"

print(f"🔗 Conectando ao banco LOCAL: {LOCAL_DB_HOST}:{LOCAL_DB_PORT}/{LOCAL_DB_NAME}")
print(f"🔗 Conectando ao banco RAILWAY: {RAILWAY_DB_HOST}:{RAILWAY_DB_PORT}/{RAILWAY_DB_NAME}")

try:
    # Criar engines
    local_engine = create_engine(LOCAL_URL)
    railway_engine = create_engine(RAILWAY_URL)
    
    # Testar conexões
    with local_engine.connect() as local_conn:
        print("✅ Conexão LOCAL estabelecida!")
        
        # Verificar tabelas locais
        result = local_conn.execute(text("SHOW TABLES"))
        local_tables = [row[0] for row in result.fetchall()]
        print(f"📋 Tabelas locais: {local_tables}")
    
    with railway_engine.connect() as railway_conn:
        print("✅ Conexão RAILWAY estabelecida!")
        
        # Verificar tabelas railway
        result = railway_conn.execute(text("SHOW TABLES"))
        railway_tables = [row[0] for row in result.fetchall()]
        print(f"📋 Tabelas railway: {railway_tables}")
    
    # Migrar dados
    print("\n🚀 INICIANDO MIGRAÇÃO...")
    
    with local_engine.connect() as local_conn, railway_engine.connect() as railway_conn:
        
        # 1. Migrar usuários (exceto admin que já existe)
        print("👥 Migrando usuários...")
        users_query = "SELECT * FROM users WHERE email != 'admin@admin.com'"
        try:
            users_result = local_conn.execute(text(users_query))
            users = users_result.fetchall()
            
            for user in users:
                insert_query = """
                INSERT IGNORE INTO users (name, username, email, password_hash, cpf, phone, address, city, state, zip_code, type, register_date, last_login)
                VALUES (:name, :username, :email, :password_hash, :cpf, :phone, :address, :city, :state, :zip_code, :type, :register_date, :last_login)
                """
                railway_conn.execute(text(insert_query), {
                    'name': user.name,
                    'username': user.username,
                    'email': user.email,
                    'password_hash': user.password_hash,
                    'cpf': user.cpf,
                    'phone': user.phone,
                    'address': user.address,
                    'city': user.city,
                    'state': user.state,
                    'zip_code': user.zip_code,
                    'type': user.type,
                    'register_date': user.register_date,
                    'last_login': user.last_login
                })
            print(f"✅ {len(users)} usuários migrados!")
        except Exception as e:
            print(f"⚠️ Erro ao migrar usuários: {e}")
        
        # 2. Migrar serviços
        print("🛠️ Migrando serviços...")
        try:
            services_result = local_conn.execute(text("SELECT * FROM services"))
            services = services_result.fetchall()
            
            for service in services:
                insert_query = """
                INSERT IGNORE INTO services (name, description, price, created_at)
                VALUES (:name, :description, :price, :created_at)
                """
                railway_conn.execute(text(insert_query), {
                    'name': service.name,
                    'description': service.description,
                    'price': service.price,
                    'created_at': service.created_at
                })
            print(f"✅ {len(services)} serviços migrados!")
        except Exception as e:
            print(f"⚠️ Erro ao migrar serviços: {e}")
        
        # 3. Migrar casos de clientes
        print("📋 Migrando casos de clientes...")
        try:
            cases_result = local_conn.execute(text("SELECT * FROM client_cases"))
            cases = cases_result.fetchall()
            
            for case in cases:
                insert_query = """
                INSERT IGNORE INTO client_cases (user_id, service_id, title, description, status, created_at, updated_at)
                VALUES (:user_id, :service_id, :title, :description, :status, :created_at, :updated_at)
                """
                railway_conn.execute(text(insert_query), {
                    'user_id': case.user_id,
                    'service_id': case.service_id,
                    'title': case.title,
                    'description': case.description,
                    'status': case.status,
                    'created_at': case.created_at,
                    'updated_at': case.updated_at
                })
            print(f"✅ {len(cases)} casos migrados!")
        except Exception as e:
            print(f"⚠️ Erro ao migrar casos: {e}")
        
        # 4. Migrar arquivos de processos
        print("📁 Migrando arquivos de processos...")
        try:
            files_result = local_conn.execute(text("SELECT * FROM process_files"))
            files = files_result.fetchall()
            
            for file in files:
                insert_query = """
                INSERT IGNORE INTO process_files (user_id, case_id, filename, original_filename, file_path, file_size, mime_type, uploaded_at)
                VALUES (:user_id, :case_id, :filename, :original_filename, :file_path, :file_size, :mime_type, :uploaded_at)
                """
                railway_conn.execute(text(insert_query), {
                    'user_id': file.user_id,
                    'case_id': file.case_id,
                    'filename': file.filename,
                    'original_filename': file.original_filename,
                    'file_path': file.file_path,
                    'file_size': file.file_size,
                    'mime_type': file.mime_type,
                    'uploaded_at': file.uploaded_at
                })
            print(f"✅ {len(files)} arquivos migrados!")
        except Exception as e:
            print(f"⚠️ Erro ao migrar arquivos: {e}")
    
    print("\n🎉 MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
    print("🔍 Verificando dados migrados...")
    
    # Verificar dados migrados
    with railway_engine.connect() as railway_conn:
        for table in ['users', 'services', 'client_cases', 'process_files']:
            try:
                result = railway_conn.execute(text(f"SELECT COUNT(*) as count FROM {table}"))
                count = result.fetchone().count
                print(f"📊 {table}: {count} registros")
            except Exception as e:
                print(f"⚠️ Erro ao contar {table}: {e}")

except Exception as e:
    print(f"❌ Erro na migração: {e}")
    sys.exit(1)
