"""4B. Создаём реальный файл SQL Normalizer: src/normalizer/sql_normalizer.py

sql_normalizer.py — Normalizer для SQL Provider (MVP/L1)
Путь: src/normalizer/sql_normalizer.py

Назначение:
  Приведение RAW ответа SQL-драйвера к формату UQP Response:
    {
      "status": "success",
      "data": {...}
    }

Используется в:
  - Router (после вызова sql_driver)
  - Тестах E2E (test_end_to_end.py)
  - L1 демо с двумя провайдерами

Методы:
  - normalize_fetch_record(raw)
  - normalize_list_records(raw)
  - normalize_execute_query(raw)

Вход:
  raw dict от sql_driver

Выход:
  нормализованный dict для UQP
"""

def normalize_fetch_record(raw: dict) -> dict:
    """
    Нормализация fetch_record.
    """
    return {
        "status": "success",
        "data": raw
    }


def normalize_list_records(raw: dict) -> dict:
    """
    Нормализация list_records.
    """
    return {
        "status": "success",
        "data": raw
    }


def normalize_execute_query(raw: dict) -> dict:
    """
    Нормализация execute_query.
    """
    return {
        "status": "success",
        "data": raw
    }