"""📄 tests/test_security_integration.py — Полный интеграционный тест

test_security_integration.py — Интеграционный тест Security Layer (L1+)
Путь: tests/test_security_integration.py

Назначение:
 - Проверить всю цепочку безопасности:
     API-key → JWT → RBAC → Router → Normalizer → Response
 - Проверить запреты и разрешения для разных ролей
 - Проверить корректность структуры ответа
"""

from fastapi.testclient import TestClient
from src.api.gateway import app

client = TestClient(app)

# JWT токены (payload в base64)
JWT_ADMIN = (
    "eyJhbGciOiJIUzI1NiJ9."
    "eyJyb2xlIjoiYWRtaW4ifQ."
    "signature"
)

JWT_EDITOR = (
    "eyJhbGciOiJIUzI1NiJ9."
    "eyJyb2xlIjoiZWRpdG9yIn0."
    "signature"
)

JWT_READER = (
    "eyJhbGciOiJIUzI1NiJ9."
    "eyJyb2xlIjoicmVhZGVyIn0."
    "signature"
)

VALID_HEADERS = {
    "X-API-Key": "demo-key",
    "Authorization": f"Bearer {JWT_ADMIN}"
}


# ----------------------------------------------------------------------
# 1. Проверяем отсутствие JWT
# ----------------------------------------------------------------------
def test_no_jwt_rejected():
    response = client.post(
        "/api/v1/query",
        headers={"X-API-Key": "demo-key"},
        json={"action": "ticket.get", "params": {"id": "1"}, "context": {}},
    )
    assert response.status_code == 403
    body = response.json()
    assert body["error"]["code"] == "NO_JWT"


# ----------------------------------------------------------------------
# 2. Проверяем неверный JWT
# ----------------------------------------------------------------------
def test_invalid_jwt_rejected():
    response = client.post(
        "/api/v1/query",
        headers={
            "X-API-Key": "demo-key",
            "Authorization": "Bearer invalid.token"
        },
        json={"action": "ticket.get", "params": {"id": "1"}, "context": {}},
    )
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "INVALID_JWT"


# ----------------------------------------------------------------------
# 3. Проверяем RBAC: reader не может делать ticket.list
# ----------------------------------------------------------------------
def test_rbac_reader_denied_ticket_list():
    headers = {
        "X-API-Key": "demo-key",
        "Authorization": f"Bearer {JWT_READER}"
    }

    response = client.post(
        "/api/v1/query",
        headers=headers,
        json={"action": "ticket.list", "params": {"project": "PRJ"}, "context": {}},
    )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "RBAC_DENY"


# ----------------------------------------------------------------------
# 4. Проверяем RBAC: editor может ticket.list
# ----------------------------------------------------------------------
def test_rbac_editor_allows_ticket_list():
    headers = {
        "X-API-Key": "demo-key",
        "Authorization": f"Bearer {JWT_EDITOR}"
    }

    response = client.post(
        "/api/v1/query",
        headers=headers,
        json={"action": "ticket.list", "params": {"project": "PRJ"}, "context": {}},
    )

    assert response.status_code == 200
    assert "data" in response.json()


# ----------------------------------------------------------------------
# 5. Проверяем RBAC: admin может делать sql.query
# ----------------------------------------------------------------------
def test_rbac_admin_allows_sql_query():
    headers = {
        "X-API-Key": "demo-key",
        "Authorization": f"Bearer {JWT_ADMIN}"
    }

    response = client.post(
        "/api/v1/query",
        headers=headers,
        json={"action": "sql.query", "params": {"sql": "SELECT 1"}, "context": {}},
    )

    assert response.status_code == 200
    assert "data" in response.json()


# ----------------------------------------------------------------------
# 6. Проверяем API-key: отсутствие API-Key → отказ
# ----------------------------------------------------------------------
def test_no_apikey_rejected():
    response = client.post(
        "/api/v1/query",
        json={"action": "ticket.get", "params": {"id": "1"}, "context": {}},
    )
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "INVALID_API_KEY"