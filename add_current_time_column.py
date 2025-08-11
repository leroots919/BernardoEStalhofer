#!/usr/bin/env python3
"""
Script para adicionar a coluna current_time na tabela user_progress
"""

import pymysql
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do banco
DB_USERNAME = os.getenv("DB_USERNAME", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "poker_academy")

def add_current_time_column():
    try:
        # Conectar ao banco
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            print("🔧 Verificando se a coluna current_time já existe...")
            
            # Verificar se a coluna já existe
            cursor.execute("""
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = %s
                AND TABLE_NAME = 'user_progress'
                AND COLUMN_NAME = 'video_time'
            """, (DB_NAME,))
            
            column_exists = cursor.fetchone()
            
            if column_exists:
                print("✅ Coluna video_time já existe!")
                return

            print("➕ Adicionando coluna video_time...")

            # Adicionar a coluna video_time
            cursor.execute("""
                ALTER TABLE user_progress
                ADD COLUMN video_time FLOAT NOT NULL DEFAULT 0.0
            """)
            
            connection.commit()
            print("✅ Coluna video_time adicionada com sucesso!")
            
            # Verificar a estrutura da tabela
            print("\n📋 Estrutura atual da tabela user_progress:")
            cursor.execute("DESCRIBE user_progress")
            columns = cursor.fetchall()
            
            for column in columns:
                field, type_info, null, key, default, extra = column
                print(f"   {field}: {type_info} (NULL: {null}, Default: {default})")
        
        connection.close()
        
    except Exception as e:
        print(f"❌ Erro ao adicionar coluna: {e}")

if __name__ == "__main__":
    add_current_time_column()
