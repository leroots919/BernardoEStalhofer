#!/usr/bin/env python3
"""
Script para testar conexão com o banco MySQL original
"""

import pymysql
import os
from dotenv import load_dotenv

# Carregar .env
load_dotenv()

# Configurações
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USERNAME = os.getenv("DB_USERNAME", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "poker_academy")

print("🔍 Testando conexão com MySQL...")
print(f"   Host: {DB_HOST}:{DB_PORT}")
print(f"   User: {DB_USERNAME}")
print(f"   Password: {'(vazio)' if not DB_PASSWORD else '***'}")
print(f"   Database: {DB_NAME}")

try:
    # Testar conexão
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4'
    )
    
    print("✅ Conexão estabelecida com sucesso!")
    
    # Testar algumas consultas
    cursor = connection.cursor()
    
    # Verificar tabelas
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    print(f"\n📊 Tabelas encontradas ({len(tables)}):")
    for table in tables:
        print(f"   - {table[0]}")
    
    # Verificar usuários
    if ('users',) in tables:
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"\n👥 Total de usuários: {user_count}")
        
        # Mostrar alguns usuários
        cursor.execute("SELECT id, name, email, type FROM users LIMIT 5")
        users = cursor.fetchall()
        
        print("📋 Usuários encontrados:")
        for user in users:
            print(f"   {user[0]}: {user[1]} ({user[2]}) - {user[3]}")
    
    # Verificar aulas
    if ('classes',) in tables:
        cursor.execute("SELECT COUNT(*) FROM classes")
        class_count = cursor.fetchone()[0]
        print(f"\n📚 Total de aulas: {class_count}")
        
        if class_count > 0:
            cursor.execute("SELECT id, name FROM classes LIMIT 3")
            classes = cursor.fetchall()
            
            print("📋 Aulas encontradas:")
            for cls in classes:
                print(f"   {cls[0]}: {cls[1]}")
    
    cursor.close()
    connection.close()
    
    print("\n🎉 Teste concluído com sucesso!")
    print("✅ Seu banco original está funcionando!")
    
except Exception as e:
    print(f"❌ Erro na conexão: {e}")
    print("\n🔧 Possíveis soluções:")
    print("   1. Verificar se MySQL está rodando")
    print("   2. Verificar credenciais no .env")
    print("   3. Instalar dependências: pip install pymysql")
