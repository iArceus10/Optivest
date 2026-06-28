from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import (
    Token,
    UserLogin,
    UserRegister,
)

from pydantic import EmailStr, field_validator

class AuthService:
    """
    Business logic for authentication.
    """

    @staticmethod
    def register(
        db: Session,
        user_data: UserRegister,
    ) -> User:
        """
        Register a new user.

        Raises:
            ValueError: If the email is already registered.
        """

        normalized_email = user_data.email.lower().strip()

        existing_user = db.scalar(
            select(User).where(
                User.email == normalized_email
            )
        )

        if existing_user:
            raise ValueError(
                "Email is already registered."
            )

        user = User(
            email=normalized_email,
            full_name=user_data.full_name,
            hashed_password=hash_password(
                user_data.password
            ),
        )

        try:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def authenticate(
        db: Session,
        credentials: UserLogin,
    ) -> Token:
        """
        Authenticate a user and return a JWT.
        """

        normalized_email = credentials.email.lower().strip()

        user = db.scalar(
            select(User).where(
                User.email == normalized_email
            )
        )

        if user is None:
            raise ValueError(
                "Invalid email or password."
            )

        if not verify_password(
            credentials.password,
            user.hashed_password,
        ):
            raise ValueError(
                "Invalid email or password."
            )

        access_token = create_access_token(
            subject=str(user.id),
        )

        return Token(
            access_token=access_token,
        )