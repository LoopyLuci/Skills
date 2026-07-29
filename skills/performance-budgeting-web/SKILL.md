---
name: performance-budgeting-web
description: "Use when setting performance budgets for web projects."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [performance-budget, web-perf, Lighthouse, Core-Web-Vitals, bundle-size]
    related_skills: [responsive-web-design-patterns, web-accessibility-practices, frontend-bootstrap, caching-strategies]
---

# Performance Budgeting for Web

Setting and enforcing performance budgets for web projects — from defining budgets and measuring with Lighthouse through CI/CD enforcement and performance regression tracking.

## When to Use

- Preventing performance regression in web applications
- Setting measurable performance targets for teams
- Enforcing budgets in CI/CD pipelines
- Monitoring Core Web Vitals (LCP, FID, CLS)

## Budget Types

```python
PERFORMANCE_BUDGETS = {
    'time': 'Page load < 3s on 3G, Time to Interactive < 5s',
    'size': 'Total JS < 300KB, total CSS < 100KB, images < 500KB',
    'count': 'HTTP requests < 25, third-party scripts < 5',
    'lighthouse': 'Performance score ≥ 90, Accessibility ≥ 90',
    'cwv': 'LCP < 2.5s, FID < 100ms, CLS < 0.1',
}

class BudgetEnforcer:
    """Enforce performance budgets in CI/CD."""
    def __init__(self, budgets: Dict):
        self.budgets = budgets
        self.results = {}
    
    def check_budget(self, metric: str, value: float) -> bool:
        budget = self.budgets.get(metric)
        if not budget: return True
        if isinstance(budget, dict):
            return all(self.check_budget(k, value) for k, v in budget.items())
        return value <= budget
    
    def report(self) -> str:
        passed = sum(1 for r in self.results.values() if r)
        total = len(self.results)
        return f"Budget check: {passed}/{total} passed"
```

## Verification Checklist

- [ ] Performance budget defined for time, size, and Core Web Vitals
- [ ] Budget enforced in CI/CD (fail build on budget exceed)
- [ ] Lighthouse scores tracked over time
- [ ] Real User Monitoring (RUM) for Core Web Vitals
- [ ] Bundle size monitoring per entry point
- [ ] Third-party script impact measured and budgeted
- [ ] Performance regression alerts configured
