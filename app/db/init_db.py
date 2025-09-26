from app.db.session import engine
from app.db.base_class import Base
from app.models.user import User
from app.models.vault_item import VaultItem

# def init_db():
#     print("Creating database tables...")
#     Base.metadata.create_all(bind=engine)
#     print("Database tables created.")

def create_db_and_tables():
    """
    Crea las tablas en la base de datos si no existen.
    """
    print("Attempting to create database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables creation complete.")




if __name__ == "__main__":
    init_db()