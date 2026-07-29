---
name: go-to-market-strategy
description: "Use when planning go-to-market and launch strategies."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [go-to-market, product-launch, GTM, market-entry, launch-strategy]
    related_skills: [product-management-roadmap, digital-marketing-strategy, pricing-strategy-optimization, sales-enablement-playbooks]
---

# Go-To-Market Strategy

Planning and executing go-to-market strategies — from market segmentation through channel strategy, launch planning, and post-launch optimization.

## When to Use

- Launching a new product or feature
- Entering a new market or geography
- Planning a GTM strategy for a startup
- Coordinating cross-functional launch activities

## GTM Framework

```python
class GTMStrategy:
    def __init__(self, product: str, target_market: str, launch_date: str, revenue_target: float):
        self.product = product
        self.market = target_market
        self.launch_date = launch_date
        self.revenue_target = revenue_target
        self.segments = []; self.channels = []; self.milestones = []
    
    def add_segment(self, name: str, personas: List[str], pain_points: List[str], priority: int = 3):
        self.segments.append({'name': name, 'personas': personas, 'pain_points': pain_points, 'priority': priority})
        return self
    
    def add_channel(self, name: str, budget_pct: float, expected_leads: int, cpl: float):
        self.channels.append({'name': name, 'budget_pct': budget_pct, 'expected_leads': expected_leads, 'cpl': cpl})
        return self
    
    def generate_plan(self) -> str:
        plan = f"🚀 GTM: {self.product} → {self.market}\nLaunch: {self.launch_date} | Revenue: ${self.revenue_target:,.0f}\n"
        plan += "=" * 40 + "\n\nSegments:\n"
        for s in sorted(self.segments, key=lambda x: x['priority']):
            plan += f"  P{s['priority']}: {s['name']}\n"
        plan += "\nChannels:\n"
        for c in sorted(self.channels, key=lambda x: x['expected_leads'], reverse=True):
            plan += f"  {c['name']}: {c['budget_pct']}% budget, ~{c['expected_leads']} leads\n"
        return plan
```

## Launch Phases

```python
LAUNCH_PHASES = {
    'T-60': 'Market research, pricing, sales playbook, positioning',
    'T-30': 'Landing page, email sequences, sales training, press kit',
    'T-7': 'Final QA, social queue, support briefing, dashboards',
    'Launch Day': 'Announcement, press release, webinar, sales activation',
    'Week 1': 'Early adopter follow-up, analytics review, paid amplification',
    'Month 1': 'GTM retrospective, channel analysis, customer interviews',
}
```

## Common Pitfalls

1. **No market validation** — building what nobody wants
2. **Sales and marketing not aligned** — leads generated but can't close
3. **No post-launch plan** — launch day is just the beginning
4. **Trying to reach everyone** — solve one problem for one audience well

## Verification Checklist

- [ ] Target segments prioritized
- [ ] Channel mix with budget allocation defined
- [ ] Pricing finalized
- [ ] Launch timeline with milestones and owners
- [ ] Success metrics defined

## See Also

- product-management-roadmap — product readiness
- digital-marketing-strategy — marketing component
- pricing-strategy-optimization — launch pricing
- sales-enablement-playbooks — sales readiness
