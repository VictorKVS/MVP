"""tests/test_end_to_end.py — полный E2E тест для Ticket + SQL

test_end_to_end.py — End-to-End тесты уровня L1
Путь: tests/test_end_to_end.py

Назначение:
 - Проверить полный поток:
   Агент → Gateway → Router → Driver → Normalizer → Агент
 - Проверить работу двух провайдеров:
   Ticket Provider + SQL Provider
 - Проверить соответствие UQP структурам
 - Проверить работу нормализации

Важно:
 - На этапе MVP тесты работают со skeleton-функциями,
   поэтому ожидаем "success" + заглушки.
"""

from src.api.gateway import app
from fastapi.testclient import TestClient

client = TestClient(app)


# ---------------------------------------------------------------------------
# E2E: TICKET PROVIDER
# ---------------------------------------------------------------------------

def test_e2e_ticket_get():
    """
    Проверяем:
      action='ticket.get'
      params={'id': 'TCK-1'}

    Ожидаем:
      status: success|placeholder
      наличие поля data
    """
    request_json = {
        "action": "ticket.get",
        "params": {"id": "TCK-1"},
        "context": {}
    }

    response = client.post("/api/v1/query", json=request_json)
    assert response.status_code == 200

    body = response.json()
    assert "status" in body
    assert "data" in body


def test_e2e_ticket_list():
    request_json = {
        "action": "ticket.list",
        "params": {"project": "PRJ"},
        "context": {}
    }

    response = client.post("/api/v1/query", json=request_json)
    assert response.status_code == 200

    body = response.json()
    assert "status" in body
    assert "data" in body


# ---------------------------------------------------------------------------
# E2E: SQL PROVIDER
# ---------------------------------------------------------------------------

def test_e2e_sql_fetch():
    """
    Проверяем SQL провайдер:
      action='sql.fetch'
      params={'table': 'users', 'id': '42'}
    """
    request_json = {
        "action": "sql.fetch",
        "params": {"table": "users", "id": "42"},
        "context": {}
    }

    response = client.post("/api/v1/query", json=request_json)
    assert response.status_code == 200

    body = response.json()
    assert "status" in body
    assert "data" in body


def test_e2e_sql_list():
    request_json = {
        "action": "sql.list",
        "params": {"table": "users"},
        "context": {}
    }

    response = client.post("/api/v1/query", json=request_json)
    assert response.status_code == 200

    body = response.json()
    assert "status" in body
    assert "data" in body


def test_e2e_sql_query_raw():
    """
    Мини-пример SQL-запроса (скелет):
      action='sql.query'
      params={'sql': 'SELECT * FROM users'}
    """
    request_json = {
        "action": "sql.query",
        "params": {"sql": "SELECT * FROM users"},
        "context": {}
    }

    response = client.post("/api/v1/query", json=request_json)
    assert response.status_code == 200

    body = response.json()
    assert "status" in body
    assert "data" in body