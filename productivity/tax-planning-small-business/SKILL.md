---
name: tax-planning-small-business
description: "Use when planning taxes for small businesses."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [tax-planning, small-business, deductions, entity-structure, quarterly-taxes]
    related_skills: [accounting-bookkeeping-basics, financial-modeling-budgeting, legal-compliance-business]
---

# Tax Planning for Small Business

Planning taxes for small businesses — from entity structure selection and quarterly estimated taxes through deductions, credits, and year-end strategies.

## When to Use

- Setting up tax structure for a new business
- Planning estimated quarterly tax payments
- Identifying deductible business expenses
- Preparing for tax filing season
- Choosing between LLC, S-Corp, and C-Corp

## Tax Considerations

```python
ENTITY_STRUCTURES = {
    'sole_prop': 'Simplest, self-employment tax on all income, personal liability',
    'llc': 'Flexible, pass-through taxation, liability protection',
    's_corp': 'Salary + distributions, self-employment tax savings, more compliance',
    'c_corp': 'Corporate tax rate, double taxation on dividends, best for investors',
}

COMMON_DEDUCTIONS = [
    'Home office (exclusive + regular use)',
    'Vehicle mileage (standard rate 65.5¢/mi for 2023)',
    'Health insurance premiums (self-employed)',
    'Retirement contributions (SEP IRA, Solo 401k)',
    'Software and subscriptions',
    'Professional services (legal, accounting)',
    'Business meals (50% deductible)',
    'Travel and lodging',
]

def estimate_quarterly_taxes(projected_income: float, entity: str) -> float:
    se_tax = projected_income * 0.153 * 0.5  # Employer portion
    income_tax = projected_income * 0.25  # Estimated rate
    return round((se_tax + income_tax) / 4, 2)
```

## Verification Checklist

- [ ] Entity structure chosen (LLC, S-Corp, C-Corp)
- [ ] EIN obtained
- [ ] Quarterly estimated taxes calculated and paid
- [ ] Business bank account separate from personal
- [ ] Receipts organized (digital + physical)
- [ ] CPA/tax advisor engaged for review
- [ ] Payroll set up if S-Corp or employees
- [ ] Sales tax registration (if applicable)
