---
name: vendor-management-procurement
description: "Use when managing vendor relationships and procurement."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vendor-management, procurement, supplier, contract, RFP, vendor-evaluation]
    related_skills: [contract-management-basics, business-continuity-planning, financial-modeling-budgeting, legal-compliance-business]
---

# Vendor Management and Procurement

Managing vendor relationships and procurement processes — from vendor selection and RFPs through contract negotiations, performance monitoring, and vendor risk management.

## When to Use

- Selecting new vendors or evaluating existing ones
- Running an RFP (Request for Proposal) process
- Negotiating vendor contracts and pricing
- Monitoring vendor performance and SLAs
- Managing vendor risk and compliance

## Procurement Process

```python
PROCUREMENT_PHASES = {
    'requirements': 'Define needs, scope, budget, timeline',
    'evaluation': 'Market research, RFP, vendor scoring, demos',
    'selection': 'Shortlist, negotiate terms, reference checks',
    'onboarding': 'Contract signature, system setup, data migration',
    'monitoring': 'Service levels, performance reviews, renewals',
    'offboarding': 'Contract end, data export, decommission',
}

class VendorScoring:
    """Score and compare vendors in an evaluation."""
    
    CRITERIA = ['Feature Fit', 'Cost', 'Support', 'Security', 
                'Integration', 'Scalability', 'Vendor Stability']
    
    @staticmethod
    def score_vendors(vendors: List[Dict], weights: List[float] = None) -> List[Dict]:
        if not weights:
            weights = [0.25, 0.20, 0.15, 0.15, 0.10, 0.10, 0.05]
        
        for v in vendors:
            total = sum(v.get(c, 0) * w for c, w in zip(VendorScoring.CRITERIA, weights))
            v['Total Score'] = round(total, 1)
        
        return sorted(vendors, key=lambda v: v['Total Score'], reverse=True)
```

## Common Pitfalls

1. **No SLA** — agreeing to service without defined performance metrics and remedies
2. **Single point of failure** — one vendor for critical service; have backup/exit plan
3. **License management** — paying for seats you don't use; audit usage quarterly
4. **Auto-renewal surprises** — contracts with auto-renewal clauses; set calendar reminders
5. **Vendor lock-in** — proprietary data formats make switching expensive; negotiate data portability

## Verification Checklist

- [ ] Requirements documented before vendor search
- [ ] RFP process with evaluation criteria and scoring
- [ ] Reference checks with current vendor customers
- [ ] Contract with clear SLAs and remedy terms
- [ ] Data portability/export clause in contract
- [ ] Vendor performance reviewed quarterly
- [ ] License usage audited quarterly (eliminate waste)
- [ ] Auto-renewal alerts set 60+ days before renewal
- [ ] Vendor risk assessment (financial health, security practices)
