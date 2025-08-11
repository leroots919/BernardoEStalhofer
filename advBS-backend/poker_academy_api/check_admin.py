#!/usr/bin/env python3
"""Script para verificar e criar usuário admin se necessário"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

# Configuração do banco
DATABASE_URL = "mysql+pymysql://root:@localhost:3306/BS"

def check_and_create_admin():
    try:
        # Conectar ao banco
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        print("🔍 Verificando usuário admin...")
        
        # Verificar se existe usuário admin
        result = session.execute(text("SELECT id, name, email, role FROM users WHERE email = 'admin@admin.com' OR email = 'admin'"))
        admin_user = result.fetchone()
        
        if admin_user:
            print(f"✅ Usuário admin encontrado: {admin_user}")
            return True
        
        print("❌ Usuário admin não encontrado. Criando...")
        
        # Criar usuário admin
        password_hash = generate_password_hash('admin123')
        
        insert_query = text("""
            INSERT INTO users (name, email, password_hash, role, type, created_at) 
            VALUES (:name, :email, :password_hash, :role, :type, NOW())
        """)
        
        session.execute(insert_query, {
            'name': 'Administrador',
            'email': 'admin@admin.com',
            'password_hash': password_hash,
            'role': 'admin',
            'type': 'admin'
        })
        
        session.commit()
        print("✅ Usuário admin criado com sucesso!")
        print("📧 Email: admin@admin.com")
        print("🔑 Senha: admin123")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    finally:
        session.close()

if __name__ == "__main__":
    check_and_create_admin()
