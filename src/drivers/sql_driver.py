"""src/drivers/sql_driver.py — SKELETON CODE (L1)

sql_driver.py — SQL Provider Driver (MVP/L1)
Путь: src/drivers/sql_driver.py

Назначение:
  SQL-драйвер является вторым провайдером уровня L1.
  Его задача — эмулировать поведение SQL-сервера в MVP:
    - получение записи
    - получение списка записей
    - выполнение SQL-запроса

Этот драйвер НЕ работает с реальной БД.
Он возвращает RAW-ответы, которые будут затем обработаны Normalizer'ом.

Используется:
  - Router (определяет driver_method)
  - Normalizer (приводит RAW → UQP формат)
  - End-to-End тесты (test_end_to_end.py)

Методы (заглушки):
  - fetch_record(table: str, id: str) -> dict
  - list_records(table: str) -> dict
  - execute_query(sql: str) -> dict

Вход:
  параметры из UQP:
    {
      "action": "sql.fetch",
      "params": {"table": "users", "id": "42"}
    }

Выход:
  RAW-ответ:
    {
      "raw_provider_response": "stub",
      "table": "...",
      "id": "...",
      ...
    }
"""

def fetch_record(table: str, record_id: str) -> dict:
    """
    Заглушка для получения записи по ID.
    """
    return {
        "raw_provider_response": "fetch_record not implemented",
        "table": table,
        "id": record_id
    }


def list_records(table: str) -> dict:
    """
    Заглушка для получения списка записей.
    """
    return {
        "raw_provider_response": "list_records not implemented",
        "table": table
    }


def execute_query(sql: str) -> dict:
    """
    Заглушка для выполнения SQL-запроса.
    """
    return {
        "raw_provider_response": "execute_query not implemented",
        "sql": sql
    }
