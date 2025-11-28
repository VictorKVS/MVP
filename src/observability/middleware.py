"""
middleware.py — Observability middleware (L2)
Путь: src/observability/middleware.py

Назначение:
  - Измерение latency
  - Инкремент Prometheus метрик
  - request_id + логирование
"""

import time

from src.observability.tracing import inject_request_id
from src.observability.logger import log_event
from src.observability.metrics import REQUEST_COUNT, REQUEST_LATENCY, ERROR_COUNT


async def observability_middleware(request, call_next):
    start_time = time.time()

    # Создаём request_id
    body = await request.json()
    req_id = inject_request_id(body)

    action = body.get("action", "unknown")
    role = "unknown"

    log_event("request_start", {"action": action, "request_id": req_id})

    try:
        response = await call_next(request)
    except Exception as ex:
        ERROR_COUNT.labels(action=action, error_code="EXCEPTION").inc()
        log_event("error", {"request_id": req_id, "exception": str(ex)})
        raise

    latency = time.time() - start_time

    REQUEST_COUNT.labels(action=action, role=role).inc()
    REQUEST_LATENCY.labels(action=action).observe(latency)

    log_event("request_end", {
        "request_id": req_id,
        "action": action,
        "latency_ms": round(latency * 1000, 2)
    })

    return response
