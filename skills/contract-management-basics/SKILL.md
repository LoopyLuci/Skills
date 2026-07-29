---
name: contract-management-basics
description: "Use when managing contracts and agreements."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [contract-management, agreements, terms, signatures, renewals, legal-ops]
    related_skills: [vendor-management-procurement, legal-compliance-business, business-insurance-guide, financial-modeling-budgeting]
---

# Contract Management Basics

Managing contracts and agreements — from contract lifecycle and types through negotiation, execution, storage, renewal/expiry tracking, and compliance.

## When to Use

- Managing customer, vendor, or partner contracts
- Tracking contract renewals and expirations
- Standardizing contract templates and terms
- Building a contract repository and management process
- Ensuring contract compliance with agreed terms

## Contract Lifecycle

```python
CONTRACT_LIFECYCLE = {
    'request': 'Business need identified, contract request submitted',
    'draft': 'Template selected, terms drafted by legal or template',
    'negotiation': 'Redlines exchanged, terms negotiated, approvals',
    'execution': 'Final version signed (e-signature or wet signature)',
    'storage': 'Executed copy stored in contract repository',
    'obligations': 'Track deliverables, milestones, SLAs',
    'amendments': 'Changes during contract term (change orders)',
    'renewal': 'Renewal or termination decision before expiry',
}

class ContractManager:
    """Track contract lifecycle and obligations."""
    def __init__(self):
        self.contracts = {}
    
    def add_contract(self, title: str, party: str, value: float,
                     start_date: str, end_date: str, 
                     contract_type: str = 'customer') -> str:
        import uuid
        cid = str(uuid.uuid4())[:8]
        self.contracts[cid] = {
            'id': cid, 'title': title, 'party': party,
            'value': value, 'start': start_date, 'end': end_date,
            'type': contract_type, 'status': 'active',
        }
        return cid
    
    def get_expiring(self, days: int = 60) -> List[Dict]:
        from datetime import datetime, timedelta
        threshold = datetime.now() + timedelta(days=days)
        return [c for c in self.contracts.values() 
                if datetime.fromisoformat(c['end']) <= threshold and c['status'] == 'active']
```

## Common Pitfalls

1. **No contract repository** — contracts scattered across emails, drives, and desks
2. **Auto-renewal surprises** — contracts with auto-renewal clauses missed; set calendar alerts
3. **No obligation tracking** — signed a contract but forgot to deliver on commitments
4. **Expired contracts** — using services under expired terms; track renewals
5. **No standard templates** — every contract negotiated from scratch; use clause libraries

## Verification Checklist

- [ ] Contract repository established (centralized, searchable)
- [ ] Standard templates for common contract types
- [ ] Negotiation guidelines (what's negotiable, approval thresholds)
- [ ] E-signature integration (DocuSign, HelloSign)
- [ ] Renewal/expiry tracking (60/30/7 day alerts)
- [ ] Obligations and milestones tracked per contract
- [ ] Contract value tracked for financial reporting
- [ ] Legal review process for non-standard terms
