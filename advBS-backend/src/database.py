# Database configuration for FastAPI
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do banco de dados
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv("DB_PASSWORD", '')
DB_NAME = os.getenv("DB_NAME", 'BS')

print(f"🔗 Conectando ao banco: {DB_HOST}:{DB_PORT}/{DB_NAME}")

def create_database_if_not_exists():
    """Criar banco de dados se não existir"""
    try:
        # Conectar sem especificar banco para criar o banco
        temp_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
        temp_engine = create_engine(temp_url)

        with temp_engine.connect() as conn:
            # Verificar se banco existe
            result = conn.execute(text(f"SHOW DATABASES LIKE '{DB_NAME}'"))
            if not result.fetchone():
                # Criar banco se não existir
                conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
                print(f"✅ Banco de dados '{DB_NAME}' criado com sucesso!")
            else:
                print(f"✅ Banco de dados '{DB_NAME}' já existe!")

        temp_engine.dispose()
        return True
    except Exception as e:
        print(f"❌ Erro ao criar banco de dados: {str(e)}")
        return False

# Criar banco se não existir
create_database_if_not_exists()

# URL de conexão
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criar engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL debugging
    pool_pre_ping=True,
    pool_recycle=300
)

# Criar sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """Criar nova sessão do banco de dados"""
    return SessionLocal()

def test_connection():
    """Testar conexão com o banco"""
    try:
        session = get_db_session()
        session.execute("SELECT 1")
        session.close()
        print("✅ Conexão com banco de dados OK!")
        return True
    except Exception as e:
        print(f"❌ Erro na conexão com banco: {str(e)}")
        return False