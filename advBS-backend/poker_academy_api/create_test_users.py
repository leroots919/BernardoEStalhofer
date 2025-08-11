#!/usr/bin/env python3
"""
Script para criar usuários de teste no banco de dados BS
"""

import sys
import os
import mysql.connector
from werkzeug.security import generate_password_hash

# Configurações do banco
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'BS'
}

def create_database_if_not_exists():
    """Cria o banco de dados BS se não existir"""
    try:
        # Conectar sem especificar o banco
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # Criar banco se não existir
        cursor.execute("CREATE DATABASE IF NOT EXISTS BS")
        print("✅ Banco de dados 'BS' criado/verificado com sucesso")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"❌ Erro ao criar banco de dados: {e}")
        return False
    
    return True

def create_tables():
    """Cria as tabelas necessárias"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Criar tabela users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                username VARCHAR(100) UNIQUE,
                email VARCHAR(100) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                type ENUM('admin', 'cliente') NOT NULL DEFAULT 'cliente',
                register_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME NULL,
                cpf VARCHAR(14),
                phone VARCHAR(20),
                address TEXT,
                city VARCHAR(100),
                state VARCHAR(2),
                zip_code VARCHAR(10)
            )
        """)
        
        # Criar tabela services
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS services (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                description TEXT,
                category ENUM('multas', 'cnh', 'acidentes', 'consultoria', 'recursos') NOT NULL,
                price DECIMAL(10, 2),
                duration_days INT,
                active BOOLEAN NOT NULL DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Criar tabela client_cases
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS client_cases (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                service_id INT NOT NULL,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                status ENUM('pendente', 'em_andamento', 'concluido', 'arquivado') NOT NULL DEFAULT 'pendente',
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
            )
        """)
        
        # Criar tabela consultations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                service_id INT NOT NULL,
                scheduled_date DATETIME NOT NULL,
                status ENUM('pendente', 'em_andamento', 'concluido', 'cancelado') NOT NULL DEFAULT 'pendente',
                notes TEXT,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
            )
        """)
        
        # Criar tabela favorites
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                user_id INT NOT NULL,
                service_id INT NOT NULL,
                PRIMARY KEY (user_id, service_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE
            )
        """)

        # Criar tabela process_files
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
        
        conn.commit()
        print("✅ Tabelas criadas com sucesso")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        return False
    
    return True

def create_test_users():
    """Cria usuários de teste"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Hash das senhas
        admin_hash = generate_password_hash("admin123")
        cliente_hash = generate_password_hash("cliente123")
        
        # Inserir usuário admin
        cursor.execute("""
            INSERT IGNORE INTO users (name, username, email, password_hash, type)
            VALUES (%s, %s, %s, %s, %s)
        """, ("Administrador", "admin", "admin@advtransito.com", admin_hash, "admin"))
        
        # Inserir usuário cliente
        cursor.execute("""
            INSERT IGNORE INTO users (name, username, email, password_hash, type)
            VALUES (%s, %s, %s, %s, %s)
        """, ("Cliente Teste", "cliente", "cliente@teste.com", cliente_hash, "cliente"))
        
        conn.commit()
        print("✅ Usuários de teste criados:")
        print("   Admin: admin@advtransito.com / admin123")
        print("   Cliente: cliente@teste.com / cliente123")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"❌ Erro ao criar usuários: {e}")
        return False
    
    return True

def create_test_services():
    """Cria serviços de teste"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        services = [
            ("Recurso de Multa", "Contestação de multas de trânsito indevidas com base na legislação vigente.", "multas", 150.00, 30),
            ("Defesa CNH - Suspensão", "Defesa contra suspensão da CNH por pontuação ou infrações graves.", "cnh", 300.00, 45),
            ("Assessoria em Acidentes", "Orientação jurídica completa em casos de acidentes de trânsito.", "acidentes", 250.00, 60),
            ("Consultoria Jurídica", "Consultoria especializada em direito de trânsito.", "consultoria", 100.00, 7),
            ("Recurso Administrativo", "Defesa em processos administrativos junto aos órgãos de trânsito.", "recursos", 200.00, 30)
        ]
        
        for service in services:
            cursor.execute("""
                INSERT IGNORE INTO services (name, description, category, price, duration_days)
                VALUES (%s, %s, %s, %s, %s)
            """, service)
        
        conn.commit()
        print("✅ Serviços de teste criados")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"❌ Erro ao criar serviços: {e}")
        return False
    
    return True

def main():
    print("🚀 Iniciando configuração do banco de dados BS...")
    
    # Criar banco de dados
    if not create_database_if_not_exists():
        return
    
    # Criar tabelas
    if not create_tables():
        return
    
    # Criar usuários de teste
    if not create_test_users():
        return
    
    # Criar serviços de teste
    if not create_test_services():
        return
    
    print("\n🎉 Configuração concluída com sucesso!")
    print("\nVocê pode agora:")
    print("1. Iniciar o servidor backend")
    print("2. Acessar o frontend")
    print("3. Fazer login com as credenciais de teste")

if __name__ == "__main__":
    main()
