---
name: customer-onboarding-automation
description: "Use when designing automated customer onboarding flows."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [customer-onboarding, automation, user-activation, time-to-value, welcome-flow]
    related_skills: [customer-success-retention, email-marketing-campaigns, crm-sales-pipeline, marketing-automation-workflows]
---

# Customer Onboarding Automation

Designing automated customer onboarding experiences that drive activation, adoption, and time-to-value.

## When to Use

- Designing a customer onboarding flow for a SaaS product
- Automating welcome sequences and guided tours
- Measuring and improving time-to-value
- Reducing churn in the first 90 days
- Building product-led growth onboarding

## Onboarding Funnel

```
Sign Up → Activation → First Value → Habit → Expansion
   ↓          ↓            ↓          ↓        ↓
Welcome   Setup      First Success  Regular  Upgrade
Email     Complete    Milestone      Usage
```

## Onboarding Automation Engine

```python
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class OnboardingAutomation:
    """Design automated onboarding flows."""
    
    def __init__(self, product: str, ttv_target_days: int = 14):
        self.product = product
        self.ttv_target = ttv_target_days
        self.steps = []
        self.triggers = []
        self.templates = {}
    
    def add_step(self, name: str, delay_hours: int, 
                 action_type: str, config: Dict,
                 condition: str = None) -> 'OnboardingAutomation':
        self.steps.append({
            'id': len(self.steps) + 1,
            'name': name, 'delay': delay_hours,
            'action': action_type, 'config': config,
            'condition': condition,
        })
        return self
    
    def build_welcome_sequence(self, company_name: str) -> 'OnboardingAutomation':
        """Build standard welcome onboarding."""
        self.add_step('Welcome Email', 0, 'email', {
            'subject': f'Welcome to {company_name}!',
            'template': 'welcome',
            'goal': 'Deliver login info, set expectations',
        })
        self.add_step('Quick Start Guide', 24, 'email', {
            'subject': 'Your first 5 steps to get started',
            'template': 'quickstart',
            'goal': 'Drive first login and setup action',
        })
        self.add_step('Account Setup Call', 72, 'task', {
            'assign_to': 'customer_success',
            'priority': 'high',
            'goal': 'Schedule 30-min onboarding call',
        }, condition='not_started_setup')
        self.add_step('First Value Milestone', 168, 'check', {
            'milestone': 'completed_core_action',
            'goal': 'Ensure customer reaches first value milestone',
        })
        return self
    
    def generate_onboarding_timeline(self) -> str:
        timeline = f"🚀 {self.product} Onboarding ({self.ttv_target}d to value)\n"
        timeline += "=" * 50 + "\n"
        cumulative = 0
        for step in self.steps:
            cumulative += step['delay']
            days = cumulative // 24
            hours = cumulative % 24
            timeline += f"\n+{days}d {hours}h: {step['name']}"
            timeline += f"\n  → {step['config'].get('goal', '')}"
            if step['condition']:
                timeline += f"\n  ⚡ Only if: {step['condition']}"
        return timeline


# Standard Day-0-30 onboarding template
def standard_onboarding(product: str) -> OnboardingAutomation:
    o = OnboardingAutomation(product)
    o.add_step('Welcome & Login Instructions', 0, 'email', 
               {'subject': f'Welcome to {product}!', 'template': 'welcome'})
    o.add_step('Account Setup Guide', 2, 'email',
               {'template': 'setup_guide'})
    o.add_step('Success Call Reminder', 48, 'task',
               {'type': 'call', 'assignee': 'CS'}, 
               condition='has_not_booked_call')
    o.add_step('First Core Action Reminder', 72, 'in_app',
               {'message': 'Complete your first [action]!'})
    o.add_step('Best Practices Guide', 168, 'email',
               {'template': 'best_practices'})
    o.add_step('30-Day Check-in', 720, 'email',
               {'template': '30_day_review'})
    return o
```

## Activation Metrics

```python
ACTIVATION_METRICS = {
    'signup_to_activation': 'Time from signup to first core action (hours)',
    'activation_rate': '% of signups completing activation in first 7 days',
    'ttv_time': 'Time-to-value: days to first success milestone',
    'setup_completion': '% completing setup wizard',
    'feature_adoption_d30': 'Avg features used by day 30',
    'onboarding_nps': 'NPS score after onboarding completes',
}

def calculate_activation_rate(signups: int, activated: int) -> float:
    return round(activated / max(signups, 1) * 100, 1)

def find_dropoff_points(step_completion: List[Dict]) -> List[Dict]:
    """Find where users drop off in the onboarding flow."""
    dropoffs = []
    for i in range(1, len(step_completion)):
        prev = step_completion[i-1]
        curr = step_completion[i]
        if prev['count'] > 0:
            drop_pct = round((1 - curr['count'] / prev['count']) * 100, 1)
            if drop_pct > 20:
                dropoffs.append({
                    'step': curr['name'],
                    'dropoff_pct': drop_pct,
                    'suggestion': f"Investigate friction at {curr['name']} step"
                })
    return dropoffs
```

## Common Pitfalls

1. **One-size-fits-all onboarding** — different user segments need different paths
2. **Information overload** — dumping all features in the first email overwhelms users
3. **Not measuring time-to-value** — if users don't see value quickly, they churn
4. **Passive onboarding** — waiting for users to take action; be proactive with reminders
5. **No human touch for high-touch segments** — enterprise customers need CS calls, not just emails

## Verification Checklist

- [ ] Welcome email sequence configured (Day 0)
- [ ] Activation milestone defined and tracked
- [ ] Time-to-value measured and optimized
- [ ] Automated reminders for stalled users
- [ ] Human touch point for high-value segments
- [ ] Drop-off points identified in funnel
- [ ] Onboarding NPS survey triggered at completion

## See Also

- customer-success-retention — retention post-onboarding
- email-marketing-campaigns — email sequences for onboarding
- marketing-automation-workflows — trigger-based onboarding
- crm-sales-pipeline — handoff from sales to onboarding
