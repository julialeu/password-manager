from typing import Generator
from app.db.session import SessionLocal

def get_db() -> Generator:
    """
    Dependencia de FastAPI para obtener una sesión de base de datos.
    Asegura que la sesión se cierre después de cada petición.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()