"""Часть 1. Создаём файлы JWT и RBAC в src/security/
📄 src/security/jwt_auth.py — JWT-lite (без проверки подписи)

jwt_auth.py — JWT Authentication (L1-lite)
Путь: src/security/jwt_auth.py

Назначение:
 - Минимальная работа с JWT токеном:
   * декодирование базовых полей
   * проверка структуры
   * извлечение роли пользователя

Важно:
 - Подпись JWT НЕ проверяется (MVP ограничение).
 - На L2 можно включить PyJWT и секрет/ключ.
"""

import base64
import json


def decode_jwt(token: str):
    """
    Мини-декодер JWT: header.payload.signature
    Возвращает payload как dict.
    """
    if not token or "." not in token:
        return None

    try:
        header_b64, payload_b64, _sig = token.split(".")

        # Добавляем недостающие '='
        padded = payload_b64 + '=' * (-len(payload_b64) % 4)

        payload_json = base64.urlsafe_b64decode(padded).decode()
        return json.loads(payload_json)
    except Exception:
        return None


def validate_jwt(token: str) -> bool:
    """
    Валидатор:
      - токен существует
      - токен имеет корректную структуру
      - payload можно декодировать
    """
    payload = decode_jwt(token)
    return payload is not None


def extract_role(token: str) -> str | None:
    """
    Извлекает поле role из payload JWT.
    """
    payload = decode_jwt(token)
    if not payload:
        return None
    return payload.get("role")