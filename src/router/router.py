"""ГОТОВЫЙ ЧИСТЫЙ ФАЙЛ — src/router/router.py

router.py — Router (MVP/L1)
Путь: src/router/router.py

Назначение:
    - Принимает UQP-запрос
    - Проверяет Policy Engine (allow/deny)
    - Проверяет Decision Engine (ALLOW/DENY)
    - Определяет провайдера по action
    - Загружает mapping из:
          PROVIDER_MAPPING_TICKET_MVP.md
          PROVIDER_MAPPING_SQL_MVP.yaml
    - Вызывает соответствующий драйвер и нормализатор
    - Возвращает UQP-ответ

Поток:
    1. action = "ticket.get"
    2. Policy Engine → allow/deny
    3. Decision Engine → ALLOW/DENY
    4. Mapping → Driver → Normalizer
    5. Ответ в UQP-формате
"""

import os
import yaml

# -----------------------------
# ДРАЙВЕРЫ
# -----------------------------
from src.drivers.ticket_driver import get_ticket, list_tickets
from src.drivers.sql_driver import fetch_record, list_records, execute_query

# -----------------------------
# НОРМАЛИЗАТОРЫ
# -----------------------------
from src.normalizer.ticket_normalizer import (
    normalize_get_ticket,
    normalize_list_tickets
)

from src.normalizer.sql_normalizer import (
    normalize_fetch_record,
    normalize_list_records,
    normalize_execute_query
)

# -----------------------------
# POLICY / DECISION
# -----------------------------
from src.policy.policy_engine import evaluate_policy
from src.decision.decision_engine import decide


# =====================================================================
# ЗАГРУЗКА МАППИНГОВ ДЛЯ ДВУХ ПРОВАЙДЕРОВ: Ticket + SQL
# =====================================================================

def load_mapping():
    """
    Читает оба файла маппинга и объединяет в единый словарь.
    Ticket mapping — из markdown, SQL mapping — из yaml.
    """
    base_path = os.getcwd()
    mapping = {}

    # ---------- Ticket Provider (MD/YAML inside MD) ----------
    ticket_map_path = os.path.join(base_path, "PROVIDER_MAPPING_TICKET_MVP.md")
    if os.path.exists(ticket_map_path):
        with open(ticket_map_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Ищем YAML-блок начиная с "ticket.get:"
        if "ticket.get:" in content:
            yaml_block = content[content.index("ticket.get:"):]
            mapping.update(yaml.safe_load(yaml_block))

    # ---------- SQL Provider (YAML) ----------
    sql_map_path = os.path.join(base_path, "PROVIDER_MAPPING_SQL_MVP.yaml")
    if os.path.exists(sql_map_path):
        with open(sql_map_path, "r", encoding="utf-8") as f:
            mapping.update(yaml.safe_load(f))

    return mapping


# Глобальный маппинг
MAPPING = load_mapping()


# =====================================================================
# ОСНОВНАЯ ФУНКЦИЯ ROUTER
# =====================================================================

def route_request(uqp_request: dict):
    """
    Главная функция маршрутизации:
        - Проверяет policy
        - Применяет decision rules
        - Вызывает корректный драйвер
        - Возвращает нормализованный ответ
    """

    action = uqp_request.get("action")
    params = uqp_request.get("params", {})

    # ----------------------
    # 1. Проверка action
    # ----------------------
    if action not in MAPPING:
        return {
            "status": "error",
            "error": {
                "code": "UNKNOWN_ACTION",
                "message": f"Action '{action}' is not registered"
            }
        }

    # ----------------------
    # 2. Policy Engine
    # ----------------------
    policy_result = evaluate_policy(action)

    # ----------------------
    # 3. Decision Engine
    # ----------------------
    decision = decide(policy_result, action)

    if decision == "DENY":
        return {
            "status": "error",
            "error": {
                "code": "POLICY_DENY",
                "message": f"Operation '{action}' was denied by policy engine"
            }
        }

    # ----------------------
    # 4. Mapping
    # ----------------------
    route = MAPPING[action]
    driver_name = route["driver"]
    driver_method = route["driver_method"]

    # =================================================================
    #                        TICKET PROVIDER
    # =================================================================
    if driver_name == "ticket":

        if driver_method == "get_ticket":
            raw = get_ticket(params.get("id"))
            return normalize_get_ticket(raw)

        if driver_method == "list_tickets":
            raw = list_tickets(params.get("project"))
            return normalize_list_tickets(raw)

    # =================================================================
    #                        SQL PROVIDER
    # =================================================================
    if driver_name == "sql":

        if driver_method == "fetch_record":
            raw = fetch_record(params.get("table"), params.get("id"))
            return normalize_fetch_record(raw)

        if driver_method == "list_records":
            raw = list_records(params.get("table"))
            return normalize_list_records(raw)

        if driver_method == "execute_query":
            raw = execute_query(params.get("sql"))
            return normalize_execute_query(raw)

    # =================================================================
    #                        FALLBACK (не должно происходить)
    # =================================================================
    return {
        "status": "error",
        "error": {
            "code": "ROUTER_INTERNAL",
            "message": "Unexpected Router state"
        }
    }