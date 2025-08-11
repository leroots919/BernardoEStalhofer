#!/usr/bin/env python3
"""
Script para verificar se o login está funcionando
"""

import sqlite3
import os
import sys
from werkzeug.security import check_password_hash

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Caminho do banco
db_path = "poker_academy.db"

if not os.path.exists(db_path):
    print("❌ Banco de dados não encontrado!")
    exit(1)

# Conectar ao banco
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("🔍 Verificando usuários no banco...")

# Verificar usuários
cursor.execute("SELECT id, name, email, password_hash, type FROM users")
users = cursor.fetchall()

print(f"📊 Total de usuários: {len(users)}")
print()

for user in users:
    user_id, name, email, password_hash, user_type = user
    print(f"👤 ID: {user_id}")
    print(f"   Nome: {name}")
    print(f"   Email: {email}")
    print(f"   Tipo: {user_type}")
    print(f"   Hash: {password_hash[:50]}...")
    print()

# Testar login específico
test_email = "admin@pokeracademy.com"
test_password = "admin123"

print(f"🧪 Testando login: {test_email}")

cursor.execute("SELECT password_hash FROM users WHERE email = ?", (test_email,))
result = cursor.fetchone()

if result:
    stored_hash = result[0]
    print(f"✅ Usuário encontrado")
    print(f"🔐 Hash armazenado: {stored_hash[:50]}...")
    
    # Testar verificação de senha
    try:
        is_valid = check_password_hash(stored_hash, test_password)
        print(f"🔑 Senha válida: {is_valid}")
    except Exception as e:
        print(f"❌ Erro ao verificar senha: {e}")
else:
    print(f"❌ Usuário não encontrado: {test_email}")

conn.close()

print()
print("🔧 Para testar o login via API:")
print(f"   Email: {test_email}")
print(f"   Senha: {test_password}")
