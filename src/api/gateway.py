"""src/api/gateway.py — Полная реализация Gateway (MVP/L1)

gateway.py — API Gateway (MVP/L1)
Путь: src/api/gateway.py

Назначение:
  - Основная точка входа UAG_MVP
  - Принимает UQP-запрос от агента
  - Выполняет Security Layer (API-key, sanitizing)
  - Передает управление в Router
  - Возвращает нормализованный UQP-ответ
  - Выполняет audit-логирование

Используемые модули:
  - security.apikey
  - security.sanitizer
  - router.router (главная логика маршрутизации)
  - logging.audit_log
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.security.apikey import validate_api_key
from src.security.sanitizer import sanitize_params
from src.router.router import route_request
from src.logging.audit_log import audit


app = FastAPI(title="UAG_MVP")


# ---------------------------------------------------------------------
#  API: /api/v1/query — основной вход агента
# ---------------------------------------------------------------------
@app.post("/api/v1/query")
async def query_endpoint(request: Request):

    # -----------------------------
    # 1. Принимаем JSON от агента
    # -----------------------------
    try:
        uqp_request = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "error": {"code": "INVALID_JSON", "message": "Cannot parse JSON"}}
        )

    action = uqp_request.get("action")
    params = uqp_request.get("params", {})
    context = uqp_request.get("context", {})

    # -----------------------------
    # 2. Security: API-key
    # -----------------------------
    api_key = request.headers.get("X-API-Key")

    if not validate_api_key(api_key):
        return JSONResponse(
            status_code=403,
            content={"status": "error", "error": {"code": "INVALID_API_KEY", "message": "API key rejected"}}
        )

    # -----------------------------
    # 3. Sanitizing
    # -----------------------------
    params = sanitize_params(params)
    uqp_request["params"] = params

    # -----------------------------
    # 4. Audit Log
    # -----------------------------
    audit(action, params)

    # -----------------------------
    # 5. Routing → Driver → Normalizer
    # -----------------------------
    result = route_request(uqp_request)

    # -----------------------------
    # 6. Возврат agent-facing ответа
    # -----------------------------
    return JSONResponse(status_code=200, content=result)