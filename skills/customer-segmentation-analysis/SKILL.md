---
name: customer-segmentation-analysis
description: "Use when segmenting customers and analyzing behavior."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [segmentation, customer-analysis, cohorts, RFM, personas, targeting]
    related_skills: [crm-sales-pipeline, email-marketing-campaigns, digital-marketing-strategy, business-metrics-kpis]
---

# Customer Segmentation and Analysis

Segmenting customers into meaningful groups for targeted marketing, personalized experiences, and product decisions — from demographic and behavioral segmentation through RFM analysis and persona development.

## When to Use

- Dividing customers into groups for targeted campaigns
- Building customer personas for product and marketing decisions
- Analyzing customer behavior patterns and purchase history
- Implementing RFM (Recency, Frequency, Monetary) analysis
- Identifying high-value segments for retention

## Segmentation Methods

```python
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import Counter
import json

class CustomerSegmentation:
    """Segment customers using multiple methodologies."""
    
    @staticmethod
    def demographic( customers: List[Dict]) -> Dict[str, List]:
        """Segment by demographic attributes."""
        segments = {}
        
        for c in customers:
            # Age group
            age = c.get('age', 0)
            if age < 25: group = '18-24'
            elif age < 35: group = '25-34'
            elif age < 45: group = '35-44'
            elif age < 55: group = '45-54'
            else: group = '55+'
            segments.setdefault(f'age_{group}', []).append(c)
            
            # Location
            region = c.get('region', 'unknown')
            segments.setdefault(f'region_{region}', []).append(c)
        
        # Summary
        return {
            group: len(members) 
            for group, members in segments.items()
        }
    
    @staticmethod
    def behavioral( customers: List[Dict]) -> Dict:
        """Segment by purchase behavior."""
        segments = {
            'high_value': [],
            'frequent': [],
            'at_risk': [],
            'new': [],
            'one_time': [],
        }
        
        for c in customers:
            total_spent = c.get('total_spent', 0)
            order_count = c.get('order_count', 0)
            days_since_last = c.get('days_since_last_purchase', 999)
            account_age_days = c.get('account_age_days', 0)
            
            if total_spent > 1000 and order_count > 5:
                segments['high_value'].append(c)
            elif order_count > 10:
                segments['frequent'].append(c)
            elif days_since_last > 90 and order_count > 0:
                segments['at_risk'].append(c)
            elif account_age_days < 30:
                segments['new'].append(c)
            elif order_count == 1:
                segments['one_time'].append(c)
        
        return {k: len(v) for k, v in segments.items()}
    
    @staticmethod
    def lifecycle_stage( customers: List[Dict]) -> Dict:
        """Segment by customer lifecycle stage."""
        stages = {
            'exploration': 'First 30 days, exploring products',
            'active': 'Regular purchasers, engaged',
            'loyal': 'High repeat rate, brand advocates',
            'declining': 'Decreasing engagement, fewer purchases',
            'churned': 'No purchase in 90+ days',
            'reactivated': 'Returned after dormant period',
        }
        
        result = {}
        for c in customers:
            days_since_last = c.get('days_since_last_purchase', 999)
            order_count = c.get('order_count', 0)
            account_age = c.get('account_age_days', 0)
            
            if days_since_last > 90 and order_count > 0:
                stage = 'churned'
            elif account_age < 30:
                stage = 'exploration'
            elif order_count > 5:
                stage = 'loyal'
            elif order_count > 1:
                stage = 'active'
            else:
                stage = 'declining'
            
            result[stage] = result.get(stage, 0) + 1
        
        return {'stages': result, 'definitions': stages}
```

## RFM Analysis

```python
class RFMAnalyzer:
    """Recency, Frequency, Monetary analysis for customer segmentation."""
    
    @staticmethod
    def analyze(customers: List[Dict]) -> List[Dict]:
        """Perform RFM analysis and assign scores (1-5)."""
        now = datetime.now()
        
        # Calculate raw RFM values
        rfm_data = []
        for c in customers:
            last_purchase = datetime.fromisoformat(c.get('last_purchase_date', now.isoformat()))
            recency = (now - last_purchase).days
            frequency = c.get('order_count', 0)
            monetary = c.get('total_spent', 0)
            rfm_data.append({'id': c.get('id'), 'recency': recency, 
                           'frequency': frequency, 'monetary': monetary})
        
        # Score each dimension (1-5, where 5 is best)
        for dim in ['recency', 'frequency', 'monetary']:
            values = sorted([d[dim] for d in rfm_data])
            # Lower recency is better; higher frequency/monetary is better
            reverse = dim != 'recency'
            
            for d in rfm_data:
                percentile = sum(1 for v in values if (v <= d[dim]) != reverse) / max(len(values), 1)
                d[f'{dim}_score'] = min(5, max(1, round(percentile * 5)))
        
        # Assign segments
        for d in rfm_data:
            r = d['recency_score']
            f = d['frequency_score']
            m = d['monetary_score']
            
            if r >= 4 and f >= 4 and m >= 4:
                d['segment'] = 'Champions'
            elif r >= 4 and f >= 3 and m >= 3:
                d['segment'] = 'Loyal Customers'
            elif r >= 3 and f >= 2 and m >= 2:
                d['segment'] = 'Potential Loyalists'
            elif r >= 4 and f <= 2:
                d['segment'] = 'New Customers'
            elif r <= 2 and f >= 3 and m >= 3:
                d['segment'] = 'At Risk'
            elif r <= 2 and f >= 4 and m >= 4:
                d['segment'] = 'Cannot Lose'
            elif r <= 2 and f <= 2:
                d['segment'] = 'Hibernating'
            else:
                d['segment'] = 'Needs Attention'
        
        return rfm_data
    
    @staticmethod
    def segment_breakdown(rfm_results: List[Dict]) -> Dict:
        """Get summary of RFM segments."""
        from collections import Counter
        segments = Counter(d['segment'] for d in rfm_results)
        return dict(segments.most_common())
```

## Persona Builder

```python
class PersonaBuilder:
    """Build detailed customer personas from data."""
    
    @staticmethod
    def create_from_data(customers: List[Dict], segment_name: str) -> Dict:
        """Create a persona representing a customer segment."""
        if not customers:
            return {'name': segment_name, 'count': 0}
        
        avg_age = sum(c.get('age', 30) for c in customers) / len(customers)
        top_regions = Counter(c.get('region', 'Unknown') for c in customers).most_common(3)
        avg_spend = sum(c.get('total_spent', 0) for c in customers) / len(customers)
        common_sources = Counter(c.get('acquisition_source', '') for c in customers 
                               if c.get('acquisition_source')).most_common(2)
        
        return {
            'name': segment_name,
            'count': len(customers),
            'demographics': {
                'avg_age': round(avg_age, 0),
                'top_regions': [r[0] for r in top_regions],
                'gender_split': 'Varies',
            },
            'behavior': {
                'avg_lifetime_value': round(avg_spend, 2),
                'avg_orders': round(sum(c.get('order_count', 0) for c in customers) / len(customers), 1),
                'top_acquisition_sources': [s[0] for s in common_sources],
            },
            'needs': [
                'Reliable customer support',
                'Competitive pricing',
                'Fast delivery/shipping',
            ],
            'marketing_channel_preferences': ['Email', 'Social Media'],
        }
```

## Common Pitfalls

1. **Too many segments** — 3-5 actionable segments beat 20 that can't be targeted; consolidate
2. **Static segments** — customer behavior changes; update segments quarterly
3. **Not linking to action** — segments without targeting strategies are academic exercises
4. **Over-relying on demographics** — behavioral segments predict future behavior better than demographics
5. **Small sample segments** — segments with <100 customers aren't statistically reliable

## Verification Checklist

- [ ] At least 3 segmentation methods applied (demographic, behavioral, RFM)
- [ ] Segments are mutually exclusive (no customer in multiple segments)
- [ ] Each segment has a clear targeting strategy
- [ ] RFM analysis completed with 1-5 scoring
- [ ] Persona document created for top 3 segments
- [ ] Segment size large enough to be actionable
- [ ] Segmentation updated at least quarterly

## See Also

- crm-sales-pipeline — acting on segments in sales
- email-marketing-campaigns — targeting segments by email
- digital-marketing-strategy — segment-based channel selection
- business-metrics-kpis — measuring segment performance
