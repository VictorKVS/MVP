# 1) tests/skeleton/api_gateway.skel.py
"""
1) tests/skeleton/api_gateway.skel.py

api_gateway.skel.py — Skeleton для src/api/gateway.py
Путь назначения: src/api/gateway.py

Назначение:
  - Точка входа UAG_MVP
  - Принимает HTTP запросы
  - Принмает UQP JSON от агента
  - Передает в Router
  - Возвращает нормализованный ответ

Вход:
  - HTTP POST /api/v1/query
  - JSON: { action, params, context }

Выход:
  - JSON: { status, data | error }
"""

def skeleton_info():
    pass