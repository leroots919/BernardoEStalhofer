# check_vanessa_user.py - Verificar dados do usuário vanessa
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app
from src.models import db, Users, UserType

def check_vanessa_user():
    with app.app_context():
        print("🔍 Verificando usuário vanessa...")
        
        # Buscar usuário vanessa
        vanessa = Users.query.filter_by(email="vanessafk007@gmail.com").first()
        
        if not vanessa:
            print("❌ Usuário vanessa não encontrado!")
            return False
        
        print("✅ Usuário vanessa encontrado:")
        print(f"   ID: {vanessa.id}")
        print(f"   Nome: {vanessa.name}")
        print(f"   Email: {vanessa.email}")
        print(f"   Tipo: {vanessa.type.value}")
        print(f"   CPF: {vanessa.cpf}")
        print(f"   Telefone: {vanessa.phone}")
        print(f"   Endereço: {vanessa.address}")
        print(f"   Cidade: {vanessa.city}")
        print(f"   Estado: {vanessa.state}")
        print(f"   CEP: {vanessa.zip_code}")
        print(f"   Data registro: {vanessa.register_date}")
        
        # Verificar se é cliente
        if vanessa.type != UserType.cliente:
            print(f"❌ PROBLEMA: Usuário não é do tipo 'cliente', é '{vanessa.type.value}'")
            return False
        
        print("✅ Usuário está correto como cliente!")
        return True

def fix_vanessa_user():
    with app.app_context():
        print("🔧 Corrigindo usuário vanessa se necessário...")
        
        vanessa = Users.query.filter_by(email="vanessafk007@gmail.com").first()
        
        if not vanessa:
            print("❌ Usuário não encontrado para correção!")
            return False
        
        # Garantir que é cliente
        if vanessa.type != UserType.cliente:
            print(f"🔧 Corrigindo tipo de '{vanessa.type.value}' para 'cliente'")
            vanessa.type = UserType.cliente
            db.session.commit()
            print("✅ Tipo corrigido!")
        
        # Verificar campos obrigatórios
        if not vanessa.name or vanessa.name.strip() == "":
            vanessa.name = "Vanessa"
            print("🔧 Nome corrigido")
        
        db.session.commit()
        print("✅ Usuário vanessa está correto!")
        return True

if __name__ == "__main__":
    print("🔍 Verificando usuário vanessa...")
    is_ok = check_vanessa_user()
    
    if not is_ok:
        print("\n🔧 Tentando corrigir...")
        fix_vanessa_user()
        
        print("\n🔍 Verificação final...")
        check_vanessa_user()
