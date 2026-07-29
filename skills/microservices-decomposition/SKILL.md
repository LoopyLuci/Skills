---
name: microservices-decomposition
description: "Use when decomposing monoliths into microservices."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [microservices, decomposition, monolith, bounded-context, domain-driven-design]
    related_skills: [distributed-systems-patterns, api-design-rest-graphql, container-networking-patterns, event-driven-architecture]
---

# Microservices Decomposition

Decomposing monolithic applications into microservices — from bounded context mapping through service boundaries, inter-service communication, data decomposition, and migration strategies.

## When to Use

- Breaking a monolith into microservices
- Identifying service boundaries from domain analysis
- Designing inter-service communication patterns
- Migrating data from shared to per-service databases
- Managing the decomposition process safely

## Decomposition Patterns

```python
DECOMPOSITION_STRATEGIES = {
    'business_capability': 'Split by business functions (orders, payments, shipping)',
    'subdomain': 'Split by DDD subdomains (core, supporting, generic)',
    'strangler_fig': 'Gradually replace monolith pieces with new services',
    'event_storming': 'Identify aggregates and bounded contexts via workshops',
}

def identify_services(domain_events: List[str]) -> List[str]:
    """Identify candidate services from domain events."""
    # Group events by noun/entity
    services = set()
    for event in domain_events:
        words = event.split()
        # First noun after the verb is likely a service candidate
        for i, w in enumerate(words):
            if w.lower() in ('created', 'updated', 'deleted', 'submitted', 'approved'):
                if i + 1 < len(words):
                    services.add(words[i + 1].lower())
    return list(services)
```

## Common Pitfalls

1. **Distributed monolith** — services that can't be deployed independently
2. **Shared database** — services sharing a database = no real decomposition
3. **Too fine-grained** — each method as a service creates overhead chaos
4. **Wrong boundaries** — splitting along technical layers (not business domains)
5. **No data strategy** — data is the hardest part; plan per-service databases

## Verification Checklist

- [ ] Bounded contexts identified and mapped
- [ ] Services align with business capabilities
- [ ] Each service has its own data store
- [ ] Inter-service communication pattern chosen (sync/async/event)
- [ ] Strangler Fig migration plan in place
- [ ] Deployment independence verified
