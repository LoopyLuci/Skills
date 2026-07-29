---
name: saas-metrics-reporting
description: "Use when tracking and reporting SaaS business metrics."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [saas, metrics, mrr, churn, LTV, CAC, subscription, reporting, board-deck]
    related_skills: [business-metrics-kpis, crm-sales-pipeline, customer-success-retention, digital-marketing-strategy]
---

# SaaS Metrics and Reporting

Tracking, analyzing, and reporting SaaS business metrics — from recurring revenue and churn through unit economics, cohort analysis, and board reporting.

## When to Use

- Building a SaaS metrics dashboard
- Preparing board decks and investor updates
- Analyzing subscription revenue and churn
- Calculating unit economics (LTV, CAC, payback)
- Running cohort analysis for retention

## Core SaaS Metrics

```python
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

class SaaS_Metrics:
    """Core SaaS metric calculations."""
    
    @staticmethod
    def calculate_mrr(subscriptions: List[Dict]) -> Dict:
        """Calculate Monthly Recurring Revenue."""
        new_mrr = 0
        churn_mrr = 0
        expansion_mrr = 0
        contraction_mrr = 0
        
        for sub in subscriptions:
            if sub.get('type') == 'new':
                new_mrr += sub['amount']
            elif sub.get('type') == 'churn':
                churn_mrr += sub['amount']
            elif sub.get('type') == 'upgrade':
                expansion_mrr += sub.get('delta', sub['amount'])
            elif sub.get('type') == 'downgrade':
                contraction_mrr += abs(sub.get('delta', sub['amount']))
        
        net_new_mrr = new_mrr + expansion_mrr - churn_mrr - contraction_mrr
        
        return {
            'new_mrr': new_mrr,
            'churn_mrr': churn_mrr,
            'expansion_mrr': expansion_mrr,
            'contraction_mrr': contraction_mrr,
            'net_new_mrr': net_new_mrr,
        }
    
    @staticmethod
    def churn_rates(customers: List[Dict], period_days: int = 30) -> Dict:
        """Calculate logo and revenue churn."""
        start_count = len(customers)
        start_mrr = sum(c.get('mrr', 0) for c in customers)
        
        churned = [c for c in customers if c.get('churned_in_period', False)]
        churn_count = len(churned)
        churn_mrr = sum(c.get('mrr', 0) for c in churned)
        
        logo_churn = churn_count / max(start_count, 1) * 100
        revenue_churn = churn_mrr / max(start_mrr, 1) * 100
        
        return {
            'logo_churn_rate': round(logo_churn, 2),
            'revenue_churn_rate': round(revenue_churn, 2),
            'logo_churn_count': churn_count,
            'revenue_churn_amount': churn_mrr,
            'annualized_logo_churn': round((1 - (1 - logo_churn/100) ** (365/period_days)) * 100, 2),
        }
    
    @staticmethod
    def unit_economics(cac_data: Dict, ltv_data: Dict) -> Dict:
        """Calculate unit economics."""
        cac = cac_data.get('total_sales_marketing_spend', 0) / max(cac_data.get('new_customers', 1), 1)
        
        avg_revenue_per_user = ltv_data.get('avg_monthly_revenue', 0)
        gross_margin = ltv_data.get('gross_margin_pct', 0.7)
        churn_rate = ltv_data.get('monthly_churn_rate', 0.05)
        
        # LTV = ARPU * Gross Margin / Monthly Churn
        ltv = (avg_revenue_per_user * gross_margin) / max(churn_rate, 0.01)
        ltv_cac = ltv / max(cac, 1)
        
        # Payback period = CAC / (ARPU * Gross Margin)
        monthly_contribution = avg_revenue_per_user * gross_margin
        payback_months = cac / max(monthly_contribution, 1)
        
        return {
            'cac': round(cac, 2),
            'ltv': round(ltv, 2),
            'ltv_cac_ratio': round(ltv_cac, 2),
            'payback_months': round(payback_months, 1),
            'health': 'Excellent' if ltv_cac >= 5 else 'Good' if ltv_cac >= 3 else 'Needs improvement' if ltv_cac >= 1 else 'Unhealthy',
        }
```

## Cohort Analysis

```python
class CohortAnalyzer:
    """Run retention cohort analysis."""
    
    @staticmethod
    def retention_cohorts(subscriptions: List[Dict]) -> Dict:
        """Calculate retention by monthly cohorts."""
        cohorts = defaultdict(lambda: {'total': 0, 'periods': {}})
        
        for sub in subscriptions:
            cohort_key = sub.get('signup_month', 'unknown')
            period = sub.get('month_since_signup', 0)
            
            cohorts[cohort_key]['total'] += 1
            if period not in cohorts[cohort_key]['periods']:
                cohorts[cohort_key]['periods'][period] = 0
            cohorts[cohort_key]['periods'][period] += 1
        
        # Convert to retention percentages
        cohort_table = {}
        for month, data in sorted(cohorts.items()):
            total = data['total']
            rates = {}
            for period in sorted(data['periods'].keys()):
                rates[period] = round(data['periods'][period] / max(total, 1) * 100, 1)
            cohort_table[month] = rates
        
        return cohort_table
```

## Board Deck Generator

```python
def generate_board_slide(metrics: Dict) -> str:
    """Generate a board update slide for a key metric."""
    slide = "📊 KPI: " + metrics.get('title', 'Metric') + "\n"
    slide += "=" * 40 + "\n"
    slide += f"Current: {metrics.get('current', 'N/A')}\n"
    slide += f"Previous: {metrics.get('previous', 'N/A')}\n"
    change = metrics.get('change_pct', 0)
    arrow = "▲" if change > 0 else "▼" if change < 0 else "→"
    slide += f"Change: {arrow} {abs(change)}%\n"
    slide += f"Target: {metrics.get('target', 'N/A')}\n"
    slide += f"Status: {'✅ On track' if metrics.get('on_track', False) else '⚠️ Needs attention'}\n"
    slide += f"\n{metrics.get('commentary', '')}"
    return slide
```

## Common Pitfalls

1. **Ignoring contraction MRR** — expansions hide downgrades; track both
2. **Gross vs net revenue retention** — gross retention is what matters; net can be misleading
3. **Cohort analysis not segmented** — aggregate retention hides different behaviors by segment
4. **CAC payback period too long** — >18 months payback is risky for VC-backed SaaS
5. **nrr vs grr confusion** — Net Revenue Retention includes upsells; Gross does not
6. **Not using SaaS benchmarks** — a metric in isolation is meaningless; compare by stage and industry

## Verification Checklist

- [ ] MRR tracked (new, churn, expansion, contraction)
- [ ] Logo and revenue churn rates calculated
- [ ] LTV and CAC calculated with clear definitions
- [ ] LTV:CAC ratio ≥ 3
- [ ] Monthly cohort retention analyzed
- [ ] Board deck template with standard SaaS metrics
- [ ] SaaS benchmarks comparison
- [ ] Dashboard automated (not manual spreadsheets)

## See Also

- business-metrics-kpis — general business KPI framework
- crm-sales-pipeline — pipeline-to-revenue metrics
- customer-success-retention — churn reduction strategies
- digital-marketing-strategy — CAC optimization
