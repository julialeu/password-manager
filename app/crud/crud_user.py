# app/crud/crud_user.py

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Busca un usuario por su dirección de email.
    
    :param db: La sesión de la base de datos.
    :param email: El email del usuario a buscar.
    :return: El objeto User si se encuentra, de lo contrario None.
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    """
    Crea un nuevo usuario en la base de datos.
    
    :param db: La sesión de la base de datos.
    :param user: Los datos del usuario a crear (schema UserCreate).
    :return: El objeto User recién creado.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user