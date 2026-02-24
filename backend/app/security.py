from datetime import datetime, timedelta, timezone
from jose import jwt
from app.settings import get_settings
from hashlib import sha256
from pwdlib import PasswordHash

settings = get_settings()

pwd_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return pwd_hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_hasher.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: int = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_delta or settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")