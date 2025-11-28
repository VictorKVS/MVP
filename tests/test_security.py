"""📄 5. tests/test_security.py

Проверяем:

API-key validator возвращает bool

sanitizing возвращает dict

sanitizing не модифицирует данные (в MVP-заглушке)


test_security.py — Тесты безопасности (MVP)
Путь: tests/test_security.py

Назначение:
 - Проверить API-key validator
 - Проверить sanitizing входных параметров
"""

from src.security.apikey import validate_api_key
from src.security.sanitizer import sanitize_params

def test_api_key_validator_returns_bool():
    assert isinstance(validate_api_key("demo"), bool)

def test_sanitizer_returns_dict():
    params = {"id": "TCK-1"}
    sanitized = sanitize_params(params)
    assert isinstance(sanitized, dict)

def test_sanitizer_preserves_keys():
    params = {"id": "TCK-1", "project": "PRJ"}
    sanitized = sanitize_params(params)
    assert sanitized.keys() == params.keys()