"""src/security/rbac.py — RBAC-lite

rbac.py — RBAC-lite (L1)
Путь: src/security/rbac.py

Назначение:
  - Минимальная ролевая модель.
  - Определяет, имеет ли роль разрешение выполнить action.

Роли уровня L1:
  - "reader" — может выполнять только GET/READ
  - "editor" — может выполнять list и fetch
  - "admin" — может выполнять любые действия кроме явно запрещённых Policy
"""

# Простейшая таблица разрешений
ROLE_MATRIX = {
    "reader": [
        "ticket.get",
        "sql.fetch"
    ],
    "editor": [
        "ticket.get",
        "ticket.list",
        "sql.fetch",
        "sql.list"
    ],
    "admin": ["*"]  # Полный доступ (кроме deny в Policy)
}


def has_permission(role: str, action: str) -> bool:
    if role not in ROLE_MATRIX:
        return False

    rules = ROLE_MATRIX[role]

    if "*" in rules:
        return True

    return action in rules