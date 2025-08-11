#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from dotenv import load_dotenv
import pymysql
from werkzeug.security import generate_password_hash

# Carregar variáveis de ambiente
load_dotenv()

def reset_student_passwords():
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
        
        print("🔧 Resetando senhas dos estudantes...")
        print("=" * 50)
        
        # Buscar estudantes
        cursor.execute("SELECT id, name, email FROM users WHERE type = 'student'")
        students = cursor.fetchall()
        
        for student in students:
            student_id, name, email = student
            
            # Gerar hash para senha 'student'
            new_password_hash = generate_password_hash('student')
            
            # Atualizar no banco
            cursor.execute(
                "UPDATE users SET password_hash = %s WHERE id = %s",
                (new_password_hash, student_id)
            )
            
            print(f"✅ {name} ({email}) - senha resetada para 'student'")
        
        # Confirmar mudanças
        connection.commit()
        print(f"\n🎯 {len(students)} senhas atualizadas com sucesso!")
        print("📋 Agora todos os estudantes podem logar com senha: 'student'")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    reset_student_passwords()
