---
name: site-reliability-engineering
description: "Use when implementing SRE patterns and practices."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [SRE, reliability, SLIs, SLOs, error-budgets, toil-automation, observability]
    related_skills: [error-budgets-slos, incident-management-on-call, chaos-engineering, open-telemetry-distributed-tracing]
---

# Site Reliability Engineering

Implementing SRE practices — from SLIs/SLOs and error budgets through toil automation, capacity planning, and reliability culture.

## When to Use

- Building reliability into production systems
- Defining and tracking service level objectives
- Automating operations to reduce toil
- Balancing reliability with feature velocity
- Implementing incident response and blameless culture

## SRE Foundations

```python
SRE_PRACTICES = {
    'slis': 'Service Level Indicators — latency, error rate, throughput, availability',
    'slos': 'Service Level Objectives — target thresholds (e.g., 99.9% uptime)',
    'error_budget': '100% - SLO = acceptable error budget; releases consume budget',
    'toil': 'Manual, repetitive, automatable operational work — target <50% of time',
    'blameless': 'Postmortems that focus on systems, not people; culture of learning',
}

class SREMonitor:
    """Track SLIs against SLOs with error budget."""
    def __init__(self, slo_target: float = 0.999):
        self.slo = slo_target
        self.error_budget = 1.0 - slo_target
        self.measurements = []
    
    def record(self, total_requests: int, failed_requests: int, window: str = '30d'):
        availability = 1 - (failed_requests / max(total_requests, 1))
        budget_consumed = (1 - availability) / self.error_budget
        self.measurements.append({
            'window': window, 'availability': round(availability, 4),
            'budget_remaining': round(max(0, 1 - budget_consumed), 4),
        })
        return self.measurements[-1]
```

## Verification Checklist

- [ ] SLIs defined for latency, error rate, throughput, availability
- [ ] SLOs set with realistic targets (99.9%, 99.95%, 99.99%)
- [ ] Error budget policy defined (consumption → freeze releases)
- [ ] Toil measured and tracked (target <50% of ops time)
- [ ] Blameless postmortem culture established
- [ ] Capacity planning with load testing
- [ ] Observability stack (metrics, traces, logs) in place
