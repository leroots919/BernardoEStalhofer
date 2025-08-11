import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import get_db_session
from sqlalchemy import text

def check_table_structure():
    """Verificar estrutura real das tabelas"""
    session = get_db_session()
    
    try:
        print("🔍 Verificando estrutura da tabela process_files...")
        
        # Verificar estrutura da tabela process_files
        result = session.execute(text("DESCRIBE process_files"))
        columns = result.fetchall()
        print("\n📋 Estrutura da tabela process_files:")
        for column in columns:
            print(f"   - {column[0]}: {column[1]}")
        
        print("\n🔍 Verificando estrutura da tabela users...")
        result = session.execute(text("DESCRIBE users"))
        columns = result.fetchall()
        print("\n📋 Estrutura da tabela users:")
        for column in columns:
            print(f"   - {column[0]}: {column[1]}")
        
        print("\n🔍 Verificando estrutura da tabela client_cases...")
        result = session.execute(text("DESCRIBE client_cases"))
        columns = result.fetchall()
        print("\n📋 Estrutura da tabela client_cases:")
        for column in columns:
            print(f"   - {column[0]}: {column[1]}")
        
        # Verificar dados na tabela process_files
        result = session.execute(text("SELECT COUNT(*) FROM process_files"))
        count = result.fetchone()[0]
        print(f"\n📊 Total de arquivos na tabela process_files: {count}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    check_table_structure()
