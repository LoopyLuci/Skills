---
name: revenue-operations-revops
description: "Use when building revenue operations and processes."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [revenue-operations, revops, sales-ops, marketing-ops, CRM, process]
    related_skills: [crm-sales-pipeline, marketing-automation-workflows, business-metrics-kpis, sales-enablement-playbooks]
---

# Revenue Operations (RevOps)

Building revenue operations that align sales, marketing, and customer success — from data unification and process design through tech stack optimization and revenue analytics.

## When to Use

- Aligning sales, marketing, and CS under common revenue goals
- Cleaning up fragmented revenue tech stack
- Building revenue reporting and forecasting
- Improving lead-to-revenue conversion
- Reducing revenue leakage and process gaps

## RevOps Framework

```python
REVOPS_PILLARS = {
    'process': 'Define, document, and optimize revenue processes end-to-end',
    'data': 'Unify customer data across systems for a single source of truth',
    'technology': 'Optimize the revenue tech stack for efficiency and automation',
    'analytics': 'Measure, report, and forecast revenue performance accurately',
}

def revops_audit(processes: List[str], tools: List[str]) -> Dict:
    """Audit RevOps maturity."""
    score = 0
    findings = []
    
    if len(processes) >= 5: score += 25
    if len(set(tools)) <= 5: score += 25  # Fewer tools = more integrated
    if 'CRM' in str(tools): score += 15
    if 'MAP' in str(tools): score += 15  # Marketing Automation Platform
    
    return {
        'maturity_score': score,
        'level': 'optimized' if score >= 80 else 'defined' if score >= 50 else 'emerging',
    }
```

## Common Pitfalls

1. **Siloed data** — CRM, MAP, and CS tools not synced; unify records
2. **Lead scoring misalignment** — marketing and sales disagree on MQL definitions
3. **Manual processes** — spreadsheets instead of automation for quotes, approvals
4. **No attribution** — can't tell which channels drive revenue
5. **Tool sprawl** — 15+ tools that don't integrate; consolidate

## Verification Checklist

- [ ] Lead-to-revenue process documented end-to-end
- [ ] CRM, MAP, and CS platform data unified
- [ ] Lead scoring model aligned between sales and marketing
- [ ] Attribution model selected and implemented
- [ ] Forecasting process defined with stages, probability, velocity
- [ ] Revenue reporting automated (not manual spreadsheets)
