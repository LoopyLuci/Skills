---
name: quarterly-business-review
description: "Use when conducting quarterly business reviews."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [QBR, business-review, performance-review, account-review, stakeholder-meeting]
    related_skills: [board-presentation-deck, business-metrics-kpis, customer-journey-mapping, sales-forecasting-advanced]
---

# Quarterly Business Reviews (QBR)

Conducting effective quarterly business reviews — from QBR structure and prep through data analysis, stakeholder alignment, and action planning.

## When to Use

- Reviewing business performance with stakeholders (customers, execs, board)
- Conducting account-level QBRs with strategic customers
- Preparing QBR presentations and materials
- Driving alignment on priorities and goals
- Turning QBR insights into action items

## QBR Structure

```python
QBR_AGENDA = {
    'executive_summary': 'Highlights, lowlights, key metrics (5 min)',
    'metrics_review': 'Revenue, usage, adoption, NPS, support (15 min)',
    'goals_progress': 'OKR progress, milestones, wins vs gaps (10 min)',
    'strategic_items': 'Key initiatives, product roadmap, partnership (10 min)',
    'risks_and_concerns': 'Open issues, churn signals, competitive threats (5 min)',
    'action_items': 'Priorities for next quarter, owners, deadlines (5 min)',
}

class QBR:
    """Prepare and structure a Quarterly Business Review."""
    def __init__(self, customer: str, quarter: str, year: int):
        self.customer = customer
        self.quarter = quarter
        self.year = year
        self.sections = []
    
    def add_metrics(self, metrics: Dict):
        self.sections.append({
            'title': 'Performance Metrics',
            'metrics': metrics,
        })
    
    def add_action_items(self, items: List[Dict]):
        self.sections.append({
            'title': 'Action Items',
            'items': [f"{i['owner']}: {i['action']} by {i['deadline']}" for i in items],
        })
    
    def generate_agenda(self) -> str:
        return f"📋 QBR: {self.customer} — Q{self.quarter} {self.year}\n" + "=" * 50 + "\n" + "\n".join(f"{k}: {v}" for k, v in QBR_AGENDA.items())
```

## Common Pitfalls

1. **No prep** — showing up without reviewing prior QBR action items wastes everyone's time
2. **Too much data** — 50 slides of charts with no narrative; tell the story
3. **Hiding bad news** — QBR is for honest assessment; hiding issues prevents getting help
4. **No action items** — great meeting with no follow-up; conclude with owners and deadlines
5. **Inconsistent cadence** — skipping QBRs or inconsistent format erodes their value

## Verification Checklist

- [ ] Prior QBR action items reviewed and status updated
- [ ] Customer/stakeholder goals clearly stated
- [ ] Performance metrics vs targets shown
- [ ] Issues and risks presented transparently
- [ ] Action items with owners and deadlines
- [ ] QBR materials sent 48 hours in advance
- [ ] Feedback collected on QBR format and content
- [ ] Post-QBR summary sent within 24 hours
