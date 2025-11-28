"""📄 src/api/gateway.py — теперь с JWT + RBAC

gateway.py — API Gateway (MVP/L1++)
Путь: src/api/gateway.py

Добавлены:
  - JWT Authentication (decode + validate)
  - RBAC-lite (проверка ролей)
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.observability.middleware import observability_middleware
app.middleware("http")(observability_middleware)



from src.security.apikey import validate_api_key
from src.security.sanitizer import sanitize_params
from src.security.jwt_auth import validate_jwt, extract_role
from src.security.rbac import has_permission

from src.router.router import route_request
from src.logging.audit_log import audit


app = FastAPIsrc/api/gateway.py
(title="UAG_MVP_L1")


@app.post("/api/v1/query")
async def query_endpoint(request: Request):

    # ----------------------------------------------
    # 1. JSON вход
    # ----------------------------------------------
    try:
        uqp_request = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"status": "error",
                     "error": {"code": "INVALID_JSON",
                               "message": "Cannot parse JSON"}}
        )

    action = uqp_request.get("action")
    params = uqp_request.get("params", {})
    context = uqp_request.get("context", {})

    # ----------------------------------------------
    # 2. API Key Validation (MVP)
    # ----------------------------------------------
    api_key = request.headers.get("X-API-Key")
    if not validate_api_key(api_key):
        return JSONResponse(
            status_code=403,
            content={"status": "error",
                     "error": {"code": "INVALID_API_KEY",
                               "message": "API key rejected"}}
        )

    # ----------------------------------------------
    # 3. JWT Validation (L1)
    # ----------------------------------------------
    jwt_token = request.headers.get("Authorization")
    if jwt_token and jwt_token.startswith("Bearer "):
        jwt_token = jwt_token.replace("Bearer ", "")
    else:
        return JSONResponse(
            status_code=403,
            content={"status": "error",
                     "error": {"code": "NO_JWT",
                               "message": "JWT token required"}}
        )

    if not validate_jwt(jwt_token):
        return JSONResponse(
            status_code=403,
            content={"status": "error",
                     "error": {"code": "INVALID_JWT",
                               "message": "JWT token invalid"}}
        )

    # ----------------------------------------------
    # 4. RBAC-lite проверка роли
    # ----------------------------------------------
    role = extract_role(jwt_token)
    if not has_permission(role, action):
        return JSONResponse(
            status_code=403,
            content={"status": "error",
                     "error": {"code": "RBAC_DENY",
                               "message": f"Role '{role}' is not allowed to perform '{action}'"}}
        )

    # ----------------------------------------------
    # 5. Sanitizing
    # ----------------------------------------------
    params = sanitize_params(params)
    uqp_request["params"] = params

    # ----------------------------------------------
    # 6. Audit Log
    # ----------------------------------------------
    audit(action, params)

    # ----------------------------------------------
    # 7. Routing
    # ----------------------------------------------
    result = route_request(uqp_request)

    return JSONResponse(status_code=200, content=result)