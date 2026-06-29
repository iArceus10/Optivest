from fastapi import status


def register_user(client):
    """
    Register a test user and return the registration payload.
    """

    payload = {
        "email": "portfolio@example.com",
        "full_name": "Portfolio User",
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
    Authenticate a user and return a JWT access token.
    """

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": payload["email"],
            "password": payload["password"],
        },
    )

    assert response.status_code == status.HTTP_200_OK

    return response.json()["access_token"]


def auth_headers(token: str) -> dict[str, str]:
    """
    Return Authorization headers.
    """

    return {
        "Authorization": f"Bearer {token}",
    }


def create_portfolio(client, headers):
    """
    Create a sample portfolio.
    """

    payload = {
        "name": "Long Term Portfolio",
        "description": "My investments",
    }

    response = client.post(
        "/api/v1/portfolios",
        json=payload,
        headers=headers,
    )

    assert response.status_code == status.HTTP_201_CREATED

    return response.json()


def test_create_portfolio(client):
    payload = register_user(client)
    token = login_user(client, payload)

    response = client.post(
        "/api/v1/portfolios",
        json={
            "name": "Growth Portfolio",
            "description": "Technology holdings",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == status.HTTP_201_CREATED

    body = response.json()

    assert body["name"] == "Growth Portfolio"
    assert body["description"] == "Technology holdings"


def test_list_portfolios(client):
    payload = register_user(client)
    token = login_user(client, payload)

    create_portfolio(
        client,
        auth_headers(token),
    )

    response = client.get(
        "/api/v1/portfolios",
        headers=auth_headers(token),
    )

    assert response.status_code == status.HTTP_200_OK

    portfolios = response.json()

    assert len(portfolios) == 1
    assert portfolios[0]["name"] == "Long Term Portfolio"


def test_get_portfolio(client):
    payload = register_user(client)
    token = login_user(client, payload)

    portfolio = create_portfolio(
        client,
        auth_headers(token),
    )

    response = client.get(
        f"/api/v1/portfolios/{portfolio['id']}",
        headers=auth_headers(token),
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["id"] == portfolio["id"]


def test_update_portfolio(client):
    payload = register_user(client)
    token = login_user(client, payload)

    portfolio = create_portfolio(
        client,
        auth_headers(token),
    )

    response = client.patch(
        f"/api/v1/portfolios/{portfolio['id']}",
        json={
            "name": "Updated Portfolio",
        },
        headers=auth_headers(token),
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["name"] == "Updated Portfolio"
    assert body["description"] == "My investments"


def test_delete_portfolio(client):
    payload = register_user(client)
    token = login_user(client, payload)

    portfolio = create_portfolio(
        client,
        auth_headers(token),
    )

    response = client.delete(
        f"/api/v1/portfolios/{portfolio['id']}",
        headers=auth_headers(token),
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get(
        f"/api/v1/portfolios/{portfolio['id']}",
        headers=auth_headers(token),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_missing_portfolio(client):
    payload = register_user(client)
    token = login_user(client, payload)

    response = client.get(
        "/api/v1/portfolios/00000000-0000-0000-0000-000000000000",
        headers=auth_headers(token),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_cannot_access_another_users_portfolio(client):
    """
    A user must not be able to access another user's portfolio.
    The API should return 404 instead of 403 to avoid leaking
    the existence of resources owned by other users.
    """

    # ----------------------------
    # User A
    # ----------------------------

    user_a = {
        "email": "alice@example.com",
        "full_name": "Alice",
        "password": "SecurePassword123!",
    }

    response = client.post(
        "/api/v1/auth/register",
        json=user_a,
    )

    assert response.status_code == status.HTTP_201_CREATED

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": user_a["email"],
            "password": user_a["password"],
        },
    )

    token_a = response.json()["access_token"]

    response = client.post(
        "/api/v1/portfolios",
        json={
            "name": "Alice Portfolio",
            "description": "Private portfolio",
        },
        headers=auth_headers(token_a),
    )

    assert response.status_code == status.HTTP_201_CREATED

    portfolio_id = response.json()["id"]

    # ----------------------------
    # User B
    # ----------------------------

    user_b = {
        "email": "bob@example.com",
        "full_name": "Bob",
        "password": "SecurePassword123!",
    }

    response = client.post(
        "/api/v1/auth/register",
        json=user_b,
    )

    assert response.status_code == status.HTTP_201_CREATED

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": user_b["email"],
            "password": user_b["password"],
        },
    )

    token_b = response.json()["access_token"]

    # ----------------------------
    # Bob tries to access Alice's portfolio
    # ----------------------------

    response = client.get(
        f"/api/v1/portfolios/{portfolio_id}",
        headers=auth_headers(token_b),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Portfolio not found."