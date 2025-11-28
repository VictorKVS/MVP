"""2) JWT Authentication Skeleton

(базовый Security Layer L1 — упрощённый)

tests/skeleton/jwt_auth.skel.py


jwt_auth.skel.py — Skeleton для JWT Authentication
Путь назначения: src/security/jwt_auth.py

Назначение:
 - Проверка JWT-токена (верификация подписи не реализована)
 - Минимальный вариант L1 (JWT-lite)
 - Используется совместно с RBAC-lite

Методы:
 - decode_jwt(token: str) -> dict | None
 - validate_jwt(token: str) -> bool

Вход:
 - JWT-токен (строка)

Выход:
 - декодированный payload или None
 - результат валидации True/False
"""

def skeleton_info():
    pass