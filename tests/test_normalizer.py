"""📄 6. tests/test_normalizer.py

Проверка нормализаторов:

должны возвращать правильную структуру

статус = success

data — словарь из raw


test_normalizer.py — Тесты нормализации (MVP)
Путь: tests/test_normalizer.py

Назначение:
 - Проверка normalize_get_ticket
 - Проверка normalize_list_tickets
"""

from src.normalizer.ticket_normalizer import normalize_get_ticket, normalize_list_tickets

def test_normalize_get_ticket():
    raw = {"id": "TCK-1"}
    result = normalize_get_ticket(raw)
    assert result["status"] == "success"
    assert "data" in result
    assert result["data"] == raw

def test_normalize_list_tickets():
    raw = {"project": "PRJ"}
    result = normalize_list_tickets(raw)
    assert result["status"] == "success"
    assert "data" in result
    assert result["data"] == raw