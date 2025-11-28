"""
metrics.py — Prometheus Metrics (L2)
Путь: src/observability/metrics.py
"""

from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "uag_requests_total",
    "Total UAG requests",
    ["action", "role"]
)

ERROR_COUNT = Counter(
    "uag_errors_total",
    "Total UAG errors",
    ["action", "error_code"]
)

REQUEST_LATENCY = Histogram(
    "uag_request_duration_seconds",
    "Request processing duration",
    ["action"]
)
