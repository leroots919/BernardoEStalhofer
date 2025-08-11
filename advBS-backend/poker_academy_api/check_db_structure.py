# check_db_structure.py - Verificar estrutura real do banco
import pymysql

def check_table_structure():
    """Verificar a estrutura real da tabela users"""
    
    # Configurações do banco
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = ""
    DB_NAME = "poker_academy"
    
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Verificar estrutura da tabela users
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        
        print("=== ESTRUTURA DA TABELA USERS ===")
        for column in columns:
            print(f"Campo: {column[0]} | Tipo: {column[1]} | Null: {column[2]} | Key: {column[3]} | Default: {column[4]}")
        
        # Verificar estrutura da tabela classes
        print("\n=== ESTRUTURA DA TABELA CLASSES ===")
        cursor.execute("DESCRIBE classes")
        columns = cursor.fetchall()
        
        for column in columns:
            print(f"Campo: {column[0]} | Tipo: {column[1]} | Null: {column[2]} | Key: {column[3]} | Default: {column[4]}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

def create_admin_with_correct_column():
    """Criar admin usando o nome correto da coluna"""
    
    # Configurações do banco
    DB_HOST = "localhost"
    DB_USER = "root"
    DB_PASSWORD = ""
    DB_NAME = "poker_academy"
    
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Verificar se admin já existe
        cursor.execute("SELECT * FROM users WHERE email = %s", ("admin@pokeracademy.com",))
        existing_admin = cursor.fetchone()
        
        if existing_admin:
            print("Admin já existe!")
            return
        
        # Usar bcrypt para hash da senha (mesmo que o backend usa)
        import bcrypt
        password_hash = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Tentar diferentes nomes de coluna para senha
        try:
            # Primeiro tentar com password_hash
            insert_query = """
            INSERT INTO users (name, email, password_hash, type, register_date) 
            VALUES (%s, %s, %s, %s, NOW())
            """
            cursor.execute(insert_query, ("admin", "admin@pokeracademy.com", password_hash, "admin"))
            
        except pymysql.err.ProgrammingError:
            # Se falhar, tentar com password
            insert_query = """
            INSERT INTO users (name, email, password, type, register_date) 
            VALUES (%s, %s, %s, %s, NOW())
            """
            cursor.execute(insert_query, ("admin", "admin@pokeracademy.com", password_hash, "admin"))
        
        connection.commit()
        print("✅ Admin criado com sucesso!")
        print("📧 Email: admin@pokeracademy.com")
        print("🔑 Senha: admin123")
        
    except Exception as e:
        print(f"❌ Erro ao criar admin: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    print("🔍 Verificando estrutura do banco...")
    check_table_structure()
    
    print("\n🔧 Tentando criar admin...")
    create_admin_with_correct_column()
