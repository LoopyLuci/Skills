---
name: marketing-attribution-modeling
description: "Use when implementing marketing attribution and ROI models."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [marketing-attribution, ROI, multi-touch, first-touch, last-touch, data-driven]
    related_skills: [demand-generation, revenue-operations-revops, website-analytics-tracking, digital-marketing-strategy]
---

# Marketing Attribution Modeling

Implementing marketing attribution models — from single-touch and multi-touch through algorithmic attribution, incrementality testing, and unified measurement.

## When to Use

- Understanding which marketing channels drive conversions
- Allocating marketing budget based on actual impact
- Moving beyond last-click attribution (which overvalues bottom-of-funnel)
- Measuring incremental impact of marketing activities
- Building a unified marketing measurement framework

## Attribution Models

```python
ATTRIBUTION_MODELS = {
    'first_touch': '100% credit to first interaction (overvalues awareness)',
    'last_touch': '100% credit to last interaction before conversion (overvalues bottom)',
    'linear': 'Equal credit to all touchpoints in the journey',
    'time_decay': 'More credit to touchpoints closer to conversion',
    'position_based': '40% first touch, 40% last touch, 20% middle (U-shaped)',
    'algorithmic': 'ML-driven attribution based on actual channel influence',
    'incremental': 'Measures lift vs control group (true causal impact)',
}

class AttributionModel:
    """Calculate channel attribution."""
    def __init__(self, model_type: str = 'multi_touch'):
        self.model_type = model_type
    
    def attribute(self, journeys: List[Dict], conversions: List[int]) -> Dict:
        channel_credit = {}
        for journey, converted in zip(journeys, conversions):
            if not converted: continue
            channels = journey.get('touchpoints', [])
            if not channels: continue
            
            if self.model_type == 'first_touch':
                channel_credit[channels[0]] = channel_credit.get(channels[0], 0) + 1
            elif self.model_type == 'last_touch':
                channel_credit[channels[-1]] = channel_credit.get(channels[-1], 0) + 1
            elif self.model_type == 'linear':
                weight = 1 / len(channels)
                for ch in channels:
                    channel_credit[ch] = channel_credit.get(ch, 0) + weight
        
        return channel_credit
```

## Common Pitfalls

1. **Last-click dominance** — underinvesting in awareness channels that drive top-of-funnel
2. **Cross-device blind spots** — attributing to wrong channel when user switches devices
3. **Offline-online gap** — online attribution misses offline purchases influenced by online
4. **View-through vs click-through** — view-through attribution is controversial; use with caution
5. **Channel cannibalization** — paid search capturing brand searches that would convert organically

## Verification Checklist

- [ ] Attribution model selected (single, multi-touch, or algorithmic)
- [ ] Cross-device tracking enabled (or probabilistic)
- [ ] Offline conversion data integrated (if applicable)
- [ ] Model regularly validated against holdout/incrementality tests
- [ ] Channel overlap and cannibalization analyzed
- [ ] Budget allocation adjusted based on attribution insights
- [ ] Causal incrementality testing (geo holdout, time-series) in roadmap
