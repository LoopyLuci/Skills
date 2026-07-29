---
name: financial-modeling-budgeting
description: "Use when building financial models and budgets."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [financial-modeling, budgeting, forecasting, P&L, cash-flow, scenario-planning]
    related_skills: [fundraising-investor-pitch, saas-metrics-reporting, business-metrics-kpis, cap-table-management]
---

# Financial Modeling and Budgeting

Building financial models and budgets — from P&L forecasting and cash flow modeling through scenario planning, unit economics, and board-ready reporting.

## When to Use

- Building annual budget and rolling forecasts
- Creating financial models for fundraising
- Analyzing unit economics and profitability
- Scenario planning (best/worst/base case)
- Managing cash flow and runway

## Model Structure

```python
class FinancialModel:
    """Three-statement financial model template."""
    def __init__(self, starting_cash: float, monthly_burn: float):
        self.cash = starting_cash
        self.burn = monthly_burn
        self.months = []
    
    def project(self, months: int = 12, revenue_growth: float = 0.05,
                expense_growth: float = 0.02) -> List[Dict]:
        projections = []
        for m in range(months):
            revenue = self._forecast_revenue(m, revenue_growth)
            expenses = self._forecast_expenses(m, expense_growth)
            net_income = revenue - expenses
            self.cash += net_income
            
            projections.append({
                'month': m + 1, 'revenue': revenue,
                'expenses': expenses, 'net_income': net_income,
                'cash_balance': self.cash, 'burn_rate': -net_income,
                'runway_months': self.cash / max(-net_income, 0.01) if net_income < 0 else 999,
            })
        return projections
    
    def _forecast_revenue(self, month: int, growth: float) -> float:
        """Simplified revenue forecast with growth rate."""
        base = 0
        return base * (1 + growth) ** month
    
    def _forecast_expenses(self, month: int, growth: float) -> float:
        return self.burn * (1 + growth) ** month
```

## Common Pitfalls

1. **Garbage in, garbage out** — model accuracy depends on assumptions; document them
2. **No scenario planning** — single forecast is always wrong; build best/worst/base
3. **Ignoring cash flow timing** — revenue recognized when invoiced, cash when received
4. **Not updating actuals** — models become quickly outdated; refresh monthly with actuals
5. **Too complex** — 50-tab spreadsheets nobody understands; keep it understandable

## Verification Checklist

- [ ] P&L, Balance Sheet, and Cash Flow statement projected
- [ ] Assumptions documented and versioned
- [ ] Scenario analysis (base, upside, downside)
- [ ] Monthly actual vs budget variance tracked
- [ ] Cash runway calculated (cash / monthly burn)
- [ ] Unit economics in model (CAC, LTV, gross margin)
- [ ] Model reviewed by finance/accounting team
