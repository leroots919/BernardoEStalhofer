#!/usr/bin/env python3
"""
Script para corrigir as colunas do banco de dados original
"""

import sqlite3
import os

# Caminho do banco
db_path = "poker_academy.db"

if not os.path.exists(db_path):
    print("❌ Banco de dados não encontrado!")
    exit(1)

# Conectar ao banco
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("🔧 Verificando estrutura da tabela classes...")

# Verificar colunas existentes
cursor.execute("PRAGMA table_info(classes)")
columns = cursor.fetchall()

print("📊 Colunas atuais:")
for col in columns:
    print(f"   - {col[1]} ({col[2]})")

# Verificar se a coluna description existe
has_description = any(col[1] == 'description' for col in columns)

if not has_description:
    print("➕ Adicionando coluna 'description'...")
    cursor.execute("ALTER TABLE classes ADD COLUMN description TEXT")
    print("✅ Coluna 'description' adicionada")
else:
    print("✅ Coluna 'description' já existe")

# Verificar se a coluna instructor existe
has_instructor = any(col[1] == 'instructor' for col in columns)

if not has_instructor:
    print("➕ Adicionando coluna 'instructor'...")
    cursor.execute("ALTER TABLE classes ADD COLUMN instructor TEXT")
    print("✅ Coluna 'instructor' adicionada")
else:
    print("✅ Coluna 'instructor' já existe")

# Verificar se a coluna video_path existe
has_video_path = any(col[1] == 'video_path' for col in columns)

if not has_video_path:
    print("➕ Adicionando coluna 'video_path'...")
    cursor.execute("ALTER TABLE classes ADD COLUMN video_path TEXT")
    print("✅ Coluna 'video_path' adicionada")
else:
    print("✅ Coluna 'video_path' já existe")

# Commit das mudanças
conn.commit()

# Verificar estrutura final
print("\n📊 Estrutura final da tabela classes:")
cursor.execute("PRAGMA table_info(classes)")
columns = cursor.fetchall()

for col in columns:
    print(f"   - {col[1]} ({col[2]})")

# Verificar quantas aulas existem
cursor.execute("SELECT COUNT(*) FROM classes")
count = cursor.fetchone()[0]
print(f"\n📚 Total de aulas: {count}")

conn.close()

print("\n🎉 Banco de dados corrigido!")
print("🔄 Agora reinicie o servidor original:")
print("   python src\\main.py")
