#!/usr/bin/env python3
"""
Script para verificar usuários no MySQL
"""

import mysql.connector
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do MySQL
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USERNAME = os.getenv("DB_USERNAME", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "poker_academy")

print("🔍 Conectando ao MySQL...")
print(f"   Host: {DB_HOST}:{DB_PORT}")
print(f"   Database: {DB_NAME}")
print(f"   User: {DB_USERNAME}")

try:
    # Conectar ao MySQL
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    
    print("✅ Conectado ao MySQL!")
    
    # Verificar se a tabela users existe
    cursor.execute("SHOW TABLES LIKE 'users'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        print("❌ Tabela 'users' não existe!")
        print("🔧 Criando tabela users...")
        
        cursor.execute("""
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                type ENUM('admin', 'student') DEFAULT 'student',
                register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print("✅ Tabela 'users' criada!")
    else:
        print("✅ Tabela 'users' existe!")
    
    # Verificar usuários existentes
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    print(f"👥 Total de usuários: {user_count}")
    
    # Listar todos os usuários
    if user_count > 0:
        cursor.execute("SELECT id, name, email, type FROM users")
        users = cursor.fetchall()
        
        print("\n📋 Usuários existentes:")
        for user in users:
            print(f"   {user[0]}: {user[1]} ({user[2]}) - {user[3]}")
    
    # Verificar se admin existe
    cursor.execute("SELECT * FROM users WHERE email = %s", ("admin@pokeracademy.com",))
    admin = cursor.fetchone()
    
    if not admin:
        print("\n🔧 Criando usuário admin...")
        password_hash = generate_password_hash("admin123")
        cursor.execute("""
            INSERT INTO users (name, email, password_hash, type) 
            VALUES (%s, %s, %s, %s)
        """, ("Admin", "admin@pokeracademy.com", password_hash, "admin"))
        conn.commit()
        print("✅ Admin criado!")
    else:
        print("\n✅ Admin já existe!")
    
    # Verificar se student existe
    cursor.execute("SELECT * FROM users WHERE email = %s", ("student@pokeracademy.com",))
    student = cursor.fetchone()
    
    if not student:
        print("🔧 Criando usuário student...")
        password_hash = generate_password_hash("student123")
        cursor.execute("""
            INSERT INTO users (name, email, password_hash, type) 
            VALUES (%s, %s, %s, %s)
        """, ("Student Test", "student@pokeracademy.com", password_hash, "student"))
        conn.commit()
        print("✅ Student criado!")
    else:
        print("✅ Student já existe!")
    
    # Verificar tabela classes
    cursor.execute("SHOW TABLES LIKE 'classes'")
    classes_table = cursor.fetchone()
    
    if not classes_table:
        print("\n🔧 Criando tabela classes...")
        cursor.execute("""
            CREATE TABLE classes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                instructor VARCHAR(255),
                video_path VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print("✅ Tabela 'classes' criada!")
    else:
        cursor.execute("SELECT COUNT(*) FROM classes")
        class_count = cursor.fetchone()[0]
        print(f"\n📚 Total de aulas: {class_count}")
    
    cursor.close()
    conn.close()
    
    print("\n🎉 Verificação concluída!")
    print("\n📋 Credenciais para login:")
    print("   Admin: admin@pokeracademy.com / admin123")
    print("   Student: student@pokeracademy.com / student123")
    
    print("\n🔄 Agora altere o main.py para usar MySQL:")
    print("   Descomente a linha do MySQL e comente a do SQLite")

except mysql.connector.Error as err:
    print(f"❌ Erro ao conectar ao MySQL: {err}")
    print("\n🔧 Verifique:")
    print("   1. Se o MySQL está rodando")
    print("   2. Se as credenciais estão corretas no .env")
    print("   3. Se o banco 'poker_academy' existe")
    
except Exception as e:
    print(f"❌ Erro: {e}")
