from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Search for a user by their email address.
    
    :param db: The database session.
    :param email: The email address of the user to search for.
    :return: The User object if found, otherwise None..
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    """
    Creates a new user in the database.
    
    :param db: The database session.
    :param user: The data for the user to be created (UserCreate schema).
    :return: The newly created User object.
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

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """
     Authenticate a user.
    
    :param db: The database session.
    :param email: The user's email address.
    :param password: The password in plain text.
    :return: The User object if authentication is successful, otherwise None.
    """
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user    