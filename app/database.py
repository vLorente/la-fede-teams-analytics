"""Base de datos"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()
# Configura la conexión a la base de datos SQLite
engine = create_engine(os.getenv('DATABASE_URI'))

# Crea una sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DeclarativeBase común para todos los modelos
Base = declarative_base()
