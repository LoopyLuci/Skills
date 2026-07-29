---
name: fractional-executive-patterns
description: "Use when working as a fractional executive (CxO)."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [fractional-executive, CTO, CFO, CEO, part-time, consulting, leadership]
    related_skills: [venture-studio-startup-incubation, product-management-roadmap, business-metrics-kpis, financial-modeling-budgeting]
---

# Fractional Executive Patterns

Working as a fractional executive (CTO/CFO/CEO) — from engagement scoping and onboarding through value delivery, team building, and multi-client management.

## When to Use

- Taking on fractional CTO, CFO, or CEO roles
- Structuring fractional executive engagements
- Managing multiple clients effectively
- Building and scaling teams as a fractional leader
- Delivering strategic value on limited hours

## Fractional Framework

```python
FRACTIONAL_ROLES = {
    'fractional_cto': 'Tech strategy, architecture decisions, engineering hiring, vendor selection',
    'fractional_cfo': 'Financial modeling, fundraising prep, board reporting, cash management',
    'fractional_ceo': 'Strategic direction, fundraising, team building, board relations',
    'fractional_cmo': 'Marketing strategy, brand positioning, demand gen, team leadership',
}

class FractionalEngagement:
    """Structure a fractional executive engagement."""
    def __init__(self, role: str, client: str, hours_per_week: int = 10):
        self.role = role
        self.client = client
        self.hours = hours_per_week
        self.deliverables = []
        self.milestones = []
    
    def add_deliverable(self, name: str, estimated_hours: int, 
                         due_date: str, depends_on: List[str] = None):
        self.deliverables.append({
            'name': name, 'hours': estimated_hours,
            'due': due_date, 'deps': depends_on or [],
        })
    
    def utilization(self) -> float:
        booked = sum(d['hours'] for d in self.deliverables)
        return round(min(booked / (self.hours * 4), 1.0) * 100, 1)
```

## Verification Checklist

- [ ] Engagement letter/SOW defined (scope, hours, duration, termination)
- [ ] Onboarding plan (knowledge transfer, stakeholder intro, tools access)
- [ ] Weekly cadence established (1:1s, all-hands, board)
- [ ] Deliverables tracked with clear success criteria
- [ ] Multi-client time management (time blocking, async work)
- [ ] Handoff plan for when engagement ends
- [ ] Confidentiality and IP agreements in place
- [ ] Professional liability insurance (E&O)
