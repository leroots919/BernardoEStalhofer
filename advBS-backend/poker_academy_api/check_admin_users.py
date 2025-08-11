# check_admin_users.py - Verificar usuários admin
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app
from src.models import db, Users, UserType

def check_admin_users():
    with app.app_context():
        print("🔍 Verificando usuários admin no banco...")
        
        # Buscar todos os usuários admin
        admins = Users.query.filter_by(type=UserType.admin).all()
        
        if not admins:
            print("❌ Nenhum usuário admin encontrado!")
            return
        
        print(f"✅ Encontrados {len(admins)} usuário(s) admin:")
        for admin in admins:
            print(f"   ID: {admin.id}")
            print(f"   Nome: {admin.name}")
            print(f"   Email: {admin.email}")
            print(f"   Tipo: {admin.type.value}")
            print(f"   Data registro: {admin.register_date}")
            print("   ---")

def check_all_users():
    with app.app_context():
        print("\n🔍 Verificando TODOS os usuários no banco...")
        
        users = Users.query.all()
        
        if not users:
            print("❌ Nenhum usuário encontrado!")
            return
        
        print(f"✅ Encontrados {len(users)} usuário(s) total:")
        for user in users:
            print(f"   ID: {user.id} | {user.name} | {user.email} | {user.type.value}")

if __name__ == "__main__":
    check_admin_users()
    check_all_users()
