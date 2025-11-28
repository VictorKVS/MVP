
"""tests/skeleton/sql_driver.skel.py

(полная версия)

sql_driver.skel.py — Skeleton SQL Driver (L1)

Путь назначения: src/drivers/sql_driver.py
Каталог хранения skeleton: tests/skeleton/sql_driver.skel.py

Назначение:
  SQL Driver — второй провайдер уровня L1.
  Используется для демонстрации multi-provider маршрутизации:
    Ticket Provider + SQL Provider.

Функциональные обязанности:
  - обработка действий:
      sql.fetch
      sql.list
      sql.query
  - возвращает RAW-ответ, который позже будет нормализован.

Методы (будущая реализация):
  - fetch_record(table: str, id: str)
  - list_records(table: str)
  - execute_query(sql: str)

Вход:
  - параметры params из UQP (table, id, sql)

Выход:
  - raw provider response в формате dict
"""

def skeleton_info():
    """Заглушка — файл skeleton."""
    pass