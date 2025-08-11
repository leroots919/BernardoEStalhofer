# create_admin.py - Script simples para criar admin
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app
from src.models import db
from src.auth import AuthService
import pymysql

def create_admin_directly():
    """Criar admin diretamente no banco usando SQL"""
    
    # Configurações do banco
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = ""
    DB_NAME = "poker_academy"
    
    try:
        # Conectar ao banco
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Verificar se admin já existe
        cursor.execute("SELECT * FROM users WHERE email = %s", ("admin@pokeracademy.com",))
        existing_admin = cursor.fetchone()
        
        if existing_admin:
            print("Admin já existe!")
            print("Email: admin@pokeracademy.com")
            return
        
        # Hash da senha
        password_hash = AuthService.hash_password("admin123")
        
        # Inserir admin
        insert_query = """
        INSERT INTO users (name, email, password, type, register_date) 
        VALUES (%s, %s, %s, %s, NOW())
        """
        
        cursor.execute(insert_query, (
            "admin",
            "admin@pokeracademy.com", 
            password_hash,
            "admin"
        ))
        
        connection.commit()
        
        print("✅ Admin criado com sucesso!")
        print("📧 Email: admin@pokeracademy.com")
        print("🔑 Senha: admin123")
        
        # Verificar se foi criado
        cursor.execute("SELECT id, name, email, type FROM users WHERE email = %s", ("admin@pokeracademy.com",))
        admin = cursor.fetchone()
        print(f"🆔 ID: {admin[0]}, Nome: {admin[1]}, Tipo: {admin[3]}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

def create_student_directly():
    """Criar aluno de teste diretamente no banco usando SQL"""
    
    # Configurações do banco
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = ""
    DB_NAME = "poker_academy"
    
    try:
        # Conectar ao banco
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Verificar se aluno já existe
        cursor.execute("SELECT * FROM users WHERE email = %s", ("aluno@pokeracademy.com",))
        existing_student = cursor.fetchone()
        
        if existing_student:
            print("Aluno de teste já existe!")
            return
        
        # Hash da senha
        password_hash = AuthService.hash_password("aluno123")
        
        # Inserir aluno
        insert_query = """
        INSERT INTO users (name, email, password, type, register_date) 
        VALUES (%s, %s, %s, %s, NOW())
        """
        
        cursor.execute(insert_query, (
            "aluno",
            "aluno@pokeracademy.com", 
            password_hash,
            "student"
        ))
        
        connection.commit()
        
        print("✅ Aluno de teste criado com sucesso!")
        print("📧 Email: aluno@pokeracademy.com")
        print("🔑 Senha: aluno123")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

def list_users():
    """Listar todos os usuários"""
    
    # Configurações do banco
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = ""
    DB_NAME = "poker_academy"
    
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, email, type, register_date FROM users")
        users = cursor.fetchall()
        
        print("\n=== USUÁRIOS NO BANCO ===")
        for user in users:
            print(f"ID: {user[0]} | Nome: {user[1]} | Email: {user[2]} | Tipo: {user[3]} | Data: {user[4]}")
        print(f"Total: {len(users)} usuários")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    print("🔧 Criando usuários de teste...")
    
    with app.app_context():
        print("\n1️⃣ Listando usuários existentes:")
        list_users()
        
        print("\n2️⃣ Criando admin:")
        create_admin_directly()
        
        print("\n3️⃣ Criando aluno de teste:")
        create_student_directly()
        
        print("\n4️⃣ Listagem final:")
        list_users()
        
        print("\n🎉 Pronto! Agora você pode fazer login com:")
        print("👨‍💼 ADMIN: admin@pokeracademy.com / admin123")
        print("👨‍🎓 ALUNO: aluno@pokeracademy.com / aluno123")
