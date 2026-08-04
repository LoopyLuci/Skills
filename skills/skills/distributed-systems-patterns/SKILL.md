---
name: distributed-systems-patterns
description: "Use when building distributed systems and services."
category: software-development
tags: [distributed-systems, consensus, replication, fault-tolerance]
---
# Distributed Systems Patterns

Core patterns for building reliable distributed systems.

## Consensus Algorithms

```python
# Raft: Leader election + log replication
# 3 phases:
# 1. Leader election (term, votes, heartbeat)
# 2. Log replication (append entries, commit index)
# 3. Safety (election restriction, log matching)

# Paxos: More general, harder to understand
# Raft is the practical choice for most systems
```

## Service Discovery

```python
# Client-side discovery
# Service registers with registry (Consul, etcd, ZooKeeper)
# Client queries registry for available instances
# Client load-balances across instances

# Server-side discovery
# Service registers with registry
# Load balancer queries registry
# Client hits load balancer (simpler client)
```

## Circuit Breaker

```python
class CircuitBreaker:
    def __init__(self, threshold: int = 5, recover_seconds: int = 30):
        self.threshold = threshold
        self.recover_seconds = recover_seconds
        self.failures = 0
        self.state = "CLOSED"     # CLOSED, OPEN, HALF_OPEN
        self.last_failure = 0

    def call(self, fn, fallback_fn=None):
        if self.state == "OPEN":
            if time.time() - self.last_failure > self.recover_seconds:
                self.state = "HALF_OPEN"
            else:
                return fallback_fn() if fallback_fn else None

        try:
            result = fn()
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure = time.time()
            if self.failures >= self.threshold:
                self.state = "OPEN"
            return fallback_fn() if fallback_fn else None
```

## Saga Pattern (Distributed Transactions)

```python
# Choreography saga (each service knows next step)
# Step 1: Order Service creates order → publishes "OrderCreated"
# Step 2: Payment Service listens → processes payment → publishes "PaymentCompleted"
# Step 3: Shipping Service listens → ships → publishes "Shipped"
# On failure: each step has a compensating action

# Orchestration saga (central coordinator)
class SagaOrchestrator:
    def __init__(self):
        self.steps = []   # [(action_fn, compensate_fn)]

    def add_step(self, action, compensation):
        self.steps.append((action, compensation))

    def execute(self):
        completed = []
        for action, compensation in self.steps:
            try:
                action()
                completed.append((action, compensation))
            except Exception:
                # Rollback in reverse order
                for _, comp in reversed(completed):
                    comp()
                raise
```

## Health Checks

```python
# Liveness: Is the process alive?
GET /healthz → 200 OK

# Readiness: Can the process serve traffic?
GET /readyz → 200 OK (waits for DB migrations, cache warmup)

# Startup: Has the process initialized?
GET /startupz → 200 OK (slower, one-time check)
```

## Pitfalls

- Network is not reliable — always expect timeouts and retries
- Latency is not zero — measure and budget for it
- Bandwidth is not infinite — batch small messages
- Topology changes — nodes join and leave unexpectedly
- Distributed consensus is slow (multiple rounds) — avoid if not needed
