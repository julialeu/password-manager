# app/schemas/user.py

from pydantic import BaseModel, EmailStr, ConfigDict

# --- User Schemas ---

# Propiedades compartidas que tienen todos los schemas del usuario
class UserBase(BaseModel):
    email: EmailStr

# Propiedades a recibir al crear un nuevo usuario
class UserCreate(UserBase):
    password: str

# Propiedades contenidas en el modelo de la DB pero que no se deben devolver
class UserInDBBase(UserBase):
    id: int
    is_active: bool
    hashed_password: str
    
    model_config = ConfigDict(from_attributes=True)

# Propiedades a devolver al cliente
class User(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)