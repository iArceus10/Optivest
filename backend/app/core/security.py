from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Configure password hashing using bcrypt.
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) ->str:
    """
    Hash a plain-text password using bcrypt.
    """
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plain-text password against its bcrypt hash.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a signed JWT access token.
    """

    if expires_delta is None:
        expires_delta = timedelta(
            minutes=settings.access_token_expire_minutes
        )

    expire = datetime.now(timezone.utc) + expires_delta

    payload: dict[str, Any] = {
        "sub": subject,
        "exp": expire,
    }

    encoded_jwt = jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )

    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and verify a JWT access token.

    Raises:
        JWTError: If the token is invalid, expired, or missing required claims.
    """

    payload = jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )

    subject = payload.get("sub")
    if subject is None:
        raise JWTError("Missing subject claim.")

    return payload