---
name: chaos-engineering
description: "Use when implementing chaos engineering experiments."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [chaos-engineering, resilience-testing, fault-injection, Gameday, reliability]
    related_skills: [security-incident-response, agent-fault-tolerance, distributed-systems-patterns, load-testing]
---

# Chaos Engineering

Implementing chaos engineering to build resilient systems — from fault injection and experiment design through steady-state hypothesis, blast radius control, and Game Days.

## When to Use

- Testing system resilience before failures happen in production
- Building confidence in fault tolerance mechanisms
- Finding edge cases that only appear under failure conditions
- Training incident response teams in realistic scenarios
- Validating SLIs/SLOs under adverse conditions

## Experiment Design

```python
CHAOS_PRINCIPLES = {
    'steady_state': 'Define normal system behavior (latency, error rate, throughput)',
    'hypothesis': 'Predict steady state continues when fault is injected',
    'blast_radius': 'Minimize impact scope (staging first, canary, production)',
    'automated': 'Experiments run automatically with rollback conditions',
    'continuous': 'Chaos as part of normal development, not one-time event',
}

class ChaosExperiment:
    """Design and run chaos experiments."""
    
    COMMON_FAULTS = [
        'Kill random pod/container',
        'Inject network latency (+100ms)',
        'Block network port (database port)',
        'Exhaust CPU on instance (stress-ng)',
        'Fill disk to 90% capacity',
        'Rotate/expire TLS certificate',
        'Kill upstream dependency process',
        'Introduce packet loss (1%/5%/10%)',
    ]
    
    def __init__(self, name: str, steady_state: Dict):
        self.name = name
        self.steady = steady_state  # expected metrics
        self.faults = []
        self.results = {}
    
    def add_fault(self, target: str, fault_type: str, 
                  duration_seconds: int = 60):
        self.faults.append({
            'target': target, 'type': fault_type,
            'duration': duration_seconds,
        })
    
    def run(self, environment: str = 'staging'):
        for fault in self.faults:
            inject_fault(fault)  # simplified
            results = measure_impact()
            self.results = results
            rollback_fault(fault)
```

## Common Pitfalls

1. **Blast radius too large** — always start in staging, then canary, then prod
2. **No rollback plan** — every experiment must have automated rollback on threshold breach
3. **Testing what you already know** — test assumptions, not known failures
4. **No steady state baseline** — can't detect deviation without knowing normal
5. **Chaos theater** — running experiments without acting on findings wastes effort

## Verification Checklist

- [ ] Steady state metrics defined (latency, error rate, throughput)
- [ ] Blast radius controls in place (canary, circuit breakers)
- [ ] Automated rollback on threshold breach
- [ ] All experiments have clear hypothesis statement
- [ ] Results documented and action items tracked
- [ ] Game Day schedule (quarterly at minimum)
- [ ] Post-experiment review with incident response team
