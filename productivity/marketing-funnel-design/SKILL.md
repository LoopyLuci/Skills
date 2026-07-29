---
name: marketing-funnel-design
description: "Use when designing marketing funnels and conversion paths."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [marketing, funnel, conversion, lead-generation, sales-funnel, AIDA]
    related_skills: [crm-sales-pipeline, ab-testing-experimentation, email-marketing-campaigns, conversion-rate-optimization]
---

# Marketing Funnel Design

Designing and optimizing marketing funnels — from awareness through acquisition, with funnel stages, conversion tracking, lead magnets, and automation sequences.

## When to Use

- Building a marketing funnel from scratch (landing page → email → sale)
- Optimizing conversion rates between funnel stages
- Designing lead magnet and email nurture sequences
- Tracking funnel metrics and identifying drop-off points
- Implementing multi-channel funnels (social, email, PPC, SEO)

## Funnel Architecture

```
TOF (Top of Funnel) — Awareness
    │ Social, SEO, Ads, Content
    ▼
MOF (Middle of Funnel) — Interest/Consideration
    │ Lead Magnet, Email Subscribe, Webinar
    ▼
BOF (Bottom of Funnel) — Decision
    │ Demo, Trial, Consultation, Sales Call
    ▼
Purchase/Conversion
    │ Thank You, Upsell, Cross-sell
    ▼
Retention/Loyalty
```

## Funnel Stage Tracker

```python
from datetime import datetime
from typing import Dict, List, Optional

class FunnelStage:
    """Define a funnel stage with conversion metrics."""
    
    def __init__(self, name: str, label: str, 
                 expected_conversion_pct: float = 100):
        self.name = name
        self.label = label
        self.expected_conversion = expected_conversion_pct  # % from previous stage
        self.entries = 0
        self.exits = 0

class MarketingFunnel:
    """Track and analyze a marketing funnel."""
    
    def __init__(self, name: str):
        self.name = name
        self.stages = []
        self.contacts = {}  # contact_id -> {stage, entered_at, source, ...}
    
    def define_stages(self, stages: List[FunnelStage]):
        """Define the funnel stages in order."""
        self.stages = stages
        if self.stages:
            self.stages[0].expected_conversion = 100  # Top of funnel is 100%
    
    def record_entry(self, contact_id: str, stage_name: str, 
                     source: str = "", metadata: Dict = None):
        """Record a contact entering a funnel stage."""
        if contact_id not in self.contacts:
            self.contacts[contact_id] = {
                'stages': {},
                'source': source,
                'first_contact': datetime.now().isoformat(),
                'metadata': metadata or {},
            }
        
        self.contacts[contact_id]['stages'][stage_name] = {
            'entered_at': datetime.now().isoformat(),
            'source': source,
        }
        
        for stage in self.stages:
            if stage.name == stage_name:
                stage.entries += 1
                break
    
    def record_conversion(self, contact_id: str, from_stage: str, to_stage: str):
        """Record a contact moving to the next stage."""
        if contact_id in self.contacts:
            self.contacts[contact_id]['stages'][to_stage] = {
                'entered_at': datetime.now().isoformat(),
                'converted_from': from_stage,
            }
            
            for stage in self.stages:
                if stage.name == to_stage:
                    stage.entries += 1
                if stage.name == from_stage:
                    stage.exits += 1
    
    def get_funnel_metrics(self) -> Dict:
        """Calculate conversion rates between each stage."""
        metrics = []
        
        for i, stage in enumerate(self.stages):
            stage_metrics = {
                'name': stage.name,
                'label': stage.label,
                'entries': stage.entries,
                'conversion_rate': None,
            }
            
            if i > 0 and self.stages[i-1].entries > 0:
                stage_metrics['conversion_rate'] = round(
                    (stage.entries / self.stages[i-1].entries) * 100, 1
                )
            
            metrics.append(stage_metrics)
        
        # Overall conversion
        first_entries = self.stages[0].entries if self.stages else 0
        last_entries = self.stages[-1].entries if self.stages else 0
        overall = round((last_entries / first_entries) * 100, 1) if first_entries > 0 else 0
        
        return {
            'funnel_name': self.name,
            'stages': metrics,
            'overall_conversion_pct': overall,
            'total_contacts': len(self.contacts),
        }
    
    def get_drop_off_points(self) -> List[Dict]:
        """Identify stages with the largest drop-off."""
        drop_offs = []
        for i in range(1, len(self.stages)):
            prev = self.stages[i-1].entries
            curr = self.stages[i].entries
            if prev > 0:
                drop_pct = round((1 - curr / prev) * 100, 1)
                drop_offs.append({
                    'from_stage': self.stages[i-1].name,
                    'to_stage': self.stages[i].name,
                    'drop_off_pct': drop_pct,
                    'lost_contacts': prev - curr,
                })
        
        return sorted(drop_offs, key=lambda x: x['drop_off_pct'], reverse=True)
```

## Lead Magnet Types

```python
LEAD_MAGNET_TEMPLATES = {
    'pdf_guide': {
        'type': 'downloadable_pdf',
        'format': 'PDF',
        'delivery': 'email',
        'description': 'Comprehensive guide on [topic]. Requires email to download.'
    },
    'checklist': {
        'type': 'checklist',
        'format': 'PDF/Web',
        'delivery': 'instant',
        'description': 'Actionable checklist [title]. Collects email for access.'
    },
    'template': {
        'type': 'template',
        'format': 'Google Doc / Notion',
        'delivery': 'email',
        'description': 'Ready-to-use template for [specific use case].'
    },
    'webinar': {
        'type': 'live_or_recorded',
        'format': 'Video',
        'delivery': 'scheduled_email',
        'description': 'Educational webinar on [topic]. Registration required.'
    },
    'assessment': {
        'type': 'interactive',
        'format': 'Web tool',
        'delivery': 'instant + email results',
        'description': 'Free assessment/audit. Collects email for results delivery.'
    },
    'email_course': {
        'type': 'drip_sequence',
        'format': 'Multi-email',
        'delivery': '5-7 day sequence',
        'description': 'Structured email course delivered over N days.'
    },
    'trial': {
        'type': 'free_trial',
        'format': 'Product access',
        'delivery': 'instant',
        'description': 'Free trial of [product/service] for N days.'
    },
}

def suggest_lead_magnet(business_type: str, audience: str) -> Dict:
    """Suggest appropriate lead magnet based on business type."""
    suggestions = {
        'saas': LEAD_MAGNET_TEMPLATES['trial'],
        'consulting': LEAD_MAGNET_TEMPLATES['assessment'],
        'ecommerce': LEAD_MAGNET_TEMPLATES['pdf_guide'],
        'education': LEAD_MAGNET_TEMPLATES['email_course'],
        'real_estate': LEAD_MAGNET_TEMPLATES['checklist'],
        'coaching': LEAD_MAGNET_TEMPLATES['webinar'],
    }
    return suggestions.get(business_type, LEAD_MAGNET_TEMPLATES['pdf_guide'])
```

## Email Nurture Sequence Builder

```python
class NurtureSequence:
    """Build automated email nurture sequences for funnel stages."""
    
    def __init__(self, name: str):
        self.name = name
        self.emails = []
    
    def add_email(self, subject: str, body_template: str, 
                  delay_days: int = 1, goal: str = ""):
        """Add an email to the sequence."""
        self.emails.append({
            'day': len(self.emails) + 1,
            'delay_days': delay_days,
            'subject': subject,
            'body_template': body_template,
            'goal': goal,
        })
        return self  # Fluent API
    
    def generate_sequence_plan(self) -> str:
        """Generate a readable sequence plan."""
        plan = f"\n=== Nurture Sequence: {self.name} ===\n"
        cumulative_delay = 0
        for email in self.emails:
            cumulative_delay += email['delay_days']
            plan += f"\nDay {cumulative_delay} | {email['subject']}"
            plan += f"\n  Goal: {email['goal']}"
            plan += f"\n  Body: {email['body_template'][:100]}..."
            plan += "\n" + "-" * 40
        return plan


# Example: welcome sequence
welcome = NurtureSequence("New Subscriber Welcome")
welcome.add_email("Welcome to [Company]!", 
    "Hi [Name], thanks for subscribing...", 
    delay_days=0, goal="Deliver lead magnet")
welcome.add_email("Here's your [lead magnet name]",
    "As promised, here's your free [resource]...",
    delay_days=1, goal="Ensure lead magnet delivery")
welcome.add_email("How can we help?",
    "Hi [Name], I noticed you downloaded [resource]...",
    delay_days=3, goal="Start conversation, qualify")
welcome.add_email("Case study: [relevant success story]",
    "See how [similar client] achieved [result]...",
    delay_days=5, goal="Build social proof")
welcome.add_email("Ready to get started?",
    "Let's schedule a quick call to discuss...",
    delay_days=7, goal="Book consultation/demo")
```

## Common Pitfalls

1. **Leaky funnel** — tracking only top and bottom, missing mid-funnel drop-off; instrument every stage
2. **Too many steps** — each extra stage drops 20-40% of people; minimize steps to conversion
3. **Weak lead magnet** — "Sign up for our newsletter" has low conversion; offer something valuable
4. **No follow-up** — 80% of leads convert between 5-12 contacts; nurture sequences are essential
5. **Funnel ≠ customer journey** — the customer's actual journey isn't a straight line; map both
6. **Vanity metrics** — traffic doesn't equal revenue; focus on conversion rate and CPA

## Verification Checklist

- [ ] Funnel stages map to actual customer journey steps
- [ ] Conversion tracking at every stage (not just top and bottom)
- [ ] Lead magnet aligned with target audience pain point
- [ ] Email nurture sequence provides value before asking for sale
- [ ] Drop-off points identified and prioritized for optimization
- [ ] A/B testing plan for top-3 drop-off stages
- [ ] Attribution model connects funnel stage to revenue

## See Also

- crm-sales-pipeline — moving leads from funnel to pipeline
- ab-testing-experimentation — testing funnel improvements
- email-marketing-campaigns — building nurture sequences
- conversion-rate-optimization — optimizing each funnel stage
