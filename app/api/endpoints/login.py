from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_user
from app.schemas.token import Token
from app.schemas.password_reset import PasswordReset
from app.core.security import create_access_token, create_password_reset_token, get_password_hash, verify_password_reset_token
from app.core.config import settings

router = APIRouter()

@router.post("/token", response_model=Token)
def login_for_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = crud_user.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/password-recovery/{email}", status_code=status.HTTP_200_OK)
def recover_password(email: str, db: Session = Depends(deps.get_db)):
    """
    Start the password recovery process.
    """
    user = crud_user.get_user_by_email(db, email=email)

    if not user:
        # No revelamos si el usuario existe o no por seguridad.
        # Simplemente actuamos como si el proceso hubiera funcionado con normalidad.
        print(f"Password recovery requested for non-existent user: {email}")
        return {"msg": "If a user with that email exists, a password recovery link has been sent."}

    password_reset_token = create_password_reset_token(email=email)
    
    print("--- PASSWORD RESET TOKEN (SIMULATED EMAIL) ---")
    print(f"User: {user.email}")
    print(f"Token: {password_reset_token}")
    print("-----------------------------------------------")
    
    return {"msg": "If a user with that email exists, a password recovery link has been sent."}

@router.post("/reset-password/", status_code=status.HTTP_200_OK)
def reset_password(
    *,
    db: Session = Depends(deps.get_db),
    reset_data: PasswordReset
):
    """
    Reset the password using a valid token.
    """
    email = verify_password_reset_token(token=reset_data.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token",
        )
    
    user = crud_user.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this email does not exist.",
        )
        
        
    
    hashed_password = get_password_hash(reset_data.new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    
    return {"msg": "Password updated successfully"}    