
"""SQL Driver Skeleton

(второй драйвер для L1 — демонстрация multi-provider)

tests/skeleton/sql_driver.skel.py

sql_driver.skel.py — Skeleton для SQL Driver (провайдер #2)
Путь назначения: src/drivers/sql_driver.py

Назначение:
 - Демонстрационный драйвер, эмулирующий доступ к SQL-базе.
 - Используется для L1 как второй провайдер.
 - Логика не реализована — только структура.

Методы:
 - execute_query(sql: str) — выполнить SQL-запрос
 - fetch_record(table: str, id: str) — получить запись
 - list_records(table: str) — список записей

Вход:
 - текст SQL или параметры выборки

Выход:
 - raw результат, который будет нормализован
"""

def skeleton_info():
    pass