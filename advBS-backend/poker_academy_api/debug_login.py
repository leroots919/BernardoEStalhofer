#!/usr/bin/env python3
"""
Script para debugar problemas de login
"""

import pymysql
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

# Carregar .env
load_dotenv()

# Configurações
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USERNAME = os.getenv("DB_USERNAME", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "poker_academy")

print("🔍 Debugando problemas de login...")

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
    
    # 1. Verificar estrutura da tabela users
    print("📊 Estrutura da tabela users:")
    cursor.execute("DESCRIBE users")
    columns = cursor.fetchall()
    
    column_names = []
    for col in columns:
        column_names.append(col[0])
        print(f"   - {col[0]}: {col[1]}")
    
    # 2. Verificar se tem campo username
    has_username = 'username' in column_names
    print(f"\n🔍 Campo 'username' existe: {has_username}")
    
    if not has_username:
        print("➕ Adicionando campo 'username'...")
        cursor.execute("ALTER TABLE users ADD COLUMN username VARCHAR(100) UNIQUE")
        
        # Copiar name para username para usuários existentes
        cursor.execute("UPDATE users SET username = name WHERE username IS NULL")
        connection.commit()
        print("✅ Campo 'username' adicionado e preenchido")
    
    # 3. Verificar usuários existentes
    print("\n👥 Usuários existentes:")
    if has_username:
        cursor.execute("SELECT id, name, username, email, type FROM users")
    else:
        cursor.execute("SELECT id, name, email, type FROM users")
    
    users = cursor.fetchall()
    
    for user in users:
        if has_username:
            user_id, name, username, email, user_type = user
            print(f"   {user_id}: {name} ({username}) - {email} - {user_type}")
        else:
            user_id, name, email, user_type = user
            print(f"   {user_id}: {name} - {email} - {user_type}")
    
    # 4. Verificar se existe admin
    cursor.execute("SELECT * FROM users WHERE email = 'admin@pokeracademy.com'")
    admin = cursor.fetchone()
    
    if not admin:
        print("\n🔧 Criando usuário admin...")
        password_hash = generate_password_hash("admin123")
        
        if has_username:
            cursor.execute("""
                INSERT INTO users (name, username, email, password_hash, type) 
                VALUES (%s, %s, %s, %s, %s)
            """, ("Admin", "admin", "admin@pokeracademy.com", password_hash, "admin"))
        else:
            cursor.execute("""
                INSERT INTO users (name, email, password_hash, type) 
                VALUES (%s, %s, %s, %s)
            """, ("Admin", "admin@pokeracademy.com", password_hash, "admin"))
        
        connection.commit()
        print("✅ Usuário admin criado!")
    else:
        print("\n✅ Usuário admin já existe!")
    
    # 5. Testar login do admin
    print("\n🧪 Testando login do admin...")
    cursor.execute("SELECT password_hash FROM users WHERE email = 'admin@pokeracademy.com'")
    result = cursor.fetchone()
    
    if result:
        stored_hash = result[0]
        is_valid = check_password_hash(stored_hash, "admin123")
        print(f"🔑 Senha 'admin123' válida: {is_valid}")
        
        if not is_valid:
            print("🔧 Atualizando senha do admin...")
            new_hash = generate_password_hash("admin123")
            cursor.execute("UPDATE users SET password_hash = %s WHERE email = 'admin@pokeracademy.com'", (new_hash,))
            connection.commit()
            print("✅ Senha do admin atualizada!")
    
    # 6. Verificar se existe student de teste
    cursor.execute("SELECT * FROM users WHERE email = 'student@pokeracademy.com'")
    student = cursor.fetchone()
    
    if not student:
        print("\n🔧 Criando usuário student de teste...")
        password_hash = generate_password_hash("student123")
        
        if has_username:
            cursor.execute("""
                INSERT INTO users (name, username, email, password_hash, type) 
                VALUES (%s, %s, %s, %s, %s)
            """, ("Student Test", "student", "student@pokeracademy.com", password_hash, "student"))
        else:
            cursor.execute("""
                INSERT INTO users (name, email, password_hash, type) 
                VALUES (%s, %s, %s, %s)
            """, ("Student Test", "student@pokeracademy.com", password_hash, "student"))
        
        connection.commit()
        print("✅ Usuário student criado!")
    
    cursor.close()
    connection.close()
    
    print("\n🎉 Debug concluído!")
    print("\n📋 Credenciais para teste:")
    print("   Admin: admin@pokeracademy.com / admin123")
    print("   Student: student@pokeracademy.com / student123")
    print("\n🔄 Agora reinicie o servidor e teste o login!")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
