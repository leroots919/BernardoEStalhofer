# Database configuration for FastAPI
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do banco de dados
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'BS')

# URL de conexão
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"🔗 Conectando ao banco: {DB_HOST}:{DB_PORT}/{DB_NAME}")

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
