"""
logger.py — JSON Logger (L2)
Путь: src/observability/logger.py

Назначение:
  - Структурированные JSON-логи для трассировки
  - Обязательный элемент L2 зрелости
"""

import json
import time
import uuid


def generate_request_id() -> str:
    return str(uuid.uuid4())


def log_event(event_type: str, data: dict):
    """
    event_type: request_start, request_end, error, audit
    """
    log_record = {
        "timestamp": time.time(),
        "event": event_type,
        **data
    }
    print(json.dumps(log_record, ensure_ascii=False))
