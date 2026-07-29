---
name: lead-generation-strategies
description: "Use when generating leads through multiple channels."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [lead-generation, demand-generation, inbound, outbound, B2B-leads]
    related_skills: [crm-sales-pipeline, marketing-funnel-design, list-building-email-growth, digital-marketing-strategy]
---

# Lead Generation Strategies

Generating high-quality leads through multiple channels — from inbound content strategies through outbound outreach, paid acquisition, and referral programs.

## When to Use

- Building a lead generation engine for a business
- Diversifying lead sources beyond one channel
- Creating inbound lead magnets and content
- Running outbound outreach campaigns
- Building referral and partner programs

## Channel Strategy

```python
LEAD_CHANNELS = {
    'inbound_content': {
        'type': 'inbound',
        'cost': 'medium',
        'time_to_results': '2-4 months',
        'lead_quality': 'high',
        'best_for': 'B2B, SaaS, consulting, education',
    },
    'paid_search': {
        'type': 'paid',
        'cost': 'high',
        'time_to_results': 'immediate',
        'lead_quality': 'medium',
        'best_for': 'High-intent searches, local services, ecommerce',
    },
    'outbound_email': {
        'type': 'outbound',
        'cost': 'low',
        'time_to_results': '1-2 weeks',
        'lead_quality': 'medium',
        'best_for': 'B2B, enterprise, specific ICP targeting',
    },
    'webinars': {
        'type': 'inbound',
        'cost': 'medium',
        'time_to_results': '1-2 months',
        'lead_quality': 'very_high',
        'best_for': 'B2B, complex products, thought leadership',
    },
    'referral': {
        'type': 'inbound',
        'cost': 'low',
        'time_to_results': '1-3 months',
        'lead_quality': 'very_high',
        'best_for': 'All B2B, services, high-ticket products',
    },
    'partnerships': {
        'type': 'inbound',
        'cost': 'medium',
        'time_to_results': '3-6 months',
        'lead_quality': 'high',
        'best_for': 'B2B, complementary products/services',
    },
    'events': {
        'type': 'inbound',
        'cost': 'high',
        'time_to_results': '1-3 months',
        'lead_quality': 'high',
        'best_for': 'Local businesses, enterprise, networking',
    },
}

def suggest_channels(budget: str, timeline: str, icp: str) -> List[str]:
    recs = []
    if budget != 'low' and timeline == 'immediate':
        recs.append('paid_search')
    if icp in ('b2b', 'enterprise'):
        recs.extend(['webinars', 'outbound_email', 'referral'])
    recs.append('inbound_content')
    recs.append('referral')
    return recs[:4]
```

## Inbound Lead Magnet Funnel

```python
def inbound_lead_funnel(topic: str, audience: str) -> Dict:
    return {
        'top_of_funnel': {
            'channel': 'SEO, social media, paid',
            'offer': f'Free guide: Ultimate Guide to {topic}',
            'cta': 'Download the free guide',
            'conversion': 'Email address',
        },
        'middle_of_funnel': {
            'channel': 'Email nurture',
            'offer': f'Webinar: How to Master {topic}',
            'cta': 'Register for webinar',
            'conversion': 'Warm lead',
        },
        'bottom_of_funnel': {
            'channel': 'Sales outreach',
            'offer': f'Free consultation/audit',
            'cta': 'Book a call',
            'conversion': 'SQL',
        },
    }
```

## Common Pitfalls

1. **Relying on one channel** — algorithm changes or ad costs can kill single-source pipeline
2. **No lead qualification** — generating leads that don't fit your ICP wastes sales time
3. **Ignoring existing customers** — referrals from happy customers close at 3-5x higher rate
4. **Inbound only** — inbound is great but slow; pair with outbound for faster pipeline
5. **No lead scoring** — not all leads are equal; score and route appropriately

## Verification Checklist

- [ ] 3+ lead generation channels active
- [ ] ICP clearly defined for targeting
- [ ] Lead magnets created for each funnel stage
- [ ] Lead scoring model in place
- [ ] Referral program established
- [ ] Conversion rates tracked per channel

## See Also

- crm-sales-pipeline — managing generated leads
- marketing-funnel-design — moving leads through funnel
- list-building-email-growth — growing email list from leads
- digital-marketing-strategy — lead gen strategy
