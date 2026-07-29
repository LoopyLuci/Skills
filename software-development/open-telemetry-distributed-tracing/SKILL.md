---
name: open-telemetry-distributed-tracing
description: "Use when implementing OpenTelemetry for observability."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [OpenTelemetry, observability, tracing, metrics, logs, distributed-tracing]
    related_skills: [site-reliability-engineering, logging-observability-patterns, model-monitoring-drift, incident-management-on-call]
---

# OpenTelemetry and Distributed Tracing

Implementing OpenTelemetry for observability — from traces, metrics, and logs through instrumentation, sampling, collectors, and backend integration.

## When to Use

- Building comprehensive observability for distributed systems
- Implementing distributed tracing (trace across microservices)
- Unified metrics, traces, and logs with OpenTelemetry standard
- Reducing observability vendor lock-in

## OpenTelemetry Setup

```python
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Initialize tracer
provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# Instrument code
with tracer.start_as_current_span("process_order") as span:
    span.set_attribute("order.id", "12345")
    span.add_event("payment_processed", {"amount": 99.99, "currency": "USD"})
    result = process_payment()
    if result.status_code != 200:
        span.set_status(trace.Status(trace.StatusCode.ERROR))
```

## Verification Checklist

- [ ] OTLP exporter configured for traces, metrics, logs
- [ ] Auto-instrumentation for common frameworks (Flask, Django, gRPC)
- [ ] Custom spans for business-critical operations
- [ ] Sampling strategy (head-based, tail-based) configured
- [ ] Collector (otel-collector) for batching and processing
- [ ] Backend integration (Jaeger, Tempo, Grafana, Datadog)
- [ ] Trace context propagation across services (W3C TraceContext)
- [ ] Metrics (RED metrics: Rate, Errors, Duration) for each service
