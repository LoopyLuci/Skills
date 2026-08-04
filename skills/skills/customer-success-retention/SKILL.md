---
name: customer-success-retention
description: "Use when building customer success and retention programs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [customer-success, retention, churn, onboarding, customer-health, NPS]
    related_skills: [crm-sales-pipeline, email-marketing-campaigns, business-metrics-kpis, customer-segmentation-analysis]
---

# Customer Success and Retention

Building customer success programs that reduce churn, increase retention, and drive expansion revenue — from onboarding and health scoring through engagement and advocacy.

## When to Use

- Building a customer success function from scratch
- Reducing churn and improving retention rates
- Designing customer onboarding and engagement programs
- Implementing customer health scoring
- Driving upsells, cross-sells, and advocacy

## Customer Lifecycle

```
Acquisition → Onboarding → Adoption → Value Realization → Expansion → Advocacy
                │                                              │
                └── At Risk ←── Churn Risk ←─── Dormant ←─────┘
```

## Onboarding Design

```python
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class OnboardingProgram:
    """Design and manage customer onboarding sequences."""
    
    def __init__(self, product_name: str, time_to_value_days: int = 30):
        self.product = product_name
        self.ttv_days = time_to_value_days
        self.steps = []
    
    def add_step(self, day: int, title: str, description: str, 
                 owner: str = 'auto', success_criteria: str = "") -> 'OnboardingProgram':
        """Add an onboarding step."""
        self.steps.append({
            'day': day,
            'title': title,
            'description': description,
            'owner': owner,
            'success_criteria': success_criteria,
        })
        return self
    
    def generate_plan(self) -> str:
        """Generate complete onboarding plan."""
        plan = f"\n🚀 {self.product} Onboarding Plan ({self.ttv_days} days to value)\n"
        plan += "=" * 50 + "\n"
        
        milestones = {'week': 1, 'month': 1}
        for step in sorted(self.steps, key=lambda s: s['day']):
            week = step['day'] // 7 + 1
            if week > milestones['week']:
                plan += f"\n── Week {milestones['week']} Complete ──\n"
                milestones['week'] = week
            
            plan += f"\nDay {step['day']}: {step['title']}"
            plan += f"\n  → {step['description']}"
            if step['success_criteria']:
                plan += f"\n  ✓ Success: {step['success_criteria']}"
        
        return plan


# Standard 30-day onboarding example
def default_onboarding(product_name: str) -> OnboardingProgram:
    onboarding = OnboardingProgram(product_name)
    onboarding.add_step(0, "Welcome & Account Setup", 
        "Send welcome email with login credentials and getting-started guide",
        'auto', "User logs in within 24 hours")
    onboarding.add_step(3, "First Success Call", 
        "Schedule 30-min call to define goals and success criteria",
        'customer_success', "Goals documented in system")
    onboarding.add_step(7, "Core Feature Training", 
        "Walk through top 3 features that deliver quickest value",
        'customer_success', "User completes core actions")
    onboarding.add_step(14, "Integration Setup", 
        "Configure any integrations or data imports",
        'customer_success', "Integrations active")
    onboarding.add_step(21, "Best Practices Review", 
        "Review usage data and suggest optimizations",
        'customer_success', "Adoption score > 60%")
    onboarding.add_step(30, "Business Review & Next Steps", 
        "30-day review: results achieved, upcoming milestones, expansion opportunities",
        'customer_success', "NPS collected, Q2 plan documented")
    return onboarding
```

## Health Scoring

```python
class CustomerHealthScore:
    """Calculate customer health scores to identify at-risk accounts."""
    
    WEIGHTS = {
        'product_usage': 0.30,
        'support_interaction': 0.20,
        'engagement': 0.20,
        'business_outcomes': 0.20,
        'sentiment': 0.10,
    }
    
    @staticmethod
    def calculate(customer: Dict) -> Dict:
        """Calculate health score (0-100) for a customer."""
        score = 0
        components = {}
        
        # Product usage (0-100)
        usage = customer.get('login_frequency', 0) * 10
        feature_adoption = customer.get('features_used', [])
        max_features = customer.get('total_features', 10)
        usage_score = min(100, usage + (len(feature_adoption) / max(max_features, 1) * 50))
        components['product_usage'] = usage_score
        score += usage_score * CustomerHealthScore.WEIGHTS['product_usage']
        
        # Support interaction
        tickets = customer.get('open_tickets', 0)
        resolution_time = customer.get('avg_resolution_hours', 24)
        support_score = max(0, 100 - tickets * 20 - resolution_time * 2)
        components['support_interaction'] = support_score
        score += support_score * CustomerHealthScore.WEIGHTS['support_interaction']
        
        # Engagement
        last_login = customer.get('days_since_login', 30)
        email_opens = customer.get('email_open_rate', 0.5)
        engagement_score = max(0, 100 - last_login * 3) + (email_opens * 20)
        components['engagement'] = min(100, engagement_score)
        score += min(100, engagement_score) * CustomerHealthScore.WEIGHTS['engagement']
        
        # Business outcomes
        if customer.get('goals_achieved', 0) > 0:
            outcomes = (customer.get('goals_achieved', 0) / max(customer.get('goals_set', 1), 1)) * 100
        else:
            outcomes = 50  # Neutral
        components['business_outcomes'] = min(100, outcomes)
        score += min(100, outcomes) * CustomerHealthScore.WEIGHTS['business_outcomes']
        
        # Sentiment (NPS, CSAT)
        nps = customer.get('nps_score', 50)
        sentiment = (nps + 100) / 2  # Convert -100..100 to 0..100
        components['sentiment'] = sentiment
        score += sentiment * CustomerHealthScore.WEIGHTS['sentiment']
        
        health = round(score)
        
        return {
            'score': health,
            'rating': 'green' if health >= 70 else 'yellow' if health >= 40 else 'red',
            'components': components,
            'trend': customer.get('health_trend', 'stable'),
        }
```

## Churn Prediction

```python
class ChurnPredictor:
    """Predict customer churn risk based on behaviors."""
    
    RISK_FACTORS = {
        'decreased_usage': {
            'description': 'Usage dropped 30%+ compared to previous 30 days',
            'weight': 0.30,
        },
        'no_login': {
            'description': 'Has not logged in for 14+ days',
            'weight': 0.25,
        },
        'negative_support': {
            'description': 'Opened support ticket with negative sentiment in last 7 days',
            'weight': 0.15,
        },
        'missed_renewal': {
            'description': 'Contract renewal date passed without action',
            'weight': 0.15,
        },
        'budget_change': {
            'description': 'Customer indicated budget cuts or changing priorities',
            'weight': 0.10,
        },
        'competitor_mention': {
            'description': 'Customer mentioned evaluating competitors',
            'weight': 0.05,
        },
    }
    
    @staticmethod
    def assess(customer: Dict) -> Dict:
        """Assess churn risk for a customer."""
        risk_score = 0
        active_risks = []
        
        if customer.get('usage_change', 0) < -0.3:
            risk_score += ChurnPredictor.RISK_FACTORS['decreased_usage']['weight']
            active_risks.append('decreased_usage')
        
        if customer.get('days_since_login', 0) > 14:
            risk_score += ChurnPredictor.RISK_FACTORS['no_login']['weight']
            active_risks.append('no_login')
        
        if customer.get('recent_negative_tickets', 0) > 0:
            risk_score += ChurnPredictor.RISK_FACTORS['negative_support']['weight']
            active_risks.append('negative_support')
        
        risk_pct = round(risk_score * 100)
        
        return {
            'customer_id': customer.get('id', 'unknown'),
            'churn_risk_pct': risk_pct,
            'risk_level': 'high' if risk_pct >= 40 else 'medium' if risk_pct >= 20 else 'low',
            'active_risk_factors': active_risks,
            'next_action': ChurnPredictor._suggest_action(active_risks),
        }
    
    @staticmethod
    def _suggest_action(risks: List[str]) -> str:
        actions = {
            'decreased_usage': 'Schedule re-engagement call, offer training',
            'no_login': 'Send re-engagement email with feature highlights',
            'negative_support': 'Escalate support ticket, assign dedicated support',
            'missed_renewal': 'Contact for renewal discussion immediately',
            'budget_change': 'Prepare ROI presentation, offer discount if needed',
            'competitor_mention': 'Share competitive comparison, strengthen relationship',
        }
        if not risks:
            return 'No action needed — customer is healthy'
        return '; '.join(actions.get(r, 'Monitor') for r in risks)
```

## Expansion Playbook

```python
class ExpansionPlaybook:
    """Define upsell, cross-sell, and expansion strategies."""
    
    PLAYBOOKS = {
        'upsell': {
            'trigger': 'Customer reaches 80%+ of plan limits',
            'approach': 'Show value of next tier, offer migration support',
            'timing': 'During quarterly business review',
        },
        'cross_sell': {
            'trigger': 'Customer asks about a feature in another product',
            'approach': 'Demo complementary product, share case studies',
            'timing': 'After value milestone achieved',
        },
        'advocacy': {
            'trigger': 'NPS ≥ 9, high usage, active engagement',
            'approach': 'Invite to customer advisory board, request case study',
            'timing': 'After 6+ months of success',
        },
    }
    
    @staticmethod
    def identify_opportunity(customer: Dict) -> List[Dict]:
        """Identify expansion opportunities for a customer."""
        opportunities = []
        
        if customer.get('usage_pct', 0) >= 80:
            opportunities.append({
                'type': 'upsell',
                'reason': f"Using {customer.get('usage_pct')}% of plan",
                'playbook': ExpansionPlaybook.PLAYBOOKS['upsell'],
            })
        
        if customer.get('nps_score', 0) >= 9:
            opportunities.append({
                'type': 'advocacy',
                'reason': 'Promoter (NPS ≥ 9)',
                'playbook': ExpansionPlaybook.PLAYBOOKS['advocacy'],
            })
        
        return opportunities
```

## Common Pitfalls

1. **Reactive vs proactive** — waiting for customers to complain instead of monitoring health scores
2. **No onboarding structure** — customers who don't see value in 30 days will churn
3. **Health score without action** — scoring is useless without automated triggers for intervention
4. **One-size-fits-all** — enterprise and SMB customers need different success approaches
5. **Success = support** — customer success is proactive, support is reactive; they're different functions
6. **Not measuring outcomes** — tracking activities (calls made) instead of outcomes (customer health improved)

## Verification Checklist

- [ ] Onboarding program designed with time-to-value milestones
- [ ] Customer health score model defined (product, support, engagement, outcomes, sentiment)
- [ ] Health score thresholds set (green/yellow/red)
- [ ] Churn risk predictors identified and monitored
- [ ] Automated triggers for health score changes
- [ ] Quarterly business review process established
- [ ] Expansion playbooks defined (upsell, cross-sell, advocacy)
- [ ] NPS/CSAT survey program active
- [ ] Customer success platform configured

## See Also

- crm-sales-pipeline — managing customer accounts
- email-marketing-campaigns — automated customer communication
- business-metrics-kpis — tracking retention and expansion metrics
- customer-segmentation-analysis — segmenting customers by health
