from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

# Caminho absoluto do banco
DB_PATH = Path(__file__).resolve().parent / "database.db"

# String de conexão para SQLite
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# Criar engine e sessão
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base ORM
Base = declarative_base()


def get_db():
    """Fornece uma sessão de banco de dados (usado em CRUD e Streamlit)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
