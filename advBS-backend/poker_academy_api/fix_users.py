#!/usr/bin/env python3
"""
Script para corrigir os usuários com hash de senha compatível
"""

import sqlite3
import os
import sys
from werkzeug.security import generate_password_hash

# Caminho do banco
db_path = "poker_academy.db"

if not os.path.exists(db_path):
    print("❌ Banco de dados não encontrado!")
    exit(1)

# Conectar ao banco
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("🔧 Corrigindo usuários com hash compatível...")

# Remover usuários existentes
cursor.execute("DELETE FROM users")

# Criar hash compatível com Werkzeug
admin_hash = generate_password_hash("admin123")
student_hash = generate_password_hash("student123")

print(f"🔐 Hash admin: {admin_hash[:50]}...")
print(f"🔐 Hash student: {student_hash[:50]}...")

# Inserir usuários com hash correto
cursor.execute('''
INSERT INTO users (name, username, email, password_hash, type, register_date)
VALUES (?, ?, ?, ?, ?, datetime('now'))
''', ("Admin", "admin", "admin@pokeracademy.com", admin_hash, "admin"))

cursor.execute('''
INSERT INTO users (name, username, email, password_hash, type, register_date)
VALUES (?, ?, ?, ?, ?, datetime('now'))
''', ("Estudante", "student", "student@pokeracademy.com", student_hash, "student"))

# Commit e verificar
conn.commit()

# Verificar se foi criado corretamente
cursor.execute("SELECT id, name, email, type FROM users")
users = cursor.fetchall()

print("✅ Usuários corrigidos:")
for user in users:
    user_id, name, email, user_type = user
    print(f"   👤 {name} ({email}) - {user_type}")

conn.close()

print()
print("🎉 Usuários corrigidos com sucesso!")
print()
print("📋 Credenciais de acesso:")
print("   👨‍💼 Admin:")
print("      Email: admin@pokeracademy.com")
print("      Senha: admin123")
print()
print("   👨‍🎓 Estudante:")
print("      Email: student@pokeracademy.com") 
print("      Senha: student123")
print()
print("🌐 Teste agora em: http://localhost:3000")
