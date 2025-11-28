"""📄 3. tests/test_router.py

Тестируем Router: должен вернуть placeholder пока нет реализации

test_router.py — Тесты Router (MVP)
Путь: tests/test_router.py

Назначение:
 - Проверить, что router принимает action и params
 - Проверить, что пока возвращает placeholder-ответ
"""

from src.router.router import route_request

def test_router_accepts_request():
    request = {
        "action": "ticket.get",
        "params": {"id": "TCK-1"}
    }

    response = route_request(request)
    assert "status" in response
    assert "data" in response


def test_router_placeholder_status():
    response = route_request({"action": "ticket.get", "params": {}})
    assert response["status"] == "placeholder"