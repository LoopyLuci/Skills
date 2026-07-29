---
name: product-analytics-instrumentation
description: "Use when implementing product analytics and user tracking."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [product-analytics, user-tracking, events, funnel, retention, cohorts, AARRR]
    related_skills: [website-analytics-tracking, saas-metrics-reporting, business-metrics-kpis, customer-feedback-surveys]
---

# Product Analytics and Instrumentation

Implementing product analytics — from event tracking and funnel analysis through retention cohorts, AARRR metrics, and data-informed product decisions.

## When to Use

- Setting up product analytics (Amplitude, Mixpanel, PostHog, Heap)
- Defining and tracking key product events
- Building funnel and retention analyses
- Measuring product-led growth metrics (AARRR)
- Making data-informed product decisions

## Analytics Framework (AARRR)

```python
AARRR_METRICS = {
    'acquisition': {
        'metrics': ['Signups', 'Signup conversion rate', 'Traffic by source', 'CAC'],
        'events': ['Page Viewed', 'Signup Started', 'Signup Completed'],
    },
    'activation': {
        'metrics': ['Activation rate', 'Time to activation', '% completed setup'],
        'events': ['Onboarding Step 1', 'Onboarding Complete', 'First Core Action'],
    },
    'retention': {
        'metrics': ['D1/D7/D30 retention', 'DAU/MAU', 'Session frequency'],
        'events': ['App Opened', 'Session Started', 'Feature Used'],
    },
    'revenue': {
        'metrics': ['MRR', 'ARPU', 'Conversion rate', 'Expansion revenue'],
        'events': ['Subscription Started', 'Payment Completed', 'Plan Upgraded'],
    },
    'referral': {
        'metrics': ['Viral coefficient', 'Referrals per user', 'Invite acceptance rate'],
        'events': ['Referral Sent', 'Referral Opened', 'Referral Converted'],
    },
}
```

## Event Tracking Plan

```python
from typing import Dict, List, Optional
from datetime import datetime

class EventTrackingPlan:
    """Define and manage product event tracking."""
    
    def __init__(self, product: str):
        self.product = product
        self.events = {}
        self.user_properties = {}
        self.funnels = []
    
    def add_event(self, name: str, category: str, 
                  description: str, properties: List[Dict],
                  trigger: str = 'user_action') -> 'EventTrackingPlan':
        self.events[name] = {
            'name': name, 'category': category,
            'description': description, 'properties': properties,
            'trigger': trigger,  # user_action, system, page_view
            'status': 'planned',
        }
        return self
    
    def add_funnel(self, name: str, steps: List[str], 
                   conversion_goal: str) -> 'EventTrackingPlan':
        self.funnels.append({
            'name': name, 'steps': steps,
            'conversion_goal': conversion_goal,
        })
        return self
    
    def generate_tracking_spec(self) -> str:
        spec = f"📊 Event Tracking Plan: {self.product}\n" + "=" * 50 + "\n"
        
        for event_name, event in self.events.items():
            spec += f"\n**{event_name}** ({event['category']})\n"
            spec += f"  Description: {event['description']}\n"
            spec += f"  Trigger: {event['trigger']}\n"
            for prop in event['properties']:
                spec += f"  Property: {prop.get('name')} ({prop.get('type', 'string')})\n"
        
        if self.funnels:
            spec += "\n**Funnels:**\n"
            for funnel in self.funnels:
                spec += f"\n  {funnel['name']}:"
                for i, step in enumerate(funnel['steps'], 1):
                    spec += f"\n    {i}. {step}"
        
        return spec
```

## Funnel Analysis

```python
class FunnelAnalyzer:
    """Analyze conversion funnels and find drop-off."""
    
    @staticmethod
    def analyze(funnel_steps: List[str], event_data: Dict) -> Dict:
        results = []
        prev_count = None
        
        for step in funnel_steps:
            count = len(event_data.get(step, []))
            if prev_count is not None:
                conversion = round(count / max(prev_count, 1) * 100, 1)
                dropoff = round((1 - count / max(prev_count, 1)) * 100, 1)
            else:
                conversion = 100.0
                dropoff = 0.0
            
            results.append({
                'step': step,
                'users': count,
                'conversion_from_previous': conversion,
                'dropoff_from_previous': dropoff,
            })
            prev_count = count
        
        return {
            'funnel': results,
            'overall_conversion': round(results[-1]['users'] / max(results[0]['users'], 1) * 100, 1) if len(results) > 1 else 100,
            'critical_dropoffs': [r for r in results if r['dropoff_from_previous'] > 30],
        }
```

## Common Pitfalls

1. **Tracking everything** — more events ≠ better insights; track what drives decisions
2. **No event taxonomy** — same event named differently on web vs mobile causes data mess
3. **Self-serve analytics not adopted** — if product team can't query data, they won't use it
4. **Data quality issues** — missing events, duplicate events, wrong properties
5. **Vanity metrics focus** — tracking page views instead of activation and retention
6. **No instrumentation review** — events drift as product changes; audit quarterly

## Verification Checklist

- [ ] Event tracking plan documents all key events
- [ ] AARRR metrics defined and tracked
- [ ] Key funnels identified and instrumented
- [ ] User properties captured for segmentation
- [ ] Data quality monitoring in place (event volume, missing props)
- [ ] Product team has self-serve analytics access
- [ ] Event naming convention documented
- [ ] Quarterly event audit scheduled

## See Also

- website-analytics-tracking — marketing analytics complement
- saas-metrics-reporting — revenue metrics from product data
- business-metrics-kpis — product KPIs
- customer-feedback-surveys — qualitative complement to quantitative
