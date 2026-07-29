---
name: service-mesh-patterns
description: "Use when designing service mesh architecture and patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [service-mesh, istio, linkerd, envoy, sidecar, microservices]
    related_skills: [api-gateway-load-balancing, zero-trust-network-architecture, distributed-systems-patterns, multi-platform-project]
---

# Service Mesh Patterns

Designing and implementing service mesh architectures for microservices communication — sidecar proxies, traffic management, observability, security, and resilience patterns using Envoy/Istio/Linkerd concepts.

## When to Use

- Managing service-to-service communication in a microservices architecture
- Implementing mTLS, traffic splitting, or circuit breaking at the mesh layer
- Adding observability (traces, metrics, logs) without application changes
- Transitioning from application-level resilience to infrastructure-level
- Multi-cluster or multi-cloud service connectivity

## Architecture

```
Pod/Container:
┌──────────────────┐
│  Service A        │
│  (Application)    │
├──────────────────┤
│  Sidecar Proxy    │ ← Envoy, Linkerd-proxy, or similar
│  (Data Plane)     │
└──────┬───────────┘
       │ mTLS + Telemetry
       │
┌──────┴───────────┐
│  Control Plane    │
│  (Istiod, etc.)   │
└──────────────────┘
```

## Sidecar Proxy Pattern

```python
class SidecarProxy:
    """Simplified sidecar proxy implementation (conceptual)."""
    
    def __init__(self, service_name, control_plane_endpoint):
        self.service_name = service_name
        self.control_plane = control_plane_endpoint
        self.routes = {}
        self.certs = None
        self.metrics = {'requests': 0, 'errors': 0, 'latency': []}
    
    def intercept_ingress(self, request):
        """Handle incoming request to the service."""
        # 1. TLS termination
        request = self.decrypt(request)
        
        # 2. Authentication / mTLS verification
        if not self.verify_mtls(request):
            return self.reject(401)
        
        # 3. Rate limiting
        if not self.rate_limiter.allow():
            return self.reject(429)
        
        # 4. Auth政策 (RBAC)
        if not self.check_auth(request):
            return self.reject(403)
        
        # 5. Telemetry
        start = time.time()
        
        # 6. Forward to local service
        response = self.forward_to_local(request)
        
        # 7. Record metrics
        self.metrics['requests'] += 1
        self.metrics['latency'].append(time.time() - start)
        
        return response
    
    def intercept_egress(self, request, target_service):
        """Handle outgoing request to another service."""
        # 1. Service discovery
        endpoints = self.resolve_service(target_service)
        
        # 2. Load balancing
        endpoint = self.load_balancer.pick(endpoints)
        
        # 3. Traffic policy (timeout, retry, circuit breaker)
        # 4. mTLS encryption
        request = self.encrypt(request, endpoint)
        
        # 5. Send with telemetry headers
        request.headers['x-request-id'] = str(uuid.uuid4())
        request.headers['x-trace-id'] = self.current_trace_id
        
        return self.send(request, endpoint)
```

## Traffic Management

### Traffic Splitting / Canary

```python
class TrafficManager:
    """Traffic routing policies for canary deployments."""
    
    def __init__(self):
        self.rules = {}
    
    def add_route_rule(self, service, subsets):
        """
        subsets: [{'name': 'stable', 'weight': 90},
                  {'name': 'canary', 'weight': 10}]
        """
        self.rules[service] = subsets
    
    def route_request(self, service, request):
        """Route request to subset based on weights."""
        if service not in self.rules:
            return service  # Default
        
        subsets = self.rules[service]
        roll = random.random() * 100
        cumulative = 0
        
        for subset in subsets:
            cumulative += subset['weight']
            if roll <= cumulative:
                return f"{service}-{subset['name']}"
        
        return f"{service}-{subsets[-1]['name']}"
    
    def match_based_routing(self, service, request):
        """Route based on request attributes (headers, cookies)."""
        # Istio-style: route based on header match
        if request.headers.get('x-canary') == 'true':
            return f"{service}-canary"
        if request.cookies.get('experiment') == 'b':
            return f"{service}-experiment-b"
        return f"{service}-stable"
```

### Timeouts and Retries

```python
class ResiliencePolicy:
    """Service-level resilience configuration."""
    
    def __init__(self, service):
        self.service = service
        self.timeout_ms = 5000
        self.retries = 3
        self.retry_on = ['connect-failure', 'refused-stream', 'unavailable']
        self.circuit_breaker = {
            'consecutive_errors': 5,
            'sleep_window_ms': 30000,
            'max_ejection_percent': 50
        }
    
    def should_retry(self, attempt, error):
        if attempt >= self.retries:
            return False
        return error.type in self.retry_on
```

## Observability

### Distributed Tracing

```python
import uuid
import time

class TraceContext:
    """Propagate trace context across service boundaries."""
    
    def __init__(self):
        self.trace_id = None
        self.span_id = None
        self.parent_span_id = None
    
    @classmethod
    def from_headers(cls, headers):
        context = cls()
        context.trace_id = headers.get('x-trace-id')
        context.span_id = headers.get('x-span-id')
        context.parent_span_id = headers.get('x-parent-span-id')
        return context
    
    @classmethod
    def new(cls):
        context = cls()
        context.trace_id = str(uuid.uuid4())
        context.span_id = str(uuid.uuid4())
        return context
    
    def to_headers(self):
        return {
            'x-trace-id': self.trace_id,
            'x-span-id': str(uuid.uuid4()),
            'x-parent-span-id': self.span_id
        }


class Tracer:
    """Collect and export trace spans."""
    
    def __init__(self, service_name):
        self.service = service_name
        self.spans = []
    
    def record_span(self, name, context, start_time, end_time, tags=None):
        span = {
            'trace_id': context.trace_id,
            'span_id': context.span_id,
            'parent_span_id': context.parent_span_id,
            'service': self.service,
            'operation': name,
            'start_time': start_time,
            'duration_ms': (end_time - start_time) * 1000,
            'tags': tags or {}
        }
        self.spans.append(span)
        return span
```

### Metrics

```python
class ServiceMetrics:
    """Request-level metrics collected by the sidecar."""
    
    def __init__(self, service_name):
        self.service = service_name
        self.counters = {'requests_total': 0, 'errors_total': 0}
        self.histograms = {'request_duration_ms': []}
        self.gauges = {'connections_active': 0}
    
    def record_request(self, duration_ms, status_code):
        self.counters['requests_total'] += 1
        if status_code >= 500:
            self.counters['errors_total'] += 1
        self.histograms['request_duration_ms'].append(duration_ms)
```

## Security

### mTLS Implementation

```python
class MutualTLS:
    """Service-to-service mTLS with automatic certificate rotation."""
    
    def __init__(self, identity):
        self.identity = identity
        self.certs = {}
    
    def request_certificate(self, spiffe_endpoint):
        """Request SPIFFE certificate from control plane."""
        # CSR generation → Control Plane signs → Return cert
        pass
    
    def verify_peer(self, peer_cert, expected_spiffe_id):
        """Verify peer certificate against expected identity."""
        from cryptography import x509
        cert = x509.load_pem_x509_certificate(peer_cert)
        # Extract SPIFFE ID from SAN extension
        spiffe_id = self._extract_spiffe(cert)
        return spiffe_id == expected_spiffe_id
```

## Common Pitfalls

1. **Sidecar resource overhead** — each sidecar adds ~50MB RAM per pod; optimize for scale
2. **Control plane latency** — misconfigured control plane causes Envoy hot-reload storms
3. **mTLS complexity** — certificate rotation, trust domain management, and root CA protection
4. **Protocol limitations** — not all protocols work transparently (UDP, HTTP/2->HTTP/1.1)
5. **Debugging overhead** — tracing adds storage cost; sample at 1-10%
6. **Feature envy** — don't put everything in the mesh; some concerns belong in the application

## Verification Checklist

- [ ] Sidecar intercepts all ingress/egress traffic transparently
- [ ] mTLS established between all services (verify with tcpdump)
- [ ] Traffic splitting routes correct % to each subset
- [ ] Circuit breaker trips and recovers correctly
- [ ] Distributed traces span all services in a request
- [ ] Metrics exported and queryable (Prometheus format)
- [ ] Certificate rotation works without connection drops

## See Also

- api-gateway-load-balancing — edge gateway vs. mesh
- zero-trust-network-architecture — ZTA with mTLS
- distributed-systems-patterns — broader microservices patterns
- multi-platform-project — multi-service deployment
