---
name: business-development-partnerships
description: "Use when building business development and partnerships."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [business-development, partnerships, strategic-alliances, channel, ecosystem]
    related_skills: [partner-channel-management, sales-enablement-playbooks, revenue-operations-revops, go-to-market-strategy]
---

# Business Development and Partnerships

Building business development and strategic partnerships — from partner identification through deal structuring, negotiation, and partnership management.

## When to Use

- Identifying and pursuing strategic partnership opportunities
- Structuring partnership deals (tech, channel, referral)
- Managing partner relationships and joint GTM
- Building a partnership pipeline

## BD Framework

```python
BD_PARTNERSHIP_TYPES = {
    'technology': 'API integration, co-building, platform embed — mutual technical value',
    'channel': 'Reseller, referral, agency — partner sells/distributes your product',
    'strategic': 'Joint venture, co-marketing, co-innovation — high value, high commitment',
    'ecosystem': 'Community, open source, standards bodies — industry influence',
}

class PartnershipPipeline:
    """Manage business development pipeline."""
    def __init__(self):
        self.partners = []
    
    def add_opportunity(self, company: str, type: str, 
                        value: float, stage: str = 'identified'):
        self.partners.append({
            'company': company, 'type': type,
            'value': value, 'stage': stage,
        })
    
    def weighted_pipeline(self) -> float:
        stage_weights = {'identified': 0.1, 'engaged': 0.3, 
                        'negotiating': 0.6, 'closed': 1.0}
        return sum(p['value'] * stage_weights.get(p['stage'], 0) for p in self.partners)
```

## Verification Checklist

- [ ] Partnership type identified (tech, channel, strategic, ecosystem)
- [ ] Target partner list with prioritization criteria
- [ ] Value proposition for each partner type
- [ ] Deal structure defined (revenue share, referral fee, co-marketing)
- [ ] Partner agreement template ready
- [ ] Joint GTM plan (for strategic partnerships)
- [ ] Partnership pipeline tracked with stages and value
- [ ] Partner performance reviewed quarterly
