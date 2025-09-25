from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.core.config import settings
from cryptography.fernet import Fernet

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Hashing de Passwords ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify whether a plaintext password matches a hashed one."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generates the hash of a password."""
    return pwd_context.hash(password)

# --- Creación y Verificación de Tokens JWT ---

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a new JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Por defecto, el token expira en 15 minutos
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

_cipher_suite = Fernet(settings.ENCRYPTION_KEY.encode('utf-8'))

def encrypt_data(data: str) -> str:
    """Encodes a string and returns it as a string."""
    if not data:
        return data
    encrypted_bytes = _cipher_suite.encrypt(data.encode('utf-8'))
    return encrypted_bytes.decode('utf-8')

def decrypt_data(encrypted_data: str) -> str:
    """Decrypts a string and returns it as a string."""
    if not encrypted_data:
        return encrypted_data
    decrypted_bytes = _cipher_suite.decrypt(encrypted_data.encode('utf-8'))
    return decrypted_bytes.decode('utf-8')

# --- Funciones para Reseteo de Contraseña ---

def create_password_reset_token(email: str) -> str:
    """Create a JWT token for password reset."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES  # Reutilizamos el tiempo de expiración
    )
    to_encode = {
        "exp": expire,
        "sub": email,
        "scope": "password_reset"  
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password_reset_token(token: str) -> str | None:
    """Verify the password reset token and return the email."""
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # Asegurarnos de que el token es para reseteo de contraseña
        if decoded_token.get("scope") == "password_reset":
            return decoded_token.get("sub")
        return None
    except JWTError:
        return None     