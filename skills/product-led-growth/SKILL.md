---
name: product-led-growth
description: "Use when implementing product-led growth strategies."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [product-led-growth, PLG, freemium, viral, self-serve, adoption]
    related_skills: [product-analytics-instrumentation, customer-onboarding-automation, saas-metrics-reporting, growth-hacking-experiments]
---

# Product-Led Growth (PLG)

Implementing product-led growth strategies — from freemium and free trial models through viral loops, self-serve conversion, and product-qualified leads (PQLs).

## When to Use

- Building a product that sells itself (self-serve motion)
- Implementing freemium, free trial, or usage-based models
- Designing viral loops and user-invite mechanics
- Identifying and acting on product-qualified leads
- Driving expansion through in-product upgrades

## PLG Metrics

```python
PLG_METRICS = {
    'pql_rate': '% of users meeting PQL criteria each month',
    'activation_rate': '% of signups reaching activation milestone',
    'time_to_value': 'Days from signup to first value moment',
    'self_serve_conversion': '% of users who upgrade without sales touch',
    'viral_coefficient': 'Avg invites sent × invite conversion rate',
    'expansion_revenue': 'Revenue from upgrades within customer base',
}

def identify_pqls(user_behavior: Dict) -> bool:
    """Determine if a user qualifies as a Product-Qualified Lead."""
    criteria = 0
    if user_behavior.get('feature_adoption', 0) >= 5: criteria += 1
    if user_behavior.get('team_members', 0) >= 3: criteria += 1
    if user_behavior.get('usage_frequency', 0) >= 10: criteria += 1
    if user_behavior.get('support_tickets', 0) <= 2: criteria += 1
    return criteria >= 3
```

## Common Pitfalls

1. **Free tier too generous** — users never need to pay; limit high-value features
2. **No activation focus** — signups that never activate are wasted; optimize first value
3. **Sales interference** — sales contacting free users too early kills PLG motion
4. **No PQL scoring** — don't know which free users are sales-ready; build PQL model
5. **Viral loop friction** — invite flows that are too complex kill virality

## Verification Checklist

- [ ] Activation milestone defined (the "aha moment")
- [ ] Free → paid conversion path clear and tested
- [ ] PQL scoring model built and validated
- [ ] Self-serve upgrade flow (no sales required)
- [ ] Viral/invite loop implemented
- [ ] Expansion triggers identified (usage limits, team invites)
- [ ] PLG + sales-led hybrid model defined (if applicable)
