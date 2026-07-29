---
name: partner-channel-management
description: "Use when building partner and channel sales programs."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [partner-management, channel-sales, partnerships, resellers, ecosystem]
    related_skills: [influencer-affiliate-programs, sales-enablement-playbooks, demand-generation, revenue-operations-revops]
---

# Partner and Channel Management

Building partner and channel sales programs — from partner recruitment and onboarding through enablement, deal registration, and performance management.

## When to Use

- Building a channel/reseller program
- Recruiting and onboarding technology partners
- Managing partner relationships and performance
- Implementing deal registration and partner incentives
- Scaling indirect revenue channels

## Partner Types

```python
PARTNER_TYPES = {
    'reseller': 'Sells your product/service directly to end customers',
    'referral': 'Refers leads for a referral fee (no reselling)',
    'technology': 'Integrates with or builds on your platform',
    'ISV': 'Independent Software Vendor embeds your technology',
    'consulting': 'Recommends your solution as part of consulting engagements',
    'system_integrator': 'Implements and customizes your solution for enterprise clients',
}

class PartnerProgram:
    """Manage partner relationships and performance."""
    def __init__(self, name: str):
        self.name = name
        self.partners = {}
    
    def add_partner(self, name: str, partner_type: str, 
                    region: str, tier: str = 'basic') -> str:
        import uuid
        pid = str(uuid.uuid4())[:8]
        self.partners[pid] = {
            'id': pid, 'name': name, 'type': partner_type,
            'region': region, 'tier': tier, 'deals': [],
            'revenue': 0.0, 'status': 'active',
        }
        return pid
    
    def record_deal(self, pid: str, value: float, 
                    deal_source: str = 'partner_initiated') -> bool:
        if pid in self.partners:
            self.partners[pid]['revenue'] += value
            self.partners[pid]['deals'].append({'value': value, 'source': deal_source})
            return True
        return False
```

## Common Pitfalls

1. **Partner conflict with direct sales** — direct and channel compete for same deals; define rules of engagement
2. **No partner enablement** — partners can't sell what they don't understand; train them
3. **Poor communication** — partners need regular updates on product, pricing, promotions
4. **Deal registration abuse** — partners registering deals they didn't originate; set rules
5. **No performance tiers** — top partners and occasional partners need different treatment

## Verification Checklist

- [ ] Partner tiers defined with clear benefits per tier
- [ ] Partner agreement/template created
- [ ] Partner portal or enablement resources available
- [ ] Deal registration system in place
- [ ] Partner training/certification program
- [ ] Partner performance metrics and review cadence
- [ ] Rules of engagement (direct vs channel) documented
