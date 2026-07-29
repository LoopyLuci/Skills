---
name: crm-sales-pipeline
description: "Use when building CRM and sales pipeline management systems."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [crm, sales, pipeline, deals, lead-management, salesforce]
    related_skills: [real-estate-crm-leads, email-marketing-campaigns, business-metrics-kpis, customer-segmentation-analysis]
---

# CRM and Sales Pipeline Management

Building and managing customer relationship management (CRM) systems and sales pipelines — from deal tracking and pipeline analytics through automation and team collaboration.

## When to Use

- Implementing a CRM for your sales team
- Building custom pipeline tracking (deals, stages, probability)
- Automating sales tasks (follow-ups, task assignment, notifications)
- Analyzing pipeline health (velocity, conversion, bottlenecks)
- Integrating CRM with other tools (email, calendar, marketing)

## Pipeline Architecture

```
Lead → MQL → SQL → Opportunity → Proposal → Negotiation → Closed Won
  ↑       ↑       ↑        ↑            ↑            ↑        ↓
  0%     10%     25%     50%          75%          90%     100%
```

## Pipeline Management

```python
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum
import json

class DealStage(str, Enum):
    LEAD = 'lead'
    MQL = 'marketing_qualified_lead'
    SQL = 'sales_qualified_lead'
    OPPORTUNITY = 'opportunity'
    PROPOSAL = 'proposal'
    NEGOTIATION = 'negotiation'
    CLOSED_WON = 'closed_won'
    CLOSED_LOST = 'closed_lost'

STAGE_PROBABILITY = {
    DealStage.LEAD: 0.05,
    DealStage.MQL: 0.10,
    DealStage.SQL: 0.25,
    DealStage.OPPORTUNITY: 0.50,
    DealStage.PROPOSAL: 0.75,
    DealStage.NEGOTIATION: 0.90,
    DealStage.CLOSED_WON: 1.0,
    DealStage.CLOSED_LOST: 0.0,
}

class SalesPipeline:
    """End-to-end sales pipeline management."""
    
    def __init__(self, name: str = "Main Pipeline"):
        self.name = name
        self.deals = {}
        self.stages = [s.value for s in DealStage if s.value != 'closed_lost']
    
    def create_deal(self, name: str, value: float, contact: Dict,
                    stage: str = 'lead', notes: str = "") -> str:
        """Create a new deal in the pipeline."""
        import uuid
        deal_id = str(uuid.uuid4())[:8]
        
        deal = {
            'id': deal_id,
            'name': name,
            'value': value,
            'weighted_value': value * STAGE_PROBABILITY.get(stage, 0),
            'contact': contact,
            'company': contact.get('company', ''),
            'stage': stage,
            'probability': STAGE_PROBABILITY.get(stage, 0),
            'created_at': datetime.now().isoformat(),
            'expected_close': None,
            'notes': notes,
            'tags': [],
            'activities': [],
            'tasks': [],
            'owner': None,
        }
        
        self.deals[deal_id] = deal
        self._log_activity(deal_id, 'created', f'Deal created at stage: {stage}')
        return deal_id
    
    def update_stage(self, deal_id: str, new_stage: str, reason: str = ""):
        """Move deal to a new stage and update weighted value."""
        if deal_id not in self.deals:
            return False
        
        old_stage = self.deals[deal_id]['stage']
        self.deals[deal_id]['stage'] = new_stage
        self.deals[deal_id]['probability'] = STAGE_PROBABILITY.get(new_stage, 0)
        self.deals[deal_id]['weighted_value'] = self.deals[deal_id]['value'] * self.deals[deal_id]['probability']
        
        self._log_activity(deal_id, 'stage_change', 
                          f'{old_stage} → {new_stage}: {reason}')
        return True
    
    def add_activity(self, deal_id: str, activity_type: str, description: str):
        """Log an activity (call, email, meeting) on a deal."""
        if deal_id in self.deals:
            self._log_activity(deal_id, activity_type, description)
    
    def _log_activity(self, deal_id: str, activity_type: str, description: str):
        self.deals[deal_id]['activities'].append({
            'timestamp': datetime.now().isoformat(),
            'type': activity_type,
            'description': description,
        })
    
    def get_pipeline_metrics(self) -> Dict:
        """Calculate key pipeline metrics."""
        total_value = 0
        weighted_value = 0
        stage_counts = {s: 0 for s in self.stages}
        
        for deal in self.deals.values():
            if deal['stage'] != 'closed_lost' and deal['stage'] != 'closed_won':
                total_value += deal['value']
                weighted_value += deal['weighted_value']
            if deal['stage'] in stage_counts:
                stage_counts[deal['stage']] += 1
        
        # Velocity (avg days from lead to proposal)
        velocities = []
        for deal in self.deals.values():
            if deal['stage'] in ('proposal', 'negotiation', 'closed_won'):
                created = datetime.fromisoformat(deal['created_at'])
                # Find when it hit proposal stage
                for activity in deal['activities']:
                    if activity['type'] == 'stage_change' and 'lead → proposal' in activity['description']:
                        proposal_time = datetime.fromisoformat(activity['timestamp'])
                        velocities.append((proposal_time - created).days)
        
        avg_velocity = sum(velocities) / len(velocities) if velocities else 0
        
        return {
            'total_pipeline_value': total_value,
            'weighted_pipeline_value': weighted_value,
            'deal_count': len(self.deals),
            'active_deals': sum(1 for d in self.deals.values() 
                              if d['stage'] not in ('closed_won', 'closed_lost')),
            'stage_distribution': stage_counts,
            'avg_velocity_days': round(avg_velocity, 1),
            'conversion_rate': self._calculate_conversion(),
        }
    
    def _calculate_conversion(self) -> float:
        """Calculate lead-to-close conversion rate."""
        won = sum(1 for d in self.deals.values() if d['stage'] == 'closed_won')
        lost = sum(1 for d in self.deals.values() if d['stage'] == 'closed_lost')
        total_closed = won + lost
        return won / total_closed if total_closed > 0 else 0
    
    def get_stuck_deals(self, days_in_stage=14) -> List[Dict]:
        """Find deals that haven't moved stages recently."""
        stuck = []
        now = datetime.now()
        
        for deal in self.deals.values():
            if deal['stage'] in ('closed_won', 'closed_lost'):
                continue
            
            # Find last stage change
            last_change = None
            for activity in reversed(deal['activities']):
                if activity['type'] == 'stage_change':
                    last_change = datetime.fromisoformat(activity['timestamp'])
                    break
            
            if last_change and (now - last_change).days >= days_in_stage:
                stuck.append({
                    'deal_id': deal['id'],
                    'name': deal['name'],
                    'stage': deal['stage'],
                    'days_stuck': (now - last_change).days,
                    'value': deal['value'],
                })
        
        return sorted(stuck, key=lambda x: x['days_stuck'], reverse=True)
    
    def create_task(self, deal_id: str, task_name: str, 
                    due_date: str, assigned_to: str):
        """Create a task associated with a deal."""
        if deal_id in self.deals:
            task = {
                'id': str(uuid.uuid4())[:8],
                'name': task_name,
                'due_date': due_date,
                'assigned_to': assigned_to,
                'completed': False,
                'created_at': datetime.now().isoformat(),
            }
            self.deals[deal_id]['tasks'].append(task)
            return task['id']
        return None
```

## Forecasting

```python
class SalesForecast:
    """Forecast future revenue based on pipeline."""
    
    @staticmethod
    def forecast(pipeline: SalesPipeline, months_ahead: int = 3) -> Dict:
        """Generate revenue forecast from pipeline."""
        monthly_forecast = {m: 0 for m in range(1, months_ahead + 1)}
        
        for deal in pipeline.deals.values():
            if deal['stage'] in ('closed_won', 'closed_lost'):
                continue
            
            expected_close = deal.get('expected_close')
            if not expected_close:
                continue
            
            close_date = datetime.fromisoformat(expected_close)
            month = close_date.month - datetime.now().month + 1
            
            if 1 <= month <= months_ahead:
                monthly_forecast[month] += deal['weighted_value']
        
        total = sum(monthly_forecast.values())
        return {
            'monthly_forecast': monthly_forecast,
            'total_forecast': total,
            'confidence': 'high' if total > 0 and pipeline._calculate_conversion() > 0.3 else 'medium',
        }
```

## Common Pitfalls

1. **Stale pipeline** — deals that should be closed-lost stay in pipeline; set inactivity alerts
2. **Over-optimistic probability** — every deal is "50% likely"; use data-driven stage probabilities
3. **No lead source tracking** — can't optimize spend; tag every deal with source
4. **Manual data entry burden** — reps avoid CRM if it's tedious; integrate with email and calendar
5. **Stage definition disputes** — sales and marketing disagree on MQL vs SQL; document clear criteria
6. **Pipeline ≠ forecast** — pipeline shows all deals; forecast should use weighted values and historical conversion

## Verification Checklist

- [ ] Pipeline stages defined with clear entry/exit criteria
- [ ] Deal source tracked for every entry
- [ ] Probability per stage reflects historical data
- [ ] Pipeline velocity tracked (avg days per stage)
- [ ] Stuck deal alerts configured (e.g., 14 days without movement)
- [ ] Forecast based on weighted pipeline, not raw pipeline
- [ ] Integration with email/calendar for auto-logging
- [ ] Conversion rate by source, owner, and deal size available

## See Also

- real-estate-crm-leads — real estate specific CRM
- email-marketing-campaigns — email sequences for sales
- business-metrics-kpis — tracking sales metrics
- customer-segmentation-analysis — segmenting the pipeline
