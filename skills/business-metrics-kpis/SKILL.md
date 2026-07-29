---
name: business-metrics-kpis
description: "Use when defining and tracking business metrics and KPIs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [kpis, metrics, dashboards, business-intelligence, reporting, OKRs]
    related_skills: [crm-sales-pipeline, digital-marketing-strategy, website-analytics-tracking, conversion-rate-optimization]
---

# Business Metrics and KPIs

Defining, tracking, and analyzing key business metrics and KPIs — from financial metrics through marketing, sales, product, and customer success KPIs.

## When to Use

- Defining KPIs for a new business or department
- Building executive dashboards and reports
- Setting OKRs and tracking progress
- Analyzing business performance across functions
- Making data-driven decisions based on metrics

## KPI Framework

```
Input Metrics (leading) → Process Metrics → Output Metrics (lagging)
     (activities)           (quality)           (results)
```

## Metric Definitions by Department

```python
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class KPIEngine:
    """Define and track metrics across departments."""
    
    METRICS_LIBRARY = {
        'revenue': {
            'MRR': 'Monthly Recurring Revenue',
            'ARR': 'Annual Run Rate (MRR × 12)',
            'ARPU': 'Average Revenue Per User',
            'LTV': 'Customer Lifetime Value',
            'Gross_Margin': 'Revenue - COGS / Revenue',
        },
        'growth': {
            'CAC': 'Customer Acquisition Cost',
            'LTV_CAC': 'LTV to CAC Ratio (>3 is healthy)',
            'Payback_Period': 'Months to recover CAC',
            'Net_Revenue_Retention': 'Revenue retention including expansions',
        },
        'sales': {
            'Pipeline_Value': 'Total value of open deals',
            'Win_Rate': 'Deals won / deals closed',
            'Sales_Cycle': 'Average days from lead to close',
            'Quota_Attainment': '% of reps hitting quota',
        },
        'marketing': {
            'MQLs': 'Marketing Qualified Leads',
            'SQLs': 'Sales Qualified Leads',
            'MQL_to_SQL': 'Conversion rate from MQL to SQL',
            'CPL': 'Cost Per Lead',
            'ROAS': 'Return on Ad Spend',
            'Organic_Traffic': 'SEO-driven website traffic',
        },
        'product': {
            'DAU_MAU': 'Daily active / monthly active users',
            'Retention_Rate': '% users returning after N days',
            'Feature_Adoption': '% users using a feature',
            'NPS': 'Net Promoter Score',
            'Churn_Rate': '% customers lost per period',
        },
        'customer_success': {
            'Churn': 'Customer churn rate',
            'Expansion_MRR': 'Revenue from upsells/cross-sells',
            'Health_Score': 'Composite customer health metric',
            'CSAT': 'Customer satisfaction score',
            'First_Response_Time': 'Avg time to respond to support',
        },
    }
    
    @staticmethod
    def define_okr(objective: str, key_results: List[Dict]) -> Dict:
        """Define OKR (Objectives and Key Results)."""
        return {
            'objective': objective,
            'key_results': [
                {
                    'kr': kr.get('name', ''),
                    'current_value': kr.get('current', 0),
                    'target_value': kr.get('target', 100),
                    'progress_pct': round((kr.get('current', 0) / max(kr.get('target', 1), 1)) * 100, 1),
                    'owner': kr.get('owner', ''),
                }
                for kr in key_results
            ],
            'confidence': 7,  # 1-10 scale
            'quarter': f"Q{(datetime.now().month - 1) // 3 + 1} {datetime.now().year}",
        }
```

## Dashboard Builder

```python
class DashboardBuilder:
    """Build business dashboards with metrics from multiple sources."""
    
    DASHBOARD_TEMPLATES = {
        'executive': {
            'title': 'Executive Dashboard',
            'sections': [
                {
                    'name': 'Revenue',
                    'metrics': ['MRR', 'ARR', 'LTV', 'CAC', 'Gross_Margin'],
                    'visuals': ['big_number', 'trend_line'],
                },
                {
                    'name': 'Growth',
                    'metrics': ['New Customers', 'Churn Rate', 'Net Revenue Retention'],
                    'visuals': ['trend_line', 'bar_chart'],
                },
                {
                    'name': 'Sales',
                    'metrics': ['Pipeline Value', 'Win Rate', 'Sales Cycle'],
                    'visuals': ['gauge', 'funnel'],
                },
            ],
        },
        'marketing': {
            'title': 'Marketing Dashboard',
            'sections': [
                {
                    'name': 'Traffic & Leads',
                    'metrics': ['Website Traffic', 'MQLs', 'SQLs', 'SQL to Revenue'],
                    'visuals': ['trend_line', 'funnel'],
                },
                {
                    'name': 'Channel Performance',
                    'metrics': ['ROAS', 'CPL', 'CPA', 'Conversion Rate'],
                    'visuals': ['bar_chart'],
                },
            ],
        },
        'product': {
            'title': 'Product Dashboard',
            'sections': [
                {
                    'name': 'Engagement',
                    'metrics': ['DAU/MAU', 'Retention Rate', 'Session Duration'],
                    'visuals': ['trend_line', 'cohort'],
                },
                {
                    'name': 'Health',
                    'metrics': ['NPS', 'CSAT', 'Churn', 'Feature Adoption'],
                    'visuals': ['gauge', 'bar_chart'],
                },
            ],
        },
    }
    
    @staticmethod
    def build_dashboard(template_name: str = 'executive') -> Dict:
        """Build a dashboard from a template."""
        template = DashboardBuilder.DASHBOARD_TEMPLATES.get(template_name, 
                   DashboardBuilder.DASHBOARD_TEMPLATES['executive'])
        
        dashboard = {
            'title': template['title'],
            'last_updated': datetime.now().isoformat(),
            'sections': [],
        }
        
        for section in template['sections']:
            metrics_data = []
            for metric in section['metrics']:
                # Look up metric definition
                for dept, metrics in KPIEngine.METRICS_LIBRARY.items():
                    if metric in metrics:
                        metrics_data.append({
                            'name': metric,
                            'description': metrics[metric],
                            'current_value': None,
                            'previous_value': None,
                            'change_pct': None,
                            'status': 'pending',
                        })
            
            dashboard['sections'].append({
                'name': section['name'],
                'metrics': metrics_data,
                'visuals': section['visuals'],
            })
        
        return dashboard
```

## Metric Health Check

```python
class MetricHealth:
    """Check metric health against targets and benchmarks."""
    
    @staticmethod
    def check(metric_name: str, current_value: float, 
              target_value: float, benchmark: float = None) -> Dict:
        """Evaluate metric health."""
        pct_of_target = round(current_value / max(target_value, 1) * 100, 1)
        
        if target_value > 0:  # Higher is better
            status = '✅ On track' if current_value >= target_value else '⚠️ Below target'
        else:  # Lower is better (churn, cost)
            status = '✅ On track' if current_value <= abs(target_value) else '⚠️ Above target'
        
        result = {
            'metric': metric_name,
            'current': current_value,
            'target': target_value,
            'progress_pct': pct_of_target,
            'status': status,
        }
        
        if benchmark:
            vs_benchmark = round((current_value - benchmark) / benchmark * 100, 1)
            result['benchmark'] = benchmark
            result['vs_benchmark_pct'] = vs_benchmark
            result['benchmark_status'] = 'Above' if vs_benchmark > 0 else 'Below'
        
        return result
    
    @staticmethod
    def health_score(metrics: List[Dict]) -> int:
        """Calculate composite business health score (0-100)."""
        if not metrics:
            return 0
        on_track = sum(1 for m in metrics if m.get('status', '').startswith('✅'))
        return round(on_track / len(metrics) * 100)
```

## Common Pitfalls

1. **Vanity metrics** — metrics that look good but don't drive decisions (page views, downloads); focus on actionable metrics
2. **Too many KPIs** — tracking 50 metrics dilutes focus; identify 5-7 "one metric that matters"
3. **Not benchmarking** — a metric in isolation means nothing; compare to industry, past periods, targets
4. **Confusing correlation with causation** — two metrics moving together doesn't mean one caused the other
5. **Manual reporting** — manually exported spreadsheets are slow and error-prone; automate dashboards
6. **Metric hoarding** — data without decisions is waste; each metric should have an associated action

## Verification Checklist

- [ ] North Star metric identified (one metric that matters most)
- [ ] 5-7 key KPIs defined per department
- [ ] Leading and lagging indicators balanced
- [ ] Targets set for each KPI (with benchmark data)
- [ ] Dashboard built and automated (no manual reporting)
- [ ] Monthly/quarterly review cadence established
- [ ] OKRs defined and aligned with KPIs
- [ ] Metric definitions documented (so everyone measures the same thing)
- [ ] Action triggers defined (what happens when a metric goes red)

## See Also

- crm-sales-pipeline — sales pipeline metrics
- digital-marketing-strategy — marketing ROI metrics
- website-analytics-tracking — website performance metrics
- conversion-rate-optimization — conversion metrics
