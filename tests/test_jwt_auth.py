"""📄 tests/test_jwt_auth.py

test_jwt_auth.py — Модульные тесты JWT (L1)
Путь: tests/test_jwt_auth.py

Назначение:
 - Проверить decode_jwt()
 - Проверить validate_jwt()
 - Проверить extract_role()
"""

from src.security.jwt_auth import decode_jwt, validate_jwt, extract_role


# JWT без подписи (payload: {"role": "admin"})
VALID_JWT = (
    "eyJhbGciOiJIUzI1NiJ9."
    "eyJyb2xlIjogImFkbWluIn0."
    "signature_stub"
)

INVALID_JWT = "invalid.token.structure"


def test_decode_jwt_valid():
    payload = decode_jwt(VALID_JWT)
    assert isinstance(payload, dict)
    assert payload.get("role") == "admin"


def test_decode_jwt_invalid():
    payload = decode_jwt(INVALID_JWT)
    assert payload is None


def test_validate_jwt_valid():
    assert validate_jwt(VALID_JWT) is True


def test_validate_jwt_invalid():
    assert validate_jwt(INVALID_JWT) is False


def test_extract_role():
    assert extract_role(VALID_JWT) == "admin"