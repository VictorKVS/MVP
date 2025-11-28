"""📄 1. tests/test_uqp.py

Мини-тесты на структуру UQP протокола (строго согласно UQP_PROTOCOL_MVP.md)


test_uqp.py — Тесты протокола UQP (MVP)
Путь: tests/test_uqp.py

Назначение:
 - Проверить минимальные требования к UQP запросу и ответу
 - Проверить обязательные поля action, params, context
 - Проверить формат ответа и ошибки
"""

import pytest

def test_uqp_request_structure():
    request = {
        "action": "ticket.get",
        "params": {"id": "TCK-1"},
        "context": {}
    }

    assert "action" in request
    assert "params" in request
    assert "context" in request
    assert isinstance(request["params"], dict)
    assert isinstance(request["context"], dict)


def test_uqp_response_success_format():
    response = {
        "status": "success",
        "data": {"id": "TCK-1"}
    }

    assert response["status"] == "success"
    assert "data" in response


def test_uqp_error_format():
    error = {
        "status": "error",
        "error": {"code": "POLICY_DENY", "message": "Operation is not allowed"}
    }

    assert error["status"] == "error"
    assert "error" in error
    assert "code" in error["error"]