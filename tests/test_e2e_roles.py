"""
test_e2e_roles.py — Расширенный E2E тест (L1++)
Путь: tests/test_e2e_roles.py

Проверяем:
  - API-key
  - JWT
  - RBAC roles
  - Router → Provider → Normalizer
  - Ticket provider
  - SQL provider
"""

from fastapi.testclient import TestClient
from src.api.gateway import app

client = TestClient(app)

# ----------------------------------------------------------------------
# JWT токены ролей (base64 payload, подпись заглушена)
# ----------------------------------------------------------------------
JWT_ADMIN = (
    "eyJhbGciOiJIUzI1NiJ9."
    "eyJyb2xlIjoiYWRtaW4ifQ."
    "sig"
)

JWT_EDITOR = (
    "eyJhbGciOiJIUzI1NiJ9."
    "eyJyb2xlIjoiZWRpdG9yIn0."
    "sig"
)

JWT_READER = (
    "eyJhbGciOiJIUzI1NiJ9."
    "eyJyb2xlIjoicmVhZGVyIn0."
    "sig"
)

VALID_APIKEY = "demo-key"


def make_headers(jwt):
    return {
        "X-API-Key": VALID_APIKEY,
        "Authorization": f"Bearer {jwt}"
    }


# ----------------------------------------------------------------------
# 1. ADMIN — ПОЛНЫЙ доступ (должен пройти ВСЁ)
# ----------------------------------------------------------------------
def test_admin_allows_everything():
    headers = make_headers(JWT_ADMIN)

    # A) ticket.get
    r1 = client.post(
        "/api/v1/query",
        headers=headers,
        json={"action": "ticket.get", "params": {"id": "123"}, "context": {}}
    )
    assert r1.status_code == 200
    assert r1.json()["status"] == "success"

    # B) ticket.list
    r2 = client.post(
        "/api/v1/query",
        headers=headers,
        json={"action": "ticket.list", "params": {"project": "PRJ"}, "context": {}}
    )
    assert r2.status_code == 200
    assert r2.json()["status"] == "success"

    # C) sql.query (полный доступ)
    r3 = client.post(
        "/api/v1/query",
        headers=headers,
        json={"action": "sql.query", "params": {"sql": "SELECT 1"}, "context": {}}
    )
    assert r3.status_code == 200
    assert r3.json()["status"] == "success"


# ----------------------------------------------------------------------
# 2. EDITOR — может читать Ticket + SQL, но НЕ может sql.query
# ----------------------------------------------------------------------
def test_editor_partial_permissions():
    headers = make_headers(JWT_EDITOR)

    # A) ticket.get — OK
    r1 = client.post(
        "/api/v1/query",
        headers=headers,
        json={"action": "ticket.get", "params": {"id": "1"}, "context": {}}
    )
    assert r1.status_code == 200

    # B) ticket.list — OK
    r2 = client.post(
        "/api/v1/query",
        headers=headers,
        json={"action": "ticket.list", "params": {"project": "PRJ"}, "context": {}}
    )
    assert r2.status_code == 200

    # C) sql.list — OK
    r3 = client.post(
        "/api/v1/query",
        headers=headers,
        json={"action": "sql.list", "params": {"table": "users"}, "context": {}}
    )
    assert r3.status_code == 200

    # D) sql.query — должен быть DENY через RBAC
    r4 = client.post(
        "/api/v1/query",
        headers=headers,
        json={"action": "sql.query", "params": {"sql": "DELETE FROM users"}, "context": {}}
    )
    assert r4.status_code == 403
    assert r4.json()["error"]["code"] == "RBAC_DENY"


# ----------------------------------------------------------------------
# 3. READER — может только ticket.get и sql.fetch
# ----------------------------------------------------------------------
def test_reader_minimal_permissions():
    headers = make_headers(JWT_READER)

    # A) ticket.get — OK
    r1 = client.post(
        "/api/v1/query",
        headers=headers,
        json={"action": "ticket.get", "params": {"id": "777"}, "context": {}}
    )
    assert r1.status_code == 200

    # B) sql.fetch — OK
    r2 = client.post(
        "/api/v1/query",
        headers=headers,
        json={"action": "sql.fetch", "params": {"table": "users", "id": "42"}, "context": {}}
    )
    assert r2.status_code == 200

    # C) ticket.list — DENY
    r3 = client.post(
        "/api/v1/query",
        headers=headers,
        json={"action": "ticket.list", "params": {"project": "PRJ"}, "context": {}}
    )
    assert r3.status_code == 403
    assert r3.json()["error"]["code"] == "RBAC_DENY"

    # D) sql.query — DENY
    r4 = client.post(
        "/api/v1/query",
        headers=headers,
        json={"action": "sql.query", "params": {"sql": "SELECT * FROM users"}, "context": {}}
    )
    assert r4.status_code == 403
    assert r4.json()["error"]["code"] == "RBAC_DENY"
