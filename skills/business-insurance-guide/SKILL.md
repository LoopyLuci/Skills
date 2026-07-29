---
name: business-insurance-guide
description: "Use when evaluating business insurance options."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [insurance, business-risk, liability, coverage, claims]
    related_skills: [business-continuity-planning, legal-compliance-business, financial-modeling-budgeting]
---

# Business Insurance Guide

Navigating business insurance — from general liability and professional liability through workers' comp, property insurance, cyber insurance, and claims management.

## When to Use

- Evaluating insurance needs for a new business
- Reviewing existing coverage for gaps
- Understanding policy types and terminology
- Filing and managing insurance claims

## Insurance Types

```python
INSURANCE_TYPES = {
    'general_liability': 'Covers third-party bodily injury, property damage, advertising injury',
    'professional_liability': 'Errors and omissions (E&O) — professional mistakes/negligence',
    'workers_comp': 'Employee injury/illness — required in most states',
    'property': 'Physical assets — office, equipment, inventory',
    'cyber': 'Data breaches, ransomware, privacy lawsuits, notification costs',
    'business_interruption': 'Lost income when operations are disrupted',
    'dando': 'Directors and officers — protects leadership from decisions',
}

def estimate_coverage(revenue: float, industry: str, employees: int) -> Dict:
    rates = {'tech': 0.005, 'healthcare': 0.015, 'construction': 0.025, 'retail': 0.008, 'consulting': 0.004}
    rate = rates.get(industry, 0.01)
    return {'general_liability': round(revenue * rate, 2), 'workers_comp': round(employees * 1200, 2)}
```

## Verification Checklist

- [ ] General liability in place ($1M+ coverage)
- [ ] Professional liability/E&O for service businesses
- [ ] Workers' comp if employees (check state requirements)
- [ ] Cyber insurance if handling customer data
- [ ] Property insurance for physical assets
- [ ] Policies reviewed annually
- [ ] Claims process documented
