from app.db.session import engine
from app.db.base_class import Base

def create_db_and_tables():
    """
    Create the tables in DB if they do not exist.
    """
    print("Attempting to create database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables creation complete.")


if __name__ == "__main__":
    init_db()