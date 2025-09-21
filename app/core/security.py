from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.core.config import settings

# Configuración de Passlib para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Hashing de Contraseñas ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña en texto plano coincide con una hasheada."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Genera el hash de una contraseña."""
    return pwd_context.hash(password)

# --- Creación y Verificación de Tokens JWT ---

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Crea un nuevo token de acceso JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Por defecto, el token expira en 15 minutos si no se especifica
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt