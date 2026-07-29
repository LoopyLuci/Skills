---
name: real-estate-crm-leads
description: "Use when managing real estate leads and clients."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [real-estate, crm, leads, property, clients, pipeline]
    related_skills: [crm-sales-pipeline, real-estate-market-analysis, email-marketing-campaigns, business-metrics-kpis]
---

# Real Estate CRM and Lead Management

Managing real estate client relationships, property leads, and transaction pipelines.

## When to Use

- Building or managing a real estate CRM system
- Tracking leads from multiple sources
- Managing the buyer/seller pipeline from first contact to closing
- Automating follow-ups and nurture sequences
- Analyzing conversion rates and agent performance

## Pipeline Stages

```python
PIPELINE_STAGES = {
    'new_lead': 'New Lead',
    'contacted': 'First Contact Made',
    'qualified': 'Qualified (budget, timeline, pre-approval)',
    'showing': 'Active Showings',
    'offer': 'Offer Made/Negotiating',
    'under_contract': 'Under Contract',
    'closing': 'Closing Process',
    'closed': 'Closed',
    'lost': 'Lost/Dead',
}
```

## Lead Management

```python
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import uuid

class LeadManager:
    """Manage real estate leads from multiple sources."""
    
    def __init__(self):
        self.leads = {}
    
    def add_lead(self, source: str, contact_info: Dict,
                 property_type: str = None, 
                 budget_range: tuple = None, notes: str = "") -> str:
        lead_id = str(uuid.uuid4())[:8]
        self.leads[lead_id] = {
            'id': lead_id, 'source': source,
            'contact': contact_info,
            'property_type': property_type,
            'budget_min': budget_range[0] if budget_range else None,
            'budget_max': budget_range[1] if budget_range else None,
            'status': 'new_lead', 'created_at': datetime.now().isoformat(),
            'last_contacted': None, 'notes': notes,
            'activity_log': [],
            'tags': [],
        }
        return lead_id
    
    def update_stage(self, lead_id: str, new_stage: str):
        if lead_id in self.leads:
            old = self.leads[lead_id]['status']
            self.leads[lead_id]['status'] = new_stage
            self.leads[lead_id]['activity_log'].append({
                'timestamp': datetime.now().isoformat(),
                'type': 'stage_change',
                'detail': f'{old} → {new_stage}'
            })
    
    def get_pipeline_summary(self) -> Dict:
        summary = {}
        for stage in PIPELINE_STAGES:
            count = sum(1 for l in self.leads.values() if l['status'] == stage)
            summary[stage] = count
        return summary
    
    def get_leads_needing_followup(self, days=3) -> List[Dict]:
        cutoff = datetime.now() - timedelta(days=days)
        return [
            l for l in self.leads.values()
            if l['status'] not in ('closed', 'lost') and (
                l['last_contacted'] is None or
                datetime.fromisoformat(l['last_contacted']) < cutoff
            )
        ]
```

## Property Matching

```python
class PropertyMatcher:
    """Score properties matching buyer preferences."""
    
    def match(self, properties: List[Dict], prefs: Dict) -> List[Dict]:
        scored = []
        for prop in properties:
            score = 0
            if prefs.get('max_price') and prop['price'] <= prefs['max_price'] * 1.1:
                score += 30
            if prefs.get('min_beds') and prop.get('beds', 0) >= prefs['min_beds']:
                score += 20
            if prefs.get('min_baths') and prop.get('baths', 0) >= prefs['min_baths']:
                score += 15
            if prefs.get('zip_codes') and prop.get('zip') in prefs['zip_codes']:
                score += 15
            scored.append({'property': prop, 'score': score})
        scored.sort(key=lambda x: x['score'], reverse=True)
        return scored[:10]
```

## Common Pitfalls

1. **Slow response to web leads** — contact within 5 minutes for highest conversion
2. **No qualification before showing** — wastes everyone's time
3. **Untracked lead sources** — can't optimize ad spend
4. **No follow-up system** — most sales happen after 5-12 contacts

## Verification Checklist

- [ ] Lead capture from all sources
- [ ] Pipeline stages defined
- [ ] Automated follow-up sequences configured
- [ ] Conversion rates tracked by source
- [ ] GDPR/CAN-SPAM compliance

## See Also

- crm-sales-pipeline — general CRM pipeline patterns
- email-marketing-campaigns — email follow-up sequences
