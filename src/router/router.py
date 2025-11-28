 """src/router/router.py — полная версия Router L1 (MVP)

router.py — Router (MVP/L1)
Путь: src/router/router.py

Назначение:
    - Принимает UQP-запрос
    - Определяет провайдера по action
    - Загружает mapping из файлов:
        PROVIDER_MAPPING_TICKET_MVP.md
        PROVIDER_MAPPING_SQL_MVP.yaml
    - Вызывает соответствующий драйвер и метод
    - Передаёт результат в нормализатор

Поток:
    1. action = "ticket.get"
    2. Найти driver и driver_method в маппинге
    3. Вызвать драйвер
    4. Вызвать нормализатор
    5. Вернуть UQP-ответ

Модули:
    - Ticket Driver
    - SQL Driver
    - Ticket Normalizer
    - SQL Normalizer
"""

import yaml
import os

# Драйверы
from src.drivers.ticket_driver import get_ticket, list_tickets
from src.drivers.sql_driver import fetch_record, list_records, execute_query

# Нормализаторы
from src.normalizer.ticket_normalizer import (
    normalize_get_ticket,
    normalize_list_tickets
)

from src.normalizer.sql_normalizer import (
    normalize_fetch_record,
    normalize_list_records,
    normalize_execute_query
)


# --------------------------------------------------------------------
#  Загружаем два маппинга: Ticket + SQL
# --------------------------------------------------------------------

def load_mapping():
    base_path = os.getcwd()

    ticket_map_path = os.path.join(base_path, "PROVIDER_MAPPING_TICKET_MVP.md")
    sql_map_path = os.path.join(base_path, "PROVIDER_MAPPING_SQL_MVP.yaml")

    mapping = {}

    # Ticket mapping (из md — читаем как YAML секцию)
    # Берём только YAML-часть файла
    if os.path.exists(ticket_map_path):
        with open(ticket_map_path, "r", encoding="utf-8") as f:
            text = f.read()

        # Выделяем YAML-блок
        if "ticket.get:" in text:
            yaml_part = text[text.index("ticket.get:"):]
            mapping.update(yaml.safe_load(yaml_part))

    # SQL mapping
    if os.path.exists(sql_map_path):
        with open(sql_map_path, "r", encoding="utf-8") as f:
            mapping.update(yaml.safe_load(f))

    return mapping


MAPPING = load_mapping()


# --------------------------------------------------------------------
#  Основной Router
# --------------------------------------------------------------------

def route_request(uqp_request: dict):
    """
    Основная функция:
        принимает action + params
        выбирает провайдера
        вызывает драйвер
        вызывает нормализатор
    """
    action = uqp_request.get("action")
    params = uqp_request.get("params", {})

    if action not in MAPPING:
        return {
            "status": "error",
            "error": {
                "code": "UNKNOWN_ACTION",
                "message": f"Action '{action}' not registered"
            }
        }

    route = MAPPING[action]
    driver_name = route["driver"]
    driver_method = route["driver_method"]

    # --------------------------------------------------------
    # 1. Ticket Provider
    # --------------------------------------------------------
    if driver_name == "ticket":
        if driver_method == "get_ticket":
            raw = get_ticket(params.get("id"))
            return normalize_get_ticket(raw)

        if driver_method == "list_tickets":
            raw = list_tickets(params.get("project"))
            return normalize_list_tickets(raw)

    # --------------------------------------------------------
    # 2. SQL Provider
    # --------------------------------------------------------
    if driver_name == "sql":
        if driver_method == "fetch_record":
            raw = fetch_record(
                params.get("table"),
                params.get("id")
            )
            return normalize_fetch_record(raw)

        if driver_method == "list_records":
            raw = list_records(params.get("table"))
            return normalize_list_records(raw)

        if driver_method == "execute_query":
            raw = execute_query(params.get("sql"))
            return normalize_execute_query(raw)

    # --------------------------------------------------------

    return {
        "status": "error",
        "error": {
            "code": "ROUTER_INTERNAL",
            "message": "Unexpected router state"
        }
    }