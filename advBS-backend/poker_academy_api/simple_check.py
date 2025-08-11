#!/usr/bin/env python3
"""
Script simples para verificar e criar usuários
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

# Caminho do banco
db_path = "poker_academy.db"

print("🔍 Verificando banco de dados...")

if not os.path.exists(db_path):
    print("❌ Banco não encontrado! Criando...")
    # Criar banco e tabelas básicas
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Criar tabela users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            type TEXT NOT NULL DEFAULT 'student',
            register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Criar tabela classes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            instructor TEXT,
            video_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    print("✅ Banco criado!")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

# Verificar usuários existentes
cursor.execute("SELECT COUNT(*) FROM users")
user_count = cursor.fetchone()[0]

print(f"👥 Usuários no banco: {user_count}")

# Verificar se admin existe
cursor.execute("SELECT * FROM users WHERE email = ?", ("admin@pokeracademy.com",))
admin = cursor.fetchone()

if not admin:
    print("🔧 Criando usuário admin...")
    password_hash = generate_password_hash("admin123")
    cursor.execute("""
        INSERT INTO users (name, email, password_hash, type) 
        VALUES (?, ?, ?, ?)
    """, ("Admin", "admin@pokeracademy.com", password_hash, "admin"))
    conn.commit()
    print("✅ Admin criado!")
else:
    print("✅ Admin já existe!")

# Verificar se student existe
cursor.execute("SELECT * FROM users WHERE email = ?", ("student@pokeracademy.com",))
student = cursor.fetchone()

if not student:
    print("🔧 Criando usuário student...")
    password_hash = generate_password_hash("student123")
    cursor.execute("""
        INSERT INTO users (name, email, password_hash, type) 
        VALUES (?, ?, ?, ?)
    """, ("Student Test", "student@pokeracademy.com", password_hash, "student"))
    conn.commit()
    print("✅ Student criado!")
else:
    print("✅ Student já existe!")

# Mostrar todos os usuários
print("\n📋 Usuários no banco:")
cursor.execute("SELECT id, name, email, type FROM users")
users = cursor.fetchall()

for user in users:
    print(f"   {user[0]}: {user[1]} ({user[2]}) - {user[3]}")

conn.close()

print("\n🎉 Pronto!")
print("\n📋 Credenciais:")
print("   Admin: admin@pokeracademy.com / admin123")
print("   Student: student@pokeracademy.com / student123")
print("\n🔄 Agora reinicie o servidor:")
print("   python src\\main.py")
