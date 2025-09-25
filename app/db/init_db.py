# app/db/init_db.py

from app.db.session import engine
from app.db.base_class import Base
from app.models.user import User
from app.models.vault_item import VaultItem

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

if __name__ == "__main__":
    init_db()