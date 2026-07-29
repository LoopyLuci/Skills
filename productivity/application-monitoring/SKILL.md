---
name: application-monitoring
description: "Prometheus metrics and Grafana dashboards for Python apps"
---

# Application Monitoring

## Prometheus Python Client
```python
from prometheus_client import Counter, Histogram, start_http_server
import time

REQUESTS = Counter("http_requests_total", "Total requests")
LATENCY = Histogram("http_request_duration_seconds", "Request latency")

def handle_request():
    REQUESTS.inc()
    with LATENCY.time():
        time.sleep(0.1)
```

## Start Metrics Endpoint
```python
start_http_server(8000)
# Metrics at http://localhost:8000/metrics
```
