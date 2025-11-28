"""📄 tests/test_sql_driver.py

test_sql_driver.py — Тесты SQL Driver (MVP/L1)
Путь: tests/test_sql_driver.py

Назначение:
 - Проверить заглушки SQL-драйвера
 - Проверить правильность структуры RAW-ответов
"""

from src.drivers.sql_driver import (
    fetch_record,
    list_records,
    execute_query
)

def test_fetch_record_returns_dict():
    result = fetch_record("users", "42")
    assert isinstance(result, dict)
    assert "table" in result
    assert "id" in result
    assert "raw_provider_response" in result


def test_list_records_returns_dict():
    result = list_records("users")
    assert isinstance(result, dict)
    assert "table" in result
    assert "raw_provider_response" in result


def test_execute_query_returns_dict():
    result = execute_query("SELECT * FROM users")
    assert isinstance(result, dict)
    assert "sql" in result
    assert "raw_provider_response" in result