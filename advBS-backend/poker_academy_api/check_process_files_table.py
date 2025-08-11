import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import get_db_session
from sqlalchemy import text

def check_and_create_process_files_table():
    """Verificar e criar tabela ProcessFiles se necessário"""
    session = get_db_session()
    
    try:
        print("🔍 Verificando se a tabela ProcessFiles existe...")
        
        # Verificar se a tabela existe
        result = session.execute(text("SHOW TABLES LIKE 'ProcessFiles'"))
        table_exists = result.fetchone() is not None
        
        if table_exists:
            print("✅ Tabela ProcessFiles já existe!")
            
            # Mostrar estrutura da tabela
            result = session.execute(text("DESCRIBE ProcessFiles"))
            columns = result.fetchall()
            print("\n📋 Estrutura da tabela ProcessFiles:")
            for column in columns:
                print(f"   - {column[0]}: {column[1]}")
        else:
            print("❌ Tabela ProcessFiles não existe. Criando...")
            
            # Primeiro verificar as tabelas existentes
            print("🔍 Verificando tabelas existentes...")
            result = session.execute(text("SHOW TABLES"))
            tables = result.fetchall()
            print("📋 Tabelas existentes:")
            for table in tables:
                print(f"   - {table[0]}")

            # Criar a tabela ProcessFiles sem foreign keys primeiro
            create_table_sql = """
            CREATE TABLE ProcessFiles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                original_filename VARCHAR(255) NOT NULL,
                stored_filename VARCHAR(255) NOT NULL,
                file_path VARCHAR(500) NOT NULL,
                file_size INT NOT NULL,
                description TEXT,
                user_id INT NOT NULL,
                case_id INT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
            
            session.execute(text(create_table_sql))
            session.commit()
            print("✅ Tabela ProcessFiles criada com sucesso!")
            
            # Verificar a estrutura criada
            result = session.execute(text("DESCRIBE ProcessFiles"))
            columns = result.fetchall()
            print("\n📋 Estrutura da tabela ProcessFiles criada:")
            for column in columns:
                print(f"   - {column[0]}: {column[1]}")
        
        # Verificar quantos arquivos existem
        result = session.execute(text("SELECT COUNT(*) FROM ProcessFiles"))
        count = result.fetchone()[0]
        print(f"\n📊 Total de arquivos na tabela: {count}")
        
        if count > 0:
            # Mostrar alguns arquivos
            result = session.execute(text("""
                SELECT id, original_filename, user_id, created_at 
                FROM ProcessFiles 
                ORDER BY created_at DESC 
                LIMIT 5
            """))
            files = result.fetchall()
            print("\n📁 Últimos arquivos:")
            for file in files:
                print(f"   ID: {file[0]} | {file[1]} | User: {file[2]} | {file[3]}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    check_and_create_process_files_table()
