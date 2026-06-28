from jose import JWTError

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_password_creates_different_hash():
    """
    Password hashes should not equal the original password.
    """

    password = "SecurePassword123!"

    hashed_password = hash_password(password)

    assert hashed_password != password


def test_verify_password_success():
    """
    A correct password should verify successfully.
    """

    password = "SecurePassword123!"

    hashed_password = hash_password(password)

    assert verify_password(
        password,
        hashed_password,
    )


def test_verify_password_failure():
    """
    An incorrect password should fail verification.
    """

    hashed_password = hash_password("SecurePassword123!")

    assert not verify_password(
        "WrongPassword",
        hashed_password,
    )


def test_create_and_decode_access_token():
    """
    A generated JWT should decode successfully.
    """

    subject = "123e4567-e89b-12d3-a456-426614174000"

    token = create_access_token(subject=subject)

    payload = decode_access_token(token)

    assert payload["sub"] == subject
    assert "exp" in payload


def test_decode_invalid_token():
    """
    Decoding an invalid JWT should raise JWTError.
    """

    invalid_token = "this.is.not.a.valid.jwt"

    try:
        decode_access_token(invalid_token)
        assert False, "JWTError was expected."

    except JWTError:
        assert True