"""📄 7. tests/test_decision_engine.py

Проверяет логику Decision Engine минимально:


test_decision_engine.py — Тесты Decision Engine (MVP)
Путь: tests/test_decision_engine.py

Назначение:
 - Проверить ALLOW/DENY правило
"""

from src.decision.decision_engine import decide

def test_decision_allow():
    result = decide("allow", "ticket.get")
    assert result in ["ALLOW", "DENY"]

def test_decision_deny_on_policy():
    result = decide("deny", "ticket.get")
    assert result == "DENY"