import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
import jwt

from app.core.config import get_settings


def _bcrypt_secret(password: str) -> str:
    """64-char hex fits bcrypt's 72-byte limit; supports any UTF-8 password length."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    hpw = hashed_password.encode("utf-8")
    try:
        if bcrypt.checkpw(_bcrypt_secret(plain_password).encode("ascii"), hpw):
            return True
    except (ValueError, TypeError):
        pass
    # Legacy: bcrypt(passlib) of plain password; bcrypt rejects secrets > 72 bytes.
    if len(plain_password.encode("utf-8")) > 72:
        return False
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hpw)
    except ValueError:
        return False


def get_password_hash(password: str) -> str:
    secret = _bcrypt_secret(password).encode("ascii")
    hashed = bcrypt.hashpw(secret, bcrypt.gensalt())
    return hashed.decode("ascii")


def create_access_token(subject: str) -> str:
    settings = get_settings()
    expire_at = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload: dict[str, Any] = {"sub": subject, "exp": expire_at}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    settings = get_settings()
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
