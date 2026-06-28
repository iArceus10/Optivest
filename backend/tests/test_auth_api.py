from fastapi import status


def register_user(client):
    """
    Register a test user and return the request payload.
    """

    payload = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "SecurePassword123!",
    }

    response = client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert response.status_code == status.HTTP_201_CREATED

    return payload


def login_user(client, payload):
    """
    Log in the registered user and return the JWT.
    """

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": payload["email"],
            "password": payload["password"],
        },
    )

    assert response.status_code == status.HTTP_200_OK

    token = response.json()["access_token"]

    return token


def test_register_user(client):
    payload = register_user(client)

    response = client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Email is already registered."


def test_login_success(client):
    payload = register_user(client)

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": payload["email"],
            "password": payload["password"],
        },
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_invalid_password(client):
    payload = register_user(client)

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": payload["email"],
            "password": "WrongPassword",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid email or password."


def test_get_current_user(client):
    payload = register_user(client)

    token = login_user(client, payload)

    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["email"] == payload["email"]
    assert body["full_name"] == payload["full_name"]


def test_get_current_user_without_token(client):
    response = client.get(
        "/api/v1/auth/me",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user_invalid_token(client):
    response = client.get(
        "/api/v1/auth/me",
        headers={
            "Authorization": "Bearer invalid_token",
        },
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED