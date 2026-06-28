from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.models.user import User

from app.database.session import get_db
from app.schemas.auth import (
    Token,
    UserRegister,
    UserLogin,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db),
):
    try:
        return AuthService.register(db, user_data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.post(
    "/login",
    response_model=Token,
)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
):
    try:
        return AuthService.authenticate(
            db,
            credentials,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )
    
@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current authenticated user",
)
def get_current_user_profile(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """
    Return the currently authenticated user's profile.
    """
    return current_user