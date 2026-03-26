#para la conexion de ba se de datos 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import os

#1. defenimos URL de la conexión 
DATABASE_URL = os.getenv("DATABASE_URL","postgresql://admin:123456@postgres:5432/DB_miapi")

# 2. Crear el motor de la conexión

engine= create_engine(DATABASE_URL)
# 3. Creamos la gestión de sessiones
SessionLocal= sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#4. Base declarativa para Modelo
Base= declarative_base()

#5 funcion que trabajar sesiones con la speticiones

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()