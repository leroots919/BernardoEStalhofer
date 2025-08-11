#!/usr/bin/env python3
"""
Script para corrigir problemas na rota de usuários
"""

import pymysql
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# Carregar .env
load_dotenv()

# Configurações
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USERNAME = os.getenv("DB_USERNAME", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "poker_academy")

print("🔧 Corrigindo problemas na rota de usuários...")

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
    
    # 1. Verificar estrutura atual
    print("📊 Verificando estrutura da tabela users...")
    cursor.execute("DESCRIBE users")
    columns = cursor.fetchall()
    
    column_names = [col[0] for col in columns]
    print(f"Colunas existentes: {column_names}")
    
    # 2. Verificar se tem campo username
    if 'username' not in column_names:
        print("➕ Adicionando campo 'username'...")
        cursor.execute("ALTER TABLE users ADD COLUMN username VARCHAR(100) UNIQUE")
        
        # Preencher username com base no name para usuários existentes
        cursor.execute("UPDATE users SET username = name WHERE username IS NULL")
        connection.commit()
        print("✅ Campo 'username' adicionado")
    
    # 3. Verificar tipo da coluna 'type'
    type_column_info = None
    for col in columns:
        if col[0] == 'type':
            type_column_info = col[1]
            break
    
    print(f"📋 Coluna 'type' atual: {type_column_info}")
    
    # 4. Se for ENUM, converter para VARCHAR temporariamente
    if type_column_info and 'enum' in type_column_info.lower():
        print("🔧 Convertendo coluna 'type' de ENUM para VARCHAR...")
        cursor.execute("ALTER TABLE users MODIFY COLUMN type VARCHAR(20) NOT NULL DEFAULT 'student'")
        connection.commit()
        print("✅ Coluna 'type' convertida para VARCHAR")
    
    # 5. Verificar usuários existentes
    cursor.execute("SELECT id, name, email, type FROM users")
    users = cursor.fetchall()
    
    print(f"\n👥 Usuários existentes ({len(users)}):")
    for user in users:
        print(f"   {user[0]}: {user[1]} - {user[2]} - {user[3]}")
    
    # 6. Garantir que existe admin
    cursor.execute("SELECT * FROM users WHERE email = 'admin@pokeracademy.com'")
    admin = cursor.fetchone()
    
    if not admin:
        print("\n🔧 Criando usuário admin...")
        password_hash = generate_password_hash("admin123")
        cursor.execute("""
            INSERT INTO users (name, username, email, password_hash, type) 
            VALUES (%s, %s, %s, %s, %s)
        """, ("Admin", "admin", "admin@pokeracademy.com", password_hash, "admin"))
        connection.commit()
        print("✅ Usuário admin criado!")
    
    # 7. Garantir que existe student de teste
    cursor.execute("SELECT * FROM users WHERE email = 'student@pokeracademy.com'")
    student = cursor.fetchone()
    
    if not student:
        print("\n🔧 Criando usuário student de teste...")
        password_hash = generate_password_hash("student123")
        cursor.execute("""
            INSERT INTO users (name, username, email, password_hash, type) 
            VALUES (%s, %s, %s, %s, %s)
        """, ("Student Test", "student", "student@pokeracademy.com", password_hash, "student"))
        connection.commit()
        print("✅ Usuário student criado!")
    
    # 8. Verificar resultado final
    cursor.execute("SELECT id, name, username, email, type FROM users")
    final_users = cursor.fetchall()
    
    print(f"\n📋 Usuários finais ({len(final_users)}):")
    for user in final_users:
        print(f"   {user[0]}: {user[1]} ({user[2]}) - {user[3]} - {user[4]}")
    
    cursor.close()
    connection.close()
    
    print("\n🎉 Correção concluída!")
    print("\n📋 Credenciais para teste:")
    print("   Admin: admin@pokeracademy.com / admin123")
    print("   Student: student@pokeracademy.com / student123")
    print("\n🔄 Reinicie o servidor e teste a aba de alunos!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
