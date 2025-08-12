#!/usr/bin/env python3
"""
Script para inicializar o banco de dados com as tabelas necessárias
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Carregar variáveis de ambiente
try:
    load_dotenv()
except:
    pass

# Configurações do banco de dados
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'BS')

# String de conexão
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"🔗 Conectando ao banco: {DB_HOST}:{DB_PORT}/{DB_NAME}")

try:
    # Criar engine
    engine = create_engine(DATABASE_URL)
    
    # Testar conexão
    with engine.connect() as connection:
        print("✅ Conexão com banco estabelecida!")
        
        # Verificar tabelas existentes
        result = connection.execute(text("SHOW TABLES"))
        existing_tables = [row[0] for row in result.fetchall()]
        print(f"📋 Tabelas existentes: {existing_tables}")
        
        # SQL para criar tabelas
        create_tables_sql = """
        -- Tabela de usuários (já deve existir)
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            username VARCHAR(100) UNIQUE,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            cpf VARCHAR(14),
            phone VARCHAR(20),
            address TEXT,
            city VARCHAR(100),
            state VARCHAR(50),
            zip_code VARCHAR(10),
            type ENUM('admin', 'cliente') DEFAULT 'cliente',
            register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP NULL
        );
        
        -- Tabela de serviços
        CREATE TABLE IF NOT EXISTS services (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            price DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Tabela de casos de clientes
        CREATE TABLE IF NOT EXISTS client_cases (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            service_id INT,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            status ENUM('pendente', 'em_andamento', 'parado_na_justica', 'concluido') DEFAULT 'pendente',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE SET NULL
        );
        
        -- Tabela de arquivos de processos
        CREATE TABLE IF NOT EXISTS process_files (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            case_id INT,
            filename VARCHAR(255) NOT NULL,
            original_filename VARCHAR(255) NOT NULL,
            file_path VARCHAR(500) NOT NULL,
            file_size INT,
            mime_type VARCHAR(100),
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (case_id) REFERENCES client_cases(id) ON DELETE SET NULL
        );
        """
        
        # Executar criação de tabelas
        print("🔨 Criando tabelas...")
        for statement in create_tables_sql.split(';'):
            statement = statement.strip()
            if statement:
                try:
                    connection.execute(text(statement))
                    print(f"✅ Executado: {statement[:50]}...")
                except Exception as e:
                    print(f"⚠️ Erro ao executar: {statement[:50]}... - {e}")
        

        # Inserir dados de exemplo
        print("📝 Inserindo dados de exemplo...")

        # Inserir serviços de exemplo
        services_sql = """
        INSERT IGNORE INTO services (name, description, price) VALUES
        ('Suspensão de CNH', 'Defesa em processo de suspensão de CNH', 1500.00),
        ('Cassação de CNH', 'Defesa em processo de cassação de CNH', 2000.00),
        ('Multa de Trânsito', 'Recurso contra multa de trânsito', 500.00),
        ('Acidente de Trânsito', 'Assessoria jurídica em acidente de trânsito', 2500.00),
        ('Habilitação Especial', 'Processo para habilitação especial', 1200.00)
        """

        try:
            connection.execute(text(services_sql))
            print("✅ Serviços de exemplo inseridos!")
        except Exception as e:
            print(f"⚠️ Erro ao inserir serviços: {e}")
        
        # Verificar tabelas criadas
        result = connection.execute(text("SHOW TABLES"))
        final_tables = [row[0] for row in result.fetchall()]
        print(f"🎉 Tabelas finais: {final_tables}")
        
        print("🎉 Banco de dados inicializado com sucesso!")

except Exception as e:
    print(f"❌ Erro ao inicializar banco: {e}")
    sys.exit(1)
