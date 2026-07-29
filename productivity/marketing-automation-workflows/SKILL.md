---
name: marketing-automation-workflows
description: "Use when building marketing automation systems and flows."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [marketing-automation, workflows, triggers, email-automation, CRM-automation]
    related_skills: [email-marketing-campaigns, crm-sales-pipeline, marketing-funnel-design, list-building-email-growth]
---

# Marketing Automation Workflows

Building automated marketing workflows that nurture leads, engage customers, and drive conversions — from trigger-based email sequences through multi-step automation and lead scoring.

## When to Use

- Automating repetitive marketing tasks (follow-ups, assignments, notifications)
- Building multi-step email automation sequences
- Implementing lead scoring and routing
- Creating behavior-triggered marketing campaigns
- Integrating marketing automation with CRM

## Workflow Engine

```python
from typing import Dict, List, Optional, Callable
from datetime import datetime, timedelta
import json
import uuid

class WorkflowTrigger:
    """Define what starts a workflow."""
    
    TYPES = {
        'form_submission': 'User submits a form',
        'page_visit': 'User visits a specific page',
        'email_click': 'User clicks a link in an email',
        'email_open': 'User opens an email',
        'purchase': 'User makes a purchase',
        'lead_created': 'New lead enters the system',
        'lead_stage_change': 'Lead moves to a new stage',
        'date_based': 'Specific date or anniversary',
        'tag_added': 'Tag is applied to a contact',
        'score_threshold': 'Lead score reaches a threshold',
    }

class AutomationWorkflow:
    """Design multi-step automation workflows."""
    
    def __init__(self, name: str, trigger_type: str, trigger_config: Dict):
        self.name = name
        self.trigger = {'type': trigger_type, 'config': trigger_config}
        self.steps = []
        self.goals = []
    
    def add_step(self, action_type: str, config: Dict,
                 delay_hours: int = 0, condition: Dict = None) -> 'AutomationWorkflow':
        """Add a step to the workflow."""
        step_id = str(uuid.uuid4())[:8]
        self.steps.append({
            'id': step_id,
            'action': action_type,
            'config': config,
            'delay': delay_hours,
            'condition': condition,
        })
        return self
    
    def add_goal(self, description: str, metric: str, target: float):
        """Add a measurable goal for this workflow."""
        self.goals.append({
            'description': description,
            'metric': metric,
            'target': target,
        })
```

## Common Workflow Templates

```python
WORKFLOW_TEMPLATES = {
    'welcome_series': {
        'name': 'Welcome Series',
        'trigger': 'form_submission',
        'steps': [
            {'action': 'send_email', 'delay': 0, 'template': 'welcome_email'},
            {'action': 'add_tag', 'delay': 0, 'tag': 'new_subscriber'},
            {'action': 'wait', 'delay': 24, 'description': 'Wait 24 hours'},
            {'action': 'send_email', 'delay': 0, 'template': 'day_1_nurture'},
            {'action': 'update_score', 'delay': 0, 'points': 5},
            {'action': 'wait', 'delay': 72, 'description': 'Wait 3 days'},
            {'action': 'send_email', 'delay': 0, 'template': 'day_4_offer'},
            {'action': 'condition', 'delay': 0, 
             'if': 'clicked_last_email', 'then': 'move_to_hot_lead'},
        ],
    },
    'abandoned_cart': {
        'name': 'Abandoned Cart Recovery',
        'trigger': 'cart_abandoned',
        'steps': [
            {'action': 'wait', 'delay': 1, 'description': 'Wait 1 hour'},
            {'action': 'send_email', 'delay': 0, 'template': 'cart_reminder_1'},
            {'action': 'wait', 'delay': 24, 'description': 'Wait 24 hours'},
            {'action': 'send_email', 'delay': 0, 'template': 'cart_reminder_2'},
            {'action': 'wait', 'delay': 48, 'description': 'Wait 48 hours'},
            {'action': 'send_email', 'delay': 0, 'template': 'cart_reminder_3'},
        ],
    },
    'lead_reattempt': {
        'name': 'Lead Re-engagement',
        'trigger': 'lead_stage_change',
        'trigger_config': {'stage': 'lost'},
        'steps': [
            {'action': 'wait', 'delay': 720, 'description': 'Wait 30 days'},
            {'action': 'send_email', 'delay': 0, 'template': 'we_miss_you'},
            {'action': 'condition', 'delay': 0,
             'if': 'opened_last_email', 'then': 'move_to_reactivated'},
            {'action': 'wait', 'delay': 720, 'description': 'Wait 30 days'},
            {'action': 'send_email', 'delay': 0, 'template': 'final_offer'},
            {'action': 'condition', 'delay': 0,
             'if': 'no_engagement', 'then': 'mark_as_inactive'},
        ],
    },
    'post_purchase': {
        'name': 'Post-Purchase Follow-up',
        'trigger': 'purchase',
        'steps': [
            {'action': 'send_email', 'delay': 0, 'template': 'order_confirmation'},
            {'action': 'wait', 'delay': 24, 'description': 'Wait 1 day'},
            {'action': 'send_email', 'delay': 0, 'template': 'shipping_update'},
            {'action': 'wait', 'delay': 168, 'description': 'Wait 7 days'},
            {'action': 'send_email', 'delay': 0, 'template': 'feedback_request'},
            {'action': 'add_tag', 'delay': 0, 'tag': 'customer'},
        ],
    },
}

def get_workflow_template(name: str) -> Dict:
    return WORKFLOW_TEMPLATES.get(name, WORKFLOW_TEMPLATES['welcome_series'])
```

## Lead Scoring

```python
class LeadScoringModel:
    """Define and calculate lead scores based on behavior."""
    
    POSITIVE_SIGNALS = {
        'email_open': 5,
        'email_click': 10,
        'page_visit': 3,
        'form_submit': 15,
        'demo_request': 30,
        'pricing_page': 20,
        'case_study_view': 10,
        'trial_start': 25,
        'webinar_attend': 20,
        'content_download': 8,
    }
    
    NEGATIVE_SIGNALS = {
        'email_unsubscribe': -50,
        'bounce': -20,
        'spam_complaint': -100,
        'job_change': -10,
    }
    
    @staticmethod
    def calculate_score(contact_events: List[Dict]) -> Dict:
        score = 0
        breakdown = []
        
        for event in contact_events:
            event_type = event.get('type', '')
            if event_type in LeadScoringModel.POSITIVE_SIGNALS:
                points = LeadScoringModel.POSITIVE_SIGNALS[event_type]
                score += points
                breakdown.append(f"+{points}: {event_type}")
            elif event_type in LeadScoringModel.NEGATIVE_SIGNALS:
                points = LeadScoringModel.NEGATIVE_SIGNALS[event_type]
                score += points
                breakdown.append(f"{points}: {event_type}")
        
        return {
            'total_score': score,
            'breakdown': breakdown,
            'rating': 'hot' if score >= 80 else 'warm' if score >= 40 else 'cold',
        }
```

## Common Pitfalls

1. **Over-automating** — not every touchpoint needs automation; personalize where it matters
2. **No testing** — automated workflows with broken links or typos go out to thousands
3. **Trigger stacking** — multiple automations triggered simultaneously confuse the contact
4. **Ignoring unengaged contacts** — sending to unengaged contacts hurts deliverability
5. **Too aggressive timing** — 5 emails in 2 days feels spammy; space them out appropriately
6. **No exit conditions** — workflows should remove contacts who convert or opt out

## Verification Checklist

- [ ] Workflow triggers clearly defined
- [ ] Steps include appropriate delays between actions
- [ ] Conditional branching configured (if/else paths)
- [ ] Lead scoring model defined (positive and negative signals)
- [ ] Exit conditions set (unsubscribe, conversion)
- [ ] Workflow tested with test contacts before going live
- [ ] Performance monitored (completion rate, conversion rate)
- [ ] Integration with CRM verified

## See Also

- email-marketing-campaigns — email sequences within workflows
- crm-sales-pipeline — lead routing and CRM integration
- marketing-funnel-design — workflow stages aligned with funnel
- list-building-email-growth — feeding leads into workflows
