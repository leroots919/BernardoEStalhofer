#!/usr/bin/env python3
"""
Script para testar consulta de usuários diretamente no banco
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

print("🔍 Testando consulta direta no banco...")

try:
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4'
    )
    
    cursor = connection.cursor()
    
    # 1. Verificar todos os usuários
    print("👥 Todos os usuários:")
    cursor.execute("SELECT id, name, email, type FROM users")
    all_users = cursor.fetchall()
    
    for user in all_users:
        print(f"   {user[0]}: {user[1]} - {user[2]} - {user[3]}")
    
    # 2. Filtrar apenas students
    print(f"\n📚 Apenas estudantes:")
    cursor.execute("SELECT id, name, email, type FROM users WHERE type = 'student'")
    students = cursor.fetchall()
    
    print(f"Total de estudantes: {len(students)}")
    for student in students:
        print(f"   {student[0]}: {student[1]} - {student[2]} - {student[3]}")
    
    # 3. Verificar se tem campo username
    cursor.execute("DESCRIBE users")
    columns = cursor.fetchall()
    
    print(f"\n📊 Estrutura da tabela:")
    for col in columns:
        print(f"   - {col[0]}: {col[1]}")
    
    cursor.close()
    connection.close()
    
    print("\n✅ Consulta direta funcionou!")
    print("🔧 O problema pode estar no SQLAlchemy ou na autenticação")
    
except Exception as e:
    print(f"❌ Erro na consulta direta: {e}")
    import traceback
    traceback.print_exc()
