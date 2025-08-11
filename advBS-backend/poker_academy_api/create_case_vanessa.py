# create_case_vanessa.py - Criar caso para vanessa
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app
from src.models import db, ClientCases, CaseStatus

def create_case_for_vanessa():
    with app.app_context():
        print("🔧 Criando caso para vanessa (ID: 9)...")
        
        try:
            # Criar novo caso para vanessa
            new_case = ClientCases(
                user_id=9,  # ID da vanessa
                service_id=1,  # Recurso de Multa
                title="Recurso de Multa - Vanessa",
                description="Contestação de multa por excesso de velocidade. Cliente recebeu multa indevida e solicita recurso administrativo.",
                status=CaseStatus.pendente
            )
            
            db.session.add(new_case)
            db.session.commit()
            
            print("✅ Caso criado com sucesso para vanessa!")
            print(f"   ID do Caso: {new_case.id}")
            print(f"   Título: {new_case.title}")
            print(f"   Status: {new_case.status.value}")
            print(f"   Data: {new_case.created_at}")
            
            return new_case.id
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro ao criar caso: {e}")
            import traceback
            traceback.print_exc()
            return None

def list_vanessa_cases():
    with app.app_context():
        print("\n📋 Casos da vanessa (ID: 9):")
        cases = ClientCases.query.filter_by(user_id=9).all()
        
        if not cases:
            print("   Nenhum caso encontrado para vanessa.")
            return
        
        for case in cases:
            print(f"   ID {case.id}: {case.title}")
            print(f"      Status: {case.status.value}")
            print(f"      Criado: {case.created_at}")
            print()

if __name__ == "__main__":
    print("🔍 Verificando casos existentes da vanessa...")
    list_vanessa_cases()
    
    print("🔧 Criando novo caso para vanessa...")
    case_id = create_case_for_vanessa()
    
    if case_id:
        print("\n🔍 Listagem final dos casos da vanessa...")
        list_vanessa_cases()
        
        print(f"\n🎉 Caso criado com sucesso! ID: {case_id}")
        print("✅ Agora vanessa tem um processo no sistema!")
        print("📝 Você pode ver este caso na interface admin.")
    else:
        print("\n❌ Falha ao criar caso para vanessa.")
