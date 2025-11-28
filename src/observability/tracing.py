"""
tracing.py — Request Tracing (L2)
Путь: src/observability/tracing.py

Назначение:
  - Генерация request_id
  - Прокидывание request_id через Gateway → Router
"""

from src.observability.logger import generate_request_id

def inject_request_id(uqp_request: dict) -> str:
    req_id = generate_request_id()
    uqp_request["request_id"] = req_id
    return req_id
