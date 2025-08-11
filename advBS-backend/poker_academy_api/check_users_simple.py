# check_users_simple.py - Script para verificar usuários existentes
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app
from src.models import db, Users
from src.auth import AuthService

def check_existing_users():
    with app.app_context():
        print("=== USUÁRIOS EXISTENTES NO BANCO ===")
        users = Users.query.all()
        
        if not users:
            print("Nenhum usuário encontrado no banco.")
            return
        
        for user in users:
            print(f"ID: {user.id}")
            print(f"Nome: {user.name}")
            print(f"Email: {user.email}")
            print(f"Tipo: {user.type.value}")
            print(f"Data de registro: {user.register_date}")
            print("-" * 30)
        
        print(f"\nTotal de usuários: {len(users)}")

def create_test_admin():
    with app.app_context():
        # Verificar se já existe um admin
        admin = Users.query.filter_by(email="admin@pokeracademy.com").first()
        if admin:
            print("Admin já existe!")
            return
        
        # Criar admin de teste
        admin_user = Users(
            name="admin",
            email="admin@pokeracademy.com",
            password_hash=AuthService.hash_password("admin123"),
            type="admin",
            register_date=db.func.current_timestamp()
        )
        
        db.session.add(admin_user)
        db.session.commit()
        print("Admin criado com sucesso!")
        print("Email: admin@pokeracademy.com")
        print("Senha: admin123")

if __name__ == "__main__":
    print("🔍 Verificando usuários...")
    check_existing_users()
    
    print("\n🔧 Criando admin se necessário...")
    create_test_admin()
    
    print("\n🔍 Verificação final...")
    check_existing_users()
