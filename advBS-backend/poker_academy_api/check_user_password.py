import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import get_db_session
from sqlalchemy import text

def check_user_password():
    """Verificar informações do usuário vanessafk007@gmail.com"""
    session = get_db_session()
    
    try:
        print("🔍 Buscando informações do usuário vanessafk007@gmail.com...")
        
        # Buscar usuário
        result = session.execute(text("""
            SELECT id, name, email, password_hash, type, register_date
            FROM users 
            WHERE email = 'vanessafk007@gmail.com'
        """))
        
        user = result.fetchone()
        
        if user:
            print(f"\n✅ Usuário encontrado:")
            print(f"   ID: {user.id}")
            print(f"   Nome: {user.name}")
            print(f"   Email: {user.email}")
            print(f"   Tipo: {user.type}")
            print(f"   Data de cadastro: {user.register_date}")
            print(f"   Hash da senha: {user.password_hash}")
            
            # Verificar se é uma senha comum
            common_passwords = ['123456', 'password', 'cliente123', 'vanessa123', '123']
            
            print(f"\n🔐 Testando senhas comuns...")
            
            # Importar função de verificação de senha
            from werkzeug.security import check_password_hash
            
            for pwd in common_passwords:
                if check_password_hash(user.password_hash, pwd):
                    print(f"✅ SENHA ENCONTRADA: '{pwd}'")
                    return pwd
                else:
                    print(f"❌ Não é: '{pwd}'")
            
            print(f"\n💡 Senha não encontrada nas opções comuns.")
            print(f"💡 Você pode redefinir a senha no banco ou usar o admin.")
            
        else:
            print("❌ Usuário não encontrado!")
            
            # Listar todos os usuários
            print("\n📋 Usuários cadastrados:")
            result = session.execute(text("SELECT id, name, email, type FROM users"))
            users = result.fetchall()
            for u in users:
                print(f"   ID: {u.id} | {u.name} | {u.email} | {u.type}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    check_user_password()
