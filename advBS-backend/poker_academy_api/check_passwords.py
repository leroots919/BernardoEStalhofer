#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from dotenv import load_dotenv
import pymysql

# Carregar variáveis de ambiente
load_dotenv()

def check_user_passwords():
    try:
        # Conectar ao banco
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'poker_academy'),
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        print("🔍 Verificando senhas dos usuários...")
        print("=" * 50)
        
        # Buscar todos os usuários
        cursor.execute("SELECT id, name, email, password_hash, type FROM users")
        users = cursor.fetchall()
        
        for user in users:
            user_id, name, email, password_hash, user_type = user
            print(f"\n👤 {name} ({email}) - {user_type}")
            print(f"   ID: {user_id}")
            print(f"   Hash: {password_hash[:50]}...")
            
            # Mostrar apenas o hash
            print(f"   🔧 Vamos resetar a senha para 'student'")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    check_user_passwords()
