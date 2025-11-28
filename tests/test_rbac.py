"""📄 tests/test_rbac.py

test_rbac.py — Модульные тесты RBAC-lite (L1)
Путь: tests/test_rbac.py

Назначение:
 - Проверить поведение ролей: reader, editor, admin
"""

from src.security.rbac import has_permission


def test_reader_permissions():
    assert has_permission("reader", "ticket.get") is True
    assert has_permission("reader", "ticket.list") is False
    assert has_permission("reader", "sql.query") is False


def test_editor_permissions():
    assert has_permission("editor", "ticket.get") is True
    assert has_permission("editor", "ticket.list") is True
    assert has_permission("editor", "sql.list") is True
    assert has_permission("editor", "sql.query") is False


def test_admin_permissions():
    assert has_permission("admin", "ticket.get") is True
    assert has_permission("admin", "sql.query") is True
    assert has_permission("admin", "unknown.action") is True