#!/usr/bin/env python3
"""
Script para atualizar a estrutura do banco de dados BS
"""

import mysql.connector
from mysql.connector import Error

def update_database():
    try:
        # Conectar ao MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='BS'
        )
        
        cursor = connection.cursor()
        
        print("🚀 Atualizando estrutura do banco de dados BS...")
        
        # Verificar se as colunas já existem
        cursor.execute("DESCRIBE users")
        existing_columns = [column[0] for column in cursor.fetchall()]
        
        # Adicionar novas colunas se não existirem
        new_columns = [
            ("cpf", "VARCHAR(14)"),
            ("phone", "VARCHAR(20)"),
            ("address", "TEXT"),
            ("city", "VARCHAR(100)"),
            ("state", "VARCHAR(2)"),
            ("zip_code", "VARCHAR(10)")
        ]
        
        for column_name, column_type in new_columns:
            if column_name not in existing_columns:
                cursor.execute(f"ALTER TABLE users ADD COLUMN {column_name} {column_type}")
                print(f"✅ Coluna '{column_name}' adicionada à tabela users")
            else:
                print(f"ℹ️  Coluna '{column_name}' já existe na tabela users")
        
        # Criar tabela process_files se não existir
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS process_files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                case_id INT,
                filename VARCHAR(255) NOT NULL,
                original_filename VARCHAR(255) NOT NULL,
                file_path VARCHAR(500) NOT NULL,
                description TEXT,
                uploaded_by_admin INT NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (case_id) REFERENCES client_cases(id) ON DELETE CASCADE,
                FOREIGN KEY (uploaded_by_admin) REFERENCES users(id)
            )
        """)
        print("✅ Tabela process_files criada/verificada")
        
        connection.commit()
        print("✅ Estrutura do banco atualizada com sucesso!")
        
    except Error as e:
        print(f"❌ Erro ao atualizar banco de dados: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    update_database()
