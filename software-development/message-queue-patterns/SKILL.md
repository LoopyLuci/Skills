---
name: message-queue-patterns
description: "Use when implementing message queues and stream processing."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [message-queue, kafka, rabbitmq, pub-sub, streaming, event-bus]
    related_skills: [event-driven-architecture, data-pipeline-streaming, microservices-decomposition, distributed-systems-patterns]
---

# Message Queue Patterns

Implementing message queue and stream processing systems — from pub-sub and point-to-point through Kafka/RabbitMQ patterns, consumer groups, and exactly-once semantics.

## When to Use

- Decoupling microservices via async messaging
- Building event-driven data pipelines
- Buffering spikes in request volume
- Implementing pub-sub for broadcast events
- Processing streams in real-time

## Queue Types

```python
QUEUE_TYPES = {
    'point_to_point': 'One producer, one consumer (competing consumers)',
    'pub_sub': 'One producer, multiple subscribers each get all messages',
    'request_reply': 'Producer sends, consumer replies (RPC over queue)',
    'dead_letter': 'Failed messages are stored for later inspection',
}

class MessageBroker:
    """Simple in-memory message broker."""
    def __init__(self):
        self.queues = {}
        self.topics = {}
    
    def create_queue(self, name: str):
        self.queues[name] = []
    
    def publish_to_queue(self, queue: str, message: dict):
        if queue in self.queues:
            self.queues[queue].append(message)
    
    def consume_from_queue(self, queue: str) -> dict:
        if queue in self.queues and self.queues[queue]:
            return self.queues[queue].pop(0)
        return None
```

## Common Pitfalls

1. **No message ordering guarantees** — Kafka partitions order within, not across; design for it
2. **Exactly-once is hard** — at-least-once with idempotent consumers is more practical
3. **No dead letter queue** — failed messages block the queue; have a DLQ
4. **Monitoring blind spot** — queue depth growing silently indicates a problem
5. **Schema evolution** — messages change shape over time; use Avro/Protobuf with schema registry

## Verification Checklist

- [ ] Queue topology matches use case (point-to-point vs pub-sub)
- [ ] Consumer idempotency implemented (replay safety)
- [ ] Dead letter queue configured per queue/topic
- [ ] Message schema versioned (schema registry)
- [ ] Monitoring on queue depth, consumer lag, throughput
- [ ] Exactly-once vs at-least-once semantics documented
