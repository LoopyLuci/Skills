---
name: demand-generation
description: "Use when building demand generation and pipeline programs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [demand-generation, pipeline, ABM, inbound, outbound, campaigns]
    related_skills: [lead-generation-strategies, marketing-funnel-design, digital-marketing-strategy, marketing-automation-workflows]
---

# Demand Generation

Building demand generation programs that create and nurture pipeline — from multi-channel campaigns through ABM (Account-Based Marketing), content syndication, and pipeline reporting.

## When to Use

- Filling the top of the funnel with qualified leads
- Running integrated multi-channel demand campaigns
- Implementing ABM for target accounts
- Measuring pipeline influence and attribution
- Scaling demand generation efforts

## Demand Gen Channels

```python
DEMAND_CHANNELS = {
    'content': 'Blogs, whitepapers, eBooks, research reports',
    'webinars': 'Live and on-demand educational sessions',
    'paid': 'Search, social, display, retargeting',
    'email': 'Nurture sequences, newsletters, campaigns',
    'events': 'Conferences, trade shows, user groups',
    'ABM': 'Targeted account campaigns, 1:1 and 1:few',
    'partners': 'Co-marketing, channel partners, affiliates',
    'direct': 'Outbound sequences, cold outreach',
}

def demand_mix(budget: float, channels: List[str]) -> Dict:
    """Recommend demand generation budget allocation."""
    recommended = {}
    if len(channels) <= 2:
        recommended = {c: budget / len(channels) for c in channels}
    else:
        recommended[channels[0]] = budget * 0.35
        remaining = budget * 0.65
        for c in channels[1:]:
            recommended[c] = remaining / (len(channels) - 1)
    return recommended
```

## Common Pitfalls

1. **Spray and pray** — blasting the same message to everyone ignores segmentation
2. **Vanity metrics** — impressions and clicks don't equal pipeline
3. **No attribution** — can't tell which channel drives SQLs and revenue
4. **Ignoring existing pipeline** — demand gen fills top, but existing pipeline needs nurturing too
5. **Content not aligned** — TOFU content doesn't lead to BOFU conversion paths

## Verification Checklist

- [ ] Channel mix defined with budget allocation
- [ ] Content mapped to buyer's journey stages
- [ ] Attribution model (first-touch, multi-touch, or custom)
- [ ] Pipeline reporting (MQLs → SQLs → Opportunities → Revenue)
- [ ] ABM target account list defined
- [ ] Nurture sequences for unconverted leads
