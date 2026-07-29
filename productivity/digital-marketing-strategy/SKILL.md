---
name: digital-marketing-strategy
description: "Use when creating digital marketing strategies and plans."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [marketing-strategy, digital-marketing, growth, planning, channels, budget]
    related_skills: [seo-search-engine-optimization, email-marketing-campaigns, social-media-content-planning, conversion-rate-optimization]
---

# Digital Marketing Strategy

Creating comprehensive digital marketing strategies — from market research and channel selection through budget planning, execution roadmaps, and performance measurement.

## When to Use

- Building a marketing strategy for a new business or product launch
- Planning annual/quarterly marketing activities and budgets
- Selecting and prioritizing marketing channels
- Setting KPIs and measuring marketing ROI

## Strategy Framework

```
Audit → Objectives → Audience → Channels → Budget → Roadmap → Execute → Measure → Iterate
```

## Marketing Channel Planner

```python
from typing import Dict, List

class ChannelPlanner:
    """Evaluate and plan marketing channel mix."""
    
    CHANNEL_PROFILES = {
        'seo': {'cost': 'medium', 'time_to_results': '3-6 months', 'scalability': 'high'},
        'ppc': {'cost': 'high', 'time_to_results': 'immediate', 'scalability': 'very_high'},
        'social_organic': {'cost': 'low', 'time_to_results': '1-3 months', 'scalability': 'medium'},
        'social_paid': {'cost': 'medium', 'time_to_results': 'immediate', 'scalability': 'high'},
        'email': {'cost': 'low', 'time_to_results': '1-2 months', 'scalability': 'high'},
        'content': {'cost': 'medium', 'time_to_results': '2-4 months', 'scalability': 'high'},
        'influencer': {'cost': 'medium', 'time_to_results': '1-3 months', 'scalability': 'medium'},
        'affiliate': {'cost': 'low', 'time_to_results': '2-4 months', 'scalability': 'high'},
    }
    
    @staticmethod
    def suggest_channels(business_type: str, goals: List[str]) -> List[str]:
        recommended = []
        if 'brand_awareness' in goals or business_type in ('ecommerce', 'b2c'):
            recommended.extend(['social_organic', 'social_paid', 'influencer'])
        if 'leads' in goals or business_type in ('b2b', 'saas', 'consulting'):
            recommended.extend(['seo', 'content', 'email', 'ppc'])
        if 'retention' in goals:
            recommended.extend(['email'])
        return list(dict.fromkeys(recommended))[:5]
```

## Budget Allocation

```python
class BudgetAllocator:
    @staticmethod
    def allocate(total_budget: float, channels: List[str], stage: str = 'growth') -> Dict[str, float]:
        strategies = {
            'launch': {'ppc': 0.35, 'social_paid': 0.25, 'influencer': 0.15, 'content': 0.10, 'seo': 0.05, 'email': 0.05, 'affiliate': 0.05},
            'growth': {'seo': 0.20, 'ppc': 0.20, 'content': 0.15, 'social_paid': 0.15, 'email': 0.10, 'affiliate': 0.10, 'influencer': 0.10},
            'mature': {'email': 0.25, 'seo': 0.25, 'content': 0.20, 'ppc': 0.10, 'affiliate': 0.10, 'social_paid': 0.10},
        }
        strategy = strategies.get(stage, strategies['growth'])
        allocations = {c: round(total_budget * strategy[c], 2) for c in channels if c in strategy}
        allocated = sum(allocations.values())
        if allocated > 0:
            factor = total_budget / allocated
            allocations = {k: round(v * factor, 2) for k, v in allocations.items()}
        return allocations
```

## KPI Report

```python
KPI_LIBRARY = {
    'awareness': ['Website Traffic', 'Social Reach', 'Brand Mentions'],
    'acquisition': ['New Leads', 'Cost Per Lead', 'Email Subscribers'],
    'conversion': ['Conversion Rate', 'CAC', 'MQLs', 'SQLs'],
    'revenue': ['Marketing Revenue', 'ROAS', 'LTV', 'Deal Size'],
    'retention': ['Churn Rate', 'Retention Rate', 'NPS'],
}

def generate_report(kpi_data: Dict) -> str:
    report = "📈 Marketing Performance Report\n" + "=" * 40 + "\n"
    for category, kpis in KPI_LIBRARY.items():
        report += f"\n[{category.upper()}]\n"
        for kpi in kpis:
            val = kpi_data.get(kpi, 'N/A')
            tgt = kpi_data.get(f"{kpi}_target", 'N/A')
            status = '✅' if val != 'N/A' and tgt != 'N/A' and val >= tgt else '⚠️'
            report += f"  {status} {kpi}: {val} (Target: {tgt})\n"
    return report
```

## Common Pitfalls

1. **No clear goals** — marketing without SMART goals can't be measured
2. **Too many channels** — focus on 3-4 core channels; don't spread thin
3. **Ignoring customer lifecycle** — balance acquisition and retention spend
4. **No testing** — assume strategies work without validation
5. **Set-and-forget** — review and adjust strategy quarterly

## Verification Checklist

- [ ] SMART marketing goals defined
- [ ] Target audience personas documented
- [ ] Channel mix selected based on goals and budget
- [ ] Budget allocated with 10-20% for testing
- [ ] KPI dashboard with targets
- [ ] Attribution model chosen
- [ ] Quarterly review cadence established

## See Also

- seo-search-engine-optimization — organic channel strategy
- email-marketing-campaigns — email strategy
- social-media-content-planning — social media strategy
- conversion-rate-optimization — optimizing performance
- content-writing-seo-copy — content marketing execution
