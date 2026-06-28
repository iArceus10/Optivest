from app.database.session import SessionLocal
from app.schemas.auth import UserLogin, UserRegister
from app.services.auth_service import AuthService

db = SessionLocal()

try:
    user = AuthService.register(
        db,
        UserRegister(
            email="john@example.com",
            full_name="John Doe",
            password="Password123!",
        ),
    )

    print(user.email)

    token = AuthService.authenticate(
        db,
        UserLogin(
            email="john@example.com",
            password="Password123!",
        ),
    )

    print(token)

finally:
    db.close()