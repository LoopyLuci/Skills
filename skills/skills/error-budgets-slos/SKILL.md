---
name: error-budgets-slos
description: "Use when implementing error budgets and SLO management."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [error-budget, SLO, SLI, reliability, burn-rate, alerting]
    related_skills: [site-reliability-engineering, incident-management-on-call, chaos-engineering, open-telemetry-distributed-tracing]
---

# Error Budgets and SLO Management

Implementing error budgets and SLO management — from SLI definition through burn rate alerting, error budget policy, and reliability decision-making.

## When to Use

- Setting SLOs for production services
- Managing error budgets between reliability and velocity
- Implementing burn-rate alerting
- Making data-driven reliability decisions

## SLO Management

```python
class SLOManager:
    """Track SLOs and error budgets with burn-rate alerts."""
    
    def __init__(self, slo_target: float, window_days: int = 30):
        self.slo = slo_target
        self.window = window_days
        self.total_events = 0
        self.bad_events = 0
    
    def record(self, total: int, bad: int):
        self.total_events += total
        self.bad_events += bad
    
    def budget_remaining(self) -> float:
        allowed_bad = self.total_events * (1 - self.slo)
        consumed = self.bad_events / max(allowed_bad, 1)
        return max(0.0, 1.0 - consumed)
    
    def burn_rate(self, window_minutes: int = 60) -> str:
        """Burn rate alerting: budget consumed faster than expected."""
        consumption_rate = self.bad_events / max(self.total_events, 1)
        expected_rate = 1 - self.slo
        
        if consumption_rate > expected_rate * 10: return "Critical: burn rate 10x"
        if consumption_rate > expected_rate * 5: return "Warning: burn rate 5x"
        if consumption_rate > expected_rate * 2: return "Notice: burn rate 2x"
        return "Normal"
```

## Verification Checklist

- [ ] SLIs defined for latency, error rate, throughput, availability
- [ ] SLO targets set per service tier (critical, standard, best-effort)
- [ ] Error budget window defined (30 days typical)
- [ ] Burn rate alerting configured (2x, 5x, 10x thresholds)
- [ ] Error budget policy documented (what happens when budget is exhausted)
- [ ] SLO dashboards visible to engineering teams
- [ ] Quarterly SLO review and adjustment process
