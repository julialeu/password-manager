from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.core.config import settings
from cryptography.fernet import Fernet

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

# ENCRYPTION_KEY = settings.SECRET_KEY[:32].encode('utf-8').ljust(32, b'\0')
# Usamos una parte de la SECRET_KEY para simplificar, pero en producción deberían ser claves separadas.
# Fernet requiere una clave de 32 bytes.

_cipher_suite = Fernet(settings.ENCRYPTION_KEY.encode('utf-8'))

def encrypt_data(data: str) -> str:
    """Cifra un string y lo devuelve como string."""
    if not data:
        return data
    encrypted_bytes = _cipher_suite.encrypt(data.encode('utf-8'))
    return encrypted_bytes.decode('utf-8')

def decrypt_data(encrypted_data: str) -> str:
    """Descifra un string y lo devuelve como string."""
    if not encrypted_data:
        return encrypted_data
    decrypted_bytes = _cipher_suite.decrypt(encrypted_data.encode('utf-8'))
    return decrypted_bytes.decode('utf-8')

# --- Funciones para Reseteo de Contraseña ---

def create_password_reset_token(email: str) -> str:
    """Crea un token JWT para el reseteo de contraseña."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES  # Reutilizamos el tiempo de expiración
    )
    to_encode = {
        "exp": expire,
        "sub": email,
        "scope": "password_reset"  # Un 'scope' para diferenciarlo de un token de acceso
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password_reset_token(token: str) -> str | None:
    """Verifica el token de reseteo de contraseña y devuelve el email."""
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # Asegurarnos de que el token es para reseteo de contraseña
        if decoded_token.get("scope") == "password_reset":
            return decoded_token.get("sub")
        return None
    except JWTError:
        return None     