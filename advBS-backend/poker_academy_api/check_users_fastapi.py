# Verificar usuários no banco BS para FastAPI
import sys
import os

# Adicionar src ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

from models import Users
from database import get_db_session

def check_users():
    print("🔍 Verificando usuários no banco BS...")
    
    try:
        session = get_db_session()
        users = session.query(Users).all()
        
        print(f"✅ Encontrados {len(users)} usuário(s):")
        for user in users:
            print(f"   ID: {user.id} | {user.name} | {user.email} | {user.type.value} | Senha: {user.password_hash}")
        
        session.close()
        
    except Exception as e:
        print(f"❌ Erro ao verificar usuários: {str(e)}")

if __name__ == "__main__":
    check_users()
