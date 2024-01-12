"""
Este módulo contiene las rutas y funciones para el manejo de items en la aplicación FastAPI.
"""

import os
import mysql.connector
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


API_KEY_NAME = "X-API-KEY"
API_KEY = "tu_apy_key_secreta"

app = FastAPI()
app.mount("/static", StaticFiles(directory="./app/static"), name="static")
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso no autorizado"
        )

# ... (resto del código)

def connect_to_database():
    # Configurar los parámetros de conexión
    config = {
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME'),
        'raise_on_warnings': True
    }

    # Establecer la conexión
    connection = mysql.connector.connect(**config)

    # Crear un cursor para ejecutar consultas
    cursor = connection.cursor()

    # Retornar la conexión y el cursor
    return connection, cursor

# Cerrar la conexión y el cursor cuando hayas terminado de usarlos
def close_database_connection(connection, cursor):
    cursor.close()
    connection.close()

# Ejemplo de uso
conn, cursor = connect_to_database()

# ... (realizar operaciones en la base de datos)

# Cerrar la conexión y el cursor al final
close_database_connection(conn, cursor)

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
