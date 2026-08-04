---
name: chaos-engineering-advanced
description: "Use when implementing advanced chaos engineering patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [chaos-engineering, resilience, Litmus, Gremlin, game-day, fault-injection]
    related_skills: [chaos-engineering, site-reliability-engineering, incident-management-on-call, error-budgets-slos]
---

# Advanced Chaos Engineering

Implementing advanced chaos engineering — from game day automation and steady-state hypothesis through Litmus/Gremlin, chaos mesh, and production verification testing.

## When to Use

- Running automated chaos experiments in CI/CD
- Building resilience pipelines (Chaos as part of deployment)
- Multi-cluster and multi-region chaos testing
- Production verification testing (PVT)

## Advanced Chaos Patterns

```python
CHAOS_ADVANCED = {
    'continuous_chaos': 'Chaos experiments as part of deployment pipeline, not one-off',
    'game_day': 'Scheduled chaos exercises with cross-team participation',
    'blast_radius_progressive': 'Start small (1 pod) → expand (zone) → region',
    'steady_state_automation': 'Automated verification that system returns to steady state post-chaos',
    'chaos_mesh': 'Kubernetes-native chaos platform, CRD-based experiment definitions',
}

# Litmus experiment template
LITMUS_EXPERIMENT = """
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosEngine
metadata:
  name: pod-delete-engine
spec:
  appinfo:
    appns: 'default'
    applabel: 'app=my-service'
  annotationCheck: 'false'
  experiments:
    - name: pod-delete
      spec:
        probe:
          - name: probe-http-200
            type: httpProbe
            httpProbe/inputs:
              url: 'https://my-service/health'
            runProbe:
              - probeDuration: 60
"""
```

## Verification Checklist

- [ ] Chaos experiments defined as code (Chaos Mesh, Litmus, Gremlin)
- [ ] Steady-state metrics captured before each experiment
- [ ] Blast radius controls (scope, duration, rollback)
- [ ] Automated rollback on critical threshold breach
- [ ] Experiments gated by error budget consumption
- [ ] Game day schedule (quarterly for critical services)
- [ ] Experiment results documented and shared
- [ ] Chaos pipeline in CI/CD (break glass on findings)
