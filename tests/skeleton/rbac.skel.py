"""3) RBAC-lite Skeleton

(роль-ограничение L1 — lightweight)

tests/skeleton/rbac.skel.py


rbac.skel.py — Skeleton для RBAC-Lite
Путь назначения: src/security/rbac.py

Назначение:
 - Минимальная ролевая модель L1
 - Связь между ролями и разрешёнными действиями
 - Работает поверх JWT (payload.role)

Методы:
 - has_permission(role: str, action: str) -> bool

Вход:
 - роль пользователя
 - action из UQP

Выход:
 - True/False
"""

def skeleton_info():
    pass