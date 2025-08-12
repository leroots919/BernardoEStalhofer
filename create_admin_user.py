#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'advBS-backend', 'src'))

import mysql.connector
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do banco de dados
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "BS")

def create_admin_user():
    """Criar usuário admin no banco de dados"""
    try:
        print(f"🔗 Conectando ao banco: {DB_HOST}:{DB_PORT}/{DB_NAME}")
        
        # Conectar ao banco
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=int(DB_PORT),
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Verificar se a tabela users existe
        cursor.execute("SHOW TABLES LIKE 'users'")
        if not cursor.fetchone():
            print("❌ Tabela 'users' não encontrada!")
            return False
        
        # Verificar estrutura da tabela
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        print("📋 Estrutura da tabela users:")
        for col in columns:
            print(f"   - {col[0]} ({col[1]})")
        
        # Verificar se admin já existe
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", ("admin", "admin@advbs.com"))
        existing_admin = cursor.fetchone()

        if existing_admin:
            print("✅ Admin já existe!")
            print("   Username: admin")
            print("   Email: admin@advbs.com")
            print("   Senha: admin123")
            return True
        
        # Gerar hash da senha
        password_hash = generate_password_hash("admin123")
        print(f"🔐 Hash gerado: {password_hash[:50]}...")
        
        # Inserir admin
        insert_query = """
        INSERT INTO users (name, username, email, password_hash, type, register_date)
        VALUES (%s, %s, %s, %s, %s, NOW())
        """

        cursor.execute(insert_query, (
            "Administrador",
            "admin",
            "admin@advbs.com",
            password_hash,
            "admin"
        ))
        
        connection.commit()
        
        print("✅ Admin criado com sucesso!")
        print("   Email: admin@advbs.com")
        print("   Senha: admin123")
        
        # Verificar se foi criado
        cursor.execute("SELECT id, name, email, type FROM users WHERE email = %s", ("admin@advbs.com",))
        admin = cursor.fetchone()
        if admin:
            print(f"   ID: {admin[0]}")
            print(f"   Nome: {admin[1]}")
            print(f"   Tipo: {admin[3]}")
        
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Erro MySQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Conexão fechada")

if __name__ == "__main__":
    print("🚀 Criando usuário admin...")
    success = create_admin_user()
    
    if success:
        print("\n🎉 Pronto! Agora você pode fazer login com:")
        print("   Email: admin@advbs.com")
        print("   Senha: admin123")
    else:
        print("\n❌ Falha ao criar usuário admin")
