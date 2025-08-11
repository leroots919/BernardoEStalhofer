#!/usr/bin/env python3
"""
Script para corrigir a estrutura da tabela users
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

print("🔧 Corrigindo estrutura da tabela users...")

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
    
    # Verificar estrutura atual da tabela users
    print("📊 Verificando estrutura atual...")
    cursor.execute("DESCRIBE users")
    columns = cursor.fetchall()
    
    print("Colunas atuais:")
    for col in columns:
        print(f"   - {col[0]}: {col[1]}")
    
    # Verificar se a coluna type é ENUM
    type_column = None
    for col in columns:
        if col[0] == 'type':
            type_column = col[1]
            break
    
    if type_column and 'enum' in type_column.lower():
        print(f"\n🔧 Coluna 'type' é ENUM: {type_column}")
        print("Alterando para VARCHAR...")
        
        # Alterar coluna type para VARCHAR
        cursor.execute("ALTER TABLE users MODIFY COLUMN type VARCHAR(20) NOT NULL DEFAULT 'student'")
        connection.commit()
        print("✅ Coluna 'type' alterada para VARCHAR")
    
    # Verificar se existe coluna register_date
    has_register_date = any(col[0] == 'register_date' for col in columns)
    
    if not has_register_date:
        print("➕ Adicionando coluna 'register_date'...")
        cursor.execute("ALTER TABLE users ADD COLUMN register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        connection.commit()
        print("✅ Coluna 'register_date' adicionada")
    
    # Verificar usuários existentes
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    print(f"\n👥 Total de usuários: {user_count}")
    
    if user_count > 0:
        cursor.execute("SELECT id, name, email, type FROM users")
        users = cursor.fetchall()
        
        print("📋 Usuários existentes:")
        for user in users:
            print(f"   {user[0]}: {user[1]} ({user[2]}) - {user[3]}")
    
    # Verificar se existe um admin
    cursor.execute("SELECT * FROM users WHERE type = 'admin' LIMIT 1")
    admin = cursor.fetchone()
    
    if not admin:
        print("\n🔧 Criando usuário admin...")
        password_hash = generate_password_hash("admin123")
        cursor.execute("""
            INSERT INTO users (name, email, password_hash, type) 
            VALUES (%s, %s, %s, %s)
        """, ("Admin", "admin@pokeracademy.com", password_hash, "admin"))
        connection.commit()
        print("✅ Usuário admin criado!")
        print("   Email: admin@pokeracademy.com")
        print("   Senha: admin123")
    else:
        print("\n✅ Usuário admin já existe!")
    
    # Verificar tabela classes
    cursor.execute("SHOW TABLES LIKE 'classes'")
    classes_table = cursor.fetchone()
    
    if classes_table:
        cursor.execute("SELECT COUNT(*) FROM classes")
        class_count = cursor.fetchone()[0]
        print(f"\n📚 Total de aulas: {class_count}")
        
        # Verificar estrutura da tabela classes
        cursor.execute("DESCRIBE classes")
        class_columns = cursor.fetchall()
        
        # Verificar se tem as colunas necessárias
        column_names = [col[0] for col in class_columns]
        
        if 'description' not in column_names:
            print("➕ Adicionando coluna 'description' na tabela classes...")
            cursor.execute("ALTER TABLE classes ADD COLUMN description TEXT")
            connection.commit()
        
        if 'instructor' not in column_names:
            print("➕ Adicionando coluna 'instructor' na tabela classes...")
            cursor.execute("ALTER TABLE classes ADD COLUMN instructor VARCHAR(255)")
            connection.commit()
        
        if 'video_path' not in column_names:
            print("➕ Adicionando coluna 'video_path' na tabela classes...")
            cursor.execute("ALTER TABLE classes ADD COLUMN video_path VARCHAR(500)")
            connection.commit()
    
    cursor.close()
    connection.close()
    
    print("\n🎉 Estrutura corrigida com sucesso!")
    print("\n📋 Credenciais para login:")
    print("   Admin: admin@pokeracademy.com / admin123")
    print("\n🔄 Agora reinicie o servidor:")
    print("   python src\\main.py")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    print("\n🔧 Verifique se o MySQL está rodando e as credenciais estão corretas.")
