#!/usr/bin/env python3
# fix_passwords.py - Script para corrigir hashes de senhas

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from werkzeug.security import generate_password_hash
import mysql.connector
from mysql.connector import Error

def fix_passwords():
    """Corrige os hashes de senhas no banco de dados"""
    connection = None
    try:
        # Conectar ao banco
        connection = mysql.connector.connect(
            host='localhost',
            database='poker_academy',
            user='root',
            password=''
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            print("🔧 Corrigindo hashes de senhas...")
            
            # Buscar todos os usuários
            cursor.execute("SELECT id, email FROM users")
            users = cursor.fetchall()
            
            for user_id, email in users:
                # Definir senha padrão baseada no email
                if email == 'admin@pokeracademy.com':
                    password = 'admin123'
                else:
                    password = '123456'  # Senha padrão para estudantes
                
                # Gerar novo hash com método correto
                new_hash = generate_password_hash(password, method='pbkdf2:sha256')
                
                # Atualizar no banco
                update_query = "UPDATE users SET password_hash = %s WHERE id = %s"
                cursor.execute(update_query, (new_hash, user_id))
                
                print(f"✅ Senha atualizada para {email}")
            
            # Confirmar mudanças
            connection.commit()
            print(f"\n🎉 Senhas corrigidas para {len(users)} usuários!")
            print("\n📋 Credenciais de acesso:")
            print("👤 Admin: admin@pokeracademy.com / admin123")
            print("👤 Estudante: student@pokeracademy.com / 123456")
            
    except Error as e:
        print(f"❌ Erro ao conectar ao MySQL: {e}")
        return False
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    
    return True

if __name__ == "__main__":
    print("🔐 Iniciando correção de senhas...")
    if fix_passwords():
        print("✅ Processo concluído com sucesso!")
    else:
        print("❌ Falha na correção de senhas!")
