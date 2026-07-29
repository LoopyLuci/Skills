---
name: system-design-patterns
description: "Use when designing large-scale distributed systems."
category: software-development
tags: [system-design, distributed-systems, scalability, architecture]
---
# System Design Patterns

Patterns for designing large-scale distributed systems.

## Core Patterns

### Caching
```
Client → [Cache] → Database
Patterns: cache-aside, read-through, write-through, write-behind
Eviction: LRU, LFU, TTL, FIFO
```

### Load Balancing
```
Client → [Load Balancer] → [Server Pool]
Algorithms: round-robin, least-connections, IP hash, weighted
```

### Database Scaling
```
Read replicas: writes → primary, reads → replicas
Sharding: horizontal split by key (user_id, region)
Partitioning: vertical split by table/column group
```

## Common Architectures

### Event-Driven
```
Service A → [Event Bus] → Service B
                         → Service C
Uses: async processing, decoupling, fan-out
Tools: Kafka, RabbitMQ, SQS, EventBridge
```

### Microservices
```
API Gateway
├── Auth Service
├── Order Service → Database
├── Payment Service → Third-party API
└── Notification Service → [Message Queue]
Communication: REST/gRPC (sync), Events (async)
```

### CQRS (Command Query Responsibility Segregation)
```
Command Path:          Query Path:
POST /orders          GET /orders
    ↓                     ↓
Command Handler        Query Handler
    ↓                     ↓
Write DB ──sync/async──→ Read DB (denormalized)
```

## Consistency Patterns

```python
# Strong consistency: all reads see latest write
# Eventual consistency: reads may see stale data, converges
# Read-your-writes: user always sees their own writes
# Monotonic reads: successive reads are never stale

# CAP Theorem: Pick 2 of 3
# Consistency, Availability, Partition Tolerance
# CP systems: HBase, MongoDB (default)
# AP systems: Cassandra, DynamoDB
```

## Rate Limiting

```python
class TokenBucket:
    def __init__(self, rate: int, capacity: int):
        self.rate = rate      # tokens per second
        self.capacity = capacity
        self.tokens = capacity
        self.last_refill = time.time()

    def allow_request(self) -> bool:
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_refill = now

        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```

## Pitfalls

- Caching adds complexity (stale data, invalidation, cold starts)
- Microservices need mature DevOps (deploy, monitor, debug)
- Eventual consistency is hard for humans to reason about
- Distributed transactions (2PC) are slow — use saga pattern instead
- Premature scaling adds cost without benefit — measure first
