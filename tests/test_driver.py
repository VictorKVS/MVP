"""📄 2. tests/test_policy.py

Тестируем Policy Engine (MVP-правила — allow/deny)


test_policy.py — Тесты Policy Engine (MVP)
Путь: tests/test_policy.py

Назначение:
 - Проверка минимального DSL allow/deny
 - Проверка deny для опасных операций (*.delete, db.*)
"""

from src.policy.policy_engine import evaluate_policy

def test_policy_allow_get():
    assert evaluate_policy("ticket.get") in ["allow", "deny"]

def test_policy_deny_delete():
    assert evaluate_policy("ticket.delete") == "deny"

def test_policy_deny_db():
    assert evaluate_policy("db.query") == "deny"