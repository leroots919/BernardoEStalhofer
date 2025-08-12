#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector
import json
from datetime import datetime
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

def get_railway_connection():
    """Conectar ao banco do Railway usando variáveis de ambiente"""
    try:
        # Estas variáveis devem estar configuradas no Railway
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'BS'),
            charset='utf8mb4'
        )
        return connection
    except Exception as e:
        print(f"❌ Erro ao conectar no Railway: {e}")
        return None

def create_database_structure():
    """Criar estrutura do banco usando o schema exportado"""
    try:
        print("📋 Criando estrutura do banco...")
        
        # Ler o schema SQL
        with open('database_schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        connection = get_railway_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        
        # Executar comandos SQL (dividir por ';')
        commands = schema_sql.split(';')
        
        for command in commands:
            command = command.strip()
            if command and not command.startswith('--'):
                try:
                    cursor.execute(command)
                    print(f"✅ Executado: {command[:50]}...")
                except Exception as e:
                    if "already exists" not in str(e).lower():
                        print(f"⚠️ Erro: {e}")
        
        connection.commit()
        print("✅ Estrutura criada com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar estrutura: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def import_table_data(table_name, table_data):
    """Importar dados de uma tabela específica"""
    try:
        connection = get_railway_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        
        if not table_data['data']:
            print(f"⚠️ Tabela {table_name} está vazia, pulando...")
            return True
        
        # Preparar query de inserção
        columns = table_data['columns']
        placeholders = ', '.join(['%s'] * len(columns))
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        
        # Inserir dados
        for row_data in table_data['data']:
            values = [row_data[col] for col in columns]
            try:
                cursor.execute(query, values)
            except Exception as e:
                print(f"⚠️ Erro ao inserir registro em {table_name}: {e}")
                # Continuar com próximo registro
        
        connection.commit()
        print(f"✅ {table_name}: {len(table_data['data'])} registros importados")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao importar {table_name}: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def import_all_data():
    """Importar todos os dados do arquivo JSON"""
    try:
        print("📤 Carregando dados exportados...")
        
        with open('database_export.json', 'r', encoding='utf-8') as f:
            export_data = json.load(f)
        
        print(f"📊 Dados de {export_data['export_date']}")
        print(f"🗂️ Tabelas a importar: {len(export_data['tables'])}")
        
        # Ordem de importação (usuários primeiro, depois dependências)
        import_order = ['users', 'services', 'client_cases', 'process_files', 'consultations', 'favorites', 'service_views', 'processfiles']
        
        success_count = 0
        
        for table_name in import_order:
            if table_name in export_data['tables']:
                print(f"\n📥 Importando {table_name}...")
                if import_table_data(table_name, export_data['tables'][table_name]):
                    success_count += 1
                else:
                    print(f"❌ Falha ao importar {table_name}")
        
        print(f"\n🎉 Importação concluída!")
        print(f"✅ {success_count}/{len(import_order)} tabelas importadas com sucesso")
        
        return success_count == len(import_order)
        
    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        return False

def test_connection():
    """Testar conexão com o Railway"""
    print("🔗 Testando conexão com Railway...")
    
    connection = get_railway_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("✅ Conexão com Railway OK!")
            
            # Mostrar informações do banco
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]
            print(f"📊 Banco atual: {db_name}")
            
            return True
        except Exception as e:
            print(f"❌ Erro no teste: {e}")
            return False
        finally:
            cursor.close()
            connection.close()
    else:
        print("❌ Falha na conexão")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando importação para Railway...")
    
    # Testar conexão
    if not test_connection():
        print("❌ Não foi possível conectar ao Railway")
        exit(1)
    
    # Criar estrutura
    print("\n1️⃣ Criando estrutura do banco...")
    if not create_database_structure():
        print("❌ Falha ao criar estrutura")
        exit(1)
    
    # Importar dados
    print("\n2️⃣ Importando dados...")
    if import_all_data():
        print("\n🎉 Migração completa!")
        print("🔑 Credenciais disponíveis:")
        print("   - Username: admin")
        print("   - Email: admin@advtransito.com")
        print("   - Senha: admin123")
    else:
        print("\n❌ Falha na migração")
