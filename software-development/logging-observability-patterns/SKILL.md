---
name: logging-observability-patterns
description: "Use when implementing structured logging and observability."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [logging, observability, structured-logging, telemetry, monitoring]
    related_skills: [debugging-techniques-advanced, performance-optimization, distributed-systems-patterns, service-mesh-patterns]
---

# Logging and Observability Patterns

Implementing structured logging, distributed tracing, metrics collection, and observability for modern applications.

## When to Use

- Designing a logging strategy for a new application
- Replacing ad-hoc print statements with structured logging
- Implementing distributed tracing across microservices
- Setting up metrics collection for monitoring
- Debugging production issues with insufficient observability

## Three Pillars of Observability

```
Logs — structured events with context
Metrics — numeric aggregations over time
Traces — end-to-end request flow across services
```

## Structured Logging

### Python (structlog)

```python
import structlog
import logging
from datetime import datetime

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
)

logger = structlog.get_logger()

# Usage — all context is structured
logger.info("user_login", user_id=42, ip="192.168.1.1", attempt=1)

# Bind context that persists across calls
log = logger.bind(request_id="req_abc123", service="auth")
log.warning("rate_limit_reached", user_id=42, limit=100)
log.info("request_completed", duration_ms=234)
```

### Rust (tracing)

```rust
use tracing::{info, warn, error, instrument};
use tracing_subscriber;

// Setup
fn main() {
    tracing_subscriber::fmt()
        .json()
        .with_target(true)
        .with_thread_ids(true)
        .init();
    
    // Structured fields
    info!(user_id = 42, action = "login", "User logged in");
}

// Automatic function tracing
#[instrument]
fn process_order(order_id: u64, items: Vec<Item>) -> Result<Order> {
    info!("Processing order");
    // ... function body
    // Fields automatically captured from parameters
}
```

## Log Levels Strategy

```python
class LogLevelPolicy:
    """When to use each log level in production."""
    
    @staticmethod
    def guidelines():
        return """
        ERROR:    Something is definitely wrong (investigate now)
                 - Database connection failures
                 - Unhandled exceptions
                 - Business logic violations that need human review
        
        WARN:     Something unexpected but handled
                 - Retry attempts
                 - Rate limiting triggered
                 - Deprecated API usage
                 - Slow queries (> threshold)
        
        INFO:     Normal operations (useful for understanding flow)
                 - User signups, logins
                 - Order placements
                 - Configuration changes
                 - Batch job start/end
        
        DEBUG:    Detailed diagnostic info (usually off in prod)
                 - Function entry/exit
                 - Query parameters
                 - State transitions
        
        TRACE:   Very detailed (enable briefly for specific debugging)
                 - Hot-path variable values
                 - Loop iterations
        """
```

## Distributed Tracing

```python
import uuid
import time
from contextvars import ContextVar

# Context variable to propagate trace context
trace_ctx = ContextVar('trace_context', default=None)

class TraceContext:
    """Propagate trace and span IDs across async boundaries."""
    
    def __init__(self, trace_id=None, parent_span_id=None):
        self.trace_id = trace_id or str(uuid.uuid4())
        self.span_id = str(uuid.uuid4())
        self.parent_span_id = parent_span_id
        self.start_time = time.time()
    
    def to_headers(self):
        return {
            'X-Trace-Id': self.trace_id,
            'X-Span-Id': self.span_id,
        }
    
    @classmethod
    def from_headers(cls, headers):
        return cls(
            trace_id=headers.get('X-Trace-Id'),
            parent_span_id=headers.get('X-Span-Id'),
        )


class Tracer:
    """Manual instrumentation for distributed tracing."""
    
    @staticmethod
    def span(name, tags=None):
        """Context manager for a tracing span."""
        class SpanContext:
            def __enter__(self):
                parent = trace_ctx.get()
                ctx = TraceContext(
                    trace_id=parent.trace_id if parent else None,
                    parent_span_id=parent.span_id if parent else None,
                )
                self.token = trace_ctx.set(ctx)
                logger.info(f"span_start", name=name, span_id=ctx.span_id,
                           trace_id=ctx.trace_id, tags=tags)
                return ctx
            
            def __exit__(self, *args):
                trace_ctx.reset(self.token)
                elapsed = time.time() - trace_ctx.get().start_time
                logger.info(f"span_end", name=name, duration_ms=round(elapsed*1000, 2))
        
        return SpanContext()

# Usage
# with Tracer.span("process_order", tags={"order_id": 42}):
#     with Tracer.span("validate_payment"):
#         ...
```

## Metrics Collection

```python
import time
from collections import defaultdict
from threading import Lock
import statistics

class MetricsRegistry:
    """Simple in-process metrics registry (prometheus-style)."""
    
    def __init__(self):
        self.counters = defaultdict(int)
        self.gauges = {}
        self.histograms = defaultdict(list)
        self.lock = Lock()
    
    def counter(self, name: str, tags: dict = None) -> None:
        """Increment a counter."""
        key = self._key(name, tags)
        with self.lock:
            self.counters[key] += 1
    
    def gauge(self, name: str, value: float, tags: dict = None) -> None:
        """Set a gauge value."""
        key = self._key(name, tags)
        with self.lock:
            self.gauges[key] = value
    
    def histogram(self, name: str, value: float, tags: dict = None) -> None:
        """Record a histogram observation."""
        key = self._key(name, tags)
        with self.lock:
            self.histograms[key].append(value)
    
    def _key(self, name, tags):
        if tags:
            tag_str = ','.join(f'{k}={v}' for k, v in sorted(tags.items()))
            return f"{name}{{{tag_str}}}"
        return name
    
    def snapshot(self) -> dict:
        """Return current values and reset histograms."""
        with self.lock:
            data = {
                'counters': dict(self.counters),
                'gauges': dict(self.gauges),
                'histograms': {},
            }
            for k, values in self.histograms.items():
                if values:
                    data['histograms'][k] = {
                        'count': len(values),
                        'sum': sum(values),
                        'avg': statistics.mean(values),
                        'p50': sorted(values)[len(values)//2],
                        'p99': sorted(values)[int(len(values)*0.99)],
                    }
            self.histograms.clear()
            return data


# Metric decorator
def timed(metric_name: str = None):
    """Decorator that records execution time as a metric."""
    def decorator(fn):
        name = metric_name or fn.__name__
        registry = MetricsRegistry()
        
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = fn(*args, **kwargs)
                registry.histogram(f"{name}_duration_ms", 
                                  (time.time() - start) * 1000)
                registry.counter(f"{name}_success")
                return result
            except Exception:
                registry.counter(f"{name}_error")
                raise
        
        return wrapper
    return decorator
```

## Observability Integration

```python
class ObservabilityMiddleware:
    """Middleware that combines logs, traces, and metrics."""
    
    def __call__(self, request):
        trace_id = request.headers.get('X-Trace-Id', str(uuid.uuid4()))
        ctx = TraceContext(trace_id=trace_id)
        token = trace_ctx.set(ctx)
        
        start = time.time()
        
        try:
            response = self.handle_request(request)
            duration = (time.time() - start) * 1000
            
            logger.info("request_complete",
                method=request.method,
                path=request.path,
                status=response.status_code,
                duration_ms=round(duration, 2),
                trace_id=trace_id,
            )
            
            metrics.histogram("request_duration", duration,
                            {"method": request.method, "status": f"{response.status_code}"[:1]+"xx"})
            
            return response
        
        except Exception as e:
            logger.error("request_error",
                method=request.method,
                path=request.path,
                error=str(e),
                trace_id=trace_id,
            )
            metrics.counter("request_error", {"method": request.method})
            raise
        
        finally:
            trace_ctx.reset(token)
```

## Common Pitfalls

1. **Logging sensitive data** — PII, passwords, tokens in logs violate GDPR/security; scrub before logging
2. **String formatting in hot paths** — f"Slow query: {query}" in a loop allocates thousands of strings; use lazy evaluation
3. **Too much INFO logging** — logs become noise; everything that's not actionable should be DEBUG
4. **No log correlation ID** — across services, logs can't be connected without a trace ID
5. **Synchronous metrics in hot paths** — blocking metrics writes slow down requests; use async or in-memory batching
6. **Metric cardinality explosion** — tagging every user_id as a label creates millions of time series; limit to reasonable cardinality

## Verification Checklist

- [ ] All logs are structured (JSON), not plain text
- [ ] Every request has a correlation/trace ID
- [ ] PII and secrets are scrubbed from logs
- [ ] Log levels are appropriate (ERROR = actionable)
- [ ] Metrics have reasonable cardinality
- [ ] Tracing spans cover all external dependencies
- [ ] Log volume is manageable (not overwhelming storage/ingestion)

## See Also

- debugging-techniques-advanced — using logs for debugging
- performance-optimization — profiling with metrics
- distributed-systems-patterns — tracing in distributed systems
- service-mesh-patterns — automatic tracing in service mesh
