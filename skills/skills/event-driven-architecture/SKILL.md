---
name: event-driven-architecture
description: "Use when designing event-driven and message-driven systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [event-driven, messaging, kafka, async, events, CQRS, saga, pub-sub]
    related_skills: [microservices-decomposition, distributed-systems-patterns, message-queue-patterns, data-pipeline-streaming]
---

# Event-Driven Architecture

Designing event-driven systems — from event schemas and message brokers through event sourcing, CQRS, sagas, and event-driven microservices.

## When to Use

- Decoupling services through asynchronous communication
- Building event-driven microservices
- Implementing event sourcing or CQRS patterns
- Orchestrating distributed transactions via sagas
- Processing event streams in real-time

## Key Patterns

```python
from typing import Dict, List, Callable
import json, uuid
from datetime import datetime

class Event:
    """Domain event with metadata."""
    def __init__(self, name: str, data: Dict, source: str = ''):
        self.id = str(uuid.uuid4())
        self.name = name
        self.data = data
        self.source = source
        self.timestamp = datetime.now().isoformat()
        self.version = 1

class EventBus:
    """Simple in-memory event bus with pub/sub."""
    def __init__(self):
        self.subscribers = {}  # event_name -> [handlers]
    
    def publish(self, event: Event):
        handlers = self.subscribers.get(event.name, [])
        for handler in handlers:
            handler(event)
    
    def subscribe(self, event_name: str, handler: Callable):
        self.subscribers.setdefault(event_name, []).append(handler)
```

## Common Pitfalls

1. **No event schema governance** — events change shape and break consumers
2. **At-most-once vs at-least-once** — choose delivery semantics per use case
3. **Eventual consistency surprises** — systems are eventually consistent; design for it
4. **Saga failure handling** — compensating transactions are hard; test failure paths
5. **Event schema evolution** — backward compatibility is essential; use Avro/Protobuf

## Verification Checklist

- [ ] Event schemas defined and versioned
- [ ] Delivery semantics chosen per event type
- [ ] Idempotent consumers (replay safety)
- [ ] Dead letter queue configured
- [ ] Monitoring on event latency and throughput
