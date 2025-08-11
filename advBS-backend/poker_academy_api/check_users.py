# check_users.py - Script para verificar usuários existentes
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app
from src.models import db, Users, Classes
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
        
        # Verificar aulas também
        print("\n=== AULAS EXISTENTES NO BANCO ===")
        classes = Classes.query.all()
        print(f"Total de aulas: {len(classes)}")
        
        if classes:
            for cls in classes[:3]:  # Mostrar apenas as 3 primeiras
                print(f"- {cls.name} (Instrutor: {cls.instructor})")
            if len(classes) > 3:
                print(f"... e mais {len(classes) - 3} aulas")

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

def create_test_student():
    with app.app_context():
        # Verificar se já existe um aluno de teste
        student = Users.query.filter_by(email="aluno@pokeracademy.com").first()
        if student:
            print("Aluno de teste já existe!")
            return
        
        # Criar aluno de teste
        student_user = Users(
            name="aluno",
            email="aluno@pokeracademy.com",
            password_hash=AuthService.hash_password("aluno123"),
            type="student",
            register_date=db.func.current_timestamp()
        )
        
        db.session.add(student_user)
        db.session.commit()
        print("Aluno de teste criado com sucesso!")
        print("Email: aluno@pokeracademy.com")
        print("Senha: aluno123")

if __name__ == "__main__":
    print("1. Verificando usuários existentes...")
    check_existing_users()
    
    print("\n2. Criando usuários de teste...")
    create_test_admin()
    create_test_student()
    
    print("\n3. Verificação final...")
    check_existing_users()
