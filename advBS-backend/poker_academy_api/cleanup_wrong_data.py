# cleanup_wrong_data.py - Remover dados incorretos criados por engano
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app
from src.models import db, Users

def cleanup_wrong_users():
    with app.app_context():
        print("🧹 Limpando dados incorretos...")
        
        # Remover usuário admin@pokeracademy.com que foi criado por engano
        wrong_admin = Users.query.filter_by(email="admin@pokeracademy.com").first()
        if wrong_admin:
            print(f"❌ Removendo usuário incorreto: {wrong_admin.email}")
            db.session.delete(wrong_admin)
            db.session.commit()
            print("✅ Usuário incorreto removido!")
        else:
            print("✅ Nenhum usuário incorreto encontrado.")
        
        # Listar usuários corretos restantes
        print("\n📋 Usuários corretos no sistema:")
        users = Users.query.all()
        
        for user in users:
            print(f"   ID {user.id}: {user.name} ({user.email}) - {user.type.value}")
        
        print(f"\nTotal de usuários: {len(users)}")

if __name__ == "__main__":
    cleanup_wrong_users()
