# app/db/init_db.py

from app.db.session import engine
# Importamos Base y los modelos para que SQLAlchemy los conozca
from app.db.base_class import Base
from app.models.user import User

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

if __name__ == "__main__":
    init_db()