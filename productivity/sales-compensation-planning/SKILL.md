---
name: sales-compensation-planning
description: "Use when designing sales compensation and commission plans."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sales-compensation, commissions, quotas, SPIFF, variable-pay, comp-plan]
    related_skills: [sales-enablement-playbooks, sales-forecasting-advanced, revenue-operations-revops, crm-sales-pipeline]
---

# Sales Compensation Planning

Designing sales compensation plans — from quota setting and commission structures through territory design, accelerators, clawbacks, and plan governance.

## When to Use

- Building or revising sales compensation plans
- Setting quotas for sales reps and teams
- Designing commission rates and accelerators
- Balancing base salary vs variable pay
- Managing comp plan administration

## Compensation Models

```python
COMP_MODELS = {
    'straight_commission': '100% variable, % of revenue closed',
    'base_plus_commission': 'Base salary + variable % on attainment',
    'tiered_commission': 'Increasing commission rate at higher attainment levels',
    'gross_margin': 'Commission based on deal profitability, not just revenue',
    'team_based': 'Mix of individual attainment and team/company performance',
}

class CompPlan:
    """Design and simulate sales compensation."""
    def __init__(self, base_salary: float, quota: float, 
                 commission_rate: float = 0.10):
        self.base = base_salary
        self.quota = quota
        self.commission = commission_rate
        self.accelerator = 0.15  # above quota rate
        self.clawback_days = 90
    
    def calculate_payout(self, closed_revenue: float) -> Dict:
        attainment = closed_revenue / self.quota
        variable = 0
        
        if closed_revenue <= self.quota:
            variable = closed_revenue * self.commission
        else:
            variable = (self.quota * self.commission + 
                       (closed_revenue - self.quota) * self.accelerator)
        
        return {
            'base': self.base / 12,
            'variable': round(variable, 2),
            'total': round(self.base / 12 + variable, 2),
            'attainment_pct': round(attainment * 100, 1),
        }
```

## Common Pitfalls

1. **Plan too complex** — reps can't calculate their own commission; keep it simple
2. **Changing plan mid-year** — erodes trust; only change for extreme circumstances
3. **No clawback policy** — deals that churn within 90 days should reverse commission
4. **Sandbagging** — closing deals slowly to make next quota easier; use accelerators
5. **No governance** — inconsistent application of comp rules causes legal exposure

## Verification Checklist

- [ ] Compensation model selected (base+commission, tiered, gross margin, etc.)
- [ ] Quotas aligned with company revenue targets (bottoms-up + top-down)
- [ ] Commission rates competitive for your market/industry
- [ ] Accelerators for above-quota performance
- [ ] Clawback policy for early churn
- [ ] Plan documentation written in plain language
- [ ] Comp plan administered in CRM (Salesforce, HubSpot)
- [ ] Plan reviewed quarterly for effectiveness
- [ ] Legal/compliance review for regulatory requirements
