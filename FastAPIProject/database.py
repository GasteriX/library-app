from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Настройки базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Для SQLite
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"  # Для PostgreSQL

# Создание engine и сессии
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})  # Для SQLite
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание базового класса
Base = declarative_base()
