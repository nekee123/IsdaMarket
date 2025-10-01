from datetime import datetime, timedelta, timezone
from typing import Dict, Any
from jose import jwt, JWTError
from passlib.context import CryptContext
from ..config import settings

# Use PBKDF2-SHA256 as the primary hashing scheme to avoid depending on the
# bcrypt C extension. PBKDF2-SHA256 is widely supported and avoids the
# 72-byte bcrypt limitation. If you prefer bcrypt, reinstall the bcrypt
# package on the host and switch schemes back to bcrypt_sha256.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Keep a password byte-limit constant for reference/validation (bcrypt limit)
# PBKDF2 itself doesn't have the 72-byte restriction, but we still enforce
# a max length in schemas to avoid accidental huge inputs.
MAX_PASSWORD_BYTES = 72


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: timedelta = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and verify a JWT access token"""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        raise ValueError("Invalid token")
