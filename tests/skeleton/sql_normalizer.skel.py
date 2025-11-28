"""4A. Создаём skeleton файл в tests/skeleton/sql_normalizer.skel.py

sql_normalizer.skel.py — Skeleton Normalizer для SQL Provider
Путь назначения: src/normalizer/sql_normalizer.py
Хранение skeleton: tests/skeleton/sql_normalizer.skel.py

Назначение:
  - Приводит RAW-ответы SQL-драйвера к UQP-ответу.
  - Используется в Router/End-to-End потоке.
  - Унифицирует структуру ответа:
      { "status": "success", "data": {...} }

Методы (заглушки):
  - normalize_fetch_record(raw: dict) -> dict
  - normalize_list_records(raw: dict) -> dict
  - normalize_execute_query(raw: dict) -> dict

Вход:
  raw dict от sql_driver

Выход:
  нормализованный dict
"""

def skeleton_info():
    pass