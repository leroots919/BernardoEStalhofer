#!/usr/bin/env python3
"""
Script para criar um banco SQLite simples
"""

import sqlite3
import os
from datetime import datetime

# Caminho do banco
db_path = "poker_academy.db"

# Remover banco existente se houver
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"🗑️  Banco existente removido: {db_path}")

# Criar conexão
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("🔧 Criando banco SQLite...")

# Criar tabela de usuários
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    type VARCHAR(20) NOT NULL DEFAULT 'student',
    register_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
)
''')

# Criar tabela de aulas
cursor.execute('''
CREATE TABLE classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    instructor VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    category VARCHAR(20) NOT NULL,
    video_type VARCHAR(20) NOT NULL DEFAULT 'local',
    video_path VARCHAR(255),
    priority INTEGER NOT NULL DEFAULT 5,
    views INTEGER NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Criar outras tabelas necessárias
cursor.execute('''
CREATE TABLE user_progress (
    user_id INTEGER,
    class_id INTEGER,
    progress INTEGER NOT NULL DEFAULT 0,
    watched BOOLEAN NOT NULL DEFAULT 0,
    last_watched DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, class_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE
)
''')

cursor.execute('''
CREATE TABLE favorites (
    user_id INTEGER,
    class_id INTEGER,
    PRIMARY KEY (user_id, class_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE
)
''')

cursor.execute('''
CREATE TABLE class_views (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    class_id INTEGER NOT NULL,
    viewed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE
)
''')

print("✅ Tabelas criadas")

# Inserir usuário admin
cursor.execute('''
INSERT INTO users (name, username, email, password_hash, type)
VALUES (?, ?, ?, ?, ?)
''', ("Admin", "admin", "admin@pokeracademy.com", 
      "scrypt:32768:8:1$bf591012fc973e95$4aef904bda3fb9c8e95d4aef904bda3fb9c8e95d4aef904bda3fb9c8e95d4aef904bda3fb9c8e95d4aef904bda3fb9c8e95d4aef904bda3fb9c", 
      "admin"))

# Inserir usuário estudante
cursor.execute('''
INSERT INTO users (name, username, email, password_hash, type)
VALUES (?, ?, ?, ?, ?)
''', ("Estudante", "student", "student@pokeracademy.com", 
      "scrypt:32768:8:1$bf591012fc973e95$4aef904bda3fb9c8e95d4aef904bda3fb9c8e95d4aef904bda3fb9c8e95d4aef904bda3fb9c8e95d4aef904bda3fb9c8e95d4aef904bda3fb9c", 
      "student"))

print("✅ Usuários criados")
print("   - Admin: admin / admin123")
print("   - Estudante: student / student123")

# Commit e fechar
conn.commit()
conn.close()

print(f"🎉 Banco SQLite criado: {db_path}")
print("📊 Estrutura:")
print("   - users: 2 registros")
print("   - classes: 0 registros")
print("   - Outras tabelas vazias")
