from app.schemas.auth import (
    UserRegister,
    UserLogin,
    Token,
    TokenPayload,
    UserResponse,
)

register = UserRegister(
    email="john@example.com",
    full_name="John Doe",
    password="Password123!",
)

print(register)

login = UserLogin(
    email="john@example.com",
    password="Password123!",
)

print(login)

token = Token(
    access_token="sample-token",
)

print(token)

payload = TokenPayload(
    sub="john@example.com",
    exp=1234567890,
)

print(payload)