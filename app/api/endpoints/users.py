# app/api/endpoints/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas.user import User, UserCreate
from app.crud import crud_user

router = APIRouter()

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate
):
    """
    Crea un nuevo usuario en el sistema.
    """
    user = crud_user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )
    
    user = crud_user.create_user(db=db, user=user_in)
    return user