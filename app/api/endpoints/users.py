from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.api import deps
from app.schemas.user import User, UserCreate
from app.crud import crud_user
from app.models.user import User as UserModel
from app.schemas.token import Token
from app.core.security import create_access_token
from app.core.config import settings

router = APIRouter()

@router.post("/", response_model=Token, status_code=status.HTTP_201_CREATED)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate
):
    """
    Create new user and returns a token access for automatic login
    """
    user = crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )
    
    # Creamos el usuario en la BD
    user = crud_user.create_user(db=db, user=user_in)
    
    # Generamos un token de acceso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    # Devolvemos el token
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
def read_users_me(
    current_user: UserModel = Depends(deps.get_current_user)
):
    """
    Obtain the current user data.
    """
    return current_user    