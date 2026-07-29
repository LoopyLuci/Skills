---
name: api-gateway-load-balancing
description: "Use when designing API gateway and load balancing patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [api-gateway, load-balancing, reverse-proxy, traffic-management]
    related_skills: [api-design-rest-graphql, proxy-server-engine, service-mesh-patterns, traffic-shaper]
---

# API Gateway and Load Balancing Patterns

Designing API gateways and load balancers for microservices — request routing, rate limiting, authentication, service discovery, and traffic management at the edge.

## When to Use

- Building an API gateway for microservices architecture
- Implementing rate limiting, authentication, or routing at edge
- Designing load balancing strategies for horizontally scaled services
- Centralizing cross-cutting concerns (auth, logging, caching)
- Replacing or supplementing Nginx, Envoy, or Kong with custom logic

## API Gateway Architecture

```
Client → API Gateway → Auth → Rate Limiter → Router → Backend Services
                         ↓          ↓           ↓
                      RBAC        Quota     Service Discovery
```

## Core Components

### Request Router

```python
import re
from typing import Callable, Dict, List, Optional

class Route:
    """API route with pattern matching and middleware."""
    def __init__(self, method: str, pattern: str, 
                 upstream: str, middlewares: List[Callable] = None):
        self.method = method.upper()
        self.pattern = re.compile(pattern)
        self.upstream = upstream
        self.middlewares = middlewares or []

class Router:
    """HTTP request router with path parameters."""
    
    def __init__(self):
        self.routes: List[Route] = []
    
    def add_route(self, method: str, path: str, upstream: str):
        """Register a route."""
        # Convert path with params to regex
        pattern = re.sub(r'\{(\w+)\}', r'(?P<\1>[^/]+)', path)
        self.routes.append(Route(method, f'^{pattern}$', upstream))
    
    def match(self, method: str, path: str) -> Optional[tuple]:
        """Match request to a route and extract path params."""
        for route in self.routes:
            if route.method != method.upper():
                continue
            match = route.pattern.match(path)
            if match:
                return route, match.groupdict()
        return None
```

### Rate Limiter

```python
import time
from collections import defaultdict
from threading import Lock

class SlidingWindowRateLimiter:
    """Sliding window rate limiter (per-client)."""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self.clients: Dict[str, list] = defaultdict(list)
        self.lock = Lock()
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if request is within rate limit."""
        now = time.time()
        
        with self.lock:
            # Clean old entries
            timestamps = self.clients[client_id]
            cutoff = now - self.window
            self.clients[client_id] = [t for t in timestamps if t > cutoff]
            
            # Check limit
            if len(self.clients[client_id]) >= self.max_requests:
                return False
            
            self.clients[client_id].append(now)
            return True


class TokenBucket:
    """Token bucket rate limiter."""
    
    def __init__(self, rate: float, burst: int):
        self.rate = rate  # Tokens per second
        self.burst = burst  # Max tokens
        self.tokens = burst
        self.last_refill = time.time()
    
    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens. Returns True if allowed."""
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
        self.last_refill = now
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
```

### Circuit Breaker

```python
import time

class CircuitBreaker:
    """Circuit breaker for upstream services."""
    
    def __init__(self, failure_threshold=5, recovery_timeout=30, half_open_max=3):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max = half_open_max
        self.state = 'closed'  # closed, open, half-open
        self.last_failure_time = 0
        self.half_open_successes = 0
    
    def call(self, fn, fallback=None):
        """Execute fn with circuit breaker."""
        if self.state == 'open':
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = 'half-open'
            else:
                return fallback() if fallback else None
        
        try:
            result = fn()
            if self.state == 'half-open':
                self.half_open_successes += 1
                if self.half_open_successes >= self.half_open_max:
                    self.state = 'closed'
                    self.failure_count = 0
                    self.half_open_successes = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = 'open'
                self.failure_count = 0
            if fallback:
                return fallback()
            raise
```

## Load Balancing Strategies

```python
import random
import hashlib

class LoadBalancer:
    """Multiple load balancing strategies."""
    
    def __init__(self, backends: list):
        self.backends = backends  # List of backend URLs
    
    # Round Robin
    def round_robin(self):
        idx = 0
        while True:
            yield self.backends[idx % len(self.backends)]
            idx += 1
    
    # Least Connections (simulated)
    def least_connections(self, connection_counts: Dict[str, int]):
        return min(connection_counts, key=connection_counts.get)
    
    # Random
    def random(self):
        return random.choice(self.backends)
    
    # IP Hash (sticky sessions)
    def ip_hash(self, client_ip: str):
        hash_val = int(hashlib.md5(client_ip.encode()).hexdigest(), 16)
        return self.backends[hash_val % len(self.backends)]
    
    # Weighted Round Robin
    def weighted_round_robin(self, weights: Dict[str, int]):
        """Distribute requests proportional to weight."""
        total = sum(weights.values())
        weighted_pool = []
        for backend, weight in weights.items():
            weighted_pool.extend([backend] * weight)
        
        idx = 0
        while True:
            yield weighted_pool[idx % len(weighted_pool)]
            idx += 1
    
    # Consistent Hashing
    def consistent_hash(self, key: str, virtual_nodes: int = 100):
        """Consistent hashing for minimal redistribution on backend changes."""
        ring = {}
        for i, backend in enumerate(self.backends):
            for v in range(virtual_nodes):
                node_key = f"{backend}:{v}"
                hash_val = hashlib.md5(node_key.encode()).hexdigest()
                ring[hash_val] = backend
        
        sorted_keys = sorted(ring.keys())
        key_hash = hashlib.md5(key.encode()).hexdigest()
        
        for ring_key in sorted_keys:
            if key_hash <= ring_key:
                return ring[ring_key]
        return ring[sorted_keys[0]]
```

## Authentication Middleware

```python
import jwt
from datetime import datetime, timedelta

class AuthMiddleware:
    """JWT-based authentication for API gateway."""
    
    def __init__(self, secret: str, algorithms: list = ['HS256']):
        self.secret = secret
        self.algorithms = algorithms
    
    def create_token(self, user_id: str, role: str, ttl: int = 3600):
        payload = {
            'user_id': user_id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(seconds=ttl)
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithms[0])
    
    def verify_token(self, token: str) -> dict:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(token, self.secret, algorithms=self.algorithms)
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def require_role(self, required_role: str):
        """Middleware factory: require specific role."""
        def middleware(request):
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            payload = self.verify_token(token)
            if not payload:
                return {'status': 401, 'body': 'Unauthorized'}
            if payload.get('role') != required_role:
                return {'status': 403, 'body': 'Forbidden'}
            request.user = payload
            return None  # Proceed
        return middleware
```

## Common Pitfalls

1. **Single point of failure** — gateway itself becomes SPOF; deploy in HA with health checks
2. **Latency addition** — each middleware adds latency; benchmark and optimize hot paths
3. **Certificate management** — TLS termination at gateway means backend-to-gateway traffic needs separate encryption
4. **Rate limiter state loss** — in-memory rate limiters lose state on restart; use Redis for persistence
5. **Stale routing tables** — backend services change; integrate with service discovery (Consul, K8s)
6. **Timeout cascading** — upstream timeouts compound; set per-service timeouts with sensible defaults

## Verification Checklist

- [ ] Routes correctly match and forward to backends
- [ ] Rate limiting blocks excessive requests (test with burst)
- [ ] Circuit breaker trips on upstream failure and recovers
- [ ] Load balancing distributes requests evenly (test with weights)
- [ ] TLS termination works (HTTPS → backend HTTP)
- [ ] Request/response transformation works (headers, body)
- [ ] Graceful degradation on backend failures

## See Also

- api-design-rest-graphql — designing the APIs being routed
- proxy-server-engine — building the underlying proxy
- service-mesh-patterns — service-to-service communication
- traffic-shaper — QoS and rate shaping
