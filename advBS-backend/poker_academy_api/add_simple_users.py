#!/usr/bin/env python3
"""
Script para adicionar usuários com emails mais simples
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

# Caminho do banco
db_path = "poker_academy.db"

if not os.path.exists(db_path):
    print("❌ Banco de dados não encontrado!")
    exit(1)

# Conectar ao banco
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("🔧 Adicionando usuários com emails simples...")

# Verificar se já existem
cursor.execute("SELECT email FROM users WHERE email IN ('admin@test.com', 'student@test.com')")
existing = cursor.fetchall()

if existing:
    print("⚠️  Usuários já existem. Removendo primeiro...")
    cursor.execute("DELETE FROM users WHERE email IN ('admin@test.com', 'student@test.com')")

# Hash das senhas (usando o mesmo método do Flask)
admin_hash = generate_password_hash("123456")
student_hash = generate_password_hash("123456")

# Inserir usuários simples
cursor.execute('''
INSERT INTO users (name, username, email, password_hash, type)
VALUES (?, ?, ?, ?, ?)
''', ("Admin", "admin", "admin@test.com", admin_hash, "admin"))

cursor.execute('''
INSERT INTO users (name, username, email, password_hash, type)
VALUES (?, ?, ?, ?, ?)
''', ("Estudante", "student", "student@test.com", student_hash, "student"))

# Commit e fechar
conn.commit()
conn.close()

print("✅ Usuários adicionados com sucesso!")
print("")
print("📋 Credenciais de acesso:")
print("   👨‍💼 Admin:")
print("      Email: admin@test.com")
print("      Senha: 123456")
print("")
print("   👨‍🎓 Estudante:")
print("      Email: student@test.com") 
print("      Senha: 123456")
print("")
print("🌐 Acesse: http://localhost:3000")
